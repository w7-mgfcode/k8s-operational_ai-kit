#!/usr/bin/env python3
"""A fresh sketch of a loop state recorder, and an audit of it.

Three subcommands over one JSON state file: phase, sprint, iteration.

    python3 recorder.py phase --state run.json --phase plan
    python3 recorder.py --audit

Standard library only. The audit writes to a temporary directory and removes it.
Exit codes: 0 ran, 1 the audit demonstrated failures on purpose, 2 requires arguments.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


class _Swap:
    """Point a sys stream at a buffer for the length of a with-block."""

    def __init__(self, name, buf):
        self.name, self.buf = name, buf

    def __enter__(self):
        self.saved = getattr(sys, self.name)
        setattr(sys, self.name, self.buf)

    def __exit__(self, *exc):
        setattr(sys, self.name, self.saved)
        return False


def redirect_stdout(buf):
    return _Swap("stdout", buf)


def redirect_stderr(buf):
    return _Swap("stderr", buf)

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
PHASES = ("init", "plan", "contract", "generate", "evaluate", "gate", "finalize")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fresh() -> dict:
    return {"phase": "init", "sprint": None, "max_iterations": 3, "sprints": {}, "history": []}


def load(path: Path) -> dict:
    if not path.exists():
        return fresh()                         # a mistyped path starts a new run
    return json.loads(path.read_text(encoding="utf-8"))   # a corrupt file raises


def save(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(path)


def cmd_phase(path: Path, phase: str, status, notes) -> int:
    if phase not in PHASES:                    # membership is the only check
        print(json.dumps({"error": f"unknown phase {phase}", "valid": list(PHASES)}))
        return 1
    state = load(path)
    entry = {"at": now(), "from": state["phase"], "to": phase,
             "status": status or "in_progress", "sprint": state["sprint"]}
    if notes:
        entry["notes"] = notes
    state["phase"] = phase
    state["history"].append(entry)
    save(path, state)
    print(json.dumps({"updated": True, "entry": entry}))
    return 0


def cmd_sprint(path: Path, sprint: str, notes) -> int:
    state = load(path)
    state["sprint"] = sprint
    state["sprints"].setdefault(sprint, {"iteration": 0, "status": "active", "evaluations": []})
    state["history"].append({"at": now(), "action": "sprint", "sprint": sprint, "notes": notes or ""})
    save(path, state)
    print(json.dumps({"updated": True, "sprint": sprint}))
    return 0


def cmd_iteration(path: Path, result: str, scores, notes) -> int:
    try:
        parsed = json.loads(scores) if scores else None
    except ValueError:
        print(json.dumps({"error": "scores are not JSON"}))
        return 2
    state = load(path)
    sprint = state["sprints"].get(state["sprint"] or "")
    if sprint is None:
        print(json.dumps({"error": "no active sprint"}))
        return 1
    sprint["iteration"] += 1
    sprint["evaluations"].append({"iteration": sprint["iteration"], "result": result,
                                  "scores": parsed, "notes": notes or ""})
    if result == "fail" and sprint["iteration"] >= state["max_iterations"]:
        sprint["status"] = "escalated"
    elif result == "pass":
        sprint["status"] = "complete"          # whatever the status was before
    state["history"].append({"at": now(), "action": "iteration", "result": result})
    save(path, state)
    print(json.dumps({"updated": True, "iteration": sprint["iteration"],
                      "result": result, "sprint_status": sprint["status"]}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="loop state recorder (sketch)")
    parser.add_argument("--audit", action="store_true", help="run the findings audit")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("phase")
    p.add_argument("--state", required=True)
    p.add_argument("--phase", required=True)
    p.add_argument("--status")
    p.add_argument("--notes")
    p = sub.add_parser("sprint")
    p.add_argument("--state", required=True)
    p.add_argument("--sprint", required=True)
    p.add_argument("--notes")
    p = sub.add_parser("iteration")
    p.add_argument("--state", required=True)
    p.add_argument("--result", required=True, choices=["pass", "fail"])
    p.add_argument("--scores")
    p.add_argument("--notes")
    return parser


def call(fn, *args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*args)
    return code, json.loads(buf.getvalue())


def rejected(argv) -> bool:
    """True when the parser refuses argv, as a skill's documented call might be refused."""
    with redirect_stderr(io.StringIO()):
        try:
            build_parser().parse_args(argv)
        except SystemExit as exc:
            return exc.code == 2
    return False


def audit() -> int:
    work = Path(tempfile.mkdtemp(prefix="recorder-demo-"))
    findings: list = []

    def finding(text: str) -> None:
        findings.append(text)
        print(f"FINDING {len(findings)}: {text}")

    try:
        thresholds = json.loads((FIXTURES / "thresholds.json").read_text(encoding="utf-8"))

        run = work / "run.json"
        code, _ = call(cmd_phase, run, "generate", None, None)
        if code == 0 and load(run)["history"][0]["from"] == "init":
            finding("a fresh run moved from 'init' straight to 'generate'; only the name was checked")

        call(cmd_sprint, run, "s1", None)
        for _ in range(3):
            call(cmd_iteration, run, "fail", None, None)
        escalated = load(run)["sprints"]["s1"]["status"]
        code, out = call(cmd_iteration, run, "pass", None, None)
        if escalated == "escalated" and out["sprint_status"] == "complete":
            finding(f"after '{escalated}', a later pass set the sprint to '{out['sprint_status']}' "
                    f"and the counter reads {out['iteration']} of 3")

        if rejected(["iteration", "--state", "x", "--result", "override"]):
            finding("'override' is not a result the parser accepts: accepting a failed sprint "
                    "can only be written as a recorded pass")

        low = work / "low.json"
        call(cmd_sprint, low, "s1", None)
        scores = json.dumps({k: 1 for k in thresholds})
        code, out = call(cmd_iteration, low, "pass", scores, None)
        if out["sprint_status"] == "complete":
            finding(f"a pass was recorded with scores {scores} against thresholds {thresholds}; "
                    "the scores are stored and never compared")

        typo = work / "no-such-run.json"
        code, _ = call(cmd_phase, typo, "plan", None, None)
        if code == 0 and typo.exists():
            finding("a mistyped --state path created a new run and reported success")

        call(cmd_phase, run, "plan", "banana", None)
        if load(run)["history"][-1]["status"] == "banana":
            finding("a status of 'banana' was stored; the status is free text")

        corrupt = work / "corrupt.json"
        corrupt.write_text("{", encoding="utf-8")
        try:
            load(corrupt)
        except ValueError:
            finding("an unparsable state file raises instead of recovering; no earlier copy exists")

        if rejected(["--state", "run.json", "--phase", "plan", "--status", "complete"]):
            finding("the flags-only call a skill might document exits 2: a subcommand is required")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"{len(findings)} findings")
    return 1 if findings else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.audit:
        return audit()
    if args.command == "phase":
        return cmd_phase(Path(args.state), args.phase, args.status, args.notes)
    if args.command == "sprint":
        return cmd_sprint(Path(args.state), args.sprint, args.notes)
    if args.command == "iteration":
        return cmd_iteration(Path(args.state), args.result, args.scores, args.notes)
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
