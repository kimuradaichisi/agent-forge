---
name: scientific-debugging
description: Hypothesis-driven debugging protocol with cost-aware fast-path triage. Enforces reproduction tests for non-trivial bugs while bypassing overhead for obvious fixes.
---

# Scientific Debugging Skill

This skill enforces disciplined, hypothesis-driven debugging for AI coding agents. It prevents expensive trial-and-error code churn ("flailing") while avoiding unnecessary overhead on trivial fixes.

---

## The Triage Rule: Fast-Path vs. Strict Gate

When an error or test failure occurs, perform an instant **Triage**:

```text
[Bug / Error Detected]
         │
         ▼
 ┌───────────────┐
 │ Triage Check  │
 └───────┬───────┘
         ├────────────────────────────────────────┐
         ▼                                        ▼
  [A. Obvious / Trivial Fix]            [B. Non-Trivial / Logic Bug]
  - Syntax error, typo, missing import  - Root cause not 100% obvious
  - Stack trace pinpoint is indisputable- Involves logic or edge cases
  - 1-2 line localized edit             - Previous fix attempt failed!
         │                                        │
         ▼                                        ▼
   【Fast-Path】                            【Strict Gate】
   - Skip repro test creation               - NEVER touch app code until
   - Apply atomic fix immediately (cheap-edit)a minimal repro test FAILS
   - Deterministic verification (lint/test) - Form single hypothesis
                                            - Atomic fix + Dual verify
```

---

## The Fast-Path Protocol (Trivial Bugs)

Use this to avoid token overhead on self-evident issues:
1. **Verify Evidence**: Stack trace or linter message unambiguously specifies the exact fix.
2. **Apply Atomic Edit**: Delegate directly to `cheap-edit` or apply one-line fix.
3. **Verify Locally**: Run compiler, linter, or existing affected test.
4. **Escalation Trigger**: **If the fast-path fix fails or error persists, you MUST IMMEDIATELY ESCALATE to the Strict Gate.** Never attempt a second speculative guess.

---

## The Strict Gate Protocol (Non-Trivial Bugs)

For all logic bugs, obscure crashes, regressions, or when a fast-path fix failed:

> **STRICT GATE: NEVER touch production/application code until you have a minimal, isolated reproduction test that demonstrably FAILS.**

```text
1. Collect & Isolate (L0 / L1)
   │  Capture error logs, stack traces, and environment state deterministically.
   ▼
2. Create Failing Repro (L1 / L2)
   │  Write the smallest standalone script or test case that reproduces the bug.
   │  Execute it -> MUST exit non-zero (FAIL).
   ▼
3. Form Single Hypothesis (L4 Parent)
   │  Identify root cause with highest causal probability.
   │  Predict WHY the repro fails and HOW the fix will turn it green.
   ▼
4. Minimal Atomic Fix (L1 / L2)
   │  Apply the smallest targeted edit addressing the root cause only.
   │  Do not refactor adjacent code.
   ▼
5. Dual Verification (L0)
   │  Run repro test -> MUST PASS.
   │  Run entire test suite -> NO REGRESSIONS.
```

---

## Delegation to Lean Routing

- **Triage & Fast-Path**: `cheap-edit` for immediate obvious fix + direct tool verification.
- **Step 1 (Logs & Trace)**: Deterministic tools (`rg`, git) or `cheap-ops` for large logs.
- **Step 2 (Repro Creation)**: `cheap-coder` or parent to craft minimal test (`tests/repro_*.py`).
- **Step 3 (Root Cause)**: Parent model performs causal reasoning.
- **Step 4 (Targeted Fix)**: `cheap-edit` for localized fix.
- **Step 5 (Verification)**: Deterministic test command execution.

---

## Deliverable: Repro Manifest (for Strict Gate)

Every non-trivial debugging session must conclude with:
- **Repro Command / File**: How to reproduce.
- **Root Cause**: Why it happened.
- **Fix Summary**: What was changed.
- **Verification Evidence**: Proof of repro pass and suite pass.
