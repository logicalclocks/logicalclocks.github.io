"""Read-only index over the Hopsworks documentation Markdown tree.

Pure standard library: walks ``docs/**/*.md``, extracts page titles and
heading sections, and builds a small BM25 search index in memory. No network
access and no mutation of the source tree.

Canonical page ids are the path relative to ``docs/`` without the ``.md``
extension, e.g. ``concepts/fs/feature_group/fg_overview``. Section anchors use
python-markdown's default ``toc`` slugify so they match the anchors rendered on
``docs.hopsworks.ai``.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

_FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_WORD = re.compile(r"[a-z0-9]+")
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$", re.MULTILINE)
_H1 = re.compile(r"^#[ \t]+(.*?)[ \t]*#*[ \t]*$", re.MULTILINE)
_HTML_TAG = re.compile(r"<[^>]+>")


def slugify(text: str, sep: str = "-") -> str:
    """Match python-markdown's default toc slugify (ASCII, lowercase)."""
    value = unicodedata.normalize("NFKD", text)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(rf"[\s{re.escape(sep)}]+", sep, value)


def _tokenize(text: str) -> list[str]:
    return _WORD.findall(text.lower())


@dataclass
class Section:
    """A heading and the prose beneath it, down to the next heading."""

    level: int
    title: str
    anchor: str
    body: str


@dataclass
class Page:
    """One documentation page loaded from a Markdown source file."""

    page_id: str
    title: str
    url: str
    markdown: str
    tokens: list[str] = field(default_factory=list)

    def sections(self) -> list[Section]:
        """Split the page into sections keyed by heading anchor."""
        matches = list(_HEADING.finditer(self.markdown))
        out: list[Section] = []
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(self.markdown)
            title = m.group(2).strip()
            out.append(
                Section(
                    level=len(m.group(1)),
                    title=title,
                    anchor=slugify(_HTML_TAG.sub("", title)),
                    body=self.markdown[start:end].strip(),
                )
            )
        return out


def _page_url(base: str, page_id: str) -> str:
    base = (base or "").rstrip("/")
    pretty = page_id[: -len("index")] if page_id.endswith("index") else page_id + "/"
    return f"{base}/{pretty.lstrip('/')}"


def _title_of(markdown: str, page_id: str) -> str:
    m = _H1.search(markdown)
    if m:
        return _HTML_TAG.sub("", m.group(1)).strip()
    return page_id.rsplit("/", 1)[-1].replace("_", " ").replace("-", " ").title()


def _nav_titles(mkdocs_yml: Path) -> dict[str, str]:
    """Map page_id -> human title from the mkdocs nav, if PyYAML is available.

    Soft enhancement: nav titles ("Overview", "Model Registry") read far better
    than titles derived from a filename. Returns an empty map if PyYAML is
    missing or the nav cannot be parsed, and the caller falls back to _title_of.
    """
    try:
        import yaml
    except ImportError:
        return {}

    class _Loader(yaml.SafeLoader):
        pass

    # mkdocs.yml embeds tags like `!!python/name:material...`; ignore them.
    _Loader.add_multi_constructor(
        "tag:yaml.org,2002:python/name:", lambda loader, suffix, node: None
    )
    _Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
    try:
        data = yaml.load(mkdocs_yml.read_text(encoding="utf-8"), Loader=_Loader)
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, dict):
        return {}

    out: dict[str, str] = {}

    def walk(node: object) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for title, value in node.items():
                if isinstance(value, str) and value.endswith(".md"):
                    out[value[:-3]] = title
                else:
                    walk(value)

    walk(data.get("nav", []))
    return out


class DocsIndex:
    """In-memory, read-only index of the documentation pages."""

    def __init__(self, docs_dir: Path, site_url: str = "https://docs.hopsworks.ai/"):
        self.docs_dir = docs_dir
        self.site_url = site_url
        self.pages: dict[str, Page] = {}
        self._df: Counter[str] = Counter()
        self._avg_len = 0.0
        mkdocs_yml = docs_dir.parent / "mkdocs.yml"
        self._nav_titles = _nav_titles(mkdocs_yml) if mkdocs_yml.exists() else {}
        self._load()

    def _load(self) -> None:
        for path in sorted(self.docs_dir.rglob("*.md")):
            rel = path.relative_to(self.docs_dir).as_posix()
            page_id = rel[:-3]  # strip .md
            try:
                raw = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            markdown = _FRONTMATTER.sub("", raw).strip()
            title = self._nav_titles.get(page_id) or _title_of(markdown, page_id)
            tokens = _tokenize(title + " " + markdown)
            self.pages[page_id] = Page(
                page_id=page_id,
                title=title,
                url=_page_url(self.site_url, page_id),
                markdown=markdown,
                tokens=tokens,
            )
        for page in self.pages.values():
            for term in set(page.tokens):
                self._df[term] += 1
        if self.pages:
            self._avg_len = sum(len(p.tokens) for p in self.pages.values()) / len(
                self.pages
            )

    def search(self, query: str, limit: int = 5) -> list[tuple[Page, float, str]]:
        """BM25-rank pages against the query; return (page, score, snippet)."""
        q_terms = _tokenize(query)
        if not q_terms or not self.pages:
            return []
        n = len(self.pages)
        k1, b = 1.5, 0.75
        scored: list[tuple[Page, float]] = []
        for page in self.pages.values():
            tf = Counter(page.tokens)
            dl = len(page.tokens) or 1
            score = 0.0
            for term in q_terms:
                if term not in tf:
                    continue
                df = self._df[term]
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                freq = tf[term]
                denom = freq + k1 * (1 - b + b * dl / self._avg_len)
                score += idf * (freq * (k1 + 1)) / denom
            if score > 0:
                scored.append((page, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            (page, score, self._snippet(page, q_terms))
            for page, score in scored[:limit]
        ]

    def _snippet(self, page: Page, q_terms: list[str], width: int = 240) -> str:
        text = _HTML_TAG.sub("", page.markdown).replace("\n", " ")
        low = text.lower()
        pos = -1
        for term in q_terms:
            pos = low.find(term)
            if pos != -1:
                break
        if pos == -1:
            return text[:width].strip()
        start = max(0, pos - width // 3)
        return ("…" if start else "") + text[start : start + width].strip() + "…"
