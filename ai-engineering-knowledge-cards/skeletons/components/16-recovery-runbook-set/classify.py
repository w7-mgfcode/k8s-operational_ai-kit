#!/usr/bin/env python3
"""Recovery runbook set — classify every step by what it does to the cluster, and
flag each change that nothing previews.

    python3 classify.py                  classify runbooks.json; exits 1 on findings
    python3 classify.py --quiet          findings only

Each step gets a class from its verb: read, guard (a dry-run, diff, saved
values or a status check of the same object), mutating, destructive, or
unknown. A mutating or destructive step is flagged when no guard step comes
before it in the same runbook. Interactive steps are flagged too: they cannot
be handed to anything but a person at a terminal.

The source runbooks are command blocks with no such classes; this is the lint
they could have had. Nothing is executed.

Exit codes: 0 = every change has a guard. 1 = findings (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

GUARD = re.compile(r"--check\b|--dry-run\b|\bdiff\b|\bhelm get values\b|\bhelm template\b")
DESTRUCTIVE = re.compile(r"\b(delete|uninstall|rollback|drain|unseal)\b")
MUTATING = re.compile(r"\b(apply|upgrade|install|patch|scale|rollout restart|replace|edit)\b|^ansible-playbook\b")
READ = re.compile(r"\b(get|describe|logs|top|history|list|status|version)\b")


def classify(step: str) -> str:
    if GUARD.search(step):
        return "guard"
    if DESTRUCTIVE.search(step):
        return "destructive"
    if MUTATING.search(step):
        return "mutating"
    if READ.search(step):
        return "read"
    return "unknown"


def interactive(step: str) -> bool:
    return any(t in ("-it", "-ti", "--stdin") for t in step.split())


def check(runbook: dict, quiet: bool) -> int:
    findings = 0
    guarded = False
    if not quiet:
        print(f"\n{runbook['name']}")
    for n, step in enumerate(runbook["steps"], 1):
        kind = classify(step)
        notes = []
        if kind == "guard":
            guarded = True
        if kind in ("mutating", "destructive") and not guarded:
            notes.append("no dry-run, snapshot or preview before it")
        if kind == "unknown":
            notes.append("verb not recognised — a script name hides what it does")
        if interactive(step):
            notes.append("interactive: cannot be generated for an unattended run")
        findings += len(notes)
        if notes or not quiet:
            flag = "  FLAG" if notes else "      "
            where = f"{runbook['name']} step {n}" if quiet else f"step {n}"
            print(f"{flag} {where:8} {kind:12} {step}")
            for note in notes:
                print(f"         {'':8} {'':12} ↳ {note}")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print findings only")
    a = ap.parse_args()

    runbooks = json.loads((HERE / "runbooks.json").read_text())["runbooks"]
    findings = sum(check(rb, a.quiet) for rb in runbooks)
    print(f"\n{findings} findings across {len(runbooks)} runbooks — "
          "in the source, the only guard on every one is an instruction not to run it")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
