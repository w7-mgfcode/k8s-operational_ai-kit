#!/usr/bin/env python3
"""Resolve every path an instruction file cites against the real tree.

Plausibility cannot be assessed by reading — plausibility is what got the file
accepted in the first place. So resolve, count, and report a truth percentage.

Usage:  python3 audit.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = ROOT / "rules"

# Paths appear in backticks, as globs, or as bare filenames with an extension.
CITED = re.compile(r"`([^`\s]+\.[A-Za-z0-9]{1,5}|[^`\s]*/[^`\s]*)`")

overall_hit = overall_total = 0
suspect = []

for rule in sorted(RULES.glob("*.md")):
    text = rule.read_text(encoding="utf-8")
    prov = re.search(r"^provenance:\s*(.+)$", text, re.M)
    cites = [c for c in CITED.findall(text)]
    hit = sum(1 for c in cites if list(ROOT.glob(c.replace("<name>", "*"))))
    total = len(cites)
    pct = (hit / total * 100) if total else 100.0
    overall_hit += hit
    overall_total += total

    print(f"{rule.name}")
    print(f"  provenance: {prov.group(1) if prov else 'UNRECORDED'}")
    print(f"  cited paths: {hit}/{total} resolve ({pct:.0f}%)")
    for c in cites:
        if not list(ROOT.glob(c.replace("<name>", "*"))):
            print(f"    MISSING  {c}")
    if pct < 50 or not prov:
        suspect.append(rule.name)
    print()

pct = (overall_hit / overall_total * 100) if overall_total else 100.0
print(f"overall: {overall_hit}/{overall_total} cited paths resolve ({pct:.0f}%)")
if suspect:
    print(f"\nsuspect: {', '.join(suspect)}")
    print("Each is internally coherent, externally false, and silent about it.")
    print("The correct action is deletion, not repair — the value was in the")
    print("repository these came from, and it did not travel.")
sys.exit(1 if suspect else 0)
