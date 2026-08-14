#!/usr/bin/env bash
# PPT-Zen installer — copies the skill to the right place for your agent runtime.
#
#   ./install.sh <agent> [--global] [--dest DIR]
#
#   agent ∈ claude | openclaw | hermes | codex | cursor | windsurf | copilot | all
#
#   default        install into the CURRENT project (./.claude/skills/... etc.)
#   --global       install for the user (~/.claude/skills/..., ~/.codex/AGENTS.md, ...)
#   --dest DIR     override the destination directory entirely (skill dirs only)
#
# The mapping lives in install/targets.json; this script mirrors it (no jq needed).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
AGENT="${1:-}"
[ -z "$AGENT" ] && { grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
shift || true
GLOBAL=0; DEST_OVERRIDE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --global) GLOBAL=1 ;;
    --dest) DEST_OVERRIDE="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac; shift
done

BUNDLE="references styles scripts examples styles.json .env.example"

install_skill_dir() {  # $1 = base dir that will contain SKILL.md
  local d="$1"
  mkdir -p "$d"
  cp "$HERE/SKILL.md" "$d/"
  for b in $BUNDLE; do
    [ -e "$HERE/$b" ] || continue
    if [ -d "$HERE/$b" ]; then rm -rf "$d/$b"; cp -R "$HERE/$b" "$d/"; else cp "$HERE/$b" "$d/"; fi
  done
  echo "installed skill -> $d"
  echo "  image key: cp $d/.env.example $d/.env  (gen_image.py reads it there for global installs)"
}

inject_agents_md() {  # $1 = dest AGENTS.md (idempotent between PPTZEN markers)
  local dest="$1"; mkdir -p "$(dirname "$dest")"
  local block; block="$(cat "$HERE/AGENTS.md")"
  if [ -f "$dest" ] && grep -q "PPTZEN:START" "$dest"; then
    awk -v repl="$block" 'BEGIN{inblk=0}
      /PPTZEN:START/{print repl; inblk=1; next}
      /PPTZEN:END/{inblk=0; next}
      !inblk{print}' "$dest" > "$dest.tmp" && mv "$dest.tmp" "$dest"
    echo "updated PPT-Zen block in $dest"
  elif [ -f "$dest" ]; then
    printf '\n%s\n' "$block" >> "$dest"; echo "appended PPT-Zen block to $dest"
  else
    printf '%s\n' "$block" > "$dest"; echo "created $dest"
  fi
}

copy_one() {  # $1 src (relative), $2 dest (relative/absolute)
  local src="$HERE/$1" dest="$2"
  mkdir -p "$(dirname "$dest")"; cp "$src" "$dest"; echo "installed $1 -> $dest"
}

do_agent() {
  case "$1" in
    claude)
      local base=".claude/skills/ppt-zen"; [ $GLOBAL = 1 ] && base="$HOME/.claude/skills/ppt-zen"
      [ -n "$DEST_OVERRIDE" ] && base="$DEST_OVERRIDE"
      install_skill_dir "$base"
      echo "  invoke: /ppt-zen  (or just ask for a deck)" ;;
    openclaw)
      local base=".openclaw/skills/ppt-zen"; [ $GLOBAL = 1 ] && base="$HOME/.openclaw/skills/ppt-zen"
      [ -n "$DEST_OVERRIDE" ] && base="$DEST_OVERRIDE"
      install_skill_dir "$base" ;;
    hermes)
      local base=".hermes/skills/ppt-zen"; [ $GLOBAL = 1 ] && base="$HOME/.hermes/skills/ppt-zen"
      [ -n "$DEST_OVERRIDE" ] && base="$DEST_OVERRIDE"
      install_skill_dir "$base" ;;
    codex)
      local dest="AGENTS.md"; [ $GLOBAL = 1 ] && dest="$HOME/.codex/AGENTS.md"
      inject_agents_md "$dest" ;;
    cursor)   copy_one "adapters/cursor/ppt-zen.mdc" ".cursor/rules/ppt-zen.mdc" ;;
    windsurf) copy_one "adapters/windsurf/ppt-zen.md" ".windsurf/rules/ppt-zen.md" ;;
    copilot)  copy_one "adapters/copilot/ppt-zen.instructions.md" ".github/instructions/ppt-zen.instructions.md" ;;
    all)
      for a in claude openclaw hermes codex cursor windsurf copilot; do do_agent "$a"; done ;;
    *) echo "unknown agent: $1 (claude|openclaw|hermes|codex|cursor|windsurf|copilot|all)" >&2; exit 1 ;;
  esac
}

do_agent "$AGENT"
