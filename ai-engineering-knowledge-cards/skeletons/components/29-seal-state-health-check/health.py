#!/usr/bin/env python3
"""Seal-state health checker — generates the commands an operator runs against
the secrets store, and parses what they printed. Then a check of how the two
halves fit together.

    python3 health.py generate                    commands for the operator, as JSON
    python3 health.py parse captured-marked.txt   seal state per pod, as JSON
    python3 health.py                             the demonstration: all three fixtures

Parse mode reads output split into per-pod sections by a '=== <pod> ===' line.
Generate mode emits one command per pod, and those commands print no such line.

Exit codes: generate and parse exit 0 — parse included, healthy or not, as in the
component; only the JSON says which. The demonstration exits 1. 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NS = "secrets"
PODS = ("store-0", "store-1", "store-2")   # fixed, as in the component


def generate() -> dict:
    checks = [{"id": f"status_{p}", "command": f"kubectl -n {NS} exec {p} -- vault status"} for p in PODS]
    checks += [{"id": "pods", "command": f"kubectl -n {NS} get pods"},
               {"id": "cert", "command": f"kubectl -n {NS} get certificate"}]
    unseal = [{"id": f"unseal_{p}", "command": f"kubectl -n {NS} exec -it {p} -- vault operator unseal",
               "note": "interactive; repeat once per key share up to the threshold"} for p in PODS]
    return {"health_checks": checks, "unseal_procedure": unseal,
            "note": "for manual execution by an operator"}


def parse(text: str) -> dict:
    parts = re.split(r"(?:^|\n)=== (\S+) ===", text)
    pods = []
    for i in range(1, len(parts), 2):
        m = re.search(r"^Sealed\s+(true|false)", parts[i + 1], re.M | re.I)
        pods.append({"name": parts[i], "sealed": None if not m else m.group(1).lower() == "true"})
    if not pods:
        return {"healthy": False, "warning": "could not parse: expected '=== <pod> ===' sections"}
    unsealed = sum(p["sealed"] is False for p in pods)
    sealed = sum(p["sealed"] is True for p in pods)
    healthy = sealed == 0 and unsealed == len(PODS)
    return {"pods": pods, "healthy": healthy,
            "summary": f"{unsealed}/{len(PODS)} pods unsealed" + ("" if healthy else " — action required")}


def demo() -> int:
    findings = 0
    g = generate()
    interactive = [c["command"] for c in g["unseal_procedure"] if " -it " in c["command"]]
    print(f"generate: {len(g['health_checks'])} read-only checks and {len(interactive)} interactive "
          f"unseal commands, in one output")
    findings += bool(interactive)

    for name, expect in (("captured-plain.txt", "what the generated commands print"),
                         ("captured-marked.txt", "with the markers only the runbook's loop adds"),
                         ("captured-four.txt", "a healthy set of four pods")):
        r = parse((HERE / name).read_text())
        verdict = r.get("summary") or r.get("warning")
        print(f"parse {name:20} ({expect}): healthy={r['healthy']}  {verdict}")
        if name != "captured-marked.txt" and not r["healthy"]:
            findings += 1

    print("\nparse exits 0 in every case above; a caller that checks the exit code sees no difference")
    print(f"\n{findings} findings — generate and parse were written against different output shapes")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", nargs="?", choices=["generate", "parse"])
    ap.add_argument("file", nargs="?", help="captured output, for parse")
    a = ap.parse_args()
    if a.mode is None:
        return demo()
    if a.mode == "generate":
        print(json.dumps(generate(), indent=2))
        return 0
    if not a.file:
        ap.error("parse needs a file of captured output")
    print(json.dumps(parse(Path(a.file).read_text()), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
