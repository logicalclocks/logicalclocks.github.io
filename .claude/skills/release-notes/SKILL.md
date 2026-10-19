---
name: release-notes
description: Write the release notes of a hopsworks-helm release, such as 5.1.0, into docs/releases. Collects the chart, rondb-helm, hopsworks-ee and hopsworks-front changes of the release, drafts its section and upgrade steps, fact-checks every entry against the source and runs the strict build. Use when asked to write, add, regenerate or audit the release notes of a Hopsworks release.
argument-hint: <X.Y.Z>
---

# Release notes for a release

Writes the `## X.Y.Z` section of `docs/releases/X.Y/index.md`, and its steps in `docs/releases/X.Y/upgrade.md` when it has any, for the `hopsworks-helm` release given as the argument.
Read `.claude/docs/releases.md` in full first: it is the contract for the page shape and every writing rule, and this skill does not repeat it.

The work has four stages, each checked before the next: collect the facts, draft, fact-check, build.
A draft is never trusted: in the 2026-10 backfill, separate adversarial passes against the source changed about one drafted entry in six, many of them for a wrong claim.

## 1. Sources

The command needs five checkouts, read-only: `hopsworks-helm`, `rondb-helm`, `hopsworks-ee`, `hopsworks-front` and `docker-images`.
They default to siblings of this repo (`../hopsworks-helm`, ...); if one is missing, ask the user where they are.
Set `S` to the directory that holds them, so the commands below need no other paths, and set up this repo's environment once; afterwards run every command with `uv run --no-sync`, because a plain `uv run` syncs again without the `cli` extra:

```sh
S=<directory holding the five checkouts>
uv sync --extra cli
```

Fetch each checkout, and this repo's `branch-*` (links are checked against them), one refspec per `git fetch`, because a release often came out after the last fetch:

```sh
git -C <repo> fetch origin --tags
git -C <repo> fetch origin '+refs/heads/branch-*:refs/remotes/origin/branch-*'
```

Never check out, commit or reset in those repos; read them with `git log`, `git show`, `git diff` and `git grep`.

## 2. Collect the facts

```sh
mkdir -p .release-notes/<X.Y.Z>
uv run --no-sync hopsworks-docs release-inputs <X.Y.Z> --helm $S/hopsworks-helm --rondb-helm $S/rondb-helm --ee $S/hopsworks-ee --front $S/hopsworks-front --docker-images $S/docker-images > .release-notes/<X.Y.Z>/inputs.md
```

`.release-notes/` is gitignored and lives in the repo, not in a temporary directory, so the work survives the session.
Read `inputs.md` in full. It gives:

- the release it compares with, and the front matter (release date, application version, Python client);
- every commit of the chart, of `rondb-helm` when the RonDB chart moved, and of `hopsworks-ee` and `hopsworks-front` between the `Release X.Y.Z` commits of the two application versions;
- on an X.Y.0, `[shipped in vX.Y.Z]` on each commit a patch release of the previous minor version already shipped, and which of those patch releases' chart commits the X.Y.0 lacks;
- the Helm values added, removed and changed, added lines that mention a deprecation, and the changed `values.*.yaml` overlays and `UPGRADE.md`;
  it doesn't say which removed values the values schema now rejects or which hooks changed, so check `values.schema.json` and the hook templates of the chart at the tag yourself;
- the Upgraded components table, with a warning for a version no component covers.

Stop and ask the user when it reports an `ERROR` (a release commit it can't find), a `released: "?"` (the GitHub release isn't published), or a RonDB chart that moves backwards.

## 3. Draft

Add the release to the page first, so the section has a place:

- its entry in the front matter `releases:` map, newest first, with the three versions from `inputs.md` as quoted strings;
- `## X.Y.Z { #hopsworks-X-Y-Z }` in release order, newest first;
- for a new minor version, `docs/releases/X.Y/index.md` with `# Release notes { #hopsworks-X-Y }` and `The releases of Hopsworks X.Y, newest first.`, modelled on an existing minor page.

Then turn the facts into entries.
Account for every commit and every value change: in an entry, in an existing entry it supports, or in the left-out list of the report.

- An X.Y.0 leaves out a commit marked `[shipped in ...]` for a patch release that came out before it, and says under its title which of those patch releases it includes, naming any change it lacks, as the "Patch releases" part of `inputs.md` shows.
  A commit shipped in a patch release that came out after it stays, with `(also in [X.Y.Z][hopsworks-X-Y-Z])`.
- Commits of different repos with the same ticket key (`[HWORKS-1234]`) are one entry.
- A change that also ships in a patch release of another minor version is listed in both releases, without a marker; check the ticket keys of a patch release against the other minor versions' patch releases of the same days.
- Read the diff of every commit you turn into an entry; a subject can promise more than the code does, and a later commit in the range can change or revert it.

For up to about 40 commits, draft it yourself.
Above that, split the commits into slices of about 40 (chart, rondb-helm, ee, front, values) and give each slice to a parallel agent at medium effort with `draft.md` in this folder as its brief, the slice, and the paths.
Agents return entries with evidence and never edit the page; you merge their entries into the section, so no two writers touch one file.

Write upgrade steps into `docs/releases/X.Y/upgrade.md` (`## From <previous minor>` for an X.Y.0, `## To X.Y.Z` for a patch) only when the release needs ordered action at upgrade.
Signals are a changed `UPGRADE.md`, a migration Job or hook, or a breaking change that has to happen before or after the `helm upgrade`.
Base the steps on the chart's `UPGRADE.md` at the tag, and link the docs pages that describe them.
A `## To X.Y.Z` section serves readers who come from an earlier release of the minor version and readers who come straight from the previous minor version; say which steps apply to whom.
When a patch release makes an existing step of the guide wrong, such as a step of `## From <previous minor>`, fix that step too and say so in the report.

Order the entries of each subsection by significance, as the guide defines it, after merging; the agents' order only holds within their slice.

Generate the table last:

```sh
uv run --no-sync hopsworks-docs release-components <X.Y.Z> --helm $S/hopsworks-helm --rondb-helm $S/rondb-helm --write
```

If it fails on a version no component covers, add the component to `scripts/release_components.py` rather than editing the table by hand.
Remove link definitions that no entry uses any more; markdownlint fails on them.

## 4. Fact-check

Give the drafted section, and the upgrade steps, to fresh agents at medium effort with `factcheck.md` in this folder as their brief.
Split the section by subsection when it has more than about 30 entries, one agent per part.
Don't edit the section or the steps while they run: they check the text as it was when they started, and an edit under them makes their findings stale.
They check the final wording against the source and report fixes with evidence; apply them once all of them have reported.
Check again, with a fresh agent, every entry or step a fix rewrote substantially or a fact-check added.

## 5. Build

```sh
uv run --no-sync hopsworks-docs markdownlint
HOPSWORKS_DOCS_CHECK_CLIENT_TAGS=1 uv run --no-sync hopsworks-docs check
```

Both must pass; the strict build fails on a broken link, an anchor that doesn't exist and a front matter error.

## Report

Tell the user:

- the release, what it compares with, and the number of entries per subsection;
- whether it has upgrade steps;
- what the fact-check changed;
- every `UNSURE` item, as a question;
- the commits left out as not user-visible, as one line of short SHAs per repo.

Leave committing and pushing to the user.
