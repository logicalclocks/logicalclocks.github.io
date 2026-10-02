# Release Pages

`docs/releases/` holds one page per release, grouped by major version (`docs/releases/<major>/<X.Y.Z>.md`), newest first in `mkdocs.yml`.
Add new releases to the top of their major's `nav:` group and to the list in `docs/releases/<major>/index.md`.

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
