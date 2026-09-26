#!/usr/bin/env python3
"""Flag breaking changes in a commit list. Executed, not read.

Its cost to the agent's context is its output, not its source — which is the
whole economic argument for level 3.

Usage:  echo "feat!: drop the v1 endpoint" | python3 detect_breaking.py
"""
import re, sys

MARKERS = (re.compile(r"^[a-z]+(\(.+\))?!:"), re.compile(r"BREAKING[ -]CHANGE", re.I))
out = []
for line in sys.stdin:
    line = line.strip()
    if line and any(m.search(line) for m in MARKERS):
        out.append(line)
print(f"{len(out)} breaking change(s)")
for line in out:
    print(f"  {line}")
