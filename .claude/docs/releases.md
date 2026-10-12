# Release Pages

The release pages are one site for every docs version, at `https://docs.hopsworks.ai/releases/`.
Every docs version links to it from its nav, so a release note is written once and never backported.

The source is `docs/releases/` on `main` only.
`mkdocs.releases.yml` builds it, and the release workflow deploys it with mike as the hidden version `releases` on every push to `main`.
The versioned docs leave `docs/releases/` out with `exclude_docs`, and CI fails a PR to a `branch-*` that touches it, because release branches never publish it.

Each release has one page, grouped by major version (`docs/releases/<major>/<X.Y.Z>.md`), newest first.
Add a new release to the top of its major's group in the `nav:` of `mkdocs.releases.yml` and to the list in `docs/releases/<major>/index.md`.
`uv run hopsworks-docs check` builds this site too; preview it with `uv run mkdocs serve -f mkdocs.releases.yml`.

## Page shape

Each page has three sections, in this order: `## Release notes`, `## Breaking changes`, `## Migrations`.
A section with nothing to report keeps its heading and says so in one sentence, for example "There are no breaking changes in this release."

## Writing entries

- Write for users and operators, not developers; an entry is not a commit message.
- Keep each entry to one or two lines.
- Start with a past-tense verb: Added, Changed, Deprecated, Removed, Fixed, Upgraded.
- Name the exact API, Helm value, config variable or CLI flag.
- Leave out changes with no user-visible effect: tests, CI, refactors, and fixes for bugs that never shipped.
- Do not link Jira or private GitHub repos and do not name customers, because the docs are public.

Release notes are one flat list with no subcategories.

Breaking changes are changes that need users or operators to do something when they upgrade.
Start each one with `**Action required:**` and say what changed, who is affected and what to do.

Migrations are numbered steps under `### Before the upgrade`, `### Upgrade` and `### After the upgrade`.
Mark each step as required or optional, give copy-paste commands with `<placeholders>`, and say when a step can't be undone.
