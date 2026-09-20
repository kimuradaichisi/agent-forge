# Guidelines for Writing Minimal Reproduction Cases

## Criteria for a Quality Repro

1. **Deterministic**: Fails 100% of the time under the same conditions (no flaky sleep timing).
2. **Minimal**: Zero unnecessary dependencies or imports. Only the failing unit/component.
3. **Automated**: Can be executed via single CLI command (e.g. `pytest tests/repro_xxx.py` or `python repro.py`).
4. **Self-asserting**: Fails with non-zero exit code or assertion failure; exits 0 on success.

## Patterns by Language / Framework

### Python
```python
# tests/test_repro_issue.py
import pytest
from my_package.module import target_function

def test_repro_issue_case():
    # Arrange minimal input that triggered bug
    payload = {"key": None}
    
    # Act & Assert
    result = target_function(payload)
    assert result == expected_value
```

### TypeScript / JavaScript (Jest / Vitest)
```typescript
import { targetFunction } from '../src/module';

describe('repro issue', () => {
  it('should handle edge case without throwing', () => {
    expect(() => targetFunction(null)).not.toThrow();
  });
});
```

### Shell / CLI tools
```bash
#!/usr/bin/env bash
set -euo pipefail
# Execute binary with offending flag
./my-cli --flag-that-crashes
```
