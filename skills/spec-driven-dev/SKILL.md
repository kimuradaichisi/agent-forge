---
name: spec-driven-dev
description: Specification-driven development with Given-When-Then acceptance criteria, a locked file boundary, and Red-First TDD. Use when implementing a new feature or changing existing behavior, before writing any production code.
---

# Spec-Driven Development Skill

This skill combines the best practices of specification consensus (Copilot Workspace), file boundary locking (SWE-agent / Devin), and strict Test-Driven Development (TDD).

## The Core Principles

1. **No Code Without Spec**: Never implement features without an approved, structured Acceptance Criteria manifest.
2. **Boundary Lock**: Declare explicitly which files may be touched. Any edits outside this boundary are rejected.
3. **Red-First Discipline**: Write the test case first and execute it to see it FAIL before implementing production code.

---

## 5-Step Protocol

```text
Step 1: Spec & Criteria (L1: cheap-ops)
  │  Break requirements into Given-When-Then acceptance criteria.
  ▼
Step 2: Boundary Declaration (L4: Parent)
  │  Enumerate exact files allowed to be created or modified.
  │  Lock out untouched modules to prevent accidental regression.
  ▼
Step 3: Test-First / RED (L2: cheap-coder)
  │  Write test cases asserting the new behavior.
  │  Run tests -> MUST FAIL (assert expected failure mode).
  ▼
Step 4: Minimal Implementation / GREEN (L2: cheap-coder)
  │  Write only enough code within allowed boundary to pass the tests.
  │  Run tests -> MUST PASS.
  ▼
Step 5: Refactor & Verify (L2 / L4)
  │  Clean up implementation without changing behavior.
  │  Run full test suite to guarantee zero regression.
```

---

## Delegation to Lean Routing

- **Step 1 (Spec & Acceptance Criteria)**: Delegate draft generation to `cheap-ops`. Parent reviews and approves.
- **Step 2 (Boundary Lock)**: Parent model declares the file boundary.
- **Step 3 (Test Writing)**: Delegate to `cheap-coder` following pattern.
- **Step 4 (Implementation)**: Delegate to `cheap-coder`.
- **Step 5 (Refactor & Suite Run)**: `cheap-coder` + deterministic test verification.

---

## Deliverable: Spec Manifest

Every feature implementation must produce a structured `spec-manifest.md`:
- **Goal & User Story**
- **Acceptance Criteria (Given-When-Then)**
- **Declared File Boundary**
- **Test Command & Proof of Red -> Green transition**

---

## Tools

Paths are relative to this skill's directory (the folder containing this `SKILL.md`, e.g. `.claude/skills/spec-driven-dev` or `.agents/skills/spec-driven-dev`). Run commands from the target repository root.

| Step | Command / file |
|---|---|
| Spec manifest (Steps 1-2) | Fill [templates/spec-manifest.md](templates/spec-manifest.md) |
| Red / Green proof (Steps 3-4) | Run the project's test command; the Red run must exit non-zero before implementation |
| Boundary check (Steps 4-5) | `python3 <skill-dir>/scripts/check_boundary.py <allowed-file>...` — fails (exit 1) if `git status` shows any file outside the list |
| TDD details | [references/tdd-protocol.md](references/tdd-protocol.md) |
