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
