---
name: scientific-debugging
description: Hypothesis-driven debugging protocol. Enforces creating a minimal reproduction test before modifying any production code.
---

# Scientific Debugging Skill

This skill enforces disciplined, hypothesis-driven debugging for AI coding agents. It eliminates trial-and-error code churn and hallucinated "fixes" by requiring deterministic failure reproduction before any fix is applied.

## The Cardinal Rule

> **NEVER touch production/application code until you have a minimal, isolated reproduction test that demonstrably FAILS.**

If you change application code before seeing a failing test or deterministic error reproduction, you are guessing. Guessing consumes tokens, introduces regressions, and destroys debug state.

---

## 5-Step Protocol

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
5. Deterministic Verification (L0)
   │  Run repro test -> MUST PASS.
   │  Run entire test suite -> NO REGRESSIONS.
```

---

## Delegation to Lean Routing

- **Step 1 (Logs & Trace)**: Run deterministic tools directly (`rg`, `git log`, inspect log files). Use `cheap-ops` if logs are voluminous.
- **Step 2 (Repro Creation)**: Use `cheap-coder` or parent to craft a minimal test in `tests/repro_*.py` or temporary repro script.
- **Step 3 (Root Cause Analysis)**: Parent model performs causal reasoning. Do not delegate root cause analysis of obscure bugs to cheap workers.
- **Step 4 (Targeted Fix)**: Use `cheap-edit` if fix is localized and unambiguous.
- **Step 5 (Verification)**: Deterministic test command execution.

---

## Deliverable: Repro Manifest

Every debugging session must conclude with or output a structured summary:
- **Repro Command / File**: How to reproduce.
- **Root Cause**: Why it happened.
- **Fix Summary**: What was changed.
- **Verification Evidence**: Proof of repro pass and suite pass.
