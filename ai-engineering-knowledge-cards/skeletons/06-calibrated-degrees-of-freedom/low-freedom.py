#!/usr/bin/env python3
"""Verify a rollback is safe to run — LOW freedom.

Scripted because it is fragile, because consistency matters more than
adaptability, and because the sequence must not vary between runs. There are
exactly two parameters.

Usage:  python3 low-freedom.py --component api --env staging
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

STATE = Path(__file__).resolve().parent / "fixture-state.json"
PROTECTED = "production"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--env", required=True)
    a = ap.parse_args()

    state = json.loads(STATE.read_text(encoding="utf-8"))
    comp = state["components"].get(a.component)

    checks: list[tuple[str, bool, str]] = []
    checks.append(("component is known", comp is not None, a.component))
    if comp is None:
        report(checks); sys.exit(1)

    checks.append(("environment is not protected", a.env != PROTECTED, a.env))
    checks.append(("a previous revision exists", comp["previous_revision"] is not None,
                   str(comp["previous_revision"])))
    checks.append(("no migration since that revision", not comp["migrated_since"],
                   "schema changed" if comp["migrated_since"] else "clean"))
    checks.append(("no dependent is mid-deploy", not comp["dependents_deploying"],
                   ", ".join(comp["dependents"]) or "none"))
    report(checks)
    sys.exit(0 if all(ok for _, ok, _ in checks) else 1)


def report(checks) -> None:
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<34} {detail}")
    if not all(ok for _, ok, _ in checks):
        print("\nrollback NOT safe — resolve every FAIL before proceeding")
    else:
        print("\nrollback safe")


if __name__ == "__main__":
    main()
