"""Check that every docs version shows the release pages of main.

Each docs build writes ``releases/fingerprint.txt`` (see ``releases_hook.py``). A
version is current when its fingerprint matches main at the checked-out commit or
at a later commit, so a check racing a newer main build doesn't fail. Versions are
main (``dev``) and every ``branch-X.Y`` that has the hook.
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from typing import Annotated

import typer
from hopsworks_docs.scripts.releases_hook import digest
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


HOOK = "scripts/releases_hook.py"
SOURCES = "docs/releases"
WORKFLOW = "mkdocs-release.yml"
ATTEMPTS = 3


def _run(*args, binary=False):
    result = subprocess.run(
        args, cwd=_DOCS_ROOT, capture_output=True, text=not binary, check=True
    )
    return result.stdout


def _fingerprint_at(ref):
    paths = _run("git", "ls-tree", "-r", "-z", "--name-only", ref, "--", SOURCES)
    sources = [
        (
            path.removeprefix(f"{SOURCES}/"),
            _run("git", "show", f"{ref}:{path}", binary=True),
        )
        for path in paths.split("\0")
        if path
    ]
    return digest(_run("git", "show", f"{ref}:{HOOK}", binary=True), sources)


def _accepted():
    """Fingerprints of main from HEAD to the latest origin/main."""
    later = _run("git", "rev-list", "HEAD..origin/main", "--", SOURCES, HOOK).split()
    return {_fingerprint_at(ref) for ref in ["HEAD", *later]}


def _versions():
    """(branch, docs version) of main and of every release branch with the hook."""
    versions = [("main", "dev")]
    refs = _run(
        "git",
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/origin/branch-*",
    ).split()
    for ref in refs:
        has_hook = subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{HOOK}"],
            cwd=_DOCS_ROOT,
            capture_output=True,
        )
        if has_hook.returncode == 0:
            branch = ref.removeprefix("origin/")
            versions.append((branch, branch.removeprefix("branch-")))
    return versions


def _deployed(version):
    shown = subprocess.run(
        ["git", "show", f"origin/gh-pages:{version}/releases/fingerprint.txt"],
        cwd=_DOCS_ROOT,
        capture_output=True,
        text=True,
    )
    return shown.stdout.strip() if shown.returncode == 0 else None


def _stale(versions):
    _run("git", "fetch", "--quiet", "origin")
    accepted = _accepted()
    return [
        (branch, version)
        for branch, version in versions
        if _deployed(version) not in accepted
    ]


def _dispatch(branch):
    """Run the docs workflow of ``branch`` and wait for it; return the finished run."""
    started = datetime.now().astimezone() - timedelta(seconds=10)
    _run("gh", "workflow", "run", WORKFLOW, "--ref", branch)
    for _ in range(30):
        time.sleep(10)
        runs = json.loads(
            _run(
                "gh",
                "run",
                "list",
                "--workflow",
                WORKFLOW,
                "--branch",
                branch,
                "--event",
                "workflow_dispatch",
                "--limit",
                "5",
                "--json",
                "databaseId,createdAt",
            )
        )
        new = [r for r in runs if datetime.fromisoformat(r["createdAt"]) >= started]
        if new:
            break
    else:
        return {"conclusion": "not started", "url": ""}
    while True:
        time.sleep(30)
        run = json.loads(
            _run(
                "gh",
                "run",
                "view",
                str(new[0]["databaseId"]),
                "--json",
                "status,conclusion,url",
            )
        )
        if run["status"] == "completed":
            return run


def sync_release_notes(
    rebuild: Annotated[
        bool,
        typer.Option(
            help="First rebuild each stale release branch with its own docs workflow."
        ),
    ] = False,
):
    """Check that every docs version shows the release pages of main."""
    versions = _versions()
    stale = _stale(versions)
    if rebuild:
        for branch, version in stale:
            # The main docs build deploys dev itself.
            if branch == "main":
                continue
            for attempt in range(1, ATTEMPTS + 1):
                run = _dispatch(branch)
                print(f"{version}: rebuild {attempt} {run['conclusion']} {run['url']}")
                # Another docs build can replace a queued run before it starts.
                if run["conclusion"] != "cancelled":
                    break
        stale = _stale(versions)

    for branch, version in versions:
        state = "stale" if (branch, version) in stale else "current"
        print(f"{version} ({branch}): {state}")
    if stale:
        names = ", ".join(version for _, version in stale)
        print(
            f"The release pages of {names} don't match main. "
            "Check the last docs build of each, fix it, and run this again.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
