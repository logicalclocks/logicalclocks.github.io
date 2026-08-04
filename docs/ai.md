# Docs for AI agents

The Hopsworks documentation is published in machine-readable form so agents and LLM tools can consume it directly.
There are two ways to use it: a live MCP server, and a set of static text artifacts.

## MCP server

`mcp.hopsworks.ai` is a read-only [Model Context Protocol](https://modelcontextprotocol.io) server over this documentation.
It indexes the same Markdown that builds this site and exposes retrieval tools to any MCP-capable client.
It is read-only: there is no write, create, or delete path, and it makes no outbound network calls.
The endpoint is rate-limited per client IP.

The tools it exposes:

| Tool | Purpose |
| ---- | ------- |
| `search_docs(query, limit)` | Full-text (BM25) search across all pages; returns page ids, URLs, and snippets. |
| `get_page(page_id)` | Full Markdown of a page by its canonical id. |
| `list_sections(page_id)` | Heading structure and anchors of a page. |
| `get_section(page_id, anchor)` | One section of a page by anchor. |
| `list_pages(prefix)` | Browse the doc map, optionally scoped by a path prefix. |

A `page_id` is the path of a page without the `.md` extension, for example `concepts/fs/feature_group/fg_overview`.

### Connect from Claude Code

Add the server at user scope so it is available in every project:

```bash
claude mcp add --transport http hopsworks-docs -s user https://mcp.hopsworks.ai/mcp
```

### Connect from Claude Desktop

Add the server to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hopsworks-docs": {
      "type": "http",
      "url": "https://mcp.hopsworks.ai/mcp"
    }
  }
}
```

### Any other MCP client

Point the client at the streamable-HTTP endpoint `https://mcp.hopsworks.ai/mcp`.
Clients that only speak stdio can run the server locally instead: see the `mcp-server/` directory in the [documentation repository](https://github.com/logicalclocks/logicalclocks.github.io) for the self-host command.

## Text artifacts

Every build also emits static files, so an agent can ingest the docs without an MCP client.

- [`llms.txt`](https://docs.hopsworks.ai/llms.txt) is a curated index of the documentation that mirrors the site navigation, following the [llmstxt.org](https://llmstxt.org) convention.
- [`llms-full.txt`](https://docs.hopsworks.ai/llms-full.txt) is the full-text Markdown corpus of every page, for bulk ingestion.
- Every page has a raw Markdown sibling: append `.md` to any page URL, for example `https://docs.hopsworks.ai/concepts/fti_pipelines.md`.

## Copy for LLM

Every page carries a **Copy for LLM** button at the top.
It copies the page's raw Markdown to your clipboard, ready to paste into a chat or prompt.
