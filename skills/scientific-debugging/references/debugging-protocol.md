# Detailed Scientific Debugging Protocol

## Step 1: Collect & Isolate
- Extract exact error messages, stack traces, and relevant context.
- Identify the last known working state (`git log`, `git bisect` hint).
- Do NOT guess what might have caused it before reading the trace.

## Step 2: Create Failing Repro (Strict Gate)
- Create a test file or minimal standalone script (e.g. `tests/repro_issue_<name>.py` or `scratch/repro.sh`).
- The repro must execute the failing code path with minimal dependencies.
- **Verification**: Run the repro. It MUST fail with the expected error.
  - If it does not fail, your reproduction is invalid or the bug has different prerequisites. Do NOT proceed to Step 3.

## Step 3: Formulate Single Hypothesis
- Analyze the failure mechanism.
- State explicitly:
  1. Root cause mechanism (e.g., "Off-by-one index when list length is 0").
  2. Predicted change (e.g., "Add guard check before indexing").
  3. Predicted outcome (e.g., "Repro test will exit 0 without IndexError").

## Step 4: Minimal Atomic Fix
- Apply the edit strictly to the identified root cause location.
- Prohibit scope creep:
  - No style refactoring.
  - No "while I'm here" changes.
  - No speculative optimizations.

## Step 5: Dual Verification
1. Run the repro case: MUST exit 0 (pass).
2. Run project tests: Full suite must pass without regressions.
3. If new failures appear, revert fix and return to Step 3.
