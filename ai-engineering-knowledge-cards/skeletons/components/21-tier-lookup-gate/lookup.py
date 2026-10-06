#!/usr/bin/env python3
"""Tier lookup gate — look a component up before a change; the exit code is the gate.

    python3 lookup.py                                   the demonstration table
    python3 lookup.py --component secrets-store         one lookup, as the skill calls it
    python3 lookup.py --component search-index --repo-path fixture-repo
    python3 lookup.py --list --component any            the table (see --list below)

The exit-code contract is the component's: 1 = critical or high, confirm first.
2 = unknown, review by hand. 0 = everything else — including a name the table
has never heard of. --component is required, as in the component, so --list on
its own stops with a usage error.

With no arguments: run a set of lookups and exit 1, because one of them — a
misspelled critical component — would proceed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXIT = {"CRITICAL": 1, "HIGH": 1, "UNKNOWN": 2}      # anything else -> 0
RULE = {
    "CRITICAL": "always confirm — platform sign-off",
    "HIGH": "always confirm",
    "MEDIUM": "confirm on first occurrence, then trust within the workstream",
    "LOW": "proceed, notify",
    "UNKNOWN": "always confirm — manual review",
    "NOT_FOUND": "cannot assess",
}


def table() -> dict[str, dict]:
    return json.loads((HERE / "tiers.json").read_text())["components"]


def normalise(name: str) -> str:
    return "-".join(name.strip().lower().replace("_", " ").split())


def lookup(component: str, repo: str | None = None) -> dict:
    name = normalise(component)
    entry = table().get(name)
    if entry:
        deps = entry["dependents"]
        out = {"component": name, "tier": entry["tier"], "dependents": deps,
               "dependents_count": entry.get("dependents_count", len(deps))}
        if "special" in entry:
            out["special"] = entry["special"]
    elif repo and (Path(repo) / "roles" / name).is_dir():
        out = {"component": name, "tier": "UNKNOWN", "dependents": [], "dependents_count": 0}
    else:
        out = {"component": name, "tier": "NOT_FOUND", "dependents": [], "dependents_count": 0,
               "error": "not in the table — check the spelling"}
    out["confirmation"] = RULE[out["tier"]]
    return out


def code(result: dict) -> int:
    return EXIT.get(result["tier"], 0)


def demo() -> int:
    print("lookups, as the skill would make them\n")
    cases = [
        ("secrets-store", None, "the store itself"),
        ("metrics", None, "a medium-tier change"),
        ("cert-isuer", None, "a typo for a critical component"),
        ("search-index", None, "a real role, missing from the table"),
        ("search-index", "fixture-repo", "the same, with the repo path the skill never passes"),
    ]
    print(f"  {'component':15} {'repo path':13} {'tier':10} exit  meaning")
    open_doors = 0
    for name, repo, why in cases:
        r = lookup(name, str(HERE / repo) if repo else None)
        rc = code(r)
        verdict = {0: "proceed", 1: "confirm", 2: "review"}[rc]
        flag = ""
        if r["tier"] == "NOT_FOUND":
            open_doors += 1
            flag = "  <- proceeds"
        print(f"  {name:15} {repo or '-':13} {r['tier']:10} {rc}     {verdict:8} {why}{flag}")

    s = lookup("secrets-store")
    print(f"\nsecrets-store: dependents_count {s['dependents_count']}, "
          f"dependents listed {len(s['dependents'])} — two numbers for one fact")
    print(f"\n{open_doors} lookups exit 0 for a component the gate cannot assess")
    return 1 if open_doors else 0


def main() -> int:
    if len(sys.argv) == 1:
        return demo()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--component", required=True, help="component to look up")
    ap.add_argument("--repo-path", help="repository to search for an untabled role")
    ap.add_argument("--list", action="store_true", help="print the table")
    a = ap.parse_args()

    if a.list:
        for name, entry in sorted(table().items()):
            print(f"  {entry['tier']:9} {name}")
        return 0
    result = lookup(a.component, a.repo_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return code(result)


if __name__ == "__main__":
    sys.exit(main())
