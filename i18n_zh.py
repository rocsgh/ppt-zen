# -*- coding: utf-8 -*-
"""PPT-Zen site i18n layer: emits /zh/ versions of the 5 marketing pages by
translating the built English HTML (single source of truth stays the builders),
plus browser-language auto-detect and a top-right EN|中文 switcher on every page."""
import re

MARKETING = ["index.html", "method.html", "example.html", "gallery.html", "install.html"]

# ordered (en, zh) replacements — applied to the full HTML of marketing pages
ZH = [
 # titles + meta
 ("<title>PPT-Zen — a judgment layer for AI-made slides</title>", "<title>PPT-Zen — AI 幻灯片的判断层</title>"),
 ("<title>Method · PPT-Zen</title>", "<title>方法论 · PPT-Zen</title>"),
 ("<title>Example — a 10-page deck with its judgment log · PPT-Zen</title>", "<title>案例 — 十页成片与判断日志 · PPT-Zen</title>"),
 ("<title>Gallery — 44 styles · PPT-Zen</title>", "<title>画廊 — 44 个风格 · PPT-Zen</title>"),
 ("<title>Install · PPT-Zen</title>", "<title>安装 · PPT-Zen</title>"),
 # nav
 ('>Method</a>', '>方法论</a>'),
 ('>Example</a>', '>案例</a>'),
 ('>Gallery</a>', '>画廊</a>'),
 ('>Install</a>', '>安装</a>'),
 # home hero
 ("Open-source judgment layer &middot; Apache-2.0", "开源判断层 &middot; Apache-2.0"),
 ("One sentence in.<br/><em>Many worlds</em> out.", "一句话进。<br/><em>万千世界</em>出。"),
 ("Your agent decides how each page should be — density, device, material — then renders every slide as one designed image.",
  "你的 agent 自己决定每一页该怎么做——详略、器物、材质——然后把每一页渲染成一整张设计好的图。"),
 ('>Install</a><a class="btn" href="example.html">See a real deck</a>', '>安装</a><a class="btn" href="example.html">看一套真实成片</a>'),
 ("The same idea &mdash; pick a material. Each one is a different world.", "同一个想法 —— 选一种材质，就是另一个世界。"),
 # home claims
 ("It decides, you don't answer questions", "它来判断，你不用回答问题"),
 ("Per page it sets the density (headline vs. detail), picks the device — the argument drawn as a thing — and holds one material across the whole deck.",
  "它逐页决定详略（提纲挈领还是细化）、想出器物——把这页的论点画成一个东西——并且全片只用一种材质。"),
 ("Full-image pages that hold up", "整页出图，经得起看"),
 ("Every slide is one designed image — typography, texture and illustration in the material you chose. English and dense data render clean; you proofread each page, and a miss regenerates in one command.",
  "每一页都是一整张设计好的图——排印、质感、插画都长在你选的材质里。英文与密集数据渲染得干净；每页你都要校对一遍，出错的页一行命令单独重出。"),
 ("Open source, your image model", "开源，图像模型你自带"),
 ("Apache-2.0 judgment layer + CC-BY styles. Works with any agent that generates images, or any OpenAI-compatible endpoint. No key ships in the repo.",
  "判断层 Apache-2.0 + 风格 CC-BY。任何能生图的 agent，或任何实现 OpenAI 图像接口的端点都能用。仓库不带任何 key。"),
 # home sections
 ("Judgment, not generation", "判断，而不是生成"),
 ("Every AI PPT tool turns content into pages. PPT-Zen open-sources the part nobody else does: <b>for each page — how much should it hold, what should it look like, and on what grounds?</b> The finished deck is copyable; the chain of decisions is not.",
  "所有 AI PPT 工具都在做同一件事：把内容变成页面。PPT-Zen 开源的是没人做的那一层：<b>这一页——该放多少、长什么样、凭什么这么定？</b>成品谁都能截图；判断链抄不走。"),
 ("Read the method &rarr;", "读方法论 &rarr;"),
 ("How it works", "怎么用"),
 ("You bring an agent and an image model. The skill brings the judgment.", "你带一个 agent 和一个图像模型，判断由这个 skill 提供。"),
 ("Install the skill</b><p>One command per runtime — Claude Code, Codex, Cursor, Windsurf, Hermes, OpenClaw.</p>",
  "装技能</b><p>每个运行时一行命令——Claude Code、Codex、Cursor、Windsurf、Hermes、OpenClaw。</p>"),
 ("Say one sentence</b><p>In your agent:</p>", "说一句话</b><p>在你的 agent 里：</p>"),
 ("Get the deck</b><p>Plan &rarr; one image per page &rarr; proofread &rarr; assembled .pptx.</p>",
  "拿到成片</b><p>计划 &rarr; 逐页出图 &rarr; 校对 &rarr; 拼装 .pptx。</p>"),
 ("Proof — a full deck, judged page by page", "证据 —— 一整套片子，逐页判断"),
 ("Relayboard: a fictional 10-page pitch generated from one sentence, told as a voyage across a 16th-century sea chart &mdash; with the judgment log for every page.",
  "Relayboard：一个虚构产品的 10 页 pitch，由一句话生成，讲成一场 16 世纪航海图上的远航 —— 每一页都附判断日志。"),
 ("Relayboard: a fictional 10-page pitch generated from one sentence, in one material — with the judgment log for every page.",
  "Relayboard：一个虚构产品的 10 页 pitch，由一句话生成、一种材质贯穿 —— 每一页都附判断日志。"),
 ("See all 10 pages + the judgment log &rarr;", "看全部 10 页 + 判断日志 &rarr;"),
 ("44 materials, one line each", "44 个风格，每个都带配方"),
 ("Every style ships a reproducible prompt formula. Contribute your own with a folder and a PR.",
  "每个风格都带一条可复现的 prompt 配方。想贡献自己的？一个文件夹、一个 PR。"),
 ("Browse all 44 styles &rarr;", "浏览全部 44 个风格 &rarr;"),
 ("One command per runtime. The repo is the product — the site just shows you around.",
  "每个运行时一行命令。仓库才是产品——官网只是带你逛逛。"),
 ("Full install matrix", "完整安装矩阵"),
 ("Open GitHub", "打开 GitHub"),
 # example page
 ("Worked example &middot; fictional product, invented demo numbers", "完整案例 &middot; 虚构产品，数字为演示内容"),
 ("Relayboard —<br/>ten pages, one sentence.", "Relayboard ——<br/>十页，一句话。"),
 ("<b>In:</b> \"Make me a 10-page pitch deck for Relayboard, an async-standup tool, in the Portolan sea-chart style.\"",
  "<b>输入：</b>「用航海图（Portolan）风格，给异步站会工具 Relayboard 做一套 10 页 pitch。」"),
 ("<b>Out:</b> the pages below — a growth story told as a voyage across a 16th-century chart.",
  "<b>输出：</b>下面这些页——一个增长故事，讲成 16 世纪海图上的一场远航。"),
 ("The labels are the judgment log, the part you can't screenshot. Notice the rhythm: headline &rarr; a dense\nevidence block &rarr; one line to land on. Every number is rendered inside the image and comes out clean.",
  "旁边的标签就是判断日志——截图截不走的那部分。注意节奏：提纲挈领 &rarr; 密集证据块 &rarr; 一句话收尾。所有数字都渲染在图里，个个清晰。"),
 ("device: ", "器物："),
 ("Same judgment, another world", "同一套判断，另一个世界"),
 ("The identical ten pages rendered in a premium dark-editorial material — the plan, densities and text\ndidn't change; only the material did. That swap is the whole product.",
  "同样的十页，换成高级暗色编辑风材质——计划、详略、文案一字未动，只换了材质。这一换，就是整个产品。"),
 ("Reproduce it", "复现它"),
 ("The exact prompts live in", "逐页的完整 prompt 就在"),
 ("(both editions) — material + device + verbatim text + the anti-garble tail, then assembled with one command.",
  "（两个版本都有）——材质 + 器物 + 逐字文案 + 防乱码尾注，一行命令拼装。"),
 ("<i>Relayboard is fictional; every metric is invented demo content. In real use the skill never invents facts — unknowns become [TO CONFIRM] placeholders.</i>",
  "<i>Relayboard 是虚构产品，所有数字都是演示内容。真实使用中这个 skill 绝不编造事实——缺的数字会显示 [TO CONFIRM] 占位。</i>"),
 # gallery page
 ("44 styles &middot; every card ships a reproducible prompt formula", "44 个风格 &middot; 每张卡都带可复现配方"),
 ("The material library.", "材质库。"),
 ("Material swatches show the same line — <i>Signal over noise</i> — so the surface is the only variable. Cinema hands show one sentence through different eyes. Click any card for the full recipe.",
  "材质样张统一用同一句话——<i>Signal over noise</i>——材质因此成为唯一变量。电影手笔组则是同一句话经过不同导演之眼。点任何一张卡看完整配方。"),
 ("Contribute a style — one folder, one PR &rarr;", "贡献一个风格——一个文件夹、一个 PR &rarr;"),
 (">All</button>", ">全部</button>"),
 ("View details &rarr;", "看详情 &rarr;"),
 # install page
 ("One command,<br/>your runtime.", "一行命令，<br/>装进你的运行时。"),
 ("Get the repo, install the skill", "拿仓库、装技能"),
 ("<th>Runtime</th><th>Command</th><th>Installs to</th><th>Trigger</th>", "<th>运行时</th><th>命令</th><th>装到哪</th><th>触发方式</th>"),
 ("<code>/ppt-zen</code>, or just ask for a deck", "<code>/ppt-zen</code>，或直接说要做 deck"),
 ("<td>ask for a deck</td>", "<td>直接说要做 deck</td>"),
 ("passive — auto-read", "被动——自动读取"),
 ("passive — auto-applied", "被动——自动生效"),
 ("<td>everything</td>", "<td>全部</td>"),
 ("<td>all of the above</td>", "<td>以上全部</td>"),
 ("Skill installs are self-contained (SKILL.md + references + styles + scripts + examples + <code>styles.json</code>). No skill system at all? Paste <code>SKILL.md</code> into the session as context.",
  "技能安装是自包含的（SKILL.md + references + styles + scripts + examples + <code>styles.json</code>）。完全没有 skill 系统？把 <code>SKILL.md</code> 整段贴进会话当上下文即可。"),
 ("Wire an image model", "接上图像模型"),
 ("Every page is a generated image. If your agent already has an image tool, there's nothing to do — the skill uses it. Otherwise point the bundled helper at <b>any endpoint that implements the OpenAI <code>/images/generations</code> API</b> (accepts <code>{model, prompt, size, n}</code>, returns <code>b64_json</code> or <code>url</code> — chat-only \"compatible\" gateways don't count):",
  "每一页都是生成的图。如果你的 agent 本身带图像工具，什么都不用配——skill 直接用它。否则把内置脚本指向<b>实现了 OpenAI <code>/images/generations</code> 接口的任意端点</b>（接受 <code>{model, prompt, size, n}</code>、返回 <code>b64_json</code> 或 <code>url</code>——只兼容 chat 的\"兼容\"网关不算）："),
 ("PPT-Zen ships <b>no key and no model</b> — the judgment is open source, the pixels are yours.",
  "PPT-Zen <b>不带任何 key、不绑定任何模型</b>——判断是开源的，像素是你自己的。"),
 ("Make a deck — what you actually say", "做一套片——你实际要说的话"),
 ("Open your agent in any project and talk. One sentence starts it; the skill decides the rest and never quizzes you about layout:",
  "在任何项目里打开你的 agent，直接说话。一句话就能开始；剩下的它来判断，绝不会反问你版式问题："),
 ("The agent writes <code>plan.md</code> (page &middot; density &middot; device &middot; exact text &middot; style) — review it if you like — then generates one image per page into <code>slides/</code>. Iterate by pointing at pages:",
  "agent 会先写 <code>plan.md</code>（页 &middot; 详略 &middot; 器物 &middot; 逐字文案 &middot; 风格）——想过目就过目——然后逐页出图到 <code>slides/</code>。之后对着页迭代："),
 ("<b>Feed it your facts.</b> Attach an outline / metrics / links — real numbers land on the slides; anything missing shows as <code>[TO CONFIRM]</code> rather than an invented figure. When the pages read clean:",
  "<b>把真实数据喂给它。</b>附上提纲 / 指标 / 链接——真数字会上片；缺的只会显示 <code>[TO CONFIRM]</code> 占位，绝不编造。页面都校对干净之后："),
 ("# it chooses", "# 它自己选"),
 ("# single page", "# 单页也行"),
 ("# same plan, new world", "# 同一计划，换个世界"),
 ("Which image models work?", "哪些图像模型能用？"),
 ("Anything behind an OpenAI-compatible <code>/images/generations</code> route — OpenAI's gpt-image models, relays, gateways. The gallery samples were generated with gpt-image class models at 1536&times;1024. Non-16:9 output is center cover-cropped at assembly, so prompts keep key content clear of the top/bottom ~8%.",
  "任何走 OpenAI 兼容 <code>/images/generations</code> 路由的——OpenAI 的 gpt-image 系、各类中转、网关。画廊样张用 gpt-image 级模型在 1536&times;1024 生成。非 16:9 的输出会在拼装时居中裁切，所以 prompt 会让关键内容避开上下约 8%。"),
 ("Is the .pptx editable?", "拼出来的 .pptx 能编辑吗？"),
 ("It's image-based: each slide is one full-bleed image. Present it, export PDF, or import into Keynote/Google Slides — but text isn't editable. Fixing a typo means regenerating that one page (the skill supports single-page regeneration).",
  "它是图片型的：每页一整张满幅图。放映、导 PDF、导入 Keynote/Google Slides 都行——但文字不可编辑。改错字 = 重出那一页（skill 支持单页重出）。"),
 ("Will it invent numbers for my deck?", "它会替我编数字吗？"),
 ("No — that's a hard rule. Facts come from your input; anything missing becomes a visible <code>[TO CONFIRM]</code> placeholder. The skill decides form, never facts.",
  "不会——这是硬规则。事实只来自你的输入；缺的会显示成 <code>[TO CONFIRM]</code> 占位。skill 只定版式，绝不编事实。"),
 ("Can I add my own style?", "我能加自己的风格吗？"),
 ("Yes — copy <code>styles/_template/</code>, fill in the STYLE.md (material recipe + a sample), open a PR. The gallery and <code>styles.json</code> regenerate automatically. Styles are CC-BY-4.0, contributions via DCO.",
  "能——复制 <code>styles/_template/</code>，填好 STYLE.md（材质配方 + 一张样张），提 PR。画廊和 <code>styles.json</code> 自动重建。风格是 CC-BY-4.0，贡献走 DCO。"),
 ("What does it cost to run?", "跑一次要花多少钱？"),
 ("Whatever your image endpoint charges — a 10-page deck is 10 images plus any single-page retries. Order of magnitude (OpenAI gpt-image list prices, mid-2026): roughly $0.06–0.25 per 1536&times;1024 image depending on quality tier, so a first pass is about $1–3; budget 20–40 minutes including proofreading. Check your own endpoint's pricing.",
  "取决于你的图像端点收费——10 页 = 10 张图，外加你选择的单页重试。量级参考（OpenAI gpt-image 官方价，2026 年中）：1536&times;1024 每张约 $0.06–0.25（看质量档），首轮 10 页约 $1–3；含逐页校对预留 20–40 分钟。以你自己端点的价格为准。"),
 ("See a finished deck first", "先看一套成片"),
 # method page
 (">The method<", ">方法论<"),
 ("A judgment layer,<br/>in five rules.", "一个判断层，<br/>五条规则讲完。"),
 ("This page is the condensed method the skill executes. The full version — with the reasoning and the models we overturned — lives in",
  "这页是 skill 实际执行的方法的浓缩版。完整版——包括推导过程和被我们推翻过的旧模型——在"),
 ("The one density test", "唯一的详略判据"),
 ("For every page: <b>is this sayable in a line, or does it only hold up when several things sit side by side?</b> Hearing is linear; seeing is simultaneous. A claim gets a HEADLINE page (one word, one number, one sentence). Evidence gets a DETAIL page (things laid out to scan). Two automatic rules: evidence pages must be detail — evidence you can't see doesn't count; and after a dense page, prefer a page that breathes.",
  "对每一页问：<b>这是「一句话说得完」的，还是「必须并置才成立」的？</b>听觉是线性的，视觉是并置的。主张给 HEADLINE 页（一个词、一个数、一句话）；证据给 DETAIL 页（把东西摆出来可扫读）。两条自动规则：证据页必须细化——看不见的证据不算数；密页之后，接一页疏的。"),
 ("Four axes, kept separate", "四根轴，各管各的"),
 ("<th>Axis</th><th>What it is</th><th>Who decides</th>", "<th>轴</th><th>是什么</th><th>谁来定</th>"),
 ("<td><b>Density</b></td><td>headline &harr; detail</td><td>the agent, per page</td>", "<td><b>详略</b></td><td>提纲挈领 &harr; 细化</td><td>agent 逐页判</td>"),
 ("<td><b>Skeleton</b></td><td>how the frame is cut (grid / light-band / flowline / color-field / standoff&hellip; or none)</td><td>auto, by the page's job</td>",
  "<td><b>骨架</b></td><td>画面怎么被切分（网格 / 光带 / 流线 / 色域 / 对峙&hellip;也可不派）</td><td>按页面职能自动派</td>"),
 ("<td><b>Device</b></td><td><b>the page's argument, drawn as a thing</b></td><td>per page — the highest-value axis</td>",
  "<td><b>器物</b></td><td><b>这一页的论点，画成一个东西</b></td><td>逐页想——最值钱的一根</td>"),
 ("<td><b>Material</b></td><td>what it's made of (ink wash / copperplate / cinematic&hellip;)</td><td>once, whole deck</td>",
  "<td><b>材质</b></td><td>用什么做的（水墨 / 铜版 / 电影感&hellip;）</td><td>全片选一次</td>"),
 ("The device — draw the argument", "器物——把论点画出来"),
 ("Material says what a page is made of; skeleton says how it's cut. Neither says <i>what to draw</i>. The device fills that gap: \"a score\" becomes a measuring stick; \"asking once is luck\" becomes dots scattering then converging; \"AI names only two brands\" becomes a funnel. The test: <b>looking at the object, can you guess what the page says?</b> One main device per page — two competing illustrations equal none. And illustration is a scale, not a switch: margin studies, typography-as-image, small marks that replace a sentence, and full hero devices all stack.",
  "材质管「用什么做的」，骨架管「画面怎么切」——它们都不管<i>画什么</i>。器物补上这个空档：「一个分数」画成一把刻度尺；「只问一次靠运气」画成散开又收敛的点阵；「AI 只报两个名字」画成一个漏斗。判据：<b>看着这个东西，能不能猜出这页在说什么？</b>一页只有一件主器物——两件互相抢就等于没有。而且插画是量级不是开关：边饰习作、排印即画面、替代一句话的小记号、整页主器物，可以叠。"),
 ("Material — one world per deck", "材质——一套片一个世界"),
 ("Material is the deck's identity: skeleton and device vary per page, the material holds. Choose it in three layers — <b>medium</b> (the craft), <b>hand</b> (whose treatment of it), <b>world</b> (the scene the deck lives in). The",
  "材质是一套片的身份：骨架和器物逐页变，材质不动。选材质分三层——<b>介质</b>（工艺本身）、<b>手笔</b>（谁的处理方式）、<b>世界</b>（整套片住在什么场景里）。"),
 ("ships every style with a reproducible formula, and <code>styles.json</code> lets an agent resolve a named style deterministically.",
  "里每个风格都带可复现配方，<code>styles.json</code> 让 agent 能把风格名确定性解析到配方。"),
 ("Form, never facts", "只定版式，绝不编事实"),
 ("The judgment layer owns how a page looks — never what it claims. The skill's hard rule: <b>no invented metrics, quotes, prices, dates, or names.</b> Facts come from your input; unknowns become visible <code>[TO CONFIRM]</code> placeholders. A beautiful slide with a made-up number is a liability, not a feature.",
  "判断层只管页面长什么样——绝不管它声称什么。skill 的硬规则：<b>不编造任何指标、引语、价格、日期、名字。</b>事实只来自你的输入；缺的变成可见的 <code>[TO CONFIRM]</code> 占位。一页配着编造数字的漂亮幻灯片是负债，不是功能。"),
 ("Install the skill</a>", "装技能</a>"),
 ("See it applied", "看它的成品"),
 # footer
 ("a judgment layer for AI-made slides", "AI 幻灯片的判断层"),
 ("Apache-2.0 (judgment layer) &middot; CC-BY-4.0 (styles) &middot; inspired by <i>Presentation Zen</i>",
  "判断层 Apache-2.0 &middot; 风格 CC-BY-4.0 &middot; 受《演说之禅》启发"),
 ("styles &middot; auto-generated from the style packs &middot;", "个风格 &middot; 由风格包自动生成 &middot;"),
 (">Contribute a style</a>", ">贡献风格</a>"),
 (">Design notes</a>", ">设计笔记</a>"),
 ("Hosted version &mdash; coming", "托管版 &mdash; 敬请期待"),
 (">GitHub</a>", ">GitHub</a>"),
]

SWITCH_JS = "localStorage.setItem('pz-lang','%s')"

DETECT = """<script>(function(){try{
var pref=localStorage.getItem('pz-lang');
var zh=location.pathname.indexOf('/zh/')===0;
var page='%PAGE%'==='index.html'?'':'%PAGE%';
if(zh){if(pref==='en'){location.replace('/'+page);}}
else{if(pref==='zh'){location.replace('/zh/'+page);}
else if(!pref&&((navigator.language||'').toLowerCase().indexOf('zh')===0)){location.replace('/zh/'+page);}}
}catch(e){}})();</script>"""

GHBTN = '<a class="btn solid" id="ghbtn"'


def hreflang(page):
    en = "%s/%s" % (BASE_URL, "" if page == "index.html" else page)
    zh = "%s/zh/%s" % (BASE_URL, "" if page == "index.html" else page)
    return ('<link rel="alternate" hreflang="en" href="%s">'
            '<link rel="alternate" hreflang="zh" href="%s">'
            '<link rel="alternate" hreflang="x-default" href="%s">') % (en, zh, en)


def inject_en(html_s, page):
    """EN marketing page: hreflang + auto-detect + switcher to zh."""
    html_s = html_s.replace("</head>", hreflang(page) + "</head>", 1)
    html_s = html_s.replace("<body>", "<body>" + DETECT.replace("%PAGE%", page), 1)
    sw = '<a class="btn" href="/zh/%s" onclick="%s">中文</a>' % (
        "" if page == "index.html" else page, SWITCH_JS % "zh")
    return html_s.replace(GHBTN, sw + GHBTN, 1)


def inject_detail(html_s):
    """EN detail page: switcher only (zh side lands on the zh gallery)."""
    sw = '<a class="btn" href="/zh/gallery.html" onclick="%s">中文</a>' % (SWITCH_JS % "zh")
    return html_s.replace(GHBTN, sw + GHBTN, 1)


def make_zh(html_s, page):
    """Translate a built EN marketing page into its /zh/ sibling."""
    for en, zh in ZH:
        html_s = html_s.replace(en, zh)
    # asset + canonical/og paths
    html_s = html_s.replace('src="img/', 'src="../img/')
    html_s = html_s.replace('href="%s/%s">' % (BASE_URL, page), 'href="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('content="%s/%s">' % (BASE_URL, page), 'content="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    # detail-page links leave the /zh/ subtree
    def fix_href(m):
        t = m.group(1)
        return m.group(0) if t + ".html" in MARKETING else 'href="../%s.html"' % t
    html_s = re.sub(r'href="([a-z0-9-]+)\.html"', fix_href, html_s)
    # hreflang + detect + switcher back to EN
    html_s = html_s.replace("</head>", hreflang(page) + "</head>", 1)
    html_s = html_s.replace("<body>", "<body>" + DETECT.replace("%PAGE%", page), 1)
    sw = '<a class="btn" href="/%s" onclick="%s">EN</a>' % (
        "" if page == "index.html" else page, SWITCH_JS % "en")
    return html_s.replace(GHBTN, sw + GHBTN, 1)


# medium labels (gallery filters + card sublabels); style names stay English as product names
MEDIUM_ZH = {
 "3D craft": "3D 工艺", "African textile": "非洲织物", "Astronomical": "天文", "Bookbinding": "书籍装帧",
 "Carving": "雕刻", "Ceramic": "陶瓷", "Chinese ink": "水墨", "Cinema": "电影",
 "Da Vinci copperplate": "达芬奇铜版", "Deco": "装饰艺术", "Diagram": "图解", "Enamel": "珐琅",
 "Fresco": "壁画", "Hand-drawn": "手绘", "Industrial": "工业", "Ink rubbing": "拓片",
 "Islamic tile": "伊斯兰瓷砖", "Lacquer": "漆器", "Modern": "现代", "Painterly": "绘画",
 "Paper craft": "纸艺", "Portolan chart": "航海图", "Print": "版画", "Technical": "技术制图",
 "Textile": "织物", "Woodblock": "木刻",
}

# example page: judgment-log roles + portolan devices
EXTRA_ZH = [
 (">See a real deck</a>", ">看一套真实成片</a>"),
 ("<b>cover</b>", "<b>封面</b>"), ("<b>problem</b>", "<b>问题</b>"), ("<b>cost</b>", "<b>成本</b>"),
 ("<b>product</b>", "<b>产品</b>"), ("<b>how</b>", "<b>流程</b>"), ("<b>traction</b>", "<b>增长</b>"),
 ("<b>pricing</b>", "<b>定价</b>"), ("<b>competition</b>", "<b>竞位</b>"), ("<b>roadmap</b>", "<b>路线图</b>"),
 ("<b>ask</b>", "<b>募资</b>"),
 ("a fleet departing toward a marked destination", "船队启航，驶向标记的目的地"),
 ("a voyage route that snaps mid-sea", "航线在海中央断裂"),
 ("giant numeral + navigator&#x27;s dividers", "巨大数字 + 领航员两脚规"),
 ("giant numeral + navigator's dividers", "巨大数字 + 领航员两脚规"),
 ("a courier boat drawing alongside", "交通艇靠上大船"),
 ("three islands on one dotted route", "一条虚线航路上的三座岛"),
 ("a fleet climbing a rising sea-lane", "船队爬升上扬的航道"),
 ("three ships of ascending size", "三条由小到大的船"),
 ("2×2 chart quadrant, one red dot", "羊皮纸上的 2×2 象限，一枚红点"),
 ("a coastline route, three harbors", "海岸线航路，三个港口"),
 ("one red route to the sunrise", "一条冲向日出的红色航线"),
 ('class="kick">Install<', 'class="kick">安装<'),
]

_orig_make_zh = make_zh
def make_zh(html_s, page):  # noqa: F811 — extend the base translator
    html_s = _orig_make_zh(html_s, page)
    for en, zh in EXTRA_ZH:
        html_s = html_s.replace(en, zh)
    for en, zh in MEDIUM_ZH.items():
        html_s = html_s.replace(">%s</button>" % en, ">%s</button>" % zh)      # filter buttons (data-f untouched)
        html_s = html_s.replace('class="sub">%s<' % en, 'class="sub">%s<' % zh)  # card sublabel, no hand
        html_s = html_s.replace('class="sub">%s &middot;' % en, 'class="sub">%s &middot;' % zh)  # with hand
    # zh journey: main GitHub links land on the Chinese README (deep links untouched)
    html_s = html_s.replace('href="https://github.com/rocsgh/ppt-zen">',
                            'href="https://github.com/rocsgh/ppt-zen/blob/master/README.zh-CN.md">')
    html_s = html_s.replace('href="https://github.com/rocsgh/ppt-zen#quick-start">',
                            'href="https://github.com/rocsgh/ppt-zen/blob/master/README.zh-CN.md#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B">')
    # method-term glosses on first-contact labels
    html_s = html_s.replace('>HEADLINE</span>', '>提纲 HEADLINE</span>')
    html_s = html_s.replace('>DETAIL</span>', '>细化 DETAIL</span>')
    return html_s

