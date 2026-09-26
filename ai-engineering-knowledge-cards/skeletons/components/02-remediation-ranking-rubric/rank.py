#!/usr/bin/env python3
"""Remediation ranking rubric — score candidate fixes, then test how much the
ranking can be trusted.

    python3 rank.py            rank, and show what the /12 display does to it
    python3 rank.py --stress   perturb each weight, add a root-cause criterion

The rubric arithmetic is exact. Its inputs are judgement: every 0/1/2 in
candidates.json is what a model would have assigned. --stress asks whether the
winner survives a small change to those choices.

Exit codes: 0 = ranked. 1 = --stress found that the winner does not survive
(the demonstration). 2 = the scores do not satisfy the rubric.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load() -> tuple[list[dict], list[dict]]:
    crit = json.loads((HERE / "rubric.json").read_text())["criteria"]
    cands = json.loads((HERE / "candidates.json").read_text())["candidates"]
    keys = [c["key"] for c in crit]
    for c in cands:
        if sorted(c["scores"]) != sorted(keys):
            sys.exit(f"{c['id']}: scores must cover exactly {keys}")
        bad = {k: v for k, v in c["scores"].items() if v not in (0, 1, 2)}
        if bad:
            sys.exit(f"{c['id']}: scores outside the 0/1/2 bands: {bad}")
    return crit, cands


def rank(crit: list[dict], cands: list[dict]) -> list[tuple[int, dict]]:
    """Weighted total, ties broken by the scores in criterion order."""
    def key(c: dict) -> tuple:
        total = sum(c["scores"][k["key"]] * k["weight"] for k in crit)
        return (total, tuple(c["scores"][k["key"]] for k in crit))
    ordered = sorted(cands, key=key, reverse=True)
    return [(key(c)[0], c) for c in ordered]


def show(crit: list[dict], cands: list[dict]) -> str:
    ranked = rank(crit, cands)
    maximum = 2 * sum(k["weight"] for k in crit)
    print(f"weights: " + "  ".join(f"{k['key']}×{k['weight']}" for k in crit)
          + f"   (max {maximum})\n")
    print("  #  option                                               /24   exact /12   rounded /12")
    for i, (total, c) in enumerate(ranked, 1):
        print(f"  {i}  {c['id']}: {c['title']:50} {total:>3}   {total / 2:>9g}   {round(total / 2):>11}")

    (t1, c1), (t2, c2) = ranked[0], ranked[1]
    if t1 == t2:
        first = next(k["key"] for k in crit if c1["scores"][k["key"]] != c2["scores"][k["key"]])
        print(f"\n  tie at {t1}: {c1['id']} beats {c2['id']} on '{first}', the first criterion where they differ")

    shown = [round(t / 2) for t, _ in ranked]
    merged = [(ranked[i][1]["id"], ranked[j][1]["id"])
              for i in range(len(ranked)) for j in range(i + 1, len(ranked))
              if shown[i] == shown[j] and ranked[i][0] != ranked[j][0]]
    if merged:
        pairs = ", ".join(f"{a}/{b}" for a, b in merged)
        print(f"  rounded display shows equal scores for {pairs}, which differ on /24:"
              " the halving invents ties")
    return c1["id"]


def stress(crit: list[dict], cands: list[dict], winner: str) -> int:
    print("\n── weight sensitivity: change one weight by one ────────────────")
    flips = []
    for k in crit:
        for delta in (-1, +1):
            w = k["weight"] + delta
            if w < 0:
                continue
            trial = [dict(c, weight=w) if c is k else c for c in crit]
            new = rank(trial, cands)[0][1]["id"]
            mark = "  <- winner changes" if new != winner else ""
            if new != winner:
                flips.append(f"{k['key']}×{w}")
            print(f"  {k['key']:12} ×{k['weight']} -> ×{w}: winner {new}{mark}")

    print("\n── add the criterion the rubric does not have ──────────────────")
    rc = {"key": "root_cause", "weight": 3}
    scored = [dict(c, scores={**c["scores"], "root_cause": c["root_cause"]}) for c in cands]
    new_ranked = rank(crit + [rc], scored)
    for total, c in new_ranked[:3]:
        print(f"  {c['id']}: {c['title']:50} {total:>3}/30")
    new = new_ranked[0][1]["id"]

    print()
    if flips or new != winner:
        print(f"  {winner} wins as written; {len(flips)} one-step weight change(s) "
              f"({', '.join(flips) or 'none'}) and a root-cause criterion "
              f"{'hand' if new != winner else 'do not hand'} it to another option.")
        print("  The ranking is a recommendation to put in front of a human, not a decision.")
        return 1
    print(f"  {winner} survives every perturbation tried.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stress", action="store_true", help="perturb weights, add root cause")
    a = ap.parse_args()
    crit, cands = load()
    winner = show(crit, cands)
    if a.stress:
        sys.exit(stress(crit, cands, winner))


if __name__ == "__main__":
    main()
