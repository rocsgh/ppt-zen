#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The dry-run judgment pack, in one command — the no-key path, end to end.

PLAN.md is the deliverable: one stanza per page carrying the judgment (density,
device, verbatim text) plus a complete ready-to-paste image prompt. This script
writes the skeleton and turns a filled-in PLAN.md into placeholder pages and a
draft.pptx you can walk through today. The agent still authors the content; this
only moves the files.

  python3 scripts/judgment_pack.py --init 10 --style portolan   # -> slides/PLAN.md
  python3 scripts/judgment_pack.py slides                       # -> slides/NN-*.jpg + draft.pptx

Resume, never restart: a page whose image already exists is skipped, so you can
drop a real image over a placeholder, run again, and only the rest is rendered.
"""
import argparse, os, re, subprocess, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

HEADER = """# Judgment pack — %(n)d pages
style: %(style)s

One stanza per page, in reading order. `density` is HEADLINE or DETAIL; `device` is
the page's argument drawn as a thing (or `none`); `text` is the verbatim on-slide
copy; `prompt` is the complete image prompt, indented, ready to paste into any image
tool as-is. The `##` line names the file the page renders to (`NN-slug.jpg`) — keep
the number, rename the slug freely.

    python3 %(self)s %(dir)s

renders a placeholder for every page and assembles draft.pptx. Got a real image for a
page? Save it over the placeholder of the same name and run that again — existing
images are left alone.
"""

STANZA = """
## %(name)s
density: HEADLINE
device: <this page's argument, drawn as one thing — or: none>
text: <the exact words to render on this page, verbatim>
prompt: |
  SURFACE:  <the chosen pack's prompt_formula SURFACE, pasted verbatim>
  SKELETON: <auto by page role, or: plain>
  DEVICE:   <the device above, described as an object>
  TEXT:     <the exact words, and where they sit>
  CRITICAL: render ONLY the text above; every letter correct; no invented glyphs; no
            other language; no structure words; text-bearing objects stay blank unless
            TEXT names their words; keep key content clear of top/bottom ~8%%.
"""


def page_name(i, n):
    if i == 1:
        return "01-cover"
    return "%02d-%s" % (i, "close" if i == n else "page")


def init(n, style, out, self_path):
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "PLAN.md")
    if os.path.exists(path):
        sys.exit("%s already exists — move it aside first (this would overwrite your judgment)." % path)
    body = HEADER % {"n": n, "style": style or "<slug from styles.json — one material, whole deck>",
                     "self": self_path, "dir": out}
    body += "".join(STANZA % {"name": page_name(i, n)} for i in range(1, n + 1))
    open(path, "w", encoding="utf-8").write(body)
    print("wrote %s (%d pages)" % (path, n))
    print("fill in every stanza, then: python3 %s %s" % (self_path, out))
    return 0


def parse_plan(path):
    """Stanzas are `## name` + key: value lines + an indented `prompt: |` block."""
    pages, cur, in_prompt = [], None, False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("## "):
            cur = {"name": line[3:].strip(), "density": "", "device": "", "text": "", "prompt": []}
            pages.append(cur)
            in_prompt = False
            continue
        if cur is None:
            continue
        if in_prompt:
            if line.strip() and not line.startswith((" ", "\t")):
                in_prompt = False          # an unindented line ends the prompt block
            else:
                cur["prompt"].append(line)
                continue
        head = line.strip().lower()
        if head.startswith("prompt:"):
            rest = line.split(":", 1)[1].strip()
            in_prompt = True
            if rest and rest != "|":
                cur["prompt"].append(rest)
        else:
            for k in ("density", "device", "text"):
                if head.startswith(k + ":"):
                    cur[k] = line.split(":", 1)[1].strip()
                    break
    for p in pages:
        p["prompt"] = textwrap.dedent("\n".join(p["prompt"])).strip()
    return pages


def image_name(i, name):
    return (name if re.match(r"^\d+-", name) else
            "%02d-%s" % (i, re.sub(r"[^\w-]+", "-", name).strip("-").lower() or "page")) + ".jpg"


def pack(d, pptx):
    plan = os.path.join(d, "PLAN.md")
    if not os.path.isfile(plan):
        sys.exit("no PLAN.md in %s — write one first: judgment_pack.py --init <N> --out %s" % (d, d))
    pages = parse_plan(plan)
    if not pages:
        sys.exit("%s has no `## <page>` stanzas — see the header of a fresh --init file for the shape." % plan)
    from placeholder_page import render
    made = skipped = 0
    for i, p in enumerate(pages, 1):
        out = os.path.join(d, image_name(i, p["name"]))
        if os.path.exists(out):
            print("page %d/%d — %s already there, keeping it" % (i, len(pages), os.path.basename(out)))
            skipped += 1
            continue
        render(out, "%d/%d" % (i, len(pages)), p["density"], p["device"], p["text"])
        print("page %d/%d — placeholder %s" % (i, len(pages), os.path.basename(out)))
        made += 1
    print("%d placeholder(s) rendered, %d page(s) already had an image" % (made, skipped))
    sys.stdout.flush()   # assemble_pptx.py writes to the same stdout; keep the order readable
    r = subprocess.call([sys.executable, os.path.join(HERE, "assemble_pptx.py"), d, pptx])
    if r:
        return r
    print("prompts to paste into any image tool: %s (one per page, drop results back into %s)" % (plan, d))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Write a PLAN.md skeleton, or turn a filled-in one into placeholders + draft.pptx.",
        epilog="No image endpoint needed: the judgment ships today, the pixels can wait.")
    ap.add_argument("dir", nargs="?", help="directory holding PLAN.md (default mode)")
    ap.add_argument("--init", type=int, metavar="N", help="write a PLAN.md skeleton of N pages instead")
    ap.add_argument("--style", default="", help="style slug to record in the plan header (--init)")
    ap.add_argument("--out", default="slides", help="where PLAN.md goes (--init; default: slides)")
    ap.add_argument("--pptx", default="", help="output deck (default: draft.pptx beside the images dir)")
    a = ap.parse_args()
    self_path = os.path.relpath(os.path.abspath(__file__)) if not os.path.isabs(sys.argv[0]) else __file__
    if a.init is not None:
        if a.init < 1:
            sys.exit("--init needs a page count of 1 or more.")
        return init(a.init, a.style, a.out, self_path)
    if not a.dir:
        ap.error("give a directory containing PLAN.md, or --init N to write one")
    d = a.dir.rstrip(os.sep) or a.dir
    return pack(d, a.pptx or os.path.join(os.path.dirname(os.path.abspath(d)), "draft.pptx"))


if __name__ == "__main__":
    sys.exit(main())
