# Platform notes

## Claude Code

Project skills: `.claude/skills/`. Project subagents: `.claude/agents/`. Simple work uses `haiku`; bounded coding uses `sonnet`; reviewer inherits parent. Optional read hook is not auto-registered.

## Codex

Portable skills: `.agents/skills/`. Project custom agents: `.codex/agents/`. Low-cost worker examples use GPT-5.6 Luna; bounded review uses GPT-5.6 Terra. Confirm that worker model IDs are available in your client/account and replace them with a supported model if needed. If a worker cannot run, use deterministic tools or the parent. `config.example.toml` is optional because agents are enabled by default.

Custom-agent directories and model inheritance follow [the official Subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents). Project skill discovery follows [the official Build skills documentation](https://learn.chatgpt.com/docs/build-skills). These checks validate configuration structure, not account access to a model.

## Gemini CLI

Gemini supports `.agents/skills/` as an interoperable alias. Project subagents: `.gemini/agents/`. `/lean` is installed in `.gemini/commands/`. Settings example is documentation only because skills and agents are enabled by default in current Gemini CLI.
