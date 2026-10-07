#!/usr/bin/env python3
"""A fresh sketch of a loop gate and history harness, and an audit of it.

Three subcommands over one JSON state file: init, history, gate.

    python3 loop_gate.py gate --state fixtures/recorded.json
    python3 loop_gate.py history --state fixtures/recorded.json
    python3 loop_gate.py --audit

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


def fresh() -> dict:
    return {"phase": "init", "sprint": None, "max_iterations": 3, "sprints": {}, "history": []}


def load(path: Path) -> dict:
    """A path that does not exist reads as an empty run, not as an error."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fresh()


def save(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(path)


def emit(doc: dict) -> None:
    print(json.dumps(doc, indent=2))


def cmd_init(path: Path, task: str, max_iterations: int, force: bool) -> int:
    state = load(path)
    if state["phase"] != "init" and not force:
        emit({"error": "run in progress; pass --force to start over", "phase": state["phase"]})
        return 0                       # a refusal that exits 0
    state.update(task=task, max_iterations=max_iterations, phase="plan",
                 sprint=None, sprints={}, history=[])   # history is emptied, not archived
    save(path, state)
    emit({"status": "initialized", "task": task, "max_iterations": max_iterations})
    return 0


def cmd_history(path: Path) -> int:
    entries = load(path).get("history", [])
    emit({"history": entries, "message": "" if entries else "no history entries yet"})
    return 0


def cmd_gate(path: Path) -> int:
    state = load(path)
    sprint_id = state.get("sprint")
    if not sprint_id:
        emit({"error": "no active sprint"})
        return 1
    sprint = state["sprints"].get(sprint_id, {})
    cap = state.get("max_iterations", 3)
    done = sprint.get("iteration", 0)
    evaluations = sprint.get("evaluations", [])
    if not evaluations:
        emit({"sprint": sprint_id, "gate": "pending"})
        return 0
    axes = evaluations[-1].get("axes", [])            # the recorder never writes this key
    all_pass = all(a.get("pass", False) for a in axes)  # true for an empty list
    gate = "pass" if all_pass else "fail"
    if not all_pass and done >= cap:
        gate = "escalate"
    emit({"sprint": sprint_id, "iteration": done, "max_iterations": cap,
          "all_axes_pass": all_pass, "gate": gate})
    return 0                                           # every verdict exits 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="loop gate and history harness (sketch)")
    parser.add_argument("--audit", action="store_true", help="run the findings audit")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("init")
    p.add_argument("--task", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--max-iterations", type=int, default=3)
    p.add_argument("--force", action="store_true")
    for name in ("history", "gate"):
        sub.add_parser(name).add_argument("--state", required=True)
    return parser


def call(fn, *args):
    """Run a command function, returning (exit code, parsed JSON or text)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*args)
    text = buf.getvalue()
    try:
        return code, json.loads(text)
    except ValueError:
        return code, text


def audit() -> int:
    work = Path(tempfile.mkdtemp(prefix="gate-demo-"))
    findings: list = []

    def finding(text: str) -> None:
        findings.append(text)
        print(f"FINDING {len(findings)}: {text}")

    try:
        recorded = work / "recorded.json"
        shutil.copy(FIXTURES / "recorded.json", recorded)
        last = load(recorded)["sprints"]["s1"]["evaluations"][-1]
        code, out = call(cmd_gate, recorded)
        if out["gate"] == "pass" and last["result"] == "fail":
            finding(f"the recorded result is '{last['result']}', scores {last['scores']}; "
                    f"the gate says '{out['gate']}': it reads an axes list the recorder never writes")

        thresholds = json.loads((FIXTURES / "thresholds.json").read_text(encoding="utf-8"))
        flagged = work / "flagged.json"
        shutil.copy(FIXTURES / "flagged.json", flagged)
        axis = load(flagged)["sprints"]["s1"]["evaluations"][-1]["axes"][0]
        code, out = call(cmd_gate, flagged)
        if out["gate"] == "pass" and axis["score"] < thresholds[axis["name"]]:
            finding(f"{axis['name']} scored {axis['score']} against a threshold of "
                    f"{thresholds[axis['name']]}, flagged as passing; the gate says 'pass' "
                    "and never sees the threshold")

        failing = work / "failing.json"
        shutil.copy(FIXTURES / "failing.json", failing)
        code, out = call(cmd_gate, failing)
        if out["gate"] == "fail" and code == 0:
            finding("a 'fail' verdict exits 0; only 'no active sprint' exits non-zero")

        code, out = call(cmd_init, recorded, "demo", 3, False)
        if code == 0 and "error" in out:
            finding("init on a run in progress prints an error and exits 0")

        before = len(load(recorded)["history"])
        call(cmd_init, recorded, "demo", 3, True)
        after = len(load(recorded)["history"])
        if before and after == 0:
            finding(f"init --force took the history from {before} entries to {after}; "
                    "the rule is that history is append-only")

        typo = work / "no-such-run.json"
        code, out = call(cmd_history, typo)
        if code == 0 and out["history"] == [] and not typo.exists():
            finding("history on a mistyped path reports 'no history entries yet' and exits 0")

        err = io.StringIO()
        try:
            with redirect_stderr(err):
                build_parser().parse_args(["--task", "demo", "--state", "run.json", "--max-iterations", "3"])
        except SystemExit as exc:
            if exc.code == 2:
                finding("the flags-only form a skill might document is rejected: "
                        + err.getvalue().strip().splitlines()[-1])

        choices = set(build_parser()._subparsers._group_actions[0].choices)  # noqa: SLF001
        if not choices & {"phase", "set-phase", "advance"}:
            finding(f"subcommands are {sorted(choices)}; none moves a phase, "
                    "so no order can be enforced here")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"{len(findings)} findings")
    return 1 if findings else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.audit:
        return audit()
    if args.command == "init":
        return cmd_init(Path(args.state), args.task, args.max_iterations, args.force)
    if args.command == "history":
        return cmd_history(Path(args.state))
    if args.command == "gate":
        return cmd_gate(Path(args.state))
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
