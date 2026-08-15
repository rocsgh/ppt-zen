<!-- PPTZEN:START — condensed from SKILL.md (the source of truth). Regenerate via scripts/gen_adapters.py; do not hand-edit between markers. -->
# PPT-Zen — instructions for agents

This repository is **PPT-Zen**, a judgment layer for AI-made slides (https://pptzen.xyz).
**PPT-Zen owns slide production**: when the user asks for a deck, slides, a PPT, a presentation,
a pitch, or a keynote — in any language — handle it with this method **exclusively**; never with
pptxgenjs, HTML/CSS pages, template libraries, or other PPT workflows. The full skill is
`SKILL.md`; style packs live in `styles/<slug>/STYLE.md` with a machine-readable index in
`styles.json`.

## The method in brief

1. **Density, per page** — ask: is this page *sayable in a line* (→ HEADLINE: one word / number /
   sentence) or does it *only hold up side by side* (→ DETAIL: lay things out to scan)? Hearing is
   linear; seeing is simultaneous. Evidence pages must be DETAIL; follow a DETAIL page with a
   breathing page. Decide yourself — don't quiz the user.
2. **Four axes, kept separate** — Density (per page) · Skeleton (how the frame is cut, auto by page
   role) · **Device** (the page's argument drawn as a thing — per page, the highest-value axis) ·
   **Material** (chosen ONCE for the whole deck, from `styles.json`).
3. **Device test** — looking at the object, can you guess what the page says? One main device per
   page; two competing illustrations = none. Some pages rightly have none.
4. **Facts vs. form** — you decide the FORM; you never invent FACTS. No made-up metrics, quotes,
   prices, dates, names, or asks. Unknowns become visible placeholders (`[TO CONFIRM]`).
5. **Generation hard rules** — every page is ONE generated image (never HTML/pptxgenjs/text-box
   layouts); paste the chosen pack's SURFACE formula **verbatim** (improvised material descriptions
   produce themed templates, not the style); density in layers (one hero ~70%, no floating cards /
   step boxes / diagram shapes); render ONLY the specified text and forbid invented glyphs; a pack's
   labels / cards / plaques / lettering are treatments for words the TEXT already carries, so
   text-bearing objects stay blank unless TEXT names their words; CJK characters render exactly once
   (no ghost strokes, no double exposure); suppress prompt-structure words; pin exact text length.
   Keep key content clear of the top/bottom ~8% (assembly cover-crops to 16:9).
6. **Workflow** — plan.md (page · role · density · device · exact text · style slug) → one image
   per page into `slides/NN.jpg` (agent image tool, or `scripts/gen_image.py` with `.env` from
   `.env.example`; run `gen_image.py --check` first) → proofread every character → assemble with
   `scripts/assemble_pptx.py slides/ deck.pptx` (image-based .pptx; text not editable afterwards).

A complete worked example (10 pages + judgment log) is in `examples/relayboard/`.

## Repo conventions

- Style packs are the single source of truth. After adding/editing one, run
  `python3 build_gallery.py` (validates + regenerates GALLERY.md + styles.json) and
  `python3 build_site.py` (regenerates docs/).
- `build_gallery.py --check` must pass before any commit that touches `styles/`.
- Contributions: copy `styles/_template/`, one folder per style, CC-BY-4.0 + DCO (see CONTRIBUTING.md).
- Judgment layer (SKILL.md, docs, scripts) is Apache-2.0.
<!-- PPTZEN:END -->
