#!/usr/bin/env python3
"""Benchmark report parser — result lines in, classified findings out.

    python3 parse.py [report.md]            findings as JSON
    python3 parse.py --audit [report.md]    what the classification gets wrong

Each result line is tried against a pattern whose status brackets are optional,
then against a second pattern written for lines without brackets. Findings are
classed by control-ID prefix, and a FAIL in the control-plane class requires
platform-team approval. Applicability is guessed from the description.

Exit codes: 0 = parsed. 1 = --audit found what the design gets wrong (the
demonstration), or the report is missing. 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Sections sent to the platform team. The etcd section is on no list.
CLASSES = (("1.", "control_plane"), ("3.", "control_plane"),
           ("4.", "worker_node"), ("5.", "policy"))

# Applicability guessed from free text: the deprecated pod security policy and
# a kubelet feature gate.
LIKELY_NA = (re.compile(r"PodSecurityPolic(y|ies)", re.I),
             re.compile(r"admission-plugins\b.*\bPodSecurity", re.I),
             re.compile(r"RotateKubeletServerCertificate", re.I))

RESULT = r"(?P<status>PASS|FAIL|WARN|INFO)\]?[ \t]+(?P<id>\d+(?:\.\d+)*)[ \t]+(?P<text>.+)$"
BRANCHES = (("brackets optional", re.compile(r"^\[?" + RESULT)),
            ("no brackets", re.compile(r"^" + RESULT.replace(r"\]?", ""))))


def classify(control: str) -> str:
    return next((c for prefix, c in CLASSES if control.startswith(prefix)), "other")


def na_pattern(text: str) -> str | None:
    return next((p.pattern for p in LIKELY_NA if p.search(text)), None)


def parse(report: str) -> tuple[dict, dict]:
    findings, branch_hits = [], {name: 0 for name, _ in BRANCHES}
    section = ""
    for line in report.splitlines():
        if line.startswith("#"):
            section = line.lstrip("# ").strip()
            continue
        for name, pattern in BRANCHES:
            m = pattern.match(line)
            if not m:
                continue
            branch_hits[name] += 1
            f = {"control_id": m["id"], "status": m["status"], "description": m["text"],
                 "section": section, "classification": classify(m["id"]),
                 "likely_na": na_pattern(m["text"]) is not None}
            if f["status"] == "FAIL":
                f["requires_approval"] = f["classification"] == "control_plane"
            findings.append(f)
            break
    fails = [f for f in findings if f["status"] == "FAIL"]
    result = {
        "total": len(findings),
        **{s.lower(): sum(f["status"] == s for f in findings) for s in ("PASS", "FAIL", "WARN")},
        "control_plane_fails": sum(f["classification"] == "control_plane" for f in fails),
        "actionable_fails": sum(not f["likely_na"] for f in fails),
        "findings": findings,
    }
    return result, branch_hits


def audit(result: dict, branch_hits: dict, raw: str) -> int:
    expect = json.loads((HERE / "expect.json").read_text())
    findings = 0

    print("approval")
    etcd = [f for f in result["findings"]
            if f["status"] == "FAIL" and f["control_id"].startswith(expect["etcd_section"])]
    for f in etcd:
        findings += 1
        print(f"  {f['control_id']:7} classed {f['classification']!r}, "
              f"requires_approval {f['requires_approval']} — {f['description'][:50]}…")
    cp = [f["control_id"] for f in result["findings"] if f.get("requires_approval")]
    print(f"  needing platform-team approval: {', '.join(cp)} only")

    print("\nparsing branches")
    unbracketed = [l for l in raw.splitlines() if BRANCHES[1][1].match(l)]
    for name, hits in branch_hits.items():
        print(f"  {name:18} {hits} lines")
    if branch_hits["no brackets"] == 0 and unbracketed:
        findings += 1
        print(f"  the {len(unbracketed)} line(s) written for the second branch all went to the first")

    print("\nnot applicable, by description")
    for f in result["findings"]:
        if f["likely_na"]:
            live = expect["live_controls"].get(f["control_id"])
            findings += bool(live)
            note = f"  <- {live}" if live else ""
            print(f"  {f['control_id']:7} matched /{na_pattern(f['description'])}/{note}")

    print(f"\n{findings} findings — the parser runs clean; its classes are wrong")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", nargs="?", default=str(HERE / "report.md"))
    ap.add_argument("--audit", action="store_true", help="show what the classes get wrong")
    a = ap.parse_args()

    path = Path(a.report)
    if not path.is_file():
        print(json.dumps({"error": f"report not found: {path.name}"}))
        return 1
    raw = path.read_text()
    result, branch_hits = parse(raw)
    if a.audit:
        return audit(result, branch_hits, raw)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
