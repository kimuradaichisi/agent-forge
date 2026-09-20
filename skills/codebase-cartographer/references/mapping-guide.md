# Codebase Exploration Guidelines

## Anti-Patterns to Avoid
1. **Blind Grep without Scope**: Grepping common words across `node_modules` or `.git`.
2. **Mass Full-File Reads**: Calling `view_file` on 10 consecutive 500-line files to find one helper function.
3. **Hallucinated Architecture**: Guessing where a feature lives instead of checking the symbol skeleton.

## Standard Exploration Recipe
1. Run `python <skill_path>/scripts/generate_map.py .` -> Immediate high-level overview.
2. Filter target symbols using `rg -n "def target_function"`.
3. Read ONLY targeted slice (e.g. lines 40-70) using targeted read tools.
4. If working with multi-module tasks, produce or consult `repo-map.md`.
