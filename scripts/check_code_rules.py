#!/usr/bin/env python3
"""Enforce AgentForge code-size rules (see CONTRIBUTING.md "Code rules").

- File:     <= 300 lines (Python / shell / PowerShell)
- Function: <= 30 lines, including signature, docstring and decorators (Python)
- Params:   <= 5 per function, excluding self/cls, counting *args/**kwargs (Python)
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_LINES = 300
MAX_FUNCTION_LINES = 30
MAX_PARAMS = 5
CODE_SUFFIXES = {".py", ".sh", ".ps1"}
EXCLUDED_DIRS = {".git", ".venv", "dist", "build", "__pycache__", ".ruff_cache", ".tmp"}


def iter_code_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for base in paths:
        candidates = [base] if base.is_file() else sorted(base.rglob("*"))
        files.extend(
            p
            for p in candidates
            if p.is_file() and p.suffix in CODE_SUFFIXES and not EXCLUDED_DIRS.intersection(p.parts)
        )
    return files


def count_params(node: ast.FunctionDef | ast.AsyncFunctionDef, in_class: bool) -> int:
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    if in_class and positional and positional[0].arg in {"self", "cls"}:
        positional = positional[1:]
    return len(positional) + len(args.kwonlyargs) + bool(args.vararg) + bool(args.kwarg)


def check_functions(tree: ast.AST, rel: str) -> list[str]:
    errors: list[str] = []
    class_members = {id(child) for node in ast.walk(tree) if isinstance(node, ast.ClassDef) for child in node.body}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        start = min([node.lineno, *(d.lineno for d in node.decorator_list)])
        length = (node.end_lineno or node.lineno) - start + 1
        if length > MAX_FUNCTION_LINES:
            errors.append(f"{rel}:{node.lineno}: function '{node.name}' has {length} lines (max {MAX_FUNCTION_LINES})")
        params = count_params(node, id(node) in class_members)
        if params > MAX_PARAMS:
            errors.append(f"{rel}:{node.lineno}: function '{node.name}' has {params} params (max {MAX_PARAMS})")
    return errors


def check_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    line_count = len(text.splitlines())
    if line_count > MAX_FILE_LINES:
        errors.append(f"{rel}: file has {line_count} lines (max {MAX_FILE_LINES})")
    if path.suffix == ".py":
        errors.extend(check_functions(ast.parse(text, filename=rel), rel))
    return errors


def main() -> int:
    targets = [Path(a).resolve() for a in sys.argv[1:]] or [ROOT]
    files = iter_code_files(targets)
    errors = [e for f in files for e in check_file(f)]
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        print(f"{len(errors)} code-rule violation(s)")
        return 1
    print(f"Code rules PASS ({len(files)} file(s) checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
