# Agent Guidelines

## Cost-aware Gemini routing

For repository and engineering work, use the `gemini-lean-routing` skill when applicable.

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
- Enforce Red-First (write failing tests before implementation).

## PR Guardian

Before shipping or opening a pull request, use the `pr-guardian` skill.

- Clean diffs of residual debug code (`print`, `console.log`, `debugger`).
- Check for leaked secrets or keys.
- Perform blast-radius caller analysis on modified symbols using `rg`.
- Generate structured PR verification summary.
