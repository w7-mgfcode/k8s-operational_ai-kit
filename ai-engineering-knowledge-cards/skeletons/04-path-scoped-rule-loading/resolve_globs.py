#!/usr/bin/env python3
"""Resolve every scoped rule's globs against the real tree.

This is the highest-value check in the pattern. A glob that matches nothing is
a rule that never loads and cannot announce its own uselessness.

Usage:  python3 resolve_globs.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = ROOT / "rules"
INDEX = RULES / "README.md"


def globs_of(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return []
    fm = text.split("---", 2)[1]
    return re.findall(r'^\s*-\s*"([^"]+)"', fm, re.M)


errors = warnings = 0
indexed = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""

for rule in sorted(RULES.glob("*.md")):
    if rule.name == "README.md":
        continue
    gs = globs_of(rule)
    if not gs:
        print(f"ERROR   {rule.name}: no paths frontmatter — this rule can never load")
        errors += 1
        continue
    for g in gs:
        hits = list(ROOT.glob(g))
        if hits:
            print(f"ok      {rule.name:<20} {g:<28} -> {len(hits)} file(s)")
        else:
            print(f"ERROR   {rule.name:<20} {g:<28} -> DEAD: matches nothing")
            errors += 1
    if f"`{rule.name}`" not in indexed:
        print(f"WARN    {rule.name}: not in the index — invisible to agents")
        print( "        without glob loading (see card 01's vendor B)")
        warnings += 1

print(f"\n{errors} dead/unloadable, {warnings} unindexed")
if errors:
    print("A rules file that lies to the agent is worse than none.")
sys.exit(1 if errors else 0)
