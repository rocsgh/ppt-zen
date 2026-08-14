# deck-modes · 密度 × 材质 两轴模型（怎么调用 + 活模板）

> **何时读我**：用户说"走留白 / 走密集"、"用某某材质/母版"、"Maya 那种"，或做全图 deck 拿不准密度/材质时。这是把成品风格拆成**两条正交的轴**，各自可独立选，别把它们混成一个。

## ⚠️ 核心：两轴正交，别混

早期我把"A=留白 / B=密集手绘"并列——**错在把密度和材质塞进一个轴**。正解是两条独立的轴，任意组合：

**轴一 · 密度（布局哲学 = Ⓐ/Ⓑ）**
- **留白**（Ⓐ 有人讲）：一张一义、大字少字、八分饱偏空，幻灯片是背景。
- **密集**（Ⓑ 发出去自己看）：一页讲透一件事、主角+卫星、信息足但分层。

**轴二 · 材质（32 母版风格库，与密度无关）**
侘寂纸墨 / 达芬奇铜版 / 铅笔手绘 / 青花瓷 / 缂丝蜀锦 / 拓片石雕 / 氰版蓝晒 / 瓷白靛青……**任一材质都能配任一密度**。材质配方（选型四判据 + 同族区别写死）见 `全图PPT出图与风格库.md`（32 母版正本）。

**组合即风格**：`密度 × 材质`。
- 侘寂 GEO 演讲 = **留白 × 侘寂纸墨**
- 达芬奇 GEO 演讲 = **留白 × 达芬奇铜版**
- Maya 那套 = **密集 × 铅笔手绘**
- （想要什么就组）密集 × 青花瓷、留白 × 拓片……都成立。

**调用**：先报密度（留白/密集），再报材质（母版名）。只报一个就问另一个，或按 Ⓐ/Ⓑ + 主题默认。判不准密度→默认密集（宁密勿空，但密要守设计地板）。

---

## 轴一 · 密度模板

### 留白（Ⓐ）
每页：大标题（三分线，不居中）+ 一行副题 + 可选一行静句；**一个**签名意象，其余全空。文字＝VERBATIM 全部，一字不多。密度 low by design（八分饱偏空）。样板成品 `aisou-geo-deck` / `geo-keynote-2026`。

### 密集（Ⓑ）
一页一职能，主角锚点 + 卫星小场景，信息足但**严格分三层**（标题/副题/caption）。常见几种密集布局（按内容选，与材质无关）：
- **叙事插画型**（Maya 同款）：中心人物/主场景（~40–55%）+ 3–6 个真实世界卫星小场景，**用飘逸连线/藤蔓串起**，绶带横幅放标题+页脚金句，可选人物名片胶囊 + 工具/信源行。signature=连线串场景。
- **信息图型**：分区面板/网格，每格一子论点，结论式小标题 + 直接标注。
- **注解图解型**：一张主图（机器/流程/地图）+ 多处引线注解。

**密集纪律（密≠乱）**：主角压得住场（明度/尺寸对比拉开）；背景/远景压淡；卫星/面板限量（≤6）；连线或对齐引导视线而非填满；主角四周留呼吸区；八分饱上限。审图问"删掉哪个卫星核心不弱？弱＝装饰，删"。样板成品 `maya-geo-zh`。

---

## 轴二 · 材质母版（配任一密度）

材质＝怎么被"画/刻/织/烧"出来。选型四判据、32 母版清单、同族必须写死的区别（景泰蓝↔搪瓷 / 青花↔瓷白靛青 / 缂丝↔蜀锦 / 蜡染↔氰版 / 拓片↔石雕）见 `全图PPT出图与风格库.md`。两个已跑熟的 STYLE 母版直接可用：

**侘寂纸墨**（留白常配，亦可密集）
```
STYLE: Japanese wabi-sabi. Aged off-white handmade paper (washi/raw linen) filling the frame,
visible fibre grain, subtle mottling, one faint water-stain — imperfect, natural, never flat or
glossy. NO gradients/glow/3D/plastic sheen. Warm charcoal-grey sumi ink, brush-influenced. ONLY
accent = vermilion (朱砂), sparing — one seal / one underline / one dot, never filled. ASYMMETRIC
on rule-of-thirds. One restrained dry-brush sumi element. Mood: scholar's quiet studio.
```
（达芬奇铜版＝同族换皮：accent 靛蓝、纸换羊皮、笔触换铜版刻线、边角加机械/镜像手稿。）

**铅笔手绘**（Maya 同款材质，密集常配，亦可留白）
```
STYLE: Warm hand-drawn pencil-and-light-ink illustration on aged cream/ivory sketchbook paper,
soft graphite shading, gentle sepia — like a page from a warm illustrated notebook (手账); never
flat vector, never photographic, never glossy. Monochrome warm sepia/graphite; ONE single accent
colour on exactly one word or one small dot (e.g. one character soft blue, or a small green
"online" dot), never on areas. Hand-lettered signature in a corner.
```

其余 30 个母版（青花/缂丝/拓片/氰版/瓷白靛青…）从风格库正本取配方，写进 STYLE 段即可。

---

## 出厂三步（任一组合通用）
大纲（每页一职能）→ 每页自含 prompt（**密度布局配方 + 材质 STYLE 母版 + 逐字中文**）→ 批量出图 3 并发 + 逐张 Read 质检（伪汉字/结构词泄漏/VERBATIM 逐字/三等分/面孔朝内/密度分层）。

**全图四硬规则始终守**：密度分层 · 禁自创中文（NEVER invent additional Chinese characters）· 结构词抑制 · 中文写死字数。
