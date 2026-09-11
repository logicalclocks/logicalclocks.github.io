"""Read-only MCP server exposing the Hopsworks documentation to AI agents.

The server indexes the local ``docs/`` Markdown tree (the same source that
builds ``docs.hopsworks.ai``) and exposes retrieval tools only. It never
mutates the docs, never makes outbound network calls, and confines all reads
to the docs directory. There is no write path.

Two transports, chosen by the ``MCP_TRANSPORT`` env var:

- ``stdio`` (default) — the usual local transport::

    HOPSWORKS_DOCS_DIR=/path/to/docs uv run --with mcp \\
        python -m hopsworks_docs_mcp

- ``streamable-http`` — a long-running HTTP endpoint (used for the hosted
  ``mcp.hopsworks.ai`` deployment). Served by uvicorn on ``MCP_HOST``/
  ``MCP_PORT`` behind a per-IP rate limit.

If ``HOPSWORKS_DOCS_DIR`` is unset the server walks up from this file to find a
``docs/`` directory that sits next to ``mkdocs.yml``. When the hosted deployment
keeps that directory in sync with ``main`` (an external ``git pull`` loop), set
``MCP_REINDEX_INTERVAL`` to have the server rebuild its index on change without
a restart.
"""

from __future__ import annotations

import os
import threading
import time
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


class _RefreshableIndex:
    """Holds the current :class:`DocsIndex`, rebuildable in place.

    Tool code reads ``_index.pages`` / ``_index.search`` unchanged: attribute
    access falls through to the inner index. A background watcher can call
    :meth:`refresh` to atomically swap in a freshly built index when the docs
    on disk change, so the hosted endpoint follows ``main`` without a restart.
    """

    def __init__(self, docs_dir: Path) -> None:
        self._dir = docs_dir
        self._inner = DocsIndex(docs_dir)

    def __getattr__(self, name: str):
        # Only reached for names not set on the wrapper itself (_dir, _inner).
        return getattr(self._inner, name)

    def refresh(self) -> None:
        self._inner = DocsIndex(self._dir)


_docs_dir = _find_docs_dir()
_index = _RefreshableIndex(_docs_dir)
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


class RateLimitMiddleware:
    """Per-client-IP token-bucket rate limit for the hosted HTTP endpoint.

    Pure ASGI (not Starlette's ``BaseHTTPMiddleware``) so it never buffers the
    streaming MCP response: it either rejects with 429 before the app runs, or
    passes the request straight through untouched. Behind a reverse proxy the
    real client is the first hop of ``X-Forwarded-For``.
    """

    def __init__(
        self, app, rps: float = 5.0, burst: int = 60, trust_forwarded: bool = True
    ) -> None:
        self.app = app
        self.rps = rps
        self.burst = burst
        self.trust_forwarded = trust_forwarded
        self._buckets: dict[str, tuple[float, float]] = {}
        self._lock = threading.Lock()

    def _client_ip(self, scope) -> str:
        if self.trust_forwarded:
            for name, value in scope.get("headers", []):
                if name == b"x-forwarded-for":
                    return value.decode("latin-1").split(",")[0].strip()
        client = scope.get("client")
        return client[0] if client else "unknown"

    def _allow(self, ip: str) -> bool:
        now = time.monotonic()
        with self._lock:
            tokens, last = self._buckets.get(ip, (float(self.burst), now))
            tokens = min(self.burst, tokens + (now - last) * self.rps)
            if tokens < 1.0:
                self._buckets[ip] = (tokens, now)
                return False
            # Opportunistic prune so idle IPs don't accumulate forever.
            if len(self._buckets) > 10_000:
                cutoff = now - 3600
                self._buckets = {
                    k: v for k, v in self._buckets.items() if v[1] > cutoff
                }
            self._buckets[ip] = (tokens - 1.0, now)
            return True

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http" or self._allow(self._client_ip(scope)):
            await self.app(scope, receive, send)
            return
        await send(
            {
                "type": "http.response.start",
                "status": 429,
                "headers": [
                    (b"content-type", b"text/plain; charset=utf-8"),
                    (b"retry-after", b"1"),
                ],
            }
        )
        await send({"type": "http.response.body", "body": b"Rate limit exceeded.\n"})


def _start_reindex_watcher(index: _RefreshableIndex, docs_dir: Path, interval: int) -> None:
    """Rebuild the index when the Markdown on disk changes.

    Cheap, git-agnostic change signal: the file count and newest mtime across
    ``*.md``. An external ``git pull`` that updates any page bumps the newest
    mtime; a merge that adds or removes pages changes the count.
    """

    def signature() -> tuple[int, float]:
        mtimes = [p.stat().st_mtime for p in docs_dir.rglob("*.md")]
        return (len(mtimes), max(mtimes, default=0.0))

    def loop(last: tuple[int, float]) -> None:
        while True:
            time.sleep(interval)
            try:
                current = signature()
                if current != last:
                    index.refresh()
                    last = current
            except Exception:  # noqa: BLE001 - a transient FS read must not kill the watcher
                pass

    threading.Thread(
        target=loop, args=(signature(),), daemon=True, name="reindex"
    ).start()


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    interval = int(os.environ.get("MCP_REINDEX_INTERVAL", "0"))
    if interval > 0:
        _start_reindex_watcher(_index, _docs_dir, interval)

    if transport == "streamable-http":
        import uvicorn

        # DNS-rebinding protection validates the Host header against an allowlist.
        # Behind a reverse proxy the Host is the public domain, so it must be
        # listed (comma-separated ``MCP_ALLOWED_HOSTS``); localhost stays allowed
        # for health checks and local runs. A missing Origin (non-browser MCP
        # clients) is permitted by the SDK, so only hosts need configuring.
        security = None
        allowed = [
            h.strip()
            for h in os.environ.get("MCP_ALLOWED_HOSTS", "").split(",")
            if h.strip()
        ]
        if allowed:
            from mcp.server.transport_security import TransportSecuritySettings

            security = TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=[
                    *allowed,
                    "localhost",
                    "localhost:*",
                    "127.0.0.1",
                    "127.0.0.1:*",
                ],
                allowed_origins=[f"https://{h}" for h in allowed],
            )

        app = mcp.streamable_http_app(transport_security=security)
        app.add_middleware(
            RateLimitMiddleware,
            rps=float(os.environ.get("MCP_RATE_RPS", "5")),
            burst=int(os.environ.get("MCP_RATE_BURST", "60")),
        )
        uvicorn.run(
            app,
            host=os.environ.get("MCP_HOST", "0.0.0.0"),
            port=int(os.environ.get("MCP_PORT", "8080")),
            log_level=os.environ.get("MCP_LOG_LEVEL", "info"),
        )
    else:
        mcp.run(transport)


if __name__ == "__main__":
    main()
