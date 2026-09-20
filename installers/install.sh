#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORM="${1:-}"; [[ -n "$PLATFORM" ]] && shift || true
TARGET="."; GLOBAL=0; DRY=0
usage(){ echo "usage: $0 <claude|codex|gemini> [target] [--global] [--dry-run]" >&2; exit 2; }
[[ "$PLATFORM" =~ ^(claude|codex|gemini)$ ]] || usage
while (($#)); do case "$1" in --global) GLOBAL=1;; --dry-run) DRY=1;; -h|--help) usage;; *) TARGET="$1";; esac; shift; done
run(){ if ((DRY)); then printf '[dry-run]'; printf ' %q' "$@"; printf '\n'; else "$@"; fi; }
copy_tree(){ local src="$1" dst="$2"; run mkdir -p "$dst"; if ((DRY)); then echo "[dry-run] cp -R $src/. $dst/"; else cp -R "$src"/. "$dst"/; fi; }
append_block(){
  local file="$1" snippet="$2"
  if ((DRY)); then echo "[dry-run] ensure AgentForge block in $file"; return; fi
  mkdir -p "$(dirname "$file")"; touch "$file"
  python3 - "$file" "$snippet" <<'PY'
from pathlib import Path
import re,sys
p=Path(sys.argv[1]); s=Path(sys.argv[2]).read_text(); text=p.read_text()
start='<!-- agentforge:lean-routing:start -->'; end='<!-- agentforge:lean-routing:end -->'
text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?', '', text, flags=re.S).rstrip()
p.write_text((text+'\n\n' if text else '')+s.strip()+'\n')
PY
}
if ((GLOBAL)); then
  case "$PLATFORM" in
    claude) SKILL_DIR="$HOME/.claude/skills"; AGENTS="$HOME/.claude/agents"; INST="$HOME/.claude/CLAUDE.md";;
    codex) SKILL_DIR="$HOME/.agents/skills"; AGENTS="$HOME/.codex/agents"; INST="$HOME/.codex/AGENTS.md";;
    gemini) SKILL_DIR="$HOME/.agents/skills"; AGENTS="$HOME/.gemini/agents"; INST="$HOME/.gemini/GEMINI.md"; CMDS="$HOME/.gemini/commands";;
  esac
else
  TARGET="$(cd "$TARGET" && pwd)"
  case "$PLATFORM" in
    claude) SKILL_DIR="$TARGET/.claude/skills"; AGENTS="$TARGET/.claude/agents"; INST="$TARGET/CLAUDE.md";;
    codex) SKILL_DIR="$TARGET/.agents/skills"; AGENTS="$TARGET/.codex/agents"; INST="$TARGET/AGENTS.md";;
    gemini) SKILL_DIR="$TARGET/.agents/skills"; AGENTS="$TARGET/.gemini/agents"; INST="$TARGET/GEMINI.md"; CMDS="$TARGET/.gemini/commands";;
  esac
fi
for skill in "$ROOT/skills"/*; do
  if [[ -d "$skill" ]]; then
    copy_tree "$skill" "$SKILL_DIR/$(basename "$skill")"
  fi
done
copy_tree "$ROOT/adapters/$PLATFORM/agents" "$AGENTS"
case "$PLATFORM" in
  claude) append_block "$INST" "$ROOT/adapters/claude/CLAUDE.md.snippet";;
  codex) append_block "$INST" "$ROOT/adapters/codex/AGENTS.md.snippet";;
  gemini) append_block "$INST" "$ROOT/adapters/gemini/GEMINI.md.snippet"; copy_tree "$ROOT/adapters/gemini/commands" "$CMDS";;
esac
printf 'AgentForge installed for %s\nSkills: %s\nAgents: %s\nInstructions: %s\n' "$PLATFORM" "$SKILL_DIR" "$AGENTS" "$INST"
