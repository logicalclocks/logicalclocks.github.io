#!/usr/bin/env python3
"""Detect text overflow in hops-viz diagram fragments.

The viz kit is monospaced, so glyph advance is deterministic: overlap is a
computable property, not a matter of eyeballing. For every <text> this checks
    - it stays inside the viewBox (with a margin), and
    - if it shares a <g> with a box rect, it fits inside that rect (with pad).
Over-estimates width (high advance ratio) so it never gives a false all-clear.
"""

from __future__ import annotations

import glob
import html
import re
import sys

# font-size (px) per text class; conservative monospace advance incl. tracking.
SIZE = {
    "viz-node-title": 13, "viz-kv-title": 13, "viz-label": 13, "viz-colhead": 12,
    "viz-node-subtitle": 11, "viz-meta": 11, "viz-kv-key": 12, "viz-kv-val": 12,
    "viz-field": 12, "viz-field-type": 12, "viz-field-role": 12, "viz-pill-text": 10,
    "viz-code": 11,  # viz-code font-size is hardcoded 11px, not a --viz-type-* token
}
DEFAULT_SIZE = 13
ADVANCE = 0.72  # px per char per px of font-size (measured mono advance ~0.71); over-estimate to stay safe
PAD = 8         # min clearance text-to-box edge
MARGIN = 2      # min clearance text-to-viewBox edge

ATTR = lambda s, a: (re.search(rf'{a}="([^"]*)"', s) or [None, None])[1]


def cls(tag: str) -> list[str]:
    c = ATTR(tag, "class") or ""
    return c.split()


def text_width(content: str, classes: list[str]) -> float:
    fs = next((SIZE[c] for c in classes if c in SIZE), DEFAULT_SIZE)
    return len(content) * fs * ADVANCE


def check(path: str) -> list[str]:
    src = open(path, encoding="utf-8").read()
    vb = ATTR(src, "viewBox")
    if not vb:
        return []
    _, _, vw, vh = (float(x) for x in vb.split())
    problems: list[str] = []

    def geom(attrs: str, raw: str):
        content = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if not content:
            return None
        if "transform=" in attrs:
            return None  # rotated/translated text: flat model can't reason, verify in browser
        x = float(ATTR(attrs, "x") or 0)
        y = float(ATTR(attrs, "y") or 0)
        w = text_width(content, cls(attrs))
        anchor = ATTR(attrs, "text-anchor") or "start"
        left = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        return content, y, left, left + w

    # A translated parent <g> (e.g. an animated packet) moves its text at render
    # time; the flat model reads the local x and mis-measures, so skip any text
    # inside such a group. Verify those in the browser instead.
    moved = [m.span() for m in re.finditer(r"<g\b[^>]*transform=[^>]*>.*?</g>", src, re.S)]

    def in_moved(pos: int) -> bool:
        return any(s <= pos < e for s, e in moved)

    # pass 1: every text stays inside the viewBox (top-level texts included, not
    # just those wrapped in a <g>)
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", src, re.S):
        if in_moved(m.start()):
            continue
        g = geom(m.group(1), m.group(2))
        if not g:
            continue
        content, _, left, right = g
        if left < MARGIN or right > vw - MARGIN:
            problems.append(f"  viewBox overflow: '{content[:42]}' [{left:.0f}..{right:.0f}] vs 0..{vw:.0f}")

    # pass 2: a text inside a <g> also fits any box rect in that group
    for grp in re.findall(r"<g\b[^>]*>.*?</g>", src, re.S):
        rects = [
            (float(ATTR(r, "x") or 0), float(ATTR(r, "y") or 0),
             float(ATTR(r, "width") or 0), float(ATTR(r, "height") or 0))
            for r in re.findall(r"<rect\b[^>]*/?>", grp)
            if {"viz-node", "viz-kv-frame", "viz-code-box"} & set(cls(r))
        ]
        if not rects:
            continue
        for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", grp, re.S):
            g = geom(m.group(1), m.group(2))
            if not g:
                continue
            content, y, left, right = g
            for rx, ry, rw, rh in rects:
                if ry <= y <= ry + rh + 4:  # text belongs to this box vertically
                    if left < rx + PAD or right > rx + rw - PAD:
                        problems.append(f"  box overflow: '{content[:42]}' [{left:.0f}..{right:.0f}] vs box [{rx+PAD:.0f}..{rx+rw-PAD:.0f}]")
    return problems


def main() -> int:
    targets = sys.argv[1:] or glob.glob("diagrams/**/*.html", recursive=True)
    bad = 0
    for p in sorted(targets):
        issues = check(p)
        if issues:
            bad += 1
            print(f"\n{p}")
            print("\n".join(issues))
    print(f"\n{'FAIL' if bad else 'OK'}: {bad} file(s) with overflow, {len(targets)} checked")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
