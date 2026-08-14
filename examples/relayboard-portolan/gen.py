#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce the Relayboard worked example, Portolan sea-chart edition.
Uses your own image model via ../../.env (copy from ../../.env.example).

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

SURFACE = ("16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine ink "
           "coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO photographic "
           "look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE red accent (a "
           "destination dot / a route) used sparingly. Full-bleed 16:9, generous open parchment.")
TAIL = ("CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented "
        "text or place names, no watermark. All text in clean correct English; decorative marks only "
        "as compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom edges.")

PAGES = [
    ("01-cover", "DEVICE: a small fleet of sailing ships departing lower-left along a curved route toward a red "
     "destination dot upper-right; a compass rose lower-right. "
     "TEXT: large title 'Relayboard' upper-left; beneath it smaller 'Async standup that respects deep work.'"),
    ("02-problem", "DEVICE: one long inked voyage route across open sea that SNAPS mid-frame — broken at a single "
     "point, the two ends drifting apart. "
     "TEXT: a single centered line 'Standups interrupt the people doing the work.'"),
    ("03-cost", "DEVICE: an enormous '23 min' lettered in dark ink as the hero, with a pair of navigator's dividers "
     "(compass tool) measuring a distance beside it. "
     "TEXT: enormous '23 min'; below it, smaller 'to refocus after a single interruption.'"),
    ("04-product", "DEVICE: a small courier boat drawing alongside a large anchored ship, a dotted line connecting "
     "them. TEXT: large 'The standup comes to you.' left; small 'Relayboard' as an ink mark top-left."),
    ("05-how", "DEVICE: three small inked islands connected left-to-right by a dotted sailing route. "
     "TEXT: heading top-left 'How it works'; three short labels under the islands: '1  Post async'  "
     "'2  Blockers surface'  '3  Only who's needed syncs'."),
    ("06-traction", "DEVICE: a rising sea-lane climbing from lower-left to upper-right drawn as a fleet of small "
     "ships ascending a curved route. TEXT: heading top-left 'Traction'; three ink annotations along the top: "
     "'340 teams', '$28k MRR', '+22% MoM'."),
    ("07-pricing", "DEVICE: three sailing ships of ascending size in a row (small sloop, mid galleon, grand galleon). "
     "TEXT: heading 'Pricing'; labels under the ships: 'Free', 'Team  $6 / seat', 'Scale  $12 / seat'."),
    ("08-competition", "DEVICE: a clean 2x2 chart quadrant inked on the parchment, thin lines, one red dot in the "
     "top-right cell. TEXT: axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight' "
     "(top); the red dot labeled 'Relayboard'. Small heading top-left 'Where we sit'."),
    ("09-roadmap", "DEVICE: a coastline with a dotted route passing three small harbors, each marked with a tiny "
     "flag. TEXT: heading 'Roadmap'; three harbor labels: 'Now  Async standup', 'Q3  Blocker routing', "
     "'Q4  Integrations'."),
    ("10-ask", "DEVICE: one bold red route arrow sweeping toward a sunrise horizon at the chart's edge, a lone ship "
     "on it. TEXT: large 'Raising $1.5M to give every team its focus back.'"),
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
