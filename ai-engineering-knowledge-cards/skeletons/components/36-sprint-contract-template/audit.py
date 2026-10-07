#!/usr/bin/env python3
"""Audit a contract template against a writer that never opens it.

Everything here is a stand-in. `emit` is a contract writer in the component's
design: it builds its text from its own strings and takes the template only as
a name in its docstring. `read_axes` is a reader shaped like the evaluation
validator's: it keeps rows whose first cell is a name and whose second is N/5.

Exit 0: --emit printed a contract.  Exit 1: the audit found problems (on purpose).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def emit(sprint: str, axes: list, thresholds: dict, out_of_scope: list, version: int = 1) -> str:
    """Build a contract from inputs. Uses the template as a structural guide, by name only."""
    rows = "\n".join(
        f"| {a} | {thresholds[a]}/5 | {'high' if thresholds[a] >= 4 else 'standard'} |" for a in axes
    )
    scope = "\n".join(f"- {item}" for item in out_of_scope) or "- None specified"
    return (
        f"# Sprint Contract: {sprint}\n\n**Version:** {version}\n**Status:** active\n\n"
        f"## Evaluation Axes\n\n| Axis | Threshold | Weight |\n|---|---|---|\n{rows}\n\n"
        "## Scoring Rules\n\n- Scale: 1-5 integer per axis\n- Pass: score meets threshold on every axis\n"
        "- Evidence is cited for every score\n\n"
        f"## Out of Scope\n\n{scope}\n\n"
        "## Contract Rules\n\n1. Frozen once implementation begins.\n2. A change needs a new version.\n"
        "3. The evaluator scores strictly against this contract.\n"
        "4. The generator may read the axes; grading itself against them is not allowed.\n"
        "5. Out-of-scope items are not penalised.\n"
    )


def read_axes(contract_text: str) -> dict:
    """Axis -> threshold, for every row that looks like `| name | N/5 | ...`."""
    found = {}
    for line in contract_text.splitlines():
        m = re.match(r"^\|\s*([A-Za-z0-9_ ]+?)\s*\|\s*([1-5])/5\s*\|", line)
        if m and m.group(1).lower() != "axis":
            found[m.group(1).lower()] = int(m.group(2))
    return found


def headings(text: str) -> list:
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", text, re.M)]


def numbered_rules(text: str) -> int:
    return len(re.findall(r"^\d+\.\s", text.split("## Contract Rules")[-1], re.M))


def report(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'ok' if ok else 'FINDING'}] {label}: {detail}")
    return ok


def audit(spec: dict) -> int:
    template = (HERE / "contract.template.md").read_text(encoding="utf-8")
    emitted = emit(spec["sprint"], spec["axes"], spec["thresholds"], spec["out_of_scope"])
    findings = 0

    missing = [h for h in headings(template) if h not in headings(emitted)]
    cols = "Description" in template and "Description" not in emitted
    rules = (numbered_rules(template), numbered_rules(emitted))
    findings += not report(
        "template versus writer",
        not (missing or cols or rules[0] != rules[1]),
        f"writer omits sections {missing}, the Description column ({cols}); rules {rules[0]} vs {rules[1]}",
    )

    work = Path(tempfile.mkdtemp(prefix="contract-audit-"))
    try:
        target = work / "contract.md"
        target.write_text(emitted, encoding="utf-8")
        lowered = {a: 1 for a in spec["axes"]}
        try:
            target.write_text(emit(spec["sprint"], spec["axes"], lowered, spec["out_of_scope"]), encoding="utf-8")
            refused = False
        except OSError:
            refused = True
        now = read_axes(target.read_text(encoding="utf-8"))
        findings += not report(
            "frozen contract",
            refused,
            f"second write for the same sprint and version succeeded; thresholds now {now}; "
            f"copies kept: {len(list(work.iterdir())) - 1}; the template's 'superseded' status was set by nothing",
        )
    finally:
        shutil.rmtree(work)

    heavy = emit("w", ["a_axis", "b_axis", "c_axis"], {"a_axis": 3, "b_axis": 3, "c_axis": 3}, [])
    flipped = heavy.replace("| standard |", "| high |")
    findings += not report(
        "weight column",
        read_axes(heavy) != {} and read_axes(heavy) != read_axes(flipped),
        f"every weight flipped, reader output unchanged: {read_axes(heavy) == read_axes(flipped)}",
    )

    filled = template.replace("[axis_name] | [N]/5", "correctness | 4/5", 1)
    filled = filled.replace("[axis_name] | [N]/5", "api-design | 3/5", 1)
    parsed = read_axes(filled)
    findings += not report(
        "skipped rows",
        len(parsed) == 3,
        f"3 rows written (one filled, one hyphenated name, one still a placeholder); reader kept {len(parsed)}: "
        f"{sorted(parsed)}; no error raised",
    )
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emit", action="store_true", help="print the contract the writer builds")
    args = ap.parse_args()
    spec = json.loads((HERE / "axes.json").read_text(encoding="utf-8"))
    if args.emit:
        print(emit(spec["sprint"], spec["axes"], spec["thresholds"], spec["out_of_scope"]), end="")
        return 0
    return audit(spec)


if __name__ == "__main__":
    sys.exit(main())
