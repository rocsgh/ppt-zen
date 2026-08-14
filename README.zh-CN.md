<p align="center"><a href="README.md">English</a> · <b>简体中文</b></p>

<h1 align="center">PPT-Zen</h1>

<p align="center"><b>一层让 AI 做幻灯片时"知道该怎么决定"的判断——不是又一个 PPT 生成器。</b></p>

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

<p align="center"><i>一句话进——「做个 PPT」。逐页判断、整页出图。<br/>同一句话，三个世界。</i></p>

---

**这个项目讲两件事：**
1. **一个会思考的 AI**，自己决定每一页*该怎么做*——你不用回答任何问题。
2. **效果真的好**——整页设计、有质感、中文不糊。（上面三张，更多看[画廊](GALLERY.md)。）

## 这是什么

市面上所有 AI PPT 工具都在解决同一件事：**怎么把内容变成页面**。PPT-Zen 开源的是没人做的那层：

> **这一页——该放多少、长什么样、凭什么这么定？**

**北极星：** 用户只说一句，其余全部由规则跑完——不问模板、不问配色、不问"每页写什么"。

## 它是一条判断链，不是功能清单

成品可复制——谁都能截图。每一页背后那条**判断链**抄不走：

```
这页是章节金句 → 一句话说得完 → 提纲挈领 → 骨架派：光带
这页是竞品证据 → 必须并置才成立 → 细化 → 骨架派：网格
       → 而且上一页是密的，所以这页之后接一页疏的
```

## 四根轴

| 轴 | 是什么 | 谁来定 |
|---|---|---|
| **详略** | 提纲挈领 ↔ 细化 | AI 逐页判 |
| **骨架** | 画面怎么被切分（网格/光带/流线/色域/对峙…可不派） | 按页面职能自动派 |
| **器物** | **这一页的论点，画成什么东西** | 逐页想——最值钱的一根 |
| **材质** | 用什么做的（水墨/铜版/铅笔…） | 全片选一次 |

详略的唯一判据：**这页是"一句话说得完"，还是"必须并置才成立"？** 因为**听觉是线性的，视觉是并置的。**

## 为什么这样设计

这不是理论——是**一夜做出 70 页真实 deck 逼出来的**，每一层都对应一个真踩的坑：

- **器物**：一张有质感的纸上摆个几何图还是空的——缺的那根轴是"这页画什么"。
- **手笔**（介质→手笔→世界）："电影质感"太笼统——诺兰和维伦纽瓦是同一介质、两只手。
- **流派体系**：为了不每次从头重造一个风格。

完整架构、推导、以及被我们推翻过的旧模型，都在 **[DESIGN.md](DESIGN.md)**。

## 如实写明人类闸门

> **注意——这是工具，不是许愿池。** 全图单页重出约 2 分钟、逐张截图质检、标题逐字校对。**这些人类闸门正是质量的来源**——我们如实写下来，而不是吹一键。

## 你会得到什么

PPT-Zen 判断并生成每一页；你最终拿到：

- `slides/01.jpg … NN.jpg` —— 每页一张整图、16:9 的幻灯片
- 一份简短的**页面计划** —— 每页是什么（提纲挈领 / 细化）+ 它的器物：判断日志
- `deck.pptx` —— 用 `scripts/assemble_pptx.py` 从这些图拼出来

它**不是**一个托管按钮。它是你的 agent 加载的一个技能 + 两个小脚本。拼成 `.pptx` 已内置；PDF / Keynote / Google Slides 用同一批满幅图导入即可。

## 快速开始

```bash
git clone https://github.com/rocsgh/ppt-zen
cd ppt-zen

# 1. 装技能（以 Claude Code 为例；或你 agent 的技能目录）
mkdir -p ~/.claude/skills/ppt-zen
cp SKILL.md ~/.claude/skills/ppt-zen/
cp -R references ~/.claude/skills/ppt-zen/

# 2. 给它一个图像模型（agent 本身能生图就跳过）
cp .env.example .env        # 然后把你的 key 填进 .env

# 3. 在你的 agent 里，一句话描述这份 deck：
#    "用 ppt-zen 帮我做一个关于 <你的项目> 的 10 页 pitch，用航海图风格。"
#    -> 它规划每一页，然后逐页把图生成到 slides/

# 4. 把这些图拼成一份真正的 .pptx
pip install python-pptx
python3 scripts/assemble_pptx.py slides/ deck.pptx
```

**不支持 skill 的 agent？** 把 `SKILL.md` 整段贴进会话当上下文。
**依赖：** `gen_image.py` 和构建脚本都是纯标准库；只有 `assemble_pptx.py` 需要 `python-pptx`。

## 图像生成（自备模型）

PPT-Zen **不带任何图像模型**——这正是它引擎无关的原因。你自己接，两条路任选：

- **你的 agent 本身能生图**（带图像工具的 Claude Code、Hermes 等）——什么都不用配，技能用 agent 现有的能力。
- **指向你自己的图像 API。** 复制 ``.env.example`` 为 ``.env`` 填入你的 key——任意 **OpenAI 兼容的图像接口**都行（OpenAI ``gpt-image``、中转、或兼容网关）：
  ```
  IMAGE_API_BASE_URL=https://api.openai.com/v1
  IMAGE_API_KEY=sk-...
  IMAGE_MODEL=gpt-image-1
  ```
  仓库自带的 ``scripts/gen_image.py`` 读 ``.env`` 出一页图：
  ```
  python3 scripts/gen_image.py "你的整页 prompt" out.jpg
  ```

> 会画字的模型（gpt-image 这类）对中文标题很关键——普通扩散模型会把字画糊。``.env`` 已被 gitignore，切勿提交 key。

## 使用 —— 怎么跑、怎么选材质/流派

装好后，直接在对话里描述你要的 deck：

```
用 ppt-zen 帮我做一个关于 <你的主题> 的 PPT。
```

这就是全部交互。**详略和骨架逐页自动定——你不用回答任何问题。** 你唯一能主导的是**材质 / 风格**：

- **让它自己选。** 什么都不说，它给全片选一个统一的材质。
- **点名一个风格。** 从[画廊](https://pptzen.xyz)挑一个，说它的名字：
  ```
  ……用航海图风格。
  ……电影，诺兰手笔。
  ……达芬奇铜版。
  ```
- **粗选或细选（介质 -> 手笔 -> 世界）。** 一个介质（"做成电影质感"）、一位大师手笔（"维伦纽瓦"）、或一整个世界——你想多细都行。

口诀：**材质全片选一次**（统一的观感）；而**器物**——每页*画什么*——逐页决定。

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
