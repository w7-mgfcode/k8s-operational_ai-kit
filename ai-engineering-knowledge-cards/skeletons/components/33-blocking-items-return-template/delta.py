#!/usr/bin/env python3
"""Fill a return template from an evaluation, and audit a hand-saved one.

    python3 delta.py            # render the return for the fabricated evaluation; exits 0
    python3 delta.py --check    # audit saved-delta.md against the evaluation; exits 1

Standard library only, offline. The "model fills the slots" step is fill_item(),
done here by plain string substitution.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ITEM = re.compile(r"^(\d+)\. (.+?) - (\S+:\d+) - Axis: (\w+)\n\s+Passing looks like: (.+)$", re.M)
BRACKET = re.compile(r"\[[^\]\n]{2,}\]")


def blocking_items(evaluation: str) -> list:
    section = evaluation.split("## Blocking Issues Summary", 1)[1].split("\n## ", 1)[0]
    return ITEM.findall(section)


def fill_item(block: str, n: str, what: str, where: str, axis: str, passing: str, run: dict) -> str:
    return (block.replace("[ITEM_NUMBER]", n).replace("[Brief description]", what)
            .replace("[axis]", axis).replace("[N]/5 (threshold: [T]/5)",
            f"{run['scores'][axis]}/5 (threshold: {run['thresholds'][axis]}/5)")
            .replace("[file:line]", where).replace("[description]", what)
            .replace("[the minimum fix needed]", passing))


def render() -> str:
    run = json.loads((HERE / "run.json").read_text(encoding="utf-8"))
    template = (HERE / "template.md").read_text(encoding="utf-8")
    head, rest = template.split("### [ITEM_NUMBER]", 1)
    block, tail = ("### [ITEM_NUMBER]" + rest).split("\n## Constraints", 1)
    items = blocking_items((HERE / "evaluation.md").read_text(encoding="utf-8"))
    out = head.replace("[SPRINT_ID]", run["sprint"]).replace("[N+1]", str(run["iteration"] + 1)) \
        .replace("[N]", str(run["iteration"]))
    out += "\n".join(fill_item(block.strip() + "\n", *i, run) for i in items)
    return out + "\n## Constraints" + tail


def check() -> int:
    saved = (HERE / "saved-delta.md").read_text(encoding="utf-8")
    evaluation = (HERE / "evaluation.md").read_text(encoding="utf-8")
    wanted = blocking_items(evaluation)
    present = re.findall(r"^### \d+\. ", saved, re.M)
    findings = []
    saved_axes = re.findall(r"\*\*Axis:\*\* (\w+)", saved)
    for _, what, where, axis, _ in wanted:
        if axis not in saved_axes:
            findings.append(f"blocker missing from the return: axis {axis} ({where})")
    note = evaluation.split("## Non-Blocking Notes", 1)[1]
    for line in re.findall(r"^- (.+?) - \S+:\d+ - Not a blocker", note, re.M):
        if line.lower() in saved.lower():
            findings.append(f"a non-blocking note was carried in: '{line}'")
    for slot in BRACKET.findall(saved):
        findings.append(f"unfilled slot left in the saved return: {slot}")
    shown = re.findall(r"threshold: (\d)/5", saved)
    if shown:
        findings.append(f"the builder is shown {len(shown)} thresholds - the bar it is told not to aim at")
    if "minimum fix" in (HERE / "template.md").read_text(encoding="utf-8"):
        findings.append("the template's last field asks for the minimum fix, from a grader told not to suggest one")
    print(f"evaluation lists {len(wanted)} blockers; the saved return has {len(present)} items")
    for f in findings:
        print("FINDING:", f)
    print(f"{len(findings)} findings (exit 1 marks them, not an error)")
    return 1 if findings else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        sys.exit(check())
    if sys.argv[1:]:
        print("usage: delta.py [--check]", file=sys.stderr)
        sys.exit(2)
    print(render())
