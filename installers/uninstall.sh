#!/usr/bin/env bash
set -euo pipefail
PLATFORM="${1:-}"; [[ -n "$PLATFORM" ]] && shift || true
TARGET="."; GLOBAL=0; DRY=0
usage(){ echo "usage: $0 <claude|codex|gemini> [target] [--global] [--dry-run]" >&2; exit 2; }
[[ "$PLATFORM" =~ ^(claude|codex|gemini)$ ]] || usage
while (($#)); do case "$1" in --global) GLOBAL=1;; --dry-run) DRY=1;; *) TARGET="$1";; esac; shift; done
run(){ if ((DRY)); then printf '[dry-run]'; printf ' %q' "$@"; printf '\n'; else "$@"; fi; }
if ((GLOBAL)); then
  case "$PLATFORM" in
    claude) SKILL="$HOME/.claude/skills/lean-routing"; AGENTS="$HOME/.claude/agents"; INST="$HOME/.claude/CLAUDE.md";;
    codex) SKILL="$HOME/.agents/skills/lean-routing"; AGENTS="$HOME/.codex/agents"; INST="$HOME/.codex/AGENTS.md";;
    gemini) SKILL="$HOME/.agents/skills/lean-routing"; AGENTS="$HOME/.gemini/agents"; INST="$HOME/.gemini/GEMINI.md"; CMDS="$HOME/.gemini/commands";;
  esac
else
  TARGET="$(cd "$TARGET" && pwd)"
  case "$PLATFORM" in
    claude) SKILL="$TARGET/.claude/skills/lean-routing"; AGENTS="$TARGET/.claude/agents"; INST="$TARGET/CLAUDE.md";;
    codex) SKILL="$TARGET/.agents/skills/lean-routing"; AGENTS="$TARGET/.codex/agents"; INST="$TARGET/AGENTS.md";;
    gemini) SKILL="$TARGET/.agents/skills/lean-routing"; AGENTS="$TARGET/.gemini/agents"; INST="$TARGET/GEMINI.md"; CMDS="$TARGET/.gemini/commands";;
  esac
fi
run rm -rf "$SKILL"
case "$PLATFORM" in
  claude) for f in cheap-ops.md cheap-edit.md cheap-coder.md reviewer.md; do run rm -f "$AGENTS/$f"; done;;
  codex) for f in cheap_ops.toml cheap_edit.toml cheap_coder.toml reviewer.toml; do run rm -f "$AGENTS/$f"; done;;
  gemini) for f in cheap-ops.md cheap-edit.md cheap-coder.md reviewer.md; do run rm -f "$AGENTS/$f"; done; run rm -f "$CMDS/lean.toml";;
esac
if [[ -f "$INST" ]]; then
  if ((DRY)); then echo "[dry-run] remove AgentForge block from $INST"; else
    python3 - "$INST" <<'PY'
from pathlib import Path
import re,sys
p=Path(sys.argv[1]); text=p.read_text(); start='<!-- agentforge:lean-routing:start -->'; end='<!-- agentforge:lean-routing:end -->'
text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?', '', text, flags=re.S).rstrip()
p.write_text(text+'\n' if text else '')
PY
  fi
fi
echo "AgentForge removed for $PLATFORM. Unrelated files were left untouched."
