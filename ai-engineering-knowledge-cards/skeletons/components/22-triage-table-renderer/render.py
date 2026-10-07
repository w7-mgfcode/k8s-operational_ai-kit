#!/usr/bin/env python3
"""Triage table renderer — parsed benchmark findings in, a triage table out.

    python3 render.py                      render parsed-findings.json to stdout
    python3 render.py other.json           render another findings file
    python3 render.py --check              where each disposition came from

The renderer can write two dispositions: NA, when the parser's likely-NA flag
is set, and TBD for everything else. --check counts them by origin, runs the
gate "every failure has a disposition" over the table, and compares the
rendered legend with the template's.

Exit codes: 0 = rendered. 1 = --check found the gate passing with no human
decision, or the legends disagreeing (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WIDTH = 80          # descriptions are cut here, with no marker

LEGEND = {
    "implement": "Fix in this sprint — actionable with clear ownership",
    "defer": "Document and move to the next sprint",
    "NA": "Not applicable to this platform",
    "TBD": "Needs human triage",
}


def disposition(f: dict) -> tuple[str, str]:
    """The only two the renderer can produce."""
    return ("NA", "deprecated — not applicable") if f.get("likely_na") else ("TBD", "to do")


def render(data: dict) -> list[str]:
    findings = data["findings"]
    out = [
        "# Benchmark triage",
        "",
        f"Report: {data.get('report_path', 'n/a')} | FAIL {data.get('fail', 0)} | "
        f"WARN {data.get('warn', 0)} | PASS {data.get('pass', 0)}",
        "",
        "| Control | Description | Class | Disposition | Rationale | Owner | Target |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in sorted((f for f in findings if f["status"] == "FAIL"), key=lambda f: f["control_id"]):
        code, why = disposition(f)
        cls = f["classification"] + (" (needs approval)" if f.get("requires_approval") else "")
        out.append(f"| {f['control_id']} | {f['description'][:WIDTH]} | {cls} | {code} | {why} | TBD | TBD |")
    out += ["", "| Control | Description | Class | Disposition |", "|---|---|---|---|"]
    for f in sorted((f for f in findings if f["status"] == "WARN"), key=lambda f: f["control_id"]):
        out.append(f"| {f['control_id']} | {f['description'][:WIDTH]} | {f['classification']} | TBD |")
    out += ["", "| Code | Meaning |", "|---|---|"]
    out += [f"| **{k}** | {v} |" for k, v in LEGEND.items()]
    return out


def gate_every_failure_dispositioned(table: list[str]) -> bool:
    """The gate as a reader would write it: no failure row with an empty disposition."""
    rows = [r.split("|") for r in table if re.match(r"\| \d", r) and r.count("|") == 8]
    return all(cells[4].strip() for cells in rows)


def template_legend() -> dict[str, str]:
    legend = {}
    for line in (HERE / "template-legend.md").read_text().splitlines():
        m = re.match(r"\| \*\*(\w+)\*\* \| (.+) \|$", line)
        if m:
            legend[m.group(1)] = m.group(2)
    return legend


def check(data: dict) -> int:
    fails = [f for f in data["findings"] if f["status"] == "FAIL"]
    by_code: dict[str, list[str]] = {}
    for f in fails:
        by_code.setdefault(disposition(f)[0], []).append(f["control_id"])

    print("dispositions on failing controls, by origin")
    print(f"  NA   from the parser's pattern match : {len(by_code.get('NA', []))}  {by_code.get('NA', [])}")
    print(f"  TBD  placeholder                     : {len(by_code.get('TBD', []))}  {by_code.get('TBD', [])}")
    print("  implement / defer                     : 0  (the renderer cannot write either)")
    print("  decided by a human                    : 0")

    table = render(data)
    passed = gate_every_failure_dispositioned(table)
    print(f"\ngate \"every failure has a disposition\": {'PASS' if passed else 'FAIL'}"
          + (" — with no human decision in the table" if passed else ""))

    cut = [f["control_id"] for f in data["findings"]
           if f["status"] in ("FAIL", "WARN") and len(f["description"]) > WIDTH]
    if cut:
        print(f"descriptions cut at {WIDTH} characters, unmarked: {cut}")

    theirs = template_legend()
    differ = [k for k in LEGEND if LEGEND[k] != theirs.get(k)]
    print(f"\nlegend: {len(differ)} of {len(LEGEND)} codes worded differently from the template")
    for k in differ:
        print(f"  {k:9} renderer: {LEGEND[k]}")
        print(f"  {'':9} template: {theirs.get(k)}")

    return 1 if passed or differ else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings", nargs="?", default=str(HERE / "parsed-findings.json"))
    ap.add_argument("--check", action="store_true", help="count dispositions by origin")
    a = ap.parse_args()
    try:
        data = json.loads(Path(a.findings).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        ap.error(f"cannot read findings: {exc}")

    if a.check:
        return check(data)
    print("\n".join(render(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
