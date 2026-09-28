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

## API reference box

A guide ends its code walkthrough (or each walkthrough section, when a page has several) with an `api` admonition, never a bare `### API Reference` heading with loose links.
Rows are the mkdocstrings symbol badge plus the autoref, exactly what the reader lands on in the API section: entry-point methods first, then each class with the methods the guide called nested under it, then any external doc with a muted `docs` badge.
No prose per row.
The last line is the single CTA into the Python API, with the `../` depth matching the page URL.

```markdown
!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_kafka_api`][hopsworks_common.project.Project.get_kafka_api]
    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaApi`][hopsworks_common.core.kafka_api.KafkaApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_topic`][hopsworks_common.core.kafka_api.KafkaApi.create_topic]
    - <code class="doc-symbol doc-symbol-docs"></code> [Kafka docs](https://kafka.apache.org/documentation/)

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
```

Badges: `class`, `method`, `function`, `attribute`, `docs`.
The `python-api/` root is not a page; link to `python-api/hopsworks/`.
