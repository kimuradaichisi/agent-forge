#!/usr/bin/env python3
"""Small deterministic routing hint. Intentionally conservative."""
from __future__ import annotations
import sys

DIRECT=("git status","rg ","grep ","run test","format","lint")
CHEAP=("scan","summarize","extract","classify","inventory","rename","normalize")
STRONG=("architecture","design","trade-off","tradeoff","ambiguous","security","migration","concurrency","distributed","debug")

def classify(task: str) -> str:
    t=task.lower().strip()
    if any(x in t for x in STRONG): return "L4_PARENT"
    if any(x in t for x in CHEAP): return "L1_CHEAP_WORKER"
    if any(x in t for x in DIRECT): return "L0_DIRECT"
    return "L2_OR_L3_INSPECT_SCOPE"

def main() -> int:
    if len(sys.argv)<2:
        print("usage: route_task.py <task>", file=sys.stderr); return 2
    print(classify(" ".join(sys.argv[1:]))); return 0

if __name__=="__main__": raise SystemExit(main())
