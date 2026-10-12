# Installation

## Linux / macOS / Bash

Project:

```bash
./installers/install.sh <claude|codex|gemini> /path/to/repository
```

Global:

```bash
./installers/install.sh <platform> --global
```

Dry run:

```bash
./installers/install.sh codex . --dry-run
```

Uninstall:

```bash
./installers/uninstall.sh codex .
```

---

## Windows (PowerShell)

Project:

```powershell
.\installers\install.ps1 <claude|codex|gemini> C:\path\to\repository
```

Global:

```powershell
.\installers\install.ps1 <platform> -Global
```

Dry run:

```powershell
.\installers\install.ps1 gemini . -DryRun
```

Uninstall:

```powershell
.\installers\uninstall.ps1 gemini .
```

---

## Global destinations

- Claude: `~/.claude/skills`, `~/.claude/agents`, `~/.claude/CLAUDE.md`
- Codex: `~/.agents/skills`, `~/.codex/agents`, `~/.codex/AGENTS.md`
- Gemini: `~/.agents/skills`, `~/.gemini/agents`, `~/.gemini/commands`, `~/.gemini/GEMINI.md`

## Verify and use

Run `python scripts/validate.py` (Python 3.11+) before installation. On Windows this exercises the PowerShell installers; on Linux/macOS it checks and exercises Bash. The validation runs in a temporary directory and verifies repeat installation, preservation of existing instructions, and removal of the installed instruction block. It does not run paid model calls.

For this repository in Codex, run `.\installers\install.ps1 codex .`. Skills are copied into `.agents/skills/` and can be invoked by name, for example `$lean-routing` or `$codebase-cartographer`. If a skill does not appear, restart Codex. See [official skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).

Install only the adapter for the platform you are using. Review model availability before using custom workers; worker failure falls back to deterministic tools or the parent. Global Codex and Gemini installs share the skill destination, so updating one also updates the shared portable skills.
