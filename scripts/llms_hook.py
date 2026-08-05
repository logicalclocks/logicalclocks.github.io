"""MkDocs build hook: emit AI-native, machine-readable artifacts.

Produced into the built site (no third-party dependency, pure mkdocs hook):

- ``<page>.md``     raw Markdown source served next to every rendered HTML page,
                    so an agent can fetch the source instead of parsing HTML.
- ``llms.txt``      curated index of the docs, following the site navigation.
- ``llms-full.txt`` full-text Markdown corpus of every page, for LLM ingestion.

``llms.txt`` / ``llms-full.txt`` follow the community proposal at
https://llmstxt.org — a convention, not a formal W3C or IETF standard.

Wired via the ``hooks:`` key in ``mkdocs.yml``.
"""

from __future__ import annotations

import os
import posixpath

# Raw Markdown of every page, keyed by source URI, collected during the run.
_raw: dict[str, str] = {}
# The rendered navigation, captured so llms.txt mirrors the site's own order.
_nav = None


def on_pre_build(*, config) -> None:
    """Reset collected state so ``mkdocs serve`` rebuilds cleanly."""
    _raw.clear()
    global _nav
    _nav = None


def on_page_markdown(markdown, *, page, config, files):
    """Stash the raw Markdown before it is rendered to HTML."""
    _raw[page.file.src_uri] = markdown
    return markdown


def on_nav(nav, *, config, files):
    """Capture the navigation tree for the llms.txt index."""
    global _nav
    _nav = nav
    return nav


def _md_dest(dest_path: str) -> str:
    """``foo/index.html`` -> ``foo/index.md`` (OS-native separators)."""
    root, _ = os.path.splitext(dest_path)
    return root + ".md"


def on_post_page(output, *, page, config):
    """Write the page's raw Markdown next to its rendered HTML."""
    md = _raw.get(page.file.src_uri)
    if md is None:
        return output
    out = os.path.join(config["site_dir"], _md_dest(page.file.dest_path))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(md)
    return output


def _abs(base: str, url: str) -> str:
    """Join the configured ``site_url`` with a page's relative URL."""
    if not base:
        return "/" + url.lstrip("/")
    return base.rstrip("/") + "/" + url.lstrip("/")


def _page_md_url(base: str, page) -> str:
    """Absolute URL of the raw-Markdown sibling of a nav page."""
    return _abs(base, _md_dest(page.file.dest_path).replace(os.sep, "/"))


def _render_index(items, base: str, depth: int, lines: list[str]) -> None:
    """Render a nav level: top entries as headings, pages as bullet links."""
    for item in items:
        if item.is_section:
            if item.title:
                lines.append("")
                lines.append("#" * min(depth + 2, 6) + f" {item.title}")
            if item.children:
                _render_index(item.children, base, depth + 1, lines)
        elif item.is_link:
            if item.title:
                lines.append(f"- [{item.title}]({item.url})")
        elif item.is_page:
            title = item.title or item.file.src_uri
            url = _abs(base, item.url)
            md = _page_md_url(base, item)
            lines.append(f"- [{title}]({url}) ([md]({md}))")
            if item.children:
                _render_index(item.children, base, depth + 1, lines)


def _iter_pages(items):
    """Yield every nav Page in navigation order, descending into sections."""
    for item in items:
        if item.is_page:
            yield item
        children = getattr(item, "children", None)
        if children:
            yield from _iter_pages(children)


def on_post_build(*, config) -> None:
    """Emit llms.txt and llms-full.txt once the whole site is built."""
    if _nav is None:
        return
    base = config.get("site_url") or ""
    site_dir = config["site_dir"]
    name = config.get("site_name", "Documentation")
    description = config.get("site_description", "")

    index = [f"# {name}"]
    if description:
        index += ["", f"> {description}"]
    _render_index(_nav.items, base, 0, index)
    index.append("")
    with open(os.path.join(site_dir, "llms.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(index))

    corpus: list[str] = [f"# {name}", ""]
    if description:
        corpus += [f"> {description}", ""]
    for page in _iter_pages(_nav.items):
        md = _raw.get(page.file.src_uri)
        if md is None:
            continue
        title = page.title or page.file.src_uri
        url = _abs(base, page.url)
        corpus += [
            "=" * 80,
            f"# {title}",
            f"Source: {url}",
            "",
            md.strip(),
            "",
        ]
    out = os.path.join(site_dir, "llms-full.txt")
    with open(out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(corpus))
