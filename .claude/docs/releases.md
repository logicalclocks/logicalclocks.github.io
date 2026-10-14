# Release Pages

Every docs version shows the same release pages, under `Releases` in its nav, so a release note is written once on `main` and never backported.

The source is `docs/releases/` on `main` only.
A release branch build (`mkdocs-release.yml`, and `mkdocs-test.yml` for a PR to a `branch-*`) first copies `docs/releases/` and `scripts/releases_hook.py` from `main`.
CI fails a PR to a `branch-*` that touches `docs/releases/`, because main's copy replaces it.
A release branch shows the pages once it has the hook and the `Releases: releases/index.md` nav entry; older branches don't.

`scripts/releases_hook.py` expands the `Releases: releases/index.md` nav entry into a page per release, grouped by major version and newest first, and generates the table in `docs/releases/<major>/index.md`.
Each release has one page, `docs/releases/<major>/<X.Y.Z>.md`; no nav edit is needed.
A new major also needs `docs/releases/<major>/index.md` holding `# Hopsworks <major>.x` and `<!-- releases -->`, and a link in `docs/releases/index.md`.
`uv run hopsworks-docs check` fails if hopsworks-api has no tag for a Python client version a page links.

Every build writes `releases/fingerprint.txt`, a hash of the release sources and the hook.
After each docs build of `main`, `mkdocs-release-notes.yml` runs `hopsworks-docs sync-release-notes --rebuild`: it rebuilds every release branch whose deployed fingerprint doesn't match `main` with that branch's own workflow, then fails if any version, `dev` included, still doesn't match.
A red run means a version shows outdated release pages, usually because its docs build is broken; fix the build and run the workflow again.
`uv run hopsworks-docs sync-release-notes` without `--rebuild` only reports.

## Page shape

A release is a `hopsworks-helm` tag `vX.Y.Z`; the page is named after it and starts with `# Hopsworks X.Y.Z { #hopsworks-X-Y-Z }`, so link to it with `[X.Y.Z][hopsworks-X-Y-Z]`.
Its front matter declares three versions, all quoted strings:

```yaml
---
released: "2026-09-28"     # date of the GitHub release
application: "5.0.12"      # appVersion in charts/hopsworks/Chart.yaml at the tag
python_client: "5.0.9"     # hopsworks-api version of the base images the chart deploys
---
```

The Python client is `base-image/hopsworks-api-version.txt` in `docker-images` at the release commit whose `version.txt` matches `hopsworks.variables.base_image_version` at the tag.
`scripts/releases_hook.py` turns the front matter into the line under the H1, the row in the major's table, and a `## Python client` section at the end of the page.
That section links the GitHub release notes of every client version since the previous release of the same minor version, so the page shows what changed in the client too.

Each page has three sections, in this order: `## Release notes`, `## Breaking changes`, `## Migrations`; the hook appends `## Python client`.
A section with nothing to report keeps its heading and says so in one sentence, for example "There are no breaking changes in this release."

A patch page lists the changes since the previous tag of its minor version.
An X.Y.0 page lists the changes since the previous minor version.
An entry that also shipped in a patch release of that minor version ends with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, or `(also in X.Y.Z)` if that patch has no page, as for 4.8, so readers on that patch can skip it.
Its release notes come after the new ones, condensed into one or two bullets per patch release, because the patch page has the details; a breaking change keeps its own entry with what to do.

## Writing entries

- Write for users and operators, not developers; an entry is not a commit message.
- Keep each entry to one line; add a second only for what a reader must act on, such as a value to set or a risk.
- Leave out defaults, internals and explanations a reader doesn't act on; the values reference has the details.
- Start with a past-tense verb: Added, Changed, Deprecated, Removed, Fixed, Upgraded.
- Name the exact API, Helm value, config variable or CLI flag.
- Leave out changes with no user-visible effect: tests, CI, refactors, and fixes for bugs that never shipped.
- Do not link Jira or private GitHub repos and do not name customers, because the docs are public.

Release notes are one flat list with no subcategories.

Breaking changes are changes that need users or operators to do something when they upgrade.
Start each one with `**Action required:**` and say what changed, who is affected and what to do.
A breaking change is not repeated in the release notes.

Migrations are numbered steps under `### Before the upgrade`, `### Upgrade` and `### After the upgrade`.
Mark each step as required or optional, give copy-paste commands with `<placeholders>`, and say when a step can't be undone.
