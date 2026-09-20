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
