#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the passive-runtime adapter files (Cursor / Windsurf / Copilot) from
AGENTS.md, which is itself the condensed form of SKILL.md (the source of truth).
Run after editing SKILL.md/AGENTS.md. Generated files carry a do-not-edit header."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (script lives in scripts/)
body = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
# strip the injection markers for standalone adapter files
core = re.sub(r"<!-- PPTZEN:(START|END)[^>]*-->\n?", "", body).strip() + "\n"
HDR = "<!-- GENERATED from AGENTS.md by scripts/gen_adapters.py — do not edit by hand. -->\n"

out = {
    "adapters/cursor/ppt-zen.mdc": (
        "---\ndescription: PPT-Zen — judgment layer for AI-made slides; apply when making decks/slides/presentations\nalwaysApply: false\n---\n"
        + HDR + core),
    "adapters/windsurf/ppt-zen.md": HDR + core,
    "adapters/copilot/ppt-zen.instructions.md": (
        "---\napplyTo: \"**\"\n---\n" + HDR + core),
}
for rel, content in out.items():
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)
    print("wrote", rel)
