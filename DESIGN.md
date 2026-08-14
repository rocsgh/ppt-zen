<p align="center"><b>English</b> · <a href="DESIGN.zh-CN.md">简体中文</a></p>

# Design & architecture

The origin, the reasoning, and the models we overturned. This is the part you can't screenshot.

---

## Where it came from

None of this is armchair theory. It was **forced out by making real, 70-page, full-image decks overnight**, repeatedly. Every rule below has a scar behind it. When a rule and the practice disagreed, the practice won — including some of our own earlier models (see *Overturned* at the bottom).

## Step 0 — one knob decides how much a page holds

Before anything else, each page gets one call:

> **Is this page sayable in a line (→ headline), or does it only hold up when several things sit side by side (→ detail)?**

Because **hearing is linear, seeing is simultaneous.** A headline page obeys presentation-zen restraint; a detail page obeys information-design density. Two automatic follow-ons: an *evidence* page must be detail (evidence you can't see doesn't count), and a detail page is followed by a page that breathes.

## The four axes

**Density × Skeleton × Device × Material.** Independent — don't mix them.

- **Density** — headline ↔ detail (Step 0). Per page, decided by the AI.
- **Skeleton** — how the frame is cut (grid / light-band / flowline / color-field / standoff… or none). Auto-assigned by page role, not asked.
- **Device — the argument of this page, drawn as a thing.** This is the axis everyone drops. Material decides *what it's made of*, skeleton decides *how it's cut* — neither decides *what it draws*. That gap is the device: a scale → a ruler; "one try is just luck" → a point-cloud scattering then converging to a line; "your customer before they meet you" → a raised hand. Two gates: it must *tie to the argument* (not a pretty thing that merely rhymes with the topic) **and** *grab attention* (not decoration in a corner). Self-check: looking at it, can you guess what the page says?
- **Material** — the surface (ink wash / copperplate / pencil…). Chosen once for the whole deck; the only axis the user might weigh in on.

### Illustration is a level, not on/off (L0–L4)
L0 none · L1 margin study (material credibility only) · L2 typography-as-illustration · L3 spot device (replaces a sentence) · L4 hero device (the argument is it). Good pages are usually stacked (big type L2 + a spot mark L3 + corner sketches L1).

### The cross-page gate
The first three gates are per-page. The fourth is not: a recurring character/concept must carry a written **identity contract** into *every* page's prompt (e.g. "Maya = a person you hired; never a robot / gears / circuitry"). The model doesn't know what other pages drew, and the material will drag it back to its own habits unless you forbid it. Check by looking at the images side by side — you can't see it in the prompt.

## Full-image = three axes multiplied
```
SURFACE:  the material recipe (all brushwork & medium)
SKELETON: pure geometry (layout; no material words; may be "none")
DEVICE:   the per-page thing (leave the slot; fill per page)
END:      full-bleed, render DEVICE in SURFACE, SKELETON composition
```
Only SURFACE + SKELETON makes a thin deck. The DEVICE slot is the most valuable and the least systematizable.

### Four hard image rules (scars, not theory)
1. **Density in layers** — background fills (dimmed), one hero at ~70% with density *inside* it, limited foreground; no floating data cards.
2. **Never invent CJK** — decorative marks may only be geometric / numbers / dimension lines.
3. **Suppress structure words** — a CRITICAL tail listing forbidden words (STYLE / LAYOUT / VERBATIM / caption / eyebrow…).
4. **Titles gain a stray character** — proofread every character of a title after generating.

## Three-tier selection: medium → hand → world
- **Medium** — what a page is made of (parchment / film / copperplate). The root of the material axis.
- **Hand** — whose hand in that medium: a school = palette + lighting + composition habits + motifs + mood as a DNA pack (it reaches into the skeleton axis). Nolan and Villeneuve are the same medium, two hands.
- **World** — the setting the audience enters (its own information grammar, camera, time, hidden symbol). The real trigger for a material is a *world setting*, not mere prettiness.

Order: pick the world → pick the medium → pick a hand if a sub-library exists → skeleton auto by role → device per page.

## The school system (organizing method, open)
A **family** is a medium's world; a **school** is a fought-and-won, four-axis-complete, reproducible, nameable pack; a **candidate** is anchored but unproven; a **loose part** is a technique with no anchor. Making a new deck: hit a school → compile directly; miss → promote a candidate; one-off need → a loose part. Two iron rules: **swap the material, you must swap the skeleton** (a re-skin makes every deck the same mold); the **world-rebuild step** = a spec table (per page: scene/region + skeleton + device) drives all prompts, so the world stays coherent and repetition dies.

⚠️ The *method* is open. Specific material masters / schools / master hands are the **community-contributed library** (`styles/`) — bring your own.

## Overturned models (kept as a warning)
- The "two kinds of deck (talk-backdrop vs info-deck)" split was replaced by a single per-page knob — the split was our own earlier model, overturned in practice.
- Illustration as a binary (has / hasn't) was replaced by the L0–L4 levels — treating it as on/off made chapter and quick-cut pages come out bare.
- "Ask the user to be friendly" — every question you ask the user is one judgment this layer is missing.
