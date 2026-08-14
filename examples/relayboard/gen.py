#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce the Relayboard worked example: 10 full-image slides in one material.

Uses your own image model via ../../.env (copy from ../../.env.example first).
The judgment behind each page — headline vs. detail, the device, the rhythm —
is written up in README.md; this file is just that judgment turned into prompts.

  python3 gen.py            # all 10 pages -> slides/
  python3 gen.py 06         # regenerate a single page
"""
import base64, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def load_env():
    cfg = dict(os.environ)
    for name in (os.path.join(HERE, ".env"), os.path.join(HERE, "..", "..", ".env")):
        if os.path.exists(name):
            for ln in open(name, encoding="utf-8"):
                ln = ln.strip()
                if ln and not ln.startswith("#") and "=" in ln:
                    k, v = ln.split("=", 1)
                    cfg.setdefault(k.strip(), v.strip())
    return cfg


# Material — chosen ONCE, identical on every page. This is the deck's identity.
SURFACE = ("Premium keynote film still. Near-black #0e0e12 background, warm off-white type, "
           "ONE coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern "
           "sans-serif typography, minimalist. A single thin line-art device per page (coral/white strokes). "
           "Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.")
TAIL = ("CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text, "
        "no watermark, no logo. All text in clean legible English. Keep labels short and correctly spelled.")

PAGES = [
    ("01-cover", "DEVICE: a single glowing coral signal node with soft concentric rings radiating outward, lower-right. "
     "TEXT: large title 'Relayboard' top-left; below it, smaller 'Async standup that respects deep work.'"),
    ("02-problem", "DEVICE: one clean thin horizontal focus line that shatters/breaks at a single point mid-frame. "
     "TEXT: a single centered line 'Standups interrupt the people doing the work.'"),
    ("03-cost", "DEVICE: a huge coral-and-white number as the hero, with a thin line-art hourglass at the side. "
     "TEXT: enormous '23 min' centered; below it, smaller 'to refocus after a single interruption.'"),
    ("04-product", "DEVICE: a clean minimalist card/tile catching an incoming signal line from the side. "
     "TEXT: large 'The standup comes to you.' left; small 'Relayboard' as a mark top-left."),
    ("05-how", "DEVICE: three simple line-art nodes connected left-to-right by a thin coral line (a 3-step flow). "
     "TEXT: three short labels under the nodes: '1  Post async'  '2  Blockers surface'  '3  Only who's needed syncs'. "
     "A small heading top-left 'How it works'."),
    ("06-traction", "DEVICE: a thin coral line rising steadily from lower-left to upper-right. "
     "TEXT: heading top-left 'Traction'; three numbers along the top: '340 teams', '$28k MRR', '+22% MoM'."),
    ("07-pricing", "DEVICE: three stacked minimalist tiers/blocks ascending in height. "
     "TEXT: heading 'Pricing'; three tier labels: 'Free', 'Team  $6 / seat', 'Scale  $12 / seat'."),
    ("08-competition", "DEVICE: a clean 2x2 quadrant, thin white axes, one coral dot in the top-right cell. "
     "TEXT: axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight' (top); "
     "the coral dot labeled 'Relayboard'. Small heading top-left 'Where we sit'."),
    ("09-roadmap", "DEVICE: a thin horizontal timeline with three small coral milestone dots. "
     "TEXT: heading 'Roadmap'; three milestone labels: 'Now  Async standup', 'Q3  Blocker routing', 'Q4  Integrations'."),
    ("10-ask", "DEVICE: a single thin coral arrow sweeping toward a bright horizon line, right side. "
     "TEXT: large centered-left 'Raising $1.5M to give every team its focus back.'"),
]


def main():
    c = load_env()
    base = c.get("IMAGE_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    key = c.get("IMAGE_API_KEY", "")
    model = c.get("IMAGE_MODEL", "gpt-image-1")
    size = c.get("IMAGE_SIZE", "1536x1024")
    if not key or key.startswith("sk-your-key"):
        sys.exit("Set IMAGE_API_KEY in .env (copy ../../.env.example). PPT-Zen ships no image key.")
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(HERE, "slides"), exist_ok=True)
    for name, spec in PAGES:
        if only and only not in name:
            continue
        prompt = SURFACE + " " + spec + " " + TAIL
        body = json.dumps({"model": model, "prompt": prompt, "size": size, "n": 1}).encode()
        req = urllib.request.Request(base + "/images/generations", data=body,
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=240))
            dd = r["data"][0]
            img = base64.b64decode(dd["b64_json"]) if dd.get("b64_json") else urllib.request.urlopen(dd["url"], timeout=90).read()
            open(os.path.join(HERE, "slides", name + ".jpg"), "wb").write(img)
            print(name, "OK")
        except Exception as e:
            print(name, "FAIL", type(e).__name__, str(e)[:160])


if __name__ == "__main__":
    main()
