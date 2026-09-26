#!/usr/bin/env python3
"""Look up blast radius BEFORE a change is drafted, then gate on it.

Running this after drafting invites rationalization, which is why the card puts
it first in the sequence.

Usage:
    python3 gate.py --component secret-store --target staging
    python3 gate.py --component network-layer --target prod-cluster
    python3 gate.py --component registry --target unknown-env
    python3 gate.py --list
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

M = json.loads((Path(__file__).resolve().parent / "matrix.json").read_text(encoding="utf-8"))
PHRASE = "confirm critical change"


def resolve_env(target: str) -> tuple[str, str]:
    """Multiple signals, and AMBIGUITY RESOLVES STRICT. Getting this backwards
    is the highest-cost error available."""
    t = target.lower()
    if "prod" in t:
        return "protected", "name contains 'prod'"
    if any(k in t for k in ("dev", "staging", "test", "sandbox")):
        return "non-protected", "name names a known non-protected environment"
    return "protected", "UNQUALIFIED — resolved strict, as the rule requires"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--component")
    ap.add_argument("--target", default="")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--confirm", default="")
    a = ap.parse_args()

    if a.list:
        for name, c in sorted(M["components"].items(), key=lambda kv: kv[1]["tier"]):
            deps = ", ".join(c["dependents"]) or "none"
            note = f"   ({c['note']})" if c.get("note") else ""
            print(f"  {c['tier']:<9} {name:<16} depends-on-it: {deps}{note}")
        print("\nshared single points of failure — they cross tier boundaries:")
        for k, v in M["shared_spof"].items():
            print(f"  {k}: {v}")
        return

    if not a.component:
        ap.error("--component is required (or --list)")

    c = M["components"].get(a.component)
    if not c:
        print(f"UNKNOWN component '{a.component}' — not in the matrix.")
        print("An unclassified component is not a safe one. Classify it first.")
        sys.exit(1)

    tier = c["tier"]
    spec = M["tiers"][tier]
    env, why = resolve_env(a.target)

    print(f"component:   {a.component}")
    print(f"tier:        {tier.upper()} — {spec['impact']}")
    print(f"dependents:  {', '.join(c['dependents']) or 'none'}")
    print(f"environment: {a.target or '(none given)'} -> {env}  [{why}]")

    if env == "protected":
        print("\nPROTECTED ENVIRONMENT — read-only, even after confirmation.")
        print("Confirmation unlocks looking. It never unlocks touching.")
        sys.exit(1)

    if spec["confirm"] == "typed-phrase":
        if a.confirm != PHRASE:
            print(f"\n*** {tier.upper()} BLAST RADIUS ***")
            print(f"    re-run with --confirm \"{PHRASE}\"")
            print("    not a yes/no — a phrase momentum cannot produce")
            sys.exit(1)
        print(f"\nconfirmed: \"{a.confirm}\" — recorded in the artifact")

    print("\nnext: DRY RUN, review its output, then apply. No exceptions.")
    print("validate by probing the dependency directly — consumers stay green")
    print("while a restart-delayed failure is already live.")
    sys.exit(0)


if __name__ == "__main__":
    main()
