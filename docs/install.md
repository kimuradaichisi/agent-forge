# Installation

Project:

```bash
./installers/install.sh <claude|codex|gemini> /path/to/repository
```

Global:

```bash
./installers/install.sh <platform> --global
```

Global destinations:

- Claude: `~/.claude/skills`, `~/.claude/agents`, `~/.claude/CLAUDE.md`
- Codex: `~/.agents/skills`, `~/.codex/agents`, `~/.codex/AGENTS.md`
- Gemini: `~/.agents/skills`, `~/.gemini/agents`, `~/.gemini/commands`, `~/.gemini/GEMINI.md`

Dry run:

```bash
./installers/install.sh codex . --dry-run
```

Uninstall:

```bash
./installers/uninstall.sh codex .
```
