# Routing Policy

## L0 — Direct deterministic

One exact grep, known-file read, named test command, formatter, or explicitly specified one-line change. Execute directly when subagent overhead would cost more.

## L1 — Cheap ops / cheap edit

Low judgment, bounded scope, predictable output: multi-file scans, large diff/log summaries, explicit extraction/classification, exact scoped renames, config/doc normalization.

## L2 — Cheap coder

Small code changes with a visible existing pattern and explicit acceptance criteria: adjacent adapter, straightforward tests, local behavior-preserving refactor, small established CLI option.

## L3 — Reviewer / parent

Bounded but interpretation-heavy work: regression analysis, side-effect review, conflicting evidence, non-obvious test failure diagnosis.

## L4 — Parent only

Architecture, ambiguous requirements, security, migration semantics, concurrency/distributed state, broad redesign, cross-domain ownership.

## Spawn threshold

Do not delegate a single trivial operation. Delegate when it reduces parent context, combines multiple tool turns, handles volume, or isolates repetitive work.
