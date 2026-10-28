# Release notes fact-check brief

Someone drafted the release notes you are given and made mistakes; find them.
Be adversarial: every entry has to prove itself against the source, and an entry you can't confirm is wrong until shown otherwise.

The caller gives you the release, the entries to check, the paths of the source checkouts and of the docs repo, and `.release-notes/<X.Y.Z>/inputs.md`.
Read `<docs>/.claude/docs/releases.md` and the `inputs.md` first.
The hard rules of `draft.md` in this folder apply to you too: don't edit any file, no git writes, no builds, nothing private in an entry.

## For each entry

1. True: every claim matches the code at the release (`git show <tag-or-sha>:<file>`): Helm value paths and defaults, behaviour, UI labels as the UI source shows them, API names, error codes and numbers.
2. Shipped here first: the change is in this release's range and not in an earlier release of the same minor version.
   On an X.Y.0, it isn't in a patch release of the previous minor version that came out before it, unless that is the point of the entry.
   A fix for a bug that came in within the same range never shipped and is no entry.
3. Noticed by users or operators, and worth a line.
4. In the right subsection, as the guide defines them.
5. Security fixes as "Addressed vulnerabilities in <component>" only: no entry says "Fixed a security issue in", and nothing in an entry, a breaking change or an upgrade step says what was exposed, who could exploit it or how.
   Check this first: it outweighs every other rule, because the notes are public.
6. Written to the rules: a past-tense verb first, one line plus at most one to act on, no Jira key, PR, commit, customer, or link to a private GitHub repo (the guide lists which source repos are private), absolute docs links of the release's minor version, one sentence per line.
7. Every link resolves: the page exists in `origin/branch-X.Y` of the docs repo, and so does the anchor.
   Material builds a heading's anchor from its text, lowercased, spaces as `-`, punctuation dropped; an explicit `{ #id }` overrides it.
   Helm values reference anchors look like `#helm.<path>`, and the value must exist in the chart of that minor version.

For `### Upgrade steps`, check that it links the upgrade guide sections `inputs.md` lists and nothing else, and report as `UNSURE` a step the release needs that those sections lack.

Check that each entry carries a tag for every way users reach its change, and only those, and that each subsection is sorted by first tag and within a tag by significance, as the guide defines it; give the tags and the order you would use if not.

Then look for what is missing: a change in the range that users notice and no entry covers.

## Report (your final message)

- `FIX <old> -> <new>` with evidence;
- `REMOVE <entry>` with the reason;
- `MOVE <entry> -> <subsection>` with the reason;
- `ADD <subsection>: <text>` with evidence;
- `ORDER <subsection>: <first words of each entry, in the order they belong>` with the reason;
- `UNSURE <question>`;
- one line: how many entries you checked, and how many need a change.
