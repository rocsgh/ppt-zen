# Design & architecture · 设计与架构

The origin, the reasoning, and the models we overturned. This is the part you can't screenshot.
由来、推导、以及被我们推翻过的模型。这是抄不走的那部分。

*(EN + 中文.)*

---

## Where it came from · 由来

None of this is armchair theory. It was **forced out by making real, 70-page, full-image decks overnight**, repeatedly. Every rule below has a scar behind it. When a rule and the practice disagreed, the practice won — including some of our own earlier models (see *Overturned* at the bottom).

这套东西不是纸上推的，是**一次次一夜做出 70 页整图 deck 逼出来的**。下面每条规则背后都有一次踩坑。规则和实践打架时，实践赢——包括我们自己早期的模型（见文末"被推翻的"）。

## Step 0 — one knob decides how much a page holds · 第零步：一根旋钮定详略

Before anything else, each page gets one判断:

> **Is this page sayable in a line (→ headline), or does it only hold up when several things sit side by side (→ detail)?**

Because **hearing is linear, seeing is simultaneous.** A headline page obeys presentation-zen restraint; a detail page obeys information-design density. Two automatic follow-ons: an *evidence* page must be detail (evidence you can't see doesn't count), and a detail page is followed by a page that breathes.

听觉是线性的，视觉是并置的。提纲挈领页归"演说之禅"，细化页归"信息设计"。两条自动规则：证据页必须细化；细化页后面接一页疏的。

## The four axes · 四根轴

**Density × Skeleton × Device × Material.** Independent — don't mix them.

- **Density** — headline ↔ detail (Step 0). Per page, decided by the AI.
- **Skeleton** — how the frame is cut (grid / light-band / flowline / color-field / standoff… or none). Auto-assigned by page role, not asked.
- **Device — the argument of this page, drawn as a thing.** This is the axis everyone drops. Material decides *what it's made of*, skeleton decides *how it's cut* — neither decides *what it draws*. That gap is the device: a scale → a ruler; "one try is just luck" → a point-cloud scattering then converging to a line; "your customer before they meet you" → a raised hand. Two gates: it must *tie to the argument* (not a pretty thing that merely rhymes with the topic) **and** *grab attention* (not sitting quietly in a corner as decoration). Self-check: looking at it, can you guess what the page says?
- **Material** — the surface (ink wash / copperplate / pencil…). Chosen once for the whole deck; the only axis the user might weigh in on.

**器物**是最容易被漏的一根：材质管"用什么笔触"，骨架管"画面怎么切"，都不管"画什么"。器物＝这页的论点画成什么东西。两道闸：紧扣主题 + 抓住注意。自查：看着它能不能猜出这页在说什么。

### Illustration is a level, not on/off (L0–L4) · 插画是量级
L0 none · L1 margin study (material credibility only) · L2 typography-as-illustration · L3 spot device (replaces a sentence) · L4 hero device (the argument is it). Good pages are usually stacked (big type L2 + a spot mark L3 + corner sketches L1).

### The cross-page gate · 跨页一致性闸
The first three gates are per-page. The fourth is not: a recurring character/concept must carry a written **identity contract** into *every* page's prompt (e.g. "Maya = a person you hired; never a robot / gears / circuitry"). The model doesn't know what other pages drew, and the material will drag it back to its own habits unless you forbid it. Check by looking at the images side by side — you can't see it in the prompt.

反复出现的角色/概念，身份约定要写进**每一页**的 prompt；材质会把它带偏，不明写就跑偏。靠并排看图查，读 prompt 看不出。

## Full-image = three axes multiplied · 出图三轴相乘
```
SURFACE:  the material recipe (all brushwork & medium)
SKELETON: pure geometry (layout; no material words; may be "none")
DEVICE:   the per-page thing (leave the slot; fill per page)
END:      full-bleed, render DEVICE in SURFACE, SKELETON composition
```
Only SURFACE + SKELETON makes a thin deck. The DEVICE slot is the most valuable and the least systematizable.

### Four hard image rules (scars, not theory) · 四条出图硬规则
1. **Density in layers** — background fills (dimmed), one hero at ~70% with density *inside* it, limited foreground; no floating data cards.
2. **Never invent CJK** — decorative marks may only be geometric / numbers / dimension lines.
3. **Suppress structure words** — a CRITICAL tail listing forbidden words (STYLE / LAYOUT / VERBATIM / caption / eyebrow…).
4. **Titles gain a stray character** — proofread every character of a title after generating.

## Three-tier selection: medium → hand → world · 三层选型
- **Medium** — what a page is made of (parchment / film / copperplate). The root of the material axis.
- **Hand** — whose hand in that medium: a school = palette + lighting + composition habits + motifs + mood as a DNA pack (it reaches into the skeleton axis). Nolan and Villeneuve are the same medium, two hands.
- **World** — the setting the audience enters (its own information grammar, camera, time, hidden symbol). The real trigger for a material is a *world setting*, not mere prettiness.

Order: pick the world → pick the medium → pick a hand if a sub-library exists → skeleton auto by role → device per page.

## The school system (organizing method, open) · 流派体系
A **family** is a medium's world; a **school** is a fought-and-won, four-axis-complete, reproducible, nameable pack; a **candidate** is anchored but unproven; a **loose part** is a technique with no anchor. Making a new deck: hit a school → compile directly; miss → promote a candidate; one-off need → a loose part. Two iron rules: **swap the material, you must swap the skeleton** (a re-skin makes every deck the same mold); the **world-rebuild step** = a spec table (per page: scene/region + skeleton + device) drives all prompts, so the world stays coherent and repetition dies.

⚠️ The *method* is open. Specific material masters / schools / master hands are the **community-contributed library** (`styles/`) — bring your own.

## Overturned models (kept as a warning) · 被推翻的模型
- The "two kinds of deck (talk-backdrop vs info-deck)" split was replaced by a single per-page knob — the split was our own earlier model, overturned in practice.
- Illustration as a binary (has / hasn't) was replaced by the L0–L4 levels — treating it as on/off made章节页和快切页 come out bare.
- "Ask the user to be friendly" — every question you ask the user is one judgment this layer is missing.

被推翻的：两分法（演讲背景图/信息 deck）→ 一根旋钮；插画二值 → 五量级；"多问用户"→ 每多问一个问题就是判断少一条。
