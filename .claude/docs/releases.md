# Release Pages

Every docs version shows the same release pages, under `Releases` in its nav, so a release note is written once on `main` and never backported.

The source is `docs/releases/` on `main` only.
A release branch build (`mkdocs-release.yml`, and `mkdocs-test.yml` for a PR to a `branch-*`) first copies `docs/releases/` and `scripts/releases_hook.py` from `main`.
CI fails a PR to a `branch-*` that touches `docs/releases/`, because main's copy replaces it.
A release branch shows the pages once it has the hook and the `Releases: releases/index.md` nav entry; older branches don't.

`scripts/releases_hook.py` expands the `Releases: releases/index.md` nav entry into a section per minor version, newest first, holding its release notes (`docs/releases/X.Y/index.md`), and generates the table of all releases in `docs/releases/index.md`; no nav edit is needed.
`uv run hopsworks-docs check` fails if hopsworks-api has no tag for a Python client version a page links.

Every build writes `releases/fingerprint.txt`, a hash of the release sources and the hook.
After each docs build of `main`, `mkdocs-release-notes.yml` runs `hopsworks-docs sync-release-notes --rebuild`: it rebuilds every release branch whose deployed fingerprint doesn't match `main` with that branch's own workflow, then fails if any version, `dev` included, still doesn't match.
A red run means a version shows outdated release pages, usually because its docs build is broken; fix the build and run the workflow again.
`uv run hopsworks-docs sync-release-notes` without `--rebuild` only reports.

To write the notes of a release, run the `/release-notes X.Y.Z` skill (`.claude/skills/release-notes/`).
It collects the facts with `uv run hopsworks-docs release-inputs X.Y.Z`, which prints the release's commits in the charts, the application, the Python client, `docker-images` and every component repo whose version moved, its Helm value changes, its front matter and its Upgraded components table.
Then it drafts the section, fact-checks every entry against the source and runs the strict build.

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
An X.Y.0 lists every change since the previous X.Y.0, including those that already shipped in a patch release of the previous minor version, so a reader who upgrades from one X.Y.0 to the next finds them all in one place.
Such an entry repeats the patch release's entry, checked against the X.Y.0, and ends its first line with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, so readers on that patch can skip it.
A change a patch release shipped and the X.Y.0 lacks is not repeated; a breaking change of the X.Y.0 says what is missing and what to do, as 5.1.0 does for the RonDB REST server probes of 5.0.13.
A patch release of the previous minor version that comes out after the X.Y.0 can backport its changes; both releases then list them, with the same marker on the X.Y.0 entry.
A release covers every change users or operators notice, from the chart (`hopsworks-helm` and `rondb-helm` commits between the tags), from the application it ships (`hopsworks-ee` and `hopsworks-front`), and from the images and components it deploys from Hopsworks repos (`docker-images`, OnlineFS, ArrowFlight, the model serving webhook and authenticator, and the others `scripts/release_inputs.py` lists); the HopsFS and RonDB repos are not sources, the RonDB chart is.
Neither application repo has tags: a version's changes end at its `Release X.Y.Z` commit on `branch-X.Y-ee` or `branch-X.Y`, which is the last commit of that version, and start after the release commit of the application version the previous release ships.
A chart release that keeps the application version has no application changes, and one that skips application versions includes them all.
Leave out application changes users don't see, such as refactors, tests and build changes; leave out `hopsworks-api` changes, because the `### Python client` subsection shows its release notes.
A chart commit and an application commit for the same ticket are one entry.
5.0.0 is the exception: 4.8 has no pages, so its front matter declares `since: "4.8.2"`, the first 4.8 release, and an entry that also shipped in a 4.8 patch release ends with `(also in 4.8.N)`.

A release section has up to six subsections, in this order, and leaves out the ones with nothing to report: `### What's changed`, `### Configuration changes`, `### Breaking changes`, `### Deprecations`, `### Upgrade steps`, `### Upgraded components`.
`### Upgrade steps` is on every X.Y.0 and only there, even when empty, and describes the steps needed to upgrade to it from the previous minor version; for now it says "No upgrade steps are listed for this release." on every release.
The hook appends a sixth, `### Python client`, which links the GitHub release notes of every hopsworks-api version new in the release; `docs/js/client-release-notes.js` replaces the links with those notes, fetched from the GitHub API in the reader's browser, one collapsed block per version, and keeps the links when GitHub can't be reached.
Never write it by hand: the notes are hopsworks-api's own, shown as they are on GitHub.

## Writing entries

- Write for users and operators, not developers; an entry is not a commit message.
- Make each entry one coherent change; don't combine unrelated changes in one entry, even small ones.
- Keep each entry to one line; add a second only for what a reader must act on, such as a value to set or a risk.
- Leave out defaults, internals and explanations a reader doesn't act on; the values reference has the details.
- Start with a past-tense verb: Added, Changed, Deprecated, Removed, Fixed; breaking changes are the exception, see below.
- Put version upgrades in `### Upgraded components`, not under `### What's changed`; keep their effect as an entry, such as "Fixed writes to an online feature group failing after its table was truncated" or "Fixed security vulnerabilities in the Strimzi operator and Kafka images".
- Name the exact API, Helm value, config variable or CLI flag.
- Link to the documentation for details and procedures instead of repeating them: say what changed and what to do, then link the page that explains it, such as an admin guide, a user guide or the Helm values reference.
  Release pages show in every docs version, so link the docs of the release's minor version with an absolute URL (`https://docs.hopsworks.ai/5.2/...`), which a relative link to a page missing from an older version would break.
  For what no docs page covers, name the file of the chart that does, such as "see `UPGRADE.md` in the 5.2 chart": the packaged chart ships its `README.md`, `UPGRADE.md`, `HELM4_MIGRATION.md` and `values.*.yaml`, but its repo is private.
- Leave out changes with no user-visible effect: tests, CI, refactors, and fixes for bugs that never shipped.
- Do not link Jira or any private GitHub repo, `hopsworks-helm` included, and do not name customers, because the docs are public; of the source repos, only `hopsworks-api` is public.
- Give no details of a security issue a release fixes: name only where it was, such as "Fixed a security issue in jobs", never what was exposed, who could exploit it or how, because the notes are public and clusters on older releases stay vulnerable.
  Fixes of known vulnerabilities in dependencies and images stay one entry per group, such as "Fixed security vulnerabilities in the Grafana and Superset images".
  A breaking change or upgrade step that a security fix needs says what to do, and at most that it is for a security fix.

`### What's changed` and `### Configuration changes` are each one flat list with no subcategories.

Order the entries of every subsection by significance, most significant first, so a reader who stops early has read what matters most.
Significance is how many users or operators an entry affects and how much: data loss, security, an outage or a failed upgrade outweigh a new feature, which outweighs an inconvenience.

- `### What's changed`: fixes for data loss, security and outages, and the headline features of the release, first; then other features and changes; then smaller fixes.
- `### Configuration changes`: changed defaults that change behaviour on upgrade first; then values that were ignored or rejected; then new values.
- `### Breaking changes`: what makes the upgrade fail or loses data first; then what breaks a running workload; then values to change.
- `### Deprecations`: what is most widely set first.

On an X.Y.0, entries marked `(also in ...)` follow the same order; they are not grouped at the end.

`### Configuration changes` lists the changes to the Helm values themselves: values added or removed, changed defaults, fixes for a value that was ignored or rejected, and changes to `values.openshift.yaml` or `values.airgap.yaml`.
A feature or fix keeps its entry under `### What's changed` and names the value that turns it on or tunes it, even when it is off by default.
Split an entry that does both, so each change is listed once.

Breaking changes are changes that need users or operators to do something when they upgrade.
Say in each one what changed, what the behaviour was before, who is affected and what to do, and link the docs page that has the procedure; it may start with what changed, such as "`helm upgrade` now stops ...", or with what to do, such as "Remove `<value>` from your values ...".
Outline the behaviour before the change in a few words, such as "instead of `default`" or "which used to keep them", so a reader can tell whether they relied on it; check it against the previous release, not the commit message.
A breaking change that a security fix needs leaves the behaviour before out, because it would describe the issue; it says only what users could do that they no longer can, such as "can no longer be queried in Trino".
A fix, security fixes included, that takes away something users rely on is a breaking change.
A breaking change is not repeated under `### What's changed`; a value it adds, removes or renames is still listed under `### Configuration changes`, which says what the value does, while the breaking change says what to do.
A change that ships in patch releases of two minor versions at about the same time, such as 5.0.14 and 5.1.2, is listed in both releases, without a marker; the `(also in ...)` marker is only for an X.Y.0 entry.

Deprecations are what a release marks for removal but still accepts, such as a Helm value the chart keeps only so existing values files validate.
Start each one with "Deprecated", and say what replaces it or that nothing reads it any more.
Find them in the chart's values, where they are marked `DEPRECATED` or `deprecated: true`; removing one later is a breaking change.

Once upgrade steps are written, they are numbered steps under `#### Before the upgrade`, `#### Upgrade` and `#### After the upgrade`.
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
