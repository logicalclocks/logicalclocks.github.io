"""Collect the facts a release section is written from.

Prints, for one ``hopsworks-helm`` release, the release it compares with, its front
matter, the commits of the chart, of ``rondb-helm``, of the application it ships
(``hopsworks-ee``, ``hopsworks-front``), of the Python client and of every other
component the chart deploys from a Hopsworks repo whose version changed (``REPOS``),
the Helm values it adds, removes or changes,
what the chart newly deprecates, the upgrade guide sections its Upgrade steps link,
its upstream chart dependency changes and the Upgraded components table, as
``.claude/docs/releases.md`` describes. The ``/release-notes`` skill writes the
section from this; nothing here is published, so it names commits freely.
"""

import json
import re
import subprocess
from functools import cache
from pathlib import Path
from typing import Annotated

import typer
from hopsworks_docs.scripts.release_components import (
    SKIPPED,
    UMBRELLA,
    _baseline,
    _change,
    _covered,
    _dependency,
    _flatten,
    _git,
    _load,
    _release,
    _remote,
    _require,
    _table,
    _uncovered,
    _versions,
)
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


HELM_REPO = "logicalclocks/hopsworks-helm"
CHART = "charts/hopsworks/Chart.yaml"
VALUES = "charts/hopsworks/values.yaml"
RONDB_CHART = "charts/rondb/Chart.yaml"
# Pins the Python client of the base images from before hopsworks-api-version.txt.
CLIENT_PIN = "base-image/internal-base/python_install.sh"
# A merge suffix such as "(#1234)", a backport marker such as "(5.0)", "[branch-5.1]"
# or "(5.0 backport)", or a trailing Jira link.
SUBJECT_NOISE = re.compile(
    r"\s*(\(#\d+\)|\((\d+\.\d+|branch-\d+\.\d+)( backport)?\)|\[(branch-)?\d+\.\d+\]"
    r"|\(backport to branch-\d+\.\d+\)|https://hopsworks\.atlassian\.net/browse/[A-Z]+-\d+)\s*"
)
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
TICKET = re.compile(r"^(\[[A-Z][A-Z0-9]+-\d+\]|[A-Z][A-Z0-9]+-\d+:)")
GUIDE = "docs/setup_installation/admin/upgrade.md"
GUIDE_URL = "https://docs.hopsworks.ai/{}/setup_installation/admin/upgrade/#{}"
# Only headings that set their anchor are seen, so every section heading but Introduction sets one.
GUIDE_HEADING = re.compile(r"^(##+) (.+?) \{ #([\w-]+) \}$", re.MULTILINE)
RELEASE_BRANCH = re.compile(r"^[^/]+/branch-(\d+)\.(\d+)$")


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
    equivalent of (``--cherry-pick``), or no commit with the same subject since
    their merge base, as a backport that needed conflicts resolved has.
    """
    if same_line:
        return _commits(repo, f"{old}..{new}")
    commits = _commits(repo, "--cherry-pick", "--right-only", f"{old}...{new}")
    try:
        base = _git(repo, "merge-base", old, new).strip()
    except subprocess.CalledProcessError:
        return commits
    shipped = {_key(subject) for _, subject in _commits(repo, f"{base}..{old}")}
    return [(sha, subject) for sha, subject in commits if _key(subject) not in shipped]


@cache
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


@cache
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
        except subprocess.CalledProcessError:
            continue
        try:
            return base, _git(
                images, "show", f"{commit}:base-image/hopsworks-api-version.txt"
            ).strip()
        except subprocess.CalledProcessError:
            pass
        try:
            pin = re.search(
                r"hopsworks\[[^\]]*\]==([\w.]+)",
                _git(images, "show", f"{commit}:{CLIENT_PIN}"),
            )
        except subprocess.CalledProcessError:
            pin = None
        return base, pin and pin[1]
    return base, None


@cache
def _release_commit(repo, branch, version):
    """The ``Release X.Y.Z`` (or ``Release for X.Y.Z``) commit of an application version."""
    pattern = rf"^Release (for )?{re.escape(version)}( \(#[0-9]+\))?$"
    ref = f"{_remote(repo)}/{branch}"
    out = _git(repo, "log", ref, "-E", f"--grep={pattern}", "--format=%h")
    return out.split()[0] if out.split() else None


@cache
def _version_ref(repo, version):
    """The tag or release commit of ``version`` in ``repo``, or None.

    A tag named after the version, else the newest ``Release <version>`` or
    ``[maven-release-plugin] prepare release <version>`` commit on the logicalclocks
    remote.
    """
    for name in (version, f"v{version}"):
        if _git(repo, "tag", "--list", name).strip():
            return name
    v = re.escape(version)
    pattern = (
        rf"^(Release (for )?v?{v}|\[maven-release-plugin\] prepare release {v})( |\(|$)"
    )
    remotes = f"--remotes={_remote(repo)}"
    out = _git(repo, "log", remotes, "-E", f"--grep={pattern}", "--format=%h")
    if out.split():
        return out.split()[0]
    # A repo that releases by setting its version file, newest such commit first.
    for path in ("version.txt", "VERSION"):
        for commit in _git(repo, "log", remotes, "--format=%h", "--", path).split():
            try:
                if _git(repo, "show", f"{commit}:{path}").strip() == version:
                    return commit
            except subprocess.CalledProcessError:
                continue
    # An image rebuild, such as Trino 483-v2, is the source release 483.
    rebuild = re.fullmatch(r"(.+)-v\d+", version)
    return _version_ref(repo, rebuild[1]) if rebuild else None


def _fork_branch(repo, version):
    """The release branch of a fork that ``version`` is built from, or None.

    The longest ``branch-*`` or ``release-*`` of the logicalclocks remote whose name
    starts the version, such as ``origin/branch-4.1`` for Hive 4.1.0.0-v1.
    """
    remote = _remote(repo)
    refs = _git(
        repo, "for-each-ref", "--format=%(refname:short)", f"refs/remotes/{remote}"
    ).split()
    branches = [
        ref
        for ref in refs
        if (name := re.fullmatch(rf"{re.escape(remote)}/(?:branch|release)-(.+)", ref))
        and re.match(rf"{re.escape(name[1])}([.-]|$)", version)
    ]
    return max(branches, key=len, default=None)


def _fork_section(lines, title, repo, version, since, until):
    """The Hopsworks commits of a fork made between two chart releases.

    Those on the release branch ``version`` is built from, else on any branch.
    """
    branch = _fork_branch(repo, version)
    out = _git(
        repo,
        "log",
        branch or f"--remotes={_remote(repo)}",
        "--no-merges",
        f"--since={since}T00:00:00",
        f"--until={until}T23:59:59",
        "--format=%h\t%s",
    )
    seen, rows = set(), []
    for line in out.splitlines():
        sha, subject = line.split("\t", 1)
        if TICKET.match(subject) and _key(subject) not in seen:
            seen.add(_key(subject))
            rows.append(f"- {sha} {subject}")
    note = (
        f"Approximate, by date and ticket key on {branch or 'every branch'}: "
        "check each against the release branch."
    )
    _section(
        lines,
        f"{title}: Hopsworks commits from {since} to {until} ({len(rows)})",
        [note, "", *rows] if rows else [],
        empty="No Hopsworks commits in that window.",
    )


def _repo_section(lines, title, repo, old_version, new_version, window=None, line=()):
    """The commits of ``repo`` between two versions, or why they can't be listed.

    For a fork, the Hopsworks commits made within ``window``, two dates. ``line`` is
    the (tag, version) of the baseline and of each marker, for ``[shipped in]``.
    """
    if not (repo / ".git").exists():
        _section(
            lines, title, [f"ERROR: no checkout at {repo}; clone it and run again."]
        )
        return
    if repo.name in FORKS and window and all(window):
        _fork_section(lines, title, repo, new_version, *window)
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
    shipped = _shipped_in(repo, [(t, v and _version_ref(repo, v)) for t, v in line])
    _section(
        lines,
        f"{title}: {old_ref}..{new_ref} ({len(commits)} commits)",
        _rows(commits, shipped),
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


def _in_table():
    """The values whose version the Upgraded components table shows, as ``chart:key``."""
    keys = set()
    for ref in _covered():
        path, _, key = ref.partition(":")
        if subchart := UMBRELLA.fullmatch(path):
            keys.add(f"{subchart[1]}:{key}")
        elif path == "values.yaml":
            keys.add(f"(umbrella):{key}")
    return keys


def _subtrees(keys, other):
    """``keys`` with each subtree that ``other`` has nothing of collapsed to one line."""
    present = {parent for key in other for parent in _parents(key)}
    groups = {}
    for key in keys:
        # A value that is a leaf here and a map in ``other`` has every parent present.
        root = next((p for p in _parents(key) if p not in present), key)
        groups.setdefault(root, []).append(key)
    return sorted(
        root
        if members == [root]
        else f"{root}.* ({len(members)} value{'s' if len(members) > 1 else ''})"
        for root, members in groups.items()
    )


def _values_diff(helm, old, new):
    before, after = _values(helm, old), _values(helm, new)
    table = _in_table()
    added = _subtrees(after.keys() - before.keys(), before)
    removed = _subtrees(before.keys() - after.keys(), after)
    both = before.keys() & after.keys()
    # A subchart default the umbrella sets in both releases isn't the one deployed.
    changed = sorted(
        (k, before[k], after[k])
        for k in both
        if before[k] != after[k]
        and k not in table
        and "(umbrella):" + k.replace(":", ".", 1) not in both
    )
    return added, removed, changed


def _dependencies(helm, tag):
    """``chart:dependency -> version`` of the upstream charts every chart depends on."""
    return {
        f"{path.split('/')[1]}:{d['name']}": d.get("version")
        for path in _git(helm, "ls-tree", "-r", "--name-only", tag).split()
        if re.fullmatch(r"charts/[^/]+/Chart\.yaml", path)
        for d in (_load(helm, tag, path) or {}).get("dependencies") or []
        if not d.get("repository", "").startswith("file://")
    }


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


def _shipped_in(repo, line):
    """Map a commit subject key to the first marker whose ref has it.

    ``line`` is the (tag, ref) of the baseline and then of each marker, oldest first,
    with no ref where ``repo`` has none for that release.
    """
    first = {}
    if not (line and line[0][1]):
        return first
    refs = [(tag, ref) for tag, ref in line if ref]
    for (_, previous), (tag, ref) in zip(refs, refs[1:]):
        for _, subject in _commits(repo, f"{previous}..{ref}"):
            first.setdefault(_key(subject), tag)
    return first


def _rows(commits, shipped):
    return [
        f"- {sha} {subject}"
        + (
            f"  [shipped in {shipped[_key(subject)]}]"
            if _key(subject) in shipped
            else ""
        )
        for sha, subject in commits
    ]


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
        _DOCS_ROOT,
        "for-each-ref",
        "--format=%(refname:short)",
        f"refs/remotes/{_remote(_DOCS_ROOT)}",
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
    _require(helm, rondb_helm, ee, front, docker_images, api)
    tag = f"v{release}"
    tags = _tags(helm)
    if tag not in tags:
        raise typer.BadParameter(f"{helm} has no tag {tag}; fetch its tags first")
    old, markers = _baseline(helm, tag)
    minor_zero = release.endswith(".0")
    # The baseline and every marker, for [shipped in]; patches mark nothing.
    line = [old, *markers] if minor_zero else []
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
    _section(
        lines,
        f"hopsworks-helm {old}..{tag} ({len(chart)} commits)",
        _rows(chart, _shipped_in(helm, [(t, t) for t in line])),
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
        rondb_line = [(t, _dependency(helm, t, RONDB_CHART, "rondb")) for t in line]
        rows += _rows(
            _commits(rondb_helm, f"v{rondb[0]}..v{rondb[1]}"),
            _shipped_in(rondb_helm, [(t, d and f"v{d}") for t, d in rondb_line]),
        )
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
            remote = _remote(repo)
            _section(
                lines,
                title,
                [
                    f"ERROR: no `Release {app}` on {remote}/{new_branch} or `Release {old_app}` on {remote}/{old_branch}; fetch {remote} first."
                ],
            )
            continue
        commits = _range(
            repo, old_commit, new_commit, same_line=new_branch == old_branch
        )
        app_line = [
            (t, _release_commit(repo, old_branch, _application(helm, t))) for t in line
        ]
        _section(
            lines,
            f"{title}: {old_commit}..{new_commit} ({len(commits)} commits)",
            _rows(commits, _shipped_in(repo, app_line)),
        )

    # Python client, base environment images and the other components
    old_base, old_client = _python_client(helm, docker_images, old)
    images_line = [(t, _python_client(helm, docker_images, t)) for t in line]
    no_base = f"ERROR: the chart sets no base_image_version at {old if base else tag}."
    if not (old_base and base):
        _section(lines, "hopsworks-api", [no_base])
    elif not (old_client and client):
        unresolved = old_base if client else base
        _section(
            lines,
            "hopsworks-api",
            [
                f"ERROR: no hopsworks-api version for base_image_version {unresolved} "
                f"in {docker_images}; fetch docker-images and run again."
            ],
        )
    elif old_client != client:
        _repo_section(
            lines,
            f"hopsworks-api {old_client} -> {client}",
            api,
            old_client,
            client,
            line=[(t, c) for t, (_, c) in images_line],
        )
    else:
        _section(lines, "hopsworks-api", [], empty=f"Unchanged ({client}).")
    if not (old_base and base):
        _section(lines, "docker-images", [no_base])
    elif old_base != base:
        _repo_section(
            lines,
            f"docker-images {old_base} -> {base} (base environment images, and the "
            "other images it builds)",
            docker_images,
            old_base,
            base,
            line=[(t, b) for t, (b, _) in images_line],
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
    shipped = [(t, _versions(helm, rondb_helm, t)) for t in line]
    by_repo = {}
    for component, repo_name in REPOS.items():
        was, now = _change(before[component], after[component])
        if was and now and was != now:
            by_repo.setdefault((repo_name, was, now), []).append(component)
    for (repo_name, was, now), components in sorted(by_repo.items()):
        _repo_section(
            lines,
            f"{repo_name} {was} -> {now} ({', '.join(components)})",
            sources / repo_name,
            was,
            now,
            window=(_released(old), _released(tag)),
            line=[
                (t, _change(before[components[0]], v[components[0]])[1])
                for t, v in shipped
            ],
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
    deps = _dependencies(helm, old), _dependencies(helm, tag)
    _section(
        lines,
        "Upstream chart dependencies changed (the table covers only the images they "
        "pin or UPSTREAM_DEFAULTS lists)",
        [
            f"- {k}: {deps[0].get(k) or 'none'} -> {deps[1].get(k) or 'removed'}"
            for k in sorted(deps[0].keys() | deps[1].keys())
            if deps[0].get(k) != deps[1].get(k)
        ],
    )
    uncovered = _uncovered(helm, rondb_helm, old, tag)
    table, left_out = _table(helm, rondb_helm, old, tag, markers)
    notes = [f"WARNING: no component covers {c}" for c in uncovered]
    notes += [f"WARNING: {s}; its values and versions are missing" for s in SKIPPED]
    notes += [f"{n}; it belongs in the notes" for n in left_out]
    _section(
        lines,
        "Upgraded components",
        ([*notes, ""] if notes else []) + [table.rstrip() or "No components changed."],
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
