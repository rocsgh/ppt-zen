# Judgment pack — Relayboard, Portolan edition (10 pages)
style: portolan  (Portolan Sea Chart — styles/portolan/STYLE.md)

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
device: a small fleet of sailing ships departing lower-left along a curved route toward a red destination dot upper-right; a compass rose lower-right
text: large title 'Relayboard' upper-left; beneath it smaller 'Async standup that respects deep work.'
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   a small fleet of sailing ships departing lower-left along a curved route toward a red
            destination dot upper-right; a compass rose lower-right.
  TEXT:     large title 'Relayboard' upper-left; beneath it smaller 'Async standup that respects
            deep work.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 02-problem
density: HEADLINE
device: one long inked voyage route across open sea that SNAPS mid-frame — broken at a single point, the two ends drifting apart
text: a single centered line 'Standups interrupt the people doing the work.'
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   one long inked voyage route across open sea that SNAPS mid-frame — broken at a single
            point, the two ends drifting apart.
  TEXT:     a single centered line 'Standups interrupt the people doing the work.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 03-cost
density: HEADLINE
device: an enormous '23 min' lettered in dark ink as the hero, with a pair of navigator's dividers (compass tool) measuring a distance beside it
text: enormous '23 min'; below it, smaller 'to refocus after a single interruption.'
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   an enormous '23 min' lettered in dark ink as the hero, with a pair of navigator's
            dividers (compass tool) measuring a distance beside it.
  TEXT:     enormous '23 min'; below it, smaller 'to refocus after a single interruption.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 04-product
density: HEADLINE
device: a small courier boat drawing alongside a large anchored ship, a dotted line connecting them
text: large 'The standup comes to you.' left; small 'Relayboard' as an ink mark top-left.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   a small courier boat drawing alongside a large anchored ship, a dotted line connecting
            them.
  TEXT:     large 'The standup comes to you.' left; small 'Relayboard' as an ink mark top-left.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 05-how
density: DETAIL
device: three small inked islands connected left-to-right by a dotted sailing route
text: heading top-left 'How it works'; three short labels under the islands: '1 Post async' '2 Blockers surface' '3 Only who's needed syncs'.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   three small inked islands connected left-to-right by a dotted sailing route.
  TEXT:     heading top-left 'How it works'; three short labels under the islands: '1 Post async' '2
            Blockers surface' '3 Only who's needed syncs'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 06-traction
density: DETAIL
device: a rising sea-lane climbing from lower-left to upper-right drawn as a fleet of small ships ascending a curved route
text: heading top-left 'Traction'; three ink annotations along the top: '340 teams', '$28k MRR', '+22% MoM'.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   a rising sea-lane climbing from lower-left to upper-right drawn as a fleet of small
            ships ascending a curved route.
  TEXT:     heading top-left 'Traction'; three ink annotations along the top: '340 teams', '$28k
            MRR', '+22% MoM'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 07-pricing
density: DETAIL
device: three sailing ships of ascending size in a row (small sloop, mid galleon, grand galleon)
text: heading 'Pricing'; labels under the ships: 'Free', 'Team $6 / seat', 'Scale $12 / seat'.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   three sailing ships of ascending size in a row (small sloop, mid galleon, grand
            galleon).
  TEXT:     heading 'Pricing'; labels under the ships: 'Free', 'Team $6 / seat', 'Scale $12 / seat'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 08-competition
density: DETAIL
device: a clean 2x2 chart quadrant inked on the parchment, thin lines, one red dot in the top-right cell
text: axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight' (top); the red dot labeled 'Relayboard'. Small heading top-left 'Where we sit'.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   a clean 2x2 chart quadrant inked on the parchment, thin lines, one red dot in the
            top-right cell.
  TEXT:     axis ends labeled 'sync' (left) 'async' (right) and 'heavy' (bottom) 'lightweight'
            (top); the red dot labeled 'Relayboard'. Small heading top-left 'Where we sit'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 09-roadmap
density: DETAIL
device: a coastline with a dotted route passing three small harbors, each marked with a tiny flag
text: heading 'Roadmap'; three harbor labels: 'Now Async standup', 'Q3 Blocker routing', 'Q4 Integrations'.
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   a coastline with a dotted route passing three small harbors, each marked with a tiny
            flag.
  TEXT:     heading 'Roadmap'; three harbor labels: 'Now Async standup', 'Q3 Blocker routing', 'Q4
            Integrations'.
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.

## 10-ask
density: HEADLINE
device: one bold red route arrow sweeping toward a sunrise horizon at the chart's edge, a lone ship on it
text: large 'Raising $1.5M to give every team its focus back.'
prompt: |
  SURFACE:  16th-century portolan sea chart on aged sepia parchment: muted watercolor ocean, fine
            ink coastlines, faint rhumb lines, small compass roses, hand-inked annotations. NO
            photographic look, NO 3D. Text in elegant legible dark-brown ink serif/calligraphy. ONE
            red accent (a destination dot / a route) used sparingly. Full-bleed 16:9, generous open
            parchment.
  DEVICE:   one bold red route arrow sweeping toward a sunrise horizon at the chart's edge, a lone
            ship on it.
  TEXT:     large 'Raising $1.5M to give every team its focus back.'
  CRITICAL: render EXACTLY the text specified and NOTHING else — no extra words, no invented text or
            place names, no watermark. All text in clean correct English; decorative marks only as
            compass points, numbers or dotted rhumb lines. Keep all text clear of the top and bottom
            edges.
