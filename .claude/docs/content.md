# Content Guide

## Writing Style

One sentence per line throughout all prose.
Use dashes for unordered lists.
Use proper sentences: capital letter, ending punctuation.
Never write a warning or restriction without explaining why.

## Markdown Lint Rules

Markdownlint config is in `.markdownlint.yaml`.
Disabled rules: MD013 (line length), MD033 (inline HTML), MD041 (first heading), MD045 (alt text), MD046 (code block style), MD052 (link refs).

## Python Code Blocks

Python code blocks (`python`, `py`, `python3`) are validated by snakeoil using ruff.
They must be syntactically valid and pass ruff at line length 88 with the rule set: `E,F,B,C4,ISC,PIE,PYI,Q,RSE,RET,SIM,TC,I,W,D2,D3,D4,INP,UP,FA`.
Snakeoil may append a trailing newline inside code blocks — CI checks for and removes these with a one-liner after running snakeoil.

## Linking

Link to other docs pages using the heading ID: `[text][heading-id]`.
Link to Python API entities using mkdocstrings syntax: `` [`ClassName`][full.module.path.ClassName] ``.
Use standard Markdown for external links: `[text](https://...)`.
Avoid relative file paths as links (e.g. `../other.md`) — they break after mike versioning.

## Assets

Images go in `docs/assets/images/<section>/` matching the section of the content that uses them.
