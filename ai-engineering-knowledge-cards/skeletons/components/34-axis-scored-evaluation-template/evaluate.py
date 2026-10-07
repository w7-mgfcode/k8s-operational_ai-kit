#!/usr/bin/env python3
"""Fill an evaluation template three ways and run a structure check over each.

    python3 evaluate.py            # the evaluation filled with the contract's own axis names; exits 0
    python3 evaluate.py --check    # three variants through the check; exits 1

Standard library only, offline. The model that fills the template is replaced by
fill(), which is string assembly over scores.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "scores.json").read_text(encoding="utf-8"))
CONTRACT = {m[0].strip().lower(): int(m[1]) for m in
            re.findall(r"^\|\s*(\w+)\s*\|\s*(\d)/5", (HERE / "contract.md").read_text(encoding="utf-8"), re.M)}


def fill(naming: str, hollow: bool = False) -> str:
    out = [f"# Evaluation: Sprint {DATA['sprint']} - Iteration {DATA['iteration']}", "",
           "## Summary", "", "Two axes fail.", "", "## Axis Scores", ""]
    kept = []
    for ax in DATA["axes"]:
        name = ax["id"] if naming == "ids" else ax["title"]
        verdict = "PASS" if ax["score"] >= CONTRACT[ax["id"]] else "FAIL"
        evidence = "[specific files and lines]" if hollow else ax["evidence"]
        listed = not hollow or ax["id"] == "error_handling"  # the hollow variant drops one summary line
        blockers = ax["blockers"]
        out += [f"### {name} - Score: {ax['score']}/5 - {verdict}", "", f"**Evidence:** {evidence}", "",
                f"**Blocking issues:** {'; '.join(blockers) or 'None'}", ""]
        if blockers and listed:
            kept.append((blockers[0], ax["id"]))
    out += ["## Blocking Issues Summary", ""]
    out += [f"{i}. {text} - Axis: {axis}" for i, (text, axis) in enumerate(kept, 1)]
    return "\n".join(out) + "\n"


def structure_errors(text: str) -> list:
    """What a structure check of this shape can see: axes scored, labels consistent, one blocker."""
    scored = {m[0].strip().lower(): (int(m[1]), m[2]) for m in
              re.findall(r"^### (.+?) - Score: (\d)/5 - (PASS|FAIL)", text, re.M)}
    errors = [f"missing score for contract axis: {a}" for a in CONTRACT if a not in scored]
    for axis, (score, label) in scored.items():
        if axis in CONTRACT and label != ("PASS" if score >= CONTRACT[axis] else "FAIL"):
            errors.append(f"label for {axis} disagrees with its threshold")
    summary = text.split("## Blocking Issues Summary", 1)[1]
    if any(l == "FAIL" for _, l in scored.values()) and not re.search(r"^\d+\. ", summary, re.M):
        errors.append("axes fail but no blocking issue is listed")
    return errors


def unseen_defects(text: str) -> list:
    """What the check above never reads."""
    found = [f"unfilled slot: {s}" for s in re.findall(r"\[[^\]\n]{4,}\]", text)]
    summary = text.split("## Blocking Issues Summary", 1)[1]
    for m in re.finditer(r"^### (.+?) - Score: \d/5 - FAIL\n\n(?:\*\*Evidence:.*\n\n)?\*\*Blocking issues:\*\* (.+)$", text, re.M):
        if m.group(2) != "None" and m.group(2).split(" - ")[0] not in summary:
            found.append(f"blocker listed under {m.group(1)} is absent from the summary")
    return found


def check() -> int:
    bad = 0
    for label, text in [("template naming (Title Case)", fill("title")),
                        ("contract identifiers", fill("ids")),
                        ("identifiers, evidence left blank, one blocker dropped", fill("ids", hollow=True))]:
        errs, unseen = structure_errors(text), unseen_defects(text)
        print(f"{label}: {'INVALID' if errs else 'valid'}")
        for e in errs:
            print("   check:", e)
        for u in unseen:
            print("   passed the check anyway:", u)
        bad += len(errs) + len(unseen)
    print(f"{bad} findings (exit 1 marks them, not an error)")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        sys.exit(check())
    if sys.argv[1:]:
        print("usage: evaluate.py [--check]", file=sys.stderr)
        sys.exit(2)
    print(fill("ids"))
