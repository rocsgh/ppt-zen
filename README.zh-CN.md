<p align="center"><a href="README.md">English</a> · <b>简体中文</b></p>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/logo-wordmark-dark.png"><img src="assets/logo-wordmark.png" alt="PPT-Zen" width="420"/></picture></p>

<p align="center"><b>一句话，得到一部电影质感的全图 PPT。</b></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/judgment%20layer-Apache--2.0-blue.svg" alt="Apache-2.0"></a>
  <a href="LICENSE-STYLES"><img src="https://img.shields.io/badge/styles-CC--BY--4.0-lightgrey.svg" alt="CC-BY-4.0"></a>
  <a href="https://github.com/rocsgh/ppt-zen/stargazers"><img src="https://img.shields.io/github/stars/rocsgh/ppt-zen?style=social" alt="stars"></a>
</p>

<p align="center"><b>🖼 <a href="https://pptzen.xyz">在线画廊 →</a></b></p>

<p align="center">
  <img src="assets/hero-portolan.jpg" width="32%"/>
  <img src="assets/hero-nolan.jpg" width="32%"/>
  <img src="assets/hero-davinci.jpg" width="32%"/>
</p>

<p align="center"><i>同一句话——「做个 PPT」。三种材质，三个世界。<br/>上面三张就是它的真实输出，未经修饰。</i></p>

---

## 这是什么

PPT-Zen 是一个装进你 AI 助手里的**做 PPT 技能**（支持 Claude Code、Cursor、Codex 等七种运行时）。装上之后，你只说一句：

> 「用 ppt-zen 做一个关于 ⟨你的项目⟩ 的 10 页 PPT，航海图风格。」

然后你得到的，不是"模板 + 文字框"，而是十张**整页画出来的幻灯片**：每一页都是一幅完整的画——标题、数据、插画、纸纹长在同一张图里。看起来像电影截帧、像出版物内页，不像办公软件。

中间你**不用回答任何问题**：不选模板、不挑配色、不填"每页写什么"。每一页放多少内容、用什么构图、配什么插画，都由它自己判断（怎么判断的，见下文「它会思考」）。

## 为什么效果好

**1. 整页出图，不是模板贴字。**
市面上的 AI PPT 是"选个模板、往文字框里填字"——底子还是办公软件，一眼看出来。PPT-Zen 每一页由会画字的图像模型**一次画成**：背景质感、文字排印、插画、装饰边框是同一幅画的有机部分，光影和纹理贯穿整页。这是"设计师画了一页"和"软件排了一页"的差别。

**2. 45 种材质世界，整套统一得像一部片子。**
古航海图的羊皮纸与矿物水彩、达芬奇手稿的铁胆墨水、诺兰电影的冷峻光影、水墨的浓淡枯润、18 世纪建国文书的蜡封与花体字……[画廊](https://pptzen.xyz)里 45 种任选。材质**全片只选一次**，从封面到尾页都是同一个世界——翻十页，观众始终认得这是同一部作品，而不是十张风格漂移的图。

**3. 中文真实可读，不出"伪汉字"。**
全图 PPT 最常见的翻车是文字画糊。PPT-Zen 依赖会写字的图像模型（gpt-image 系），prompt 里写死每一处文字的确切字符，出图后**逐张质检、标题逐字校对**——伪汉字、自创字直接重出。中文楷书标题在羊皮纸上是真的楷书，不是像素浆糊。

**4. 每页有一件"画出来的论点"。**
讲公平，画一杆天平；讲流程自动化，画一台齿轮机器；讲"问一次纯属运气"，画墨点散开又收敛成一线。插画不是配图装饰，是**把这页的论点画成一个看得见的东西**——看着图就能猜出这页在说什么。这是普通模板永远给不了的一层。

## 它会思考：每一页都是它自己判断的

你不填任何表单，是因为这些决定它替你做了——**逐页做**：

| 它决定什么 | 怎么决定 |
|---|---|
| **这页放多少** | 一句话说得完的 → 大字留白、提纲挈领；必须并排看才明白的（对比、清单、证据）→ 摆开细化，可扫读 |
| **用什么构图** | 按页面职能自动派：章节金句 → 光带；证据对比 → 网格；封面 → 流线…… |
| **画什么插画** | 把这页的论点翻译成一件东西——最费脑、也最值钱的一步 |
| **全片什么材质** | 你点名就用你的；不点名它选一个，然后整套锁死 |

一条真实的判断链长这样：

```
这页是章节金句 → 一句话说得完 → 提纲挈领 → 构图派：光带 → 插画：一个词本身就是画面
这页是竞品证据 → 必须并置才成立 → 细化 → 构图派：网格 → 插画：小对勾与叉替代整句评语
       → 而且上一页是密的，所以这页之后自动接一页疏的，给观众喘息
```

这些规则不是拍脑袋——是几十套真实 deck（70 页的宣讲、57 页的产品分析、10 页的股权文书）一页一页磨出来的，每条规则背后都有一个真踩过的坑。完整推导（包括被我们推翻的旧模型）在 **[DESIGN.zh-CN.md](DESIGN.zh-CN.md)**。

## 从一句话到成片，中间发生了什么

1. **页面计划**：先产出 `plan.md`——每页的详略、构图、插画写成清单，这是它的"判断日志"，你可以在出图前改；
2. **选材质**：按你点名的（或它选的）材质，锁定全片的 prompt 配方；
3. **逐页出图**：每页一条自含的整页 prompt，交给图像模型画成 16:9 整图；
4. **质检**：逐张检查——伪汉字、错字、构图崩坏的页面单页重出（约 2 分钟一张，不用整套重来）；
5. **拼片**：`assemble_pptx.py` 把图拼成可直接放映的 `deck.pptx`。

> **如实说明：这是工具，不是许愿池。** 逐张质检、标题逐字校对这些"人类闸门"正是质量的来源——我们把它写在流程里，而不是吹"一键零缺陷"。

## 你会得到什么

- `slides/01.jpg … NN.jpg` —— 每页一张 16:9 整图
- `plan.md` —— 页面计划：每页是什么、为什么这么定
- `deck.pptx` —— 拼好的成片；PDF / Keynote / Google Slides 用同一批图导入即可

它**不是**一个托管按钮，是你的 agent 加载的一个技能 + 两个小脚本——所以它跑在你自己的模型和 key 上，引擎无关。

想先看一套再决定装不装？完整的 `deck.pptx` 和全部十张 JPG 都随仓库发布，就在 [`examples/`](examples/) 下——克隆下来直接打开，不需要任何 key。

## 快速开始

```bash
git clone https://github.com/rocsgh/ppt-zen
cd ppt-zen

# 1. 按你的运行时装技能（矩阵见下）
./install.sh                          # 先看看这台机器上装了哪些运行时
./install.sh auto                     # 一键装进探测到的每个运行时
./install.sh claude --global          # 或者指定一个：Claude Code -> ~/.claude/skills/ppt-zen/

# 2. 给它一个图像模型（agent 本身能生图就跳过，例如 Hermes）
cp .env.example .env                  # 把你的 key 填进 .env
python3 scripts/gen_image.py --check  # 体检：读配置 + 试生成一张图，跑长任务前先验证

# 3. 在你的 agent 里，一句话：
#    "用 ppt-zen 帮我做一个关于 <你的项目> 的 10 页 pitch，用航海图风格。"
#    -> 它先出页面计划（plan.md），再逐页把图生成到 slides/

# 4. 拼成图片型 .pptx（非 16:9 的图会居中裁切到 16:9）
pip install python-pptx
python3 scripts/assemble_pptx.py slides/ deck.pptx
```

### 安装矩阵——按运行时选

不确定自己装了什么？`./install.sh` 不带参数会探测本机（`PATH` 上的命令、`~/.<运行时>/` 目录、
或 `./.claude/` 这类项目标记），把每个探测到的运行时会装到哪打印出来；`./install.sh auto` 就按这份
探测结果一键安装——项目标记优先于全局位置，Cursor/Windsurf/Copilot 没有对应项目目录时直接跳过
（它们没有全局位置）。

| 运行时 | 命令 | 装到哪 | 触发方式 |
|---|---|---|---|
| **Claude Code** | `./install.sh claude [--global]` | `.claude/skills/ppt-zen/` | `/ppt-zen` 或直接说要做 deck |
| **OpenClaw** | `./install.sh openclaw [--global]` | `.openclaw/skills/ppt-zen/` | 直接说要做 deck |
| **Hermes** | `./install.sh hermes` | `~/.hermes/skills/creative/ppt-zen/`（或 `$HERMES_HOME`） | 直接说要做 deck |
| **Codex CLI** | `./install.sh codex [--global]` | `AGENTS.md` / `~/.codex/AGENTS.md` | 被动——自动读取 |
| **Cursor** | `./install.sh cursor` | `.cursor/rules/ppt-zen.mdc` | 被动——自动生效 |
| **Windsurf** | `./install.sh windsurf` | `.windsurf/rules/ppt-zen.md` | 被动——自动生效 |
| **GitHub Copilot** | `./install.sh copilot` | `.github/instructions/` | 被动——自动生效 |
| 全部 | `./install.sh all` | 以上全部 | — |
| 你实际装了的 | `./install.sh auto` | 本机探测到的每个运行时 | — |

技能安装是**自包含**的（SKILL.md + references + styles + scripts + examples + `styles.json` 机器可读风格索引 + `requirements.txt`）；
`AGENTS.md` 安装带幂等标记、重装原地更新。完整映射见 [`install/targets.json`](install/targets.json)；
被动运行时的文件由 `scripts/gen_adapters.py` 从 `AGENTS.md` 生成。

**Hermes 特别说明。** Hermes 没有项目级技能目录——它只扫 `$HERMES_HOME/skills`（默认 `~/.hermes/skills`）
和 `skills.external_dirs`，所以 `hermes` 一律装到那里，`--global` 不起作用。**装完必须重启 Hermes
网关/进程**——技能索引缓存在进程内，不重启就认不到。Hermes 自带的 `powerpoint` 技能（python-pptx
文本框式 deck）会继续共存；做设计过的整页出图 deck 时，以 ppt-zen 为准。

**完全没有 skill 系统？** 把 `SKILL.md` 整段贴进会话当上下文。
**依赖：** 辅助脚本纯标准库；只有 `assemble_pptx.py` 需要 `python-pptx`（自带 Pillow，用于 16:9 裁切）。

## 图像生成（自备模型）

PPT-Zen **不带任何图像模型**——这正是它引擎无关的原因。看你属于哪一半：

| 你的运行时 | 你要做什么 |
|---|---|
| **Claude Code · Codex · Cursor · Windsurf · Copilot** | 你需要一个图像 key——照下面 30 秒配好 `.env`。 |
| **Hermes**（或任何自带图像工具的 agent） | 什么都不用配，技能直接用 agent 已有的工具。 |

**自备 key。** 复制 ``.env.example`` 为 ``.env`` 填进去——任意 **OpenAI 兼容的图像接口**都行（OpenAI ``gpt-image``、中转、或兼容网关；只兼容 chat 的网关不算）：

```
IMAGE_API_BASE_URL=https://api.openai.com/v1
IMAGE_API_KEY=sk-...
IMAGE_MODEL=gpt-image-1
```

OpenAI、通用中转、火山方舟 / 豆包 Seedream 的模板可直接粘贴：[`references/providers.md`](references/providers.md)。然后：

```
python3 scripts/gen_image.py --check-config                 # 体检：只读配置，一个字节都不发
python3 scripts/gen_image.py --check                        # 再加一次真探测：真生成一张图、真计费
python3 scripts/gen_image.py "你的整页 prompt" out.jpg
```

> 会画字的模型（gpt-image 这类）对中文标题很关键——普通扩散模型会把字画糊。``.env`` 已被 gitignore，切勿提交 key。

### 卡在出图这一步？

`python3 scripts/gen_image.py --check` 是唯一要跑的命令：它会打印读到的 `.env`、遮掩后的 key，在你的端点上真生成一张图（探测前会先提示这一点；只想看配置就用 `--check-config`），并把失败翻译成人话：

| 结论 | 意思 |
|---|---|
| `no usable key` | 没有 `.env`，或 `IMAGE_API_KEY` 还是 `.env.example` 里的占位值。 |
| `HTTP 401 / 403` | key 不对、已过期，或这个端点上没有图像额度。 |
| `HTTP 404 / 405`，或返回的不是 JSON | 这个 base URL 根本没有实现图像接口——通常是只兼容 chat 的网关。 |
| `could not reach the endpoint` | 连不上、太慢或被拦：检查 `IMAGE_API_BASE_URL`、网络和代理。 |

长任务不再像卡死：脚本每页打印 `gen_image: requesting slides/03.jpg (attempt 1/3)`，5xx / 超时自己重试（4xx 绝不重试——那是配置问题，等也没用）。重试次数由 `IMAGE_MAX_ATTEMPTS` 控制（默认 3，取值限定 1–5）。中断后再跑会**续跑**：`slides/` 里已有的页直接跳过。

`--check` 会在你的端点上真生成一张图、真计费——它探测前会先说明这一点。只想看配置就用 `python3 scripts/gen_image.py --check-config`：同样的体检报告，一个字节都不发；`--help` 列出全部变量。

**没有 key，或今天不想配？** 照样让它做。你拿到的不是报错，而是一份判断包：`slides/PLAN.md`（每页的详略、器物、逐字文案，以及一段完整可粘贴的出图 prompt）、占位页、以及拼好的 `draft.pptx`。这份判断包就是一条命令——agent 会替你跑，你也可以自己跑：

```bash
python3 scripts/judgment_pack.py --init 10 --style portolan   # -> slides/PLAN.md 骨架
python3 scripts/judgment_pack.py slides                       # -> 占位页 + draft.pptx
```

把任意一段 prompt 交给你已有的出图工具（Midjourney、即梦、豆包…），把图放回 `slides/` 覆盖同名占位页，再跑一次第二条命令——已经有图的页不会被动。key 从此只是可选的最后一步。一份做完的判断包见 [`examples/relayboard/slides/PLAN.md`](examples/relayboard/slides/PLAN.md)。

## 从场景开始

45 种材质不知道点哪个？按你的场景取默认值，把这句话说出去：

| 场景 | 默认材质 | 你就这么说 |
|---|---|---|
| 融资 / 路演 | 航海图 Portolan | `「用航海图（Portolan）风格，给 <项目> 做一套 10 页 pitch。」` |
| 咨询 / 季度复盘 | 瑞士网格 Swiss Grid | `「用瑞士网格风格，给 <团队> 做一套 12 页 Q3 复盘。」` |
| 内部分享 | 活版报纸 Letterpress Broadsheet | `「用活版报纸风格，做一套 8 页 <主题> 内部分享。」` |

## 怎么选风格（唯一由你主导的事）

装好后，直接在对话里描述你要的 deck。**内容层面的判断全部自动**；你唯一能主导的是**材质 / 风格**：

- **让它自己选。** 什么都不说，它给全片选一个统一的材质。
- **点名一个风格。** 从[画廊](https://pptzen.xyz)挑一个，说它的名字：
  ```
  ……用航海图风格。
  ……电影，诺兰手笔。
  ……达芬奇铜版。
  ```
- **粗选或细选（介质 -> 手笔 -> 世界）。** 一个介质（"做成电影质感"）、一位大师手笔（"维伦纽瓦"）、或一整个世界——你想多细都行。

口诀：**材质全片选一次**（统一的观感）；而**插画**——每页*画什么*——逐页决定。

## 风格与画廊

在 **[GALLERY.md](GALLERY.md)** 翻每个风格——都带一条可复现的 prompt 配方。贡献你自己的：复制 `styles/_template/` 提 PR（见 **[CONTRIBUTING](CONTRIBUTING.md)**）。画廊从风格包自动生成，你的贡献自动出现。

## 想让它替你做？

判断层免费自助。帮你跑完整"出图 → 质检 → 拼片"流水线的托管版，另行推出。

## 文档

| | |
|---|---|
| 🖼 [在线画廊](https://pptzen.xyz) | 翻每个风格 + 它的 prompt 配方 |
| 🎨 [GALLERY.md](GALLERY.md) | 同一个画廊，仓库内 |
| 🏗️ [DESIGN.zh-CN.md](DESIGN.zh-CN.md) | 架构、由来、被推翻的模型 |
| 🤝 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) | 用一个文件夹贡献你的风格 |
| 🔒 [BOUNDARY.zh-CN.md](BOUNDARY.zh-CN.md) | 哪些开源、哪些私有 |

## 许可（两层）

- **判断层**（SKILL / 文档 / 代码）：**[Apache-2.0](LICENSE)**
- **风格包与画廊内容**（`styles/`、图片）：**[CC-BY-4.0](LICENSE-STYLES)**，贡献走 DCO

哪些开源、哪些私有：**[BOUNDARY.md](BOUNDARY.md)**。

## 受启发

本项目的设计判断**受** Garr Reynolds《演说之禅》(*Presentation Zen*) **启发**，与作者及出版方**无官方隶属关系**；文字皆为原创。
