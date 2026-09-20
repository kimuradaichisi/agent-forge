# AgentForge

Portable engineering workflows for AI coding agents.

AgentForge standardizes **how agents work**, independently from the tools they use. It bundles portable engineering skills:

- **`lean-routing`**: Routes work through the cheapest reliable path (Deterministic tools -> Cheap worker -> Strong reasoning -> Mechanical verification).
- **`scientific-debugging`**: Eliminates trial-and-error code churn by requiring a minimal failing reproduction test before touching any production code.

Adapters are included for Claude Code, OpenAI Codex, and Gemini CLI. The core skills are platform-neutral; model names and CLI-specific wiring live only in adapters.

## Quick start

### Bash (macOS / Linux / WSL)

Project install:

```bash
./installers/install.sh claude .
./installers/install.sh codex .
./installers/install.sh gemini .
```

Global install:

```bash
./installers/install.sh claude --global
./installers/install.sh codex --global
./installers/install.sh gemini --global
```

Preview:

```bash
./installers/install.sh gemini . --dry-run
```

Uninstall:

```bash
./installers/uninstall.sh gemini .
```

### PowerShell (Windows)

Project install:

```powershell
.\installers\install.ps1 claude .
.\installers\install.ps1 codex .
.\installers\install.ps1 gemini .
```

Global install:

```powershell
.\installers\install.ps1 gemini -Global
```

Preview & Uninstall:

```powershell
.\installers\install.ps1 gemini . -DryRun
.\installers\uninstall.ps1 gemini .
```

## Default routing

| Route | Claude | Codex | Gemini |
|---|---|---|---|
| cheap ops | Haiku | GPT-5.6 Luna / low | Gemini 2.5 Flash-Lite |
| tiny edits | Haiku | GPT-5.6 Luna / low | Gemini 2.5 Flash-Lite |
| bounded coding | Sonnet | GPT-5.6 Luna / medium | Gemini 2.5 Flash |
| review | inherit parent | GPT-5.6 Terra / high | inherit parent |
| architecture / ambiguity | parent | parent | parent |

## Repository structure

```text
agent-forge/
├── skills/
│   ├── lean-routing/          # cost-aware delegation
│   └── scientific-debugging/  # hypothesis-driven bug fixing
├── adapters/
│   ├── claude/             # model + subagent wiring
│   ├── codex/
│   └── gemini/
├── installers/
├── registry/
├── scripts/
├── docs/
└── examples/
```

## Design rule

```text
AgentForge = HOW agents work
External tools = WHAT agents can use
```

AgentForge does not depend on proprietary repository-analysis tools. `rg`, Git, tests, parsers and static analysis are sufficient for the base workflow.

## Safe installation

The installer copies AgentForge-owned files and appends a marker-delimited policy block to `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`. It does **not** replace the whole instruction file. Re-running installation is idempotent.

Codex and Gemini share the interoperable `.agents/skills/lean-routing` location. Claude receives the same core skill under `.claude/skills/lean-routing`.

## Validate

```bash
python3 scripts/validate.py
# or
make check
```

## License

MIT
