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
