#!/usr/bin/env python3
"""Remediation plan template — fill it from an investigation, then check that what
came out is a plan and not a filled-in form.

    python3 plan.py                    render from investigation.json and check it
    python3 plan.py --print            ... and print the rendered plan
    python3 plan.py --check bad-plan.md   check an existing plan

The checks are what the source template had no equivalent of. Exit codes: 0 = the
plan passes. 1 = the plan has defects (bad-plan.md has them on purpose).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLACEHOLDER = re.compile(r"\{\{\w+\}\}|<(?!!--)[a-z][^>\n]*>")


def render(inv: dict) -> str:
    fill = dict(inv)
    fill["evidence"] = "\n".join(f"- {e}" for e in inv["evidence"])
    fill["rejected"] = "\n".join(f"- {r}" for r in inv["rejected"])
    fill["steps"] = "\n".join(f"{i}. {s}" for i, s in enumerate(inv["steps"], 1))
    fill["rollback"] = "\n".join(f"{i}. {s}" for i, s in enumerate(inv["rollback"], 1))
    fill["verification"] = "\n".join(f"- [ ] {v}" for v in inv["verification"])
    fill["progression"] = "\n".join("| " + " | ".join(r) + " |" for r in inv["progression"])
    fill["redaction"] = "\n".join(f"- {r}" for r in inv["redaction"]) or "none detected"
    doc = (HERE / "template.md").read_text()
    for k, v in fill.items():
        if isinstance(v, str):
            doc = doc.replace("{{" + k + "}}", v)
    return doc


def parse(doc: str) -> tuple[dict, dict]:
    _, fm, body = doc.split("---", 2)
    front = dict(re.findall(r'^(\w+):\s*"?([^"\n]*)"?\s*$', fm, re.M))
    sections = {}
    for chunk in re.split(r"^## ", body, flags=re.M)[1:]:
        head, _, text = chunk.partition("\n")
        sections[head.strip()] = text.strip()
    return front, sections


def check(doc: str) -> list[str]:
    front, sec = parse(doc)
    found = []

    for m in PLACEHOLDER.finditer(doc):
        line = doc[: m.start()].count("\n") + 1
        found.append(f"line {line}: unfilled placeholder {m.group(0)}")

    ctx = sec.get("Context", "")
    m = re.search(r"Cluster / Namespace:\*\*\s*`([^`]*)`\s*/\s*`([^`]*)`", ctx)
    if m and (m.group(1), m.group(2)) != (front.get("cluster"), front.get("namespace")):
        found.append(f"frontmatter says {front.get('cluster')}/{front.get('namespace')}, "
                     f"Context says {m.group(1)}/{m.group(2)}")
    m = re.search(r"Option `(\w+)`", sec.get("Chosen Option", ""))
    if m and m.group(1) != front.get("ranked_option"):
        found.append(f"frontmatter ranked_option {front.get('ranked_option')}, "
                     f"Chosen Option says {m.group(1)}")

    rc = sec.get("Root Cause", "")
    if "`confirmed`" in rc:
        ev = rc.split("**Evidence:**", 1)[-1]
        real = [l for l in ev.splitlines() if l.startswith("- ") and not PLACEHOLDER.search(l)]
        if len(real) < 2:
            found.append(f"status 'confirmed' with {len(real)} piece(s) of real evidence")

    rows = [r for r in sec.get("Environment Progression", "").splitlines()
            if r.startswith("|") and not r.startswith("|--") and "Prerequisite" not in r]
    copied = [r.split("|")[1].strip() for r in rows[1:]
              if any(c.strip() == "same" for c in r.split("|")[3:5])]
    if copied:
        found.append(f"progression rows {', '.join(copied)} say 'same': no environment-specific check")

    if not re.search(r"^\d+\.", sec.get("Rollback", ""), re.M):
        found.append("Rollback has no ordered steps")
    if not sec.get("Redaction Review"):
        found.append("Redaction Review is empty — it must list what was scrubbed, or say 'none detected'")
    return found


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", metavar="PLAN", help="check an existing plan instead")
    ap.add_argument("--print", action="store_true", help="print the rendered plan")
    a = ap.parse_args()

    if a.check:
        name, doc = a.check, (HERE / a.check).read_text()
    else:
        name, doc = "rendered from investigation.json", render(json.loads((HERE / "investigation.json").read_text()))
        if a.print:
            print(doc)
    problems = check(doc)
    print(f"{name}: {len(problems)} defect(s)")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
