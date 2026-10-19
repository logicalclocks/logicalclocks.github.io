# Release Pages

Every docs version shows the same release pages, under `Releases` in its nav, so a release note is written once on `main` and never backported.

The source is `docs/releases/` on `main` only.
A release branch build (`mkdocs-release.yml`, and `mkdocs-test.yml` for a PR to a `branch-*`) first copies `docs/releases/` and `scripts/releases_hook.py` from `main`.
CI fails a PR to a `branch-*` that touches `docs/releases/`, because main's copy replaces it.
A release branch shows the pages once it has the hook and the `Releases: releases/index.md` nav entry; older branches don't.

`scripts/releases_hook.py` expands the `Releases: releases/index.md` nav entry into a section per minor version, newest first, holding its release notes (`docs/releases/X.Y/index.md`) and its upgrade guide (`docs/releases/X.Y/upgrade.md`), and generates the table of all releases in `docs/releases/index.md`; no nav edit is needed.
`uv run hopsworks-docs check` fails if hopsworks-api has no tag for a Python client version a page links.

Every build writes `releases/fingerprint.txt`, a hash of the release sources and the hook.
After each docs build of `main`, `mkdocs-release-notes.yml` runs `hopsworks-docs sync-release-notes --rebuild`: it rebuilds every release branch whose deployed fingerprint doesn't match `main` with that branch's own workflow, then fails if any version, `dev` included, still doesn't match.
A red run means a version shows outdated release pages, usually because its docs build is broken; fix the build and run the workflow again.
`uv run hopsworks-docs sync-release-notes` without `--rebuild` only reports.

## Page shape

The release notes of a minor version, `docs/releases/X.Y/index.md`, start with `# Release notes { #hopsworks-X-Y }` and hold one section per release, newest first: `## X.Y.Z { #hopsworks-X-Y-Z }`, so link to a release with `[X.Y.Z][hopsworks-X-Y-Z]`.
A release is a `hopsworks-helm` tag `vX.Y.Z`.
The front matter declares every release, newest first, with its versions as quoted strings:

```yaml
---
releases:
  "5.1.1":
    released: "2026-10-09"     # date of the GitHub release
    application: "5.1.1"       # appVersion in charts/hopsworks/Chart.yaml at the tag
    python_client: "5.1.1"     # hopsworks-api version of the base images the chart deploys
  "5.1.0":
    released: "2026-09-24"
    application: "5.1.0"
    python_client: "5.1.0"
---
```

The Python client is `base-image/hopsworks-api-version.txt` in `docker-images` at the release commit whose `version.txt` matches `hopsworks.variables.base_image_version` at the tag.
Under each section title, `scripts/releases_hook.py` renders the release date, the release it lists the changes since, the application version and the Python client, linking the GitHub release notes of every client version new in the release.

A patch release lists the changes since the previous release of its minor version, and an X.Y.0 since the first release of the previous minor version, so minor versions compare with each other: 5.2.0 with 5.1.0, 5.1.0 with 5.0.0.
Each change is listed once, under the release that first shipped it, so an X.Y.0 leaves out the changes that already shipped in a patch release of the previous minor version; a sentence under its title says which of those patch releases it includes, and names any of their changes it lacks.
A patch release of the previous minor version that comes out after the X.Y.0 can backport its changes; both releases then list them, and the X.Y.0 entry ends with `(also in [X.Y.Z][hopsworks-X-Y-Z])`.
A release covers every change users or operators notice, from the chart (`hopsworks-helm` and `rondb-helm` commits between the tags) and from the application it ships (`hopsworks-ee` and `hopsworks-front`).
Neither application repo has tags: a version's changes end at its `Release X.Y.Z` commit on `branch-X.Y-ee` or `branch-X.Y`, which is the last commit of that version, and start after the release commit of the application version the previous release ships.
A chart release that keeps the application version has no application changes, and one that skips application versions includes them all.
Leave out application changes users don't see, such as refactors, tests and build changes; leave out `hopsworks-api` changes, because the line under the release title links its release notes.
A chart commit and an application commit for the same ticket are one entry.
5.0.0 is the exception: 4.8 has no pages, so its front matter declares `since: "4.8.2"`, the first 4.8 release, and an entry that also shipped in a 4.8 patch release ends with `(also in 4.8.N)`.

A release section has up to five subsections, in this order, and leaves out the ones with nothing to report: `### What's changed`, `### Configuration changes`, `### Breaking changes`, `### Deprecations`, `### Upgraded components`.

The upgrade guide of a minor version, `docs/releases/X.Y/upgrade.md`, starts with `# Upgrading to Hopsworks X.Y { #upgrading-to-X-Y }`.
It has `## From <previous minor> { #upgrading-to-X-Y-0 }` and a `## To X.Y.Z { #upgrading-to-X-Y-Z }` for each patch release with steps, oldest first, each with numbered steps under `### Before the upgrade`, `### Upgrade` and `### After the upgrade`.

## Writing entries

- Write for users and operators, not developers; an entry is not a commit message.
- Make each entry one coherent change; don't combine unrelated changes in one entry, even small ones.
- Keep each entry to one line; add a second only for what a reader must act on, such as a value to set or a risk.
- Leave out defaults, internals and explanations a reader doesn't act on; the values reference has the details.
- Start with a past-tense verb: Added, Changed, Deprecated, Removed, Fixed.
- Put version upgrades in `### Upgraded components`, not under `### What's changed`; keep their effect as an entry, such as "Fixed writes to an online feature group failing after its table was truncated" or "Fixed security vulnerabilities in the Strimzi operator and Kafka images".
- Name the exact API, Helm value, config variable or CLI flag.
- Link to the documentation for details and procedures instead of repeating them: say what changed and what to do, then link the page that explains it, such as an admin guide, a user guide or the Helm values reference.
  Release pages show in every docs version, so link the docs of the release's minor version with an absolute URL (`https://docs.hopsworks.ai/5.2/...`), which a relative link to a page missing from an older version would break.
  Link the chart's `UPGRADE.md`, `README.md` or `HELM4_MIGRATION.md` at the release tag (`https://github.com/logicalclocks/hopsworks-helm/blob/vX.Y.Z/...`) only for what no docs page covers.
- Leave out changes with no user-visible effect: tests, CI, refactors, and fixes for bugs that never shipped.
- Do not link Jira or private GitHub repos and do not name customers, because the docs are public.

`### What's changed` and `### Configuration changes` are each one flat list with no subcategories.

`### Configuration changes` lists the changes to the Helm values themselves: values added or removed, changed defaults, fixes for a value that was ignored or rejected, and changes to `values.openshift.yaml` or `values.airgap.yaml`.
A feature or fix keeps its entry under `### What's changed` and names the value that turns it on or tunes it, even when it is off by default.
Split an entry that does both, so each change is listed once.

Breaking changes are changes that need users or operators to do something when they upgrade.
Say in each one what changed, who is affected and what to do, and link the upgrade guide step or the docs page that has the procedure.
A breaking change is not repeated under `### What's changed`.

Deprecations are what a release marks for removal but still accepts, such as a Helm value the chart keeps only so existing values files validate.
Start each one with "Deprecated", and say what replaces it or that nothing reads it any more.
Find them in the chart's values, where they are marked `DEPRECATED` or `deprecated: true`; removing one later is a breaking change.

Upgrade steps live in the upgrade guide, not in the release notes.
The 5.0 and 5.1 releases were written up after they shipped, so they have no upgrade guide.
Mark each step as required or optional and say when a step can't be undone.
A step that the documentation describes links to it; give a copy-paste command with `<placeholders>` only when no page has one.

## Upgraded components

A table of every component whose version changed in the chart, named after the two releases it compares: `| Component | 5.1.0 | 5.1.1 |`, one row per component, sorted by name.
It compares with the release the section lists the changes since; on an X.Y.0, a version that already shipped in a patch release of the previous minor version ends with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, or `(also in 4.8.N)` for 4.8, which has no pages.
A release without upgraded components has no such subsection.

Generate it with `uv run hopsworks-docs release-components X.Y.Z --helm <hopsworks-helm> --rondb-helm <rondb-helm> --write`, which needs both checkouts with their tags.
It fails when a version changed that no component in `scripts/release_components.py` covers; add the component there rather than editing the table by hand.
It takes the versions from the chart at both tags, not from commit messages:

- every image tag, `appVersion` and version setting in the `values.yaml` and `Chart.yaml` of each chart in `hopsworks-helm`, with the umbrella `values.yaml` overriding a subchart's;
- RonDB and its images from `rondb-helm` at the tag the `rondb` dependency names;
- for an image the chart doesn't pin, the default of the upstream chart at its dependency version from `UPSTREAM_DEFAULTS`, such as Prometheus `v2.51.2` from `prometheus` 25.20.2; it fails on a dependency version that isn't listed.

It shows the image tag as the version; if a rebuilt image's tag doesn't name what it ships, add it to `SHIPS`, which gives `8.4.5-debian-12-r0-h3 (MySQL 8.4.11)`.
It leaves out the Hopsworks application, which the line under the release title gives, and prints the components new or removed in the release, which belong in the notes.
