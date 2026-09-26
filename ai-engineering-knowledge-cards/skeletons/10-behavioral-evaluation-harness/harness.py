#!/usr/bin/env python3
"""Replay real prompts and assert which capability fired.

Routing is a claim about model behavior, not a property of your files. The
only way to check it is to run the prompt and look.

Usage:
    python3 harness.py --dry-run
    python3 harness.py
    python3 harness.py --baseline
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
BASE = json.loads((ROOT / "baseline.json").read_text(encoding="utf-8"))
SKILLS = ROOT.parent / "03-description-as-router" / "corrected"


def invoke(prompt: str) -> tuple[str | None, str]:
    """STUB — a real harness shells out to the actual CLI in the actual project
    directory, with a timeout, and fails loudly if the CLI is absent.

    The stub routes on trigger-phrase overlap so the skeleton runs offline.
    """
    best, best_score = None, 0
    for skill in sorted(SKILLS.glob("*.md")):
        text = skill.read_text(encoding="utf-8").lower()
        desc = text.split("---")[1] if text.startswith("---") else text
        score = sum(1 for w in prompt.lower().split() if len(w) > 3 and w in desc)
        if score > best_score:
            best, best_score = skill.stem, score
    return (best, f"routed on {best_score} term(s)") if best_score >= 2 else (None, "no match")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    a = ap.parse_args()

    if a.baseline:
        print("recorded runs — a result without a baseline means nothing:\n")
        for r in BASE["runs"]:
            print(f"  {r['date']}  {r['accuracy']:.0%}  {r['note']}")
        print("\nThe third run is why the baseline exists: a description edit")
        print("that fixed one case broke a neighbour, and only the aggregate showed it.")
        return

    if a.dry_run:
        print("would run, without invoking anything:\n")
        for c in CASES["cases"]:
            print(f"  [{c['kind']:<9}] {c['id']}: {c['prompt']}")
        return

    passed = 0
    for c in CASES["cases"]:
        got, why = invoke(c["prompt"])
        ok = got == c["expect"]
        passed += ok
        mark = "PASS" if ok else "FAIL"
        exp = c["expect"] or "(nothing should fire)"
        print(f"{mark}  [{c['kind']:<9}] {c['id']}  expected {exp}")
        print(f"      got: {got or '(nothing)'} — {why}")
        if c.get("why"):
            print(f"      {c['why']}")
    n = len(CASES["cases"])
    acc = passed / n
    print(f"\naccuracy {passed}/{n} = {acc:.0%}")
    last = BASE["runs"][-1]["accuracy"]
    print(f"baseline {last:.0%} ({BASE['runs'][-1]['date']}) — "
          + ("regression" if acc < last else "stable or improved"))
    sys.exit(0)


if __name__ == "__main__":
    main()
