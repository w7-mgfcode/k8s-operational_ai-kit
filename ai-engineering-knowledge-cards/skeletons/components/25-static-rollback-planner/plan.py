#!/usr/bin/env python3
"""Static rollback planner — one fixed recipe per workstream, and a check of it
against what a change actually touched.

    python3 plan.py [--workstream A]     the recipe, as the component prints it
    python3 plan.py --audit              the A recipe against changes.json

The recipe is a constant keyed by workstream. --audit replays the git commands
on paper against a fabricated change log: which changed files no command
restores, which restores are no-ops because the change is already committed, and
which would throw away uncommitted work. Nothing here runs git.

Exit codes: 0 = printed. 1 = --audit found gaps (the demonstration). 2 = usage
error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PLANS = {
    "A": {"name": "secrets-store TLS",
          "steps": ["Set the TLS feature flag off", "Revert the listener to plain HTTP",
                    "Lint and syntax-check", "Dry-run the role", "Operator applies",
                    "Check every secrets-store replica is unsealed"],
          "git": ["git diff HEAD -- roles/secrets-store/",
                  "git checkout HEAD -- roles/secrets-store/tasks/tls.yml"]},
    "B": {"name": "auto-unseal",
          "steps": ["Remove the transit seal stanza", "Dry-run the role", "Operator applies",
                    "Unseal every replica by hand"],
          "git": ["git checkout HEAD -- roles/secrets-store/tasks/unseal.yml"]},
    "C": {"name": "admission-policy remediation",
          "steps": ["Find the role change behind the regression", "Dry-run the role",
                    "Operator applies", "Check the policy report"],
          "git": ["git checkout HEAD -- roles/<affected-role>/"]},
    "D": {"name": "benchmark controls",
          "steps": ["Find the control fix behind the instability", "Dry-run", "Operator applies",
                    "Re-run the benchmark"],
          "git": ["git revert <commit>"]},
    "E": {"name": "cluster hygiene",
          "steps": ["Restore the removed object from its manifest or release history"],
          "git": []},
}


def restored_by(command: str) -> str | None:
    """The path a 'git checkout HEAD -- <path>' restores, or None."""
    prefix = "git checkout HEAD -- "
    return command[len(prefix):] if command.startswith(prefix) else None


def covers(target: str, path: str) -> bool:
    return path == target or (target.endswith("/") and path.startswith(target))


def audit(workstream: str) -> int:
    attempts = json.loads((HERE / "changes.json").read_text())["attempts"]
    plan = PLANS[workstream]
    targets = [t for c in plan["git"] if (t := restored_by(c))]
    gaps = 0

    for label, changes in attempts.items():
        print(f"attempt '{label}' — {len(changes)} file(s) changed; "
              f"the plan printed is the same as for every other attempt")
        for ch in changes:
            hit = [t for t in targets if covers(t, ch["path"])]
            if not hit:
                gaps += 1
                print(f"  never restored   {ch['path']}")
                continue
            if ch["committed"]:
                gaps += 1
                print(f"  no-op restore    {ch['path']}  (the change is already in HEAD, so restoring HEAD keeps it)")
            if ch["uncommitted"]:
                gaps += 1
                print(f"  discards work    {ch['path']}  (uncommitted edits overwritten, no warning)")
        print()

    print(f"{gaps} gaps — the recipe is fixed per workstream; the change is not")
    return 1 if gaps else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workstream", choices=sorted(PLANS), default="A")
    ap.add_argument("--audit", action="store_true",
                    help="check the recipe against changes.json")
    a = ap.parse_args()

    if a.audit:
        return audit(a.workstream)
    plan = PLANS[a.workstream]
    print(json.dumps({"workstream": a.workstream, "name": plan["name"],
                      "rollback_steps": plan["steps"], "git_commands": plan["git"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
