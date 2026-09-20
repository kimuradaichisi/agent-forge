#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-}"
MAX_LINES="${AGENTFORGE_MAX_DIRECT_READ_LINES:-500}"
[[ -n "$TARGET" && -f "$TARGET" ]] || exit 0
LINES=$(wc -l < "$TARGET" | tr -d ' ')
if (( LINES > MAX_LINES )); then
  printf '%s
' "[AgentForge] Large full-file read: $TARGET ($LINES lines). Prefer targeted search/read or cheap-ops first."
  exit 2
fi
