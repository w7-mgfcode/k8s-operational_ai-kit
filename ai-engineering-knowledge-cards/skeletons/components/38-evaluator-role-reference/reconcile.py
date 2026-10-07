#!/usr/bin/env python3
"""Reconcile what an evaluator role reference asks for with what is checked.

Two checks, each over fabricated files:

    python3 reconcile.py --formats   # one blocking issue in three shapes; exits 1
    python3 reconcile.py --version   # a declared contract version nothing compares; exits 1

Exit 2: a fixture is missing or an option is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCATION = re.compile(r"[\w/.-]+\.\w+:\d+(-\d+)?")


def elements(issue: str, axes: list) -> dict:
    """Which of the four required elements an issue text carries."""
    first = re.sub(r"^\d+\.\s*", "", issue.splitlines()[0])
    return {
        "what": bool(re.sub(r"[\W_]+", "", first)),
        "where": bool(LOCATION.search(issue)),
        "axis": any(a in issue for a in axes),
        "passing": "passing" in issue.lower(),
    }


def formats() -> int:
    cfg = json.loads((HERE / "issue-formats.json").read_text(encoding="utf-8"))
    axes = ["correctness", "error_handling", "test_coverage"]
    print(f"{'format':52} " + " ".join(f"{e:8}" for e in cfg["required_elements"]) + " numbered-item count")
    short = 0
    for name, text in cfg["formats"].items():
        got = elements(text, axes)
        count = len(re.findall(r"^\d+\.\s", text, re.M))
        short += not all(got[e] for e in cfg["required_elements"])
        print(f"{name:52} " + " ".join(f"{'yes' if got[e] else 'NO':8}" for e in cfg["required_elements"]) + f" {count}")
    print(f"\n{short} of {len(cfg['formats'])} shapes lack an element the same document requires; "
          "a counter of numbered items reads all three as one issue.")
    return 1 if short else 0


def axes_of(contract: str) -> dict:
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"^\|\s*([a-z_]+)\s*\|\s*([1-5])/5\s*\|", contract, re.M)}


def structure_check(evaluation: str, contract: str) -> list:
    """Every axis scored, and each label agrees with its threshold."""
    thresholds, errors = axes_of(contract), []
    scored = {m.group(1): (int(m.group(2)), m.group(3))
              for m in re.finditer(r"^###\s+(\S+)\s+-\s+Score:\s*(\d)/5\s+-\s+(PASS|FAIL)", evaluation, re.M)}
    for axis, t in thresholds.items():
        if axis not in scored:
            errors.append(f"{axis} not scored")
        elif scored[axis][1] != ("PASS" if scored[axis][0] >= t else "FAIL"):
            errors.append(f"{axis} label disagrees with threshold {t}")
    return errors


def version() -> int:
    ev = (HERE / "evaluation-v1.md").read_text(encoding="utf-8")
    ct = (HERE / "contract-v2.md").read_text(encoding="utf-8")
    declared = re.search(r"^\*\*Contract version:\*\*\s*(\d+)", ev, re.M).group(1)
    on_disk = re.search(r"^\*\*Version:\*\*\s*(\d+)", ct, re.M).group(1)
    problems = structure_check(ev, ct)
    print(f"structure check against the contract on disk: {'clean' if not problems else problems}")
    print(f"evaluation declares contract version {declared}; the contract on disk is version {on_disk}")
    print(f"the structure check read only the contract on disk (test_coverage bar there: "
          f"{axes_of(ct)['test_coverage']}/5); a bar moved between versions passes the same way")
    print("declared version compared by the structure check: no")
    return 1 if declared != on_disk and not problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--formats", action="store_true")
    ap.add_argument("--version", action="store_true")
    args = ap.parse_args()
    try:
        if args.formats:
            return formats()
        if args.version:
            return version()
    except OSError as exc:
        print(f"missing fixture: {exc}", file=sys.stderr)
        return 2
    ap.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
