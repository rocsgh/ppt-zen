#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the PPT-Zen product site (docs/) from the style packs.

v3 — product-site restructure (site = the pitch, GitHub = the install):
  index.html    home: thesis + interactive material switcher (signature element)
  method.html   the judgment layer, condensed
  example.html  Relayboard proof page (slides + judgment log)
  gallery.html  the 44-style wall (filterable)
  install.html  per-runtime install matrix + image-model wiring + FAQ
  <slug>.html   one detail page per style (URLs unchanged)
  sitemap.xml / robots.txt

Design: "type-specimen book" — locked light (marketing rule), ink-on-paper chrome,
grotesque display + mono spec labels, the specimens are the only colour. One accent
(International-Klein-ish blue) reserved for interaction.
"""
import os, re, glob, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(DOCS, "img")
BASE_URL = "https://pptzen.xyz"
GH = "https://github.com/rocsgh/ppt-zen"

SWITCHER = ["davinci-copperplate", "ink-wash", "stele-rubbing", "cinema-nolan", "kintsugi", "papercraft"]
FEATURED = ["davinci-copperplate", "portolan", "cinema-wongkarwai", "cinema-nolan",
            "cinema-wesanderson", "kintsugi", "stele-rubbing", "swiss-grid"]

RB_PAGES = [  # slide file, role, density, device (portolan edition), text shown
 ("01-cover", "cover", "HEADLINE", "a fleet departing toward a marked destination", "Relayboard — Async standup that respects deep work."),
 ("02-problem", "problem", "HEADLINE", "a voyage route that snaps mid-sea", "Standups interrupt the people doing the work."),
 ("03-cost", "cost", "HEADLINE", "giant numeral + navigator's dividers", "23 min to refocus after a single interruption."),
 ("04-product", "product", "HEADLINE", "a courier boat drawing alongside", "The standup comes to you."),
 ("05-how", "how", "DETAIL", "three islands on one dotted route", "1 Post async · 2 Blockers surface · 3 Only who's needed syncs"),
 ("06-traction", "traction", "DETAIL", "a fleet climbing a rising sea-lane", "340 teams · $28k MRR · +22% MoM"),
 ("07-pricing", "pricing", "DETAIL", "three ships of ascending size", "Free · Team $6/seat · Scale $12/seat"),
 ("08-competition", "competition", "DETAIL", "2×2 chart quadrant, one red dot", "sync↔async · heavy↔lightweight"),
 ("09-roadmap", "roadmap", "DETAIL", "a coastline route, three harbors", "Now · Q3 · Q4"),
 ("10-ask", "ask", "HEADLINE", "one red route to the sunrise", "Raising $1.5M to give every team its focus back."),
]


# ---------------- pack loading (unchanged data layer) ----------------
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
    return [p.strip() for p in re.split(r"\n\s*\n", body)
            if p.strip() and not p.strip().startswith("#") and not p.strip().startswith("![")]


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


# ---------------- design system ----------------
CSS = """
:root{
 --paper:#f7f5f0; --panel:#fdfcfa; --ink:#16151a; --ink2:#3d3b44; --muted:#716e78;
 --line:#e5e2d9; --line2:#d5d2c8; --acc:#2430d8; --codebg:#141319; --codefg:#eae7e0;
 --disp:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",system-ui,sans-serif;
 --mono:"SF Mono",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;color:var(--ink);font:1.0625rem/1.62 var(--disp);background:var(--paper);
 background-image:radial-gradient(var(--line) .6px,transparent .6px);
 background-size:26px 26px;background-position:-13px -13px}
a{color:inherit;text-decoration:none}
img{max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.kick{font:.72rem/1.5 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:11px;
 font:600 .92rem var(--disp);border:1px solid var(--line2);color:var(--ink);background:var(--panel);cursor:pointer;
 transition:border-color .15s,transform .15s}
.btn:hover{border-color:var(--ink)}
.btn:active{transform:scale(.98)}
.btn.solid{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.btn.solid:hover{background:#000}
nav{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-bottom:1px solid var(--line)}
.mark{font-weight:800;letter-spacing:-.03em;font-size:1.18rem}
.navlinks{display:flex;gap:4px;align-items:center;flex-wrap:wrap}
.navlinks a.nl{padding:9px 13px;border-radius:9px;font:600 .92rem var(--disp);color:var(--ink2)}
.navlinks a.nl:hover{color:var(--ink);background:var(--panel)}
.navlinks a.nl.on{color:var(--ink);text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:2px;text-decoration-color:var(--acc)}
#ghbtn small{font:600 .78rem var(--mono);color:inherit;opacity:.75}
.sec{border-top:1px solid var(--line);margin-top:64px;padding-top:22px}
.sec .shead{display:flex;align-items:baseline;gap:14px;margin-bottom:8px}
.sec .num{font:700 .8rem var(--mono);color:var(--acc);letter-spacing:.08em}
.sec h2{font-size:clamp(1.6rem,3.4vw,2.2rem);letter-spacing:-.025em;margin:0;font-weight:800}
.sec .lede{color:var(--ink2);max-width:62ch;margin:6px 0 26px}
footer{border-top:1px solid var(--line);margin-top:80px;padding:36px 0 60px;color:var(--muted);font-size:.88rem}
footer .cols{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
footer a{color:var(--ink2);text-decoration:underline;text-underline-offset:2px}
pre{background:var(--codebg);color:var(--codefg);padding:16px 18px;border-radius:12px;overflow:auto;
 font:.82rem/1.6 var(--mono);border:1px solid #24232b}
code{font-family:var(--mono);font-size:.88em}
p code,li code,td code{background:#ecead g}
/* hero */
.hero{display:grid;grid-template-columns:.92fr 1.08fr;gap:52px;align-items:center;padding:64px 0 8px}
.hero h1{font-size:clamp(2.5rem,5.6vw,4.1rem);line-height:1.0;letter-spacing:-.04em;font-weight:800;margin:14px 0 0}
.hero h1 em{font-style:normal;color:var(--acc)}
.hero .lede{font-size:1.16rem;line-height:1.55;color:var(--ink2);margin:18px 0 24px;max-width:34ch}
.hero-cta{display:flex;gap:10px;flex-wrap:wrap}
.switcher .stage{border-radius:14px;overflow:hidden;border:1px solid var(--line2);background:var(--panel);
 box-shadow:0 2px 0 rgb(20 18 15/.03),0 26px 56px -26px rgb(20 18 15/.5)}
.switcher .stage img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}
.chips button{font:.74rem/1 var(--mono);letter-spacing:.03em;border:1px solid var(--line2);background:var(--panel);
 color:var(--ink2);border-radius:99px;padding:9px 13px;cursor:pointer;min-height:34px;transition:all .15s}
.chips button:hover{border-color:var(--ink);color:var(--ink)}
.chips button.on{background:var(--acc);border-color:var(--acc);color:#fff}
.switcher .cap{margin-top:10px}
/* home bits */
.claims{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:34px 0 0}
.claim{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.claim b{display:block;font-size:1.02rem;margin-bottom:5px}
.claim span{color:var(--muted);font-size:.92rem;line-height:1.5;display:block}
.chain{background:var(--codebg);color:var(--codefg);border-radius:14px;padding:22px 24px;border:1px solid #24232b;
 font:.86rem/1.9 var(--mono);overflow:auto}
.chain .ln{display:block;opacity:0;transform:translateY(4px);transition:opacity .4s,transform .4s}
.chain .ln.show{opacity:1;transform:none}
.chain .c1{color:#8f8d97}.chain .c2{color:#9db4ff}.chain .c3{color:#eae7e0}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.step{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px}
.step .n{font:700 .78rem var(--mono);color:var(--acc)}
.step b{display:block;font-size:1.05rem;margin:8px 0 6px}
.step p{color:var(--muted);font-size:.92rem;margin:0 0 10px;line-height:1.5}
.step pre{padding:10px 12px;font-size:.74rem}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.strip img{border-radius:10px;border:1px solid var(--line2);aspect-ratio:16/10;object-fit:cover;width:100%;display:block}
.morelink{font:600 .95rem var(--disp);color:var(--ink)}
.morelink:hover{color:var(--acc)}
/* card wall */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 4px}
.filters button{background:transparent;border:1px solid var(--line2);color:var(--ink2);min-height:36px;
 padding:0 13px;border-radius:99px;cursor:pointer;font:.75rem/1 var(--mono);letter-spacing:.04em}
.filters button:hover{border-color:var(--ink)}
.filters button.on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:22px;padding:22px 0 30px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:block;
 transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s,border-color .18s}
.card .ph{overflow:hidden;aspect-ratio:16/10;background:var(--line)}
.card img{width:100%;height:100%;display:block;object-fit:cover;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.card:hover{transform:translateY(-4px);border-color:var(--line2);box-shadow:0 24px 46px -24px rgb(20 18 15/.5)}
.card:hover img{transform:scale(1.035)}
.card .body{padding:15px 17px 17px}
.card .nm{font-weight:700;font-size:1.06rem;letter-spacing:-.01em}
.card .sub{font:.7rem/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:5px 0 10px}
.card .tags{display:flex;flex-wrap:wrap;gap:5px}
.card .tag{font:.66rem/1 var(--mono);color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:4px 8px}
.card .more{font:.7rem/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--acc);margin-top:12px}
/* tables */
table{border-collapse:collapse;width:100%;font-size:.94rem}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
th{font:.72rem/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
tr:hover td{background:var(--panel)}
.tablewrap{overflow-x:auto;background:transparent;border:1px solid var(--line);border-radius:14px}
.tablewrap table{min-width:640px}
.tablewrap th{background:var(--panel)}
/* example */
.rb{display:grid;grid-template-columns:1.25fr .75fr;gap:18px;align-items:start;margin-bottom:26px}
.rb img{border-radius:12px;border:1px solid var(--line2);width:100%;display:block}
.rb .meta{padding-top:4px}
.rb .meta .d{font:700 .74rem var(--mono);letter-spacing:.08em;color:var(--acc)}
.rb .meta .d.hd{color:#0a7a4b}
.rb .meta b{display:block;font-size:1.1rem;margin:6px 0 4px;letter-spacing:-.01em}
.rb .meta p{color:var(--muted);margin:0 0 6px;font-size:.92rem}
.rb .meta .tx{font:.8rem/1.5 var(--mono);color:var(--ink2)}
/* detail */
.hero-img{width:100%;border-radius:18px;border:1px solid var(--line2);display:block;margin:30px 0;
 box-shadow:0 30px 60px -30px rgb(20 18 15/.5)}
.d{max-width:920px}
.d h1{font-size:clamp(2rem,4.6vw,3rem);letter-spacing:-.03em;font-weight:800;margin:0 0 12px;line-height:1.02}
.chipsrow{margin:0 0 22px;display:flex;flex-wrap:wrap;gap:7px}
.chip{font:.72rem/1 var(--mono);letter-spacing:.05em;border:1px solid var(--line2);border-radius:99px;padding:6px 11px;color:var(--muted)}
.chip.k{color:#fff;background:var(--ink);border-color:var(--ink)}
.world{font-size:1.18rem;line-height:1.45;color:var(--ink2);margin:0 0 24px;padding-left:16px;border-left:3px solid var(--acc)}
.d p{max-width:68ch;color:var(--ink2)}
.d h2{font:.72rem/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:38px 0 10px}
/* prose pages */
.prose{max-width:860px}
.prose h2{font-size:1.45rem;letter-spacing:-.02em;margin:40px 0 10px;font-weight:800}
.prose h2 .num{font:700 .78rem var(--mono);color:var(--acc);margin-right:10px}
.prose p,.prose li{color:var(--ink2);max-width:70ch}
.prose b{color:var(--ink)}
.faq details{border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:2px 18px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;padding:12px 0;font-size:.98rem}
.faq p{margin:0 0 14px}
@media(max-width:860px){
 .hero{grid-template-columns:1fr;gap:30px;padding:40px 0 8px}
 .claims,.steps{grid-template-columns:1fr}
 .strip{grid-template-columns:repeat(2,1fr)}
 .rb{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){
 *{transition:none!important;scroll-behavior:auto}
 .card:hover,.card:hover img{transform:none}
 .chain .ln{opacity:1;transform:none}
}
@media(prefers-contrast:more){:root{--muted:#54525a;--line:#c9c6bf;--line2:#b0ada5}}
"""

STAR_JS = """
fetch('https://api.github.com/repos/rocsgh/ppt-zen').then(r=>r.json()).then(d=>{
 if(d && typeof d.stargazers_count==='number'){var e=document.getElementById('ghstars');
 if(e){e.textContent=d.stargazers_count>=1000?(d.stargazers_count/1000).toFixed(1)+'k':d.stargazers_count;}}
}).catch(()=>{});
"""

FAVICON = ("data:image/svg+xml," +
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='12' fill='%2316151a'/%3E"
           "%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='36' fill='%23f7f5f0' text-anchor='middle'%3E%E7%A6%85%3C/text%3E%3C/svg%3E")


def shell(title, desc, path, ogimg, inner, js="", active=""):
    def on(k):
        return ' class="nl on"' if k == active else ' class="nl"'
    nav = ("""<div class="wrap"><nav><a class="mark" href="index.html">PPT&#8209;Zen</a>
<div class="navlinks">
<a%s href="method.html">Method</a>
<a%s href="example.html">Example</a>
<a%s href="gallery.html">Gallery</a>
<a%s href="install.html">Install</a>
<a class="btn solid" id="ghbtn" href="%s">GitHub &#9733; <small id="ghstars"></small></a>
</div></nav></div>""") % (on("method"), on("example"), on("gallery"), on("install"), GH)
    foot = ("""<footer><div class="wrap"><div class="cols">
<div>PPT-Zen &middot; a judgment layer for AI-made slides<br/>
Apache-2.0 (judgment layer) &middot; CC-BY-4.0 (styles) &middot; inspired by <i>Presentation Zen</i></div>
<div style="text-align:right">
<a href="%s">GitHub</a> &middot; <a href="%s/blob/master/CONTRIBUTING.md">Contribute a style</a> &middot; <a href="%s/blob/master/DESIGN.md">Design notes</a><br/>
<span class="kick" style="letter-spacing:.1em">Hosted version &mdash; coming</span>
</div></div></div></footer>""") % (GH, GH, GH)
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s/%s">
<link rel="icon" href="%s">
<meta property="og:type" content="website"><meta property="og:site_name" content="PPT-Zen">
<meta property="og:title" content="%s"><meta property="og:description" content="%s">
<meta property="og:url" content="%s/%s"><meta property="og:image" content="%s/img/%s">
<meta name="twitter:card" content="summary_large_image">
<style>%s</style></head><body>%s%s%s<script>%s%s</script></body></html>""") % (
        html.escape(title), html.escape(desc), BASE_URL, path, FAVICON,
        html.escape(title), html.escape(desc), BASE_URL, path, BASE_URL, ogimg,
        CSS, nav, inner, foot, STAR_JS, js)


# ---------------- pages ----------------
def page_home(packs):
    by = {p["slug"]: p for p in packs}
    chips, first = [], None
    for i, s in enumerate(SWITCHER):
        if s not in by or not os.path.exists(os.path.join(IMG, s + ".jpg")):
            continue
        nm = by[s].get("name", s)
        if first is None:
            first = s
        chips.append('<button data-img="img/%s.jpg"%s>%s</button>' % (s, ' class="on"' if i == 0 else "", html.escape(nm)))
    claims = """
<div class="claims">
<div class="claim"><b>It decides, you don't answer questions</b><span>Per page it sets the density (headline vs. detail), picks the device — the argument drawn as a thing — and holds one material across the whole deck.</span></div>
<div class="claim"><b>Full-image pages that hold up</b><span>Every slide is one designed image — typography, texture and illustration in the material you chose. English and dense data render clean.</span></div>
<div class="claim"><b>Open source, your image model</b><span>Apache-2.0 judgment layer + CC-BY styles. Works with any agent that generates images, or any OpenAI-compatible endpoint. No key ships in the repo.</span></div>
</div>"""
    chain = """
<div class="chain" id="chain">
<span class="ln"><span class="c1">page 03 &middot;</span> <span class="c3">"23 minutes to refocus"</span></span>
<span class="ln"><span class="c1">&rarr; sayable in one line?</span> <span class="c2">yes &rarr; HEADLINE</span> <span class="c1">(one giant number)</span></span>
<span class="ln"><span class="c1">&rarr; device:</span> <span class="c3">a draining hourglass</span> <span class="c1">— the cost of interruption, drawn</span></span>
<span class="ln"><span class="c1">page 08 &middot;</span> <span class="c3">"where we sit vs. the market"</span></span>
<span class="ln"><span class="c1">&rarr; only holds up side by side?</span> <span class="c2">yes &rarr; DETAIL</span> <span class="c1">(2&times;2 quadrant)</span></span>
<span class="ln"><span class="c1">&rarr; previous page was dense &rarr;</span> <span class="c3">this one breathes</span></span>
</div>"""
    steps = """
<div class="steps">
<div class="step"><span class="n">STEP 1</span><b>Install the skill</b><p>One command per runtime — Claude Code, Codex, Cursor, Windsurf, Hermes, OpenClaw.</p><pre>./install.sh claude --global</pre></div>
<div class="step"><span class="n">STEP 2</span><b>Say one sentence</b><p>In your agent:</p><pre>"Make me a 10-page pitch deck
 about &lt;project&gt;, Portolan style."</pre></div>
<div class="step"><span class="n">STEP 3</span><b>Get the deck</b><p>Plan &rarr; one image per page &rarr; proofread &rarr; assembled .pptx.</p><pre>python3 scripts/assemble_pptx.py \\
  slides/ deck.pptx</pre></div>
</div>"""
    strip = "".join('<a href="example.html"><img loading="lazy" src="img/rbp/%s.jpg" alt=""/></a>' % f
                    for f, *_ in [RB_PAGES[0], RB_PAGES[2], RB_PAGES[5], RB_PAGES[7]])
    feat = []
    for s in FEATURED:
        if s in by and os.path.exists(os.path.join(IMG, s + ".jpg")):
            p = by[s]
            feat.append('<a class="card" href="%s.html"><div class="ph"><img loading="lazy" src="img/%s.jpg" alt="%s"/></div>'
                        '<div class="body"><div class="nm">%s</div><div class="sub">%s</div></div></a>' % (
                            s, s, html.escape(p.get("name", "")), html.escape(p.get("name", "")),
                            html.escape(p.get("medium", ""))))
    inner = ("""<div class="wrap">
<section class="hero">
<div>
<div class="kick">Open-source judgment layer &middot; Apache-2.0</div>
<h1>One sentence in.<br/><em>Many worlds</em> out.</h1>
<p class="lede">Your agent decides how each page should be — density, device, material — then renders every slide as one designed image.</p>
<div class="hero-cta"><a class="btn solid" href="install.html">Install</a><a class="btn" href="example.html">See a real deck</a></div>
</div>
<div class="switcher">
<div class="stage"><img id="swimg" src="img/%s.jpg" alt="The same idea rendered in different materials"/></div>
<div class="chips" id="swchips">%s</div>
<div class="cap kick">The same idea &mdash; pick a material. Each one is a different world.</div>
</div>
</section>
%s
<section class="sec"><div class="shead"><span class="num">01</span><h2>Judgment, not generation</h2></div>
<p class="lede">Every AI PPT tool turns content into pages. PPT-Zen open-sources the part nobody else does: <b>for each page — how much should it hold, what should it look like, and on what grounds?</b> The finished deck is copyable; the chain of decisions is not.</p>
%s
<p style="margin-top:14px"><a class="morelink" href="method.html">Read the method &rarr;</a></p></section>
<section class="sec"><div class="shead"><span class="num">02</span><h2>How it works</h2></div>
<p class="lede">You bring an agent and an image model. The skill brings the judgment.</p>%s</section>
<section class="sec"><div class="shead"><span class="num">03</span><h2>Proof — a full deck, judged page by page</h2></div>
<p class="lede">Relayboard: a fictional 10-page pitch generated from one sentence, in one material — with the judgment log for every page.</p>
<div class="strip">%s</div>
<p style="margin-top:14px"><a class="morelink" href="example.html">See all 10 pages + the judgment log &rarr;</a></p></section>
<section class="sec"><div class="shead"><span class="num">04</span><h2>%d materials, one line each</h2></div>
<p class="lede">Every style ships a reproducible prompt formula. Contribute your own with a folder and a PR.</p>
<div class="grid">%s</div>
<p><a class="morelink" href="gallery.html">Browse all %d styles &rarr;</a></p></section>
<section class="sec"><div class="shead"><span class="num">05</span><h2>Install</h2></div>
<p class="lede">One command per runtime. The repo is the product — the site just shows you around.</p>
<pre>git clone %s
cd ppt-zen &amp;&amp; ./install.sh claude --global   # or codex / cursor / windsurf / hermes / openclaw / all</pre>
<p style="margin-top:16px"><a class="btn solid" href="install.html">Full install matrix</a> <a class="btn" href="%s">Open GitHub</a></p></section>
</div>""") % (first, "".join(chips), claims, chain, steps, strip, len(packs), "".join(feat), len(packs), GH, GH)
    js = """
var chips=document.querySelectorAll('#swchips button'),img=document.getElementById('swimg');
chips.forEach(function(b){var pre=new Image();pre.src=b.dataset.img;
 b.onclick=function(){chips.forEach(function(x){x.classList.remove('on')});b.classList.add('on');img.src=b.dataset.img;};});
var lns=document.querySelectorAll('#chain .ln');
if(matchMedia('(prefers-reduced-motion: reduce)').matches){lns.forEach(function(l){l.classList.add('show')});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
 lns.forEach(function(l,i){setTimeout(function(){l.classList.add('show')},i*350)});io.disconnect();}})});
 io.observe(document.getElementById('chain'));}
"""
    return shell("PPT-Zen — a judgment layer for AI-made slides",
                 "One sentence in, many worlds out. An open-source skill that decides how each slide should be, then renders it full-image in the material you choose.",
                 "", "portolan.jpg", inner, js, active="")


def page_method():
    inner = """<div class="wrap prose">
<section class="hero" style="display:block;padding-bottom:0">
<div class="kick">The method</div>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);letter-spacing:-.035em;line-height:1.02;margin:12px 0 0">A judgment layer,<br/>in five rules.</h1>
<p class="lede" style="max-width:60ch;font-size:1.1rem;color:var(--ink2);margin-top:16px">This page is the condensed method the skill executes. The full version — with the reasoning and the models we overturned — lives in <a href="https://github.com/rocsgh/ppt-zen/blob/master/SKILL.md" style="text-decoration:underline">SKILL.md</a> and <a href="https://github.com/rocsgh/ppt-zen/blob/master/DESIGN.md" style="text-decoration:underline">DESIGN.md</a>.</p>
</section>
<h2><span class="num">1</span>The one density test</h2>
<p>For every page: <b>is this sayable in a line, or does it only hold up when several things sit side by side?</b> Hearing is linear; seeing is simultaneous. A claim gets a HEADLINE page (one word, one number, one sentence). Evidence gets a DETAIL page (things laid out to scan). Two automatic rules: evidence pages must be detail — evidence you can't see doesn't count; and after a dense page, prefer a page that breathes.</p>
<h2><span class="num">2</span>Four axes, kept separate</h2>
<div class="tablewrap"><table>
<tr><th>Axis</th><th>What it is</th><th>Who decides</th></tr>
<tr><td><b>Density</b></td><td>headline &harr; detail</td><td>the agent, per page</td></tr>
<tr><td><b>Skeleton</b></td><td>how the frame is cut (grid / light-band / flowline / color-field / standoff&hellip; or none)</td><td>auto, by the page's job</td></tr>
<tr><td><b>Device</b></td><td><b>the page's argument, drawn as a thing</b></td><td>per page — the highest-value axis</td></tr>
<tr><td><b>Material</b></td><td>what it's made of (ink wash / copperplate / cinematic&hellip;)</td><td>once, whole deck</td></tr>
</table></div>
<h2><span class="num">3</span>The device — draw the argument</h2>
<p>Material says what a page is made of; skeleton says how it's cut. Neither says <i>what to draw</i>. The device fills that gap: "a score" becomes a measuring stick; "asking once is luck" becomes dots scattering then converging; "AI names only two brands" becomes a funnel. The test: <b>looking at the object, can you guess what the page says?</b> One main device per page — two competing illustrations equal none. And illustration is a scale, not a switch: margin studies, typography-as-image, small marks that replace a sentence, and full hero devices all stack.</p>
<h2><span class="num">4</span>Material — one world per deck</h2>
<p>Material is the deck's identity: skeleton and device vary per page, the material holds. Choose it in three layers — <b>medium</b> (the craft), <b>hand</b> (whose treatment of it), <b>world</b> (the scene the deck lives in). The <a href="gallery.html" style="text-decoration:underline">gallery</a> ships every style with a reproducible formula, and <code>styles.json</code> lets an agent resolve a named style deterministically.</p>
<h2><span class="num">5</span>Form, never facts</h2>
<p>The judgment layer owns how a page looks — never what it claims. The skill's hard rule: <b>no invented metrics, quotes, prices, dates, or names.</b> Facts come from your input; unknowns become visible <code>[TO CONFIRM]</code> placeholders. A beautiful slide with a made-up number is a liability, not a feature.</p>
<p style="margin-top:30px"><a class="btn solid" href="install.html">Install the skill</a> <a class="btn" href="example.html">See it applied</a></p>
</div>"""
    return shell("Method · PPT-Zen", "The condensed judgment method: one density test, four axes, the device, one material per deck, form never facts.",
                 "method.html", "swiss-grid.jpg", inner, active="method")


def page_example():
    rows = []
    for f, role, dens, dev, tx in RB_PAGES:
        rows.append(("""<div class="rb"><img loading="lazy" src="img/rbp/%s.jpg" alt="%s"/>
<div class="meta"><span class="d%s">%s</span><b>%s</b><p>device: %s</p><div class="tx">%s</div></div></div>""") % (
            f, html.escape(role), " hd" if dens == "HEADLINE" else "", dens, html.escape(role), html.escape(dev), html.escape(tx)))
    dark = "".join('<img loading="lazy" src="img/rb/%s.jpg" alt=""/>' % f
                   for f, *_ in [RB_PAGES[0], RB_PAGES[2], RB_PAGES[6], RB_PAGES[9]])
    inner = ("""<div class="wrap">
<section class="hero" style="display:block;padding-bottom:0">
<div class="kick">Worked example &middot; fictional product, invented demo numbers</div>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);letter-spacing:-.035em;line-height:1.02;margin:12px 0 0">Relayboard —<br/>ten pages, one sentence.</h1>
<p class="lede" style="max-width:62ch;font-size:1.1rem;color:var(--ink2);margin-top:16px">
<b>In:</b> "Make me a 10-page pitch deck for Relayboard, an async-standup tool, in the Portolan sea-chart style."
<b>Out:</b> the pages below — a growth story told as a voyage across a 16th-century chart.
The labels are the judgment log, the part you can't screenshot. Notice the rhythm: headline &rarr; a dense
evidence block &rarr; one line to land on. Every number is rendered inside the image and comes out clean.</p>
</section>
<section class="sec" style="border-top:none;margin-top:36px;padding-top:0">%s</section>
<section class="sec"><div class="shead"><span class="num">&#8646;</span><h2>Same judgment, another world</h2></div>
<p class="lede">The identical ten pages rendered in a premium dark-editorial material — the plan, densities and text
didn't change; only the material did. That swap is the whole product.</p>
<div class="strip">%s</div></section>
<section class="sec"><div class="shead"><span class="num">&#8594;</span><h2>Reproduce it</h2></div>
<p class="lede">The exact prompts live in <a href="https://github.com/rocsgh/ppt-zen/tree/master/examples" style="text-decoration:underline">examples/</a> (both editions) — material + device + verbatim text + the anti-garble tail, then assembled with one command.</p>
<pre>cd examples/relayboard-portolan          # or examples/relayboard (dark edition)
cp ../../.env.example .env               # your image model key
python3 gen.py                           # 10 pages -> slides/
python3 ../../scripts/assemble_pptx.py slides deck.pptx</pre>
<p style="margin-top:14px"><i>Relayboard is fictional; every metric is invented demo content. In real use the skill never invents facts — unknowns become [TO CONFIRM] placeholders.</i></p>
</section></div>""") % ("".join(rows), dark)
    return shell("Example — a 10-page deck with its judgment log · PPT-Zen",
                 "A complete worked deck: ten full-image pages from one sentence, with the per-page judgment log (density, device, exact text).",
                 "example.html", "rbp/01-cover.jpg", inner, active="example")


def page_gallery(packs):
    mediums = sorted(set(p.get("medium", "Other") for p in packs))
    cards = []
    for p in packs:
        s = p["slug"]
        name = p.get("name", "")
        medium = p.get("medium", "Other")
        hand = p.get("hand", "").strip()
        tags = re.findall(r"[\w一-鿿-]+", p.get("tags", ""))
        sub = html.escape(medium) + ((" &middot; " + html.escape(hand)) if hand else "")
        tag_html = "".join('<span class="tag">%s</span>' % html.escape(t) for t in tags[:4])
        cards.append(('<a class="card" href="%s.html" data-medium="%s">'
                      '<div class="ph"><img loading="lazy" src="img/%s.jpg" alt="%s"/></div>'
                      '<div class="body"><div class="nm">%s</div><div class="sub">%s</div>'
                      '<div class="tags">%s</div><div class="more">View details &rarr;</div></div></a>') % (
            s, html.escape(medium), s, html.escape(name), html.escape(name), sub, tag_html))
    filt = ['<button class="on" data-f="all">All</button>'] + \
           ['<button data-f="%s">%s</button>' % (html.escape(m), html.escape(m)) for m in mediums]
    inner = ("""<div class="wrap">
<section class="hero" style="display:block;padding-bottom:0">
<div class="kick">%d styles &middot; every card ships a reproducible prompt formula</div>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);letter-spacing:-.035em;margin:12px 0 0">The material library.</h1>
<p class="lede" style="max-width:60ch;font-size:1.08rem;color:var(--ink2);margin-top:14px">Material swatches show the same line — <i>Signal over noise</i> — so the surface is the only variable. Cinema hands show one sentence through different eyes. Click any card for the full recipe.</p>
</section>
<div class="filters">%s</div><div class="grid">%s</div>
<p><a class="morelink" href="https://github.com/rocsgh/ppt-zen/blob/master/CONTRIBUTING.md">Contribute a style — one folder, one PR &rarr;</a></p>
</div>""") % (len(packs), "".join(filt), "".join(cards))
    js = """
var btns=document.querySelectorAll('.filters button');
btns.forEach(function(b){b.onclick=function(){btns.forEach(function(x){x.classList.remove('on')});b.classList.add('on');
 var f=b.dataset.f;document.querySelectorAll('.card').forEach(function(c){c.style.display=(f==='all'||c.dataset.medium===f)?'':'none'});};});
"""
    return shell("Gallery — %d styles · PPT-Zen" % len(packs),
                 "Browse every PPT-Zen style: materials, cinema hands, bespoke worlds — each with a reproducible prompt formula.",
                 "gallery.html", "stele-rubbing.jpg", inner, js, active="gallery")


def page_install():
    inner = """<div class="wrap prose">
<section class="hero" style="display:block;padding-bottom:0">
<div class="kick">Install</div>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);letter-spacing:-.035em;margin:12px 0 0">One command,<br/>your runtime.</h1>
</section>
<h2><span class="num">1</span>Get the repo, install the skill</h2>
<pre>git clone https://github.com/rocsgh/ppt-zen
cd ppt-zen
./install.sh claude --global      # see the matrix below for your runtime</pre>
<div class="tablewrap" style="margin-top:16px"><table>
<tr><th>Runtime</th><th>Command</th><th>Installs to</th><th>Trigger</th></tr>
<tr><td><b>Claude Code</b></td><td><code>./install.sh claude [--global]</code></td><td><code>.claude/skills/ppt-zen/</code></td><td><code>/ppt-zen</code> or just ask for a deck</td></tr>
<tr><td><b>OpenClaw</b></td><td><code>./install.sh openclaw [--global]</code></td><td><code>.openclaw/skills/ppt-zen/</code></td><td>ask for a deck</td></tr>
<tr><td><b>Hermes</b></td><td><code>./install.sh hermes [--global]</code></td><td><code>.hermes/skills/ppt-zen/</code></td><td>ask for a deck</td></tr>
<tr><td><b>Codex CLI</b></td><td><code>./install.sh codex [--global]</code></td><td><code>AGENTS.md</code> / <code>~/.codex/AGENTS.md</code></td><td>passive — auto-read</td></tr>
<tr><td><b>Cursor</b></td><td><code>./install.sh cursor</code></td><td><code>.cursor/rules/ppt-zen.mdc</code></td><td>passive — auto-applied</td></tr>
<tr><td><b>Windsurf</b></td><td><code>./install.sh windsurf</code></td><td><code>.windsurf/rules/ppt-zen.md</code></td><td>passive — auto-applied</td></tr>
<tr><td><b>GitHub Copilot</b></td><td><code>./install.sh copilot</code></td><td><code>.github/instructions/</code></td><td>passive — auto-applied</td></tr>
<tr><td>everything</td><td><code>./install.sh all</code></td><td>all of the above</td><td>—</td></tr>
</table></div>
<p style="margin-top:12px">Skill installs are self-contained (SKILL.md + references + styles + scripts + examples + <code>styles.json</code>). No skill system at all? Paste <code>SKILL.md</code> into the session as context.</p>
<h2><span class="num">2</span>Wire an image model</h2>
<p>Every page is a generated image. If your agent already has an image tool, there's nothing to do — the skill uses it. Otherwise point the bundled helper at <b>any OpenAI-compatible images endpoint</b>:</p>
<pre>cp .env.example .env                  # IMAGE_API_BASE_URL / IMAGE_API_KEY / IMAGE_MODEL / IMAGE_SIZE
python3 scripts/gen_image.py --check  # verify before a long run</pre>
<p>PPT-Zen ships <b>no key and no model</b> — the judgment is open source, the pixels are yours.</p>
<h2><span class="num">3</span>Make a deck</h2>
<pre>"Make me a 10-page pitch deck about &lt;your project&gt; with ppt-zen, in the Portolan style."</pre>
<p>The agent plans (<code>plan.md</code>), generates one image per page into <code>slides/</code>, you proofread, then:</p>
<pre>pip install python-pptx
python3 scripts/assemble_pptx.py slides/ deck.pptx</pre>
<h2><span class="num">?</span>FAQ</h2>
<div class="faq">
<details><summary>Which image models work?</summary><p>Anything behind an OpenAI-compatible <code>/images/generations</code> route — OpenAI's gpt-image models, relays, gateways. The gallery samples were generated with gpt-image class models at 1536&times;1024. Non-16:9 output is center cover-cropped at assembly, so prompts keep key content clear of the top/bottom ~8%.</p></details>
<details><summary>Is the .pptx editable?</summary><p>It's image-based: each slide is one full-bleed image. Present it, export PDF, or import into Keynote/Google Slides — but text isn't editable. Fixing a typo means regenerating that one page (the skill supports single-page regeneration).</p></details>
<details><summary>Will it invent numbers for my deck?</summary><p>No — that's a hard rule. Facts come from your input; anything missing becomes a visible <code>[TO CONFIRM]</code> placeholder. The skill decides form, never facts.</p></details>
<details><summary>Can I add my own style?</summary><p>Yes — copy <code>styles/_template/</code>, fill in the STYLE.md (material recipe + a sample), open a PR. The gallery and <code>styles.json</code> regenerate automatically. Styles are CC-BY-4.0, contributions via DCO.</p></details>
<details><summary>What does it cost to run?</summary><p>Whatever your image endpoint charges — a 10-page deck is 10 images (plus any single-page retries you choose).</p></details>
</div>
<p style="margin-top:26px"><a class="btn solid" href="__GH__">Open GitHub</a> <a class="btn" href="example.html">See a finished deck first</a></p>
</div>""".replace("__GH__", GH)
    return shell("Install · PPT-Zen", "Install the PPT-Zen skill in Claude Code, Codex CLI, Cursor, Windsurf, Hermes, OpenClaw or Copilot — one command each — and wire any OpenAI-compatible image model.",
                 "install.html", "swiss-grid.jpg", inner, active="install")


def page_detail(p):
    dst_name = p["slug"] + ".jpg"
    name = p.get("name", "")
    medium = p.get("medium", "Other")
    hand = p.get("hand", "").strip()
    tags = re.findall(r"[\w一-鿿-]+", p.get("tags", ""))
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
<img class="hero-img" src="img/%s" alt="%s"/>
<h1>%s</h1><div class="chipsrow">%s</div>
%s%s
<h2>Prompt formula</h2><pre>%s</pre>%s
<p class="kick" style="margin-top:24px">License: %s &middot; contributions via DCO</p>
<p style="margin-top:18px"><a class="btn" href="gallery.html">&larr; All styles</a> <a class="btn solid" href="install.html">Use this style</a></p>
</div>""") % (
        dst_name, html.escape(name), html.escape(name), "".join(chips),
        ('<p class="world">%s</p>' % html.escape(world)) if world else "",
        paras, formula if formula else "(none)",
        ('<h2>Source</h2><p>%s</p>' % inline_md(source)) if source else "", html.escape(lic))
    return shell(name + " · PPT-Zen", medium + " recipe for AI-made slides, with a reproducible prompt formula.",
                 p["slug"] + ".html", dst_name, inner, active="gallery")


def build():
    packs = load()
    os.makedirs(IMG, exist_ok=True)
    # sync pack samples
    for p in packs:
        samp = (p.get("samples") or ["samples/01.jpg"])[0]
        src = os.path.join(p["_dir"], samp)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(IMG, p["slug"] + ".jpg"))
    # sync example slides (both editions)
    for sub, dirname in (("rb", "relayboard"), ("rbp", "relayboard-portolan")):
        d = os.path.join(IMG, sub)
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(os.path.join(ROOT, "examples", dirname, "slides", "*.jpg")):
            shutil.copyfile(f, os.path.join(d, os.path.basename(f)))
    pages = {
        "index.html": page_home(packs),
        "method.html": page_method(),
        "example.html": page_example(),
        "gallery.html": page_gallery(packs),
        "install.html": page_install(),
    }
    for p in packs:
        pages[p["slug"] + ".html"] = page_detail(p)
    for fn, content in pages.items():
        open(os.path.join(DOCS, fn), "w", encoding="utf-8").write(content)
    # sitemap + robots
    urls = ["", "method.html", "example.html", "gallery.html", "install.html"] + \
           [p["slug"] + ".html" for p in packs]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + \
         ["<url><loc>%s/%s</loc></url>" % (BASE_URL, u) for u in urls] + ["</urlset>"]
    open(os.path.join(DOCS, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(DOCS, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE_URL)
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print("site built: %d pages (%d styles) + sitemap + robots" % (len(pages), len(packs)))


if __name__ == "__main__":
    build()
