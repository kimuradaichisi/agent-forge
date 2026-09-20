---
name: lean-routing
description: Cost-aware engineering workflow. Use for repository exploration, coding, refactoring, review, documentation, or repetitive engineering work where deterministic tools and cheap workers should be preferred before expensive reasoning. Cheap workers must escalate ambiguity instead of guessing.
---

# Lean Routing

Route every engineering task through the cheapest reliable execution path.

## Order

1. **ELIMINATE** unnecessary work.
2. **DETERMINISTIC** tools before models.
3. **CHEAP WORKER** for bounded, repetitive, high-volume work.
4. **REASON** with the parent/strong model only when judgment is required.
5. **VERIFY** mechanically whenever possible.

## R0 — Eliminate

Before reading, generating, or delegating, ask whether the step is needed, whether the answer is already in context, and whether the output can be smaller.

## R1 — Deterministic first

Prefer exact tools for exact questions:

- `rg` / grep / find / glob
- Git diff / history / blame
- parser / AST / LSP / symbol index
- dependency graph
- formatter / linter / type checker
- tests / schema validation / static analysis

A single trivial command should normally be run directly by the parent rather than spawning a subagent.

## R2 — Cheap worker

Delegate when work is self-contained and large, repetitive, predictable, mechanically verifiable, or likely to pollute parent context.

- `cheap-ops`: search, scan, extract, inventory, summarize evidence; read-only.
- `cheap-edit`: tiny exact edits with explicit targets and acceptance criteria.
- `cheap-coder`: small pattern-following implementation or local behavior-preserving refactor.

Every delegation must specify narrow goal, explicit scope, expected output, forbidden decisions, evidence requirements, and escalation conditions.

## R3 — Parent / strong reasoning

Keep these with the parent or stronger reviewer:

- architecture and boundary decisions;
- contradictory or missing requirements;
- difficult debugging;
- cross-module ownership decisions;
- security/auth/privacy-sensitive behavior;
- persistent-data or schema migration semantics;
- concurrency, distributed state, ordering, transactions;
- business/technical trade-offs;
- materially different valid implementations.

## Escalation contract

When cheap work reaches material ambiguity, stop and return:

```text
ESCALATE
Reason: ...
Evidence: ...
Smallest next question/decision: ...
```

Do not burn repeated cheap-model calls on a task that actually needs judgment.

## R4 — Verification

Prefer targeted tests, then formatter/lint/type/static checks, focused diff review, and only then broader tests when impact warrants it.

Review classes:

- `BLOCKER`
- `SHOULD FIX`
- `DEFER`

Proceed only when `BLOCKER = 0` and the deterministic quality gate passes. A model saying “looks good” is not a quality gate.

## Zero-point avoidance

Define failure before optimization. Typical zero-point conditions include wrong-file modification, ignoring an explicit path, unintended public behavior change, unsupported inference presented as fact, destructive action without approval, regression, or omitted verification.

## Parent workflow

```text
Task
  -> unnecessary?                 -> eliminate
  -> one exact deterministic op?  -> execute directly
  -> bounded/repetitive/large?     -> cheap worker
  -> meaningful judgment needed?  -> parent / reviewer
  -> verify deterministically
  -> synthesize only needed evidence
```

## Context policy

Workers return compact evidence so the parent does not automatically re-read everything:

```text
RESULT
Files: ...
Symbols: ...
Findings: ...
Changes: ...
Verification: ...
Uncertainty: none | ...
```

## Retry policy

- Mechanical/tool failure: narrow or reframe once; retry once.
- Ambiguity/judgment failure: escalate immediately.
- Never loop cheap agents until they imitate expensive reasoning.

See `references/routing-policy.md` and `references/escalation-policy.md`.
