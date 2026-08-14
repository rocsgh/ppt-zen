#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the gallery site (docs/) from the style packs.

Single source of truth = styles/<slug>/STYLE.md. Emits:
  docs/index.html      filterable card gallery; each card links to its detail page
  docs/<slug>.html     one detail page per style (big sample + full description + prompt formula)
  docs/img/<slug>.jpg  each pack's first sample
Run after adding/editing a pack.
"""
import os, re, glob, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "img")


def parse_front(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", s, re.S)
    if not m:
        return {}, ""
    fm, body = m.group(1), m.group(2)
    d, key = {}, None
    for ln in fm.split("\n"):
        if not ln.strip() or ln.strip().startswith("#"):
            continue
        indented = ln.startswith("  ") or ln.startswith("\t")
        mm = re.match(r"^([a-z_]+):\s?(.*)$", ln)
        if mm and not indented:
            key = mm.group(1)
            val = mm.group(2).strip()
            if val in (">", "|"):
                d[key] = ""
            elif key == "samples":
                d["_samples"] = []
            else:
                d[key] = val.strip().strip(chr(34))
        elif key == "samples" and ln.strip().startswith("- "):
            d.setdefault("_samples", []).append(ln.strip()[2:].strip())
        elif indented and key:
            d[key] = (d.get(key, "") + "\n" + ln.strip()).strip()
    if d.get("_samples"):
        d["samples"] = d["_samples"]
    elif d.get("samples"):
        d["samples"] = [d["samples"]]
    return d, body.strip()


def inline_md(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t.replace("\n", " ")


def body_paras(body):
    out = []
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p.startswith("#") or p.startswith("!["):
            continue
        out.append(p)
    return out


def load():
    packs = []
    for style in sorted(glob.glob(os.path.join(ROOT, "styles", "*", "STYLE.md"))):
        pd = os.path.dirname(style)
        slug = os.path.basename(pd)
        if slug == "_template":
            continue
        d, body = parse_front(style)
        d["slug"] = d.get("slug", slug)
        d["_dir"] = pd
        d["_body"] = body
        packs.append(d)
    return packs


CSS = """
:root{--bg:#faf8f4;--fg:#181414;--muted:#6b6460;--card:#fff;--line:#e7e0d6;--accent:#b23b2e;--code:#2a2320}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151210;--fg:#f3efe9;--muted:#9a9088;--card:#1f1b18;--line:#332c26;--accent:#e0654f;--code:#0f0c0a}}
:root[data-theme=dark]{--bg:#151210;--fg:#f3efe9;--muted:#9a9088;--card:#1f1b18;--line:#332c26;--accent:#e0654f;--code:#0f0c0a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}
a{color:inherit}
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
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:block;transition:transform .12s ease,border-color .12s ease}
.card:hover{transform:translateY(-3px);border-color:var(--accent)}
.card img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}
.card .body{padding:14px 16px}
.card .nm{font-weight:700;font-size:1.05rem}
.card .meta{color:var(--muted);font-size:.82rem;margin:4px 0 8px}
.card .tag{display:inline-block;font-size:.7rem;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:1px 8px;margin:0 4px 4px 0}
.card .more{color:var(--accent);font-size:.82rem;font-weight:600;margin-top:6px}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:30px 20px 50px;border-top:1px solid var(--line)}
/* detail */
.top{display:flex;justify-content:space-between;align-items:center;padding:20px 0}
.top a{text-decoration:none;font-weight:600;font-size:.92rem}
.hero{width:100%;border-radius:16px;border:1px solid var(--line);display:block;margin:6px 0 26px}
.d h1{font-size:clamp(1.8rem,4vw,2.6rem);margin:0 0 10px;letter-spacing:-.02em}
.chips{margin:0 0 18px}
.chip{display:inline-block;font-size:.78rem;border:1px solid var(--line);border-radius:99px;padding:3px 11px;margin:0 6px 6px 0;color:var(--muted)}
.chip.k{color:var(--accent);border-color:var(--accent)}
.world{font-style:italic;color:var(--muted);font-size:1.05rem;margin:0 0 20px;padding-left:14px;border-left:3px solid var(--accent)}
.d p{max-width:70ch}
.d h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:34px 0 8px}
pre{background:var(--code);color:#e8e2da;padding:16px;border-radius:10px;overflow:auto;font-size:.8rem;line-height:1.5;white-space:pre-wrap}
code{background:var(--code);color:#e8e2da;padding:1px 5px;border-radius:4px;font-size:.85em}
.src{color:var(--muted);font-size:.86rem;margin-top:22px}
"""

FILTER_JS = """
const btns=document.querySelectorAll('.filters button');
btns.forEach(b=>b.onclick=()=>{btns.forEach(x=>x.classList.remove('on'));b.classList.add('on');
 const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>{c.style.display=(f==='all'||c.dataset.medium===f)?'':'none'});});
"""


def page(title, desc, inner, js=""):
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><meta name="description" content="%s">
<style>%s</style></head><body>%s%s</body></html>""" % (
        html.escape(title), html.escape(desc), CSS, inner,
        ("<script>%s</script>" % js) if js else ""))


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
        name = p.get("name", "")
        medium = p.get("medium", "Other")
        hand = p.get("hand", "").strip()
        tags = re.findall(r"[\w一-鿿-]+", p.get("tags", ""))
        # --- card ---
        tag_html = "".join('<span class="tag">%s</span>' % html.escape(t) for t in tags[:4])
        cards.append(
            ('<a class="card" href="%s.html" data-medium="%s">'
             '<img loading="lazy" src="img/%s" alt="%s"/>'
             '<div class="body"><div class="nm">%s</div>'
             '<div class="meta">%s%s</div>%s'
             '<div class="more">View details &rarr;</div>'
             '</div></a>') % (
                p["slug"], html.escape(medium), dst_name, html.escape(name), html.escape(name),
                html.escape(medium), (" &middot; " + html.escape(hand)) if hand else "", tag_html))
        # --- detail page ---
        chips = ['<span class="chip">%s</span>' % html.escape(medium)]
        if hand:
            chips.append('<span class="chip k">hand: %s</span>' % html.escape(hand))
        chips += ['<span class="chip">%s</span>' % html.escape(t) for t in tags]
        world = p.get("world", "").strip()
        paras = "".join("<p>%s</p>" % inline_md(x) for x in body_paras(p.get("_body", "")))
        formula = html.escape(p.get("prompt_formula", "").strip())
        source = p.get("source", "").strip()
        lic = p.get("license", "CC-BY-4.0")
        inner = ("""<div class="wrap d">
<div class="top"><a href="index.html">&larr; All styles</a><a href="https://github.com/rocsgh/ppt-zen">GitHub &#9733;</a></div>
<img class="hero" src="img/%s" alt="%s"/>
<h1>%s</h1>
<div class="chips">%s</div>
%s%s
<h2>Prompt formula</h2><pre>%s</pre>
%s
<p class="src">License: %s &middot; contributions via DCO. %s</p>
<footer>PPT-Zen &middot; a judgment layer for AI-made slides &middot; <a href="index.html">back to the gallery</a></footer>
</div>""") % (
            dst_name, html.escape(name), html.escape(name), "".join(chips),
            ('<p class="world">%s</p>' % html.escape(world)) if world else "",
            paras,
            formula if formula else "(none)",
            ('<h2>Source</h2><p>%s</p>' % inline_md(source)) if source else "",
            html.escape(lic),
            ("Inspired discipline from <i>Presentation Zen</i>." ))
        open(os.path.join(DOCS, p["slug"] + ".html"), "w", encoding="utf-8").write(
            page(name + " · PPT-Zen", medium + " material recipe for AI-made slides.", inner))

    filt = ['<button class="on" data-f="all">All</button>'] + \
           ['<button data-f="%s">%s</button>' % (html.escape(m), html.escape(m)) for m in mediums]
    inner = ("""<header><div class="wrap"><h1>PPT-Zen</h1>
<p>A judgment layer for AI-made slides &mdash; not another PPT generator. Every style ships one reproducible prompt formula.</p>
<div class="links"><a class="primary" href="https://github.com/rocsgh/ppt-zen">GitHub &#9733;</a>
<a href="https://github.com/rocsgh/ppt-zen#quick-start">Install</a>
<a href="https://github.com/rocsgh/ppt-zen/blob/master/CONTRIBUTING.md">Contribute a style</a></div></div></header>
<div class="wrap"><div class="filters">%s</div><div class="grid">%s</div></div>
<footer>%d styles &middot; auto-generated from the style packs &middot; Apache-2.0 (judgment layer) + CC-BY-4.0 (styles) &middot; Inspired by <i>Presentation Zen</i></footer>""") % (
        "".join(filt), "".join(cards), len(packs))
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(
        page("PPT-Zen · Gallery", "A judgment layer for AI-made slides. Browse styles, each with a reproducible prompt formula.",
             inner, FILTER_JS))
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print("site built: %d cards + %d detail pages, %d mediums" % (len(cards), len(packs), len(mediums)))


if __name__ == "__main__":
    build()
