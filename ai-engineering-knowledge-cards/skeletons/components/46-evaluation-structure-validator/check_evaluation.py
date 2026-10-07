#!/usr/bin/env python3
"""A fresh sketch of an evaluation structure validator, and an audit of it.

    python3 check_evaluation.py --contract fixtures/contract.md --evaluation fixtures/evaluation_ok.md
    python3 check_evaluation.py --audit

Standard library only. The audit writes to a temporary directory and removes it.
Exit codes: 0 valid / ran, 1 invalid / the audit demonstrated failures on purpose,
2 requires arguments or an unreadable input.
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
FIXTURES = HERE / "fixtures"

AXIS_HEADING = re.compile(r"^###\s+(.+?)\s+[—-]\s+Score:\s*(\d)/5\s+[—-]\s+(PASS|FAIL)\s*$", re.I)


def parse_contract(text: str) -> dict:
    """Axis -> threshold, from table rows shaped `| name | N/5 | ... |`."""
    axes = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        name, threshold = cells[0], cells[1]
        # word characters and spaces only: any other row is skipped without a message
        if re.fullmatch(r"\w[\w ]*", name) and re.fullmatch(r"\d/5", threshold):
            if name.lower() != "axis":
                axes[name.lower()] = int(threshold[0])
    return axes


def parse_evaluation(text: str) -> dict:
    out = {"summary": False, "axes": {}, "issues": []}
    in_issues = False
    for line in text.splitlines():
        if re.match(r"^##\s+Summary", line):
            out["summary"] = True
        m = AXIS_HEADING.match(line)
        if m:
            out["axes"][m.group(1).strip().lower()] = {"score": int(m.group(2)), "label": m.group(3).upper()}
        if re.match(r"^##\s+Blocking Issues", line):
            in_issues = True
            continue
        if in_issues and re.match(r"^##\s", line):
            in_issues = False
        if in_issues:
            item = re.match(r"^\d+\.\s+(.*)$", line)     # numbered items only
            if item:
                # "looks like a file reference": a word, a dot, a word
                out["issues"].append({"text": item.group(1), "file_like": bool(re.search(r"\w\.\w", item.group(1)))})
    return out


def validate(contract: dict, ev: dict) -> dict:
    errors, warnings = [], []
    if not ev["summary"]:
        errors.append("missing summary heading")
    missing = sorted(set(contract) - set(ev["axes"]))
    if missing:
        errors.append("missing scores for contract axes: " + ", ".join(missing))
    extra = sorted(set(ev["axes"]) - set(contract))
    if extra:
        warnings.append("scores for axes not in the contract (ignored): " + ", ".join(extra))
    for name, a in ev["axes"].items():
        if not 1 <= a["score"] <= 5:
            errors.append(f"score for {name} is {a['score']}; must be 1-5")
    for name in sorted(set(contract) & set(ev["axes"])):
        a = ev["axes"][name]
        expected = "PASS" if a["score"] >= contract[name] else "FAIL"
        if a["label"] != expected:
            errors.append(f"{name}: score {a['score']} against threshold {contract[name]} is {expected}, marked {a['label']}")
    failing = [n for n in set(contract) & set(ev["axes"]) if ev["axes"][n]["label"] == "FAIL"]
    if failing and not ev["issues"]:
        errors.append("an axis is marked FAIL and no blocking issue is listed")
    blind = [i for i in ev["issues"] if not i["file_like"]]
    if blind:
        warnings.append(f"{len(blind)} blocking issue(s) lack a file reference")
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "axes_checked": len(contract), "axes_scored": len(ev["axes"]),
            "blocking_issues": len(ev["issues"])}


def check(contract_text: str, evaluation_text: str) -> dict:
    return validate(parse_contract(contract_text), parse_evaluation(evaluation_text))


def report(heads, issues="1. a problem in importer/rows.py:3 — Axis: x", summary=True) -> str:
    body = "# Evaluation\n\n" + ("## Summary\n\nx\n\n" if summary else "") + "## Axis Scores\n\n"
    body += "".join(f"### {h}\n\n**Evidence:** x\n\n" for h in heads)
    return body + "## Blocking Issues Summary\n\n" + issues + "\n"


def audit() -> int:
    work = Path(tempfile.mkdtemp(prefix="validate-demo-"))
    findings: list = []

    def finding(text: str) -> None:
        findings.append(text)
        print(f"FINDING {len(findings)}: {text}")

    try:
        contract = (FIXTURES / "contract.md").read_text(encoding="utf-8")
        ok = ["correctness — Score: 4/5 — PASS", "error_handling — Score: 3/5 — PASS",
              "test_coverage — Score: 3/5 — PASS"]

        r = check(contract, report(["Correctness — Score: 4/5 — PASS", "Error Handling — Score: 3/5 — PASS",
                                    "Test Coverage — Score: 3/5 — PASS"]))
        if not r["valid"]:
            finding("an evaluation that scored every axis, headed in words, is rejected: " + r["errors"][0])

        hyphen = contract + "| error-handling | 3/5 | standard |\n"
        r = check(hyphen, report(ok))
        if r["valid"] and r["axes_checked"] == 3:
            finding("the contract has four rows and the validator checks 3: the hyphenated axis "
                    "was skipped, and an evaluation that never scored it is valid")

        two_fail = ["correctness — Score: 1/5 — FAIL", "error_handling — Score: 1/5 — FAIL",
                    "test_coverage — Score: 3/5 — PASS"]
        r = check(contract, report(two_fail, "1. only about correctness, in importer/rows.py:3"))
        if r["valid"]:
            finding("two axes marked FAIL and one blocking issue: valid; the issue names no axis the check reads")

        r = check(contract, report(two_fail, "1. it is bad, e.g. very bad\n2. also bad, v2.0 is worse"))
        if r["valid"] and not r["warnings"]:
            finding("blocking issues that cite no file pass without a warning: 'e.g.' and 'v2.0' look like files")

        r = check(contract, report(two_fail, "- a bullet issue in importer/rows.py:3\n- another in importer/cli.py:9"))
        if not r["valid"] and r["blocking_issues"] == 0:
            finding("a correct list of issues written as bullets counts as zero issues and fails the report")

        na = ["correctness — Score: 4/5 — PASS", "error_handling — Score: 5/5 — PASS",
              "test_coverage — Score: 3/5 — PASS"]
        r = check(contract, report(na, "None."))
        if r["valid"]:
            finding("an axis declared 'not applicable' and scored 5 passes with no issue and no way to tell")

        praise = (FIXTURES / "evaluation_praise.md").read_text(encoding="utf-8")
        r = check(contract, praise)
        if r["valid"]:
            finding("a report of praise with 'looks fine' as evidence is valid: the checks are about shape")

        lowered = contract.replace("4/5", "1/5").replace("3/5", "1/5")
        weak = report(["correctness — Score: 2/5 — PASS", "error_handling — Score: 1/5 — PASS",
                       "test_coverage — Score: 1/5 — PASS"], "None.")
        (work / "lowered.md").write_text(lowered, encoding="utf-8")
        r = check((work / "lowered.md").read_text(encoding="utf-8"), weak)
        if r["valid"] and not check(contract, weak)["valid"]:
            finding("the same weak report is invalid against the agreed contract and valid against a "
                    "lowered one: the validator reads whichever file it is given")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"{len(findings)} findings")
    return 1 if findings else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="evaluation structure validator (sketch)")
    parser.add_argument("--contract")
    parser.add_argument("--evaluation")
    parser.add_argument("--audit", action="store_true", help="run the findings audit")
    args = parser.parse_args()
    if args.audit:
        return audit()
    if not (args.contract and args.evaluation):
        parser.print_usage(sys.stderr)
        return 2
    try:
        contract = parse_contract(Path(args.contract).read_text(encoding="utf-8"))
        text = Path(args.evaluation).read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}))
        return 2
    if not contract:
        print(json.dumps({"valid": False, "errors": ["no axes found in the contract"]}))
        return 2
    result = validate(contract, parse_evaluation(text))
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
