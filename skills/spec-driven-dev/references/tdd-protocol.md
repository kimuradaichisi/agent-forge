# Detailed TDD & Boundary Protocol

## Step 1: Acceptance Criteria (Given-When-Then)
State each requirement clearly:
- **Given**: Initial context / state.
- **When**: Action triggered.
- **Then**: Expected observable outcome or side-effect.

## Step 2: File Boundary Definition
- Explicitly list target files (e.g., `src/auth.py`, `tests/test_auth.py`).
- Prohibit modifications to files outside the declared list.
- If a dependency outside the boundary requires changes, STOP and ESCALATE to the parent model to expand the boundary.

## Step 3: Red Phase (Verification of Test Failure)
- Run the test suite on the newly created test.
- The test must fail for the expected reason (e.g., `AttributeError: no method 'foo'`).
- If the test passes before implementation, the test is invalid or the feature already exists!

## Step 4: Green Phase (Minimal Implementation)
- Write minimal code to satisfy the test assertions.
- Do not add speculative options, premature abstractions, or extra features.

## Step 5: Refactor & Dual Verification
1. Clean code formatting, comments, and structure.
2. Run newly added test -> MUST PASS.
3. Run full project test suite -> MUST PASS (0 regressions).
