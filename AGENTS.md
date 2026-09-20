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

## Scientific Debugging

When investigating bugs, errors, or test failures, use the `scientific-debugging` skill.

- **Strict Gate**: Never modify application code until you have created a minimal reproduction test case that demonstrably FAILS.
- Formulate a single root-cause hypothesis before making any code change.
- Make the smallest atomic fix addressing only the root cause.
- Deterministically verify that the reproduction test passes and the full test suite suffers no regressions.

