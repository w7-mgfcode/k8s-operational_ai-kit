#!/usr/bin/env python3
"""Installation glossary — pull the facts out of the definitions, compare them
with the current state, and find terms a second dictionary defines differently.

    python3 staleness.py                 both checks; exits 1
    python3 staleness.py --facts         list the checkable facts only; exits 0

A glossary row is a definition; the version, count, endpoint, deadline or time
inside it is a measurement. This extracts the measurements by shape and checks
each against state.json. Anything it cannot shape-match is left alone, which is
the honest limit of the method.

Exit codes: 0 = nothing stale or duplicated. 1 = stale facts or conflicting
definitions (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROW = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", re.M)
FACT_SHAPES = {
    "version": r"\bv\d+\.\d+(?:\.\d+)?\b",
    "count": r"\b\d+ (?:nodes|replicas|apps|workers|gateways)\b",
    "endpoint": r"\b[a-z][\w.-]*:\d{2,5}\b",
    "deadline": r"\bQ[1-4] \d{4}\b",
    "time": r"\b\d{2}:\d{2}\b",
}


def terms(path: str) -> dict[str, str]:
    return {t.strip(): m.strip() for t, m in ROW.findall((HERE / path).read_text())}


def facts(meaning: str) -> list[tuple[str, str]]:
    found = []
    for kind, rx in FACT_SHAPES.items():
        found += [(kind, v) for v in re.findall(rx, meaning)]
    return found


def stale(glossary: dict[str, str], state: dict[str, list[str]]) -> int:
    n = 0
    print("facts in the glossary, checked against the current state")
    for term, meaning in glossary.items():
        for kind, value in facts(meaning):
            current = state.get(term, [])
            if value in current:
                print(f"  ok     {term:24} {kind:9} {value}")
                continue
            n += 1
            now = next((c for c in current if facts(c) and facts(c)[0][0] == kind), "unknown")
            print(f"  STALE  {term:24} {kind:9} {value:22} now: {now}")
    return n


def conflicts(a: dict[str, str], b: dict[str, str]) -> int:
    n = 0
    print("\nterms both dictionaries define")
    for term in sorted(set(a) & set(b)):
        if a[term] == b[term]:
            print(f"  same      {term}")
            continue
        n += 1
        print(f"  DIFFERENT {term}\n            glossary:   {a[term]}\n            dictionary: {b[term]}")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--facts", action="store_true", help="list the extracted facts and stop")
    a = ap.parse_args()

    glossary = terms("glossary.md")
    if a.facts:
        for term, meaning in glossary.items():
            print(f"  {term:24} " + (", ".join(v for _, v in facts(meaning)) or "(definition only)"))
        return 0
    state = json.loads((HERE / "state.json").read_text())["facts"]
    n = stale(glossary, state) + conflicts(glossary, terms("dictionary.md"))
    print(f"\n{n} findings — the header says to use every one of these terms exactly")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
