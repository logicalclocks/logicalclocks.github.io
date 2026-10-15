"""MkDocs build hook for the release pages in ``docs/releases/``.

Their source is on main only; a release branch build copies ``docs/releases/`` and
this hook from main first, so every docs version shows the same release pages.
The nav entry ``Releases: releases/index.md`` expands to a section per major and
minor version with a page per release, newest first, and is dropped when
``docs/releases/`` is absent, as in a local build of a release branch.

A release page (``releases/<major>/X.Y.Z.md``) starts with
``# Hopsworks X.Y.Z { #hopsworks-X-Y-Z }`` and declares ``released``, ``application``
and ``python_client`` in its front matter. From those this renders the line under
the page title, a "Python client" section linking the GitHub release notes of every
client version new in that release, and the table of a major's ``index.md`` where it
holds ``<!-- releases -->``.

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
RELEASE_PAGE = re.compile(r"^releases/(\d+)/(\d+\.\d+\.\d+)\.md$")
VERSION = re.compile(r"\d+\.\d+\.\d+")
FIELDS = ("released", "application", "python_client")
CLIENT_REPO = "https://github.com/logicalclocks/hopsworks-api"
CLIENT_RELEASES = CLIENT_REPO + "/releases/tag/{}"

# major -> [(version, front matter)], oldest first; rebuilt by on_files on every build
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


def _release_nav(docs_dir):
    """The nav section of the release pages, grouped by major and minor, newest first."""
    root = Path(docs_dir) / RELEASES
    majors = sorted(
        (p for p in root.iterdir() if p.is_dir() and p.name.isdigit()),
        key=lambda p: int(p.name),
        reverse=True,
    )
    section: list = [NAV_ENTRY]
    for major in majors:
        versions = sorted(
            (p.stem for p in major.glob("*.md") if VERSION.fullmatch(p.stem)),
            key=_version,
            reverse=True,
        )
        minors: dict = {}
        for v in versions:
            minors.setdefault(v.rpartition(".")[0], []).append(
                {v: f"{RELEASES}/{major.name}/{v}.md"}
            )
        section.append(
            {
                f"{major.name}.x": [
                    f"{RELEASES}/{major.name}/index.md",
                    *({minor: pages} for minor, pages in minors.items()),
                ]
            }
        )
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
        match = RELEASE_PAGE.match(file.src_uri)
        if match:
            major, version = match.groups()
            _releases.setdefault(major, []).append(
                (version, _read_release(file, version))
            )
    for releases in _releases.values():
        releases.sort(key=lambda release: _version(release[0]))
        _check_clients(releases)
    return files


def _read_release(file, version):
    with open(file.abs_src_path, encoding="utf-8") as source:
        markdown, meta = get_data(source.read())
    missing = [field for field in FIELDS if not meta.get(field)]
    if missing:
        raise PluginError(
            f"{file.src_uri}: front matter is missing {', '.join(missing)}"
        )
    fields = {field: str(meta[field]) for field in FIELDS}
    if not VERSION.fullmatch(fields["python_client"]):
        raise PluginError(f"{file.src_uri}: python_client must be a quoted X.Y.Z")
    title = f"# Hopsworks {version} {{ #{_anchor(version)} }}"
    if markdown.lstrip().partition("\n")[0] != title:
        raise PluginError(f"{file.src_uri}: must start with '{title}'")
    return fields


def _check_clients(releases):
    for (before, old), (version, new) in zip(releases, releases[1:]):
        same_minor = _version(before)[:2] == _version(version)[:2]
        if same_minor and _version(new["python_client"]) < _version(
            old["python_client"]
        ):
            raise PluginError(
                f"{version}: python_client {new['python_client']} is older than "
                f"{old['python_client']} of {before}"
            )


def _version(text):
    return tuple(int(part) for part in text.split("."))


def _anchor(version):
    return "hopsworks-" + version.replace(".", "-")


def _client_link(version):
    _linked_clients.add(version)
    return f"[{version}]({CLIENT_RELEASES.format(version)})"


def _new_clients(release, previous_client, client):
    """The client versions new in ``release``, newest first.

    Every patch in between is listed, so a patch hopsworks-api never tagged fails
    the tag check.
    """
    major, minor, patch = _version(client)
    if previous_client and _version(previous_client)[:2] == (major, minor):
        first = _version(previous_client)[2] + 1
    elif _version(release)[:2] == (major, minor):
        first = 0
    else:
        first = patch
    return [f"{major}.{minor}.{p}" for p in range(patch, first - 1, -1)]


def _client_section(version, releases):
    index = [release[0] for release in releases].index(version)
    client = releases[index][1]["python_client"]
    previous = None
    if index > 0 and _version(releases[index - 1][0])[:2] == _version(version)[:2]:
        previous = releases[index - 1]
    lines = ["## Python client", ""]
    if previous and previous[1]["python_client"] == client:
        first = next(
            r[0]
            for r in releases
            if _version(r[0])[:2] == _version(version)[:2]
            and r[1]["python_client"] == client
        )
        lines.append(
            f"Python environments keep the Python client {_client_link(client)}, "
            f"which came with [{first}][{_anchor(first)}]."
        )
        return "\n".join(lines)
    lines.append(f"Python environments come with the Python client {client}.")
    if previous:
        lines.append(
            f"Release notes of the client versions since [{previous[0]}][{_anchor(previous[0])}]:"
        )
    else:
        lines.append("Release notes of the client:")
    lines.append("")
    new = _new_clients(
        version, previous[1]["python_client"] if previous else None, client
    )
    lines.extend(f"- {_client_link(v)}" for v in new)
    return "\n".join(lines)


def _releases_table(releases):
    lines = [
        "| Release | Released | Application | Python client |",
        "| ------- | -------- | ----------- | ------------- |",
    ]
    for version, fields in reversed(releases):
        lines.append(
            f"| [{version}][{_anchor(version)}] | {fields['released']} | {fields['application']} "
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


def on_page_markdown(markdown, *, page, config, files):
    match = RELEASE_PAGE.match(page.file.src_uri)
    if match:
        major, version = match.groups()
        releases = _releases[major]
        fields = dict(releases)[version]
        header = (
            f"Released on {fields['released']} · Application {fields['application']} "
            f"· [Python client {fields['python_client']}](#python-client)"
        )
        title, _, body = markdown.lstrip().partition("\n")
        section = _client_section(version, releases)
        return f"{title}\n\n{header}\n{body.rstrip()}\n\n{section}\n"
    major = re.fullmatch(r"releases/(\d+)/index\.md", page.file.src_uri)
    if major and "<!-- releases -->" in markdown:
        return markdown.replace(
            "<!-- releases -->", _releases_table(_releases.get(major[1], []))
        )
    return markdown
