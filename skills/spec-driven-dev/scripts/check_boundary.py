#!/usr/bin/env python3
"""Deterministic boundary checker for spec-driven development."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Check if current git modifications respect declared file boundary.")
    parser.add_argument("allowed_files", nargs="+", help="Files allowed to be modified or created")
    args = parser.parse_args()

    allowed = {Path(f).resolve() for f in args.allowed_files}

    # Get modified/created files from git
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"git status error: {res.stderr}", file=sys.stderr)
        return 2

    violating_files: list[str] = []
    for line in res.stdout.splitlines():
        if not line.strip():
            continue
        # Status code is first 2 chars
        path_str = line[3:].strip()
        if " -> " in path_str:
            path_str = path_str.split(" -> ")[1]
        p = Path(path_str).resolve()
        if p not in allowed:
            violating_files.append(path_str)

    if violating_files:
        print("[Spec-Driven-Dev] BOUNDARY VIOLATION DETECTED!", file=sys.stderr)
        print("The following modified files are OUTSIDE your declared boundary:", file=sys.stderr)
        for vf in violating_files:
            print(f"  - {vf}", file=sys.stderr)
        print("Revert changes to these files or escalate to parent to expand the boundary.", file=sys.stderr)
        return 1

    print(f"[Spec-Driven-Dev] PASS: All modifications are strictly within declared boundary ({len(allowed)} file(s) allowed).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
