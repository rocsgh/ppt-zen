#!/usr/bin/env bash
# PPT-Zen installer — copies the skill to the right place for your agent runtime.
#
#   ./install.sh                   detect the runtimes on this machine and report where PPT-Zen would go
#   ./install.sh auto              install into every runtime detected (project markers win over global)
#   ./install.sh <agent> [--global] [--dest DIR]
#
#   agent ∈ claude | openclaw | hermes | codex | cursor | windsurf | copilot | all
#
#   default        install into the CURRENT project (./.claude/skills/... etc.)
#   --global       install for the user (~/.claude/skills/..., ~/.codex/AGENTS.md, ...)
#   --dest DIR     override the destination directory entirely (skill dirs only)
#
#   note: hermes has no project-level skills dir — it always installs into
#         ${HERMES_HOME:-$HOME/.hermes}/skills/creative/ppt-zen (--global is a no-op).
#
# The mapping lives in install/targets.json; this script mirrors it (no jq needed).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
AGENT="${1:-}"
usage() { grep '^#' "$0" | sed 's/^# \{0,1\}//'; }
shift || true
GLOBAL=0; DEST_OVERRIDE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --global) GLOBAL=1 ;;
    --dest) DEST_OVERRIDE="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac; shift
done

BUNDLE="references styles scripts examples styles.json requirements.txt .env.example"

install_skill_dir() {  # $1 = base dir that will contain SKILL.md; $2 = "nohint" to skip the image-key line
  local d="$1"
  mkdir -p "$d"
  cp "$HERE/SKILL.md" "$d/"
  for b in $BUNDLE; do
    [ -e "$HERE/$b" ] || continue
    if [ -d "$HERE/$b" ]; then rm -rf "$d/$b"; cp -R "$HERE/$b" "$d/"; else cp "$HERE/$b" "$d/"; fi
  done
  echo "installed skill -> $d"
  if [ "${2:-}" != "nohint" ]; then
    echo "  image key: cp $d/.env.example $d/.env  (gen_image.py reads it there for global installs)"
    echo "  verify   : python3 $d/scripts/gen_image.py --check   (templates: $d/references/providers.md)"
  fi
}

# --- absolute paths for installs that live outside this checkout -------------
# AGENTS.md and the adapters name PPT-Zen's own files relatively (SKILL.md,
# scripts/…, styles.json, .env.example). Those resolve only inside the repo —
# injected into someone's project they dangle. So when the destination sits
# outside the checkout, rewrite the resource tokens to absolute paths and
# reframe the opening line. Every rewrite reads the pristine repo file, and each
# pattern is anchored on a backtick that the rewrite itself consumes, so running
# install twice writes the same bytes.
BT='`'
HERE_SED="$(printf '%s' "$HERE" | sed 's/[&|\\]/\\&/g')"

outside_repo() {  # $1 = destination path; true when it is NOT inside this checkout
  local d; d="$(cd "$(dirname "$1")" 2>/dev/null && pwd)" || return 0
  case "$d/" in "$HERE"/*) return 1 ;; esac
  return 0
}

absolutize() {  # stdin -> stdout
  sed -e "s|^This repository is \*\*PPT-Zen\*\*, a judgment layer for AI-made slides (https://pptzen.xyz)\.\$|PPT-Zen is installed at ${BT}${HERE_SED}${BT} — a judgment layer for AI-made slides (https://pptzen.xyz). Its files are named below by absolute path; you work in the user's project, not in that directory.|" \
      -e "s|${BT}SKILL\.md|${BT}${HERE_SED}/SKILL.md|g" \
      -e "s|${BT}styles\.json|${BT}${HERE_SED}/styles.json|g" \
      -e "s|${BT}styles/|${BT}${HERE_SED}/styles/|g" \
      -e "s|${BT}scripts/|${BT}${HERE_SED}/scripts/|g" \
      -e "s|${BT}references/|${BT}${HERE_SED}/references/|g" \
      -e "s|${BT}examples/|${BT}${HERE_SED}/examples/|g" \
      -e "s|${BT}\.env\.example|${BT}${HERE_SED}/.env.example|g" \
      -e "s|${BT}python3 build_|${BT}python3 ${HERE_SED}/build_|g" \
      -e "s|${BT}build_gallery\.py|${BT}${HERE_SED}/build_gallery.py|g"
}

inject_agents_md() {  # $1 = dest AGENTS.md (idempotent between PPTZEN markers)
  local dest="$1"; mkdir -p "$(dirname "$dest")"
  local block; block="$(cat "$HERE/AGENTS.md")"
  if outside_repo "$dest"; then
    block="$(printf '%s\n' "$block" | absolutize)"
    case "$block" in *"This repository is"*)
      echo "warning: AGENTS.md's opening line changed — absolutize() no longer reframes it (install.sh)" >&2 ;;
    esac
  fi
  if [ -f "$dest" ] && grep -q "PPTZEN:START" "$dest"; then
    # the block goes through a file, not -v: awk on macOS warns on multi-line -v values
    local blockfile; blockfile="$dest.pptzen.tmp"; printf '%s\n' "$block" > "$blockfile"
    awk -v bf="$blockfile" 'BEGIN{inblk=0}
      /PPTZEN:START/{while ((getline l < bf) > 0) print l; inblk=1; next}
      /PPTZEN:END/{inblk=0; next}
      !inblk{print}' "$dest" > "$dest.tmp" && mv "$dest.tmp" "$dest"
    rm -f "$blockfile"
    echo "updated PPT-Zen block in $dest"
  elif [ -f "$dest" ]; then
    printf '\n%s\n' "$block" >> "$dest"; echo "appended PPT-Zen block to $dest"
  else
    printf '%s\n' "$block" > "$dest"; echo "created $dest"
  fi
}

copy_one() {  # $1 src (relative), $2 dest (relative/absolute)
  local src="$HERE/$1" dest="$2"
  mkdir -p "$(dirname "$dest")"; cp "$src" "$dest"
  if outside_repo "$dest"; then
    absolutize < "$dest" > "$dest.tmp" && mv "$dest.tmp" "$dest"
  fi
  echo "installed $1 -> $dest"
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
      # Hermes only scans $HERMES_HOME/skills (default ~/.hermes) plus skills.external_dirs —
      # there is no project-level ./.hermes/skills, so --global is a no-op here. Skills nest
      # as <category>/<name>/; a flat dir would register "ppt-zen" as its own category.
      local base="${HERMES_HOME:-$HOME/.hermes}/skills/creative/ppt-zen"
      [ -n "$DEST_OVERRIDE" ] && base="$DEST_OVERRIDE"
      install_skill_dir "$base" nohint
      echo "  1. restart your Hermes gateway/process — the skill index is cached in-process"
      echo "  2. pip install python-pptx  (needed to assemble the deck)"
      echo "  3. image endpoint: an agent-native image tool works out of the box; otherwise cp $base/.env.example $base/.env and set IMAGE_API_*" ;;
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

DETECTED=""; MISSING_PROJECT=""; IN_REPO=0

have() { command -v "$1" >/dev/null 2>&1; }
add_detected() { DETECTED="$DETECTED$1|$2|$3|$4
"; }

detect_runtimes() {
  # no bash 4 here: DETECTED is a newline-separated list of "agent|scope|evidence|dest"
  DETECTED=""; MISSING_PROJECT=""; IN_REPO=0
  # running from inside the ppt-zen checkout itself: its own AGENTS.md / .github / etc. are
  # sources, not a user project — only global targets make sense here
  [ "$HERE" = "$(pwd)" ] && IN_REPO=1
  if [ $IN_REPO = 0 ] && [ -d "./.claude" ]; then add_detected claude project "./.claude/ in this project" ".claude/skills/ppt-zen"
  elif have claude; then      add_detected claude global "claude on PATH" "$HOME/.claude/skills/ppt-zen"
  elif [ -d "$HOME/.claude" ]; then add_detected claude global "~/.claude exists" "$HOME/.claude/skills/ppt-zen"; fi

  if [ $IN_REPO = 0 ] && [ -d "./.openclaw" ]; then add_detected openclaw project "./.openclaw/ in this project" ".openclaw/skills/ppt-zen"
  elif have openclaw; then      add_detected openclaw global "openclaw on PATH" "$HOME/.openclaw/skills/ppt-zen"
  elif [ -d "$HOME/.openclaw" ]; then add_detected openclaw global "~/.openclaw exists" "$HOME/.openclaw/skills/ppt-zen"; fi

  # hermes has no project level — always ${HERMES_HOME:-~/.hermes}/skills/creative/ppt-zen
  if [ -n "${HERMES_HOME:-}" ]; then   add_detected hermes fixed "HERMES_HOME is set" "${HERMES_HOME}/skills/creative/ppt-zen"
  elif [ -d "$HOME/.hermes" ]; then    add_detected hermes fixed "~/.hermes exists" "$HOME/.hermes/skills/creative/ppt-zen"
  elif have hermes; then               add_detected hermes fixed "hermes on PATH" "$HOME/.hermes/skills/creative/ppt-zen"; fi

  if [ $IN_REPO = 0 ] && [ -f "./AGENTS.md" ]; then add_detected codex project "./AGENTS.md in this project" "AGENTS.md"
  elif [ -d "$HOME/.codex" ]; then add_detected codex global "~/.codex exists" "$HOME/.codex/AGENTS.md"
  elif have codex; then            add_detected codex global "codex on PATH" "$HOME/.codex/AGENTS.md"; fi

  # project-only runtimes: no global location exists, so an absent marker means skip
  if [ $IN_REPO = 0 ] && [ -d "./.cursor" ]; then add_detected cursor project "./.cursor/ in this project" ".cursor/rules/ppt-zen.mdc"
  else MISSING_PROJECT="$MISSING_PROJECT cursor:./.cursor/"; fi
  if [ $IN_REPO = 0 ] && [ -d "./.windsurf" ]; then add_detected windsurf project "./.windsurf/ in this project" ".windsurf/rules/ppt-zen.md"
  else MISSING_PROJECT="$MISSING_PROJECT windsurf:./.windsurf/"; fi
  if [ $IN_REPO = 0 ] && [ -d "./.github" ]; then add_detected copilot project "./.github/ in this project" ".github/instructions/ppt-zen.instructions.md"
  else MISSING_PROJECT="$MISSING_PROJECT copilot:./.github/"; fi
}

report_detected() {
  if [ -z "$DETECTED" ]; then
    echo "PPT-Zen — no agent runtime found on this machine (looked for claude, openclaw, hermes, codex, cursor, windsurf, copilot)."
    echo "Pick one explicitly:"; echo
    usage; return 0
  fi
  echo "PPT-Zen — runtimes detected here:"; echo
  [ $IN_REPO = 1 ] && echo "  (inside the ppt-zen repo — project-level targets skipped; cd into your project to install there)" && echo
  while IFS='|' read -r a scope why dest; do
    [ -z "$a" ] && continue
    printf '  %-9s %-9s %-30s -> %s\n' "$a" "($scope)" "$why" "$dest"
  done <<EOF
$DETECTED
EOF
  echo
  echo "  ./install.sh auto      install into all of the above"
  echo
  usage
}

run_auto() {
  local installed="" a scope why dest
  if [ -z "$DETECTED" ]; then
    echo "no agent runtime detected — nothing installed."; echo
    usage; exit 1
  fi
  while IFS='|' read -r a scope why dest; do
    [ -z "$a" ] && continue
    if [ "$scope" = project ]; then GLOBAL=0; else GLOBAL=1; fi
    do_agent "$a"
    installed="$installed $a"
  done <<EOF
$DETECTED
EOF
  for m in $MISSING_PROJECT; do
    echo "skipped ${m%%:*} — no ${m##*:} here (project-only runtime, it has no global location)"
  done
  echo "installed:$installed"
  case " $installed " in *" hermes "*) echo "reminder: restart your Hermes gateway/process — the skill index is cached in-process" ;; esac
}

if [ -z "$AGENT" ]; then detect_runtimes; report_detected; exit 0; fi
if [ "$AGENT" = auto ]; then detect_runtimes; run_auto; exit 0; fi
do_agent "$AGENT"
