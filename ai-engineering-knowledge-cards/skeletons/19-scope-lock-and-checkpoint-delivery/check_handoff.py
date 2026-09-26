#!/usr/bin/env python3
"""Enforce the one rule that matters: next step #1 must be executable without
reading the rest of the document. It is the only part guaranteed to be read.

Usage:  python3 check_handoff.py <handoff.md>
"""
from __future__ import annotations
import re, sys
from pathlib import Path

VAGUE = ("continue", "finish", "keep going", "work on", "look into", "follow up",
         "carry on", "resume", "proceed with", "wrap up")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: check_handoff.py <handoff.md>", file=sys.stderr); sys.exit(2)
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    issues = 0

    m = re.search(r"^\s*1\.\s+(.+?)(?=\n\s*\d\.|\n##|\Z)", text, re.M | re.S)
    if not m:
        print("ERROR  no numbered next step #1"); sys.exit(1)
    step = " ".join(m.group(1).split())
    print(f"next step #1: {step[:96]}\n")

    for v in VAGUE:
        if re.search(rf"^\W*{v}\b", step, re.I):
            print(f"ERROR  starts with '{v}' — that is a topic, not an action"); issues += 1
    if not re.search(r"`[^`]+`|\b\w+\.\w+\b|:\d+", step):
        print("ERROR  names no file, command or location — the next session"); 
        print("       cannot act on it without reading everything else"); issues += 1
    if len(step.split()) < 8:
        print("ERROR  too short to be executable"); issues += 1

    if "## Dead ends" not in text:
        print("WARN   no dead-ends section — the section nobody writes and the"); 
        print("       next session most needs"); issues += 1
    elif not re.search(r"## Dead ends\s*\n+(.*?\n)*?\s*-\s+\w", text):
        print("WARN   dead-ends section is empty"); issues += 1

    print(f"\n{issues} issue(s)" if issues else "\nhandoff is actionable")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
