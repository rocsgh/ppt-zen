---
name: ppt-zen
description: >-
  Make a slide deck, slides, a presentation, a pitch, or a keynote — or design a single
  slide. Full-bleed image slides with a judgment layer: decides per page how much it should
  hold (headline vs. detail) and what to draw (the device), renders every page in ONE chosen
  material. Also use when the user says "ppt-zen" or names a ppt-zen gallery style
  (Portolan, Swiss grid, Ink wash, Neon Nocturne, ...).
license: Apache-2.0
metadata:
  homepage: https://pptzen.xyz
  version: "1.0"
---

# PPT-Zen — a judgment layer for AI-made slides

You already turn content into pages. This skill is the layer most tools skip: **for each page,
how much should it hold, what should it look like, and on what grounds?** The user gives one
sentence ("make me a deck about X"); you decide everything else and render each page full-image.

## 0. What this needs — image generation (engine-agnostic)

Every page is a generated image. You need exactly one way to make images. In order of preference:

1. **The agent already has an image-generation tool.** Use it. The contract this skill assumes is
   minimal: `generate(prompt: str, size: str) -> image bytes/file`, landscape, ≥1.3 MP. If your
   runtime's tool has a different signature, adapt — you only ever need "prompt in, one landscape
   image out."
2. **No image tool? Use the bundled helper.** `scripts/gen_image.py "<full-page prompt>" out.jpg`
   calls any OpenAI-compatible images endpoint. Copy `.env.example` to `.env`, set
   `IMAGE_API_BASE_URL`, `IMAGE_API_KEY`, `IMAGE_MODEL`, `IMAGE_SIZE`. It POSTs
   `{model, prompt, size, n:1}` to `{BASE}/images/generations` and reads `data[0].b64_json`
   (or `data[0].url`). Run `python3 scripts/gen_image.py --check` first to verify the endpoint.

**This skill ships NO image key and NO model.** It is the judgment + prompts; the pixels come from
your model.

> Aspect ratio: image models rarely emit native 16:9. Generate landscape (e.g. `1536x1024`, 3:2)
> and let assembly **cover-crop to 16:9** — so keep every title and key element clear of the top
> and bottom ~8% of the frame (say so in each prompt). `scripts/assemble_pptx.py` does the crop.

## 1. The one rule of density (this is the whole method in one line)

For every page ask: **is this "sayable in a line", or does it "only hold up when several things
sit side by side"?** Because **hearing is linear; seeing is simultaneous.**

| the page is… | → knob | put on screen |
|---|---|---|
| one claim / one number / a chapter beat | **HEADLINE** | one word, one number, one sentence |
| steps, a comparison, a list, a matrix | **DETAIL** | lay the things out so they can be scanned |

Two rules that run automatically:
- **Evidence pages must be DETAIL** — right after "AI already names competitors", show the names.
  Evidence you can't see doesn't count.
- **Dense stretches need relief** — never stack two *visually heavy* treatments back-to-back.
  A run of DETAIL pages is fine when each stays light (three labels, one chart, a 2×2 — see the
  example's evidence block), but land on a breathing HEADLINE page after the block.

You decide the knob per page. You do **not** ask the user.

## 2. The four axes (independent — don't merge them)

| axis | what | who decides |
|---|---|---|
| **Density** | headline ↔ detail | you, per page (rule §1) |
| **Skeleton** | how the frame is cut (grid / light-band / flowline / color-field / standoff… or none) | auto, by the page's job |
| **Device** | **the page's argument, drawn as a thing** | you, per page — the highest-value axis |
| **Material** | what it's made of (ink wash / copperplate / cinematic / Swiss grid…) | **chosen once, whole deck** |

## 3. Device — draw the argument (most-skipped axis)

Material is "made of what"; skeleton is "how the frame is cut" — **neither says what to draw.**
The device is the gap between them: **this page's meaning, drawn as an object.**
- "a score" → a measuring stick; "70% at work, 30% at home" → a balance scale; "asking once is
  luck" → dots scattering then converging (that *is* sampling); "AI names only 1–2 brands" → a funnel.
- Test: **looking at the object, can you guess what the page is about?** If not, change it.
- **One main device per page.** Two competing illustrations = no illustration.
- Some pages have none (a pure comparison, a list, a single number). Forcing a device there loses.

**How to find it (don't skip to drawing):** ① keyword the page in 2–3 words → ② map each to a
visible thing → ③ sketch 2–3 candidates → ④ pick the simplest that reads, not the cleverest.

**Illustration has levels, not on/off** — and good pages stack them:
`L0` material+type only · `L1` faint margin studies (credibility, no info) · `L2` typography IS the
image (a chapter word) · `L3` a small mark that replaces a sentence (a red ✗ = "this one's false")
· `L4` a main device that owns the page. "No main device" ≠ blank — it still gets L1/L2 or L3.

**Cross-page consistency (single-page checks miss this):** for any recurring character or concept,
write its identity down and put it (and its bans) into *every* page's prompt — a model doesn't know
what the other pages drew. (e.g. "Maya = a person, never a robot/gears/circuitry.")

## 4. Material — chosen once; pick from the gallery

Material is the deck's identity: change skeleton and device per page, but **hold material fixed** so
ten pages read as one artifact. (Only break it if the material *change itself* is the argument, once,
at a real turning point.)

Browse `styles/<slug>/STYLE.md` (or the live gallery at https://pptzen.xyz, and `styles.json` for a
machine-readable index of slug → name / medium / hand / prompt_formula). Each pack ships a reusable
`prompt_formula` (SURFACE / SKELETON / DEVICE / END / CRITICAL). Resolve a user's named style to its
slug via `styles.json` (match `name`, `slug`, or `aliases`) and record the resolved slug in the plan.

**Three-layer selection** — medium → hand → world:
- **medium** = the craft (cinema, ink, copperplate, tile…). **hand** = whose treatment within it
  (a cold monumental hand vs. a warm hazy hand are the same medium, different eyes). **world** = the
  scene the deck lives in. If the user only gives a vibe, pick a medium that fits the subject's own
  materials; ask one question only if genuinely stuck.

## 5. Facts vs. form — decide the FORM, never invent FACTS

The judgment layer owns **how a page looks**, not **what it claims**. Hard rule:

> **Never invent metrics, quotations, prices, dates, company names, or fundraising asks.**

Use only facts the user supplied. For any number/claim you don't have, write a visible placeholder
(`[TO CONFIRM]`, `<your metric>`) — never a plausible-looking fabrication. Before generating, list the
factual claims each page will show and confirm every one traces to the user's input. A deck is
presented as true; a beautiful slide with a made-up "$28k MRR" is a liability, not a feature.

**How facts get in — two modes** (this is how "one sentence in" and "never invent" coexist):
- **Source-backed (default):** the sentence sets the deck; facts come from whatever material the
  user attached or the conversation already contains. If a data page has no source, it ships with
  placeholders — a complete *structural* draft the user fills in, not a fact-ready deck.
- **Research mode (only if your runtime can browse and the user asked for it):** you may gather
  facts, but every claim gets its source recorded in `plan.md` next to the page that uses it.
The one-sentence promise is about *form* — the user never answers layout questions. It is not a
license to hallucinate content.

## 6. Full-image generation — four hard rules

Each page is one self-contained prompt. Always:
1. **Density in layers** — background texture fills but recedes; one hero ~70%; foreground accents
   limited; **no floating data cards / sidebars / widgets.**
2. **Never invent glyphs** — state the exact text to render and forbid any other words; decorative
   marks must be geometric only (ticks, numbers, dimension lines). Non-Latin scripts especially:
   spell out the exact characters and forbid additions.
3. **Suppress structural words** — end every prompt with a CRITICAL line forbidding prompt-structure
   words (STYLE / SURFACE / DEVICE / VERBATIM / label / caption…) from appearing in the image.
4. **Pin exact text length** — "render exactly these N words/characters — no additions", or the model
   adds a stray word.

Prompt skeleton (material × skeleton × device):
```
SURFACE:  <the chosen material's recipe — one per deck>
SKELETON: <auto by page role; or "plain">
DEVICE:   <this page's argument as an object; or "none">
TEXT:     <exact words to render, and where>
CRITICAL: render ONLY the text above; every letter correct; no invented glyphs; no other language;
          no structure words; keep key content clear of top/bottom ~8%.
```
Dense/text-heavy pages: generate at higher resolution than single-word pages.

## 7. If it's presented live (constraints you only learn from real rooms)

- **Confirm the screen aspect first** — big venues are often ultra-wide, not 16:9. This is one of the
  few things worth asking the user.
- **Leave a presenter corridor** — keep key info out of the bottom third; on ultra-wide, push subjects
  to the sides and keep the middle open (the speaker stands there).
- **Assertion capsule** — a fixed-position one-line conclusion on every page ("so what?"); detail
  pages especially need a place that states what to conclude.
- **Bilingual citations** — `Local Title (English Title)`; person name localized on top, original
  smaller/lighter below; facts only, no adjectives.

## 8. Workflow (one sentence in → a deck out)

1. **Plan** — write `plan.md`: one row per page with `role · density · device · exact text · style_slug`.
   This is the judgment log (the part nobody can screenshot). Decide material once, up front.
2. **Generate** — one image per page into `slides/NN.jpg`, using the agent's image tool or
   `scripts/gen_image.py`. Use deterministic filenames; regenerate a single page in isolation.
   Work in the user's project directory; call the helpers by their full path under the repo or the
   installed skill directory (`gen_image.py` reads `.env` from the current directory first, then
   from the repo root next to the script).
3. **QC the images** — proofread every character of every title against the plan, confirm no
   invented glyphs and no cross-page contradiction, and check nothing important sits in the
   top/bottom ~8% that assembly will crop. This gate is where the quality comes from.
4. **Assemble, then check the deck** — `python3 scripts/assemble_pptx.py slides/ deck.pptx`
   (16:9 full-bleed; non-16:9 images are center cover-cropped). Open the result: page order,
   crop, nothing eaten. Regenerate and reassemble single pages as needed. The output is an
   **image-based** `.pptx`: great to present, but text isn't editable — fixing a typo means
   regenerating that one page. PDF / Keynote / Google Slides import the same images.

See `examples/relayboard/` for a full ten-page worked deck plus its judgment log.
Optional deep-dives ship in `references/` (design laws, skeleton library, visual patterns,
delivery coaching — currently in Chinese; load them when you need the underlying reasoning).

## Delivery self-check

- [ ] Density set per page? Evidence pages detailed, dense blocks landing on a breathing page?
- [ ] Each page: a device that reads (or a deliberate "none"), one main device only?
- [ ] Material fixed across the whole deck? Style resolved to a real slug?
- [ ] **Every factual claim traces to the user's input? No invented numbers/quotes/prices/dates?**
- [ ] Four hard rules on every prompt? Key content clear of the crop zone?
- [ ] Recurring characters/concepts pinned identically in every prompt?
- [ ] Proofread every character after generation? Assembled and opened the `.pptx`?
