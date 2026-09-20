# Platform notes

## Claude Code

Project skills: `.claude/skills/`. Project subagents: `.claude/agents/`. Simple work uses `haiku`; bounded coding uses `sonnet`; reviewer inherits parent. Optional read hook is not auto-registered.

## Codex

Portable skills: `.agents/skills/`. Project custom agents: `.codex/agents/`. Low-cost work uses GPT-5.6 Luna; bounded review uses GPT-5.6 Terra. `config.example.toml` is optional because agents are enabled by default.

## Gemini CLI

Gemini supports `.agents/skills/` as an interoperable alias. Project subagents: `.gemini/agents/`. `/lean` is installed in `.gemini/commands/`. Settings example is documentation only because skills and agents are enabled by default in current Gemini CLI.
