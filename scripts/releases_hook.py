"""MkDocs build hook for the release pages in ``docs/releases/``.

Their source is on main only; a release branch build copies them, this hook, and
their script and styles from main first (``FROM_MAIN``), so every docs version
shows the same release pages.
The nav entry ``Releases: releases/index.md`` expands to a section per minor version,
newest first, holding its release notes, and is dropped when
``docs/releases/`` is absent, as in a local build of a release branch.

The release notes of a minor version (``releases/X.Y/index.md``) declare every
release in their front matter, newest first, and hold one
``## X.Y.Z { #hopsworks-X-Y-Z }`` section per release in the same order. Under each
section title this renders the Helm chart version, the release date, the release
it lists the changes since and the Python client, and at the end of each release
the GitHub release notes of every client version new in it. It also renders the
table of all releases where ``releases/index.md`` holds ``<!-- releases -->``.

The build writes ``releases/fingerprint.txt``, a hash of the files in
``FROM_MAIN``, which ``hopsworks-docs sync-release-notes`` compares across versions.

With ``HOPSWORKS_DOCS_CHECK_CLIENT_TAGS`` set, as ``hopsworks-docs check`` does, the
build fails if hopsworks-api has no tag for a client version it links.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import subprocess
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority
from mkdocs.utils.meta import get_data


log = logging.getLogger("mkdocs.hooks.releases")

RELEASES = "releases"
NAV_ENTRY = "releases/index.md"
FINGERPRINT = "releases/fingerprint.txt"
NOTES_PAGE = re.compile(r"^releases/(\d+\.\d+)/index\.md$")
SECTION = re.compile(r"^## (\d+\.\d+\.\d+) \{ #hopsworks-[\d-]+ \}$", re.MULTILINE)
VERSION = re.compile(r"\d+\.\d+\.\d+")
FIELDS = ("released", "python_client")
# what every docs version takes from main, relative to the repository root; the copy
# steps of mkdocs-release.yml and mkdocs-test.yml repeat it
FROM_MAIN = (
    "docs/releases",
    "docs/css/releases.css",
    "docs/js/client-release-notes.js",
    "scripts/releases_hook.py",
)
# how users reach a change, in the order entries carry and are sorted by them
TAGS = ("API", "FRONTEND", "HELM")
ENTRY_TAGS = re.compile(r"^- ((?:\[[A-Z]+\] )*)")
# a bracketed word that is not a link, such as [Api] or the [HELM] of [API][HELM]
TAG_LIKE = re.compile(r"\[(?:[A-Z]+\](?!\()|(?i:api|frontend|helm)\](?![(\[]))")
UNTAGGED = ("Upgrade steps", "Upgraded components")
CLIENT_REPO = "https://github.com/logicalclocks/hopsworks-api"
CLIENT_RELEASES = CLIENT_REPO + "/releases/tag/{}"

# version -> front matter of every release, oldest first; rebuilt by on_files
_releases = {}
# client versions linked by this build
_linked_clients = set()


def digest(sources):
    """Hash the (path, content) pairs of the files in ``FROM_MAIN``."""
    result = hashlib.sha256()
    for path, content in sorted(sources):
        result.update(path.encode() + b"\0" + content + b"\0")
    return result.hexdigest()


def fingerprint(root):
    """The digest of the files in ``FROM_MAIN`` under the repository ``root``."""
    files = [
        path
        for name in FROM_MAIN
        for path in (root / name, *(root / name).rglob("*"))
        if path.is_file()
    ]
    return digest(
        (path.relative_to(root).as_posix(), path.read_bytes()) for path in files
    )


def _minors(docs_dir):
    """The minor version folders with release notes, newest first."""
    root = Path(docs_dir) / RELEASES
    return sorted(
        (p for p in root.iterdir() if (p / "index.md").is_file()),
        key=lambda p: _version(p.name),
        reverse=True,
    )


def _release_nav(docs_dir):
    section: list = [NAV_ENTRY]
    for minor in _minors(docs_dir):
        section.append({minor.name: f"{RELEASES}/{minor.name}/index.md"})
    return section


def on_config(config):
    present = (Path(config.docs_dir) / NAV_ENTRY).is_file()
    if not config.nav:
        return config
    nav = []
    for item in config.nav:
        if isinstance(item, dict) and list(item.values()) == [NAV_ENTRY]:
            if present:
                nav.append({next(iter(item)): _release_nav(config.docs_dir)})
            else:
                log.info(
                    "docs/releases/ is missing, so the Releases section is left out; "
                    "copy it from main with: git checkout origin/main -- docs/releases"
                )
            continue
        nav.append(item)
    config.nav = nav
    return config


def on_files(files, *, config):
    _releases.clear()
    _linked_clients.clear()
    for file in files.documentation_pages():
        match = NOTES_PAGE.match(file.src_uri)
        if match:
            _releases.update(_read_minor(file, match[1]))
    ordered = sorted(_releases.items(), key=lambda release: _version(release[0]))
    _releases.clear()
    _releases.update(ordered)
    oldest = next(iter(_releases), None)
    if oldest and not _releases[oldest].get("since"):
        raise PluginError(
            f"{RELEASES}/{oldest.rpartition('.')[0]}/index.md: {oldest} is the oldest "
            "release, so it must be an X.Y.0 that declares since"
        )
    minors = set()
    for version, fields in _releases.items():
        minor = version.rpartition(".")[0]
        if minor not in minors and not version.endswith(".0"):
            raise PluginError(
                f"{RELEASES}/{minor}/index.md: declare {minor}.0, the first release of {minor}"
            )
        minors.add(minor)
        if fields.get("since") and version != oldest:
            raise PluginError(
                f"{RELEASES}/{minor}/index.md: only the oldest release declares since; "
                f"{version} compares with the first release of the previous minor version"
            )
    _check_clients()
    # In the source, so that llms_hook exports them
    for file in files.documentation_pages():
        if NOTES_PAGE.match(file.src_uri):
            file.content_string = SECTION.sub(
                lambda title: f"{title[0]}\n\n{_header(title[1])}", file.content_string
            )
        elif file.src_uri == NAV_ENTRY:
            file.content_string = file.content_string.replace(
                "<!-- releases -->", _releases_table()
            )
    return files


def _read_minor(file, minor):
    """The releases a minor version's page declares, checked against its sections."""
    markdown, meta = get_data(file.content_string)
    declared = meta.get("releases")
    if not isinstance(declared, dict) or not declared:
        raise PluginError(f"{file.src_uri}: front matter must declare its releases")
    releases = {}
    for version, fields in declared.items():
        version = str(version)
        if not VERSION.fullmatch(version) or version.rpartition(".")[0] != minor:
            raise PluginError(f"{file.src_uri}: {version} is not a {minor} release")
        fields = fields or {}
        unknown = set(fields) - {*FIELDS, "since"}
        if unknown:
            raise PluginError(
                f"{file.src_uri}: {version} has unknown fields {', '.join(sorted(unknown))}"
            )
        missing = [field for field in FIELDS if not fields.get(field)]
        if missing:
            raise PluginError(
                f"{file.src_uri}: {version} is missing {', '.join(missing)}"
            )
        if not VERSION.fullmatch(str(fields["python_client"])):
            raise PluginError(
                f"{file.src_uri}: {version} python_client must be a quoted X.Y.Z"
            )
        since = str(fields.get("since") or "")
        if since and not version.endswith(".0"):
            raise PluginError(f"{file.src_uri}: only an X.Y.0 release declares since")
        older = VERSION.fullmatch(since) and _version(since) < _version(version)
        if since and not older:
            raise PluginError(
                f"{file.src_uri}: {version} since must be a quoted X.Y.Z older than {version}"
            )
        releases[version] = {key: str(value) for key, value in fields.items()}
    newest_first = sorted(releases, key=_version, reverse=True)
    if list(releases) != newest_first:
        raise PluginError(f"{file.src_uri}: list the releases newest first")
    sections = SECTION.findall(markdown)
    if sections != newest_first:
        raise PluginError(
            f"{file.src_uri}: needs a '## X.Y.Z {{ #hopsworks-X-Y-Z }}' section per "
            f"release, newest first: {', '.join(newest_first)}"
        )
    for version in sections:
        title = f"## {version} {{ #{_anchor(version)} }}"
        if title not in markdown:
            raise PluginError(
                f"{file.src_uri}: the section of {version} must be '{title}'"
            )
    _check_tags(file, markdown)
    return releases


def _check_tags(file, markdown):
    """Every entry starts with known tags in order, and a subsection is sorted by them."""
    version = subsection = None
    previous = 0
    for line in markdown.splitlines():
        if title := SECTION.match(line):
            version, subsection = title[1], None
        elif line.startswith("### "):
            subsection, previous = line[4:], 0
        elif line.startswith("- ") and version and subsection not in UNTAGGED:
            tagged = ENTRY_TAGS.match(line)[1]
            tags = re.findall(r"\[([A-Z]+)\]", tagged)
            where = f"{file.src_uri}: {version} {subsection}: {line[:70]}"
            if TAG_LIKE.match(line, 2 + len(tagged)):
                raise PluginError(
                    f"{where}: write each tag in capitals and follow it by a space"
                )
            if any(tag not in TAGS for tag in tags):
                raise PluginError(f"{where}: use only the tags {', '.join(TAGS)}")
            ranks = [TAGS.index(tag) for tag in tags] or [len(TAGS)]
            if ranks != sorted(set(ranks)):
                raise PluginError(
                    f"{where}: list its tags once each, in the order {', '.join(TAGS)}"
                )
            if ranks[0] < previous:
                raise PluginError(
                    f"{where}: sort the entries by their first tag, untagged last"
                )
            previous = ranks[0]


def _check_clients():
    versions = list(_releases)
    for before, version in zip(versions, versions[1:]):
        old, new = _releases[before], _releases[version]
        if _version(new["python_client"]) < _version(old["python_client"]):
            raise PluginError(
                f"{RELEASES}/{version.rpartition('.')[0]}/index.md: {version}: python_client "
                f"{new['python_client']} is older than "
                f"{old['python_client']} of {before}"
            )


def _version(text):
    return tuple(int(part) for part in text.split("."))


def _anchor(version):
    return "hopsworks-" + version.replace(".", "-")


def _link(version):
    return f"[{version}][{_anchor(version)}]" if version in _releases else version


def _client_link(version):
    _linked_clients.add(version)
    return f"[{version}]({CLIENT_RELEASES.format(version)})"


def _since(version):
    """The release ``version`` lists the changes since.

    A patch compares with the previous release of its minor version, an X.Y.0 with
    the first release of the previous minor version, or with the ``since`` it
    declares when that minor version has no page, as 5.0.0 does for 4.8.
    """
    fields = _releases[version]
    if fields.get("since"):
        return fields["since"]
    earlier = [v for v in _releases if _version(v) < _version(version)]
    if not version.endswith(".0"):
        return earlier[-1]
    previous = [v for v in earlier if _version(v)[:2] == _version(earlier[-1])[:2]]
    return previous[0]


def _new_clients(previous_client, client):
    """The client versions since ``previous_client``, oldest first.

    Every patch in between is listed, so a patch hopsworks-api never tagged fails
    the tag check.
    """
    major, minor, patch = _version(client)
    if previous_client and _version(previous_client)[:2] == (major, minor):
        first = _version(previous_client)[2] + 1
    else:
        first = 0
    return [f"{major}.{minor}.{p}" for p in range(first, patch + 1)]


def _client(version):
    client = _releases[version]["python_client"]
    previous = _releases.get(_since(version), {}).get("python_client")
    if previous == client:
        return f"Python client {_client_link(client)}, unchanged"
    new = _new_clients(previous, client)
    if len(new) == 1:
        return f"Python client {_client_link(client)}"
    return f"Python client {client} ({', '.join(_client_link(v) for v in new)})"


def _header(version):
    fields = _releases[version]
    return (
        f"Helm chart {version} · Released on {fields['released']} "
        f"· Changes since {_link(_since(version))} · {_client(version)}"
    )


def _releases_table():
    lines = [
        "| Helm chart | Released | Python client |",
        "| ---------- | -------- | ------------- |",
    ]
    for version, fields in reversed(_releases.items()):
        lines.append(
            f"| {_link(version)} | {fields['released']} "
            f"| {_client_link(fields['python_client'])} |"
        )
    return "\n".join(lines)


def on_post_build(*, config):
    if _releases:
        target = Path(config.site_dir) / FINGERPRINT
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(fingerprint(Path(config.docs_dir).parent) + "\n")
    if not os.environ.get("HOPSWORKS_DOCS_CHECK_CLIENT_TAGS"):
        return
    try:
        refs = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", CLIENT_REPO],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        ).stdout
    except subprocess.SubprocessError as error:
        raise PluginError(f"Can't list the tags of hopsworks-api: {error}") from error
    tags = {line.rpartition("refs/tags/")[2] for line in refs.splitlines()}
    missing = sorted(_linked_clients - tags, key=_version)
    if missing:
        raise PluginError(
            f"hopsworks-api has no tag for the linked client versions {', '.join(missing)}"
        )


def _client_notes(version):
    """The Python client subsection of a release.

    It links the GitHub release notes of every client version new in the release;
    ``docs/js/client-release-notes.js`` replaces the links with the notes themselves
    in the reader's browser, and leaves them when GitHub can't be reached.
    """
    client = _releases[version]["python_client"]
    previous = _releases.get(_since(version), {}).get("python_client")
    if previous == client:
        return f"### Python client\n\nThe Python client is unchanged, {client}."
    new = _new_clients(previous, client)
    links = ", ".join(_client_link(v) for v in new)
    return (
        "### Python client\n\n"
        f'<div class="hops-client-notes" data-versions="{" ".join(new)}" markdown>\n\n'
        f"The release notes of hopsworks-api {links}.\n\n</div>"
    )


def _with_client_notes(markdown):
    """``markdown`` with the Python client subsection at the end of each release."""
    titles = list(SECTION.finditer(markdown))
    parts = [markdown[: titles[0].start()]] if titles else [markdown]
    for title, following in zip(titles, [*titles[1:], None]):
        end = following.start() if following else len(markdown)
        section = markdown[title.start() : end].rstrip("\n")
        parts.append(f"{section}\n\n{_client_notes(title[1])}\n\n")
    return "".join(parts)


def _tag_labels(markdown):
    """Render the tags that start an entry as labels, before Markdown reads them as links."""

    def labels(entry):
        tags = re.findall(r"\[([A-Z]+)\]", entry[1])
        spans = "".join(f'<span class="hops-release-tag">{tag}</span> ' for tag in tags)
        return f"- {spans}"

    return re.sub(r"^- ((?:\[[A-Z]+\] )+)", labels, markdown, flags=re.MULTILINE)


# After llms_hook has stored the Markdown, so its export keeps the plain tags
@event_priority(-50)
def on_page_markdown(markdown, *, page, config, files):
    if NOTES_PAGE.match(page.file.src_uri):
        return _with_client_notes(_tag_labels(markdown))
    return markdown
