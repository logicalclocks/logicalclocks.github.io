# Hopsworks Documentation

## Commands

```bash
uv venv && uv pip install -r requirements-docs.txt # setup
uv pip install "git+https://github.com/logicalclocks/hopsworks-api.git@main#subdirectory=python" # install Python API (needed for API docs section)
touch docs/javadoc; uv run mkdocs build -s; rm docs/javadoc # build (strict)
uv run mike deploy <version> latest --update-alias # build a versioned bundle to the gh-pages worktree (use repo's current version, e.g. 4.4); first time only: `uv run mike set-default latest`
uv run mike serve # serve the gh-pages worktree locally (preview); does NOT live-reload from source — re-run `mike deploy` after edits
npx markdownlint-cli2 "**/*.md" # lint Markdown (requires Node.js)
uv tool install md-snakeoil && snakeoil --line-length 88 --rules "E,F,B,C4,ISC,PIE,PYI,Q,RSE,RET,SIM,TC,I,W,D2,D3,D4,INP,UP,FA" docs # lint Python code blocks
```

`uv run mkdocs serve` is available too, but its livereload watcher does not fire rebuilds in this repo's plugin combination on macOS — `mike serve` is the canonical preview tool per the repo README.

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
