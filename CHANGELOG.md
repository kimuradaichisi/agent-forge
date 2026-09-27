# Changelog

## Unreleased

- Fixed three `SKILL.md` descriptions that were invalid YAML and prevented the skills from loading.
- Skill descriptions now state when to use each skill; every `SKILL.md` documents its bundled scripts, references and templates.
- Documented a parent-performs-the-step fallback when `cheap-*` workers are unavailable.
- Fixed the skill name in `AGENTS.md` (`gemini-lean-routing` -> `lean-routing`).
- `check_boundary.py`: files inside new untracked directories are now checked individually (previously reported as the directory, always a violation).
- `scan_diff.py`: new `--allow-print GLOB` option to exempt intentional CLI output from the debug-print check (secrets and breakpoints are still reported).
- Added unit tests (`tests/`, `make test`).
- Added uv/ruff/shellcheck tooling, `make check` quality gate (incl. `*:Zone.Identifier` cleanup), code-size rules, and `make skills-link`.

## 0.1.0 - 2026-09-20

- Initial AgentForge monorepo.
- Added platform-neutral `lean-routing`, `codebase-cartographer`, `scientific-debugging`, `spec-driven-dev`, and `pr-guardian` skills.
- Added cost-aware Triage (Fast-Path vs. Strict Gate) to `scientific-debugging`.
- Added Claude Code, Codex, and Gemini CLI adapters with `/debug`, `/spec`, `/pr`, and `/map` command support.
- Added idempotent project/global installers and uninstallers (Bash & PowerShell).
- Added validation and packaging scripts plus GitHub Actions validation.


