#!/usr/bin/env python3
"""Pick a container from the two axes: who decides, and whose context pays.

Usage:
    python3 choose.py                 # run the worked examples
    python3 choose.py --interactive
"""
from __future__ import annotations
import sys

CASES = [
    ("Audit dependencies on a large tree, on request", False, True,
     "the user asks for it AND it reads hundreds of files"),
    ("Warn about a credential in a diff", True, False,
     "must fire without being asked — that is the entire value"),
    ("Generate release notes for a given tag range", False, False,
     "user-initiated, takes an argument, produces a bounded result"),
    ("Investigate why a test suite is flaky", True, True,
     "should fire on the symptom, and reads a lot to answer"),
]


def decide(auto: bool, heavy: bool) -> tuple[str, str]:
    if not auto:
        return ("COMMAND", "user decides; no routing contract needed") if not heavy \
            else ("COMMAND -> SUBAGENT", "user invokes; the command delegates the reading")
    return ("SKILL -> SUBAGENT", "routes automatically, then delegates the heavy reading") \
        if heavy else ("SKILL", "needs a routing contract — see card 03")


def main() -> None:
    if "--interactive" in sys.argv:
        desc = input("What does the capability do?\n> ")
        auto = input("Must it fire WITHOUT the user asking? [y/N] ").lower().startswith("y")
        heavy = input("Does it generate large intermediate material? [y/N] ").lower().startswith("y")
        c, why = decide(auto, heavy)
        print(f"\n{desc}\n  -> {c}\n     {why}")
        return

    for desc, auto, heavy, note in CASES:
        c, why = decide(auto, heavy)
        print(f"{desc}")
        print(f"  auto-fire={str(auto):<5} heavy={str(heavy):<5} -> {c}")
        print(f"  {note}")
        print(f"  {why}\n")


if __name__ == "__main__":
    main()
