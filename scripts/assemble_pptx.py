#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble a folder of 16:9 page images into a real .pptx (each image full-bleed).

This is the "how do I turn N generated slides into a deck" step. PPT-Zen decides
and generates the pages; this makes the deliverable.

Usage:
  pip install python-pptx
  python3 scripts/assemble_pptx.py slides/ deck.pptx
"""
import os, sys, glob


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: assemble_pptx.py <images_dir> <out.pptx>")
    src, out = sys.argv[1], sys.argv[2]
    try:
        from pptx import Presentation
        from pptx.util import Inches
    except ImportError:
        sys.exit("Need python-pptx:  pip install python-pptx")
    imgs = sorted(g for ext in ("*.jpg", "*.jpeg", "*.png") for g in glob.glob(os.path.join(src, ext)))
    if not imgs:
        sys.exit("no .jpg/.png images found in " + src)
    prs = Presentation()
    prs.slide_width = Inches(13.333)   # 16:9
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    for p in imgs:
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(out)
    print("wrote %s (%d slides)" % (out, len(imgs)))


if __name__ == "__main__":
    main()
