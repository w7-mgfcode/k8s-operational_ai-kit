#!/usr/bin/env python3
"""Compare the pack against the repository as it is now.

This is the stage that separates projection from documentation. Without it the
pack is a hand-written document with extra steps — and MORE authority, because
its citations signal a rigor its age no longer earns.

Usage:  python3 drift.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = HERE / "pack.json"
REPO = HERE / "fixture-repo"

if not PACK.exists():
    print("no pack.json — run map.py first", file=sys.stderr)
    sys.exit(2)

pack = json.loads(PACK.read_text(encoding="utf-8"))
stale = 0

print(f"pack generated {pack['generated']}\n")

for name, c in sorted(pack["components"].items()):
    for ev in c["evidence"]:
        if not (REPO / ev).exists():
            print(f"STALE  {name}: cited evidence {ev} no longer exists")
            stale += 1

from map import scan  # noqa: E402
current = scan(REPO)
added = set(current["components"]) - set(pack["components"])
removed = set(pack["components"]) - set(current["components"])
for n in sorted(added):
    print(f"STALE  {n}: exists in the repository, absent from the pack")
    stale += 1
for n in sorted(removed):
    print(f"STALE  {n}: in the pack, gone from the repository")
    stale += 1

for name, c in sorted(pack["components"].items()):
    cur = current["components"].get(name)
    if cur and set(cur["depends_on"]) != set(c["depends_on"]):
        print(f"STALE  {name}: dependencies changed "
              f"{c['depends_on']} -> {cur['depends_on']}")
        print( "       -> the derived blast-radius tier may have changed too")
        stale += 1

if stale:
    print(f"\n{stale} stale section(s) — refresh these, not the whole pack.")
    print("Full regeneration discards human edits and costs a full run.")
else:
    print("no drift")
sys.exit(1 if stale else 0)
