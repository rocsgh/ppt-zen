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
 ("<title>Method · PPT-Zen</title>", "<title>原理 · PPT-Zen</title>"),
 ("<title>Example — a 10-page deck with its judgment log · PPT-Zen</title>", "<title>成片 — 十页与逐页判断日志 · PPT-Zen</title>"),
 # gallery <title>/og:title handled count-agnostically in ZH_COUNT_RE
 ("<title>Install · PPT-Zen</title>", "<title>上手 · PPT-Zen</title>"),
 # nav
 ('>Method</a>', '>原理</a>'),
 ('>Example</a>', '>成片</a>'),
 ('>Gallery</a>', '>风格库</a>'),
 ('>Install</a>', '>上手</a>'),
 # home section-05 heading + method-page inline link to the gallery (page references, not nav)
 ("<h2>Install</h2>", "<h2>上手</h2>"),
 (">gallery</a>", ">风格库</a>"),
 # home hero
 ("Open-source judgment layer &middot; Apache-2.0", "开源判断层 &middot; Apache-2.0"),
 ("One sentence in.<br/><em>Many worlds</em> out.", "一句话进。<br/><em>万千世界</em>出。"),
 ("Your agent decides how each page should be — density, device, material — then renders every slide as one designed image.",
  "你的 agent 自己决定每一页该怎么做——详略、器物、材质——然后把每一页渲染成一整张设计好的图。"),
 ('>Install</a><a class="btn" href="example.html">See a real deck</a>', '>上手</a><a class="btn" href="example.html">看一套真实成片</a>'),
 ("The same idea &mdash; pick a material. Each one is a different world.", "同一个想法 —— 选一种材质，就是另一个世界。"),
 # home "what it is" band
 ('<div class="kick">What it is</div>', '<div class="kick">这是什么</div>'),
 ("PPT-Zen is a taste skill you install into your AI agent. You say one sentence; it decides how much each page holds, what it looks like and in which material — then renders every page as one designed image and assembles the .pptx.",
  "PPT-Zen 是装进你 AI agent 里的一个审美技能。你说一句话，它决定每页放多少内容、长什么样、用什么材质——然后把每一页画成一整张设计图，拼装成 .pptx 交给你。"),
 ('<b>Install</b> — one command', '<b>装上</b>——一行命令'),
 ('<b>Say one sentence</b> in your agent', '<b>对你的 agent 说一句话</b>'),
 ('<b>Get the deck</b> — designed pages, assembled .pptx', '<b>拿到成片</b>——设计过的整页图，拼好的 .pptx'),
 # home claims
 ("It decides, you don't answer questions", "它来判断，你不用回答问题"),
 ("Per page it sets the density (headline vs. detail), picks the device — the argument drawn as a thing — and holds one material across the whole deck.",
  "它逐页决定详略（提纲挈领还是细化）、想出器物——把这页的论点画成一个东西——并且全片只用一种材质。"),
 ("Full-image pages that hold up", "整页出图，经得起看"),
 ("Every slide is one designed image — typography, texture and illustration in the material you chose. English and dense data render clean; you proofread each page, and a miss regenerates in one command.",
  "每一页都是一整张设计好的图——排印、质感、插画都长在你选的材质里。英文与密集数据渲染得干净；每页你都要校对一遍，出错的页一行命令单独重出。"),
 ("Open source, your image model", "开源，图像模型你自带"),
 ("Apache-2.0 judgment layer + CC-BY styles. Works with any agent that generates images, or any endpoint speaking the OpenAI images API. No key ships in the repo.",
  "判断层 Apache-2.0 + 风格 CC-BY。任何能生图的 agent，或任何实现 OpenAI 图像接口的端点都能用。仓库不带任何 key。"),
 # home sections
 ("Judgment, not generation", "判断，而不是生成"),
 ("Every AI PPT tool turns content into pages. PPT-Zen open-sources the part nobody else does: <b>for each page — how much should it hold, what should it look like, and on what grounds?</b> The finished deck is copyable; the chain of decisions is not.",
  "所有 AI PPT 工具都在做同一件事：把内容变成页面。PPT-Zen 开源的是没人做的那一层：<b>这一页——该放多少、长什么样、凭什么这么定？</b>成品谁都能截图；判断链抄不走。"),
 ("Read the method &rarr;", "看原理 &rarr;"),
 ("How it works", "怎么用"),
 ("You bring an agent and an image model. The skill brings the judgment.", "你带一个 agent 和一个图像模型，判断由这个 skill 提供。"),
 ("Install the skill</b><p>One command per runtime — Claude Code, Codex, Cursor, Windsurf, Hermes, OpenClaw.</p>",
  "装技能</b><p>每个运行时一行命令——Claude Code、Codex、Cursor、Windsurf、Hermes、OpenClaw。</p>"),
 ("./install.sh auto   # detects your runtimes; or: claude / hermes / ... --global",
  "./install.sh auto   # 探测你装了哪些运行时；或指定：claude / hermes / ... --global"),
 # command stays a command; only the trailing comment is Chinese (matches the home page)
 ("./install.sh auto                 # detects your runtimes; matrix below for one-by-one",
  "./install.sh auto                 # 探测你装了哪些运行时；想逐个装看下面的矩阵"),
 ("Say one sentence</b><p>In your agent:</p>", "说一句话</b><p>在你的 agent 里：</p>"),
 # the ask itself — Chinese is a first-class input to the skill, so these are real commands
 ('<pre>"Make me a 10-page pitch deck\n about &lt;project&gt;, Portolan style."</pre>',
  '<pre>「用航海图（Portolan）风格，\n 给〈你的项目〉做一套 10 页 pitch。」</pre>'),
 ("Get the deck</b><p>Plan &rarr; one image per page &rarr; proofread &rarr; assembled .pptx.</p>",
  "拿到成片</b><p>计划 &rarr; 逐页出图 &rarr; 校对 &rarr; 拼装 .pptx。</p>"),
 ("Proof — a full deck, judged page by page", "证据 —— 一整套片子，逐页判断"),
 ("Relayboard: a fictional 10-page pitch generated from one sentence, told as a voyage across a 16th-century sea chart &mdash; with the judgment log for every page.",
  "Relayboard：一个虚构产品的 10 页 pitch，由一句话生成，讲成一场 16 世纪航海图上的远航 —— 每一页都附判断日志。"),
 ("Relayboard: a fictional 10-page pitch generated from one sentence, in one material — with the judgment log for every page.",
  "Relayboard：一个虚构产品的 10 页 pitch，由一句话生成、一种材质贯穿 —— 每一页都附判断日志。"),
 ("See all 10 pages + the judgment log &rarr;", "看全部 10 页 + 判断日志 &rarr;"),
 # "NN materials, one line each" handled in ZH_COUNT_RE
 ("Every style ships a reproducible prompt formula. Contribute your own with a folder and a PR.",
  "每个风格都带一条可复现的 prompt 配方。想贡献自己的？一个文件夹、一个 PR。"),
 # "Browse all NN styles" handled in ZH_COUNT_RE
 ("One command per runtime. The repo is the product — the site just shows you around.",
  "每个运行时一行命令。仓库才是产品——官网只是带你逛逛。"),
 ("Full install matrix", "完整安装矩阵"),
 ("Open GitHub", "打开 GitHub"),
 # example page
 ("Worked example &middot; fictional product, invented demo numbers", "完整成片 &middot; 虚构产品，数字为演示内容"),
 ("Relayboard —<br/>ten pages, one sentence.", "Relayboard ——<br/>十页，一句话。"),
 ("<b>In:</b> \"Make me a 10-page pitch deck for Relayboard, an async-standup tool, in the Portolan sea-chart style.\"",
  "<b>输入：</b>「用航海图（Portolan）风格，给异步站会工具 Relayboard 做一套 10 页 pitch。」"),
 ("<b>Out:</b> the pages below — a growth story told as a voyage across a 16th-century chart.",
  "<b>输出：</b>下面这些页——一个增长故事，讲成 16 世纪海图上的一场远航。"),
 ("The labels are the judgment log, the part you can't screenshot. Notice the rhythm: headline &rarr; a dense\nevidence block &rarr; one line to land on. Every number is rendered inside the image and comes out clean.",
  "旁边的标签就是判断日志——截图截不走的那部分。注意节奏：提纲挈领 &rarr; 密集证据块 &rarr; 一句话收尾。所有数字都渲染在图里，个个清晰。"),
 # longer (home) first: the example-page pair below is a prefix of it
 ("The finished <code>deck.pptx</code> and all ten JPGs ship in the repo under <code>examples/</code> — clone and open them, no key needed.",
  "完整的 <code>deck.pptx</code> 和全部十张 JPG 都随仓库发布，就在 <code>examples/</code> 下——克隆下来直接打开，不需要任何 key。"),
 ("The finished <code>deck.pptx</code> and all ten JPGs ship in ", "完整的 <code>deck.pptx</code> 和全部十张 JPG 都随仓库发布，见 "),
 ("examples/</a> &mdash; clone the repo and open them, no key needed.", "examples/</a> —— 克隆下来直接打开，不需要任何 key。"),
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
 # "NN styles · every card ships..." handled in ZH_COUNT_RE
 ("The material library.", "材质库。"),
 ("Material swatches show the same line — <i>Signal over noise</i> — so the surface is the only variable. Cinema hands show one sentence through different eyes. Click any card for the full recipe.",
  "材质样张统一用同一句话——<i>Signal over noise</i>——材质因此成为唯一变量。电影手笔组则是同一句话经过不同导演之眼。点任何一张卡看完整配方。"),
 ("Start from a scenario", "从场景开始"),
 ("<tr><th>Scenario</th><th>Default material</th><th>What you say</th></tr>",
  "<tr><th>场景</th><th>默认材质</th><th>你就这么说</th></tr>"),
 ("<tr><td>Fundraise / pitch</td><td>Portolan Sea Chart</td><td><code>\"Make me a 10-page pitch deck about &lt;project&gt;, Portolan style.\"</code></td></tr>",
  "<tr><td>融资 / 路演</td><td>航海图 Portolan</td><td><code>「用航海图（Portolan）风格，给〈项目〉做一套 10 页 pitch。」</code></td></tr>"),
 ("<tr><td>Consulting / quarterly review</td><td>Swiss Grid</td><td><code>\"Make me a 12-page Q3 review for &lt;team&gt;, Swiss Grid style.\"</code></td></tr>",
  "<tr><td>咨询 / 季度复盘</td><td>瑞士网格 Swiss Grid</td><td><code>「用瑞士网格风格，给〈团队〉做一套 12 页 Q3 复盘。」</code></td></tr>"),
 ("<tr><td>Internal share</td><td>Letterpress Broadsheet</td><td><code>\"Make me an 8-page internal share about &lt;topic&gt;, Letterpress Broadsheet style.\"</code></td></tr>",
  "<tr><td>内部分享</td><td>活版报纸 Letterpress Broadsheet</td><td><code>「用活版报纸风格，做一套 8 页〈主题〉内部分享。」</code></td></tr>"),
 ("Contribute a style — one folder, one PR &rarr;", "贡献一个风格——一个文件夹、一个 PR &rarr;"),
 (">All</button>", ">全部</button>"),
 ("View details &rarr;", "看详情 &rarr;"),
 # install page
 ("One command,<br/>your runtime.", "一行命令，<br/>装进你的运行时。"),
 ("Get the repo, install the skill", "拿仓库、装技能"),
 ("<th>Runtime</th><th>Command</th><th>Installs to</th><th>Trigger</th>", "<th>运行时</th><th>命令</th><th>装到哪</th><th>触发方式</th>"),
 ("<code>/ppt-zen</code> or just ask for a deck", "<code>/ppt-zen</code>，或直接说要做 deck"),
 ("<td>ask for a deck</td>", "<td>直接说要做 deck</td>"),
 ("passive — auto-read", "被动——自动读取"),
 ("passive — auto-applied", "被动——自动生效"),
 ("<td>everything</td>", "<td>全部</td>"),
 ("<td>all of the above</td>", "<td>以上全部</td>"),
 ("<tr><td>auto</td><td><code>./install.sh auto</code></td><td>every runtime detected on this machine</td><td>—</td></tr>",
  "<tr><td>自动探测</td><td><code>./install.sh auto</code></td><td>本机探测到的每个运行时</td><td>—</td></tr>"),
 ("<b>Project-level rows install into the current directory</b> — Codex, Cursor, Windsurf and Copilot all write beside whatever project you are standing in, so run the installer <i>from your project</i>, not from inside the clone: <code>cd my-project &amp;&amp; /path/to/ppt-zen/install.sh codex</code>. It rewrites the skill's file references to absolute paths so they still resolve from over there.",
  "<b>项目级的那几行装在「当前目录」</b>——Codex、Cursor、Windsurf、Copilot 都是往你此刻所在的项目里写，所以要<i>在你的项目里</i>跑安装脚本，而不是在克隆下来的仓库里跑：<code>cd my-project &amp;&amp; /path/to/ppt-zen/install.sh codex</code>。脚本会把技能里引用的文件路径改写成绝对路径，换个目录也照样能找到。"),
 ("Skill installs are self-contained (SKILL.md + references + styles + scripts + examples + <code>styles.json</code> + <code>requirements.txt</code>). No skill system at all? Paste <code>SKILL.md</code> into the session as context.",
  "技能安装是自包含的（SKILL.md + references + styles + scripts + examples + <code>styles.json</code> + <code>requirements.txt</code>）。完全没有 skill 系统？把 <code>SKILL.md</code> 整段贴进会话当上下文即可。"),
 ("<b>Hermes:</b> there is no project-level skill directory — the installer always writes to <code>$HERMES_HOME/skills</code> (default <code>~/.hermes/skills</code>), so <code>--global</code> is a no-op. Restart your Hermes gateway/process afterwards: the skill index is cached in-process. Hermes&rsquo; builtin <code>powerpoint</code> skill (text-box decks) keeps working alongside it; for designed full-image decks ppt-zen supersedes it.",
  "<b>Hermes：</b>它没有项目级技能目录——安装脚本一律写入 <code>$HERMES_HOME/skills</code>（默认 <code>~/.hermes/skills</code>），<code>--global</code> 不起作用。装完请重启 Hermes 网关/进程：技能索引缓存在进程内。Hermes 自带的 <code>powerpoint</code> 技能（文本框式 deck）会继续共存；做设计过的整页出图 deck 时，以 ppt-zen 为准。"),
 ("Wire an image model", "接上图像模型"),
 ("Every page is a generated image, and PPT-Zen ships none. Which half applies to you:",
  "每一页都是生成的图，而 PPT-Zen 不带图像模型。看你属于哪一半："),
 ("<tr><th>Your runtime</th><th>What you do</th></tr>", "<tr><th>你的运行时</th><th>你要做什么</th></tr>"),
 ("<td>You need an image key — the 30-second <code>.env</code> setup below.</td>",
  "<td>你需要一个图像 key——照下面 30 秒配好 <code>.env</code>。</td>"),
 ("<tr><td><b>Hermes</b> (or any agent with its own image tool)</td><td>Nothing to configure. The skill uses the tool the agent already has.</td></tr>",
  "<tr><td><b>Hermes</b>（或任何自带图像工具的 agent）</td><td>什么都不用配，skill 直接用 agent 已有的工具。</td></tr>"),
 ("<tr><td><b>Already export <code>OPENAI_API_KEY</code>?</b></td><td>Nothing to configure either — the helper reuses it silently.</td></tr>",
  "<tr><td><b>已经 export 过 <code>OPENAI_API_KEY</code>？</b></td><td>也什么都不用配——脚本会自动复用它。</td></tr>"),
 ("Bring your own key: <b>any endpoint that implements the OpenAI <code>/images/generations</code> API</b> (accepts <code>{model, prompt, size, n}</code>, returns <code>b64_json</code> or <code>url</code> — chat-only \"compatible\" gateways don't count):",
  "自备 key：<b>实现了 OpenAI <code>/images/generations</code> 接口的任意端点</b>都行（接受 <code>{model, prompt, size, n}</code>、返回 <code>b64_json</code> 或 <code>url</code>——只兼容 chat 的\"兼容\"网关不算）："),
 ("python3 scripts/gen_image.py --check  # doctor: reads your config, generates one test image",
  "python3 scripts/gen_image.py --check  # 体检：读你的配置，试生成一张图"),
 ("<code>--check</code> is the support story: it masks your key, probes the endpoint, and turns whatever went wrong into one plain verdict with the fix — bad key, chat-only gateway, unreachable host. Ready-to-paste <code>.env</code> blocks for OpenAI, generic relays and 火山方舟 / 豆包 Seedream:",
  "<code>--check</code> 就是全部的排障入口：它遮掉你的 key、探一次端点，把任何失败翻译成一句人话结论 + 怎么修——key 不对、只兼容 chat 的网关、连不上。OpenAI、通用中转、火山方舟 / 豆包 Seedream 的 <code>.env</code> 模板可直接粘贴："),
 ("providers.md</a>.</p>", "providers.md</a>。</p>"),
 ("PPT-Zen ships <b>no key and no model</b> — the judgment is open source, the pixels are yours. A hosted trial that skips this step is coming.",
  "PPT-Zen <b>不带任何 key、不绑定任何模型</b>——判断是开源的，像素是你自己的。省掉这一步的托管版试用，正在做。"),
 ("<b>No key today?</b> Ask for the deck anyway. You get the judgment pack: the per-page plan with a ready-to-paste prompt for every page, placeholder pages, and an assembled <code>draft.pptx</code>. Paste any prompt into an image tool you already have, drop the result into <code>slides/</code>, reassemble. The key becomes an optional last step.",
  "<b>今天没有 key？</b>照样让它做。你会拿到一份判断包：逐页计划 + 每页一段可直接粘贴的 prompt、占位页、以及拼好的 <code>draft.pptx</code>。把任意一段 prompt 贴进你已有的出图工具，把图放回 <code>slides/</code>，重拼一次即可。key 从此只是可选的最后一步。"),
 ("Make a deck — what you actually say", "做一套片——你实际要说的话"),
 ("Open your agent in any project and talk. One sentence starts it; the skill decides the rest and never quizzes you about layout:",
  "在任何项目里打开你的 agent，直接说话。一句话就能开始；剩下的它来判断，绝不会反问你版式问题："),
 ("The agent writes <code>plan.md</code> (page &middot; density &middot; device &middot; exact text &middot; style) — review it if you like — then generates one image per page into <code>slides/</code>. Iterate by pointing at pages:",
  "agent 会先写 <code>plan.md</code>（页 &middot; 详略 &middot; 器物 &middot; 逐字文案 &middot; 风格）——想过目就过目——然后逐页出图到 <code>slides/</code>。之后对着页迭代："),
 ("<b>Feed it your facts.</b> Attach an outline / metrics / links — real numbers land on the slides; anything missing shows as <code>[TO CONFIRM]</code> rather than an invented figure. When the pages read clean:",
  "<b>把真实数据喂给它。</b>附上提纲 / 指标 / 链接——真数字会上片；缺的只会显示 <code>[TO CONFIRM]</code> 占位，绝不编造。页面都校对干净之后："),
 # the two ask blocks: whole <pre> swapped so the examples are Chinese sentences you can paste as-is
 ('<pre>"Make me a 10-page pitch deck about &lt;your project&gt; with ppt-zen, in the Portolan style."\n'
  '"Design a keynote about our Q3 results — pick a material that fits."   <span style="color:#8f8d97"># it chooses</span>\n'
  '"One slide only: \'23 minutes to refocus\', make it land."               <span style="color:#8f8d97"># single page</span></pre>',
  '<pre>「用航海图（Portolan）风格，给〈你的项目〉做一套 10 页 pitch。」\n'
  '「把我们 Q3 业绩做成一套 keynote——材质你来选。」                <span style="color:#8f8d97">＃ 材质它自己选</span>\n'
  '「就一页：『23 分钟才能重新专注』，把它做得掷地有声。」           <span style="color:#8f8d97">＃ 单页也行</span></pre>'),
 ('<pre>"Regenerate page 6 — the numbers feel cramped."\n'
  '"Swap the whole deck to the Kintsugi material."      <span style="color:#8f8d97"># same plan, new world</span>\n'
  '"Page 4\'s device isn\'t readable, try a funnel."</pre>',
  '<pre>「第 6 页重出——数字挤在一起了。」\n'
  '「整套片换成金缮（Kintsugi）材质。」        <span style="color:#8f8d97">＃ 同一计划，换个世界</span>\n'
  '「第 4 页的器物看不明白，换成漏斗试试。」</pre>'),
 ("Which image models work?", "哪些图像模型能用？"),
 ("Anything behind an OpenAI-compatible <code>/images/generations</code> route — OpenAI's gpt-image models, relays, gateways. The gallery samples were generated with gpt-image class models at 1536&times;1024. Non-16:9 output is center cover-cropped at assembly, so prompts keep key content clear of the top/bottom ~8%.",
  "任何走 OpenAI 兼容 <code>/images/generations</code> 路由的——OpenAI 的 gpt-image 系、各类中转、网关。风格库里的样张用 gpt-image 级模型在 1536&times;1024 生成。非 16:9 的输出会在拼装时居中裁切，所以 prompt 会让关键内容避开上下约 8%。"),
 ("Is the .pptx editable?", "拼出来的 .pptx 能编辑吗？"),
 ("It's image-based: each slide is one full-bleed image. Present it, export PDF, or import into Keynote/Google Slides — but text isn't editable. Fixing a typo means regenerating that one page (the skill supports single-page regeneration).",
  "它是图片型的：每页一整张满幅图。放映、导 PDF、导入 Keynote/Google Slides 都行——但文字不可编辑。改错字 = 重出那一页（skill 支持单页重出）。"),
 ("Will it invent numbers for my deck?", "它会替我编数字吗？"),
 ("No — that's a hard rule. Facts come from your input; anything missing becomes a visible <code>[TO CONFIRM]</code> placeholder. The skill decides form, never facts.",
  "不会——这是硬规则。事实只来自你的输入；缺的会显示成 <code>[TO CONFIRM]</code> 占位。skill 只定版式，绝不编事实。"),
 ("Can I add my own style?", "我能加自己的风格吗？"),
 ("Yes — copy <code>styles/_template/</code>, fill in the STYLE.md (material recipe + a sample), open a PR. The gallery and <code>styles.json</code> regenerate automatically. Styles are CC-BY-4.0, contributions via DCO.",
  "能——复制 <code>styles/_template/</code>，填好 STYLE.md（材质配方 + 一张样张），提 PR。风格库和 <code>styles.json</code> 自动重建。风格是 CC-BY-4.0，贡献走 DCO。"),
 ("What does it cost to run?", "跑一次要花多少钱？"),
 ("Whatever your image endpoint charges — a 10-page deck is 10 images plus any single-page retries. Order of magnitude (OpenAI gpt-image list prices, mid-2026): roughly $0.06–0.25 per 1536&times;1024 image depending on quality tier, so a first pass is about $1–3; budget 20–40 minutes including proofreading. Check your own endpoint's pricing.",
  "取决于你的图像端点收费——10 页 = 10 张图，外加你选择的单页重试。量级参考（OpenAI gpt-image 官方价，2026 年中）：1536&times;1024 每张约 $0.06–0.25（看质量档），首轮 10 页约 $1–3；含逐页校对预留 20–40 分钟。以你自己端点的价格为准。"),
 ("See a finished deck first", "先看一套成片"),
 # method page
 (">The method<", ">原理<"),
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


def inject_en_detail(html_s, page):
    """EN detail page: hreflang + auto-detect + switcher to its zh sibling."""
    html_s = html_s.replace("</head>", hreflang(page) + "</head>", 1)
    html_s = html_s.replace("<body>", "<body>" + DETECT.replace("%PAGE%", page), 1)
    sw = '<a class="btn" href="/zh/%s" onclick="%s">中文</a>' % (page, SWITCH_JS % "zh")
    return html_s.replace(GHBTN, sw + GHBTN, 1)


def make_zh(html_s, page):
    """Translate a built EN marketing page into its /zh/ sibling."""
    for en, zh in ZH:
        html_s = html_s.replace(en, zh)
    # asset + canonical/og paths
    html_s = html_s.replace('src="img/', 'src="../img/')
    html_s = html_s.replace('data-img="img/', 'data-img="../img/')
    html_s = html_s.replace('href="%s/%s">' % (BASE_URL, page), 'href="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('content="%s/%s">' % (BASE_URL, page), 'content="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    # detail-page links stay in /zh/ — every style has a zh sibling now
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
 "Manuscript": "手稿", "Paper craft": "纸艺", "Portolan chart": "航海图", "Print": "版画",
 "Technical": "技术制图", "Textile": "织物", "Woodblock": "木刻",
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
 ('class="kick">Install<', 'class="kick">上手<'),
]

# count-agnostic strings — the style count changes as packs are contributed
ZH_COUNT_RE = [
 (r"Gallery — (\d+) styles · PPT-Zen", r"风格库 — \1 个风格 · PPT-Zen"),
 (r"(\d+) styles &middot; every card ships a reproducible prompt formula", r"\1 个风格 &middot; 每张卡都带可复现配方"),
 (r"(\d+) materials, one line each", r"\1 个风格，每个都带配方"),
 (r"Browse all (\d+) styles &rarr;", r"浏览全部 \1 个风格 &rarr;"),
]

_orig_make_zh = make_zh
def make_zh(html_s, page):  # noqa: F811 — extend the base translator
    html_s = _orig_make_zh(html_s, page)
    for pat, rep in ZH_COUNT_RE:
        html_s = re.sub(pat, rep, html_s)
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
    # style display names: home material switcher + gallery card titles
    for en_name, zh_name in i18n_zh_styles.NAME_ZH.values():
        esc = _html.escape(en_name)
        html_s = html_s.replace(">%s</button>" % esc, ">%s</button>" % zh_name)
        html_s = html_s.replace(
            '<div class="nm">%s</div>' % esc,
            '<div class="nm">%s <span style="color:var(--ink2);font-weight:400;font-size:.85em">%s</span></div>'
            % (zh_name, esc))
    return html_s


# ---------------- style detail pages ----------------
import html as _html  # noqa: E402
import i18n_zh_styles  # noqa: E402

_detail_text_used = set()


def make_zh_detail(html_s, page):
    """Translate a built EN style-detail page into its /zh/ sibling.
    Prompt formulas stay English on purpose — they are the reproducible input."""
    slug = page[:-len(".html")]
    for en, zh in i18n_zh_styles.TEXT_ZH:
        if en in html_s:
            _detail_text_used.add(en)
            html_s = html_s.replace(en, zh)
    for en, zh in i18n_zh_styles.DETAIL_CHROME_ZH + i18n_zh_styles.DETAIL_COMMON_ZH:
        html_s = html_s.replace(en, zh)
    # display name: <title>/og:title + h1 (EN name kept as the product name)
    names = i18n_zh_styles.NAME_ZH.get(slug)
    if names:
        en_name, zh_name = names
        esc = _html.escape(en_name)
        html_s = html_s.replace("%s · PPT-Zen" % esc, "%s · PPT-Zen" % zh_name)
        html_s = html_s.replace(
            "<h1>%s</h1>" % esc,
            '<h1>%s <span style="font-size:.55em;color:var(--ink2);font-weight:400">%s</span></h1>'
            % (zh_name, esc))
    # medium: chip + meta-description prefix
    for en, zh in MEDIUM_ZH.items():
        esc = _html.escape(en)
        html_s = html_s.replace('<span class="chip">%s</span>' % esc,
                                '<span class="chip">%s</span>' % zh)
        html_s = html_s.replace('content="%s 材质配方' % esc, 'content="%s材质配方' % zh)
    # asset + canonical/og paths
    html_s = html_s.replace('src="img/', 'src="../img/')
    html_s = html_s.replace('href="%s/%s">' % (BASE_URL, page), 'href="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('content="%s/%s">' % (BASE_URL, page), 'content="%s/zh/%s">' % (BASE_URL, page))
    html_s = html_s.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    # hreflang + detect + switcher back to EN
    html_s = html_s.replace("</head>", hreflang(page) + "</head>", 1)
    html_s = html_s.replace("<body>", "<body>" + DETECT.replace("%PAGE%", page), 1)
    sw = '<a class="btn" href="/%s" onclick="%s">EN</a>' % (page, SWITCH_JS % "en")
    return html_s.replace(GHBTN, sw + GHBTN, 1)


def unused_detail_pairs():
    """EN strings from TEXT_ZH that matched no page — content drifted, fix the pair."""
    return [en for en, _ in i18n_zh_styles.TEXT_ZH if en not in _detail_text_used]

