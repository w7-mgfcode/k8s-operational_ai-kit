#!/usr/bin/env python3
"""Evaluate a command against the ladder. Deny is checked FIRST.

Usage:
    python3 ladder.py "kubectl get pods"
    python3 ladder.py --audit
"""
from __future__ import annotations
import argparse, fnmatch, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = json.loads((ROOT / "policy-shared.json").read_text(encoding="utf-8"))
PERSONAL = json.loads((ROOT / "policy-personal.json").read_text(encoding="utf-8"))

DEMO = [
    ("kubectl get pods -n payments", "routine inspection"),
    ("git push origin main", "context-dependent — the one thing worth asking about"),
    ("kubectl delete pod api-0", "irreversible"),
    ("bash cleanup.sh", "runs `kubectl delete` inside — shallow matching cannot see it"),
]


def to_glob(rule: str) -> str:
    """Bash(kubectl get:*) -> kubectl get*   — ':*' means 'and anything after'."""
    inner = rule[5:-1] if rule.startswith("Bash(") and rule.endswith(")") else rule
    return inner.replace(":*", "*")


def evaluate(cmd: str, merged: dict) -> tuple[str, str]:
    for rung in ("deny", "ask", "allow"):        # order is the whole design
        for rule in merged.get(rung, []):
            if fnmatch.fnmatch(cmd, to_glob(rule)):
                return rung, rule
    return "default", "-"


def merge() -> dict:
    return {r: SHARED.get(r, []) + PERSONAL.get(r, []) for r in ("deny", "ask", "allow")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", nargs="?")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    merged = merge()

    if a.audit:
        print(f"shared:   {len(SHARED['allow'])} allow, {len(SHARED['ask'])} ask, {len(SHARED['deny'])} deny")
        print(f"personal: {len(PERSONAL['allow'])} allow, {len(PERSONAL['ask'])} ask, {len(PERSONAL['deny'])} deny")
        print("\npersonal grants nobody has reviewed:")
        for r in PERSONAL["allow"]:
            oneoff = "curl" in r and "?" not in r or "api.example.org/repos" in r
            print(f"  {r[:66]}{'   <- a one-time fetch, retained forever' if oneoff else ''}")
        broad = [r for r in PERSONAL["allow"] if r.endswith(":*)")]
        print("\nSHADOWING RISK — a broad personal allow next to a specific shared deny:")
        for r in broad:
            for d in SHARED["deny"]:
                if to_glob(d).startswith(to_glob(r).rstrip("*")):
                    print(f"  personal allow {r}")
                    print(f"  shared  deny  {d}")
                    print("  -> only DENY-FIRST ordering saves this. Check that ordering.")
        return

    if not a.command:
        for cmd, why in DEMO:
            rung, rule = evaluate(cmd, merged)
            print(f"{rung.upper():<8} {cmd}")
            print(f"         matched {rule}  ({why})")
            if rung == "ask":
                print("         ^ the weakest rung. every prompt is answered by a")
                print("           human who has already approved eleven of these.")
            if rung == "default" and cmd.startswith("bash "):
                print("         ^ BYPASS: the denied verb is inside a script.")
                print("           the ladder sees command text, nothing more.")
        return

    rung, rule = evaluate(a.command, merged)
    print(f"{rung.upper()}  {a.command}\nmatched: {rule}")
    sys.exit(0 if rung in ("allow", "ask") else 1)


if __name__ == "__main__":
    main()
