#!/usr/bin/env python3
"""Compare a prose tier table with the lookup script's built-in copy, then
derive tiers from dependent counts and show where the hand-assigned tiers differ.

    python3 compare.py            all three checks
    python3 compare.py --derive   only the count-derived tiers

The two files are the component's two copies of one classification. Neither
reads the other, which is the failure; the derivation is what card 17 asks the
classification to be based on, and what neither copy did.

Exit codes: 0 = the copies agree and every tier matches its count.
1 = findings (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The derivation rule. Any monotone rule would do; the point is that a rule
# exists and the tier follows from the count, not the other way round.
THRESHOLDS = ((5, "CRITICAL"), (3, "HIGH"), (1, "MEDIUM"), (0, "LOW"))
UNCOUNTABLE = re.compile(r"\ball\b", re.I)


def rows(block: str) -> list[list[str]]:
    out = []
    for line in block.splitlines():
        if line.startswith("|") and not set(line) <= set("|-: "):
            out.append([c.strip() for c in line.strip().strip("|").split("|")])
    return out[1:] if out else []


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def parse_prose(text: str) -> tuple[dict, dict, list[str]]:
    components = {}
    for tier, block in re.findall(r"^### (\w+)\n(.*?)(?=^##|\Z)", section(text, "Tiers"), re.M | re.S):
        for name, _impact, deps in rows(block):
            components[name] = {"tier": tier, "dependents": [] if deps == "—" else
                                [d.strip() for d in deps.split(",")]}
    confirm = {t: a for t, a in rows(section(text, "Confirmation"))}
    spofs = [r[0] for r in rows(section(text, "Shared single points of failure"))]
    return components, confirm, spofs


def derive(deps: list[str]) -> str | None:
    if any(UNCOUNTABLE.search(d) for d in deps):
        return None
    return next(tier for floor, tier in THRESHOLDS if len(deps) >= floor)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--derive", action="store_true", help="only the count-derived tiers")
    a = ap.parse_args()

    prose, confirm, spofs = parse_prose((HERE / "tiers.md").read_text(encoding="utf-8"))
    script = json.loads((HERE / "tiers.json").read_text(encoding="utf-8"))
    findings = 0

    if not a.derive:
        print("1. the prose table against the script's copy")
        for name in sorted(set(prose) | set(script["components"])):
            p, s = prose.get(name), script["components"].get(name)
            if not p or not s:
                findings += 1
                print(f"   {name:14} only in {'the script' if s else 'the prose'}")
                continue
            if p["tier"] != s["tier"]:
                findings += 1
                print(f"   {name:14} tier {p['tier']} in prose, {s['tier']} in the script")
            if sorted(p["dependents"]) != sorted(s["dependents"]):
                findings += 1
                extra = f", count stated as {s['dependents_count']}" if "dependents_count" in s else ""
                print(f"   {name:14} dependents differ: {len(p['dependents'])} in prose, "
                      f"{len(s['dependents'])} in the script{extra}")
        for tier, action in confirm.items():
            if script["confirmation"].get(tier) != action:
                findings += 1
                print(f"   {tier:14} confirmation: '{action}' vs '{script['confirmation'].get(tier)}'")

        print("\n2. shared single points of failure the script can answer for")
        for system in spofs:
            found = system in script["components"]
            findings += not found
            print(f"   {system:14} {'found' if found else 'NOT FOUND — the lookup has no row for it'}")
        print()

    print("3. tiers derived from dependent counts (prose table)")
    print(f"   rule: {', '.join(f'>={f} {t}' for f, t in THRESHOLDS)}")
    for name, entry in prose.items():
        derived = derive(entry["dependents"])
        if derived is None:
            findings += 1
            print(f"   {name:14} assigned {entry['tier']:8} cannot be derived: dependents are not countable")
        elif derived != entry["tier"]:
            findings += 1
            print(f"   {name:14} assigned {entry['tier']:8} count {len(entry['dependents'])} derives {derived}")

    print(f"\n{findings} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
