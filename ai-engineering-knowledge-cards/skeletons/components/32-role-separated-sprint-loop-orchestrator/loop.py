#!/usr/bin/env python3
"""A miniature role-separated sprint loop, and an audit of what it leaves to prose.

    python3 loop.py run     # build, grade and gate a fabricated sprint; exits 0
    python3 loop.py audit   # what the skill's own text promises that nothing holds; exits 1

Standard library only, offline. The model is a stub: call_model() prints and
returns the next canned answer from fixtures.json.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
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

FIX = json.loads((Path(__file__).parent / "fixtures.json").read_text(encoding="utf-8"))


def call_model(role: str, brief: str, answer):
    """Stand-in for a subagent spawn: print what would be sent, return the canned reply."""
    print(f"[stub] call_model(role={role}): {brief}", file=sys.stderr)
    return answer


def gate(contract: dict, scores: dict) -> list:
    """The arithmetic the pattern asks for: every axis at or above its threshold."""
    return [axis for axis, floor in contract.items() if scores.get(axis, 0) < floor]


def run() -> int:
    contract, cap = FIX["contract"], FIX["max_iterations"]
    print(f"contract frozen: {contract}  (cap {cap})")
    delta = None
    for n, canned in enumerate(FIX["iterations"], 1):
        call_model("generator", "implement the sprint" + (" + delta" if delta else ""), None)
        result = call_model("evaluator", "grade against the contract", canned)
        failing = gate(contract, result["scores"])
        print(f"iteration {n}: scores={result['scores']} failing={failing or 'none'}")
        if not failing:
            print("gate: pass")
            return 0
        if n >= cap:
            print("gate: escalate to the owner")
            return 0
        delta = result["blocking"]
        print(f"delta back to the generator: {delta}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="loop.py")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("run")
    sub.add_parser("audit")
    rec = sub.add_parser("record")
    rec.add_argument("--state", required=True)
    rec.add_argument("--phase", required=True)
    return ap


def audit() -> int:
    findings = []
    parser = build_parser()
    for text in FIX["documented_commands"]:
        err = io.StringIO()
        with redirect_stderr(err):
            try:
                parser.parse_args(text.split())
                code = 0
            except SystemExit as exc:
                code = exc.code
        if code:
            findings.append(f"documented command exits {code}: {text}")
    for role, tools in FIX["prose_forbidden"].items():
        held = sorted(set(tools) & set(FIX["harness_grants_all"]))
        findings.append(f"{role}: prose forbids {held}, a general-purpose spawn grants them")
    findings.append(f"spawn failure fallback: {FIX['on_spawn_failure']} - one context builds and grades")
    if not any("accept" in v or "override" in v for v in FIX["sprint_status_values"]):
        findings.append("owner option 'override and accept' has no sprint status to record it in")
    for f in findings:
        print("FINDING:", f)
    print(f"{len(findings)} findings (exit 1 marks them, not an error)")
    return 1


if __name__ == "__main__":
    args = build_parser().parse_args()
    sys.exit({"run": run, "audit": audit}.get(args.command, lambda: 2)())
