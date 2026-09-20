#!/usr/bin/env python3
"""Deterministic checker for reproduction tests."""
from __future__ import annotations
import argparse
import subprocess
import sys

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a reproduction command under scientific debugging protocol.")
    parser.add_argument("command", nargs="+", help="The repro command to execute")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--expect-failure", action="store_true", help="Assert that command fails (exit code != 0)")
    group.add_argument("--expect-success", action="store_true", help="Assert that command succeeds (exit code == 0)")
    
    args = parser.parse_args()
    cmd = args.command
    if len(cmd) == 1:
        # If passed as single string, run via shell
        result = subprocess.run(cmd[0], shell=True)
    else:
        result = subprocess.run(cmd)

    code = result.returncode
    if args.expect_failure:
        if code != 0:
            print(f"[Scientific-Debugging] PASS: Repro confirmed failing as expected (exit code {code}).")
            return 0
        else:
            print("[Scientific-Debugging] FAIL: Repro unexpectedly SUCCEEDED (exit code 0). You must create a failing test before modifying code!", file=sys.stderr)
            return 1
    else:
        if code == 0:
            print("[Scientific-Debugging] PASS: Repro succeeded after fix (exit code 0).")
            return 0
        else:
            print(f"[Scientific-Debugging] FAIL: Repro still FAILING after fix (exit code {code}).", file=sys.stderr)
            return 1

if __name__ == "__main__":
    raise SystemExit(main())
