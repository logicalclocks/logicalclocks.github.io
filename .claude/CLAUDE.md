# Hopsworks Documentation

## Commands

```bash
uv sync --extra cli # setup: mkdocs plus the hopsworks-docs CLI in .venv
uv pip install ../hopsworks-api/python # Python API for the API docs section; CI clones hopsworks-api next to this repo
uv run hopsworks-docs check # build in strict mode (creates the docs/javadoc stub itself)
uv run hopsworks-docs serve # preview with live reload
uv run hopsworks-docs markdownlint # lint Markdown
uv run hopsworks-docs snakeoil # lint Python code blocks (ruff at line length 88)
uv run hopsworks-docs linkchecker # check for broken links
```

## Rules

- One sentence per line in all Markdown prose
- Every new page must have an entry in the `nav:` section of `mkdocs.yml`
- `concepts/` is for "what" and "why"; `user_guides/` is for "how to"; `setup_installation/` is for infrastructure and admin
- Python code blocks in Markdown must be syntactically valid and pass snakeoil/ruff at line length 88
- Do not write prose in API reference pages — edit docstrings in `hopsworks-api` instead
- Never commit credentials, API keys, or tokens
- Never write anything that helps exploit a vulnerability, fixed or not, in a page, a commit message or a PR: not what was exposed, who could exploit it, how or under which conditions, and not what users could do before a fix or can no longer do. A change a security fix needs says what to do, at most that it addresses a vulnerability, and only the effects an operator acts on, such as an error code or a value to set; an opt-out value "keeps the behaviour of X.Y.Z, without the fix". The docs and this repo are public, and clusters that haven't upgraded stay vulnerable.

## Agent Docs

- @docs/README.md — full command reference, content structure, and links to detail docs
- @docs/content.md — writing conventions, code blocks, linking, and assets
- @docs/design-system.md — visual language: tokens, logo, nav, search, diagrams; read before any CSS/nav/visual change
- @docs/captures.md — UI screenshots and GIFs: where the pixels come from, browser session, scoping rules, helpers
- @docs/caveats/README.md — known gotchas; add new ones as separate files in this folder
