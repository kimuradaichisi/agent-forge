#!/usr/bin/env python3
"""Deterministic git diff scanner for PR hygiene."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from fnmatch import fnmatch

PRINT_PATTERN = r"^\+\s*print\("

DEBUG_PATTERNS = [
    (PRINT_PATTERN, "Python debug print statement"),
    (r"^\+\s*(import\s+pdb|breakpoint\(\))", "Python breakpoint / pdb"),
    (r"^\+\s*console\.(log|debug)\(", "JS/TS console.log statement"),
    (r"^\+\s*debugger;", "JS/TS debugger statement"),
    (r"^\+\s*(fmt\.Println|println!|dbg!)\(", "Go/Rust print/dbg macro"),
]

SECRET_PATTERNS = [
    (r"^\+.*(AIzaSy[0-9A-Za-z-_]{33})", "Google API key leak"),
    (r"^\+.*(sk-[a-zA-Z0-9]{20,})", "OpenAI / standard secret key leak"),
    (r"^\+.*(ghp_[a-zA-Z0-9]{30,})", "GitHub personal token leak"),
]


def read_diff() -> str:
    res = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=False)
    if res.stdout:
        return res.stdout
    # Check staged diff if working tree clean
    res = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=False)
    return res.stdout


def scan_line(line: str, current_file: str, print_allowed: bool) -> list[str]:
    warnings: list[str] = []
    # Check debug code (print() is exempt in files where it is the intended output channel)
    for pat, desc in DEBUG_PATTERNS:
        if (pat != PRINT_PATTERN or not print_allowed) and re.search(pat, line):
            warnings.append(f"DEBUG CODE in {current_file}: {desc} -> {line.strip()}")

    # Check secrets (never exempt)
    for pat, desc in SECRET_PATTERNS:
        if re.search(pat, line):
            warnings.append(f"POSSIBLE SECRET in {current_file}: {desc} -> {line.strip()[:40]}...")
    return warnings


def scan(diff: str, allow_print: Sequence[str] = ()) -> list[str]:
    warnings: list[str] = []
    current_file = ""
    print_allowed = False

    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            print_allowed = any(fnmatch(current_file, pattern) for pattern in allow_print)
            continue

        if not line.startswith("+") or line.startswith("+++"):
            continue

        warnings.extend(scan_line(line, current_file, print_allowed))
    return warnings


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan the git diff for leftover debug code and leaked secrets.")
    parser.add_argument(
        "--allow-print",
        action="append",
        default=[],
        metavar="GLOB",
        help="Do not report print() in files matching GLOB (repo-relative, repeatable), e.g. CLI scripts",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    diff = read_diff()
    if not diff:
        print("[PR-Guardian] Clean: No unstaged or staged git diff detected.")
        return 0

    warnings = scan(diff, allow_print=args.allow_print)
    if warnings:
        print("[PR-Guardian] HYGIENE CHECKS FAILED:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)
        return 1

    print("[PR-Guardian] PASS: Diff hygiene check clean (0 residual debug calls, 0 secrets).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
