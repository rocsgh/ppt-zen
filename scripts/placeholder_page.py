#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render ONE placeholder page for the dry-run fallback (no image endpoint configured).

It is not a slide — it is a page-shaped card carrying the judgment for that page
(number, density, device, title) so the deck's structure can be assembled, reviewed
and presented while the real images are still missing. Hand the matching prompt card
from slides/PLAN.md to any image tool, drop the result over the placeholder, reassemble.

Usage:
  python3 scripts/placeholder_page.py slides/03-evidence.jpg \\
      --page 3/10 --density DETAIL --device "a funnel narrowing to two names" \\
      --title "AI names only two brands"

Needs Pillow (already installed as a python-pptx dependency).
"""
import argparse, sys

W, H = 1600, 900
BG, INK, DIM, RULE = (233, 231, 227), (36, 34, 32), (122, 118, 112), (176, 172, 166)
FONTS = ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
         "C:\\Windows\\Fonts\\arial.ttf")
# CJK-capable fonts, tried first when the text needs them — the Latin list above renders 中文 as tofu.
FONTS_CJK = ("/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc",
             "/System/Library/Fonts/STHeiti Light.ttc",
             "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
             "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
             "C:\\Windows\\Fonts\\msyh.ttc")


def needs_cjk(text):
    return any("\u2e80" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u30ff" or "\uac00" <= ch <= "\ud7af"
               or "\uf900" <= ch <= "\ufaff" or "\uff00" <= ch <= "\uffef" for ch in text)


def font(size, text=""):
    from PIL import ImageFont
    paths = (FONTS_CJK + FONTS) if needs_cjk(text) else FONTS
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)   # Pillow >= 10.1: scalable default
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, f, width):
    """Word-wrap, with a per-character fallback so CJK and unbroken tokens still break."""
    lines, line = [], ""
    for word in text.split() or [text]:
        trial = (line + " " + word).strip()
        if line and draw.textlength(trial, font=f) > width:
            lines.append(line)
            line = word
        else:
            line = trial
        while draw.textlength(line, font=f) > width and len(line) > 1:
            cut = len(line)
            while cut > 1 and draw.textlength(line[:cut], font=f) > width:
                cut -= 1
            lines.append(line[:cut])
            line = line[cut:]
    if line:
        lines.append(line)
    return lines


def main():
    ap = argparse.ArgumentParser(description="Render one PPT-Zen placeholder page.")
    ap.add_argument("out")
    ap.add_argument("--page", default="", help='e.g. "3/10"')
    ap.add_argument("--density", default="", help="HEADLINE or DETAIL")
    ap.add_argument("--device", default="", help="the page's device, one line")
    ap.add_argument("--title", default="", help="the page's verbatim title text")
    a = ap.parse_args()
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("Need Pillow:  pip install pillow   (it also ships with python-pptx)")

    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((48, 48, W - 48, H - 48), outline=RULE, width=2)

    cjk_probe = (a.title or "") + (a.device or "")
    f_small, f_tag = font(30), font(34)
    f_title, f_dev = font(76, cjk_probe), font(38, cjk_probe)
    if a.page:
        d.text((92, 92), "PAGE " + a.page.upper(), font=f_small, fill=DIM)
    if a.density:
        tag = a.density.upper()
        w = d.textlength(tag, font=f_tag)
        d.rectangle((W - 112 - w - 28, 84, W - 112 + 14, 84 + 52), outline=INK, width=2)
        d.text((W - 112 - w - 14, 96), tag, font=f_tag, fill=INK)

    title = a.title or "[ page title goes here ]"
    lines = wrap(d, title, f_title, W - 260)[:4]
    y = H // 2 - (len(lines) * 96) // 2 - 40
    for ln in lines:
        d.text((128, y), ln, font=f_title, fill=INK)
        y += 96
    if a.device:
        y += 26
        d.line((128, y, 228, y), fill=RULE, width=3)
        y += 26
        for ln in wrap(d, "device: " + a.device, f_dev, W - 260)[:2]:
            d.text((128, y), ln, font=f_dev, fill=DIM)
            y += 50

    foot = "PLACEHOLDER — no image model configured. Prompt for this page: slides/PLAN.md"
    d.text((92, H - 128), foot, font=f_small, fill=DIM)
    im.save(a.out, "JPEG", quality=88)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
