"""Assemble a GIF from viewport screenshots of successive UI states.

Usage:
    capture_gif.py <frames dir> <out.gif> <margin fraction> [bottom margin fraction]

The directory holds pairs frame_NN.png (a viewport screenshot) and
rect_NN.json (the card's rectangle in that frame: x, y, w, h, iw, plus a
"state" label; a frame without a state is skipped). Every frame is cropped
around the largest rectangle seen, so the card can move between frames,
halved to 1x and quantised. The first frame holds longer, the last longest.
"""

import glob
import json
import os
import sys

from PIL import Image


def main() -> None:
    d, out, margin = sys.argv[1], sys.argv[2], float(sys.argv[3])
    bottom = float(sys.argv[4]) if len(sys.argv) > 4 else margin
    frames = []
    for rf in sorted(glob.glob(os.path.join(d, "rect_*.json"))):
        with open(rf) as fh:
            r = json.load(fh)
        if not isinstance(r, dict) or r.get("state") is None:
            continue
        p = rf.replace("rect_", "frame_").replace(".json", ".png")
        if os.path.exists(p):
            frames.append((p, r))
    if not frames:
        raise SystemExit("no frame_NN.png / rect_NN.json pairs with a state")
    first = Image.open(frames[0][0])
    dpr = first.width / frames[0][1]["iw"]
    w = max(r["w"] for _, r in frames)
    h = max(r["h"] for _, r in frames)
    mx, my, mb = w * margin, h * margin, h * bottom

    def box(r: dict) -> tuple[int, ...]:
        return tuple(round(v * dpr) for v in (r["x"] - mx, r["y"] - my, r["x"] + w + mx, r["y"] + h + mb))

    imgs = []
    for p, r in frames:
        im = Image.open(p).convert("RGB").crop(box(r))
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
        imgs.append(im.quantize(colors=128, method=Image.Quantize.MEDIANCUT))
    durations = [1500] + [900] * max(0, len(imgs) - 2) + ([2500] if len(imgs) > 1 else [])
    imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=durations, loop=0, optimize=True)
    print(len(imgs), "frames", imgs[0].size, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main()
