#!/usr/bin/env python3
"""Checkpoint status report — fill a template from a sprint state, then check
what the fill left behind.

    python3 render.py            render template.md from state.json to stdout
    python3 render.py --check    render, then look for what nothing in the
                                 source looked for

The renderer fills what the state file holds, the way the model fills the
source template: the header, the workstream rows, a trigger state when it is
one of the words the slot offers, and the evidence lines it has values for.
Everything else stays a bracketed slot.

Exit codes: 0 = rendered. 1 = --check found defects in the rendered report
(the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLOT = re.compile(r"\[([^\]\n]+)\]")


def render(template: str, state: dict) -> str:
    rows = "\n".join(f"| {k} | {w['name']} | {w['status']} | {w['validation']} |"
                     for k, w in state["workstreams"].items())
    out = template.format(checkpoint=state["checkpoint"], sprint=state["sprint"],
                          environment=state["environment"], workstream_rows=rows)
    lines = []
    for line in out.splitlines():
        trig = re.match(r"\| (.+?) \| \[([^\]]+)\] \|$", line)
        if trig and trig.group(1) in state["triggers"]:
            value = state["triggers"][trig.group(1)]
            if value in trig.group(2).split("/"):
                line = f"| {trig.group(1)} | {value} |"
        ev = re.match(r"- (.+?): \[", line)
        if ev and ev.group(1) in state["evidence"]:
            line = f"- {ev.group(1)}: {state['evidence'][ev.group(1)]}"
        lines.append(line)
    return "\n".join(lines) + "\n"


def check(report: str, template: str, state: dict) -> int:
    findings = 0
    print("slots left unfilled")
    for n, line in enumerate(report.splitlines(), 1):
        for m in SLOT.finditer(line):
            findings += 1
            print(f"  line {n:<3} [{m.group(1)}]")

    print("\ntrigger states the template has no word for")
    for trig, value in state["triggers"].items():
        m = re.search(rf"\| {re.escape(trig)} \| \[([^\]]+)\] \|", template)
        offered = m.group(1).split("/") if m else []
        if value not in offered:
            findings += 1
            allowed = state["trigger_vocabulary"][trig]
            print(f"  {trig}: state file says '{value}'; template offers {len(offered)} "
                  f"of the {len(allowed)} states the state file allows")

    print("\ncounts written into the template")
    m = re.search(r"all (\d+) pods", template)
    if m and int(m.group(1)) != state["secrets_store_pods"]:
        findings += 1
        print(f"  health line asks about {m.group(1)} pods; this cluster runs {state['secrets_store_pods']}")

    print(f"\n{findings} defects in a report the template's shape allows")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="check the rendered report")
    a = ap.parse_args()
    template = (HERE / "template.md").read_text()
    state = json.loads((HERE / "state.json").read_text())
    report = render(template, state)
    sys.stdout.write(report)
    if a.check:
        print("\n---\n")
        return check(report, template, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
