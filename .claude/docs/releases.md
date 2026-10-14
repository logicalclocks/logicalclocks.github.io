# Release Pages

The release pages are one site for every docs version, at `https://docs.hopsworks.ai/releases/`.
Every docs version links to it from its nav, so a release note is written once and never backported.

The source is `docs/releases/` on `main` only.
`mkdocs.releases.yml` builds it, and the release workflow deploys it with mike as the hidden version `releases` on every push to `main`.
The versioned docs leave `docs/releases/` out with `exclude_docs`, and CI fails a PR to a `branch-*` that touches it, because release branches never publish it.

Each release has one page, grouped by major version (`docs/releases/<major>/<X.Y.Z>.md`), newest first.
Add a new release to the top of its major's group in the `nav:` of `mkdocs.releases.yml`; the table in `docs/releases/<major>/index.md` is generated.
A new major also needs `docs/releases/<major>/index.md` holding `# Hopsworks <major>.x` and `<!-- releases -->`, a nav group, and a link in `docs/releases/index.md`.
`uv run hopsworks-docs check` builds this site too, and fails if hopsworks-api has no tag for a Python client version a page links; preview it with `uv run mkdocs serve -f mkdocs.releases.yml`.

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
