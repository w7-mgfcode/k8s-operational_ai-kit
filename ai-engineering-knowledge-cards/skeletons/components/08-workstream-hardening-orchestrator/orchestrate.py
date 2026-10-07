#!/usr/bin/env python3
"""Workstream hardening orchestrator — scope lock, tier-gated confirmation,
operator hand-off and a checkpoint summary over a fabricated sprint.

    python3 orchestrate.py            run the sprint as the skill describes it
    python3 orchestrate.py --audit    what the state file says against what its
                                      triggers allow — and who would notice

The skill keeps its rules in prose: look up the tier first, confirm by tier,
pause a workstream whose trigger is open, never run a cluster command. This
prototype runs those rules as code, then shows that the state file the source
skill writes holds a workstream past an open trigger, and that a reporter
which only prints — the source's design — passes it without a word.

Exit codes: 0 = sprint ran. 1 = --audit found a workstream past an open
trigger or dependency (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANDS = ("quick_win", "medium_effort", "deep_work")
MOVING = {"in_progress", "complete"}


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def confirm(question: str) -> bool:
    """Stub for the user's yes/no. The real skill asks in chat."""
    print(f"    confirm? {question} -> yes (stub)")
    return True


def hand_to_operator(ws_id: str, role: str) -> None:
    """Stub for cluster-aware mode: print the dry-run/apply pair, run nothing."""
    print(f"    for the operator ({ws_id}):")
    print(f"      ansible-playbook <phase>.yml --tags {role} --check   # first")
    print(f"      ansible-playbook <phase>.yml --tags {role}           # after reviewing the dry-run")


def gate_needed(tier: str, component: str, tiers: dict, asked: set, ws_id: str) -> str | None:
    if component in tiers["always_confirm"]:
        return "always (secrets store)"
    if tier in ("CRITICAL", "HIGH"):
        return f"always ({tier})"
    if tier == "MEDIUM" and ws_id not in asked:
        return "first change in this workstream (MEDIUM)"
    return None


def blocked_by(ws: dict, plan: dict) -> list[str]:
    """What the skill's prose says must hold before a workstream moves."""
    why = [f"depends on {d} ({plan['workstreams'][d]['status']})"
           for d in ws["depends_on"] if plan["workstreams"][d]["status"] != "complete"]
    for t in ws["triggers"]:
        trig = plan["triggers"][t]
        if trig["state"] not in trig["ok"]:
            why.append(f"trigger '{trig['question']}' is {trig['state']}")
    return why


def run(plan: dict, tiers: dict) -> int:
    print(f"scope lock: {plan['sprint']['name']}, environment {plan['sprint']['environment']}, "
          f"cluster access {'yes' if plan['sprint']['cluster_access'] else 'no'}")
    confirm(f"lock {len(plan['workstreams'])} entries across {len(BANDS)} bands?")
    asked: set[str] = set()
    for band in BANDS:
        members = [(k, w) for k, w in plan["workstreams"].items() if w["band"] == band]
        if not members:
            continue
        print(f"\n{band.replace('_', ' ')}")
        for ws_id, ws in members:
            why = blocked_by(ws, plan)
            if why:
                print(f"  {ws_id} {ws['name']}: paused — {'; '.join(why)}")
                continue
            tier = tiers["tiers"].get(ws["component"], "UNKNOWN")
            print(f"  {ws_id} {ws['name']}: {ws['component']} is {tier}")
            reason = gate_needed(tier, ws["component"], tiers, asked, ws_id)
            if reason and not confirm(f"change {ws['component']} — {reason}"):
                continue
            asked.add(ws_id)
            if plan["sprint"]["cluster_access"]:
                hand_to_operator(ws_id, ws["role"])
    print("\ncheckpoints")
    for cp, when in plan["checkpoints"].items():
        print(f"  {cp}: {when}")
    return 0


def report_like_source(plan: dict) -> None:
    """The source's status script: print states, evaluate nothing."""
    for k, w in plan["workstreams"].items():
        print(f"  {k}  {w['name']:<42} {w['status']}")
    for t in plan["triggers"].values():
        print(f"  trigger  {t['question']:<38} {t['state']}")


GATES = [
    ("look up the tier before any change", "prose", "a script the model is told to run"),
    ("confirm by tier", "prose", "nothing records the answer"),
    ("pause B while a trigger is open", "prose", "the status script prints, never compares"),
    ("never run a cluster command", "prose", "no allowed-tools, no hook, no deny rule"),
    ("dry-run before every apply", "prose", "a command pair the operator may ignore"),
    ("lint and syntax check", "code", "the gate runner shells out to them itself"),
]


def audit(plan: dict) -> int:
    print("the source-style status report")
    report_like_source(plan)
    print("  (no warning: it prints what the file says)\n")
    print("what the skill's own rules say about that file")
    findings = 0
    for k, w in plan["workstreams"].items():
        why = blocked_by(w, plan)
        if w["status"] in MOVING and why:
            findings += 1
            print(f"  {k} is {w['status']} but {'; '.join(why)}")
    print("\nwhere each rule lives")
    for rule, kind, note in GATES:
        print(f"  {kind:5}  {rule:<38} {note}")
    print(f"\n{findings} workstream(s) past an open gate, accepted by a reporter that only prints")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", action="store_true", help="check the state file against its triggers")
    a = ap.parse_args()
    plan, tiers = load("sprint.json"), load("tiers.json")
    return audit(plan) if a.audit else run(plan, tiers)


if __name__ == "__main__":
    sys.exit(main())
