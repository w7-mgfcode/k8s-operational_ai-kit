#!/usr/bin/env python3
"""A fresh sketch of a sprint contract writer, and an audit of it.

    python3 contract_writer.py --sprint s1 --axes '["correctness","error_handling","test_coverage"]' \\
        --thresholds '{"correctness":4,"error_handling":3,"test_coverage":3}' --output out/contract.md
    python3 contract_writer.py --audit

Standard library only. The audit writes to a temporary directory and removes it.
Exit codes: 0 ran, 1 invalid inputs / the audit demonstrated failures on purpose,
2 requires arguments or JSON that does not parse.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


class _Swap:
    """Point a sys stream at a buffer for the length of a with-block."""

    def __init__(self, name, buf):
        self.name, self.buf = name, buf

    def __enter__(self):
        self.saved = getattr(sys, self.name)
        setattr(sys, self.name, self.buf)

    def __exit__(self, *exc):
        setattr(sys, self.name, self.saved)
        return False


def redirect_stdout(buf):
    return _Swap("stdout", buf)


def redirect_stderr(buf):
    return _Swap("stderr", buf)

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"


def validate_inputs(axes: list, thresholds: dict) -> list:
    problems = []
    if len(axes) > 7:
        problems.append(f"too many axes: {len(axes)} (limit 7)")
    if len(axes) < 3:                                    # advice elsewhere, a hard error here
        problems.append(f"too few axes: {len(axes)} (3 are advised)")
    problems += [f"no threshold given for {name}" for name in axes if name not in thresholds]
    for name, value in thresholds.items():
        if name not in axes:
            problems.append(f"{name} has a threshold but is not an axis")
        if not isinstance(value, int) or value < 1 or value > 5:
            problems.append(f"{name}: threshold {value!r} is not an integer from 1 to 5")
    return problems                                      # nothing rejects a repeated axis


def render(sprint: str, axes: list, thresholds: dict, out_of_scope: str, version: int) -> str:
    lines = [f"# Sprint Contract: {sprint}", "",
             f"**Version:** {version}",
             f"**Created:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             "**Status:** active", "",
             "## Evaluation Axes", "",
             "| Axis | Threshold | Weight |", "|------|-----------|--------|"]
    for axis in axes:
        weight = "high" if thresholds[axis] >= 4 else "standard"     # computed, not an input
        lines.append(f"| {axis} | {thresholds[axis]}/5 | {weight} |")
    lines += ["", "## Scoring Rules", "",
              "- Scale: integer 1-5 per axis",
              "- Pass: score at or above threshold on every axis", "",
              "## Out of Scope", ""]
    items = [i.strip() for i in out_of_scope.split(",") if i.strip()]    # split on every comma
    lines += [f"- {i}" for i in items] or ["- None specified"]
    lines += ["", "## Contract Rules", "",
              "1. The bar is fixed when building starts.",
              "2. Any change is a new version, signed off by the owner."]
    return "\n".join(lines) + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)                                    # replaces whatever is there


def run(sprint, axes_json, thresholds_json, out_of_scope, output: Path, version: int) -> int:
    try:
        axes, thresholds = json.loads(axes_json), json.loads(thresholds_json)
    except ValueError as exc:
        print(json.dumps({"error": f"invalid JSON: {exc}"}))
        return 2
    errors = validate_inputs(axes, thresholds)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}))
        return 1
    write(output, render(sprint, axes, thresholds, out_of_scope, version))
    print(json.dumps({"valid": True, "sprint": sprint, "axes": axes, "output": str(output), "version": version}))
    return 0


def quiet(fn, *args):
    import io
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*args)
    return code, buf.getvalue()


def validator_can_see(axis: str) -> bool:
    """The row pattern a reader of the contract uses: word characters and spaces only."""
    return re.fullmatch(r"\w[\w ]*", axis) is not None


def audit() -> int:
    work = Path(tempfile.mkdtemp(prefix="contract-demo-"))
    findings: list = []

    def finding(text: str) -> None:
        findings.append(text)
        print(f"FINDING {len(findings)}: {text}")

    names = ["correctness", "error_handling", "test_coverage"]
    try:
        out = work / "s1" / "contract.md"
        quiet(run, "s1", json.dumps(names), json.dumps(dict(zip(names, [4, 3, 3]))), "", out, 1)
        first = out.read_text(encoding="utf-8")
        code, _ = quiet(run, "s1", json.dumps(names), json.dumps(dict(zip(names, [1, 1, 1]))), "", out, 1)
        second = out.read_text(encoding="utf-8")
        siblings = sorted(p.name for p in out.parent.iterdir())
        if code == 0 and first != second and "**Version:** 1" in second and siblings == ["contract.md"]:
            finding("the contract was rewritten with every threshold at 1/5, still version 1, "
                    f"and the directory holds only {siblings}: no copy, no superseded state")

        code, text = quiet(run, "s2", '["correctness","error_handling"]', '{"correctness":4,"error_handling":3}', "", work / "s2.md", 1)
        if code == 1 and "recommended" in text:
            finding("two axes exit 1 with a message that says 'recommended'")

        outline = (FIXTURES / "template_outline.txt").read_text(encoding="utf-8")
        wanted = [s.strip() for s in outline.splitlines()[0].split(":", 1)[1].split("|")]
        have = re.findall(r"^## (.+)$", second, re.M)
        missing = [s for s in wanted if s not in have]
        if missing:
            finding(f"sections in the template outline and not in the file: {missing}; "
                    "the table also has no description column")

        weights = re.findall(r"\| (\w+) \| (\d)/5 \| (\w+) \|", first)
        if all((int(t) >= 4) == (w == "high") for _, t, w in weights):
            finding("weights " + ", ".join(f"{t}/5 = {w}" for _, t, w in weights)
                    + ": a function of the threshold; no flag sets it")

        quiet(run, "s3", json.dumps(names), json.dumps(dict(zip(names, [4, 3, 3]))),
              "date formats (day, month, year order)", work / "s3.md", 1)
        bullets = re.findall(r"^- (.+)$", (work / "s3.md").read_text(encoding="utf-8"), re.M)
        if len([b for b in bullets if "Scale" not in b and "Pass" not in b]) > 1:
            finding("one out-of-scope item with commas became "
                    f"{len([b for b in bullets if 'Scale' not in b and 'Pass' not in b])} bullets")

        dupes = ["correctness", "correctness", "error_handling"]
        code, _ = quiet(run, "s4", json.dumps(dupes), '{"correctness":4,"error_handling":3}', "", work / "s4.md", 1)
        rows = (work / "s4.md").read_text(encoding="utf-8").count("| correctness |") if code == 0 else 0
        if rows == 2:
            finding("an axis listed twice validates and is written as two table rows")

        odd = ["correctness", "error-handling", "test_coverage"]
        code, _ = quiet(run, "s5", json.dumps(odd), '{"correctness":4,"error-handling":3,"test_coverage":3}', "", work / "s5.md", 1)
        if code == 0 and not validator_can_see("error-handling"):
            finding("'error-handling' is written to the contract; the reader's row pattern "
                    "(word characters and spaces) cannot see it")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"{len(findings)} findings")
    return 1 if findings else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="sprint contract writer (sketch)")
    parser.add_argument("--sprint")
    parser.add_argument("--axes")
    parser.add_argument("--thresholds")
    parser.add_argument("--out-of-scope", default="")
    parser.add_argument("--output")
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--audit", action="store_true", help="run the findings audit")
    args = parser.parse_args()
    if args.audit:
        return audit()
    if not (args.sprint and args.axes and args.thresholds and args.output):
        parser.print_usage(sys.stderr)
        return 2
    return run(args.sprint, args.axes, args.thresholds, args.out_of_scope, Path(args.output), args.version)


if __name__ == "__main__":
    sys.exit(main())
