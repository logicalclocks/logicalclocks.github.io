---
name: release-notes
description: Write the release notes of a hopsworks-helm release, such as 5.1.0, into docs/releases. Collects the changes of the release in the chart and in every Hopsworks repo whose component it moves, drafts its section, fact-checks every entry against the source and runs the strict build. Use when asked to write or add the release notes of a Hopsworks release.
argument-hint: <X.Y.Z>
---

# Release notes for a release

Writes the `## X.Y.Z` section of `docs/releases/X.Y/index.md` for the `hopsworks-helm` release given as the argument.
Read `.claude/docs/releases.md` in full first: it is the contract for the page shape and every writing rule, and this skill does not repeat it.

The work has four stages, each checked before the next: collect the facts, draft, fact-check, build.
A draft is never trusted: in the 2026-10 backfill, separate adversarial passes against the source changed about one drafted entry in six, many of them for a wrong claim.

## 0. Main only

Release notes are changed on `main` only, and reach the release branches from there: every docs version shows `main`'s `docs/releases/`, because the release branch builds copy it, the hook and the release pages' script and styles from `main` before they build, as `.claude/docs/releases.md` describes.
Work on a branch of `main` whose pull request goes to `main`, and check it before anything else.
`R` is the remote that points at `logicalclocks`: `origin` in a plain clone, `upstream` in a project of the workspaces repo, whose `origin` is your fork; the same holds in every checkout below.

```sh
R=origin   # or upstream, see git remote -v
git fetch $R main
git log --oneline $R/main..HEAD
```

It lists the commits the branch adds to `main`, which are only those of your change; a long list, or release commits of a `branch-X.Y`, means the branch is based on a release branch.

Stop and tell the user if the branch isn't based on `main` or its pull request targets a `branch-*`: never change `docs/releases/` on a release branch, nor cherry-pick a release notes change to one; CI fails such a pull request, and the next release branch build would overwrite it anyway.

## 1. Sources

The facts come from every repo the release ships, read-only, all checked out side by side in one directory:

- the charts, `hopsworks-helm` and `rondb-helm`;
- the application, `hopsworks-ee` and `hopsworks-front`, and the Python and Java clients, `hopsworks-api`;
- the images, `docker-images`, which builds the base environments and many other images;
- the components the chart deploys from a Hopsworks repo, as `REPOS` in `scripts/release_inputs.py` maps them: `flyingduck`, `clusterj-onlinefs`, `model-serving-webhook`, `model-serving-authenticator`, `hops-git`, `tools`, `sparkhistoryserver`, and the forks `trino`, `hive`, `hudi`, `incubator-uniffle` and `spark`.

HopsFS and RonDB repos are left out on purpose; `rondb-helm` stays.
They default to siblings of this repo; if one is missing, `release-inputs` and `release-components` fail with `ERROR: no checkout at <path>`, or `release-inputs` reports it in the section of a component repo, and you ask the user where it is or clone it.
Set `S` to the directory that holds them, and set up this repo's environment once, with the Python API the strict build of step 5 needs, as CI does; `uv sync` is exact and removes a Python API installed before it, so install the API after it.
Afterwards run every command with `uv run --no-sync`, because a plain `uv run` syncs the environment to the lock file again, which can change the packages the Python API installed:

```sh
S=<directory holding the checkouts>
uv sync --extra cli
uv pip install $S/hopsworks-api/python
```

Fetch every branch and tag of each checkout, and of this repo (links are checked against its `branch-*`, and `release-inputs` reads the upgrade guide from them), because a release often came out after the last fetch; component repos name their release branches in different ways, so fetch them all:

```sh
git -C <repo> fetch $R --tags
git -C <repo> fetch $R
```

Never check out, commit or reset in those repos; read them with `git log`, `git show`, `git diff` and `git grep`.

## 2. Collect the facts

```sh
mkdir -p .release-notes/<X.Y.Z>
uv run --no-sync hopsworks-docs release-inputs <X.Y.Z> --sources $S > .release-notes/<X.Y.Z>/inputs.md
```

`.release-notes/` is gitignored and lives in the repo, not in a temporary directory, so the work survives the session.
Read `inputs.md` in full.
It gives:

- the release it compares with, the front matter (release date, Python client), and the application version, which sets the `hopsworks-ee` and `hopsworks-front` ranges but isn't shown;
- every commit of the chart, of `rondb-helm` when the RonDB chart moved, and of `hopsworks-ee` and `hopsworks-front` between the `Release X.Y.Z` commits of the two application versions;
- the commits of `hopsworks-api` and `docker-images` between the Python client and base image versions of the two releases, and of each component repo whose version moved, between the tags or `Release` commits of its two versions;
  for a fork, only the Hopsworks commits (a ticket key in the subject) made between the two release dates on the release branch the new version is built from, or on every branch when none matches, because Upgraded components covers the upstream version;
  a fork checkout must fetch its release branches, which a narrow `remote.$R.fetch` doesn't (`git fetch $R +refs/heads/branch-483:refs/remotes/$R/branch-483`);
  a repo without a tag or release commit for a version says so, and you find its commits by hand;
  on an X.Y.0, the ranges leave out the changes the previous X.Y.0 already shipped through a backport;
- on an X.Y.0, `[shipped in vX.Y.Z]` on each commit of the charts, the application, `hopsworks-api`, `docker-images` and the component repos, except the forks, that a patch release of the previous minor version already shipped, naming the first one, also when the backport rewords the subject with `[branch-X.Y]`, `(branch-X.Y)`, `(X.Y backport)` or a trailing Jira URL, and which of those patch releases' chart commits the X.Y.0 lacks;
- the Helm values added and removed, and those changed except the versions the Upgraded components table shows and the subchart defaults the umbrella chart overrides, added lines that mention a deprecation, and the changed `values.*.yaml` overlays;
  it doesn't say which removed values the values schema now rejects or which hooks changed, so check `values.schema.json` and the hook templates of the chart at the tag yourself;
- the sections of the upgrade guide that `### Upgrade steps` links, with the docs version to link, or that the guide has none for the release;
- the upstream chart dependencies whose version changed, of which the table covers only the images they pin or `UPSTREAM_DEFAULTS` lists;
- the Upgraded components table, with a warning for a version no component covers and for a chart file it couldn't parse, and the components and images new or removed in the release, which belong in the notes.

Stop and ask the user when it reports an `ERROR` (a release commit it can't find, a Python client it can't resolve, or a checkout that is missing), a `released: "?"` (the GitHub release isn't published, or `gh` can't reach GitHub, which also leaves the fork sections without their date window), or a RonDB chart that moves backwards.

## 3. Draft

Add the release to the page first, so the section has a place:

- its entry in the front matter `releases:` map, newest first, with the release date and Python client from `inputs.md` as quoted strings;
- `## X.Y.Z { #hopsworks-X-Y-Z }` in release order, newest first;
- for a new minor version, `docs/releases/X.Y/index.md` with `# Release notes { #hopsworks-X-Y }` and `The releases of Hopsworks X.Y, newest first.`, modelled on an existing minor page.

Then turn the facts into entries.
Account for every commit and every value change: in an entry, in an existing entry it supports, or in the left-out list of the report.

- An X.Y.0 repeats the entries of the previous minor version's patch releases rather than drafting new ones for the commits marked `[shipped in ...]`: copy each patch entry into the same subsection, end its first line with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, point its docs links at the X.Y.0's minor version, and check that the change is in the X.Y.0 and still described correctly there.
  Leave out what the X.Y.0 lacks, as the "Patch releases" part of `inputs.md` shows, and say so in a breaking change.
  A commit shipped in a patch release that came out after the X.Y.0 gets an entry with the same marker.
- Commits of different repos with the same ticket key (`[HWORKS-1234]`) are one entry, unless the ticket bundles unrelated changes, which get one entry each.
- A change that also ships in a patch release of another minor version is listed in both releases, without a marker; check the ticket keys of a patch release against the other minor versions' patch releases of the same days.
- Read the diff of every commit you turn into an entry; a subject can promise more than the code does, and a later commit in the range can change or revert it.

For up to about 40 commits, draft it yourself.
Above that, split the commits into slices of about 40 (chart, rondb-helm, ee, front, api, images, components, values) and give each slice to a parallel agent at medium effort with `draft.md` in this folder as its brief, the slice, and the paths.
Agents return entries with evidence and never edit the page; you merge their entries into the section, so no two writers touch one file.

Write `### Upgrade steps` as the guide says, linking the upgrade guide sections `inputs.md` lists.
Read those sections, and list in the report the steps the release needs at upgrade that they lack, from a migration Job or hook, or a breaking change that has to happen before or after the `helm upgrade`, so the user can add them to the guide.

Sort the entries of each subsection by first tag and within a tag by significance, as the guide defines it, after merging; the agents' order only holds within their slice.

Generate the table last:

```sh
uv run --no-sync hopsworks-docs release-components <X.Y.Z> --helm $S/hopsworks-helm --rondb-helm $S/rondb-helm --write
```

If it fails on a version no component covers, add the component to `COMPONENTS` in `scripts/release_components.py`, or the setting to `IGNORED` when it only looks like a version, rather than editing the table by hand.
Remove link definitions that no entry uses any more; markdownlint fails on them.

A patch of a minor version that is no longer the newest also updates the X.Y.0 of the next minor version, which lists its backports with `(also in ...)`, as the guide says.
Run `release-inputs` for that X.Y.0, which marks the commits the patch shipped with `[shipped in vX.Y.Z]`, add the marker to the entries of those commits, add an entry with the marker for a commit that has none, and regenerate its table with `release-components <X.Y.0> --write`.

## 4. Fact-check

Give the drafted section to fresh agents at medium effort with `factcheck.md` in this folder as their brief.
Split the section by subsection when it has more than about 30 entries, one agent per part.
Don't edit the section while they run: they check the text as it was when they started, and an edit under them makes their findings stale.
They check the final wording against the source and report fixes with evidence; apply them once all of them have reported.
Check again, with a fresh agent, every entry a fix rewrote substantially or a fact-check added.

## 5. Build

```sh
uv run --no-sync hopsworks-docs markdownlint
uv run --no-sync hopsworks-docs check
```

Both must pass; the strict build fails on a release cross-reference such as `[5.2.1][hopsworks-5-2-1]` that doesn't resolve, on a front matter or entry tag error and on a hopsworks-api tag missing for a linked client version.
It doesn't check the absolute `https://docs.hopsworks.ai/X.Y/...` links or their anchors, so step 7 of the fact-check is their only check.
The check of the client tags needs github.com.

## Report

Tell the user:

- the release, what it compares with, and the number of entries per subsection;
- the upgrade steps the release needs that the upgrade guide lacks;
- what the fact-check changed;
- every `UNSURE` item, as a question;
- the commits left out as not user-visible, as one line of short SHAs per repo.

Leave committing and pushing to the user.
