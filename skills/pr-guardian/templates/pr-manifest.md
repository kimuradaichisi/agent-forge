# Pull Request Manifest

## Title: [prefix]: [Short description]

### 1. Summary & Motivation
- **What**: [Concise summary of changes]
- **Why**: [Business context or problem solved]

### 2. Type of Change
- [ ] 🚀 New Feature (`feat`)
- [ ] 🐛 Bug Fix (`fix`)
- [ ] ♻️ Refactoring (`refactor`)
- [ ] 📝 Documentation (`docs`)
- [ ] ⚡ Performance Optimization (`perf`)

### 3. Blast Radius (Impact Analysis)
- **Modified Core Symbols**:
  - `SymbolName` (in `file:line`)
- **Direct Dependents / Call-Sites**:
  - `CallerFile:line` -> [Impact status: Tested / Unaffected]

### 4. Verification & Hygiene Checklist
- [x] Zero leftover debug statements (`print`, `console.log`, `debugger`).
- [x] Zero hardcoded secrets / API tokens.
- [x] Documentation & comments synchronized with code changes.
- [x] All automated tests passing: `[command]` (`[results]`).
