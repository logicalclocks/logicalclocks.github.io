"""Collect the facts a release section is written from.

Prints, for one ``hopsworks-helm`` release, the release it compares with, its front
matter, the commits of the chart, of ``rondb-helm``, of the application it ships
(``hopsworks-ee``, ``hopsworks-front``), of the Python client and of every other
component the chart deploys from a Hopsworks repo whose version changed (``REPOS``),
the Helm values it adds, removes or changes,
what the chart newly deprecates, the upgrade guide sections its Upgrade steps link,
and the Upgraded components table, as
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
    _versions,
)
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


HELM_REPO = "logicalclocks/hopsworks-helm"
CHART = "charts/hopsworks/Chart.yaml"
VALUES = "charts/hopsworks/values.yaml"
RONDB_CHART = "charts/rondb/Chart.yaml"
# A merge suffix such as "(#1234)", or a backport marker such as "(5.0)" or "[5.1]".
SUBJECT_NOISE = re.compile(r"\s*(\(#\d+\)|\(\d+\.\d+\)|\[\d+\.\d+\])\s*")
# The checkouts default to siblings of this repo, as CI clones hopsworks-api.
SOURCES = _DOCS_ROOT.parent
# The repo that builds a component of the Upgraded components table, for the
# components built by Hopsworks; HopsFS and RonDB are left out on purpose.
# docker-images, which builds the base environment images and many other images,
# hopsworks-ee, hopsworks-front and hopsworks-api have their own sections.
REPOS = {
    "ArrowFlight server": "flyingduck",
    "Git image": "hops-git",
    "Hive Metastore": "hive",
    "Hudi bundle of the Hive Metastore": "hudi",
    "Inference logger": "model-serving-webhook",
    "Model serving authenticator": "model-serving-authenticator",
    "Model serving webhook": "model-serving-webhook",
    "OnlineFS": "clusterj-onlinefs",
    "Remote shuffle service (Apache Uniffle)": "incubator-uniffle",
    "Spark": "spark",
    "Spark history server": "sparkhistoryserver",
    "Storage initializer": "model-serving-webhook",
    "Toolbox image (hwutils)": "tools",
    "Trino": "trino",
}
# Forks of upstream projects: Upgraded components covers their upstream changes, so
# only Hopsworks commits, whose subject starts with a ticket key, are listed.
FORKS = {"hive", "hudi", "incubator-uniffle", "spark", "trino"}
TICKET = re.compile(r"^\[?[A-Z][A-Z0-9]+-\d+\]")
# A version setting; the Upgraded components table covers these.
VERSION_LEAF = re.compile(r"(^|[._])(tag|version|image|digest)$", re.IGNORECASE)
GUIDE = "docs/setup_installation/admin/upgrade.md"
GUIDE_URL = "https://docs.hopsworks.ai/{}/setup_installation/admin/upgrade/#{}"
# Every heading of the upgrade guide sets its anchor.
GUIDE_HEADING = re.compile(r"^(##+) (.+?) \{ #([\w-]+) \}$", re.MULTILINE)
RELEASE_BRANCH = re.compile(r"^origin/branch-(\d+)\.(\d+)$")


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
    """The ``Release X.Y.Z`` (or ``Release for X.Y.Z``) commit of an application version."""
    pattern = rf"^Release (for )?{re.escape(version)}( \(#[0-9]+\))?$"
    out = _git(
        repo, "log", f"origin/{branch}", "-E", f"--grep={pattern}", "--format=%h"
    )
    return out.split()[0] if out.split() else None


def _version_ref(repo, version):
    """The tag or release commit of ``version`` in ``repo``, or None.

    A tag named after the version, else the newest ``Release <version>`` or
    ``[maven-release-plugin] prepare release <version>`` commit on origin.
    """
    for name in (version, f"v{version}"):
        if _git(repo, "tag", "--list", name).strip():
            return name
    v = re.escape(version)
    pattern = (
        rf"^(Release (for )?v?{v}|\[maven-release-plugin\] prepare release {v})( |\(|$)"
    )
    out = _git(
        repo, "log", "--remotes=origin", "-E", f"--grep={pattern}", "--format=%h"
    )
    if out.split():
        return out.split()[0]
    # A repo that releases by setting its version file, newest such commit first.
    for path in ("version.txt", "VERSION"):
        for commit in _git(
            repo, "log", "--remotes=origin", "--format=%h", "--", path
        ).split():
            try:
                if _git(repo, "show", f"{commit}:{path}").strip() == version:
                    return commit
            except subprocess.CalledProcessError:
                continue
    # An image rebuild, such as Trino 483-v2, is the source release 483.
    rebuild = re.fullmatch(r"(.+)-v\d+", version)
    return _version_ref(repo, rebuild[1]) if rebuild else None


def _fork_section(lines, title, repo, since, until):
    """The Hopsworks commits of a fork made between two chart releases."""
    out = _git(
        repo,
        "log",
        "--remotes=origin",
        "--no-merges",
        f"--since={since}",
        f"--until={until}",
        "--format=%h\t%s",
    )
    seen, rows = set(), []
    for line in out.splitlines():
        sha, subject = line.split("\t", 1)
        if TICKET.match(subject) and _key(subject) not in seen:
            seen.add(_key(subject))
            rows.append(f"- {sha} {subject}")
    note = "Approximate, by date and ticket key: check each against the release branch."
    _section(
        lines,
        f"{title}: Hopsworks commits from {since} to {until} ({len(rows)})",
        [note, "", *rows] if rows else [],
        empty="No Hopsworks commits in that window.",
    )


def _repo_section(lines, title, repo, old_version, new_version, window=None):
    """The commits of ``repo`` between two versions, or why they can't be listed.

    For a fork, the Hopsworks commits made within ``window``, two dates.
    """
    if not (repo / ".git").exists():
        _section(
            lines, title, [f"ERROR: no checkout at {repo}; clone it and run again."]
        )
        return
    if repo.name in FORKS and window and all(window):
        _fork_section(lines, title, repo, *window)
        return
    old_ref, new_ref = _version_ref(repo, old_version), _version_ref(repo, new_version)
    if not (old_ref and new_ref):
        missing = [
            v for v, r in ((old_version, old_ref), (new_version, new_ref)) if not r
        ]
        _section(
            lines,
            title,
            [
                f"No tag or release commit for {', '.join(missing)} in {repo.name}; "
                "find the commits between the two versions by hand, for example from "
                "the version bump commits or the release branches."
            ],
        )
        return
    commits = _range(repo, old_ref, new_ref, same_line=False)
    _section(
        lines,
        f"{title}: {old_ref}..{new_ref} ({len(commits)} commits)",
        [f"- {sha} {subject}" for sha, subject in commits],
    )


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


def _upgrade_guide(release, since):
    """The upgrade guide sections an upgrade to RELEASE follows, as rows.

    An X.Y.0 follows the section from the previous minor version, a patch release
    its ``Changes from X.Y.Z`` section, read from the oldest release branch of this
    repo, from the release's minor version on, whose guide has it.
    """
    minor = tuple(int(p) for p in release.split(".")[:2])
    if release.endswith(".0"):
        title = f"{since.rpartition('.')[0]}.x to {release.rpartition('.')[0]}.x"
    else:
        title = f"Changes from {release}"
    refs = _git(
        _DOCS_ROOT, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin"
    ).split()
    branches = sorted(
        ((int(m[1]), int(m[2])), ref)
        for ref in refs
        if (m := RELEASE_BRANCH.match(ref))
    )
    for version, ref in branches:
        if version < minor:
            continue
        try:
            guide = _git(_DOCS_ROOT, "show", f"{ref}:{GUIDE}")
        except subprocess.CalledProcessError:
            continue
        headings = GUIDE_HEADING.findall(guide)
        start = next(
            (i for i, h in enumerate(headings) if h[:2] == ("##", title)), None
        )
        if start is None:
            continue
        docs = "{}.{}".format(*version)
        rows = [f"From {ref}:{GUIDE}; link the {docs} docs.", ""]
        if release.endswith(".0"):
            before = next(h for h in headings if h[1] == "Before every upgrade")
            rows.append(f"- {before[1]}: {GUIDE_URL.format(docs, before[2])}")
        rows.append(f"- {title}: {GUIDE_URL.format(docs, headings[start][2])}")
        for level, text, anchor in headings[start + 1 :]:
            if level == "##":
                break
            rows.append(f"    - {text}: {GUIDE_URL.format(docs, anchor)}")
        return rows
    return [
        f"No release branch from {minor[0]}.{minor[1]} on has the section {title!r}."
    ]


def _section(lines, title, rows, empty="None."):
    lines += ["", f"## {title}", ""]
    lines += rows or [empty]


def release_inputs(
    release: Annotated[str, typer.Argument(help="The release, e.g. 5.1.0.")],
    sources: Annotated[
        Path,
        typer.Option(
            help="The directory holding the checkouts of hopsworks-helm, rondb-helm, "
            "hopsworks-ee, hopsworks-front, hopsworks-api, docker-images and the repos "
            "in REPOS, each fetched with its tags and release branches."
        ),
    ] = SOURCES,
):
    """Print the facts the release section of RELEASE is written from."""
    helm, rondb_helm = sources / "hopsworks-helm", sources / "rondb-helm"
    ee, front = sources / "hopsworks-ee", sources / "hopsworks-front"
    docker_images, api = sources / "docker-images", sources / "hopsworks-api"
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
    lines.append(
        f"Application {app} ({CHART} appVersion; {old_app} at {old}); it sets the "
        "hopsworks-ee and hopsworks-front ranges below and isn't part of the page."
    )
    _section(
        lines,
        "Front matter",
        [
            f'released: "{_released(tag) or "?"}"  (GitHub release of {tag}; ? = not published yet or gh unavailable)',
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

    # Python client, base environment images and the other components
    old_base, old_client = _python_client(helm, docker_images, old)
    if old_client and client and old_client != client:
        _repo_section(
            lines, f"hopsworks-api {old_client} -> {client}", api, old_client, client
        )
    else:
        _section(lines, "hopsworks-api", [], empty=f"Unchanged ({client}).")
    if old_base and base and old_base != base:
        _repo_section(
            lines,
            f"docker-images {old_base} -> {base} (base environment images, and the "
            "other images it builds)",
            docker_images,
            old_base,
            base,
        )
    else:
        _section(
            lines,
            "docker-images",
            [],
            empty=f"Base environment images unchanged ({base}); images docker-images "
            "builds for other components may still have changed, see Upgraded components.",
        )
    before, after = _versions(helm, rondb_helm, old), _versions(helm, rondb_helm, tag)
    by_repo = {}
    for component, repo_name in REPOS.items():
        if (
            before.get(component)
            and after.get(component)
            and before[component] != after[component]
        ):
            by_repo.setdefault(
                (repo_name, before[component], after[component]), []
            ).append(component)
    for (repo_name, was, now), components in sorted(by_repo.items()):
        _repo_section(
            lines,
            f"{repo_name} {was} -> {now} ({', '.join(components)})",
            sources / repo_name,
            was,
            now,
            window=(_released(old), _released(tag)),
        )
    unchanged = sorted({REPOS[c] for c in REPOS} - {r for r, _, _ in by_repo})
    _section(lines, "Component repos with no version change", [", ".join(unchanged)])

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
        if re.search(r"(^|/)values\.[\w-]+\.yaml$", p)
    ]
    _section(lines, "Changed values overlays", [f"- {p}" for p in other])
    _section(lines, "Upgrade guide", _upgrade_guide(release, since))

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
