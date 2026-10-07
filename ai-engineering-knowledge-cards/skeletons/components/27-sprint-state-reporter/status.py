#!/usr/bin/env python3
"""Sprint state reporter — renders the sprint state file as a table, Markdown or
JSON, and applies a workstream status update. Then a check of what it never does.

    python3 status.py                                   table, from state.json
    python3 status.py --format markdown --checkpoint C  the checkpoint report
    python3 status.py --update B --status done-ish      what an update would save
    python3 status.py --audit                           what the report leaves out

The reporter reads the state file and prints it. It does not decide anything:
the checkpoint it is asked for, the status vocabulary, workstream dependencies
and trigger states all pass through it unexamined. --audit shows each.

The skeleton never writes state.json; --update prints what would be saved.

Exit codes: 0 = rendered. 1 = --audit found what the reporter does not check
(the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATUSES = ("not_started", "in_progress", "complete", "paused", "rolled_back")


def render(state: dict, fmt: str = "table", checkpoint: str | None = None) -> str:
    """Render the state. `checkpoint` is accepted and never read — as in the component."""
    if fmt == "json":
        return json.dumps(state, indent=2)
    ws, tr, cp = state["workstreams"], state["triggers"], state["checkpoints"]
    if fmt == "markdown":
        out = [f"# Sprint status: {state['sprint']['name']}", "",
               "| WS | Name | Status | Band | Validation | Blockers |", "|---|---|---|---|---|---|"]
        out += [f"| {k} | {w['name']} | {w['status']} | {w['band']} | {w['validation']} | "
                f"{', '.join(w['blockers']) or 'none'} |" for k, w in ws.items()]
        out += ["", "| Trigger | State | Otherwise |", "|---|---|---|"]
        out += [f"| {t['question']} | {t['state']} | {t['otherwise']} |" for t in tr.values()]
        out += ["", "| Checkpoint | Target | Status |", "|---|---|---|"]
        out += [f"| {k} | {c['target']} | {c['status']} |" for k, c in cp.items()]
        return "\n".join(out)
    # table: workstreams only — triggers and checkpoints appear in Markdown alone
    out = [f"{'WS':<4}{'Name':<22}{'Status':<14}{'Band':<15}Validation"]
    out += [f"{k:<4}{w['name']:<22}{w['status']:<14}{w['band']:<15}{w['validation']}" for k, w in ws.items()]
    return "\n".join(out)


def apply_update(state: dict, ws: str, status: str) -> dict:
    """Set a status. Any string is accepted — as in the component."""
    state["workstreams"][ws]["status"] = status
    return state


def gated(state: dict) -> dict[str, list[str]]:
    """What the reporter could compute and never does: what holds each workstream."""
    ws, held = state["workstreams"], {}
    for key, w in ws.items():
        reasons = [f"waits on {d} ({ws[d]['status']})" for d in w["dependencies"]
                   if ws[d]["status"] != "complete"]
        reasons += [f"trigger {name} is {t['state']}" for name, t in state["triggers"].items()
                    if key in t["gates"] and t["state"] != t["proceed_on"]]
        if reasons:
            held[key] = reasons
    return held


def audit(state: dict) -> int:
    findings = 0

    print("checkpoint argument")
    a = render(state, "markdown", checkpoint="A")
    c = render(state, "markdown", checkpoint="C")
    if a == c:
        findings += 1
        print(f"  the report for checkpoint A and for checkpoint C is identical "
              f"({len(a.splitlines())} lines) — C's backlog and risks are nowhere in it")

    print("\nstatus vocabulary")
    trial = apply_update(json.loads(json.dumps(state)), "B", "done-ish")
    if trial["workstreams"]["B"]["status"] not in STATUSES:
        findings += 1
        print(f"  update B to 'done-ish': accepted. The documented values are {', '.join(STATUSES)}")

    print("\nwhat the report shows, and what actually holds each workstream")
    for key, reasons in gated(state).items():
        w = state["workstreams"][key]
        shown = f"{w['status']}, blockers: {', '.join(w['blockers']) or 'none'}"
        findings += 1
        print(f"  {key}  report: {shown:32} actually: {'; '.join(reasons)}")

    print(f"\n{findings} findings — the reporter prints state; nothing in it decides what may proceed")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default=str(HERE / "state.json"))
    ap.add_argument("--format", choices=["table", "markdown", "json"], default="table")
    ap.add_argument("--checkpoint", choices=["A", "B", "C"])
    ap.add_argument("--update", choices=["A", "B", "C", "D", "E"])
    ap.add_argument("--status")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()

    state = json.loads(Path(a.state).read_text())
    if a.audit:
        return audit(state)
    if a.update:
        if not a.status:
            ap.error("--update needs --status")
        before = state["workstreams"][a.update]["status"]
        apply_update(state, a.update, a.status)
        print(f"{a.update}: {before} -> {a.status}  (accepted; not saved — the skeleton never writes its fixture)")
        return 0
    print(render(state, a.format, a.checkpoint))
    return 0


if __name__ == "__main__":
    sys.exit(main())
