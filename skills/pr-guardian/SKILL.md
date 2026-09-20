---
name: pr-guardian
description: Pre-ship hygiene scanner, blast-radius analyzer, and automated PR manifest generator.
---

# PR Guardian Skill

This skill enforces high-standard pre-commit / pre-push hygiene and generates comprehensive Pull Request manifests. It borrows blast-radius analysis from Qodo (PR-Agent) and deterministic cleanliness checks from modern pre-commit conventions.

## The Core Principles

1. **Zero Leftover Debug Code**: Prohibit residual `print`, `console.log`, `debugger`, or breakpoint statements.
2. **Blast-Radius Awareness**: Explicitly identify and list all callers/dependents of modified symbols before shipping.
3. **Documentation Parity**: If public APIs or configuration keys changed, corresponding documentation must be updated.
4. **Structured PR Evidence**: Generate a ready-to-merge PR description with verification proof.

---

## 4-Step Protocol

```text
Step 1: Hygiene & Secret Scan (L0: scan_diff.py)
  │  Inspect git diff for leftover debug code, TODOs, and credential leaks.
  ▼
Step 2: Blast-Radius Extraction (L0: rg / ripgrep)
  │  Extract changed symbols and search repository for affected call-sites.
  ▼
Step 3: Doc-Sync Check (L1: cheap-ops)
  │  Verify whether modified APIs, settings, or CLI flags have matching doc updates.
  ▼
Step 4: PR Manifest Generation (L1: cheap-ops)
  │  Compile Why/What/Blast-Radius/Verification into pr-manifest.md.
```

---

## Delegation to Lean Routing

- **Step 1 (Hygiene & Secret Scan)**: Run deterministic `scan_diff.py` directly (Cost: 0).
- **Step 2 (Blast-Radius Extraction)**: Run `rg` directly (Cost: 0).
- **Step 3 (Doc-Sync Check)**: Delegate check to `cheap-ops`.
- **Step 4 (PR Manifest Generation)**: Delegate Markdown formatting to `cheap-ops`.

---

## Deliverable: PR Manifest

Every shipping inspection produces a `pr-manifest.md`:
- **PR Title & Summary**
- **Type of Change (Feature / Fix / Refactor / Docs)**
- **Blast Radius (Impact Analysis)**
- **Hygiene Verification Proof**
- **Reviewer Checklist**
