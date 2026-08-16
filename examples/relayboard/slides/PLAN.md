# Judgment pack — Relayboard, dark editorial edition (10 pages)
style: bespoke — the dark-editorial material below is the deck's own; the gallery packs in styles.json work the same way

One stanza per page, in reading order. `density` is HEADLINE or DETAIL; `device` is the
page's argument drawn as a thing; `text` is the verbatim on-slide copy; `prompt` is the
complete image prompt — exactly what produced the image of the same name in this folder,
ready to paste into any image tool. The `##` line names the page's file.

This is the artifact PPT-Zen hands you when there's no image endpoint: the judgment ships
first, the pixels follow. Re-render or extend it with

    python3 <skill_dir>/scripts/judgment_pack.py slides

which leaves every existing image alone (all ten are already here) and rebuilds the deck.
The same prompts live in `gen.py`, which regenerates the images against your own endpoint.

> Relayboard is fictional; every metric below is invented demo content.

## 01-cover
density: HEADLINE
device: a single glowing coral signal node with soft concentric rings radiating outward, lower-right
text: large title 'Relayboard' top-left; below it, smaller 'Async standup that respects deep work.'
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a single glowing coral signal node with soft concentric rings radiating outward,
            lower-right.
  TEXT:     large title 'Relayboard' top-left; below it, smaller 'Async standup that respects deep
            work.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 02-problem
density: HEADLINE
device: one clean thin horizontal focus line that shatters/breaks at a single point mid-frame
text: a single centered line 'Standups interrupt the people doing the work.'
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   one clean thin horizontal focus line that shatters/breaks at a single point mid-frame.
  TEXT:     a single centered line 'Standups interrupt the people doing the work.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 03-cost
density: HEADLINE
device: a huge coral-and-white number as the hero, with a thin line-art hourglass at the side
text: enormous '23 min' centered; below it, smaller 'to refocus after a single interruption.'
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a huge coral-and-white number as the hero, with a thin line-art hourglass at the side.
  TEXT:     enormous '23 min' centered; below it, smaller 'to refocus after a single interruption.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 04-product
density: HEADLINE
device: a clean minimalist card/tile catching an incoming signal line from the side
text: large 'The standup comes to you.' left; small 'Relayboard' as a mark top-left.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a clean minimalist card/tile catching an incoming signal line from the side.
  TEXT:     large 'The standup comes to you.' left; small 'Relayboard' as a mark top-left.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 05-how
density: DETAIL
device: three simple line-art nodes connected left-to-right by a thin coral line (a 3-step flow)
text: three short labels under the nodes: '1 Post async' '2 Blockers surface' '3 Only who's needed syncs'. A small heading top-left 'How it works'.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   three simple line-art nodes connected left-to-right by a thin coral line (a 3-step
            flow).
  TEXT:     three short labels under the nodes: '1 Post async' '2 Blockers surface' '3 Only who's
            needed syncs'. A small heading top-left 'How it works'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 06-traction
density: DETAIL
device: a thin coral line rising steadily from lower-left to upper-right
text: heading top-left 'Traction'; three numbers along the top: '340 teams', '$28k MRR', '+22% MoM'.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a thin coral line rising steadily from lower-left to upper-right.
  TEXT:     heading top-left 'Traction'; three numbers along the top: '340 teams', '$28k MRR', '+22%
            MoM'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 07-pricing
density: DETAIL
device: three stacked minimalist tiers/blocks ascending in height
text: heading 'Pricing'; three tier labels: 'Free', 'Team $6 / seat', 'Scale $12 / seat'.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   three stacked minimalist tiers/blocks ascending in height.
  TEXT:     heading 'Pricing'; three tier labels: 'Free', 'Team $6 / seat', 'Scale $12 / seat'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 08-competition
density: DETAIL
device: a clean 2x2 quadrant, thin white axes, one coral dot in the top-right cell
text: axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight' (top); the coral dot labeled 'Relayboard'. Small heading top-left 'Where we sit'.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a clean 2x2 quadrant, thin white axes, one coral dot in the top-right cell.
  TEXT:     axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight'
            (top); the coral dot labeled 'Relayboard'. Small heading top-left 'Where we sit'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 09-roadmap
density: DETAIL
device: a thin horizontal timeline with three small coral milestone dots
text: heading 'Roadmap'; three milestone labels: 'Now Async standup', 'Q3 Blocker routing', 'Q4 Integrations'.
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a thin horizontal timeline with three small coral milestone dots.
  TEXT:     heading 'Roadmap'; three milestone labels: 'Now Async standup', 'Q3 Blocker routing',
            'Q4 Integrations'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.

## 10-ask
density: HEADLINE
device: a single thin coral arrow sweeping toward a bright horizon line, right side
text: large centered-left 'Raising $1.5M to give every team its focus back.'
prompt: |
  SURFACE:  Premium keynote film still. Near-black #0e0e12 background, warm off-white type, ONE
            coral (#ff5a4d) accent, subtle film grain, generous negative space, crisp modern
            sans-serif typography, minimalist. A single thin line-art device per page (coral/white
            strokes). Full-bleed 16:9. No UI chrome, no data cards, no sidebars, no eyebrow labels.
  DEVICE:   a single thin coral arrow sweeping toward a bright horizon line, right side.
  TEXT:     large centered-left 'Raising $1.5M to give every team its focus back.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text,
            no watermark, no logo. All text in clean legible English. Keep labels short and
            correctly spelled.
