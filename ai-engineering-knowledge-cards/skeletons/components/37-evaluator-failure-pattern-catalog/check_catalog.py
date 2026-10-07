#!/usr/bin/env python3
"""Run a failure-pattern catalog's own self-check against an evaluation.

The catalog tells the evaluator to run eight checks on its own output before
submitting. Each is mechanical. Here they run as code over a fabricated
evaluation, next to what a structure-only validator would have caught.

    python3 check_catalog.py                       # the eight checks; exits 1
    python3 check_catalog.py --structure-only      # what a structure validator sees; exits 1
    python3 check_catalog.py --calibration         # a model answer against its own bands; exits 1

Exit 2: a file is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRAISE = re.compile(r"\b(great|good|nice|solid|clean|reads well|sound|well-organi[sz]ed)\b", re.I)
FLAW = re.compile(r"\b(fail|missing|without|not|no|untested|drops?|dropped|swallow)\w*\b", re.I)
VAGUE = re.compile(r"\b(overall|generally|mostly)\b", re.I)
HEDGE = re.compile(r"\b(might|could|perhaps|maybe)\b", re.I)
COMPARE = re.compile(r"\b(better than|improved since|than the previous|compared to the last)\b", re.I)
CITE = re.compile(r"[\w/.-]+\.\w+:\d+")


def sections(text: str) -> dict:
    """Axis name -> body, for `### name - Score: N/5 - PASS|FAIL` headings."""
    out = {}
    for m in re.finditer(r"^###\s+(\S+)\s+-\s+Score:\s*(\d)/5\s+-\s+(PASS|FAIL)\s*$(.*?)(?=^#{2,3}\s|\Z)",
                         text, re.M | re.S):
        out[m.group(1)] = {"score": int(m.group(2)), "status": m.group(3), "body": m.group(4)}
    return out


def blockers(text: str) -> list:
    block = re.search(r"^##\s+Blocking Issues.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return [l for l in (block.group(1).splitlines() if block else []) if re.match(r"^\d+\.\s", l)]


def contract_axes(text: str) -> set:
    return {m.group(1) for m in re.finditer(r"^\|\s*([a-z_]+)\s*\|\s*\d/5", text, re.M)}


def run_checks(ev: str, contract: str) -> list:
    """Eight checks, in the catalog's order: (id, name, tripped, detail)."""
    secs, bl = sections(ev), blockers(ev)
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", ev))
    praise_n = sum(1 for s in sentences if PRAISE.search(s))
    flaw_n = sum(1 for s in sentences if FLAW.search(s))
    scoring = "\n".join(s["body"] for s in secs.values()) + ev.split("## Axis Scores")[0]
    blocker_text = " ".join(bl)
    uncited = [a for a, s in secs.items() if not CITE.search(s["body"])]
    unblocked = [a for a, s in secs.items() if s["status"] == "FAIL" and not any(a in b for b in bl)]
    after = [a for a, s in secs.items() if PRAISE.search(s["body"]) and s["status"] == "FAIL"]
    gap = sorted(contract_axes(contract) ^ set(secs))
    return [
        (1, "praise sentences outnumber flaw sentences", praise_n > flaw_n, f"{praise_n} vs {flaw_n}"),
        (2, "'overall', 'generally', 'mostly' in scoring text", bool(VAGUE.search(scoring)),
         sorted({m.group(0).lower() for m in VAGUE.finditer(scoring)})),
        (3, "hedging near blocking issues", bool(HEDGE.search(blocker_text)),
         sorted({m.group(0).lower() for m in HEDGE.finditer(blocker_text)})),
        (4, "an axis section with no file:line citation", bool(uncited), uncited),
        (5, "a FAIL axis no blocking issue names", bool(unblocked), unblocked),
        (6, "'better than before' language", bool(COMPARE.search(ev)),
         [m.group(0).lower() for m in COMPARE.finditer(ev)]),
        (7, "axes scored differ from contract axes", bool(gap), gap),
        (8, "praise inside a FAIL axis section", bool(after), after),
    ]


def structure_only(ev: str, contract: str) -> list:
    """What a structure validator sees: axes scored; a FAIL axis with *any* blocker."""
    secs, bl = sections(ev), blockers(ev)
    gap = sorted(contract_axes(contract) ^ set(secs))
    any_fail = any(s["status"] == "FAIL" for s in secs.values())
    return [
        (4, "an axis section with no file:line citation", False, "not checked"),
        (5, "a FAIL axis no blocking issue names", any_fail and not bl,
         "checks only that some blocking issue exists"),
        (7, "axes scored differ from contract axes", bool(gap), gap),
    ]


def band_for(bands: list, share: float):
    for b in bands:
        if b["min"] <= share <= b["max"]:
            return b["score"]
    return None


def calibration() -> int:
    cfg = json.loads((HERE / "bands.json").read_text(encoding="utf-8"))
    m = cfg["model_answer"]
    share = m["tested"] / m["specified"]
    print(f"model answer: {m['tested']} of {m['specified']} scenarios tested -> score {m['score_given']}")
    print(f"the bands:    {share:.1%} falls in the band for score {band_for(cfg['bands'], share)}")
    holes = [x for x in range(0, 101, 5) if band_for(cfg["bands"], x / 100) is None]
    runs, start = [], None
    for x in range(0, 101, 5):
        if x in holes and start is None:
            start = x
        if x not in holes and start is not None:
            runs.append((start, x - 5))
            start = None
    if start is not None:
        runs.append((start, 100))
    spans = ", ".join(f"{a}%-{b}%" for a, b in runs)
    print(f"shares with no band (steps of 5%): {spans} - {len(holes)} of 21 points")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--structure-only", action="store_true")
    ap.add_argument("--calibration", action="store_true")
    args = ap.parse_args()
    try:
        if args.calibration:
            return calibration()
        ev = (HERE / "evaluation-sloppy.md").read_text(encoding="utf-8")
        contract = (HERE / "contract.md").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"missing fixture: {exc}", file=sys.stderr)
        return 2
    rows = structure_only(ev, contract) if args.structure_only else run_checks(ev, contract)
    for n, name, tripped, detail in rows:
        print(f"{n}. {'TRIPPED' if tripped else 'clear  '} {name}  ->  {detail}")
    tripped_n = sum(1 for r in rows if r[2])
    total = 3 if args.structure_only else 8
    print(f"{tripped_n} of {total} checks tripped" + ("" if not args.structure_only else " (the other five are not in a structure check)"))
    return 1 if tripped_n else 0


if __name__ == "__main__":
    sys.exit(main())
