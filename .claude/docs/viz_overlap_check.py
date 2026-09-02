#!/usr/bin/env python3
"""Detect layout-mechanic violations in hops-viz diagram fragments.

The viz kit is monospaced and grid-drawn, so its rules are computable, not a
matter of eyeballing. For every fragment this checks:
    - text stays inside the viewBox (with a margin);
    - text inside a box rect fits that rect (with pad);
    - M1 earned approach: an edge's straight run-in to its arrowhead is at least
      RUN_IN; a curved approach is earned by definition and exempt;
    - M2 force field: no two separate, unconnected block borders sit closer than
      CLEAR; nested, contained, and edge-connected blocks are exempt;
    - M3 arrowhead cap: no arrow marker renders larger than 9x9 userspace units;
    - M4 anchored arrows: every edge that ends in an arrow (marker-end) also
      starts on a node (marker-start knob).
Distances follow the 8-unit spacing grid, not the arrowhead: the marker owns its
pixels, the grid owns spacing, so a future marker tweak never re-litigates
layout. Over-estimates text width so it never gives a false all-clear.
See design-system.md "Edge and layout mechanics" for the rationale.
"""

from __future__ import annotations

import glob
import html
import math
import re
import sys

CLEAR = 24.0  # M2 force field: min border-to-border gap = 3 grid units
RUN_IN = 16.0  # M1 earned approach: min straight run-in to an arrowhead = 2 units
DOCK_EPS = 4.0  # how close an edge endpoint must sit to a block to count as docked
ARROW_MAX = 9.0  # M3: max arrow marker side in userspace units (75% of the old 12)

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
CELL_PAD = 4    # inside a kv row cell (hairline inset, authored at 6)
MARGIN = 2      # min clearance text-to-viewBox edge

# lookbehind so a short name can't match inside a longer one: `d` must not match
# the `d="` inside `id="`, nor `x` the `x="` inside `data-to-x="`.
ATTR = lambda s, a: (re.search(rf'(?<![\w-]){a}="([^"]*)"', s) or [None, None])[1]

NUM = re.compile(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", re.I)
CURVE = {"C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}  # arg count per curve command


def path_geom(d: str):
    """Walk an SVG path `d`. Return (start, end, run_in_len, ends_curved).

    start/end are absolute points; run_in_len is the length of the terminal
    segment (the run into marker-end); ends_curved is True when that terminal
    segment is a Bezier/arc, which counts as an earned approach. None if empty.
    """
    cx = cy = 0.0
    sx = sy = 0.0  # current subpath start, for Z
    start = prev = None
    curved = False
    for letter, argstr in re.findall(r"([A-Za-z])([^A-Za-z]*)", d):
        u, rel = letter.upper(), letter.islower()
        nums = [float(n) for n in NUM.findall(argstr)]
        if u == "M":
            for j in range(0, len(nums) - 1, 2):
                nx, ny = nums[j], nums[j + 1]
                if rel and start is not None:
                    nx += cx
                    ny += cy
                prev = (cx, cy) if start is not None else None
                cx, cy, curved = nx, ny, False  # moveto + implicit L are straight
                if start is None:
                    start = (cx, cy)
                    sx, sy = cx, cy
        elif u == "L":
            for j in range(0, len(nums) - 1, 2):
                nx, ny = nums[j], nums[j + 1]
                if rel:
                    nx += cx
                    ny += cy
                prev, (cx, cy), curved = (cx, cy), (nx, ny), False
        elif u == "H":
            for n in nums:
                prev, cx, curved = (cx, cy), (n + cx if rel else n), False
        elif u == "V":
            for n in nums:
                prev, cy, curved = (cx, cy), (n + cy if rel else n), False
        elif u in CURVE:
            step = CURVE[u]
            for j in range(0, len(nums) - step + 1, step):
                nx, ny = nums[j + step - 2], nums[j + step - 1]
                if rel:
                    nx += cx
                    ny += cy
                prev, (cx, cy), curved = (cx, cy), (nx, ny), True
        elif u == "Z":
            prev, (cx, cy), curved = (cx, cy), (sx, sy), False
    if start is None or prev is None:
        return None
    return start, (cx, cy), math.hypot(cx - prev[0], cy - prev[1]), curved


def near_rect(p, rect) -> bool:
    """True if point p sits within DOCK_EPS of rect (0 distance when inside)."""
    x, y = p
    x0, y0, x1, y1 = rect
    dx = max(x0 - x, x - x1, 0.0)
    dy = max(y0 - y, y - y1, 0.0)
    return math.hypot(dx, dy) <= DOCK_EPS


def id_rects(src: str) -> dict:
    """Map each element id to its bounding rect (x0,y0,x1,y1).

    An id sits on a <rect> directly or on a <g> wrapping one; either way the
    geometry is the first rect. Lets scene edges (data-from/data-to, drawn by
    hops-viz.js with no `d`) resolve to real endpoints so the connected-pair
    exemption sees them instead of flagging two joined boxes as crowding.
    """
    out = {}
    for m in re.finditer(r'<(g|rect)\b([^>]*)\bid="([\w-]+)"([^>]*)>', src):
        idv, attrs = m.group(3), m.group(2) + m.group(4)
        r = attrs
        if m.group(1) == "g":
            rm = re.search(r"<rect\b([^>]*)>", src[m.end():m.end() + 800])
            if not rm:
                continue
            r = rm.group(1)
        x, y, w, h = (ATTR(r, k) for k in ("x", "y", "width", "height"))
        if None not in (x, y, w, h):
            out[idv] = (float(x), float(y), float(x) + float(w), float(y) + float(h))
    return out


def dock(rect, side: str, xo=None, yo=None):
    """Point where an edge docks on a rect's named side (with optional x/y override)."""
    x0, y0, x1, y1 = rect
    cx = float(xo) if xo is not None else (x0 + x1) / 2
    cy = float(yo) if yo is not None else (y0 + y1) / 2
    return {"top": (cx, y0), "bottom": (cx, y1),
            "left": (x0, cy), "right": (x1, cy)}.get(side, (cx, cy))


def cls(tag: str) -> list[str]:
    c = ATTR(tag, "class") or ""
    return c.split()


TITLE_CLS = {"viz-node-title", "viz-kv-title", "viz-label", "viz-colhead", "viz-pill-text"}


def text_width(content: str, classes: list[str], safe: bool = True) -> float:
    """Glyph run width. `safe` uses the 0.72 over-estimate (a title inside its
    node must never be close); measured (0.68 bold tracked titles, 0.6 plain)
    is for texts authored flat against a frame edge, where 0.72 only re-litigates
    figures that render fine."""
    fs = next((SIZE[c] for c in classes if c in SIZE), DEFAULT_SIZE)
    adv = ADVANCE if safe else (0.68 if TITLE_CLS & set(classes) else 0.6)
    return len(content) * fs * adv


def check(path: str) -> list[str]:
    src = open(path, encoding="utf-8").read()
    vb = ATTR(src, "viewBox")
    if not vb:
        return []
    _, _, vw, vh = (float(x) for x in vb.split())
    problems: list[str] = []

    # A scene's `text` op rewrites a <text> at play time ("–" becomes "+1 204
    # rows"); the static content is the short placeholder, so measure the longest
    # value the scene will ever write instead. Substitute before every pass.
    scene = re.search(r'<script[^>]*data-viz-scene[^>]*>(.*?)</script>', src, re.S)
    if scene:
        longest: dict[str, str] = {}
        for sid, val in re.findall(r'"#([\w-]+)":\s*\{[^{}]*?"text":\s*"((?:[^"\\]|\\.)*)"', scene.group(1)):
            if len(val) > len(longest.get(sid, "")):
                longest[sid] = val
        for sid, val in longest.items():
            src = re.sub(rf'(<text\b[^>]*\bid="{sid}"[^>]*>)(.*?)(</text>)', lambda m: m.group(1) + val + m.group(3), src, count=1, flags=re.S)

    def geom(attrs: str, raw: str, safe: bool = True):
        content = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if not content:
            return None
        if "transform=" in attrs:
            return None  # rotated/translated text: flat model can't reason, verify in browser
        x = float(ATTR(attrs, "x") or 0)
        y = float(ATTR(attrs, "y") or 0)
        w = text_width(content, cls(attrs), safe)
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
             float(ATTR(r, "width") or 0), float(ATTR(r, "height") or 0),
             "viz-kv-cell" in cls(r))  # a row cell: hairline inset, measured width
            for r in re.findall(r"<rect\b[^>]*/?>", grp)
            if {"viz-node", "viz-kv-frame", "viz-code-box", "viz-kv-cell"} & set(cls(r))
        ]
        if not rects:
            continue
        for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", grp, re.S):
            for rx, ry, rw, rh, cell in rects:
                g = geom(m.group(1), m.group(2), safe=not cell)
                if not g:
                    break
                content, y, left, right = g
                pad = CELL_PAD if cell else PAD
                if ry <= y <= ry + rh + 4:  # text belongs to this box vertically
                    if left < rx + pad or right > rx + rw - pad:
                        problems.append(f"  box overflow: '{content[:42]}' [{left:.0f}..{right:.0f}] vs box [{rx+pad:.0f}..{rx+rw-pad:.0f}]")

    # pass 2b: a top-level text (not wrapped with its box) whose anchor point
    # sits inside a block still has to fit that block. Header titles, metas and
    # footnotes are usually authored flat next to the frame, not inside a <g>.
    flat_rects = [
        (float(ATTR(r, "x") or 0), float(ATTR(r, "y") or 0),
         float(ATTR(r, "width") or 0), float(ATTR(r, "height") or 0))
        for r in re.findall(r"<rect\b[^>]*/?>", src)
        if {"viz-node", "viz-kv-frame", "viz-code-box"} & set(cls(r))
    ]
    grouped = [m.span() for m in re.finditer(r"<g\b[^>]*>.*?</g>", src, re.S)]
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", src, re.S):
        if in_moved(m.start()) or any(s0 <= m.start() < e0 for s0, e0 in grouped):
            continue
        g = geom(m.group(1), m.group(2), safe=False)
        if not g:
            continue
        content, y, left, right = g
        x = float(ATTR(m.group(1), "x") or 0)
        for rx, ry, rw, rh in flat_rects:
            if rx < x < rx + rw and ry < y <= ry + rh:
                if left < rx + PAD or right > rx + rw - PAD:
                    problems.append(f"  box overflow: '{content[:42]}' [{left:.0f}..{right:.0f}] vs box [{rx+PAD:.0f}..{rx+rw-PAD:.0f}]")
                break

    # pass 2c: a header-band title sits on the band's vertical centre. The band
    # path is `M x y+6 a6.. h.. a6.. v(h)`, so the band is h+6 tall from y; the
    # title baseline lands at y + band/2 + 6 (optical centre for a 13px cap),
    # and a right-aligned meta in the same band shares that baseline.
    for m in re.finditer(r'<path class="viz-kv-header" d="M[\d.]+ ([\d.]+)\s+a6 6 0 0 1 6 -6\s+h[\d.]+\s+a6 6 0 0 1 6 6\s+v(\d+)', src):
        top = float(m.group(1)) - 6
        band = float(m.group(2)) + 6
        want = top + band / 2 + 6
        nxt = src.find('<path class="viz-kv-header"', m.end())
        blk = src[m.end(): nxt if nxt > 0 else len(src)]
        t = re.search(r'<text class="viz-kv-title"[^>]*\by="([\d.]+)"[^>]*>(.*?)</text>', blk, re.S)
        if t and abs(float(t.group(1)) - want) > 2:
            problems.append(f"  band title off-centre: '{t.group(2)[:32]}' baseline {float(t.group(1)):.0f}, want {want:.0f} (band {band:.0f} from {top:.0f})")
        # an icon in the band is centred on the title's cap centre (baseline - 4.7
        # for a 13px cap); a 24-grid icon's centre is translate.y + 12 * scale.
        if t:
            cap = float(t.group(1)) - 4.7
            for ic in re.finditer(r'<g class="viz-icon" transform="translate\(([\d.]+),\s*([\d.]+)\) scale\(([\d.]+)\)"', blk[:t.start()]):
                cy = float(ic.group(2)) + 12 * float(ic.group(3))
                if abs(cy - cap) > 2:
                    problems.append(f"  band icon off-centre: centre {cy:.0f} vs title cap centre {cap:.0f} (translate y {float(ic.group(2)):g}, want {cap - 12 * float(ic.group(3)):.0f})")

    # pass 3: no two texts overlap each other. A title colliding with a
    # right-aligned meta, or a subtitle riding into a header band, is a text-vs-
    # text overlap the box passes never see. Each glyph box is [left,right] x
    # [y-0.8fs, y+0.2fs]; two overlapping by more than OVL in both axes collide.
    # Measured advance, not the overflow pass's safe over-estimate (0.72), so
    # width here reflects real rendering. Per class: bold, uppercase, tracked
    # titles run ~0.68/char; plain fields ~0.6. One ratio would either miss a
    # title collision or false-flag two close fields.
    OVL = 4.0
    texts = []
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", src, re.S):
        if in_moved(m.start()):
            continue
        attrs, raw = m.group(1), m.group(2)
        if "transform=" in attrs:
            continue
        if re.search(r"opacity:\s*0\b", attrs):
            continue  # animation-hidden: a scene reveals it; swap pairs share a spot
        content = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if not content:
            continue
        x = float(ATTR(attrs, "x") or 0)
        y = float(ATTR(attrs, "y") or 0)
        classes = cls(attrs)
        fs = next((SIZE[c] for c in classes if c in SIZE), DEFAULT_SIZE)
        adv = 0.68 if TITLE_CLS & set(classes) else 0.6
        w = len(content) * fs * adv
        anchor = ATTR(attrs, "text-anchor") or "start"
        left = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        texts.append((content, left, left + w, y - 0.8 * fs, y + 0.2 * fs))
    for i in range(len(texts)):
        ci, l1, r1, t1, b1 = texts[i]
        for j in range(i + 1, len(texts)):
            cj, l2, r2, t2, b2 = texts[j]
            if min(r1, r2) - max(l1, l2) > OVL and min(b1, b2) - max(t1, t2) > OVL:
                problems.append(f"  text collision: '{ci[:24]}' overlaps '{cj[:24]}'")

    # M3: arrowheads render at 75% of the old head. No arrow marker may exceed
    # ARROW_MAX on either side (knobs, id ~ '-knob', are exempt).
    for mk in re.finditer(r"<marker\b([^>]*)>", src):
        a = mk.group(1)
        mid = ATTR(a, "id") or ""
        if "arrow" not in mid:
            continue
        mw = float(ATTR(a, "markerWidth") or 0)
        mh = float(ATTR(a, "markerHeight") or 0)
        if mw > ARROW_MAX or mh > ARROW_MAX:
            problems.append(f"  M3 arrowhead too large: #{mid} is {mw:.0f}x{mh:.0f}, max {ARROW_MAX:.0f} each side")

    # collect every edge once, with its endpoints and terminal run, for M1/M4
    # and the M2 exemption. Endpoints let us tell an edge-connected block pair
    # (governed by M1) apart from two crowded, unrelated blocks (governed by M2).
    edges = []  # (tag, start, end, run_in, curved)
    boxes_by_id = id_rects(src)
    for e in re.finditer(r"<(?:path|line)\b[^>]*?class=\"[^\"]*viz-edge[^\"]*\"[^>]*?>", src):
        tag = e.group(0)
        d = ATTR(tag, "d")
        df, dt = ATTR(tag, "data-from"), ATTR(tag, "data-to")
        if d:
            g = path_geom(d)
        elif df in boxes_by_id and dt in boxes_by_id:  # scene edge, drawn by JS
            s = dock(boxes_by_id[df], ATTR(tag, "data-from-side"), ATTR(tag, "data-from-x"))
            en = dock(boxes_by_id[dt], ATTR(tag, "data-to-side"), ATTR(tag, "data-to-x"))
            g = (s, en, math.inf, True)  # JS routes it: run-in not measurable, skip M1
        else:  # a <line> edge
            pts = [ATTR(tag, k) for k in ("x1", "y1", "x2", "y2")]
            if None in pts:
                continue
            x1, y1, x2, y2 = (float(v) for v in pts)
            g = ((x1, y1), (x2, y2), math.hypot(x2 - x1, y2 - y1), False)
        if g:
            edges.append((tag, *g))

    # the blocks every mechanic reasons about: compute once, before M1/M4/M2.
    BLOCK = {"viz-node", "viz-kv-frame", "viz-zone", "viz-code-box"}
    blocks = []
    for r in re.finditer(r"<rect\b([^>]*)>", src):
        if in_moved(r.start()):
            continue  # translated group: real position differs, verify in browser
        a = r.group(1)
        if not (BLOCK & set(cls(a))):
            continue
        x = float(ATTR(a, "x") or 0)
        y = float(ATTR(a, "y") or 0)
        w = float(ATTR(a, "width") or 0)
        h = float(ATTR(a, "height") or 0)
        blocks.append((x, y, x + w, y + h))

    def docks(pt) -> bool:
        return pt is not None and any(near_rect(pt, b) for b in blocks)

    # M1: an arrow's straight run-in must be at least RUN_IN. A curved approach
    # is earned; a straight stub too short to let the head breathe is not.
    for tag, _s, end, run_in, curved in edges:
        if "marker-end=" not in tag or curved:
            continue
        if run_in < RUN_IN:
            problems.append(f"  M1 cramped approach: arrow into [{end[0]:.0f},{end[1]:.0f}] has {run_in:.0f}u straight run-in, need {RUN_IN:.0f}")

    # M4: a connector that ends in an arrow must start on a node. "Connector" is
    # the point: the rule is about an edge whose start docks a block but lost its
    # knob. An arrow starting in open space is an axis or a standalone direction
    # arrow, a different species, so it is not an M4 defect.
    for tag, s, _e, _r, _c in edges:
        if "marker-end=" in tag and "marker-start=" not in tag and docks(s):
            where = ATTR(tag, "d") or ATTR(tag, "x1") or "?"
            problems.append(f"  M4 arrow has no source node: edge '{where[:34]}' lacks marker-start knob")

    # Arrow into a pill: a compute node wears a pill straddling its top edge, so
    # an edge docking that top-centre lands the arrowhead on the pill. Dock the
    # edge off to the side of the pill, or move the pill, so the head stays clear.
    pills = []
    for r in re.finditer(r"<rect\b([^>]*)>", src):
        if "viz-pill" in cls(r.group(1)):
            a = r.group(1)
            x, y = float(ATTR(a, "x") or 0), float(ATTR(a, "y") or 0)
            w, h = float(ATTR(a, "width") or 0), float(ATTR(a, "height") or 0)
            pills.append((x, y, x + w, y + h))
    for tag, _s, end, _r, _c in edges:
        if "marker-end=" not in tag:
            continue
        if any(x0 <= end[0] <= x1 and y0 <= end[1] <= y1 for x0, y0, x1, y1 in pills):
            problems.append(f"  arrow into pill: head at [{end[0]:.0f},{end[1]:.0f}] lands on a kind pill")

    # M2: force field. No two SEPARATE block borders sit closer than CLEAR.
    # Exempt: nested/contained blocks (a node in a zone, a code box in a node)
    # and any pair an edge deliberately connects (that gap is the edge's run-in,
    # M1's concern, not crowding).
    def connected(ra, rb) -> bool:
        for _t, s, e, _r, _c in edges:
            if (near_rect(s, ra) and near_rect(e, rb)) or (near_rect(s, rb) and near_rect(e, ra)):
                return True
        return False

    for i in range(len(blocks)):
        ax0, ay0, ax1, ay1 = blocks[i]
        for j in range(i + 1, len(blocks)):
            bx0, by0, bx1, by1 = blocks[j]
            a_in_b = bx0 <= ax0 and by0 <= ay0 and ax1 <= bx1 and ay1 <= by1
            b_in_a = ax0 <= bx0 and ay0 <= by0 and bx1 <= ax1 and by1 <= ay1
            if a_in_b or b_in_a:
                continue  # containment: nesting, not crowding
            dx = max(bx0 - ax1, ax0 - bx1, 0.0)
            dy = max(by0 - ay1, ay0 - by1, 0.0)
            if dx == 0 and dy == 0:
                continue  # intersecting but not nested: a distinct fault, not force-field
            sep = dx if dy == 0 else dy if dx == 0 else math.hypot(dx, dy)
            if sep < CLEAR and not connected(blocks[i], blocks[j]):
                problems.append(f"  M2 force field: blocks at [{ax0:.0f},{ay0:.0f}] and [{bx0:.0f},{by0:.0f}] only {sep:.0f}u apart, need {CLEAR:.0f}")
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
