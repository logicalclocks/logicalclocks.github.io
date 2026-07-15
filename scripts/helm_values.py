import base64
import io
import re
import tarfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Annotated

import typer
import yaml
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from packaging.version import InvalidVersion, Version


_DEFAULT_PAGE = (
    _DOCS_ROOT / "docs" / "setup_installation" / "common" / "helm_chart_values.md"
)
_VALUES_HEADING = "\n## Values\n"
_BEGIN = "<!-- BEGIN GENERATED VALUES -->"
_END = "<!-- END GENERATED VALUES -->"

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
        return max(entries, key=lambda e: str(e.get("created", ""))) if entries else None

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


def _readme_from_registry(
    repo_url: str, chart_version: str | None, username: str, password: str
) -> tuple[str, str, str] | None:
    """Resolve a chart in a Helm (Nexus) repo and return (readme, version, appVersion).

    Returns None (and warns) if nothing suitable is found, so the build keeps
    the page placeholder instead of failing.
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
            f"'{chart_version or 'any'}'; leaving the page placeholder.",
            err=True,
        )
        return None

    urls = chosen.get("urls") or []
    if not urls:
        typer.echo(
            f"WARNING: chart {chosen.get('version')} has no download URL; "
            "leaving the page placeholder.",
            err=True,
        )
        return None

    url = urls[0]
    if not url.startswith(("http://", "https://")):
        url = f"{base}/{url.lstrip('/')}"
    version = str(chosen.get("version", ""))
    app_version = str(chosen.get("appVersion", ""))
    typer.echo(f"Using chart {version} (appVersion {app_version}) from {base}")

    archive = _http_get(url, username, password)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        # The chart README is the top-level "<chart>/README.md" (one slash);
        # deeper matches are subchart READMEs. Require a regular file so a
        # directory/symlink/special member never reaches extractfile() (which
        # would return None) and crash instead of skipping gracefully.
        member = next(
            (
                m
                for m in tar.getmembers()
                if m.isfile()
                and m.name.count("/") == 1
                and m.name.endswith("/README.md")
            ),
            None,
        )
        if member is None:
            typer.echo(
                "WARNING: README.md not found in the chart package; "
                "leaving the page placeholder.",
                err=True,
            )
            return None
        extracted = tar.extractfile(member)
        return extracted.read().decode("utf-8"), version, app_version


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
    page: Annotated[
        Path,
        typer.Option(help="Reference page to inject the values table into."),
    ] = _DEFAULT_PAGE,
) -> None:
    """Inject the Helm chart README values table into the reference page.

    Source the chart README either from a local checkout (``--chart``) or, for
    CI, from the published chart package in a Nexus Helm repo (``--repo-url``,
    optionally ``--chart-version`` for release matching). Slices the ``## Values``
    table out of that README and writes it, with a line recording the chart
    version, between the generation markers in ``page``. The result is consumed
    by the documentation build and is not committed. If no matching chart or no
    ``## Values`` section is found, the page placeholder is left in place rather
    than failing the build.
    """
    if chart:
        readme: str = (chart / "README.md").read_text(encoding="utf-8")
        meta = yaml.safe_load((chart / "Chart.yaml").read_text(encoding="utf-8")) or {}
        version = str(meta.get("version", ""))
        app_version = str(meta.get("appVersion", ""))
    elif repo_url:
        resolved = _readme_from_registry(repo_url, chart_version, username, password)
        if resolved is None:
            return
        readme, version, app_version = resolved
    else:
        raise typer.BadParameter("provide either --chart <dir> or --repo-url <url>")

    if _VALUES_HEADING not in readme:
        typer.echo(
            "WARNING: '## Values' section not found in the chart README "
            "(older chart versions predate it); leaving the page placeholder.",
            err=True,
        )
        return
    # The '## Values' section is the last one in the README, so take everything
    # after its heading to EOF -- that is the full Key/Type/Default/Description table.
    table = _neutralize_markdown_refs(readme.split(_VALUES_HEADING, 1)[1].strip())

    note = f"_Generated from the Hopsworks Helm chart `{version}`"
    note += f" (Hopsworks `{app_version}`)._" if app_version else "._"

    content = page.read_text()
    if _BEGIN not in content or _END not in content:
        msg = f"Injection markers ({_BEGIN} / {_END}) not found in {page}"
        raise typer.BadParameter(msg)
    head = content[: content.index(_BEGIN) + len(_BEGIN)]
    tail = content[content.index(_END) :]
    page.write_text(f"{head}\n\n{note}\n\n{table}\n\n{tail}")
    typer.echo(f"Injected chart {version} values ({table.count(chr(10)) + 1} lines)")
