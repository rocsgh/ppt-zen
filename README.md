<p align="center"><b>English</b> · <a href="README.zh-CN.md">简体中文</a></p>

<h1 align="center">PPT-Zen</h1>

<p align="center"><b>A judgment layer for AI-made slides — not another PPT generator.</b></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/judgment%20layer-Apache--2.0-blue.svg" alt="Apache-2.0"></a>
  <a href="LICENSE-STYLES"><img src="https://img.shields.io/badge/styles-CC--BY--4.0-lightgrey.svg" alt="CC-BY-4.0"></a>
  <a href="https://github.com/rocsgh/ppt-zen/stargazers"><img src="https://img.shields.io/github/stars/rocsgh/ppt-zen?style=social" alt="stars"></a>
</p>

<p align="center"><b>🖼 <a href="https://rocsgh.github.io/ppt-zen/">Live gallery →</a></b></p>

<p align="center">
  <img src="assets/hero-portolan.jpg" width="32%"/>
  <img src="assets/hero-nolan.jpg" width="32%"/>
  <img src="assets/hero-davinci.jpg" width="32%"/>
</p>

<p align="center"><i>One sentence in — "make me a deck." Judged page by page, generated full-image.<br/>Same line, three worlds.</i></p>

---

**Two things this project is about:**
1. **A thinking AI** that decides *how* each page should be — you don't answer questions.
2. **Output that actually looks good** — full-image, designed, text that isn't garbled. (See the strip above; more in the [Gallery](GALLERY.md).)

## What it is

Every AI PPT tool solves the same problem: *how to turn content into pages.* PPT-Zen open-sources the part nobody else does:

> **This page — how much should it hold, what should it look like, and on what grounds is it decided that way?**

**North star:** the user says one sentence and the rules run everything else — no template picker, no color questionnaire, no "what goes on each slide?".

## It's a judgment chain, not a feature list

The finished deck is copyable — anyone can screenshot one. The **chain of decisions** behind each page is not:

```
Page = a chapter pull-quote → sayable in a line → HEADLINE → skeleton: light-band
Page = competitive evidence → only holds up side by side → DETAIL → skeleton: grid
       → and the previous page was dense, so this one breathes
```

## The four axes

| Axis | What it is | Who decides |
|---|---|---|
| **Density** | headline ↔ detail | AI, per page |
| **Skeleton** | how the frame is cut (grid / light-band / flowline / color-field / standoff… or none) | auto by page role |
| **Device** | **the argument of this page, drawn as a thing** | per page — the most valuable axis |
| **Material** | what it's made of (ink wash / copperplate / pencil…) | once, whole deck |

The one density test: *is this page sayable in a line (→ headline), or does it only hold up when several things sit side by side (→ detail)?* Because **hearing is linear, seeing is simultaneous.**

## Why it's built this way

This isn't theory — it was **forced out by making real 70-page decks overnight**, and every layer answers a real problem we hit:

- **Device** was added because a beautiful material on a bare geometric page still felt empty — the missing axis was *what the page draws*.
- **Hand** (medium → hand → world) was added because "cinematic" is too vague — Nolan and Villeneuve are the same medium, two different hands.
- **The school system** exists so you don't rebuild a look from scratch every time.

The full architecture, the reasoning, and the models we've overturned along the way live in **[DESIGN.md](DESIGN.md)**.

## Honest about the human gates

> **Note — a tool, not a wishing well.** Full-image work means ~2 min per page to regenerate, screenshot QC, and proofread every character of a title. **These human gates are where the quality comes from** — we write them down instead of promising magic.

## What you get

PPT-Zen decides and generates the pages; you end up with:

- `slides/01.jpg … NN.jpg` — one full-image, 16:9 slide per page
- a short **page plan** — what each page is (headline / detail) and its device: the judgment log
- `deck.pptx` — assembled from the images with `scripts/assemble_pptx.py`

It is **not** a hosted button. It is a skill your agent runs, plus two small helper scripts. Assembling into `.pptx` is included; PDF / Keynote / Google Slides import the same full-bleed images.

## Quick start

```bash
git clone https://github.com/rocsgh/ppt-zen
cd ppt-zen

# 1. install the skill (Claude Code shown; or your agent's skills dir)
mkdir -p ~/.claude/skills/ppt-zen
cp SKILL.md ~/.claude/skills/ppt-zen/
cp -R references ~/.claude/skills/ppt-zen/

# 2. give it an image model (skip if your agent already generates images)
cp .env.example .env        # then put your key in .env

# 3. in your agent, describe the deck — one sentence:
#    "Make me a 10-page pitch deck about <your project> with ppt-zen, in the Portolan style."
#    -> it plans the pages, then generates one image per page into slides/

# 4. assemble the images into a real .pptx
pip install python-pptx
python3 scripts/assemble_pptx.py slides/ deck.pptx
```

**No skill system?** Paste `SKILL.md` into the session as context.
**Dependencies:** `gen_image.py` and the build scripts are pure standard library; only `assemble_pptx.py` needs `python-pptx`.

## Image generation (bring your own model)

PPT-Zen ships **no image model** — that is what keeps it engine-agnostic. You wire up your own, one of two ways:

- **Your agent already generates images** (Claude Code with an image tool, Hermes, etc.) — nothing to configure; the skill uses whatever the agent has.
- **Point at your own image API.** Copy `.env.example` to `.env` and fill your key — any **OpenAI-compatible images endpoint** works (OpenAI ``gpt-image``, a relay, or a compatible gateway):
  ```
  IMAGE_API_BASE_URL=https://api.openai.com/v1
  IMAGE_API_KEY=sk-...
  IMAGE_MODEL=gpt-image-1
  ```
  The included ``scripts/gen_image.py`` reads ``.env`` and generates a page:
  ```
  python3 scripts/gen_image.py "your full-page prompt" out.jpg
  ```

> A model that renders text well (gpt-image class) matters for readable titles — plain diffusion models garble text. ``.env`` is gitignored; never commit your key.

## Usage — how to run it, how to pick a style

Once installed, just describe the deck in chat:

```
Make me a deck about <your topic> with ppt-zen.
```

That is the whole interface. **Density and skeleton are decided per page — you do not answer questions.** The one thing you can steer is the **material / style**:

- **Let it pick.** Say nothing about looks; it chooses one coherent material for the whole deck.
- **Name a style.** Pick one from the [gallery](https://rocsgh.github.io/ppt-zen/) and say its name:
  ```
  ...in the Portolan sea-chart style.
  ...cinema, Nolan hand.
  ...da Vinci copperplate.
  ```
- **Coarse or fine (medium -> hand -> world).** A medium ("make it cinematic"), a specific hand ("Villeneuve"), or a whole world — go as detailed as you like.

Rule of thumb: **material is chosen once for the whole deck** (a consistent look); the **device** — what each page *draws* — is decided page by page.

## Styles & Gallery

Browse every style — each with a reproducible prompt formula — in **[GALLERY.md](GALLERY.md)**. Add your own: copy `styles/_template/` and open a PR (see **[CONTRIBUTING](CONTRIBUTING.md)**). The gallery is auto-generated from the packs, so your contribution shows up automatically.

## Want it done for you?

The skill is free and self-serve. A hosted version that runs the full generate → QC → assemble pipeline for you is coming separately.

## Docs

| | |
|---|---|
| 🖼 [Live gallery](https://rocsgh.github.io/ppt-zen/) | browse every style + its prompt formula |
| 🎨 [GALLERY.md](GALLERY.md) | the same gallery, in-repo |
| 🏗️ [DESIGN.md](DESIGN.md) | architecture, origin, and the models we overturned |
| 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) | add your own style in one folder |
| 🔒 [BOUNDARY.md](BOUNDARY.md) | what's open vs. what stays private |

## License

- **Judgment layer** (SKILL, docs, code): **[Apache-2.0](LICENSE)**
- **Style packs & gallery content** (`styles/`, images): **[CC-BY-4.0](LICENSE-STYLES)**, contributions via DCO

What's in the open vs private: **[BOUNDARY.md](BOUNDARY.md)**.

## Inspired by

The design discipline is **inspired by** Garr Reynolds' *Presentation Zen*. This project is **unofficial and unaffiliated** with the author or publisher; all prose is our own.
