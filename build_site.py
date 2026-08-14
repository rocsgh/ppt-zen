#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the GitHub Pages preview site (docs/) from the style packs.

Single source of truth = styles/<slug>/STYLE.md. Run after adding/editing a pack.
Copies each pack's first sample into docs/img/ and emits a self-contained,
filterable gallery at docs/index.html.
"""
import os, re, glob, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "img")


def parse_front(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", s, re.S)
    if not m:
        return {}
    fm, d, key = m.group(1), {}, None
    for ln in fm.split("\n"):
        if ln.strip().startswith("#") or not ln.strip():
            continue
        mm = re.match(r"^([a-z_]+):\s?(.*)$", ln)
        if mm:
            key = mm.group(1)
            d[key] = mm.group(2).strip().strip(chr(34))
        elif key == "samples" and ln.strip().startswith("- "):
            d.setdefault("_samples", []).append(ln.strip()[2:].strip())
        elif key == "prompt_formula" and (ln.startswith("  ") or ln.startswith("\t")):
            d["prompt_formula"] = (d.get("prompt_formula", "") + "\n" + ln.strip()).strip()
    if "_samples" in d:
        d["samples"] = d["_samples"]
    elif d.get("samples"):
        d["samples"] = [d["samples"]]
    return d


def load():
    packs = []
    for style in sorted(glob.glob(os.path.join(ROOT, "styles", "*", "STYLE.md"))):
        pd = os.path.dirname(style)
        slug = os.path.basename(pd)
        if slug == "_template":
            continue
        d = parse_front(style)
        d["slug"] = d.get("slug", slug)
        d["_dir"] = pd
        packs.append(d)
    return packs


CSS = """
:root{--bg:#faf8f4;--fg:#181414;--muted:#6b6460;--card:#fff;--line:#e7e0d6;--accent:#b23b2e;--code:#2a2320}
:root[data-theme=dark],:root:not([data-theme=light]) @media(prefers-color-scheme:dark){}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151210;--fg:#f3efe9;--muted:#9a9088;--card:#1f1b18;--line:#332c26;--accent:#e0654f;--code:#0f0c0a}}
:root[data-theme=dark]{--bg:#151210;--fg:#f3efe9;--muted:#9a9088;--card:#1f1b18;--line:#332c26;--accent:#e0654f;--code:#0f0c0a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header{text-align:center;padding:56px 20px 24px}
header h1{font-size:clamp(2rem,5vw,3.2rem);margin:0 0 8px;letter-spacing:-.02em}
header p{color:var(--muted);font-size:1.1rem;margin:0 auto;max-width:640px}
.links{margin-top:18px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.links a{color:var(--fg);text-decoration:none;border:1px solid var(--line);padding:8px 16px;border-radius:99px;font-size:.9rem;font-weight:600}
.links a.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.filters{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:28px 0 8px}
.filters button{background:var(--card);border:1px solid var(--line);color:var(--fg);padding:6px 14px;border-radius:99px;cursor:pointer;font-size:.86rem}
.filters button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;padding:24px 0 60px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.card img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}
.card .body{padding:14px 16px}
.card .nm{font-weight:700;font-size:1.05rem}
.card .meta{color:var(--muted);font-size:.82rem;margin:4px 0 8px}
.card .tag{display:inline-block;font-size:.7rem;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:1px 8px;margin:0 4px 4px 0}
.card details{margin-top:8px}
.card summary{cursor:pointer;color:var(--accent);font-size:.85rem;font-weight:600}
.card pre{background:var(--code);color:#e8e2da;padding:12px;border-radius:8px;overflow:auto;font-size:.74rem;line-height:1.45;white-space:pre-wrap;margin-top:8px}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:30px 20px 50px;border-top:1px solid var(--line)}
"""

JS = """
const btns=document.querySelectorAll('.filters button');
btns.forEach(b=>b.onclick=()=>{btns.forEach(x=>x.classList.remove('on'));b.classList.add('on');
 const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>{c.style.display=(f==='all'||c.dataset.medium===f)?'':'none'});});
"""


def build():
    packs = load()
    os.makedirs(IMG, exist_ok=True)
    mediums = sorted(set(p.get("medium", "Other") for p in packs))
    cards = []
    for p in packs:
        samp = (p.get("samples") or ["samples/01.jpg"])[0]
        src = os.path.join(p["_dir"], samp)
        dst_name = p["slug"] + ".jpg"
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(IMG, dst_name))
        tags = "".join('<span class="tag">%s</span>' % html.escape(t) for t in
                       re.findall(r"[\w一-鿿-]+", p.get("tags", "")))
        hand = (" · " + html.escape(p["hand"])) if p.get("hand") else ""
        formula = html.escape(p.get("prompt_formula", "").strip())
        cards.append(
            ('<div class="card" data-medium="%s">'
             '<img loading="lazy" src="img/%s" alt="%s"/>'
             '<div class="body"><div class="nm">%s%s</div>'
             '<div class="meta">%s</div>%s'
             '<details><summary>Prompt formula</summary><pre>%s</pre></details>'
             '</div></div>') % (
                html.escape(p.get("medium", "Other")), dst_name, html.escape(p.get("name", "")),
                html.escape(p.get("name", "")), hand, html.escape(p.get("medium", "")), tags, formula))
    filt = ['<button class="on" data-f="all">All</button>'] + \
           ['<button data-f="%s">%s</button>' % (html.escape(m), html.escape(m)) for m in mediums]
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PPT-Zen · Gallery</title>
<meta name="description" content="A judgment layer for AI-made slides. Browse styles, each with a reproducible prompt formula.">
<style>%s</style></head><body>
<header><div class="wrap"><h1>PPT-Zen</h1>
<p>A judgment layer for AI-made slides — not another PPT generator. Every style ships one reproducible prompt formula.</p>
<div class="links"><a class="primary" href="https://github.com/rocsgh/ppt-zen">GitHub ★</a>
<a href="https://github.com/rocsgh/ppt-zen#install">Install</a>
<a href="https://github.com/rocsgh/ppt-zen/blob/master/CONTRIBUTING.md">Contribute a style</a></div></div></header>
<div class="wrap"><div class="filters">%s</div>
<div class="grid">%s</div></div>
<footer>Auto-generated from the style packs · Apache-2.0 (judgment layer) + CC-BY-4.0 (styles) · Inspired by <i>Presentation Zen</i></footer>
<script>%s</script></body></html>""" % (CSS, "".join(filt), "".join(cards), JS)
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print("site built: %d cards, %d mediums" % (len(cards), len(mediums)))


if __name__ == "__main__":
    build()
