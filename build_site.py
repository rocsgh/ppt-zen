#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the gallery site (docs/) from the style packs — pt-ui redesign.

Brand layer (PPT-Zen's own, NOT the SoaRank warm-paper/indigo system): "the neutral
gallery" — monochrome ink-on-paper chrome, grotesque display + mono spec-labels, zero
chromatic accent, so the swatch images are the only colour on the page. Signature
element: a hero that proves the thesis (one line -> many worlds) with a three-material trio.

Emits index.html (filterable card wall) + one detail page per style + docs/img/<slug>.jpg.
Single source of truth = styles/<slug>/STYLE.md.
"""
import os, re, glob, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "img")
# three visually-contrasting samples for the hero trio (slugs stay stable across renames)
HERO_TRIO = ["portolan", "cinema-wongkarwai", "swiss-grid"]


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
:root{
 --bg:#f3f2ef; --panel:#fbfbf9; --ink:#17161b; --ink2:#3b3a41; --muted:#78767f;
 --line:#e2e0da; --line2:#d3d0c8; --shadow:20 18 15;
 --disp:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",system-ui,sans-serif;
 --mono:"SF Mono",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;
}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
 --bg:#0e0e11; --panel:#17171b; --ink:#f4f3ef; --ink2:#c9c7cf; --muted:#8f8d97;
 --line:#26262c; --line2:#33333a; --shadow:0 0 0;
}}
:root[data-theme=dark]{
 --bg:#0e0e11; --panel:#17171b; --ink:#f4f3ef; --ink2:#c9c7cf; --muted:#8f8d97;
 --line:#26262c; --line2:#33333a; --shadow:0 0 0;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;color:var(--ink);font:1.0625rem/1.6 var(--disp);
 background:var(--bg);
 background-image:radial-gradient(var(--line) .6px,transparent .6px);
 background-size:24px 24px;background-position:-12px -12px;}
a{color:inherit;text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.kick{font:.72rem/1.4 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}

/* nav */
nav{display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:1px solid var(--line)}
.mark{font-weight:800;letter-spacing:-.03em;font-size:1.15rem}
.mark b{color:var(--ink)}
.nav-links{display:flex;gap:6px;align-items:center}
.btn{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:10px;
 font:600 .9rem var(--disp);border:1px solid var(--line2);color:var(--ink);background:var(--panel)}
.btn.solid{background:var(--ink);color:var(--bg);border-color:var(--ink)}

/* hero */
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;padding:72px 0 40px}
.hero h1{font-size:clamp(2.6rem,6.2vw,4.6rem);line-height:.98;letter-spacing:-.04em;font-weight:800;margin:14px 0 0}
.hero .lede{font-size:1.2rem;line-height:1.5;color:var(--ink2);margin:20px 0 6px;max-width:30ch}
.hero .thesis{font-size:1.05rem;color:var(--muted);margin:0 0 26px}
.hero .thesis b{color:var(--ink);font-weight:700}
.hero-cta{display:flex;gap:10px;flex-wrap:wrap}
.hero-cta .btn{min-height:46px;padding:0 20px}
.trio{position:relative}
.trio .row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.trio figure{margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--line2);
 box-shadow:0 1px 0 rgb(var(--shadow)/.04),0 14px 34px -18px rgb(var(--shadow)/.5)}
.trio img{width:100%;display:block;aspect-ratio:3/4;object-fit:cover}
.trio .cap{margin-top:12px;text-align:center}

/* section head */
.shead{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);
 padding-top:26px;margin-top:26px}
.shead h2{font-size:1.5rem;letter-spacing:-.02em;margin:0}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0 6px}
.filters button{background:transparent;border:1px solid var(--line2);color:var(--ink2);min-height:36px;
 padding:0 13px;border-radius:99px;cursor:pointer;font:.75rem/1 var(--mono);letter-spacing:.04em}
.filters button:hover{border-color:var(--ink)}
.filters button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}

/* card wall */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:22px;padding:22px 0 64px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:block;
 transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s,border-color .18s}
.card .ph{overflow:hidden;aspect-ratio:16/10;background:var(--line)}
.card img{width:100%;height:100%;display:block;object-fit:cover;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.card:hover{transform:translateY(-4px);border-color:var(--line2);
 box-shadow:0 2px 0 rgb(var(--shadow)/.03),0 24px 46px -24px rgb(var(--shadow)/.55)}
.card:hover img{transform:scale(1.035)}
.card .body{padding:15px 17px 17px}
.card .nm{font-weight:700;font-size:1.06rem;letter-spacing:-.01em}
.card .sub{font:.7rem/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:5px 0 10px}
.card .tags{display:flex;flex-wrap:wrap;gap:5px}
.card .tag{font:.66rem/1 var(--mono);letter-spacing:.03em;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:4px 8px}
.card .more{font:.7rem/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink);margin-top:12px}

footer{border-top:1px solid var(--line);padding:34px 0 60px;color:var(--muted);font-size:.86rem;text-align:center}
footer a{color:var(--ink2);text-decoration:underline;text-underline-offset:2px}

/* detail */
.top{display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:1px solid var(--line)}
.top a{font:600 .9rem var(--disp)}
.d{max-width:900px}
.hero-img{width:100%;border-radius:18px;border:1px solid var(--line2);display:block;margin:30px 0 30px;
 box-shadow:0 2px 0 rgb(var(--shadow)/.03),0 30px 60px -30px rgb(var(--shadow)/.5)}
.d h1{font-size:clamp(2rem,4.6vw,3rem);letter-spacing:-.03em;font-weight:800;margin:0 0 12px;line-height:1.02}
.chips{margin:0 0 22px;display:flex;flex-wrap:wrap;gap:7px}
.chip{font:.72rem/1 var(--mono);letter-spacing:.05em;border:1px solid var(--line2);border-radius:99px;padding:6px 11px;color:var(--muted)}
.chip.k{color:var(--bg);background:var(--ink);border-color:var(--ink)}
.world{font-size:1.2rem;line-height:1.45;color:var(--ink2);margin:0 0 24px;padding-left:16px;border-left:3px solid var(--ink)}
.d p{max-width:68ch;color:var(--ink2)}
.d p b{color:var(--ink)}
.d h2{font:.72rem/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:38px 0 10px}
pre{background:#141319;color:#e9e6df;padding:18px;border-radius:12px;overflow:auto;font:.8rem/1.55 var(--mono);white-space:pre-wrap;border:1px solid #24232b}
code{font-family:var(--mono);font-size:.86em}
.src{color:var(--muted);font-size:.86rem;margin-top:24px}

@media(max-width:820px){.hero{grid-template-columns:1fr;gap:30px;padding:44px 0 24px}.trio img{aspect-ratio:16/11}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}.card:hover{transform:none}.card:hover img{transform:none}}
@media(prefers-contrast:more){:root{--muted:#54525a;--line:#c9c6bf;--line2:#b3b0a8}}
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
        html.escape(title), html.escape(desc), CSS, inner, ("<script>%s</script>" % js) if js else ""))


def nav():
    return ("""<div class="wrap"><nav><a class="mark" href="index.html">PPT&#8209;<b>Zen</b></a>
<div class="nav-links"><a class="btn" href="https://github.com/rocsgh/ppt-zen#quick-start">Install</a>
<a class="btn" href="https://github.com/rocsgh/ppt-zen/blob/master/CONTRIBUTING.md">Contribute</a>
<a class="btn solid" href="https://github.com/rocsgh/ppt-zen">GitHub &#9733;</a></div></nav></div>""")


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
        sub = medium + ((" &nbsp;&middot;&nbsp; " + html.escape(hand)) if hand else "")
        tag_html = "".join('<span class="tag">%s</span>' % html.escape(t) for t in tags[:4])
        cards.append(
            ('<a class="card" href="%s.html" data-medium="%s">'
             '<div class="ph"><img loading="lazy" src="img/%s" alt="%s"/></div>'
             '<div class="body"><div class="nm">%s</div><div class="sub">%s</div>'
             '<div class="tags">%s</div><div class="more">View details &rarr;</div>'
             '</div></a>') % (p["slug"], html.escape(medium), dst_name, html.escape(name),
                              html.escape(name), sub, tag_html))
        # detail page
        chips = ['<span class="chip">%s</span>' % html.escape(medium)]
        if hand:
            chips.append('<span class="chip k">hand: %s</span>' % html.escape(hand))
        chips += ['<span class="chip">%s</span>' % html.escape(t) for t in tags]
        world = p.get("world", "").strip()
        paras = "".join("<p>%s</p>" % inline_md(x) for x in body_paras(p.get("_body", "")))
        formula = html.escape(p.get("prompt_formula", "").strip())
        source = p.get("source", "").strip()
        lic = p.get("license", "CC-BY-4.0")
        inner = (nav() + """<div class="wrap d">
<img class="hero-img" src="img/%s" alt="%s"/>
<h1>%s</h1><div class="chips">%s</div>
%s%s
<h2>Prompt formula</h2><pre>%s</pre>%s
<p class="src">License: %s &middot; contributions via DCO &middot; inspired discipline from <i>Presentation Zen</i>.</p>
</div><footer><div class="wrap">PPT-Zen &middot; a judgment layer for AI-made slides &middot; <a href="index.html">&larr; back to the gallery</a></div></footer>""") % (
            dst_name, html.escape(name), html.escape(name), "".join(chips),
            ('<p class="world">%s</p>' % html.escape(world)) if world else "",
            paras, formula if formula else "(none)",
            ('<h2>Source</h2><p>%s</p>' % inline_md(source)) if source else "", html.escape(lic))
        open(os.path.join(DOCS, p["slug"] + ".html"), "w", encoding="utf-8").write(
            page(name + " · PPT-Zen", (medium + " recipe for AI-made slides."), inner))

    # hero trio
    trio = "".join('<figure><img loading="eager" src="img/%s.jpg" alt=""/></figure>' % s
                   for s in HERO_TRIO if os.path.exists(os.path.join(IMG, s + ".jpg")))
    filt = ['<button class="on" data-f="all">All</button>'] + \
           ['<button data-f="%s">%s</button>' % (html.escape(m), html.escape(m)) for m in mediums]
    inner = (nav() + """<div class="wrap"><section class="hero">
<div><div class="kick">Open-source &middot; Apache-2.0 + CC-BY-4.0</div>
<h1>PPT&#8209;Zen</h1>
<p class="lede">A judgment layer for AI-made slides &mdash; not another PPT generator.</p>
<p class="thesis"><b>One sentence in. Many worlds out.</b> Your agent decides how each page should look, then renders it full-image in the material you choose.</p>
<div class="hero-cta"><a class="btn solid" href="https://github.com/rocsgh/ppt-zen">GitHub &#9733;</a>
<a class="btn" href="https://github.com/rocsgh/ppt-zen#quick-start">Quick start</a></div></div>
<div class="trio"><div class="row">%s</div><div class="cap kick">the same idea &mdash; three materials</div></div>
</section>
<div class="shead"><h2>The library</h2><div class="kick">%d styles</div></div>
<div class="filters">%s</div><div class="grid">%s</div></div>
<footer><div class="wrap">%d styles &middot; auto-generated from the style packs &middot; Apache-2.0 (judgment layer) + CC-BY-4.0 (styles) &middot; inspired by <i>Presentation Zen</i></div></footer>""") % (
        trio, len(packs), "".join(filt), "".join(cards), len(packs))
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(
        page("PPT-Zen · Gallery", "A judgment layer for AI-made slides. Browse styles, each with a reproducible prompt formula.",
             inner, FILTER_JS))
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print("site built: %d cards + %d detail pages, %d mediums, trio=%d" % (
        len(cards), len(packs), len(mediums), trio.count("<figure")))


if __name__ == "__main__":
    build()
