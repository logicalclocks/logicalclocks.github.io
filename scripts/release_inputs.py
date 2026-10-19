"""Collect the facts a release section is written from.

Prints, for one ``hopsworks-helm`` release, the release it compares with, its front
matter, the commits of the chart, of ``rondb-helm`` and of the application it ships
(``hopsworks-ee``, ``hopsworks-front``), the Helm values it adds, removes or changes,
what the chart newly deprecates, and the Upgraded components table, as
``.claude/docs/releases.md`` describes. The ``/release-notes`` skill writes the
section from this; nothing here is published, so it names commits freely.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from hopsworks_docs.scripts.release_components import (
    _baseline,
    _dependency,
    _flatten,
    _git,
    _load,
    _release,
    _table,
    _uncovered,
)
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


HELM_REPO = "logicalclocks/hopsworks-helm"
CHART = "charts/hopsworks/Chart.yaml"
VALUES = "charts/hopsworks/values.yaml"
RONDB_CHART = "charts/rondb/Chart.yaml"
# A merge suffix such as "(#1234)", or a backport marker such as "(5.0)" or "[5.1]".
SUBJECT_NOISE = re.compile(r"\s*(\(#\d+\)|\(\d+\.\d+\)|\[\d+\.\d+\])\s*")
# A version setting; the Upgraded components table covers these.
# The checkouts default to siblings of this repo, as CI clones hopsworks-api.
SOURCES = _DOCS_ROOT.parent
VERSION_LEAF = re.compile(r"(^|[._])(tag|version|image|digest)$", re.IGNORECASE)


def _tags(helm):
    return sorted(
        (
            t
            for t in _git(helm, "tag", "--list", "v*").split()
            if re.fullmatch(r"v\d+\.\d+\.\d+", t)
        ),
        key=_release,
    )


def _key(subject):
    return SUBJECT_NOISE.sub(" ", subject).strip().lower()


def _commits(repo, *rev):
    """(short sha, subject) of the non-merge commits of ``rev``, oldest first."""
    out = _git(repo, "log", "--reverse", "--no-merges", "--format=%h\t%s", *rev)
    return [tuple(line.split("\t", 1)) for line in out.splitlines() if line]


def _range(repo, old, new, same_line):
    """The commits ``new`` adds over ``old``.

    A plain range on one branch, else the commits of ``new`` that ``old`` has no
    equivalent of (``--cherry-pick``).
    """
    if same_line:
        return _commits(repo, f"{old}..{new}")
    return _commits(repo, "--cherry-pick", "--right-only", f"{old}...{new}")


def _released(tag):
    try:
        out = subprocess.run(
            ["gh", "release", "view", tag, "-R", HELM_REPO, "--json", "publishedAt"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return json.loads(out)["publishedAt"][:10]


def _application(helm, tag):
    return (_load(helm, tag, CHART) or {}).get("appVersion")


def _python_client(helm, images, tag):
    """The hopsworks-api version of the base images the chart at ``tag`` deploys."""
    base = ((_load(helm, tag, VALUES) or {}).get("variables") or {}).get(
        "base_image_version"
    )
    if not base:
        return None, None
    for commit in _git(
        images, "log", "--all", "--format=%H", "--", "version.txt"
    ).split():
        try:
            if _git(images, "show", f"{commit}:version.txt").strip() != base:
                continue
            client = _git(
                images, "show", f"{commit}:base-image/hopsworks-api-version.txt"
            )
        except subprocess.CalledProcessError:
            continue
        return base, client.strip()
    return base, None


def _release_commit(repo, branch, version):
    """The ``Release X.Y.Z`` commit of an application version: its last commit."""
    pattern = rf"^Release {re.escape(version)}( \(#[0-9]+\))?$"
    out = _git(
        repo, "log", f"origin/{branch}", "-E", f"--grep={pattern}", "--format=%h"
    )
    return out.split()[0] if out.split() else None


def _app_branch(repo_name, version):
    minor = version.rpartition(".")[0]
    return f"branch-{minor}-ee" if repo_name == "hopsworks-ee" else f"branch-{minor}"


def _values(helm, tag):
    """Every Helm value of every chart at ``tag``, as ``chart:path -> default``."""
    values = {}
    paths = [
        p
        for p in _git(helm, "ls-tree", "-r", "--name-only", tag).split()
        if re.fullmatch(r"(charts/[^/]+/)?values\.yaml", p)
    ]
    for path in paths:
        chart = path.split("/")[1] if path.startswith("charts/") else "(umbrella)"
        for key, value in _flatten(_load(helm, tag, path) or {}):
            values[f"{chart}:{key}"] = value
    return values


def _parents(key):
    """``chart:a``, ``chart:a.b``, ... up to ``key`` itself."""
    chart, _, path = key.partition(":")
    parts = re.split(r"\.(?![^\[]*\])", path)
    return [f"{chart}:{'.'.join(parts[: i + 1])}" for i in range(len(parts))]


def _subtrees(keys, other):
    """``keys`` with each subtree that ``other`` has nothing of collapsed to one line."""
    present = {parent for key in other for parent in _parents(key)}
    groups = {}
    for key in keys:
        if VERSION_LEAF.search(key):
            continue
        root = next(p for p in _parents(key) if p not in present)
        groups.setdefault(root, []).append(key)
    return sorted(
        root
        if members == [root]
        else f"{root}.* ({len(members)} value{'s' if len(members) > 1 else ''})"
        for root, members in groups.items()
    )


def _values_diff(helm, old, new):
    before, after = _values(helm, old), _values(helm, new)
    added = _subtrees(after.keys() - before.keys(), before)
    removed = _subtrees(before.keys() - after.keys(), after)
    changed = sorted(
        (k, before[k], after[k])
        for k in before.keys() & after.keys()
        if before[k] != after[k] and not VERSION_LEAF.search(k)
    )
    return added, removed, changed


def _added_lines(repo, old, new, *paths, pattern):
    diff = _git(repo, "diff", old, new, "--", *paths)
    current, hits = None, []
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line.removeprefix("+++ b/")
        elif (
            line.startswith("+")
            and not line.startswith("+++")
            and re.search(pattern, line)
        ):
            hits.append(f"{current}: {line[1:].strip()}")
    return hits


def _shipped_in(repo, line_tags, keys_of):
    """Map a commit subject key to the first tag of ``line_tags`` that has it."""
    first = {}
    for previous, tag in zip(line_tags, line_tags[1:]):
        for _, subject in keys_of(repo, previous, tag):
            first.setdefault(_key(subject), tag)
    return first


def _section(lines, title, rows, empty="None."):
    lines += ["", f"## {title}", ""]
    lines += rows or [empty]


def release_inputs(
    release: Annotated[str, typer.Argument(help="The release, e.g. 5.1.0.")],
    helm: Annotated[
        Path, typer.Option(help="A hopsworks-helm checkout with its tags.")
    ] = SOURCES / "hopsworks-helm",
    rondb_helm: Annotated[
        Path, typer.Option(help="A rondb-helm checkout with its tags.")
    ] = SOURCES / "rondb-helm",
    ee: Annotated[
        Path, typer.Option(help="A hopsworks-ee checkout with origin/branch-X.Y-ee.")
    ] = SOURCES / "hopsworks-ee",
    front: Annotated[
        Path, typer.Option(help="A hopsworks-front checkout with origin/branch-X.Y.")
    ] = SOURCES / "hopsworks-front",
    docker_images: Annotated[
        Path, typer.Option(help="A docker-images checkout.")
    ] = SOURCES / "docker-images",
):
    """Print the facts the release section of RELEASE is written from."""
    tag = f"v{release}"
    tags = _tags(helm)
    if tag not in tags:
        raise typer.BadParameter(f"{helm} has no tag {tag}; fetch its tags first")
    old, markers = _baseline(helm, tag)
    minor_zero = release.endswith(".0")
    since = old.removeprefix("v")
    lines = [f"# Inputs for {release}", ""]
    lines.append(
        f"Compares with {since}"
        + (
            f"; marks what shipped in {', '.join(m.removeprefix('v') for m in markers)}"
            if markers
            else ""
        )
        + "."
    )

    # Front matter
    base, client = _python_client(helm, docker_images, tag)
    app, old_app = _application(helm, tag), _application(helm, old)
    _section(
        lines,
        "Front matter",
        [
            f'released: "{_released(tag) or "?"}"  (GitHub release of {tag}; ? = not published yet or gh unavailable)',
            f'application: "{app}"  ({CHART} appVersion; {old_app} at {old})',
            f'python_client: "{client or "?"}"  (base_image_version {base}; docker-images base-image/hopsworks-api-version.txt)',
        ]
        + (
            [f'since: "{since}"  (only when the previous minor version has no page)']
            if minor_zero
            else []
        ),
    )

    # Chart commits
    chart = _range(helm, old, tag, same_line=not minor_zero)
    shipped = {}
    if minor_zero:
        shipped = _shipped_in(
            helm, [old, *markers], lambda r, a, b: _commits(r, f"{a}..{b}")
        )
    _section(
        lines,
        f"hopsworks-helm {old}..{tag} ({len(chart)} commits)",
        [
            f"- {sha} {subject}"
            + (
                f"  [shipped in {shipped[_key(subject)]}]"
                if _key(subject) in shipped
                else ""
            )
            for sha, subject in chart
        ],
    )

    # RonDB chart
    rondb = [_dependency(helm, t, RONDB_CHART, "rondb") for t in (old, tag)]
    rows = []
    if all(rondb) and rondb[0] != rondb[1]:
        rows = [f"rondb dependency {rondb[0]} -> {rondb[1]}"]
        if _release(f"v{rondb[1]}") < _release(f"v{rondb[0]}"):
            rows.append(
                "WARNING: the RonDB chart moves backwards; changes of the newer one are lost."
            )
        rows += [
            f"- {sha} {subject}"
            for sha, subject in _commits(rondb_helm, f"v{rondb[0]}..v{rondb[1]}")
        ]
    _section(lines, "rondb-helm", rows, empty=f"Unchanged ({rondb[1]}).")

    # Application commits
    for name, repo in (("hopsworks-ee", ee), ("hopsworks-front", front)):
        title = f"{name} {old_app} -> {app}"
        if app == old_app:
            _section(
                lines,
                title,
                [],
                empty="The application version is unchanged: no application changes.",
            )
            continue
        new_branch, old_branch = _app_branch(name, app), _app_branch(name, old_app)
        new_commit = _release_commit(repo, new_branch, app)
        old_commit = _release_commit(repo, old_branch, old_app)
        if not (new_commit and old_commit):
            _section(
                lines,
                title,
                [
                    f"ERROR: no `Release {app}` on origin/{new_branch} or `Release {old_app}` on origin/{old_branch}; fetch origin first."
                ],
            )
            continue
        commits = _range(
            repo, old_commit, new_commit, same_line=new_branch == old_branch
        )
        app_shipped = {}
        if minor_zero:
            line = [old_commit] + [
                c
                for c in (
                    _release_commit(repo, old_branch, _application(helm, m))
                    for m in markers
                )
                if c
            ]
            app_shipped = _shipped_in(
                repo,
                list(dict.fromkeys(line)),
                lambda r, a, b: _commits(r, f"{a}..{b}"),
            )
            app_of = {
                _release_commit(repo, old_branch, _application(helm, m)): m
                for m in markers
            }
            app_shipped = {k: app_of.get(v, v) for k, v in app_shipped.items()}
        _section(
            lines,
            f"{title}: {old_commit}..{new_commit} ({len(commits)} commits)",
            [
                f"- {sha} {subject}"
                + (
                    f"  [shipped in {app_shipped[_key(subject)]}]"
                    if _key(subject) in app_shipped
                    else ""
                )
                for sha, subject in commits
            ],
        )

    # Values
    added, removed, changed = _values_diff(helm, old, tag)
    _section(lines, "Helm values added", [f"- {k}" for k in added])
    _section(lines, "Helm values removed", [f"- {k}" for k in removed])
    _section(
        lines,
        "Helm defaults changed",
        [f"- {k}: {a!r} -> {b!r}" for k, a, b in changed],
    )
    _section(
        lines,
        "Newly deprecated (added lines mentioning deprecation)",
        _added_lines(
            helm,
            old,
            tag,
            "*values.yaml",
            "*values.schema.json",
            "*README.md",
            pattern=r"(?i)deprecat",
        ),
    )
    other = [
        p
        for p in _git(helm, "diff", "--name-only", old, tag).split()
        if re.search(r"(^|/)(values\.[\w-]+\.yaml|UPGRADE\.md|HELM4_MIGRATION\.md)$", p)
    ]
    _section(
        lines, "Changed values overlays and upgrade docs", [f"- {p}" for p in other]
    )

    # Components
    uncovered = _uncovered(helm, rondb_helm, old, tag)
    table = _table(helm, rondb_helm, old, tag, markers)
    _section(
        lines,
        "Upgraded components",
        (
            [f"WARNING: no component covers {c}" for c in uncovered] + [""]
            if uncovered
            else []
        )
        + [table.rstrip() or "No components changed."],
    )

    # What an X.Y.0 includes from the previous minor version
    if minor_zero and markers:
        rows = []
        content = {_key(s) for _, s in _commits(helm, tag)}
        for previous, patch in zip([old, *markers], markers):
            missing = [
                f"{sha} {s}"
                for sha, s in _commits(helm, f"{previous}..{patch}")
                if _key(s) not in content and not s.startswith("Release ")
            ]
            state = (
                f"{len(missing)} chart commits not in {tag}"
                if missing
                else "all chart commits included"
            )
            rows.append(
                f"- {patch.removeprefix('v')} (released {_released(patch) or '?'}): {state}"
            )
            rows += [f"    - {m}" for m in missing]
        _section(
            lines,
            f"Patch releases of {since.rpartition('.')[0]} in {release} (by commit subject)",
            rows,
        )

    typer.echo("\n".join(lines))
