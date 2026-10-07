#!/usr/bin/env python3
"""Diff the sprint state template against the two builders that are supposed
to produce it.

    python3 drift.py

Reports fields only one copy has, values that differ between copies,
checkpoints with relative deadlines or no deliverables, and whether any
builder reads the template its usage line points at.

Exit codes: 0 = the three copies agree. 1 = they drift (the demonstration).
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import builders

HERE = Path(__file__).resolve().parent
TODAY = "2026-01-12"


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        if k.startswith("_"):
            continue
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def reads_template(path: Path) -> bool:
    """Does the builder module mention template.json anywhere it could open it?"""
    tree = ast.parse(path.read_text())
    return any(isinstance(n, ast.Constant) and isinstance(n.value, str) and "template.json" in n.value
               for n in ast.walk(tree))


def main() -> int:
    template = json.loads((HERE / "template.json").read_text())
    copies = {
        "template": flatten(template),
        "detector": flatten(builders.build_from_detector(["web-frontend", "payments", "vendor-ingress"], TODAY)),
        "init": flatten(builders.build_from_init(TODAY)),
    }
    findings = 0

    print("fields only some copies have")
    keys = sorted(set().union(*copies.values()))
    for k in keys:
        have = [n for n, c in copies.items() if k in c]
        if len(have) < len(copies) and not k.startswith(("sprint.name", "sprint.created", "sprint.output_dir")):
            findings += 1
            print(f"  {k:<40} only in {', '.join(have)}")

    print("\nvalues that differ between copies")
    for k in ("workstreams.B.requires_trigger", "workstreams.C.owned_roles"):
        vals = {n: c.get(k) for n, c in copies.items()}
        if len({json.dumps(v) for v in vals.values()}) > 1:
            findings += 1
            print(f"  {k}")
            for n, v in vals.items():
                print(f"    {n:<9} {v}")

    print("\ncheckpoints")
    for n, c in copies.items():
        for cp in "ABC":
            target, deliv = c.get(f"checkpoints.{cp}.target", ""), c.get(f"checkpoints.{cp}.deliverables", [])
            notes = []
            if "tomorrow" in target:
                notes.append(f"relative deadline '{target}'")
            if not deliv:
                notes.append("no deliverables")
            if notes:
                findings += 1
                print(f"  {n:<9} {cp}: {'; '.join(notes)}")

    print("\nthe usage line")
    print(f"  template says: {template['_usage']}")
    if not reads_template(HERE / "builders.py"):
        findings += 1
        print("  builders.py never names template.json — editing the template changes no sprint")

    print(f"\n{findings} disagreements between three copies of one structure")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
