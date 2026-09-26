#!/usr/bin/env python3
"""Detect policy restated in a router.

A router may point at the contract and describe its own vendor's mechanics.
The moment it states a rule, the rule has two homes and they will diverge.

Heuristic, not proof: flags imperative policy language and any line whose
wording overlaps heavily with a contract line.

Usage:  python3 check_routers.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMPERATIVE = re.compile(r"\b(must|never|always|should|required|shall)\b", re.I)


def rule_lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines()
            if re.match(r"^\s*\d+\.\s", ln) or IMPERATIVE.search(ln)]


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"\w+", s.lower()) if len(w) > 3}


contract = (ROOT / "CONTRACT.md").read_text(encoding="utf-8")
c_rules = rule_lines(contract)
findings = 0

for router in sorted((ROOT / "routers").glob("*.md")):
    for ln in rule_lines(router.read_text(encoding="utf-8")):
        best = max((len(words(ln) & words(c)) / max(len(words(c)), 1), c)
                   for c in c_rules)
        score, match = best
        if score >= 0.5:
            findings += 1
            print(f"RESTATED  {router.name}")
            print(f"          router:   {ln[:72]}")
            print(f"          contract: {match[:72]}")
            if score < 0.95:
                print(f"          ^ and it has ALREADY DIVERGED (overlap {score:.0%})")
            print()
        else:
            findings += 1
            print(f"POLICY    {router.name}: {ln[:72]}")
            print("          a router states mechanics, never rules — and this one")
            print("          states a requirement the contract does not have at all\n")

print(f"{findings} finding(s)" if findings else "clean — no router states policy")
sys.exit(1 if findings else 0)
