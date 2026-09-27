# PR Hygiene & Cleanliness Rules

## Prohibited Artifacts in Diffs

1. **Leftover Debug Statements**:
   - Python: `print(`, `breakpoint()`, `import pdb; pdb.set_trace()`
   - JavaScript/TypeScript: `console.log(`, `console.debug(`, `debugger;`
   - Go: `fmt.Println(`, `println(`
   - Rust: `println!(`, `dbg!(`
2. **Leftover TODO / FIXME without Issue Link**:
   - Naked `// TODO` or `# FIXME` comments added without tracking tickets.
3. **Accidental Credential Leaks**:
   - Strings resembling `AIzaSy*`, `sk-*`, `ghp_*`, private keys, or `.env` files.
4. **Noise / Formatting Artifacts**:
   - Unintended mass whitespace changes or mixed line endings (CRLF vs LF).

## Known False Positives (`scan_diff.py`)

- **Intentional CLI output**: `scan_diff.py` matches every added line starting with `print(`, including the real output of command-line scripts (usage messages, PASS/FAIL reports). Exempt those files with `--allow-print GLOB` (repeatable, repo-relative `fnmatch` glob where `*` also matches `/`). Do not delete intentional output to silence the scan. Secrets and breakpoints are never exempted.
- **Reformatting**: an auto-formatter that rewraps an existing `print(` call re-adds it to the diff and re-triggers the finding.
