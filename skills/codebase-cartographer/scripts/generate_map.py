#!/usr/bin/env python3
"""Deterministic repository skeleton and map generator.
Zero LLM cost. Uses AST and pattern matching to build compact repo maps.
"""
from __future__ import annotations
import ast
import os
import re
import sys
from pathlib import Path

IGNORE_DIRS = {
    '.git', '.venv', 'venv', '__pycache__', 'node_modules', '.idea',
    '.vscode', 'dist', 'build', '.gemini', '.claude', '.agents', '.codex',
    'coverage', '.pytest_cache', '.tmp'
}

def extract_python_symbols(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding='utf-8')
        tree = ast.parse(content)
    except Exception:
        return []

    symbols: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            method_str = f"({', '.join(methods[:5])}{'...' if len(methods) > 5 else ''})" if methods else ""
            symbols.append(f"class {node.name}{method_str}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(f"def {node.name}()")
    return symbols

def extract_js_ts_symbols(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return []
    symbols: list[str] = []
    for line in content.splitlines():
        line = line.strip()
        m = re.match(r'^(export\s+)?(class|interface|type|function|const|let)\s+([A-Za-z0-9_]+)', line)
        if m:
            kind = m.group(2)
            name = m.group(3)
            symbols.append(f"{kind} {name}")
    return symbols[:10]

def build_map(root: Path) -> str:
    lines: list[str] = [
        "# Codebase Map (Automated Skeleton)",
        f"Root: `{root.resolve().name}`\n",
        "| File | Type | Lines | Key Symbols / Exports |",
        "|---|---|---|---|"
    ]

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.')]
        for f in sorted(filenames):
            if f.startswith('.'):
                continue
            file_path = Path(dirpath) / f
            rel = file_path.relative_to(root)
            ext = file_path.suffix.lower()

            try:
                line_count = len(file_path.read_text(encoding='utf-8', errors='ignore').splitlines())
            except Exception:
                continue

            symbols: list[str] = []
            file_type = ext.lstrip('.') or 'file'

            if ext == '.py':
                symbols = extract_python_symbols(file_path)
            elif ext in ('.js', '.ts', '.jsx', '.tsx'):
                symbols = extract_js_ts_symbols(file_path)
            elif ext in ('.sh', '.ps1', '.toml', '.json', '.yaml', '.yml', '.md'):
                symbols = ['(config/doc/script)']

            sym_str = ", ".join(symbols[:6]) if symbols else "-"
            lines.append(f"| `{rel.as_posix()}` | {file_type} | {line_count} | {sym_str} |")

    return "\n".join(lines)

def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    repo_map = build_map(target)
    print(repo_map)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
