# Hopsworks Documentation

## Commands

```bash
uv venv && uv pip install -r requirements-docs.txt # setup
uv pip install "git+https://github.com/logicalclocks/hopsworks-api.git@main#subdirectory=python" # install Python API (needed for API docs section)
touch docs/javadoc; uv run mkdocs build -s; rm docs/javadoc # build (strict)
uv run mkdocs serve # preview with live reload
npx markdownlint-cli2 "**/*.md" # lint Markdown (requires Node.js)
uv tool install md-snakeoil && snakeoil --line-length 88 --rules "E,F,B,C4,ISC,PIE,PYI,Q,RSE,RET,SIM,TC,I,W,D2,D3,D4,INP,UP,FA" docs # lint Python code blocks
```

## Rules

- One sentence per line in all Markdown prose
- Every new page must have an entry in the `nav:` section of `mkdocs.yml`
- `concepts/` is for "what" and "why"; `user_guides/` is for "how to"; `setup_installation/` is for infrastructure and admin
- Python code blocks in Markdown must be syntactically valid and pass snakeoil/ruff at line length 88
- Do not write prose in API reference pages — edit docstrings in `hopsworks-api` instead
- Never commit credentials, API keys, or tokens

## Agent Docs

- @docs/README.md — full command reference, content structure, and links to detail docs
- @docs/content.md — writing conventions, code blocks, linking, and assets
- @docs/caveats/README.md — known gotchas; add new ones as separate files in this folder
