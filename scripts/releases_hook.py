"""MkDocs build hook for the release pages in ``docs/releases/``.

Their source is on main only; a release branch build copies ``docs/releases/`` and
this hook from main first, so every docs version shows the same release pages.
The nav entry ``Releases: releases/index.md`` expands to a section per minor version,
newest first, holding its release notes, and is dropped when
``docs/releases/`` is absent, as in a local build of a release branch.

The release notes of a minor version (``releases/X.Y/index.md``) declare every
release in their front matter, newest first, and hold one
``## X.Y.Z { #hopsworks-X-Y-Z }`` section per release in the same order. Under each
section title this renders the release date, the release it lists the changes
since, the application version and the Python client, linking the GitHub release
notes of every client version new in that release. It also renders the table of
all releases where ``releases/index.md`` holds ``<!-- releases -->``.

The build writes ``releases/fingerprint.txt``, a hash of the release sources and
this hook, which ``hopsworks-docs sync-release-notes`` compares across versions.

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
from mkdocs.utils.meta import get_data


log = logging.getLogger("mkdocs.hooks.releases")

RELEASES = "releases"
NAV_ENTRY = "releases/index.md"
FINGERPRINT = "releases/fingerprint.txt"
NOTES_PAGE = re.compile(r"^releases/(\d+\.\d+)/index\.md$")
SECTION = re.compile(r"^## (\d+\.\d+\.\d+) \{ #hopsworks-[\d-]+ \}$", re.MULTILINE)
VERSION = re.compile(r"\d+\.\d+\.\d+")
FIELDS = ("released", "application", "python_client")
CLIENT_REPO = "https://github.com/logicalclocks/hopsworks-api"
CLIENT_RELEASES = CLIENT_REPO + "/releases/tag/{}"

# version -> front matter of every release, oldest first; rebuilt by on_files
_releases = {}
# client versions linked by this build
_linked_clients = set()


def digest(hook, sources):
    """Hash the hook source and the (path under docs/releases, content) pairs."""
    result = hashlib.sha256(hook)
    for path, content in sorted(sources):
        result.update(path.encode() + b"\0" + content + b"\0")
    return result.hexdigest()


def fingerprint(docs_dir):
    """The digest of the release sources under ``docs_dir`` and of this hook."""
    root = Path(docs_dir) / RELEASES
    sources = [
        (path.relative_to(root).as_posix(), path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    ]
    return digest(Path(__file__).read_bytes(), sources)


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
    _check_clients()
    return files


def _read_minor(file, minor):
    """The releases a minor version's page declares, checked against its sections."""
    with open(file.abs_src_path, encoding="utf-8") as source:
        markdown, meta = get_data(source.read())
    declared = meta.get("releases")
    if not isinstance(declared, dict) or not declared:
        raise PluginError(f"{file.src_uri}: front matter must declare its releases")
    releases = {}
    for version, fields in declared.items():
        version = str(version)
        if not VERSION.fullmatch(version) or version.rpartition(".")[0] != minor:
            raise PluginError(f"{file.src_uri}: {version} is not a {minor} release")
        fields = fields or {}
        missing = [field for field in FIELDS if not fields.get(field)]
        if missing:
            raise PluginError(f"{file.src_uri}: {version} is missing {', '.join(missing)}")
        if not VERSION.fullmatch(str(fields["python_client"])):
            raise PluginError(f"{file.src_uri}: {version} python_client must be a quoted X.Y.Z")
        if fields.get("since") and not version.endswith(".0"):
            raise PluginError(f"{file.src_uri}: only an X.Y.0 release declares since")
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
            raise PluginError(f"{file.src_uri}: the section of {version} must be '{title}'")
    return releases


def _check_clients():
    versions = list(_releases)
    for before, version in zip(versions, versions[1:]):
        old, new = _releases[before], _releases[version]
        if _version(new["python_client"]) < _version(old["python_client"]):
            raise PluginError(
                f"{version}: python_client {new['python_client']} is older than "
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
        f"Released on {fields['released']} · Changes since {_link(_since(version))} "
        f"· Application {fields['application']} · {_client(version)}"
    )


def _releases_table():
    lines = [
        "| Release | Released | Application | Python client |",
        "| ------- | -------- | ----------- | ------------- |",
    ]
    for version, fields in reversed(_releases.items()):
        lines.append(
            f"| {_link(version)} | {fields['released']} | {fields['application']} "
            f"| {_client_link(fields['python_client'])} |"
        )
    return "\n".join(lines)


def on_post_build(*, config):
    if _releases:
        target = Path(config.site_dir) / FINGERPRINT
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(fingerprint(config.docs_dir) + "\n")
    if not os.environ.get("HOPSWORKS_DOCS_CHECK_CLIENT_TAGS"):
        return
    refs = subprocess.run(
        ["git", "ls-remote", "--tags", "--refs", CLIENT_REPO],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
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
        body = markdown[title.end() : end].rstrip("\n")
        version = title[1]
        parts.append(
            f"{title[0]}\n\n{_header(version)}{body}\n\n{_client_notes(version)}\n\n"
        )
    return "".join(parts)


def on_page_markdown(markdown, *, page, config, files):
    if NOTES_PAGE.match(page.file.src_uri):
        return _with_client_notes(markdown)
    if page.file.src_uri == NAV_ENTRY and "<!-- releases -->" in markdown:
        return markdown.replace("<!-- releases -->", _releases_table())
    return markdown
