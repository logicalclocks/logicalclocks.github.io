# Hopsworks Docs MCP Server

A read-only [Model Context Protocol](https://modelcontextprotocol.io) server that
exposes the Hopsworks documentation to AI agents.
It indexes the local `docs/` Markdown tree (the same source that builds
`docs.hopsworks.ai`) and serves retrieval tools over stdio.

## Safety model

- Read-only. There is no write, create, or delete path.
- No network access. The server reads Markdown files and nothing else.
- Reads are confined to the docs directory.
- Tool output is capped (12k characters per call) so one call cannot flood an
  agent's context.

## Tools

| Tool | Purpose |
| ---- | ------- |
| `search_docs(query, limit)` | BM25 search across all pages; returns page ids, URLs, snippets. |
| `get_page(page_id)` | Full raw Markdown of a page by canonical id. |
| `list_sections(page_id)` | Heading structure and anchors of a page. |
| `get_section(page_id, anchor)` | One section of a page by anchor. |
| `list_pages(prefix)` | Browse the doc map, optionally scoped by path prefix. |

A `page_id` is the path under `docs/` without the `.md` extension, e.g.
`concepts/fs/feature_group/fg_overview`.

## Run

```bash
HOPSWORKS_DOCS_DIR=/path/to/logicalclocks.github.io/docs \
  uv run --with mcp python -m hopsworks_docs_mcp
```

If `HOPSWORKS_DOCS_DIR` is unset, the server walks up from its own location to
find a `docs/` directory next to `mkdocs.yml`.

## Hosted deployment

A hosted instance runs at `https://mcp.hopsworks.ai/mcp` over streamable-http.
It is public, unauthenticated, and read-only, so any MCP client can connect without credentials.

The hosted instance tracks the `main` branch of this repo.
It does not serve the released, mike-versioned `docs.hopsworks.ai` site, and it does not see feature branches or local working trees.
`docker-entrypoint.sh` keeps a shallow clone of `main` and pulls it every `SYNC_INTERVAL` (default 300s), and the server reindexes on change every `MCP_REINDEX_INTERVAL` (default 60s), so the endpoint follows `main` with no restart.

A docs change is therefore visible to the MCP within a few minutes of landing on `main`.
Work that lives only on a feature branch or an unpushed working tree is invisible until it merges to `main`.

The image bakes in the server code only, never the docs.
Rebuild and redeploy the image when the server code changes; a docs change never needs an image rebuild.

## Wire into a client

See `examples/claude-code.mcp.json` (add it to your project `.mcp.json`) and
edit the two absolute paths. The same command/args/env shape works for Claude
Desktop's `claude_desktop_config.json`.

## Not yet exposed

Tools the 2026 docs roadmap calls for but whose underlying content does not
exist in the docs yet: `diagnose_error_code`, `estimate_resources` (sizing),
`validate_config`, `check_version_compatibility`. They are intentionally
omitted rather than stubbed: they will be added once the error catalogue,
sizing logic and config reference land in `docs/`.
