"""Replay a walkthrough's commands against the tool and compare what it shows.

    python3 replay.py                      # both walkthroughs
    python3 replay.py recovery             # one

Each step is OK, MISMATCH (the tool printed something else), REJECTED (the tool refused the
command form) or NO-COMMAND (the walkthrough describes work with nothing to run).
Runs in a temporary directory and removes it.

Exit codes: 0 = every step reproduced, 1 = a step did not.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def replay(name: str, steps: list, tmp: Path) -> int:
    state = str(tmp / f"{name}.json")
    bad = 0
    print(f"== {name}")
    for i, step in enumerate(steps, 1):
        if "note" in step:
            print(f"  {i}. NO-COMMAND  {step['note']}")
            bad += 1
            continue
        argv = [sys.executable, "-B", str(HERE / "loop_tool.py")] + step["run"].format(state=state).split()
        p = subprocess.run(argv, capture_output=True, text=True)
        if p.returncode == 2:
            label = "(flags only, no subcommand)" if step["run"].startswith("--") else step["run"].split()[0]
            print(f"  {i}. REJECTED    exit 2 for: {label}")
            bad += 1
            continue
        try:
            got = json.loads(p.stdout)
        except ValueError:
            got = {}
        same = all(got.get(k) == v for k, v in step["shown"].items())
        if same:
            print(f"  {i}. OK          {step['run'].split()[0]}")
        else:
            print(f"  {i}. MISMATCH    shown {step['shown']}, printed {got}")
            bad += 1
    runs = [s.get("run", "") for s in steps]
    for i, r in enumerate(runs):
        if "--result fail" in r and not any(x.startswith("gate") for x in runs[i + 1:]):
            print("  note: a failure is recorded and the gate is never run after it")
    return bad


def main(argv: list) -> int:
    data = json.loads((HERE / "walkthroughs.json").read_text(encoding="utf-8"))
    names = argv or list(data)
    tmp = Path(tempfile.mkdtemp(prefix="walk-"))
    try:
        bad = sum(replay(n, data[n], tmp) for n in names)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{bad} steps did not reproduce")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
