#!/usr/bin/env python3
"""Decide completeness mechanically. A person asked whether a brief is complete
will say yes — optimistically, and while looking at the parts they wrote.

Usage:
    python3 validate_brief.py --brief partial-brief.yaml --tier complex
    python3 validate_brief.py --brief partial-brief.yaml --tier moderate
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = json.loads((ROOT / "tier_rules.json").read_text(encoding="utf-8"))


def parse(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip().strip('"')
            out[m.group(1)] = "" if v in ("TBD", "") else v
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--tier", required=True, choices=list(RULES["tiers"]))
    a = ap.parse_args()

    brief = parse(Path(a.brief))
    tier = RULES["tiers"][a.tier]
    filled = [s for s in RULES["sections"] if brief.get(s)]
    gaps = [s for s in tier["required"] if not brief.get(s)]
    applied = [s for s in tier["defaulted"] if not brief.get(s)]

    print(f"tier: {a.tier} ({tier['score']})")
    print(f"found {len(filled)} section(s) already filled: {', '.join(filled)}")
    print("  -> fast path: these will NOT be asked about again\n")

    if applied:
        print("defaults applied — announced, never silent:")
        for s in applied:
            print(f"  {s:<12} = {RULES['defaults'][s]}")
        print()

    if gaps:
        print(f"INCOMPLETE — {len(gaps)} required section(s) missing")
        for s in gaps:
            print(f"  {s:<12} ask as: {RULES['personas'][s]}")
        print("\nInterview resumes at the first gap. Nothing is generated yet.")
        sys.exit(1)

    print("COMPLETE — ready to hand to the generator (card 09)")
    sys.exit(0)


if __name__ == "__main__":
    main()
