#!/usr/bin/env python3
"""Check a filled benchmark triage table against the template's own rules.

    python3 check_table.py                 check filled.md
    python3 check_table.py some-table.md   check another filled table

The legend is read from template.md. The decision rules cannot be: they are
prose, so they are transcribed below by hand — which is the component's gap in
miniature. The check then does what nothing in the source did: hold every row
to the legend and the rules, and recompute the summary from the rows.

Exit codes: 0 = the table obeys its template. 1 = findings (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Transcribed from template.md's "Decision rules" — prose, not data.
APPROVAL_SECTIONS = {"1", "3"}        # control plane: approval before implement
DIRECT_SECTIONS = {"4"}               # worker nodes: implement directly
REVIEW_SECTIONS = {"5"}               # policies: review against workstream C
PLACEHOLDER_RATIONALES = {"deprecated/na", "todo", ""}


def table_after(text: str, heading: str) -> list[dict[str, str]]:
    """Rows of the first Markdown table under a '## heading'."""
    block = text.split(f"## {heading}", 1)
    if len(block) < 2:
        return []
    lines: list[str] = []
    for l in block[1].splitlines():
        if l.startswith("|"):
            lines.append(l)
        elif lines:
            break                       # the first table ends at its first non-row line
    if len(lines) < 2:
        return []
    cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    head = cells(lines[0])
    return [dict(zip(head, cells(l))) for l in lines[2:]]


def summary(text: str) -> dict[str, int]:
    return {k.strip(): int(v) for k, v in re.findall(r"^- ([^:]+): (\d+)$", text, re.M)}


def check(filled: str, template: str) -> list[str]:
    legend = {r["Code"] for r in table_after(template, "Disposition legend")}
    rows = table_after(filled, "Failed controls")
    findings: list[str] = []
    counts = {"implement": 0, "defer": 0, "NA": 0, "TBD": 0, "approval": 0}

    for r in rows:
        cid, disp = r["Control ID"], r["Disposition"]
        section = cid.split(".")[0]
        why = r["Rationale"].lower()
        if disp not in legend:
            findings.append(f"{cid}: disposition '{disp}' is not in the legend {sorted(legend)}")
        else:
            counts[disp] += 1
        if section in APPROVAL_SECTIONS:
            counts["approval"] += 1
            if disp == "implement" and "approv" not in why:
                findings.append(f"{cid}: control-plane item set to implement with no approval "
                                "recorded (the table has no approval column; only the rationale was searched)")
        elif section not in DIRECT_SECTIONS | REVIEW_SECTIONS:
            findings.append(f"{cid}: section {section} matches no decision rule — "
                            f"classified '{r['Classification']}', disposition '{disp}' ungoverned")
        if disp == "TBD":
            findings.append(f"{cid}: still TBD, yet the file exists — the gate's only test")
        if disp == "NA" and why in PLACEHOLDER_RATIONALES:
            findings.append(f"{cid}: NA with a placeholder rationale — a pre-filled guess counted as dispositioned")

    stated = summary(filled)
    computed = {
        "Actionable failures": counts["implement"],
        "Control-plane failures needing approval": counts["approval"],
        "Deferred": counts["defer"],
        "Not applicable": counts["NA"],
        "Still undetermined": counts["TBD"],
    }
    for key, value in computed.items():
        if stated.get(key) != value:
            findings.append(f"summary '{key}' says {stated.get(key)}, the rows say {value}")

    header = re.search(r"FAIL: (\d+)", filled)
    if header and int(header.group(1)) != len(rows):
        findings.append(f"header says {header.group(1)} failures, the table has {len(rows)} rows")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", nargs="?", default=str(HERE / "filled.md"))
    a = ap.parse_args()
    try:
        filled = Path(a.table).read_text(encoding="utf-8")
    except OSError as exc:
        ap.error(f"cannot read {a.table}: {exc}")
    template = (HERE / "template.md").read_text(encoding="utf-8")

    findings = check(filled, template)
    print(f"{len(table_after(filled, 'Failed controls'))} failed controls checked against the template\n")
    for f in findings:
        print(f"  {f}")
    print(f"\n{len(findings)} findings. The source's gate checked only that the file exists, "
          "so this table would have passed it.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
