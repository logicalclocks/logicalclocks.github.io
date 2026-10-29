# Release Pages

Every docs version shows the same release pages, under `Releases` in its nav, so a release note is written once on `main` and never backported.

The source is `docs/releases/` on `main` only.
A release branch build (`mkdocs-release.yml`, and `mkdocs-test.yml` for a PR to a `branch-*`) of a branch that has the hook first removes `docs/releases/`, `docs/css/releases.css`, `docs/js/client-release-notes.js` and `scripts/releases_hook.py`, then checks out from `main` those of them that `main` has, so it removes what `main` no longer has; when `main` has none of them, it does nothing more.
Both workflows repeat this list, `FROM_MAIN` in `scripts/releases_hook.py`; a change to it needs the same change to both workflows on `main` and on every release branch, or those builds stay stale.
CI fails a PR to a `branch-*` that touches `docs/releases/`, and, once the branch has the hook, one that touches `docs/css/releases.css`, `docs/js/client-release-notes.js` or `scripts/releases_hook.py`, because main's copy replaces them.
A release branch shows the pages once it has this backport; older branches don't:

- `scripts/releases_hook.py`, `docs/css/releases.css` and `docs/js/client-release-notes.js`;
- in `mkdocs.yml`, the `hooks:` entry, the `Releases: releases/index.md` nav entry, `css/releases.css` in `extra_css` and `js/client-release-notes.js` in `extra_javascript`;
- in `.markdownlint.yaml`, `MD024: siblings_only: true`, because the pages repeat their subsection headings under every release;
- in `.github/workflows/mkdocs-release.yml`, `queue: max` on its `concurrency:`, the `workflow_dispatch:` trigger, the `if` of the branch name step that covers it, and the copy step;
- in `.github/workflows/mkdocs-test.yml`, the release pages guard and the copy step;
- optionally `scripts/check.py`, for the client tag check.

`scripts/releases_hook.py` expands the `Releases: releases/index.md` nav entry into a section per minor version, newest first, holding its release notes (`docs/releases/X.Y/index.md`), and generates the table of all releases in `docs/releases/index.md`; no nav edit is needed.
The llms export (`scripts/llms_hook.py`) gets the pages with the line under each release title and the table of all releases, and with the tags as written.
`uv run hopsworks-docs check` fails if hopsworks-api has no tag for a Python client version a page links.

Every build writes `releases/fingerprint.txt`, a hash of the files in `FROM_MAIN`.
After each successful docs build of `main`, `mkdocs-release-notes.yml` runs `hopsworks-docs sync-release-notes --rebuild`: it rebuilds every release branch whose deployed fingerprint doesn't match `main` with that branch's own workflow, one at a time, then fails if any version, `dev` included, still doesn't match.
A branch whose rebuild can't be started is reported and left stale, and the others are still rebuilt; a cancelled rebuild is not retried.
`mkdocs-release-notes.yml` and `mkdocs-release.yml` set `queue: max` on their `concurrency:`, so a new run waits behind a pending one instead of replacing it.
A red run means a version shows outdated release pages, usually because its docs build is broken; fix the build and run the workflow again.
`uv run hopsworks-docs sync-release-notes` without `--rebuild` fetches the remote that points at `logicalclocks` and only reports.
The rebuilds stop after 100 minutes, inside the job's 120: one still running is reported as timed out, and the branches after it as not rebuilt.
Run it on `main`: it accepts the release pages of `HEAD` and of later `main` commits, so on a branch that changed them it reports every version stale.

To write the notes of a release, run the `/release-notes X.Y.Z` skill (`.claude/skills/release-notes/`).
It collects the facts with `uv run hopsworks-docs release-inputs X.Y.Z`, which prints the release's commits in the charts, the application, the Python client, `docker-images` and every component repo whose version moved, its Helm value changes, its upstream chart dependency changes, its front matter and its Upgraded components table.
`release-inputs` fails with `ERROR: no checkout at <path>` before printing anything when a checkout of `hopsworks-helm`, `rondb-helm`, `hopsworks-ee`, `hopsworks-front`, `docker-images` or `hopsworks-api` is missing.
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
    python_client: "5.1.1"     # hopsworks-api version of the base images the chart deploys
  "5.1.0":
    released: "2026-09-24"
    python_client: "5.1.0"
---
```

The Python client is `base-image/hopsworks-api-version.txt` in `docker-images` at the release commit whose `version.txt` matches `hopsworks.variables.base_image_version` at the tag, or, for a base image from before that file, the `hopsworks[...]==X` pin in `base-image/internal-base/python_install.sh` there.
Under each section title, `scripts/releases_hook.py` renders the Helm chart version, the release date, the release it lists the changes since and the Python client, linking the GitHub release notes of every client version new in the release.

A patch release lists the changes since the previous release of its minor version, and an X.Y.0 since the first release of the previous minor version, so minor versions compare with each other: 5.2.0 with 5.1.0, 5.1.0 with 5.0.0.
An X.Y.0 lists every change since the previous X.Y.0, including those that already shipped in a patch release of the previous minor version, so a reader who upgrades from one X.Y.0 to the next finds them all in one place.
Such an entry repeats the patch release's entry, checked against the X.Y.0, and ends its first line with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, so readers on that patch can skip it; a change that shipped in two patch releases names both, such as `(also in [5.0.6][hopsworks-5-0-6] and [5.0.9][hopsworks-5-0-9])`.
A change a patch release shipped and the X.Y.0 lacks is not repeated; a breaking change of the X.Y.0 says what is missing and what to do, as 5.1.0 does for the RonDB REST server probes of 5.0.13.
A patch release of the previous minor version that comes out after the X.Y.0 can backport its changes; both releases then list them, with the same marker on the X.Y.0 entry.
A release covers every change users or operators notice, from the chart (`hopsworks-helm` and `rondb-helm` commits between the tags), from the application it ships (`hopsworks-ee` and `hopsworks-front`), and from the images and components it deploys from Hopsworks repos (`docker-images`, OnlineFS, ArrowFlight, the model serving webhook and authenticator, and the others `scripts/release_inputs.py` lists); the HopsFS and RonDB repos are not sources, the RonDB chart is.
Neither application repo has tags: a version's changes end at its `Release X.Y.Z` commit on `branch-X.Y-ee` or `branch-X.Y`, which is the last commit of that version, and start after the release commit of the application version the previous release ships.
A chart release that keeps the application version has no application changes, and one that skips application versions includes them all.
The Python and Java clients (`hopsworks-api`, the commits between the Python client versions of the two releases) are sources too: SDK features, behaviour changes, fixes, breaking changes and deprecations users of either client notice; the `### Python client` subsection still links the full hopsworks-api release notes.
Leave out changes users don't see, such as refactors, tests, build changes, version bumps and dependency pins with no user-visible effect.
A chart, application or client commit for the same ticket is one entry, unless the ticket bundles unrelated changes, such as a batch of UI fixes: then each change is its own entry, as for any other unrelated changes.
5.0.0 is the exception: 4.8 has no pages, so its front matter declares `since: "4.8.2"`, the first 4.8 release, and an entry that also shipped in a 4.8 patch release ends with `(also in 4.8.N)`.
The hook fails the build on a front matter field other than `released`, `python_client` and `since`, on a `since` that isn't a quoted X.Y.Z older than its release, on `since` on any release but the oldest on the pages, when the oldest release on the pages isn't an X.Y.0 that declares `since`, when the oldest release of a minor version isn't its X.Y.0, and, naming the page, when a release's `python_client` is older than that of the release before it.

A release section has up to six subsections, in this order, and leaves out the ones with nothing to report: `### What's changed`, `### Breaking changes`, `### Deprecations`, `### Upgrade steps`, `### Upgraded components`, `### Configuration changes`.
`### Upgrade steps` links the sections of the upgrade guide, `docs/setup_installation/admin/upgrade.md`, that an upgrade to the release follows, and doesn't repeat them, so each step is written and kept up to date in one place.
Every X.Y.0 has it: it links `Before every upgrade` and the section from the previous minor version, such as `5.1.x to 5.2.x`, or says "No upgrade steps are listed for this release." when the guide has no such section, as for 5.0.0.
A patch release has it only when the guide has a `Changes from X.Y.Z` section for it, and links that section.
The guide is in the docs from 5.2 on, so 5.1.0 links the 5.2 docs; `release-inputs` prints the sections and the docs version to link.
A step the release needs that the guide lacks belongs in the guide, which changes on the release branches like any other docs page, not in the release notes.
The hook appends a last one, `### Python client`, which links the GitHub release notes of every hopsworks-api version new in the release; `docs/js/client-release-notes.js` replaces the links with those notes, fetched from the GitHub API in the reader's browser, one collapsed block per version, and keeps the links when GitHub can't be reached.
Never write it by hand: the notes are hopsworks-api's own, shown as they are on GitHub.

## Writing entries

- Write for users and operators, not developers; an entry is not a commit message.
- Make each entry one coherent change; don't combine unrelated changes in one entry, even small ones.
- Keep each entry to one line; add a second only for what a reader must act on, such as a value to set or a risk.
- Leave out defaults, internals and explanations a reader doesn't act on; the values reference has the details.
- Start with a past-tense verb: Added, Changed, Deprecated, Removed, Fixed; breaking changes are the exception, see below.
- Put version upgrades in `### Upgraded components`, not under `### What's changed`; keep their effect as an entry, such as "Fixed writes to an online feature group failing after its table was truncated" or "Addressed vulnerabilities in the Strimzi operator and Kafka images".
- Name the exact API, Helm value, config variable or CLI flag.
- Link to the documentation for details and procedures instead of repeating them: say what changed and what to do, then link the page that explains it, such as an admin guide, a user guide or the Helm values reference.
  Release pages show in every docs version, so link the docs of the release's minor version with an absolute URL (`https://docs.hopsworks.ai/5.2/...`), which a relative link to a page missing from an older version would break.
  A page the release's minor version lacks is linked in the oldest docs version that has it, such as the 5.2 upgrade guide and Upgrading OpenSearch from a 5.1 release.
  For what no docs page covers, name the file of the chart that does, such as "see `values.openshift.yaml` in the 5.2 chart": the packaged chart ships its `README.md` and `values.*.yaml`, but `hopsworks-helm` is private.
  Up to 5.2.1 it also shipped `UPGRADE.md` and `HELM4_MIGRATION.md`; they are docs pages now, the upgrade guide and Upgrading with Helm 4, so link those.
- Leave out changes with no user-visible effect: tests, CI, refactors, and fixes for bugs that never shipped.
- Do not link Jira or any private GitHub repo, and do not name customers, because the docs are public.
  Of the source repos, `hopsworks-helm`, `hopsworks-ee`, `hopsworks-front`, `docker-images`, `flyingduck`, `clusterj-onlinefs`, `model-serving-webhook`, `model-serving-authenticator`, `hops-git`, `tools` and `sparkhistoryserver` are private; `hopsworks-api`, `rondb-helm` and the forks (`trino`, `hive`, `hudi`, `incubator-uniffle`, `spark`) are public.
  Check a repo with `gh repo view <org>/<repo> --json visibility` before linking it.
- Write a security fix as "Addressed vulnerabilities in <component>", such as "Addressed vulnerabilities in jobs", and nothing more: never write "Fixed a security issue in", and never say what was exposed, who could exploit it or how, because the notes are public and clusters on older releases stay vulnerable.
  Fixes of known vulnerabilities in dependencies and images stay one entry per group, such as "Addressed vulnerabilities in the Grafana and Superset images".
  A breaking change or upgrade step that a security fix needs says what to do, and at most that it addresses a vulnerability.

`### What's changed` and `### Configuration changes` are each one flat list with no subcategories.

An entry starts with the tags that say how users reach the change, so a reader can skip what they don't use:

- `[API]`: the Python and Java clients, the `hops` CLI and the REST API;
- `[FRONTEND]`: the Hopsworks UI;
- `[HELM]`: the Helm charts: their values, install and upgrade, and cluster variables.

Tag by where users notice the change, not by the repo it is in: a server change users see in the UI is `[FRONTEND]`, one they see through the clients or the REST API is `[API]`, and one they see in both carries both.
A fix in a component the chart deploys, such as OnlineFS or ArrowFlight, takes the tag of where users notice it, such as `[API]` for a failed insert.
An entry users reach in none of these ways, such as a fix of known vulnerabilities in images or of a component that only operators see, has no tag.
An entry users reach in more than one way carries each tag, in that order, such as `- [API] [FRONTEND] Added ...`.
Every entry of `### Configuration changes` is `[HELM]`.
The tag stays out of a second line of an entry.

Sort the entries of every subsection by their first tag, in the order above, then the entries without a tag, and within each group by significance, most significant first.
Significance is how many users or operators an entry affects and how much: data loss, security, an outage or a failed upgrade outweigh a new feature, which outweighs an inconvenience.

- `### What's changed`: fixes for data loss, security and outages, and the headline features of the release, first; then other features and changes; then smaller fixes.
- `### Configuration changes`: changed defaults that change behaviour on upgrade first; then values that were ignored or rejected; then new values.
- `### Breaking changes`: what makes the upgrade fail or loses data first; then what breaks a running workload; then values to change.
- `### Deprecations`: what is most widely set first.

On an X.Y.0, entries marked `(also in ...)` follow the same order; they are not grouped at the end.
`uv run hopsworks-docs check` fails on an entry that starts with a bracketed word in capitals, or with `API`, `FRONTEND` or `HELM` in any case, that isn't exactly one of the tags followed by a space, such as `[DOCS]`, `[Api]` or the `[HELM]` of `[API][HELM]`, on tags out of order, and on an entry out of tag order in its subsection.

`### Configuration changes` lists the changes to the Helm values themselves: values added or removed, changed defaults, fixes for a value that was ignored or rejected, and changes to `values.openshift.yaml` or `values.airgap.yaml`.
A feature or fix keeps its entry under `### What's changed` and names the value that turns it on or tunes it, even when it is off by default.
Split an entry that does both, so each change is listed once.

Breaking changes are changes that need users or operators to do something when they upgrade.
Say in each one what changed, what the behaviour was before, who is affected and what to do, and link the docs page that has the procedure; it may start with what changed, such as "`helm upgrade` now stops ...", or with what to do, such as "Remove `<value>` from your values ...".
Outline the behaviour before the change in a few words, such as "instead of `default`" or "which used to keep them", so a reader can tell whether they relied on it; check it against the previous release, not the commit message.
A breaking change that a security fix needs leaves the behaviour before out, because it would describe the issue; it says only what users could do that they no longer can, such as "can no longer be queried in Trino".
A fix that takes away something users rely on is a breaking change, also when it addresses a vulnerability.
A breaking change is not repeated under `### What's changed`; a value it adds, removes or renames is still listed under `### Configuration changes`, which says what the value does, while the breaking change says what to do.
A change that ships in patch releases of two minor versions at about the same time, such as 5.0.14 and 5.1.2, is listed in both releases, without a marker; the `(also in ...)` marker is only for an X.Y.0 entry.

Deprecations are what a release marks for removal but still accepts, such as a Helm value the chart keeps only so existing values files validate.
Start each one with "Deprecated", and say what replaces it or that nothing reads it any more.
Find them in the chart's values, where they are marked `DEPRECATED` or `deprecated: true`; removing one later is a breaking change.

## Upgraded components

A table of every component whose version changed in the chart, named after the two releases it compares: `| Component | 5.1.0 | 5.1.1 |`, one row per component, sorted by name.
It compares with the release the section lists the changes since; on an X.Y.0, a version that already shipped in a patch release of the previous minor version ends with `(also in [X.Y.Z][hopsworks-X-Y-Z])`, or `(also in 4.8.N)` for 4.8, which has no pages.
A release without upgraded components has no such subsection.

Generate it with `uv run hopsworks-docs release-components X.Y.Z --helm <hopsworks-helm> --rondb-helm <rondb-helm> --write`, which needs both checkouts with their tags.
It fails with `ERROR: no checkout at <path>` when a checkout is missing.
It also fails when a version changed that no component in `scripts/release_components.py` covers; add the component to `COMPONENTS` there, or the setting to `IGNORED` when it only looks like a version, rather than editing the table by hand.
It takes the versions from the chart at both tags, not from commit messages:

- every image tag, `appVersion` and version setting in the `values.yaml` and `Chart.yaml` of each chart in `hopsworks-helm`, with the umbrella `values.yaml` overriding a subchart's;
- RonDB and its images from `rondb-helm` at the tag the `rondb` dependency names;
- for an image the chart doesn't pin, the default of the upstream chart at its dependency version from `UPSTREAM_DEFAULTS`, such as Prometheus `v2.51.2` from `prometheus` 25.20.2; it fails on a dependency version that isn't listed.

It shows the image tag as the version; if a rebuilt image's tag doesn't name what it ships, add it to `SHIPS`, which gives `8.4.5-debian-12-r0-h3 (MySQL 8.4.11)`.
A component whose version stays the same shows the first of its other settings that changed, such as a rebuilt image tag ending in `-h2`.
It leaves out the Hopsworks application, which the line under the release title gives, and prints the components and images new or removed in the release, which belong in the notes, and the chart files it couldn't parse; `release-inputs` prints both in its Upgraded components section.
