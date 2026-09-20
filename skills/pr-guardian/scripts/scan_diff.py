#!/usr/bin/env python3
"""Deterministic git diff scanner for PR hygiene."""
from __future__ import annotations
import re
import subprocess
import sys

DEBUG_PATTERNS = [
    (r'^\+\s*print\(', "Python debug print statement"),
    (r'^\+\s*(import\s+pdb|breakpoint\(\))', "Python breakpoint / pdb"),
    (r'^\+\s*console\.(log|debug)\(', "JS/TS console.log statement"),
    (r'^\+\s*debugger;', "JS/TS debugger statement"),
    (r'^\+\s*(fmt\.Println|println!|dbg!)\(', "Go/Rust print/dbg macro"),
]

SECRET_PATTERNS = [
    (r'^\+.*(AIzaSy[0-9A-Za-z-_]{33})', "Google API key leak"),
    (r'^\+.*(sk-[a-zA-Z0-9]{20,})', "OpenAI / standard secret key leak"),
    (r'^\+.*(ghp_[a-zA-Z0-9]{30,})', "GitHub personal token leak"),
]

def main() -> int:
    res = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True)
    diff = res.stdout
    if not diff:
        # Check staged diff if working tree clean
        res = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
        diff = res.stdout

    if not diff:
        print("[PR-Guardian] Clean: No unstaged or staged git diff detected.")
        return 0

    warnings: list[str] = []
    current_file = ""

    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        if not line.startswith("+") or line.startswith("+++"):
            continue

        # Check debug code
        for pat, desc in DEBUG_PATTERNS:
            if re.search(pat, line):
                warnings.append(f"DEBUG CODE in {current_file}: {desc} -> {line.strip()}")

        # Check secrets
        for pat, desc in SECRET_PATTERNS:
            if re.search(pat, line):
                warnings.append(f"POSSIBLE SECRET in {current_file}: {desc} -> {line.strip()[:40]}...")

    if warnings:
        print("[PR-Guardian] HYGIENE CHECKS FAILED:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)
        return 1

    print("[PR-Guardian] PASS: Diff hygiene check clean (0 residual debug calls, 0 secrets).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
