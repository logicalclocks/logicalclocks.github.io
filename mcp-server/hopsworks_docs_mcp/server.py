"""Read-only MCP server exposing the Hopsworks documentation to AI agents.

The server indexes the docs Markdown (the same source that builds
``docs.hopsworks.ai``) and exposes retrieval tools only. It never mutates the
docs, never makes outbound network calls, and confines all reads to the docs
directories. There is no write path.

Two layouts, chosen by the environment:

- ``HOPSWORKS_DOCS_ROOT`` (hosted): a directory holding the site's mike
  ``versions.json`` and one checkout of the docs repo per version, named after
  the version (``5.1/docs``, ``5.0/docs``, ``dev/docs``). Every tool takes a
  ``version`` argument and defaults to the version aliased ``latest``. An
  external sync loop (``docker-entrypoint.sh``) keeps the tree current.
- ``HOPSWORKS_DOCS_DIR`` (local): a single ``docs/`` directory, served as
  ``HOPSWORKS_DOCS_VERSION`` (default ``latest``). If unset, the server walks up
  from this file to find a ``docs/`` directory next to ``mkdocs.yml``.

Page URLs are built on ``HOPSWORKS_DOCS_SITE`` (default
``https://docs.hopsworks.ai/``) plus the version path, so they resolve on the
versioned site.

Two transports, chosen by ``MCP_TRANSPORT``: ``stdio`` (default) and
``streamable-http`` (the hosted ``mcp.hopsworks.ai`` endpoint, served by
uvicorn on ``MCP_HOST``/``MCP_PORT`` behind a per-IP rate limit). Set
``MCP_REINDEX_INTERVAL`` to rebuild the indexes when the docs on disk change,
without a restart.
"""

from __future__ import annotations

import contextlib
import json
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .index import DocsIndex, Page


# Every tool here is read-only: no writes, no side effects, safe to retry.
_READ_ONLY = ToolAnnotations(read_only_hint=True, idempotent_hint=True)

# Cap tool output so a single call cannot flood an agent's context.
_MAX_CHARS = 12_000

_SITE = os.environ.get("HOPSWORKS_DOCS_SITE", "https://docs.hopsworks.ai/").rstrip("/")


@dataclass
class _Version:
    """One documentation version: its mike name, aliases and index."""

    name: str
    aliases: list[str]
    hidden: bool
    docs_dir: Path
    signature: tuple[int, float]
    index: DocsIndex


def _signature(docs_dir: Path) -> tuple[int, float]:
    """Cheap change signal: the ``*.md`` count and newest mtime."""
    mtimes = [p.stat().st_mtime for p in docs_dir.rglob("*.md")]
    return (len(mtimes), max(mtimes, default=0.0))


def _find_local_docs_dir() -> Path:
    env = os.environ.get("HOPSWORKS_DOCS_DIR")
    if env:
        path = Path(env).expanduser().resolve()
        if not any(path.rglob("*.md")):
            raise SystemExit(f"HOPSWORKS_DOCS_DIR={path} has no Markdown files")
        return path
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "docs"
        if (parent / "mkdocs.yml").exists() and candidate.is_dir():
            return candidate
    raise SystemExit(
        "Could not locate docs/. Set HOPSWORKS_DOCS_DIR to the docs directory, "
        "or HOPSWORKS_DOCS_ROOT to a versioned docs tree."
    )


class _Library:
    """The documentation versions this server can answer from.

    In the hosted layout the versions and the ``latest`` alias come from the
    site's own ``versions.json``, so the server follows the published site with
    no version list of its own. :meth:`refresh` rereads it and rebuilds only the
    versions whose Markdown changed; lookups see either the old or the new map,
    never a half-built one.
    """

    def __init__(self) -> None:
        root = os.environ.get("HOPSWORKS_DOCS_ROOT")
        self._root = Path(root).expanduser().resolve() if root else None
        self._local = None if self._root else _find_local_docs_dir()
        self._versions: dict[str, _Version] = {}
        self._lock = threading.Lock()
        self.refresh()
        if not self._versions:
            raise SystemExit(f"No documentation versions found under {self._root}")

    def _entries(self) -> list[tuple[str, list[str], bool, Path]]:
        if self._local is not None:
            name = os.environ.get("HOPSWORKS_DOCS_VERSION", "latest")
            return [(name, [], False, self._local)]
        raw = json.loads((self._root / "versions.json").read_text(encoding="utf-8"))
        out = []
        for entry in raw:
            docs_dir = self._root / entry["version"] / "docs"
            if docs_dir.is_dir():
                hidden = bool(entry.get("properties", {}).get("hidden", False))
                out.append(
                    (entry["version"], entry.get("aliases", []), hidden, docs_dir)
                )
        return out

    def refresh(self) -> None:
        with self._lock:
            current = self._versions
            fresh: dict[str, _Version] = {}
            for name, aliases, hidden, docs_dir in self._entries():
                signature = _signature(docs_dir)
                old = current.get(name)
                if old is not None and old.signature == signature:
                    index = old.index
                else:
                    index = DocsIndex(docs_dir, site_url=f"{_SITE}/{name}/")
                fresh[name] = _Version(
                    name, aliases, hidden, docs_dir, signature, index
                )
            self._versions = fresh

    def all(self) -> list[_Version]:
        return list(self._versions.values())

    def default(self) -> _Version:
        versions = self._versions
        for v in versions.values():
            if "latest" in v.aliases:
                return v
        return next(v for v in versions.values() if not v.hidden)

    def resolve(self, version: str) -> _Version | str:
        """Return the version, or an error message naming the valid ones."""
        want = version.strip()
        if not want or want == "latest":
            return self.default()
        versions = self._versions
        if want in versions:
            return versions[want]
        for v in versions.values():
            if want in v.aliases:
                return v
        names = ", ".join(v.name for v in versions.values())
        return (
            f'No documentation version "{want}". Available: {names}. Use list_versions.'
        )


_library = _Library()
mcp = MCPServer(
    "hopsworks-docs",
    instructions=(
        "Read-only access to the Hopsworks documentation. Start with search_docs "
        "when you don't know the page id, then get_page or get_section. page_id is "
        "the path under docs/ without .md, e.g. concepts/fs/feature_group/fg_overview. "
        "Every tool answers from the latest release unless you pass version, "
        'e.g. version="5.0"; list_versions shows what exists.'
    ),
)


def _clip(text: str) -> str:
    if len(text) <= _MAX_CHARS:
        return text
    return text[:_MAX_CHARS] + f"\n\n… [truncated at {_MAX_CHARS} chars]"


def _page(v: _Version, page_id: str) -> Page | None:
    return v.index.pages.get(page_id.strip().strip("/"))


def _no_page(v: _Version, page_id: str) -> str:
    return (
        f'No page with id "{page_id}" in version {v.name}. '
        "Use search_docs or list_pages."
    )


@mcp.tool(annotations=_READ_ONLY)
def list_versions() -> str:
    """List the documentation versions this server can answer from.

    Every other tool defaults to the latest release; pass one of these names
    as their version argument to read the docs of an older release, or "dev"
    for the unreleased next version.

    Returns each version with its aliases.
    """
    lines = ["Documentation versions (newest first):\n"]
    for v in _library.all():
        tags = [*v.aliases, *(["unreleased"] if v.hidden else [])]
        suffix = f" ({', '.join(tags)})" if tags else ""
        lines.append(f"- {v.name}{suffix}: {len(v.index.pages)} pages")
    return "\n".join(lines)


@mcp.tool(annotations=_READ_ONLY)
def search_docs(query: str, limit: int = 5, version: str = "") -> str:
    """Search the Hopsworks documentation and return the best-matching pages.

    Use this first when you don't already know the exact page id. It ranks
    every documentation page against the query (BM25) and returns their id,
    title, URL and a matching snippet. Do NOT use it to fetch a page whose id
    you already have; call get_page instead.

    Args:
        query: natural-language or keyword query, e.g. "online feature store
            latency" or "create an external feature group".
        limit: maximum results (1-20, default 5).
        version: documentation version, e.g. "5.0" or "dev". Empty or
            "latest" = the latest release. See list_versions.

    Returns a ranked list; each item shows the page_id to pass to get_page.

    Example: search_docs("kafka storage connector", 3).
    """
    v = _library.resolve(version)
    if isinstance(v, str):
        return v
    limit = max(1, min(20, limit))
    hits = v.index.search(query, limit)
    if not hits:
        return f'No documentation page matched "{query}" in version {v.name}.'
    lines = [f'{len(hits)} result(s) for "{query}" in version {v.name}:\n']
    for page, score, snippet in hits:
        lines.append(f"- page_id: {page.page_id}")
        lines.append(f"  title: {page.title}")
        lines.append(f"  url: {page.url}")
        lines.append(f"  score: {score:.2f}")
        lines.append(f"  snippet: {snippet}\n")
    return _clip("\n".join(lines))


@mcp.tool(annotations=_READ_ONLY)
def get_page(page_id: str, version: str = "") -> str:
    """Return the full raw Markdown of one documentation page by its id.

    Use this once you know the page id (from search_docs or list_pages). The
    id is the path under docs/ without the .md extension, e.g.
    "concepts/fs/feature_group/fg_overview". If the page is long, prefer
    list_sections + get_section to fetch only the part you need.

    Args:
        page_id: canonical page id (no leading slash, no .md).
        version: documentation version, e.g. "5.0" or "dev". Empty or
            "latest" = the latest release. See list_versions.

    Returns the page's Markdown source, or an error listing near matches.
    """
    v = _library.resolve(version)
    if isinstance(v, str):
        return v
    page = _page(v, page_id)
    if page is None:
        near = [p for p in v.index.pages if page_id.strip("/") in p][:5]
        hint = ("\nDid you mean:\n" + "\n".join(near)) if near else ""
        return _no_page(v, page_id) + hint
    return _clip(
        f"# {page.title}\nversion: {v.name}\nurl: {page.url}\n\n{page.markdown}"
    )


@mcp.tool(annotations=_READ_ONLY)
def list_sections(page_id: str, version: str = "") -> str:
    """List the section headings and their anchors for one page.

    Use this to see a page's structure before pulling a single section with
    get_section, instead of fetching the whole page. Not useful for pages with
    no headings.

    Args:
        page_id: canonical page id (see get_page).
        version: documentation version, e.g. "5.0" or "dev". Empty or
            "latest" = the latest release. See list_versions.

    Returns each heading with its level and anchor.
    """
    v = _library.resolve(version)
    if isinstance(v, str):
        return v
    page = _page(v, page_id)
    if page is None:
        return _no_page(v, page_id)
    sections = page.sections()
    if not sections:
        return f'Page "{page_id}" has no sub-headings; use get_page.'
    lines = [f"Sections of {page_id} (version {v.name}):\n"]
    for s in sections:
        lines.append(f"- [{'#' * s.level}] {s.title}  (anchor: {s.anchor})")
    return "\n".join(lines)


@mcp.tool(annotations=_READ_ONLY)
def get_section(page_id: str, anchor: str, version: str = "") -> str:
    """Return one section of a page by its anchor.

    Use this to fetch a targeted part of a long page (the anchor comes from
    list_sections, or from a URL fragment like #online-api). Do NOT guess the
    anchor; call list_sections first if unsure.

    Args:
        page_id: canonical page id (see get_page).
        anchor: section anchor, with or without a leading '#'.
        version: documentation version, e.g. "5.0" or "dev". Empty or
            "latest" = the latest release. See list_versions.

    Returns the heading and the prose beneath it up to the next heading.
    """
    v = _library.resolve(version)
    if isinstance(v, str):
        return v
    page = _page(v, page_id)
    if page is None:
        return _no_page(v, page_id)
    want = anchor.strip().lstrip("#")
    for s in page.sections():
        if s.anchor == want:
            return _clip(
                f"# {s.title}\nversion: {v.name}\n{page.url}#{s.anchor}\n\n{s.body}"
            )
    available = ", ".join(s.anchor for s in page.sections()) or "(none)"
    return f'No anchor "{want}" on {page_id}. Available: {available}'


@mcp.tool(annotations=_READ_ONLY)
def list_pages(prefix: str = "", version: str = "") -> str:
    """List documentation page ids, optionally filtered by a path prefix.

    Use this to browse the doc map or to enumerate a subsection (e.g. prefix
    "user_guides/fs" for all Feature Store guides). With no prefix it returns
    every page id, which can be large, so pass a prefix to scope it.

    Args:
        prefix: path prefix under docs/, e.g. "concepts/mlops". Empty = all.
        version: documentation version, e.g. "5.0" or "dev". Empty or
            "latest" = the latest release. See list_versions.

    Returns matching page ids with their titles.
    """
    v = _library.resolve(version)
    if isinstance(v, str):
        return v
    prefix = prefix.strip().strip("/")
    pages = v.index.pages
    ids = sorted(pid for pid in pages if pid.startswith(prefix))
    if not ids:
        return f'No pages under prefix "{prefix}" in version {v.name}.'
    lines = [f"{len(ids)} page(s) in version {v.name}:\n"]
    for pid in ids:
        lines.append(f"- {pid}: {pages[pid].title}")
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


def _start_reindex_watcher(library: _Library, interval: int) -> None:
    """Rebuild changed versions when the docs on disk change.

    The sync loop adds, removes or updates version checkouts; each tick rereads
    ``versions.json`` and reindexes only the versions whose Markdown count or
    newest mtime moved.
    """

    def loop() -> None:
        while True:
            time.sleep(interval)
            # A transient FS read must not kill the watcher.
            with contextlib.suppress(Exception):
                library.refresh()

    threading.Thread(target=loop, daemon=True, name="reindex").start()


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    interval = int(os.environ.get("MCP_REINDEX_INTERVAL", "0"))
    if interval > 0:
        _start_reindex_watcher(_library, interval)

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
