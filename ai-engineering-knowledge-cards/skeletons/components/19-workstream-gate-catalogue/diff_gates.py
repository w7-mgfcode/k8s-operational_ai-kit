#!/usr/bin/env python3
"""Workstream gate catalogue — the document and the code, compared gate by gate.

    python3 diff_gates.py                  every workstream
    python3 diff_gates.py --workstream B   one workstream

The catalogue (catalogue.json) is what the reference says each gate requires.
The runner table (runner.json) is what the gate runner actually checks. Both
describe one sprint; nothing in the component keeps them equal. This script
reports every place they disagree, and every file a gate checks that no script
in the skill writes.

Exit codes: 0 = the two halves agree. 1 = they disagree (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def keyed(gates: list[dict], ws: str | None) -> dict[tuple[str, str], dict]:
    return {(g["workstream"], g["gate"]): g for g in gates
            if ws is None or g["workstream"] == ws}


def compare(doc: dict, code: dict, ws: str | None) -> list[str]:
    findings = []
    d, c = keyed(doc["gates"], ws), keyed(code["gates"], ws)

    for key in sorted(d):
        name = f"{key[0]}/{key[1]}"
        if key not in c:
            findings.append(f"{name:22} in the document only — the runner never checks "
                            f"\"{d[key]['criterion']}\"")
            continue
        g, r = d[key], c[key]
        if g["blocking"] != r["blocking"]:
            findings.append(f"{name:22} document: blocking={g['blocking']}, "
                            f"runner: blocking={r['blocking']} — a failure here "
                            f"{'fails' if g['blocking'] else 'passes'} on paper and "
                            f"{'fails' if r['blocking'] else 'passes'} in code")
        if g.get("wait_seconds") != r.get("wait_seconds"):
            findings.append(f"{name:22} document waits {g.get('wait_seconds')}s, "
                            f"runner waits {r.get('wait_seconds')}s before it looks")
        if g["kind"] != r["kind"]:
            findings.append(f"{name:22} document checks {g['kind']} "
                            f"(\"{g['criterion']}\"), runner checks {r['kind']}")

    for key in sorted(set(c) - set(d)):
        findings.append(f"{key[0]}/{key[1]:20} in the runner only — no criterion written down")

    produced = code.get("produced_by", {})
    for key, g in sorted(c.items()):
        target = g.get("target")
        if target and target not in produced:
            findings.append(f"{key[0]}/{key[1]:20} checks {target}, and nothing in the "
                            f"skill writes it — the gate can only fail, or pass on a stale copy")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workstream", choices=list("ABCDE"), help="limit to one workstream")
    a = ap.parse_args()

    doc, code, runbook = load("catalogue.json"), load("runner.json"), load("runbook-excerpt.json")
    findings = compare(doc, code, a.workstream)

    scope = f"workstream {a.workstream}" if a.workstream else "all workstreams"
    print(f"gates where the catalogue and the runner disagree ({scope})\n")
    for f in findings:
        print(f"  {f}")
    if not findings:
        print("  none")

    if a.workstream is None:
        same = doc["post_apply_suite"] == runbook["post_apply_suite"]
        print("\npost-apply health suite: written in the catalogue and in the runbook set, "
              f"{'identical today' if same else 'already different'} — nothing compares them")

    print(f"\n{len(findings)} disagreements between two files that describe one sprint")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
