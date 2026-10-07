#!/usr/bin/env python3
"""Workstream gate runner — offline gates for one workstream, plus the cluster
commands an operator should run. Then a check of what passes and why.

    python3 run_gates.py --workstream A --plan plan.json
    python3 run_gates.py --workstream B --plan plan.json --cluster-access
    python3 run_gates.py --audit

The gates are a fixed table per workstream: local commands (lint, syntax) and
file-existence checks run here; cluster commands are only printed. Local
commands go through run_local(), a stub that prints instead of opening a shell
and returns the exit code recorded in local-results.json.

The plan argument is required and never read — as in the component.

Exit codes: 0 = overall PASS. 1 = overall FAIL, or --audit found what the
gates let through (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "fixture-repo"
NS, PODS = "secrets", ("store-0", "store-1", "store-2")

LINT = {"id": "lint", "cmd": "make lint", "blocking": False}
SYNTAX = {"id": "syntax", "cmd": "make syntax-check", "blocking": True}
STATUS = [f"kubectl -n {NS} exec {p} -- vault status" for p in PODS]

GATES = {
    "A": {"offline": [LINT, SYNTAX, {"id": "tls_task", "exists": "roles/secrets-store/tasks/tls.yml"}],
          "cluster": STATUS + ["kubectl get certificate -A"]},
    "B": {"offline": [LINT, SYNTAX, {"id": "unseal_task", "exists": "roles/secrets-store/tasks/unseal.yml"}],
          "cluster": STATUS + [f"kubectl -n {NS} delete pod store-0 && sleep 30 && "
                               f"kubectl -n {NS} exec store-0 -- vault status"]},
    "C": {"offline": [LINT, SYNTAX],
          "cluster": ["kubectl get policyreport -A", "kubectl get clusterpolicyreport"]},
    "D": {"offline": [{"id": "triage_table", "exists": "out/hardening-*/triage-table.md"}],
          "cluster": ["kubectl -n kube-system logs job/kube-bench"]},
    "E": {"offline": [{"id": "hygiene_report", "exists": "out/hardening-*/hygiene-report.md"}],
          "cluster": ["kubectl get pods -A", "helm list -A", "kubectl get nodes"]},
}
# Which step of the skill writes each file a gate looks for. None: no step does.
PRODUCERS = {"triage-table.md": "the triage table renderer", "hygiene-report.md": None}
WRITE_VERBS = re.compile(r"\b(delete|apply|patch|scale|drain|cordon|rollout restart|unseal)\b")


def run_local(cmd: str) -> int:
    """Stub for subprocess.run(cmd, shell=True, cwd=repo). Prints, never executes."""
    print(f"[stub] run_local: would run `{cmd}` through a shell in fixture-repo/", file=sys.stderr)
    return json.loads((HERE / "local-results.json").read_text()).get(cmd, 0)


def run_gate(gate: dict) -> dict:
    if "exists" in gate:
        found = sorted(REPO.glob(gate["exists"]))
        return {"id": gate["id"], "status": "PASS" if found else "FAIL", "blocking": True,
                "matched": [str(p.relative_to(REPO)) for p in found]}
    code = run_local(gate["cmd"])
    return {"id": gate["id"], "status": "PASS" if code == 0 else "FAIL", "blocking": gate["blocking"]}


def validate(ws: str, plan: str, cluster_access: bool = False) -> dict:
    """`plan` is accepted and never opened — as in the component."""
    results = [run_gate(g) for g in GATES[ws]["offline"]]
    failed = [r for r in results if r["status"] != "PASS"]
    out = {"workstream": ws, "gates": results,
           "overall": "FAIL" if any(r["blocking"] for r in failed) else "PASS"}
    if cluster_access:
        out["run_manually"] = [{"command": c, "kind": "write" if WRITE_VERBS.search(c) else "read"}
                               for c in GATES[ws]["cluster"]]
    return out


def audit() -> int:
    plan = json.loads((HERE / "plan.json").read_text())   # the audit reads it; the runner never does
    findings = []

    r = validate("A", "no-such-plan.json")
    if r["overall"] == "PASS":
        findings.append("plan argument: a path that does not exist is accepted, and A still passes")

    for ws, g in (("A", "tls_task"), ("B", "unseal_task")):
        gate = next(x for x in validate(ws, "")["gates"] if x["id"] == g)
        path = REPO / gate["matched"][0] if gate["matched"] else None
        if gate["status"] == "PASS" and path and "Stub" in path.read_text():
            findings.append(f"{ws} {g}: passes on {gate['matched'][0]}, a stub that existed before any work")

    for ws in "DE":
        gate = validate(ws, "")["gates"][0]
        for m in gate["matched"]:
            if not m.startswith(plan["output_dir"] + "/"):
                findings.append(f"{ws} {gate['id']}: passes on {m}, written by an earlier sprint")
        name = Path(GATES[ws]["offline"][0]["exists"]).name
        if PRODUCERS.get(name) is None:
            findings.append(f"{ws} {gate['id']}: no step of the skill writes {name}; the gate fails until someone writes one by hand")

    r = validate("A", "")
    lint = next(x for x in r["gates"] if x["id"] == "lint")
    if lint["status"] == "FAIL" and r["overall"] == "PASS":
        findings.append("lint fails and the overall result is PASS — lint is never blocking")

    local = sorted({g["cmd"] for ws in GATES for g in GATES[ws]["offline"] if "cmd" in g})
    findings.append(f"{len(local)} local commands executed through a shell, not generated: {', '.join(local)}")

    for ws in GATES:
        for c in validate(ws, "", cluster_access=True)["run_manually"]:
            if c["kind"] == "write":
                findings.append(f"{ws} cluster 'validation' is a write: {c['command']}")

    print()
    for f in findings:
        print(f"  {f}")
    print(f"\n{len(findings)} findings — the gates check that something exists, not that this sprint made it")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workstream", choices=sorted(GATES))
    ap.add_argument("--plan", help="required, as in the component — and never read")
    ap.add_argument("--cluster-access", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    if a.audit:
        return audit()
    if not a.workstream or not a.plan:
        ap.error("--workstream and --plan are required")
    result = validate(a.workstream, a.plan, a.cluster_access)
    print(json.dumps(result, indent=2))
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
