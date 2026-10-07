#!/usr/bin/env python3
"""Repository scope detector — directory layout in, pre-filled sprint state out.

    python3 detect.py [fixture-repo]            the pre-filled state, as JSON
    python3 detect.py --audit [fixture-repo]    what the pre-fill decided for you

The detector looks in fixed places for roles, numbered phase playbooks,
inventories, a version-pin file, encrypted variables, a benchmark report and the
secrets-store task stubs, and turns what it finds into the sprint's starting
state. Nothing is written: the state goes to stdout.

Exit codes: 0 = printed. 1 = --audit found decisions the pre-fill made silently
(the demonstration), or the repository has no roles. 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The only places looked in: the root, and one nested layout.
LAYOUTS = (".", "infra/cluster")
STUBS = {"A": "roles/secrets-store/tasks/tls.yml", "B": "roles/secrets-store/tasks/unseal.yml"}


def first_dir(root: Path, name: str) -> Path | None:
    return next((root / l / name for l in LAYOUTS if (root / l / name).is_dir()), None)


def detect(root: Path) -> dict:
    roles_dir = first_dir(root, "roles")
    found = {
        "roles": sorted(d.name for d in roles_dir.iterdir() if d.is_dir()) if roles_dir else [],
        "playbooks": sorted(p.name for l in LAYOUTS for p in (root / l).glob("*.yml")
                            if re.match(r"\d\d-", p.name)),
        "version_pins": next((str(p.relative_to(root)) for p in root.glob("**/group_vars/all/versions.yml")), None),
        "encrypted_vars": next((str(p.relative_to(root)) for p in root.glob("**/group_vars/*.vault.yml")), None),
        "benchmark_report": None,
        "stubs": {ws: (root / path).is_file() for ws, path in STUBS.items()},
    }
    reports_dir = first_dir(root, "tmp")
    if reports_dir:
        reports = sorted(reports_dir.glob("benchmark-report-*.md"))
        found["benchmark_report"] = str(reports[-1].relative_to(root)) if reports else None
    return found


def prefill(found: dict) -> dict:
    """The sprint's starting state, built from the detection alone."""
    today = date.today().isoformat()
    ws = {
        "A": {"name": "secrets-store TLS", "band": "quick_win",
              "blockers": [] if found["stubs"]["A"] else ["TLS task stub not found"]},
        "B": {"name": "auto-unseal", "band": "medium_effort", "dependencies": ["A"],
              "requires_decision": ["unseal_schema"],
              "blockers": [] if found["stubs"]["B"] else ["auto-unseal task stub not found"]},
        "C": {"name": "admission-policy remediation", "band": "quick_win",
              "owned_roles": list(found["roles"]), "blockers": []},
        "D": {"name": "benchmark triage", "band": "quick_win",
              "report": found["benchmark_report"],
              "blockers": [] if found["benchmark_report"] else ["no benchmark report found"]},
        "E": {"name": "cluster hygiene", "band": "medium_effort", "blockers": []},
    }
    for w in ws.values():
        w.update(status="not_started", validation="pending")
    return {
        "sprint": {"created": today, "environment": "dev"},
        "detected": {k: v for k, v in found.items() if k != "roles"} | {"roles": len(found["roles"])},
        "workstreams": ws,
        "decision_triggers": {"unseal_schema": {"state": "unresolved"},
                              "tls_stability": {"state": "pending"},
                              "platform_conflict": {"state": "pending"}},
        "checkpoints": {"A": {"target": f"{today} EOD", "deliverables": []},
                        "B": {"target": "tomorrow midday", "deliverables": []},
                        "C": {"target": "tomorrow EOD", "deliverables": []}},
    }


def audit(root: Path, state: dict) -> int:
    issues = []
    owners = [l.strip() for l in (root / "OWNERS").read_text().splitlines()
              if l.strip() and not l.startswith("#")]
    extra = sorted(set(state["workstreams"]["C"]["owned_roles"]) - set(owners))
    if extra:
        issues.append(f"owned roles pre-filled with every role; not owned here: {', '.join(extra)}")

    for ws, path in STUBS.items():
        f = root / path
        if f.is_file() and all(l.startswith("#") or not l.strip() for l in f.read_text().splitlines()):
            issues.append(f"workstream {ws} unblocked because {path} exists — it holds only comments")

    for cp, c in state["checkpoints"].items():
        if not re.match(r"\d{4}-\d\d-\d\d", c["target"]):
            issues.append(f"checkpoint {cp} target is the literal string {c['target']!r}, not a date")

    template = json.loads((HERE / "state-template.json").read_text())
    ours, theirs = state["workstreams"]["B"]["requires_decision"], template["workstreams"]["B"]["requires_decision"]
    if ours != theirs:
        issues.append(f"workstream B waits on {ours}; the state template says {theirs}")
    empty = [cp for cp, c in state["checkpoints"].items() if not c["deliverables"]
             and template["checkpoints"][cp]["deliverables"]]
    if empty:
        issues.append(f"checkpoints {', '.join(empty)} have no deliverables; the template lists them")

    anywhere = sorted(str(p.relative_to(root)) for p in root.rglob("benchmark-report-*.md"))
    if anywhere and not state["workstreams"]["D"]["report"]:
        issues.append(f"workstream D blocked for want of a report; one exists at {anywhere[-1]} "
                      f"(looked only in tmp/ under {', '.join(LAYOUTS)})")

    for i in issues:
        print(f"  - {i}")
    print(f"\n{len(issues)} decisions the pre-fill made without asking")
    return 1 if issues else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=str(HERE / "fixture-repo"))
    ap.add_argument("--audit", action="store_true", help="list what the pre-fill decided")
    a = ap.parse_args()

    root = Path(a.repo)
    found = detect(root)
    if not found["roles"]:
        print(json.dumps({"error": "no roles directory in any known layout"}))
        return 1
    state = prefill(found)
    if a.audit:
        return audit(root, state)
    print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
