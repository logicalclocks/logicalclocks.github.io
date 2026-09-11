"""Crop a viewport screenshot to a rectangle measured in the page.

Usage:
    capture_crop.py <viewport.png> <out.png> '<rect json>' [--margin F] [--top-min Y]

The rect is the JSON an `agent-browser eval` returns from getBoundingClientRect
plus the viewport width: {"x", "y", "w", "h", "iw"}. The device scale is
derived from the screenshot width divided by "iw", so any viewport works.
--margin is a fraction of the rectangle added on every side (0.03 for a card,
0.18 for a modal). --top-min clamps the crop's top edge in css pixels, used to
keep a sticky header out of the shot.
"""

import argparse
import json

from PIL import Image


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("rect")
    ap.add_argument("--margin", type=float, default=0.0)
    ap.add_argument("--top-min", type=float, default=None)
    a = ap.parse_args()
    rect = json.loads(a.rect)
    im = Image.open(a.src)
    dpr = im.width / rect["iw"]
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
    mx, my = w * a.margin, h * a.margin
    x0, y0, x1, y1 = x - mx, y - my, x + w + mx, y + h + my
    if a.top_min is not None:
        y0 = max(y0, a.top_min)
    box = tuple(round(v * dpr) for v in (max(0, x0), max(0, y0), x1, y1))
    box = (box[0], box[1], min(im.width, box[2]), min(im.height, box[3]))
    im.crop(box).save(a.out)
    print(a.out, Image.open(a.out).size)


if __name__ == "__main__":
    main()
