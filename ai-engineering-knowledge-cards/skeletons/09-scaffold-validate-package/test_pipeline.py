#!/usr/bin/env python3
"""Functional tests for the pipeline — including cases that MUST fail.

A gate that is never tested against known-bad input is a gate you are trusting
on faith. Cleans up after itself.

Usage:  python3 test_pipeline.py
"""
from __future__ import annotations
import shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
fails = 0


def run(script: str, *args: str) -> int:
    return subprocess.run([PY, str(HERE / script), *args],
                          capture_output=True, text=True).returncode


def check(label: str, got: int, want: int) -> None:
    global fails
    ok = got == want
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  {label:<52} exit={got} (want {want})")


tmp = Path(tempfile.mkdtemp())
try:
    check("scaffold rejects uppercase", run("scaffold.py", "BadName", "--out", str(tmp)), 1)
    check("scaffold rejects reserved word", run("scaffold.py", "claude-thing", "--out", str(tmp)), 1)
    check("scaffold rejects trailing hyphen", run("scaffold.py", "trailing-", "--out", str(tmp)), 1)
    check("scaffold accepts a good name", run("scaffold.py", "good-skill", "--out", str(tmp)), 0)
    check("validate PASSES a TODO stub (warnings only)", run("validate.py", str(tmp / "good-skill")), 0)
    check("validate fails on malformed", run("validate.py", str(HERE / "malformed")), 1)
    check("PACKAGE REFUSES malformed", run("package.py", str(HERE / "malformed"), "--out", str(tmp)), 1)
    check("package accepts valid", run("package.py", str(tmp / "good-skill"), "--out", str(tmp)), 0)
    check("archive was written", 0 if (tmp / "good-skill.zip").exists() else 1, 0)
    check("no archive for malformed", 0 if not (tmp / "malformed.zip").exists() else 1, 0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{'all pass' if not fails else f'{fails} failure(s)'}")
sys.exit(1 if fails else 0)
