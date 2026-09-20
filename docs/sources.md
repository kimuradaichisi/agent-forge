# Platform source notes

Adapter paths/capabilities were checked against current platform documentation on 2026-09-20.

- Codex: repository skills under `.agents/skills`; project custom agents under `.codex/agents`; multi-agent enabled by default.
- Gemini CLI: `.agents/skills` is a supported alias; project subagents under `.gemini/agents`; custom commands under `.gemini/commands`; skills and agents enabled by default.
- Claude Code: project skills under `.claude/skills`; project subagents under `.claude/agents`; project/user `CLAUDE.md` files provide persistent instructions.
