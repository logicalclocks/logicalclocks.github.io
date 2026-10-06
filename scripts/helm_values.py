import base64
import io
import json
import re
import tarfile
import tempfile
import textwrap
import urllib.error
import urllib.request
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Annotated

import typer
import yaml
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from packaging.version import InvalidVersion, Version


_DEFAULT_PAGES_DIR = (
    _DOCS_ROOT / "docs" / "setup_installation" / "common" / "helm_chart_values"
)
_INDEX = "index.md"
_GLOBAL = "global"
_VALUES_HEADING = "\n## Values\n"
_BEGIN = "<!-- BEGIN GENERATED VALUES -->"
_END = "<!-- END GENERATED VALUES -->"
# What the committed pages hold between the markers (see reset_helm_values).
_PLACEHOLDER = "_The values table is generated from the Hopsworks Helm chart during the documentation build._"
_INDEX_PLACEHOLDER = (
    "_The values tables are generated from the Hopsworks Helm chart during the documentation build._\n"
    "_To preview them locally, run `uv run --extra cli hopsworks-docs gen-helm-values --chart <path-to-hopsworks-helm>`,"
    " and `uv run hopsworks-docs reset-helm-values` before committing._"
)

# Test-harness settings (loadtest credentials and the like), not deployment
# configuration.
_EXCLUDED_PREFIXES = ("hopsworks.tests.",)
# Longer defaults (whole subchart overrides as one-line JSON) are shown as a
# collapsed YAML block instead.
_MAX_INLINE_DEFAULT = 80
# Smaller groups of keys are merged into the page's "General" section, so the
# table of contents is not a list of one-row sections.
_MIN_SECTION_ROWS = 5

# Docs of the upstream charts the subcharts install, keyed by Helm repository
# URL without its trailing slash. Artifact Hub where the chart is listed,
# otherwise the chart README at its release tag.
_UPSTREAM_DOCS = {
    "https://helm.releases.hashicorp.com": "https://artifacthub.io/packages/helm/hashicorp/{name}/{version}",
    "https://grafana.github.io/helm-charts": "https://artifacthub.io/packages/helm/grafana/{name}/{version}",
    "https://prometheus-community.github.io/helm-charts": "https://artifacthub.io/packages/helm/prometheus-community/{name}/{version}",
    "https://strimzi.io/charts": "https://artifacthub.io/packages/helm/strimzi/{name}/{version}",
    "https://ray-project.github.io/kuberay-helm": "https://artifacthub.io/packages/helm/kuberay-operator/{name}/{version}",
    "https://trinodb.github.io/charts": "https://artifacthub.io/packages/helm/trino/{name}/{version}",
    "https://apache.github.io/superset": "https://artifacthub.io/packages/helm/superset/{name}/{version}",
    "oci://registry-1.docker.io/bitnamicharts": "https://artifacthub.io/packages/helm/bitnami/{name}/{version}",
    "https://kubeflow.github.io/spark-operator": "https://github.com/kubeflow/spark-operator/blob/v{version}/charts/spark-operator-chart/README.md",
    "https://repo.hops.works/master/kueue": "https://github.com/kubernetes-sigs/kueue/blob/v{version}/charts/kueue/README.md",
    "https://logicalclocks.github.io/rondb-helm": "https://github.com/logicalclocks/rondb-helm/blob/v{version}/values.schema.json",
}
# Upstream charts whose values.schema.json is rendered on the subchart page,
# keyed by subchart. docs.hopsworks.ai/rondb-helm/ shows whichever version was
# published last, not the one this chart pins.
_RENDERED_SCHEMAS = {"rondb": "rondb"}
# Top-level keys listed under "Other values" on the index by design: the
# library chart has a single override knob.
_NO_PAGE = {"hopsworkslib"}
# Values a typical install sets, taken from the example values files of the
# AWS, Azure and GCP setup guides, with what each one decides.
_COMMON_VALUES = (
    (
        "global._hopsworks.cloudProvider",
        "The cloud the cluster runs on; HopsFS, Consul and Hopsworks configure themselves from it.",
    ),
    (
        "global._hopsworks.storageClassName",
        "The storage class of every persistent volume.",
    ),
    (
        "global._hopsworks.imageRegistry",
        "The registry the Hopsworks images are pulled from.",
    ),
    ("global._hopsworks.imagePullSecrets", "The pull secrets for that registry."),
    (
        "global._hopsworks.managedDockerRegistery",
        "Use the cloud provider's container registry for the images Hopsworks builds for users.",
    ),
    (
        "global._hopsworks.managedObjectStorage",
        "Use a cloud bucket for HopsFS data and for the RonDB and OpenSearch backups.",
    ),
    (
        "global._hopsworks.minio.enabled",
        "Deploy MinIO in the cluster; turn it off when a cloud bucket is used.",
    ),
    (
        "global._hopsworks.externalLoadBalancers.enabled",
        "Expose services through LoadBalancer Services.",
    ),
    ("hopsworks.ingress.host", "The host name of the Hopsworks UI and API."),
    ("hopsworks.ingress.ingressClassName", "The ingress controller that serves it."),
    (
        "hopsworks.velero.backup.enabled",
        "Back up Kubernetes resources with Velero, which needs its own install.",
    ),
    (
        "rondb.rondb.clusterSize",
        "The size of the RonDB cluster: data replicas, node groups, MySQL and REST API servers.",
    ),
)
# Marks a default that is prose rather than a value (see _default_value).
_PROSE = object()
# Marks a schema key without a default, or a key no override mentions.
_ABSENT = object()

# Inline code spans and genuine external links are kept verbatim; everything
# else has its square brackets escaped (see _neutralize_markdown_refs). The link
# pattern is single-line (no newlines in the text or URL) so it cannot swallow
# whole table rows when a description's URL has no closing paren on its line.
_CODE_SPAN = re.compile(r"`[^`]*`")
_EXTERNAL_LINK = re.compile(r"\[[^\]\n]+\]\(https?://[^)\s]+\)")
# Private-use code points that cannot occur in the README, used to stash the
# protected spans while brackets are escaped.
_HOLD_OPEN = chr(0xE000)
_HOLD_CLOSE = chr(0xE001)
_HOLD_RE = re.compile(re.escape(_HOLD_OPEN) + r"(\d+)" + re.escape(_HOLD_CLOSE))
# The site has no magiclink extension, so a bare URL in a description renders
# as plain text until it is wrapped as a Markdown autolink.
_BARE_URL = re.compile(r"(?<![<\w])https?://[^\s<>`]+")
_LINK_OR_CODE = re.compile(f"({_CODE_SPAN.pattern}|{_EXTERNAL_LINK.pattern})")
_URL_TRAILER = ".,;:!?'\""

# A helm-docs values row: | key | type | default | description |. The default
# is matched first as a whole code span because it can contain " | " itself
# (a shell command, a JSON object).
_ROW = re.compile(
    r"\| (?P<key>\S+) \| (?P<type>.*?) \| (?P<default>`.*?`|.*?) \| (?P<description>.*?) ?\|"
)
_TABLE_RULE = re.compile(r"\|[-:| ]+\|")
# Keys quote segments that contain dots: annotations."prometheus.io/path".
_KEY_SEGMENT = re.compile(r'"[^"]*"|[^.]+')
_LIST_INDEX = re.compile(r"\[\d+\]$")
# Any list index in a key: [3] in a README key, [] in a schema array-item key.
_LIST_INDEX_ANY = re.compile(r"\[(\d*)\]")


@dataclass(frozen=True)
class _Row:
    key: str
    type_: str
    default: str
    description: str
    # Extra facts for the entry's first line: schema constraints, overrides.
    notes: tuple[str, ...] = ()


def _neutralize_markdown_refs(text: str) -> str:
    """Escape bracket-based link/reference syntax in helm-docs descriptions.

    helm-docs descriptions occasionally contain Markdown links to relative
    paths (e.g. ``[values.yaml](./values.yaml)``) or reference-style brackets
    (e.g. ``key[=value][:effect]``). mkdocs treats the former as broken doc
    links and mkdocs-autorefs treats the latter as unresolved cross-references,
    both of which fail the strict build. Escape square brackets so they render
    as literal text, while leaving inline code spans (the default values) and
    genuine ``http(s)`` links untouched.
    """
    stash: list[str] = []

    def _hold(match: re.Match) -> str:
        stash.append(match.group(0))
        return f"{_HOLD_OPEN}{len(stash) - 1}{_HOLD_CLOSE}"

    text = _CODE_SPAN.sub(_hold, text)
    text = _EXTERNAL_LINK.sub(_hold, text)
    text = text.replace("[", "\\[").replace("]", "\\]")

    # Un-stash iteratively: a stashed span can itself contain sentinels for
    # other stashed spans, which a single pass would leave unresolved and leak
    # the literal private-use characters into the page. An index that was never
    # stashed (a stray sentinel already in the README) degrades to literal text
    # rather than crashing, matching the module's graceful-degradation contract.
    def _restore(m: re.Match) -> str:
        idx = int(m.group(1))
        return stash[idx] if idx < len(stash) else m.group(0)

    while _HOLD_RE.search(text):
        new = _HOLD_RE.sub(_restore, text)
        if new == text:  # nothing resolvable left; avoid an infinite loop
            break
        text = new
    return text


def _wrap_url(match: re.Match) -> str:
    url = match.group(0).rstrip(_URL_TRAILER)
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1].rstrip(_URL_TRAILER)
    return f"<{url}>{match.group(0)[len(url) :]}"


def _autolink(text: str) -> str:
    """Wrap bare URLs as ``<url>``, leaving code spans and Markdown links alone.

    Trailing punctuation and an unbalanced closing parenthesis stay outside
    the link: "(see https://x/y)." links ``https://x/y``.
    """
    parts = _LINK_OR_CODE.split(text)
    # re.split puts the captured code spans and links at the odd indices.
    for i in range(0, len(parts), 2):
        parts[i] = _BARE_URL.sub(_wrap_url, parts[i])
    return "".join(parts)


def _http_get(url: str, username: str, password: str) -> bytes:
    """GET a URL, optionally with HTTP basic auth. Fail loudly on errors."""
    request = urllib.request.Request(url)
    if username:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        request.add_header("Authorization", f"Basic {token}")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            return response.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        typer.echo(f"ERROR: failed to fetch {url}: {exc}", err=True)
        raise typer.Exit(1) from exc


def _select_chart(entries: list[dict], chart_version: str | None) -> dict | None:
    """Pick the chart entry to document from a Helm repo index.

    With ``chart_version`` (release docs), keep entries whose chart ``version``
    is that major.minor (or an exact match) and pick the highest patch by
    semver. Without it (dev docs), pick the most recently published entry by the
    index ``created`` timestamp -- dev charts are time-stamped pre-releases, so
    newest-published is the latest dev build.
    """
    if not chart_version:
        return (
            max(entries, key=lambda e: str(e.get("created", ""))) if entries else None
        )

    candidates = [
        e
        for e in entries
        if str(e.get("version", "")) == chart_version
        or str(e.get("version", "")).startswith(f"{chart_version}.")
    ]
    if not candidates:
        return None

    def _parse(entry: dict) -> Version | None:
        try:
            return Version(str(entry.get("version", "")))
        except InvalidVersion:
            return None

    parseable = [(e, v) for e in candidates if (v := _parse(e)) is not None]
    if parseable:
        return max(parseable, key=lambda pair: pair[1])[0]
    # Fall back to newest-published if none of the versions are valid semver.
    return max(candidates, key=lambda e: str(e.get("created", "")))


def _archive_from_registry(
    repo_url: str, chart_version: str | None, username: str, password: str
) -> bytes | None:
    """Resolve a chart in a Helm (Nexus) repo and return its package archive.

    Returns None (and warns) if nothing suitable is found, so the build keeps
    the page placeholders instead of failing.
    """
    base = repo_url.rstrip("/")
    # `or {}` guards an empty/invalid index.yaml (safe_load returns None) so a
    # bad response keeps the placeholder rather than raising AttributeError.
    index = yaml.safe_load(_http_get(f"{base}/index.yaml", username, password)) or {}
    entries = (index.get("entries") or {}).get("hopsworks") or []

    chosen = _select_chart(entries, chart_version)
    if chosen is None:
        typer.echo(
            f"WARNING: no chart in {base} matches version "
            f"'{chart_version or 'any'}'; leaving the page placeholders.",
            err=True,
        )
        return None

    urls = chosen.get("urls") or []
    if not urls:
        typer.echo(
            f"WARNING: chart {chosen.get('version')} has no download URL; "
            "leaving the page placeholders.",
            err=True,
        )
        return None

    url = urls[0]
    if not url.startswith(("http://", "https://")):
        url = f"{base}/{url.lstrip('/')}"
    typer.echo(
        f"Using chart {chosen.get('version')} "
        f"(appVersion {chosen.get('appVersion')}) from {base}"
    )
    return _http_get(url, username, password)


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _segments(key: str) -> list[str]:
    return _KEY_SEGMENT.findall(key)


def _parse_rows(values_section: str, prefix: str = "") -> list[_Row]:
    """Parse a helm-docs values table, with ``prefix`` put before every key.

    Only table lines are read: a README rendered from helm-docs' default
    template carries a footer after the table. Exits with an error if a table
    line does not parse: a page silently missing values is worse than a build
    failure that names the row.
    """
    rows = []
    unparsed = []
    for line in values_section.splitlines():
        line = line.strip()
        is_header = line.startswith("| Key |") or _TABLE_RULE.fullmatch(line)
        if not line.startswith("|") or is_header:
            continue
        match = _ROW.fullmatch(line)
        if match is None:
            unparsed.append(line)
            continue
        key, type_, default, description = match.groups()
        rows.append(_Row(prefix + key, type_, default, description))
    if unparsed:
        for line in unparsed:
            typer.echo(f"ERROR: unparseable values row: {line}", err=True)
        typer.echo(
            "ERROR: the chart README values table no longer matches the "
            "helm-docs layout this generator reads (| key | type | default | "
            "description |).",
            err=True,
        )
        raise typer.Exit(1)
    return rows


def _resolve_ref(node: dict, defs: dict) -> dict:
    ref = node.get("$ref", "")
    if not ref.startswith("#/$defs/"):
        return node
    siblings = {k: v for k, v in node.items() if k != "$ref"}
    return {**defs[ref.removeprefix("#/$defs/")], **siblings}


def _helm_merge(base: dict, override: dict) -> dict:
    """Coalesce two layers of Helm values the way Helm does.

    Maps merge key by key, any other value (lists included) replaces the base
    one, and a null removes the key; it is kept here as None, which is what
    the chart's templates then see.
    """
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _helm_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _json_code(value: object) -> str:
    return f"`{json.dumps(value, separators=(',', ':'))}`"


def _override_note(chart_default: object, chart: str) -> str:
    if chart_default is _ABSENT:
        return f"set by Hopsworks, the `{chart}` chart has no default"
    if len(_json_code(chart_default)) > _MAX_INLINE_DEFAULT:
        return f"Hopsworks overrides the `{chart}` chart default"
    return (
        f"Hopsworks overrides the `{chart}` chart default {_json_code(chart_default)}"
    )


def _constraints(node: dict) -> tuple[str, ...]:
    # `required` is left out: it means "present when the parent object is",
    # which the defaults already satisfy, so it would read as "you must set it".
    notes = [
        f"{word} {_json_code(node[word])}"
        for word in ("minimum", "maximum")
        if word in node
    ]
    if "pattern" in node:
        notes.append(f"pattern `{node['pattern']}`")
    examples = node.get("examples") or ([node["example"]] if "example" in node else [])
    if examples:
        notes.append(f"example {_json_code(examples[0])}")
    return tuple(notes)


def _schema_rows(
    schema: dict, prefix: str, overrides: dict | None = None, chart: str = ""
) -> list[_Row]:
    """Flatten a values.schema.json into rows keyed under ``prefix``.

    ``overrides`` are the values the parent chart sets for this one; their
    effect replaces the schema default, and the entry names the ``chart``'s
    own default. Overrides under array items are not applied. Array item
    properties are listed as ``key[].field``. Only local ``#/$defs/``
    references are resolved.
    """
    defs = schema.get("$defs") or {}
    rows: list[_Row] = []

    def _walk(node: dict, path: str, override: object) -> None:
        for name, child in (node.get("properties") or {}).items():
            child = _resolve_ref(child, defs)
            key = f"{path}.{name}"
            type_ = child.get("type", "")
            description = " ".join(str(child.get("description", "")).split())
            if "enum" in child:
                type_ = "enum"
                allowed = ", ".join(f"`{json.dumps(v)}`" for v in child["enum"])
                description = f"{description} One of: {allowed}.".strip()
            if isinstance(type_, list):
                type_ = "|".join(type_)
            value = child.get("default", _ABSENT)
            notes: tuple[str, ...] = ()
            child_override = (
                override.get(name, _ABSENT) if isinstance(override, dict) else _ABSENT
            )
            # A map override on an object with declared properties lands on
            # the child entries instead.
            if child_override is not _ABSENT and not (
                child.get("properties") and isinstance(child_override, dict)
            ):
                effective = child_override
                if isinstance(child_override, dict) and isinstance(value, dict):
                    effective = _helm_merge(value, child_override)
                if effective != value:
                    notes = (_override_note(value, chart),)
                    value = effective
            default = "" if value is _ABSENT else _json_code(value)
            notes += _constraints(child)
            rows.append(_Row(key, type_, default, description, notes))
            _walk(child, key, child_override)
            if isinstance(child.get("items"), dict):
                _walk(_resolve_ref(child["items"], defs), f"{key}[]", _ABSENT)

    _walk(schema, prefix, overrides or {})
    return rows


def _undeclared_overrides(schema: dict, overrides: dict, prefix: str) -> list[str]:
    """Return the override keys the schema does not declare.

    Below a free-form map (an object without declared properties) any key is
    accepted. An undeclared key is usually an override the chart has renamed
    or dropped, which then silently stops applying.
    """
    defs = schema.get("$defs") or {}
    found: list[str] = []

    def _walk(node: dict, override: object, path: str) -> None:
        properties = node.get("properties")
        if not properties or not isinstance(override, dict):
            return
        for name, value in override.items():
            if name in properties:
                _walk(_resolve_ref(properties[name], defs), value, f"{path}.{name}")
            else:
                found.append(f"{path}.{name}")

    _walk(schema, overrides, prefix)
    return found


def _dependency_schema(subchart: Path, name: str, version: str) -> dict | None:
    """Return the values.schema.json of a subchart's vendored dependency.

    A packaged chart has the dependency unpacked under ``charts/<name>/``; a
    local checkout has the ``<name>-<version>.tgz`` archive ``helm dependency
    build`` downloads for the pinned version. None when neither is present.
    """
    unpacked = subchart / "charts" / name / "values.schema.json"
    if unpacked.is_file():
        return json.loads(unpacked.read_text(encoding="utf-8"))
    archive = subchart / "charts" / f"{name}-{version}.tgz"
    if not archive.is_file():
        return None
    with tarfile.open(archive, mode="r:gz") as tar:
        try:
            member = tar.extractfile(f"{name}/values.schema.json")
        except KeyError:
            return None
        return json.load(member) if member is not None else None


class _BlockDumper(yaml.SafeDumper):
    """Dump multi-line strings (embedded config files) as ``|`` blocks."""


def _represent_str(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_BlockDumper.add_representer(str, _represent_str)


def _dump_yaml(value: object) -> str:
    dumped = yaml.dump(
        value, Dumper=_BlockDumper, sort_keys=False, allow_unicode=True, width=1000
    ).rstrip()
    # A lone plain scalar is followed by the "..." document end marker.
    return dumped.removesuffix("\n...")


def _default_value(default: str) -> object:
    """Parse a rendered default back into its value.

    Returns ``_PROSE`` for a default that is not JSON, such as a helm-docs
    ``@default`` text ("check values.yaml").
    """
    raw = (
        default[1:-1] if default.startswith("`") and default.endswith("`") else default
    )
    if raw == "nil":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return _PROSE


def _default_block(row: _Row) -> str:
    value = _default_value(row.default)
    # YAML for every parsed value: a string default such as '["/bin/bash", …]'
    # keeps its quotes, so it is not copied into a values file as a list.
    if value is _PROSE:
        lang, body = "text", row.default.strip("`")
    else:
        lang, body = "yaml", _dump_yaml(value)
    fence = textwrap.indent(f"```{lang}\n{body}\n```", "    ")
    return f'??? note "Default"\n\n{fence}'


def _anchor(key: str) -> str:
    """Return the HTML id of a key's entry: ``helm.`` plus the key, URL-safe."""
    path = _LIST_INDEX_ANY.sub(lambda m: f".{m.group(1)}" if m.group(1) else "", key)
    return "helm." + re.sub(r"[^A-Za-z0-9._-]+", "-", path.replace('"', ""))


def _is_deprecated(row: _Row) -> bool:
    return re.match(r"\s*deprecated\b", row.description, re.IGNORECASE) is not None


def _render_entries(rows: list[_Row]) -> str:
    # A definition list, not a table: a code chip in a table cell never wraps
    # (design-system.md, "Tables"), and keys alone run to 90 characters.
    # .hops-values in docs/css/custom.css gives it the table's density.
    entries = []
    for row in sorted(rows, key=lambda r: (_is_deprecated(r), r.key)):
        anchor = _anchor(row.key)
        term = f"`{row.key}`"
        if _is_deprecated(row):
            term += ' <span class="hops-values-deprecated">Deprecated</span>'
        term += (
            f' <a class="headerlink" href="#{anchor}" title="Permanent link">#</a>'
            f" {{ #{anchor} }}"
        )
        long_default = len(row.default) > _MAX_INLINE_DEFAULT
        facts = [f"Type `{row.type_}`"] if row.type_ else []
        if row.default and not long_default:
            facts.append(f"default {_neutralize_markdown_refs(row.default)}")
        facts += [_neutralize_markdown_refs(note) for note in row.notes]
        lines = [term, f":   {', '.join(facts) or 'Value'}."]
        if row.description:
            description = _autolink(_neutralize_markdown_refs(row.description))
            lines.append(f"    {description}")
        if long_default:
            lines += ["", textwrap.indent(_default_block(row), "    ")]
        entries.append("\n".join(lines))
    body = "\n\n".join(entries)
    return f'<div class="hops-values" markdown>\n\n{body}\n\n</div>'


def _key_path(key: str) -> list[str | int]:
    path: list[str | int] = []
    for segment in _segments(key):
        path.append(_LIST_INDEX_ANY.sub("", segment).strip('"'))
        path += [int(i) for i in _LIST_INDEX_ANY.findall(segment) if i]
    return path


def _set_path(tree: dict, path: list[str | int], value: object) -> None:
    node: object = tree
    for step, next_step in zip(path, path[1:]):
        if isinstance(node, list) and isinstance(step, int):
            node.extend([None] * (step + 1 - len(node)))
            current = node[step]
        elif isinstance(node, dict):
            current = node.get(step)
        else:
            return
        # A parent's scalar or null default gives way to a listed child.
        if not isinstance(current, (dict, list)):
            current = {} if isinstance(next_step, str) else []
            node[step] = current
        node = current
    last = path[-1]
    if isinstance(node, list) and isinstance(last, int):
        node.extend([None] * (last + 1 - len(node)))
        node[last] = value
    elif isinstance(node, dict):
        node[last] = value


def _values_file_block(rows: list[_Row]) -> str | None:
    """Return the rows' defaults nested as in a values file, as a collapsed block.

    Parents are set before their children, so a listed child refines an
    object default and the keys it does not list stay. Array item fields
    (``key[].field``) and prose defaults are left out. None when nothing is
    left.
    """
    tree: dict = {}
    for row in sorted(rows, key=lambda r: len(_key_path(r.key))):
        if "[]" in row.key:
            continue
        value = _default_value(row.default)
        if value is not _PROSE:
            _set_path(tree, _key_path(row.key), value)
    if not tree:
        return None
    fence = textwrap.indent(f"```yaml\n{_dump_yaml(tree)}\n```", "    ")
    return f'??? example "Defaults as YAML"\n\n{fence}'


def _section(key: str, depth: int) -> str | None:
    """Name the group a key belongs to: its first segment below the page.

    ``depth`` is the number of leading segments shared by every key on the
    page; None for a key that is the page's own prefix. Underscore namespaces
    (``global._hopsworks``) are skipped, and list items
    (``wipeWhenUninstall[3]``) group under their list. An object key and its
    children share a group.
    """
    rest = _segments(key)[depth:]
    if len(rest) > 1 and rest[0].startswith("_"):
        rest = rest[1:]
    return _LIST_INDEX.sub("", rest[0]) if rest else None


def _heading(level: str, title: str, anchor: str) -> str:
    # Explicit ids, because mkdocs-autorefs resolves [text][id] site-wide: a
    # generated "## terminal" would make the Terminal guide's anchor ambiguous.
    slug = re.sub(r"[^a-z0-9_-]+", "-", anchor.lower()).strip("-")
    return f"{level} {title} {{ #{slug} }}"


def _section_body(rows: list[_Row]) -> str:
    block = _values_file_block(rows)
    entries = _render_entries(rows)
    return f"{block}\n\n{entries}" if block else entries


def _render_rows(rows: list[_Row], depth: int, level: str, anchor: str) -> str:
    groups: dict[str | None, list[_Row]] = {}
    for row in rows:
        groups.setdefault(_section(row.key, depth), []).append(row)
    sections = sorted(
        (name, group)
        for name, group in groups.items()
        if name is not None and len(group) >= _MIN_SECTION_ROWS
    )
    named = {name for name, _ in sections}
    general = [row for row in rows if _section(row.key, depth) not in named]
    if not sections:
        return _section_body(general)
    parts = []
    if general:
        title = _heading(level, "General", f"{anchor}-general")
        parts.append(f"{title}\n\n{_section_body(general)}")
    for name, group in sections:
        title = _heading(level, name, f"{anchor}-{name}")
        parts.append(f"{title}\n\n{_section_body(group)}")
    return "\n\n".join(parts)


def _key_link(key: str, targets: dict[str, str]) -> str:
    return f"[`{key}`]({targets[key]})" if key in targets else f"`{key}`"


def _condition_text(condition: str | None, targets: dict[str, str]) -> str:
    keys = [p.strip() for p in (condition or "").split(",") if p.strip()]
    paths = [_key_link(key, targets) for key in keys]
    if not paths:
        return "Always deployed."
    if len(paths) == 1:
        return f"Deployed when {paths[0]} is `true`."
    return (
        "Deployed according to the first of these values that is set: "
        f"{', '.join(paths)}."
    )


def _upstream_link(dependency: dict, problems: list[str]) -> str:
    name, version = dependency["name"], str(dependency["version"])
    repository = str(dependency.get("repository", "")).rstrip("/")
    label = f"`{name}` {version}"
    template = _UPSTREAM_DOCS.get(repository)
    if template is None:
        problems.append(f"no docs link for chart {name} from {repository}")
        return label
    return f"[{label}]({template.format(name=name, version=version)})"


def _upstream_admonition(key: str, upstream: list[dict], links: list[str]) -> str:
    lines = [
        f"- Values under `{key}.{dep.get('alias') or dep['name']}` go to "
        f"{link} from `{dep.get('repository')}`."
        for dep, link in zip(upstream, links)
    ]
    body = textwrap.indent("\n".join(lines), "    ")
    return f'!!! info "Upstream charts"\n\n{body}'


def _with_deployed_default(row: _Row, deployed: dict) -> _Row:
    path = [segment.strip('"') for segment in _segments(row.key)[1:]]
    if not path or any("[" in segment for segment in path):
        return row
    node: object = deployed
    for segment in path:
        if not isinstance(node, dict) or segment not in node:
            return row
        node = node[segment]
    shown = _default_value(row.default)
    if shown is _PROSE or shown == node:
        return row
    # helm-docs writes null as nil.
    return replace(row, default="`nil`" if node is None else _json_code(node))


def _deployed_rows(
    rows: list[_Row], subchart: Path, root_override: object
) -> list[_Row]:
    """Show what Hopsworks deploys for a subchart's values.

    The README rows carry the subchart's own defaults; the root chart's
    values for it are merged over them the way Helm merges them. A
    values.yaml PyYAML cannot read (Helm's parser is more lenient) leaves
    the rows as they are, with a warning.
    """
    if not isinstance(root_override, dict) or not root_override:
        return rows
    try:
        values = _load_yaml(subchart / "values.yaml")
    except yaml.YAMLError as exc:
        reason = getattr(exc, "problem", None) or exc
        typer.echo(
            f"WARNING: cannot parse {subchart / 'values.yaml'} ({reason}); "
            "showing its own defaults without the root chart's overrides",
            err=True,
        )
        return rows
    deployed = _helm_merge(values, root_override)
    return [_with_deployed_default(row, deployed) for row in rows]


def _schema_section(prefix: str, name: str, link: str, rows: list[_Row]) -> str:
    key = prefix.split(".")[0]
    intro = (
        f"These are the values of the {link} chart, set under `{prefix}`.\n"
        "The defaults are what Hopsworks deploys: the chart's own, with the "
        f"`{key}` and `{prefix}` overrides above applied.\n"
        "Where Hopsworks overrides a value, the entry also gives the chart's own default."
    )
    anchor = f"helm-values-{prefix}"
    title = _heading("##", f"`{name}` chart values", anchor)
    return f"{title}\n\n{intro}\n\n{_render_rows(rows, 2, '###', anchor)}"


def _common_values(targets: dict[str, str], problems: list[str]) -> str:
    lines = ["| Value | What it sets |", "| --- | --- |"]
    for key, purpose in _COMMON_VALUES:
        if key not in targets:
            problems.append(f"common value {key} is not in the chart")
            continue
        lines.append(f"| {_key_link(key, targets)} | {purpose} |")
    title = _heading("##", "Common values", "helm-values-common")
    return f"{title}\n\n" + "\n".join(lines)


def _inject(page: Path, body: str) -> None:
    content = page.read_text(encoding="utf-8")
    if _BEGIN not in content or _END not in content:
        msg = f"Injection markers ({_BEGIN} / {_END}) not found in {page}"
        raise typer.BadParameter(msg)
    head = content[: content.index(_BEGIN) + len(_BEGIN)]
    tail = content[content.index(_END) :]
    page.write_text(f"{head}\n\n{body}\n\n{tail}", encoding="utf-8")


@dataclass
class _Page:
    stub: Path
    rows: list[_Row]
    upstream: list[dict]
    # (prefix, dependency, rows) of each upstream chart rendered from its schema.
    schemas: list[tuple[str, dict, list[_Row]]]


def _generate(chart: Path, pages_dir: Path, strict: bool) -> None:
    readme = (chart / "README.md").read_text(encoding="utf-8")
    if _VALUES_HEADING not in readme:
        typer.echo(
            "WARNING: '## Values' section not found in the chart README "
            "(older chart versions predate it); leaving the page placeholders.",
            err=True,
        )
        return
    meta = _load_yaml(chart / "Chart.yaml")
    root_values = _load_yaml(chart / "values.yaml")
    version, app_version = meta.get("version", ""), meta.get("appVersion", "")
    note = f"_Generated from the Hopsworks Helm chart `{version}`"
    note += f" (Hopsworks `{app_version}`)._" if app_version else "._"
    conditions = {
        dep["name"]: dep.get("condition") for dep in meta.get("dependencies") or []
    }
    problems: list[str] = []

    # A root README rendered without `helm-docs -u` (hopsworks-helm#2469) has
    # only the root and global values; each subchart's README has its own,
    # keyed from the subchart. With `-u` the root table repeats them all. The
    # first row of a key wins, so a key the root chart overrides keeps the
    # root's row in both layouts (`-u` lists it twice). The '## Values'
    # section is the last one in a README, so take everything after its heading.
    sources = [(readme, "")]
    for subchart_readme in sorted((chart / "charts").glob("*/README.md")):
        prefix = f"{subchart_readme.parent.name}."
        sources.append((subchart_readme.read_text(encoding="utf-8"), prefix))
    rows: list[_Row] = []
    known: set[str] = set()
    for text, prefix in sources:
        if _VALUES_HEADING not in text:
            continue
        for row in _parse_rows(text.split(_VALUES_HEADING, 1)[1], prefix):
            if row.key not in known:
                rows.append(row)
                known.add(row.key)
    by_key: dict[str, list[_Row]] = {}
    for row in rows:
        if not row.key.startswith(_EXCLUDED_PREFIXES):
            by_key.setdefault(_segments(row.key)[0], []).append(row)

    # First pass: which page every key lands on, so pages can link each other.
    pages: dict[str, _Page] = {}
    stubs = sorted(
        (p for p in pages_dir.glob("*.md") if p.name != _INDEX),
        key=lambda p: (p.stem != _GLOBAL, p.stem),
    )
    for stub in stubs:
        key = stub.stem
        subchart = chart / "charts" / key
        upstream = [
            dep
            for dep in _load_yaml(subchart / "Chart.yaml").get("dependencies") or []
            if not str(dep.get("repository", "")).startswith("file://")
        ]
        rows = _deployed_rows(by_key.pop(key, []), subchart, root_values.get(key))
        page = _Page(stub, rows, upstream, [])
        for dep in upstream:
            if _RENDERED_SCHEMAS.get(key) != dep["name"]:
                continue
            schema = _dependency_schema(subchart, dep["name"], str(dep["version"]))
            if schema is None:
                problems.append(
                    f"no values.schema.json for {dep['name']} under {subchart}; "
                    "run `helm dependency build` there to include it"
                )
                continue
            dep_key = dep.get("alias") or dep["name"]
            prefix = f"{key}.{dep_key}"
            # What Hopsworks deploys: the dependency's defaults, then the
            # subchart's values for it, then the root chart's.
            overrides = _helm_merge(
                _load_yaml(subchart / "values.yaml").get(dep_key) or {},
                (root_values.get(key) or {}).get(dep_key) or {},
            )
            problems += [
                f"Hopsworks overrides {path}, which the {dep['name']} "
                f"{dep['version']} schema does not declare"
                for path in _undeclared_overrides(schema, overrides, prefix)
            ]
            rows = _schema_rows(schema, prefix, overrides, dep["name"])
            page.schemas.append((prefix, dep, rows))
        pages[key] = page
    leftover = [row for rows in by_key.values() for row in rows]
    unplaced = sorted(set(by_key) - _NO_PAGE)
    if unplaced:
        problems.append(
            f"no page for top-level keys {', '.join(unplaced)}; add a stub with "
            "the generation markers and a nav entry"
        )
    targets = {row.key: f"{_INDEX}#{_anchor(row.key)}" for row in leftover}
    for page in pages.values():
        for row in page.rows + [r for _, _, rows in page.schemas for r in rows]:
            targets[row.key] = f"{page.stub.name}#{_anchor(row.key)}"

    index_lines = ["| Values | Upstream charts | Keys |", "| --- | --- | --- |"]
    for key, page in pages.items():
        links = [_upstream_link(dep, problems) for dep in page.upstream]
        parts = [note]
        if key in conditions:
            parts.append(_condition_text(conditions[key], targets))
        if page.upstream:
            parts.append(_upstream_admonition(key, page.upstream, links))
        if page.rows:
            parts.append(_render_rows(page.rows, 1, "##", f"helm-values-{key}"))
        else:
            parts.append(f"Chart `{version}` has no `{key}` values.")
        count = len(page.rows)
        by_name = dict(zip((dep["name"] for dep in page.upstream), links))
        for prefix, dep, rows in page.schemas:
            parts.append(
                _schema_section(prefix, dep["name"], by_name[dep["name"]], rows)
            )
            count += len(rows)
        _inject(page.stub, "\n\n".join(parts))

        # An aliased dependency (trino and trinotest) installs the same chart twice.
        upstream_cell = ", ".join(dict.fromkeys(links))
        index_lines.append(
            f"| [`{key}`][helm-values-{key}] | {upstream_cell} | {count} |"
        )

    index = [
        note,
        _common_values(targets, problems),
        _heading("##", "All values", "helm-values-pages")
        + "\n\n"
        + "\n".join(index_lines),
    ]
    if leftover:
        title = _heading("##", "Other values", "helm-values-other")
        index.append(f"{title}\n\n{_section_body(leftover)}")
    _inject(pages_dir / _INDEX, "\n\n".join(index))
    typer.echo(
        f"Injected chart {version} values into {len(stubs)} pages "
        f"({len(leftover)} rows without a page: {', '.join(sorted(by_key)) or 'none'})"
    )
    for problem in problems:
        typer.echo(f"WARNING: {problem}", err=True)
    if strict and problems:
        typer.echo("ERROR: --strict and the warnings above were raised.", err=True)
        raise typer.Exit(1)


def gen_helm_values(
    chart: Annotated[
        Path | None,
        typer.Option(help="Path to a local hopsworks-helm checkout (preview)."),
    ] = None,
    repo_url: Annotated[
        str | None,
        typer.Option(help="Nexus Helm repo base URL to fetch the chart from."),
    ] = None,
    chart_version: Annotated[
        str | None,
        typer.Option(
            help="Chart version major.minor to match, picking the latest patch, "
            "e.g. 4.8 (release docs). Omit for the latest published chart "
            "(e.g. the dev channel)."
        ),
    ] = None,
    username: Annotated[
        str,
        typer.Option(envvar="NEXUS_USER", help="Nexus username (private repos)."),
    ] = "",
    password: Annotated[
        str,
        typer.Option(envvar="NEXUS_PASSWORD", help="Nexus password (private repos)."),
    ] = "",
    pages_dir: Annotated[
        Path,
        typer.Option(help="Folder of the reference pages to inject the values into."),
    ] = _DEFAULT_PAGES_DIR,
    strict: Annotated[
        bool,
        typer.Option(
            help="Fail when a top-level key has no page, an upstream chart has "
            "no docs link, a common value is missing, a rendered schema is "
            "absent, or an override names a key that schema does not declare "
            "(the PR check)."
        ),
    ] = False,
) -> None:
    """Inject the Helm chart values into the reference pages, one per top-level key.

    Source the chart either from a local checkout (``--chart``) or, for CI,
    from the published chart package in a Nexus Helm repo (``--repo-url``,
    optionally ``--chart-version`` for release matching). Each ``<key>.md``
    stub in ``pages_dir`` receives the rows of the chart README ``## Values``
    table under that key, the subchart's deployment condition and links to the
    upstream charts it installs; ``index.md`` receives the common values, the
    overview table and any rows whose key has no stub. The result is consumed
    by the documentation build and is not committed. If no matching chart or
    no ``## Values`` section is found, the page placeholders are left in place
    rather than failing the build; a values row that does not parse always
    fails it.
    """
    if chart:
        _generate(chart, pages_dir, strict)
        return
    if not repo_url:
        raise typer.BadParameter("provide either --chart <dir> or --repo-url <url>")
    archive = _archive_from_registry(repo_url, chart_version, username, password)
    if archive is None:
        return
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            tar.extractall(tmp, filter="data")
        charts = [p.parent for p in Path(tmp).glob("*/Chart.yaml")]
        if len(charts) != 1:
            typer.echo(
                "WARNING: expected one chart at the top of the package; "
                "leaving the page placeholders.",
                err=True,
            )
            return
        _generate(charts[0], pages_dir, strict)


def reset_helm_values(
    pages_dir: Annotated[
        Path,
        typer.Option(help="Folder of the reference pages to reset."),
    ] = _DEFAULT_PAGES_DIR,
) -> None:
    """Put the committed placeholder back between the markers of every values page.

    Undoes ``gen-helm-values`` in a working copy, since the generated values
    are never committed; text outside the markers is kept. The PR check runs
    this and fails when it changes a committed page.
    """
    pages = sorted(pages_dir.glob("*.md"))
    for page in pages:
        _inject(page, _INDEX_PLACEHOLDER if page.name == _INDEX else _PLACEHOLDER)
    typer.echo(f"Reset {len(pages)} pages in {pages_dir} to their placeholders")
