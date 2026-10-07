#!/usr/bin/env python3
"""Render a run outcome from a sprint-loop state, and list what the form cannot say.

    python3 outcome.py            # the report; exits 0
    python3 outcome.py --check    # the report's gaps against the state; exits 1

Standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
STATE = json.loads((HERE / "state.json").read_text(encoding="utf-8"))
VOCAB = json.loads((HERE / "vocab.json").read_text(encoding="utf-8"))
SPRINT_WORD = {"complete": "passed", "escalated": "escalated"}


def run_status(sprints: dict) -> str:
    states = {s["status"] for s in sprints.values()}
    if states == {"complete"}:
        return "all_passed"
    return "escalated" if "escalated" in states else "unknown"


def final_scores(sprint: dict) -> str:
    scored = [e["scores"] for e in sprint["evaluations"] if "scores" in e]
    return ", ".join(f"{k}:{v}" for k, v in scored[-1].items()) if scored else "n/a"


def wall_minutes() -> int:
    times = [datetime.fromisoformat(e["timestamp"]) for s in STATE["sprints"].values() for e in s["evaluations"]]
    return int((max(times) - min(times)).total_seconds() // 60)


def render() -> str:
    sprints = STATE["sprints"]
    lines = [f"# Final Report: {STATE['task']}", "", f"**Status:** {run_status(sprints)}",
             f"**Total sprints:** {len(sprints)}",
             f"**Total iterations:** {sum(s['iteration'] for s in sprints.values())}", "",
             "| Sprint | Status | Iterations | Final Scores | Blocking Issues Resolved |",
             "|---|---|---|---|---|"]
    for sid, s in sprints.items():
        lines.append(f"| {sid} | {SPRINT_WORD.get(s['status'], s['status'])} | {s['iteration']} | "
                     f"{final_scores(s)} | n/a |")
    lines += ["", f"**Total wall time:** {wall_minutes()} minutes (derived here from timestamps)",
              "**Most-iterated axis:** n/a"]
    return "\n".join(lines)


def check() -> int:
    sprints, findings = STATE["sprints"], []
    used = {s["status"] for s in sprints.values()}
    for v in sorted(used - set(SPRINT_WORD)):
        findings.append(f"state status '{v}' has no word in the report")
    for sid, s in sprints.items():
        if s["status"] == "complete" and any("accepted" in e.get("notes", "") for e in s["evaluations"]):
            findings.append(f"{sid} reads 'passed' but its only record of an override is free text")
    findings.append(f"the report's three run statuses overlap for this run: "
                    f"{run_status(sprints)} and partially_passed both fit; nothing defines the second")
    findings.append("'Blocking Issues Resolved' has no source: the state holds no blocker list")
    unscored = [f"{sid}#{e['iteration']}" for sid, s in sprints.items() for e in s["evaluations"] if "scores" not in e]
    findings.append(f"'Most-iterated axis' needs scores for every iteration; missing for {', '.join(unscored)}, "
                    "and thresholds live in contract files the state does not name")
    names = {k: len(v) for k, v in VOCAB.items()}
    findings.append(f"five vocabularies for one fact, no mapping between them: {names}")
    for f in findings:
        print("FINDING:", f)
    print(f"{len(findings)} findings (exit 1 marks them, not an error)")
    return 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        sys.exit(check())
    if sys.argv[1:]:
        print("usage: outcome.py [--check]", file=sys.stderr)
        sys.exit(2)
    print(render())
