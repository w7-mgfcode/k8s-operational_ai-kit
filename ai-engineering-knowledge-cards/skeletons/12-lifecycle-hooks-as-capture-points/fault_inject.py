#!/usr/bin/env python3
"""Prove the hooks fail open.

Breaks the filesystem calls each hook depends on, runs it, and asserts the
exit code is still 0. A hook that breaks the session it was meant to help is
the failure this pattern exists to prevent.

Usage:  python3 fault_inject.py
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HOOKS = Path(__file__).resolve().parent / "hooks"


def run(hook: str, stdin: str, env_break: bool) -> int:
    cmd = [sys.executable, str(HOOKS / hook)]
    if env_break and hook == "session_end.py":
        cmd += ["--daily-dir", "/proc/nonexistent/cannot-create"]
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    return p.returncode


cases = [
    ("session_end.py", "a: one\nb: two\nc: three\n", False, "normal"),
    ("session_end.py", "a: one\nb: two\nc: three\n", True, "unwritable daily dir"),
    ("session_end.py", "", False, "empty stdin"),
    ("session_start.py", "", False, "normal"),
]

fail = 0
for hook, stdin, brk, label in cases:
    rc = run(hook, stdin, brk)
    ok = rc == 0
    fail += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  {hook:<18} {label:<24} exit={rc}")

print("\nfail-open holds" if not fail else f"\n{fail} hook(s) failed the session")
sys.exit(1 if fail else 0)
