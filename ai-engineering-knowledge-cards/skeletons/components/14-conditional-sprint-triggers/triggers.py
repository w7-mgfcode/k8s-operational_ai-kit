#!/usr/bin/env python3
"""Three sprint triggers as state machines that are actually evaluated.

    python3 triggers.py              replay events.json: transitions, decisions, bypasses
    python3 triggers.py --print-only the same states, reported the source's way

The transition table is the reference's own, as data. Every 'set' event is
checked against it; every 'start' event is checked against a decision function
that turns trigger states into the workstreams allowed to start. --print-only
shows what the source's status report did instead: print the final strings.

Exit codes: 0 = every transition legal and every start allowed.
1 = rejected transitions, bypasses or unevidenced stability (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TRANSITIONS = {
    "schema": {"unresolved": {"resolved", "deferred"}},
    "tls": {"pending": {"stable", "unstable"}, "unstable": {"pending"}, "stable": {"unstable"}},
    "conflict": {"pending": {"no_conflict", "conflict", "pending_approval"}, "conflict": {"deferred"}},
}
QUESTIONS = {
    "schema": ("Unseal-key schema agreed?", "pause B, continue C/D/E"),
    "tls": ("TLS stable after A?", "roll A back behind its flag, do not start B"),
    "conflict": ("Benchmark items conflict with the platform?", "defer with a rationale"),
}


def allowed(states: dict[str, str], done: set[str]) -> dict[str, str]:
    """Which workstreams may start now, with the reason for each refusal."""
    verdict = {"A": "", "C": "", "E": "", "D": ""}
    if states["tls"] == "unstable":
        verdict["A"] = "TLS unstable: roll back, do not restart"
    b = []
    if "A" not in done:
        b.append("A not complete")
    if states["schema"] != "resolved":
        b.append(f"schema {states['schema']}")
    if states["tls"] != "stable":
        b.append(f"TLS {states['tls']}")
    verdict["B"] = "; ".join(b)
    verdict["D-control-plane"] = "" if states["conflict"] == "no_conflict" else \
        f"platform conflict {states['conflict']}"
    return verdict


def replay(log: dict) -> int:
    states = dict(log["initial"])
    done: set[str] = set()
    findings = 0
    print(f"start      {states}\n")
    for e in log["events"]:
        if e["kind"] == "set":
            t, new = e["trigger"], e["state"]
            legal = TRANSITIONS[t].get(states[t], set())
            if new not in legal:
                findings += 1
                print(f"{e['at']}  REJECT  {t}: {states[t]} -> {new}   allowed: {sorted(legal) or 'none'}")
                continue
            note = ""
            if t == "tls" and new == "stable" and not e.get("evidence"):
                findings += 1
                note = "   no evidence and no window start recorded"
            print(f"{e['at']}  set     {t}: {states[t]} -> {new}{note}")
            states[t] = new
        elif e["kind"] == "complete":
            done.add(e["workstream"])
            print(f"{e['at']}  done    {e['workstream']}")
        else:
            why = allowed(states, done).get(e["workstream"], "")
            if why:
                findings += 1
                print(f"{e['at']}  BYPASS  start {e['workstream']}: {why}")
            else:
                print(f"{e['at']}  start   {e['workstream']}")

    print("\nnow")
    for ws, why in allowed(states, done).items():
        print(f"  {ws:16} {'may start' if not why else 'blocked: ' + why}")
    print(f"\n{findings} findings")
    return 1 if findings else 0


def print_only(log: dict) -> int:
    """What the source's status output did: show the strings, decide nothing."""
    states = dict(log["initial"])
    for e in log["events"]:
        if e["kind"] == "set":
            states[e["trigger"]] = e["state"]        # any string is accepted
    print("| Trigger | State | If unresolved |")
    print("|---|---|---|")
    for t, (question, action) in QUESTIONS.items():
        print(f"| {question} | {states[t]} | {action} |")
    print("\nNo transition was checked and no workstream was allowed or refused.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print-only", action="store_true", help="report the states the source's way")
    a = ap.parse_args()
    log = json.loads((HERE / "events.json").read_text(encoding="utf-8"))
    return print_only(log) if a.print_only else replay(log)


if __name__ == "__main__":
    sys.exit(main())
