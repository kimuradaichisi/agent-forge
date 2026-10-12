# Agent Guidelines

## Code Rules (hard limits)

- File: **<= 300 lines**. Function / method: **<= 30 lines**. Parameters: **<= 5** (excluding `self` / `cls`).
- Enforced by `make check` (`scripts/check_code_rules.py` + ruff `PLR0913`). Refactor instead of suppressing.
- Run `make check` before finishing any change; it also deletes stray `*:Zone.Identifier` files.

## Cost-aware Gemini routing

For repository and engineering work, use the portable `lean-routing` skill. In Gemini CLI, the legacy `gemini-lean-routing` skill may be used when available. Apply only the active platform's worker names and models; in Codex use `cheap_ops`, `cheap_edit`, and `cheap_coder`. If the configured workers or models are unavailable, execute deterministic work directly and keep judgment with the parent.

- Prefer deterministic tools before model reasoning.
- Do not spawn a subagent for a single trivial tool call when direct execution is cheaper.
- Delegate repetitive, read-heavy, high-volume, or structured extraction work to `cheap-ops` (`gemini-2.5-flash-lite`).
- Delegate tiny exact edits with explicit acceptance criteria to `cheap-edit` (`gemini-2.5-flash-lite`).
- Delegate small pattern-following implementation to `cheap-coder` (`gemini-2.5-flash`).
- Use `reviewer` or the parent for bounded reasoning-heavy review.
- Keep architecture, ambiguous requirements, security-sensitive changes, migrations, concurrency, persistence semantics, and cross-cutting design in the parent.
- Cheap agents must return `ESCALATE` rather than guess.
- Prefer deterministic verification over another LLM call.

## Codebase Cartographer

When exploring, onboarding, or investigating repository structure, use the `codebase-cartographer` skill.

- **Strict Rule**: NEVER perform mass full-file reads to explore. Run `generate_map.py` first (L0 / Zero cost).
- Use the symbol skeleton to orient yourself, locate entry points, and guide targeted slice reads.
- Always trigger before `spec-driven-dev` (to set boundaries) and `scientific-debugging` (to trace callers).

## Scientific Debugging

When investigating bugs, errors, or test failures, use the `scientific-debugging` skill.

- **Triage First**:
  - *Fast-Path (Obvious Fix)*: For typos, syntax errors, or unambiguous stack traces, apply a 1-line atomic fix immediately and verify.
  - *Strict Gate (Non-Trivial / Logic / Regressions)*: If the root cause is non-obvious or if a fast-path attempt fails, NEVER modify application code until you have created a minimal reproduction test case that demonstrably FAILS.
- Formulate a single root-cause hypothesis before making any code change.
- Make the smallest atomic fix addressing only the root cause.
- Deterministically verify that the reproduction test passes and the full test suite suffers no regressions.

## Spec-Driven Development

When implementing new features or modifying behavior, use the `spec-driven-dev` skill.

- Establish Given-When-Then acceptance criteria before coding.
- Declare and lock the file boundary; reject edits to unapproved files.
- Enforce Red-First for code behavior changes. The evidence-backed one-line Fast-Path in Scientific Debugging takes precedence for obvious fixes; documentation-only changes use document checks.

## PR Guardian

Before shipping or opening a pull request, use the `pr-guardian` skill.

- Clean diffs of residual debug code (`print`, `console.log`, `debugger`).
- Check for leaked secrets or keys.
- Perform blast-radius caller analysis on modified symbols using `rg`.
- Generate structured PR verification summary.

<!-- agentforge:lean-routing:start -->
## AgentForge Workflows

### 1. Lean Routing
Use the `lean-routing` skill for engineering tasks where cost-aware delegation applies:
- Use direct tools for small exact tasks. If configured workers/models are unavailable, use tools or the parent and report the limitation; never substitute Gemini-only models.
- Prefer deterministic tools before model reasoning.
- Do not spawn a subagent for a single trivial tool call when direct execution is cheaper.
- Delegate repetitive, read-heavy, high-volume, or structured extraction work to `cheap_ops`.
- Delegate tiny exact edits with explicit acceptance criteria to `cheap_edit`.
- Delegate small pattern-following implementation to `cheap_coder`.
- Use `reviewer` or the parent for bounded reasoning-heavy review.
- Keep architecture, ambiguous requirements, security-sensitive changes, migrations, concurrency, persistence semantics, and cross-cutting design in the parent.
- Cheap agents must return `ESCALATE` rather than guess.
- Prefer deterministic verification over another LLM call.

### 2. Codebase Cartographer (Exploration & Orientation)
When exploring, onboarding, or understanding architecture, use `codebase-cartographer`:
- **Strict rule**: NEVER read dozens of full files blindly. Run `generate_map.py` first (L0 / Zero cost).
- Use the symbol skeleton to orient yourself, locate entry points, and guide targeted reads.
- Triggers before `spec-driven-dev` (to set boundaries) and `scientific-debugging` (to trace callers).

### 3. Spec-Driven Development
When building features or modifying behavior, use the `spec-driven-dev` skill:
- Formulate Given-When-Then acceptance criteria before writing code.
- Explicitly declare the allowed file boundary (use cartographer first); never edit files outside the boundary.
- Write tests first and verify they FAIL (Red) before implementing code (Green). For bug fixes, Scientific Debugging's evidence-backed one-line Fast-Path takes precedence; documentation-only changes use document checks.

### 4. Scientific Debugging
When investigating bugs, errors, or test failures, use the `scientific-debugging` skill:
- **Triage First**:
  - *Fast-Path (Obvious Fix)*: For typos, syntax errors, or unambiguous stack traces, apply a 1-line atomic fix immediately and verify.
  - *Strict Gate (Non-Trivial / Logic / Regressions)*: If the cause is non-obvious or if a fast-path attempt fails, NEVER touch application code until you have created a minimal repro test that demonstrably FAILS.
- Formulate a single root-cause hypothesis before editing.
- Apply the smallest atomic fix addressing only the root cause.
- Verify deterministically that the repro passes and no regressions occur.

### 5. PR Guardian
Before shipping or submitting a PR, use the `pr-guardian` skill:
- Remove temporary debug prints and breakpoints; intended CLI output and product logging are valid. Review tracked and new files for secrets; scanner output is a heuristic, not comprehensive proof.
- Perform blast-radius caller analysis on modified symbols using `rg`.
- Generate a structured `pr-manifest.md` ready for review.
<!-- agentforge:lean-routing:end -->
