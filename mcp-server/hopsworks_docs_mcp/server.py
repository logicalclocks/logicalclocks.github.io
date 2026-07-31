"""Read-only MCP server exposing the Hopsworks documentation to AI agents.

The server indexes the local ``docs/`` Markdown tree (the same source that
builds ``docs.hopsworks.ai``) and exposes retrieval tools only. It never
mutates the docs, never reaches the network, and confines all reads to the
docs directory. There is no write path.

Run over stdio (the usual MCP transport):

    HOPSWORKS_DOCS_DIR=/path/to/docs uv run --with mcp \\
        python -m hopsworks_docs_mcp

If ``HOPSWORKS_DOCS_DIR`` is unset the server walks up from this file to find a
``docs/`` directory that sits next to ``mkdocs.yml``.
"""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .index import DocsIndex

# Every tool here is read-only: no writes, no side effects, safe to retry.
_READ_ONLY = ToolAnnotations(read_only_hint=True, idempotent_hint=True)

# Cap tool output so a single call cannot flood an agent's context.
_MAX_CHARS = 12_000


def _find_docs_dir() -> Path:
    env = os.environ.get("HOPSWORKS_DOCS_DIR")
    if env:
        path = Path(env).expanduser().resolve()
        if not (path / "..").resolve().joinpath("mkdocs.yml").exists() and not any(
            path.glob("*.md")
        ):
            raise SystemExit(f"HOPSWORKS_DOCS_DIR={path} has no Markdown files")
        return path
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "docs"
        if (parent / "mkdocs.yml").exists() and candidate.is_dir():
            return candidate
    raise SystemExit(
        "Could not locate docs/. Set HOPSWORKS_DOCS_DIR to the docs directory."
    )


_index = DocsIndex(_find_docs_dir())
mcp = MCPServer(
    "hopsworks-docs",
    instructions=(
        "Read-only access to the Hopsworks documentation. Start with search_docs "
        "when you don't know the page id, then get_page or get_section. page_id is "
        "the path under docs/ without .md, e.g. concepts/fs/feature_group/fg_overview."
    ),
)


def _clip(text: str) -> str:
    if len(text) <= _MAX_CHARS:
        return text
    return text[:_MAX_CHARS] + f"\n\n… [truncated at {_MAX_CHARS} chars]"


@mcp.tool(annotations=_READ_ONLY)
def search_docs(query: str, limit: int = 5) -> str:
    """Search the Hopsworks documentation and return the best-matching pages.

    Use this first when you don't already know the exact page id. It ranks
    every documentation page against the query (BM25) and returns their id,
    title, URL and a matching snippet. Do NOT use it to fetch a page whose id
    you already have; call get_page instead.

    Args:
        query: natural-language or keyword query, e.g. "online feature store
            latency" or "create an external feature group".
        limit: maximum results (1-20, default 5).

    Returns a ranked list; each item shows the page_id to pass to get_page.

    Example: search_docs("kafka storage connector", 3).
    """
    limit = max(1, min(20, limit))
    hits = _index.search(query, limit)
    if not hits:
        return f'No documentation page matched "{query}".'
    lines = [f'{len(hits)} result(s) for "{query}":\n']
    for page, score, snippet in hits:
        lines.append(f"- page_id: {page.page_id}")
        lines.append(f"  title: {page.title}")
        lines.append(f"  url: {page.url}")
        lines.append(f"  score: {score:.2f}")
        lines.append(f"  snippet: {snippet}\n")
    return _clip("\n".join(lines))


@mcp.tool(annotations=_READ_ONLY)
def get_page(page_id: str) -> str:
    """Return the full raw Markdown of one documentation page by its id.

    Use this once you know the page id (from search_docs or list_pages). The
    id is the path under docs/ without the .md extension, e.g.
    "concepts/fs/feature_group/fg_overview". If the page is long, prefer
    list_sections + get_section to fetch only the part you need.

    Args:
        page_id: canonical page id (no leading slash, no .md).

    Returns the page's Markdown source, or an error listing near matches.
    """
    page = _index.pages.get(page_id.strip().strip("/"))
    if page is None:
        near = [p for p in _index.pages if page_id.strip("/") in p][:5]
        hint = ("\nDid you mean:\n" + "\n".join(near)) if near else ""
        return f'No page with id "{page_id}". Use search_docs or list_pages.{hint}'
    return _clip(f"# {page.title}\nurl: {page.url}\n\n{page.markdown}")


@mcp.tool(annotations=_READ_ONLY)
def list_sections(page_id: str) -> str:
    """List the section headings and their anchors for one page.

    Use this to see a page's structure before pulling a single section with
    get_section, instead of fetching the whole page. Not useful for pages with
    no headings.

    Args:
        page_id: canonical page id (see get_page).

    Returns each heading with its level and anchor.
    """
    page = _index.pages.get(page_id.strip().strip("/"))
    if page is None:
        return f'No page with id "{page_id}". Use search_docs or list_pages.'
    sections = page.sections()
    if not sections:
        return f'Page "{page_id}" has no sub-headings; use get_page.'
    lines = [f"Sections of {page_id}:\n"]
    for s in sections:
        lines.append(f"- [{'#' * s.level}] {s.title}  (anchor: {s.anchor})")
    return "\n".join(lines)


@mcp.tool(annotations=_READ_ONLY)
def get_section(page_id: str, anchor: str) -> str:
    """Return one section of a page by its anchor.

    Use this to fetch a targeted part of a long page (the anchor comes from
    list_sections, or from a URL fragment like #online-api). Do NOT guess the
    anchor; call list_sections first if unsure.

    Args:
        page_id: canonical page id (see get_page).
        anchor: section anchor, with or without a leading '#'.

    Returns the heading and the prose beneath it up to the next heading.
    """
    page = _index.pages.get(page_id.strip().strip("/"))
    if page is None:
        return f'No page with id "{page_id}". Use search_docs or list_pages.'
    want = anchor.strip().lstrip("#")
    for s in page.sections():
        if s.anchor == want:
            return _clip(f"# {s.title}\n{page.url}#{s.anchor}\n\n{s.body}")
    available = ", ".join(s.anchor for s in page.sections()) or "(none)"
    return f'No anchor "{want}" on {page_id}. Available: {available}'


@mcp.tool(annotations=_READ_ONLY)
def list_pages(prefix: str = "") -> str:
    """List documentation page ids, optionally filtered by a path prefix.

    Use this to browse the doc map or to enumerate a subsection (e.g. prefix
    "user_guides/fs" for all Feature Store guides). With no prefix it returns
    every page id, which can be large, so pass a prefix to scope it.

    Args:
        prefix: path prefix under docs/, e.g. "concepts/mlops". Empty = all.

    Returns matching page ids with their titles.
    """
    prefix = prefix.strip().strip("/")
    ids = sorted(pid for pid in _index.pages if pid.startswith(prefix))
    if not ids:
        return f'No pages under prefix "{prefix}".'
    lines = [f"{len(ids)} page(s):\n"]
    for pid in ids:
        lines.append(f"- {pid}: {_index.pages[pid].title}")
    return _clip("\n".join(lines))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
