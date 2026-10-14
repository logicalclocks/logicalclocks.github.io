"""MkDocs build hook for the release notes site (``mkdocs.releases.yml``).

Its ``docs_dir`` is ``docs/releases``, so the stylesheets, scripts, logo and
favicon the inherited config points at are outside it; this adds them from ``docs/``.

A release page (``<major>/X.Y.Z.md``) declares ``released``, ``application`` and
``python_client`` in its front matter. From those this renders the line under the
page title, a "Python client" section linking the GitHub release notes of every
client version new in that release, and the table of a major's ``index.md`` where
it holds ``<!-- releases -->``.
"""

from __future__ import annotations

import os
import re

from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File
from mkdocs.utils.meta import get_data


RELEASE_PAGE = re.compile(r"^(\d+)/(\d+\.\d+\.\d+)\.md$")
VERSION = re.compile(r"\d+\.\d+\.\d+")
FIELDS = ("released", "application", "python_client")
CLIENT_RELEASES = "https://github.com/logicalclocks/hopsworks-api/releases/tag/{}"

# major -> [(version, front matter)], oldest first; rebuilt by on_files on every build
_releases = {}


def on_files(files, *, config):
    docs = os.path.join(os.path.dirname(config.config_file_path), "docs")
    shared = [
        *config.extra_css,
        *(str(script) for script in config.extra_javascript),
        config.theme["logo"],
        config.theme["favicon"],
    ]
    for path in shared:
        files.append(File(path, docs, config.site_dir, config.use_directory_urls))

    _releases.clear()
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
    if markdown.lstrip().partition("\n")[0] != f"# Hopsworks {version}":
        raise PluginError(f"{file.src_uri}: must start with '# Hopsworks {version}'")
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
    return "hopsworks-" + version.replace(".", "")


def _client_link(version):
    return f"[{version}]({CLIENT_RELEASES.format(version)})"


def _new_clients(release, previous_client, client):
    """The client versions new in ``release``, newest first.

    hopsworks-api tags every patch of a minor, so the patches in between exist.
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
    if "<!-- releases -->" in markdown:
        major = os.path.dirname(page.file.src_uri)
        return markdown.replace(
            "<!-- releases -->", _releases_table(_releases.get(major, []))
        )
    return markdown
