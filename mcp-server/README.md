# Hopsworks Docs MCP Server

A read-only [Model Context Protocol](https://modelcontextprotocol.io) server that
exposes the Hopsworks documentation to AI agents.
It indexes the docs Markdown (the same source that builds `docs.hopsworks.ai`)
and serves retrieval tools over stdio or streamable-http.

## Safety model

- Read-only. There is no write, create, or delete path.
- No network access. The server reads Markdown files and nothing else; syncing the docs is the entrypoint's job, outside the server process.
- Reads are confined to the docs directories.
- Tool output is capped (12k characters per call) so one call cannot flood an
  agent's context.

## Tools

| Tool | Purpose |
| ---- | ------- |
| `list_versions()` | Documentation versions the server holds, with their aliases. |
| `search_docs(query, limit, version)` | BM25 search across all pages; returns page ids, URLs, snippets. |
| `get_page(page_id, version)` | Full raw Markdown of a page by canonical id. |
| `list_sections(page_id, version)` | Heading structure and anchors of a page. |
| `get_section(page_id, anchor, version)` | One section of a page by anchor. |
| `list_pages(prefix, version)` | Browse the doc map, optionally scoped by path prefix. |

A `page_id` is the path under `docs/` without the `.md` extension, e.g.
`concepts/fs/feature_group/fg_overview`.

`version` is optional on every tool.
Empty or `latest` answers from the latest release; pass a version name such as `5.0`, or `dev` for the unreleased next version.
Every answer names the version it came from, and page URLs carry the version path (`https://docs.hopsworks.ai/5.1/...`), so they resolve on the versioned site.

## Run locally

```bash
HOPSWORKS_DOCS_DIR=/path/to/logicalclocks.github.io/docs \
HOPSWORKS_DOCS_VERSION=5.1 \
  uv run --with mcp --with pyyaml python -m hopsworks_docs_mcp
```

A local run serves the single checkout it is pointed at, under the name in `HOPSWORKS_DOCS_VERSION` (default `latest`, which is also the URL path).
Check out the `branch-X.Y` of the version you need; `main` is `dev`.
If `HOPSWORKS_DOCS_DIR` is unset, the server walks up from its own location to
find a `docs/` directory next to `mkdocs.yml`.

## Hosted deployment

A hosted instance runs at `https://mcp.hopsworks.ai/mcp` over streamable-http.
It is public, unauthenticated, and read-only, so any MCP client can connect without credentials.

The hosted instance serves every version the docs site lists.
`docker-entrypoint.sh` reads the site's `versions.json` (`DOCS_VERSIONS_URL`) and keeps one shallow, Markdown-only checkout per version under `DOCS_ROOT`: `dev` from `main`, every other version from `branch-<version>`.
It resyncs every `SYNC_INTERVAL` (default 300s), and the server reindexes the versions that changed every `MCP_REINDEX_INTERVAL` (default 60s), with no restart.
A new release is picked up on its own: once its branch exists and the site moves `latest` to it, the MCP follows.

A docs change is visible to the MCP within a few minutes of landing on its branch.
A version the site lists without a matching branch is skipped.

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `DOCS_REPO` | the docs repo on GitHub | Repository to clone. |
| `DOCS_VERSIONS_URL` | `https://docs.hopsworks.ai/versions.json` | The site's mike version list. |
| `DOCS_ROOT` | `/docs-repo` | Where the per-version checkouts live. |
| `HOPSWORKS_DOCS_SITE` | `https://docs.hopsworks.ai/` | Base of the page URLs. |

The image bakes in the server code only, never the docs.
Rebuild and redeploy the image when the server code changes; a docs change never needs an image rebuild.

## Wire into a client

See `examples/claude-code.mcp.json` (add it to your project `.mcp.json`) and
edit the two absolute paths. The same command/args/env shape works for Claude
Desktop's `claude_desktop_config.json`.

## Not yet exposed

Tools the 2026 docs roadmap calls for that are not built yet:
`diagnose_error_code` and `validate_config`, which the generated
[REST status codes](https://docs.hopsworks.ai/latest/reference/rest_error_codes/) and
[configuration variables](https://docs.hopsworks.ai/latest/setup_installation/admin/configuration_reference/)
references can now back, and `estimate_resources` (sizing) and
`check_version_compatibility`, whose content does not exist in the docs yet.
