#!/usr/bin/env python3
"""Check the evaluation's STRUCTURE against the contract.

The evaluator is the one role with an incentive to be agreeable, so its output
is the one output that gets mechanically checked.

Usage:  python3 validate_evaluation.py --contract contract.json --evaluation evaluation-inflated.json
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HEDGES = [
    (r"\bmost cases\b", "score inflation: 'most cases' is not 'all specified cases'"),
    (r"\bmight need\b|\bcould use\b|\bsome attention\b", "hedge-as-pass: a blocker phrased as a suggestion"),
    (r"\boverall\b.{0,40}\b(sound|good|solid)\b", "praise sandwich: a flaw framed between positives"),
    (r"\bnice\b|\bgreat\b", "praise in a flaw-first report"),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--evaluation", required=True)
    a = ap.parse_args()

    c = json.loads(Path(a.contract).read_text(encoding="utf-8"))
    e = json.loads(Path(a.evaluation).read_text(encoding="utf-8"))
    issues = 0

    for axis, spec in c["axes"].items():
        if axis not in e.get("scores", {}):
            print(f"ERROR  axis '{axis}' not scored"); issues += 1
            continue
        score = e["scores"][axis]
        below = score < spec["threshold"]
        print(f"  {axis:<16} {score}/{spec['threshold']} {'BELOW THRESHOLD' if below else 'ok'}")
        if below and not any(axis in b for b in e.get("blocking", [])):
            print(f"ERROR  '{axis}' is below threshold with no blocking issue recorded")
            issues += 1

    notes = " ".join(e.get("notes", "").split())
    for pat, why in HEDGES:
        if re.search(pat, notes, re.I):
            print(f"ERROR  sycophancy pattern — {why}"); issues += 1

    for oos in c["out_of_scope"]:
        if re.search(rf"\b{re.escape(oos)}\b", notes, re.I):
            print(f"ERROR  penalizes '{oos}', which the contract puts OUT OF SCOPE")
            issues += 1

    concrete = re.search(r"\b\w+\.\w+:\d+", notes)
    if e.get("blocking") and not concrete:
        print("ERROR  blocking issues with no cited location"); issues += 1
    if not e.get("blocking") and re.search(r"==|secret|injection|vulnerab", notes, re.I):
        print("ERROR  notes describe a security flaw but nothing is marked blocking")
        issues += 1

    print(f"\n{issues} structural problem(s) in the evaluation" if issues
          else "\nevaluation is well-formed")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
