#!/usr/bin/env python3
"""Dry-run-first invocation contract — build the check/apply pair, and make the
"check first" rule something a program can refuse, not a sentence.

    python3 invoke.py                    the session, then the audit (exits 1)
    python3 invoke.py --pair registry    print one role's check and apply runs
    python3 invoke.py --audit contract-hardcoded.json

The pair differs only by --check. The ledger records every check run's exact
arguments; an apply is allowed only if a check with the same arguments, minus
the flag, came first. A tag that matches no role is refused before it runs,
because a run that selects no tasks succeeds and checks nothing.

Nothing is executed and nothing is written: run_playbook() is a stub that
prints, and the ledger lives in memory.

Exit codes: 0 = clean. 1 = refusals or audit findings (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAR = re.compile(r"^\$\{([A-Z_]+)\}$")


def resolve(value: str) -> str:
    """${NAME} comes from the environment; anything else is a hard-coded value."""
    m = VAR.match(value)
    if not m:
        return value
    return os.environ.get(m.group(1), f"<unset:{m.group(1)}>")


def build(contract: dict, tag: str, check: bool, extra: list[str] | None = None) -> list[str]:
    op = contract["operator"]
    argv = ["ansible-playbook", contract["playbook"],
            "-i", contract["inventory"],
            "-e", "@" + contract["encrypted_vars"],
            "--private-key", resolve(op["private_key"]),
            "-e", "kubeconfig=" + resolve(op["kubeconfig"]),
            "--vault-password-file", resolve(op["vault_password"]),
            "--tags", tag, *(extra or [])]
    return argv + ["--check"] if check else argv


def run_playbook(argv: list[str]) -> None:
    """Stub: the real contract hands this line to an operator. Nothing runs."""
    print("      would run: " + " ".join(argv[:2]) + " … --tags " + argv[argv.index("--tags") + 1]
          + (" --check" if argv[-1] == "--check" else ""))


def session(contract: dict, events: list[dict]) -> int:
    ledger: list[list[str]] = []          # every check run, as exact arguments
    refused = 0
    print("session — every apply must follow a check with the same arguments")
    for e in events:
        tag, extra = e["tag"], e.get("extra", [])
        label = f"{e['run']:5} {tag}" + (" " + " ".join(extra) if extra else "")
        if tag not in contract["roles"]:
            refused += 1
            print(f"  REFUSED  {label:40} no role has this tag: the run would select no tasks and pass")
            continue
        argv = build(contract, tag, e["run"] == "check", extra)
        if e["run"] == "check":
            ledger.append(argv)
            print(f"  ok       {label}")
            run_playbook(argv)
        elif argv + ["--check"] in ledger:
            print(f"  ok       {label}")
            run_playbook(argv)
        else:
            refused += 1
            near = [c for c in ledger if c[c.index("--tags") + 1] == tag]
            why = "the check ran with different arguments" if near else "no check run recorded"
            print(f"  REFUSED  {label:40} {why}")
    print(f"  {refused} refused — in the source, all of them would have been handed to the operator")
    return refused


def audit(contract: dict) -> int:
    findings = 0
    print("\naudit — operator values must be ${VARIABLES}, not one person's settings")
    for key, value in contract["operator"].items():
        if VAR.match(value):
            print(f"  ok       {key:16} from the environment")
        else:
            findings += 1
            kind = "a path in someone's home directory" if value.startswith("~") else "a literal value"
            print(f"  FINDING  {key:16} hard-coded: {kind}")
    return findings


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", metavar="ROLE", help="print the check and apply runs for one role")
    ap.add_argument("--audit", metavar="CONTRACT", help="audit one contract file only")
    a = ap.parse_args()

    contract = load("contract.json")
    if a.pair:
        if a.pair not in contract["roles"]:
            ap.error(f"no role '{a.pair}' in contract.json")
        for check in (True, False):
            print(" ".join(build(contract, a.pair, check)))
        return 0
    if a.audit:
        return 1 if audit(load(a.audit)) else 0

    problems = session(contract, load("session.json")["events"])
    problems += audit(contract)
    problems += audit(load("contract-hardcoded.json"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
