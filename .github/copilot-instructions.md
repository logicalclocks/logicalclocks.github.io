# Copilot Review Instructions

This repository is the Hopsworks documentation site (docs.hopsworks.ai), built with mkdocs and mike.
There is no application code; all content is Markdown files under `docs/` and configuration in `mkdocs.yml`.

## Content Type

Every page belongs in one of three directories:

- `docs/concepts/` — conceptual explanation ("what" and "why"); flag any step-by-step instructions here
- `docs/user_guides/` — procedural guides ("how to"); flag conceptual explanations mixed in
- `docs/setup_installation/` — infrastructure and admin; flag user-facing how-tos placed here

## Navigation

Every new Markdown file must have a corresponding entry in the `nav:` section of `mkdocs.yml`.
Flag any PR that adds a page without updating `mkdocs.yml`.

## Python API Reference

Do not write prose in API reference pages — all content must live in docstrings in the `hopsworks-api` repository.
Flag any custom Markdown text added to API reference pages beyond a title.

## Python Code Blocks

Python code blocks (tagged `python`, `py`, `python3`) are validated by snakeoil with ruff.
Flag blocks that are syntactically invalid, have unused imports, or violate ruff rules.
Line length limit is 88 characters.

## Markdown Style

One sentence per line throughout all prose — flag multi-sentence lines.
Unordered lists must use dashes, not asterisks or plus signs.
Flag bare URLs in prose; they should use Markdown link syntax.

## Linking

Internal cross-references use heading IDs in square brackets: `[text][heading-id]`.
Python API links use mkdocstrings syntax: `[ClassName][full.module.path.ClassName]`.
Flag any relative file paths used as links (e.g. `../other.md`) — they may break after mike versioning.

## Assets

Images must go in `docs/assets/images/<section>/` matching the section of the content that uses them.
Flag images placed directly in content directories.

## Spelling and Terminology

Flag typos and spelling mistakes.
Prefer "Hopsworks" (not "HopsWorks" or "hopsworks") in prose.
Prefer "Feature Store", "Feature Group", "Feature View" (capitalized as proper nouns).

## General Review Practices

Flag content that duplicates information already present elsewhere in the docs without adding value.
Flag admonitions that state a restriction without explaining why.
Flag broken or missing links to other sections.
Flag images with no surrounding context or explanation in the prose.
