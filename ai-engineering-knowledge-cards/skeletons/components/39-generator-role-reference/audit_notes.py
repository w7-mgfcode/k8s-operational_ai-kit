#!/usr/bin/env python3
"""Audit an implementer's hand-off notes against the rules a role reference gives it.

    python3 audit_notes.py            # the notes' rules, and file scope three ways; exits 1
    python3 audit_notes.py --wording  # four statements of one rule, side by side; exits 1

Exit 2: a fixture is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = ["Changes Made", "Assumptions", "Known Gaps", "Files Modified"]
BANNED = [
    ("quality statement", re.compile(r"\b(is|are) (good|correct|complete|clean|well[- ]structured)\b", re.I)),
    ("comparison", re.compile(r"\bbetter than\b", re.I)),
    ("pre-emptive defence", re.compile(r"\bthe evaluator (might|may|will)\b", re.I)),
    ("disclaimer", re.compile(r"\b(could|would|can) be (improved|better)\b|\bcould be improved\b", re.I)),
]


def sections(text: str) -> dict:
    out, name = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            name = m.group(1)
            out[name] = []
        elif name is not None:
            out[name].append(line)
    return out


def bullets(lines: list) -> list:
    return [re.sub(r"^-\s*", "", l).split(" - ")[0].split(":")[0].strip() for l in lines if l.startswith("- ")]


def audit() -> int:
    notes = (HERE / "implementation-notes.md").read_text(encoding="utf-8")
    spec = (HERE / "sprint-spec.md").read_text(encoding="utf-8")
    actual = {l.strip() for l in (HERE / "changed-files.txt").read_text(encoding="utf-8").splitlines() if l.strip()}
    secs = sections(notes)
    findings = 0

    absent = [s for s in REQUIRED if s not in secs]
    print(f"required sections absent: {absent or 'none'}")
    findings += bool(absent)

    print("banned wording, by line and section:")
    hits = 0
    for n, line in enumerate(notes.splitlines(), 1):
        for label, rx in BANNED:
            if rx.search(line):
                where = next((s for s, body in secs.items() if line in body), "?")
                print(f"  line {n} in '{where}': {label}")
                hits += 1
    print(f"  {hits} hit(s); the 'Known Gaps' section holds both an unfinished item and a note "
          "on what could be better, and only the wording tells them apart")
    findings += bool(hits)

    in_spec = set(re.findall(r"^\s+-\s+(\S+\.\w+)\s*$", spec, re.M))
    reported = set(bullets(secs.get("Files Modified", [])))
    print("file scope, three lists:")
    print(f"  spec lists {len(in_spec)}; notes report {len(reported)}; the tree shows {len(actual)} changed")
    print(f"  reported but not in spec: {sorted(reported - in_spec) or 'none'}")
    print(f"  changed but not in spec:  {sorted(actual - in_spec) or 'none'}")
    print(f"  changed but not reported: {sorted(actual - reported) or 'none'}")
    print("  compared by anything in the loop: no; the notes are the only record, and the "
          "implementer wrote them")
    findings += bool((actual - in_spec) or (actual - reported))
    return 1 if findings else 0


def wording() -> int:
    cfg = json.loads((HERE / "wordings.json").read_text(encoding="utf-8"))
    print(cfg["question"])
    print(f"{'where':26} {'may read':10} {'may steer by it':16} may self-score")
    for w in cfg["wordings"]:
        print(f"{w['where']:26} {w['may_read']:10} {w['may_steer_by_it']:16} {w['may_self_score']}")
    steer = {w["may_steer_by_it"] for w in cfg["wordings"]}
    print(f"\n{len(steer)} different answers on whether the implementer may build toward the criteria.")
    return 1 if len(steer) > 1 else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wording", action="store_true")
    args = ap.parse_args()
    try:
        return wording() if args.wording else audit()
    except OSError as exc:
        print(f"missing fixture: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
