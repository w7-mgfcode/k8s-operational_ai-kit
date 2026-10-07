#!/usr/bin/env python3
"""Render a workstream tracking brief from the sprint state — and audit why the
source's brief was never filled, and what a hand-filled one gets wrong.

    python3 brief.py           render one brief per workstream from state.json
    python3 brief.py A         render workstream A only
    python3 brief.py --audit   orphan check, vocabulary diff, stale-copy diff

Rendering derives every block from state.json, so a rendered brief cannot
disagree with it. The source had no renderer: the brief was a template filled by
hand, if at all.

Exit codes: 0 = rendered. 1 = --audit found findings (the demonstration).
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIRM_TIERS = {"CRITICAL", "HIGH"}


def load_state() -> dict:
    return json.loads((HERE / "state.json").read_text(encoding="utf-8"))


def render(letter: str, state: dict) -> str:
    ws = state["workstreams"][letter]
    tier = state["tiers"][ws["component"]]
    template = (HERE / "brief-template.md").read_text(encoding="utf-8")
    template = re.sub(r"^Status: \[.*\]$", "Status: {status}", template, flags=re.M)
    return template.format(
        letter=letter, name=ws["name"], band=ws["band"], status=ws["status"],
        objective=ws["objective"], component=ws["component"], tier=tier["tier"],
        count=len(tier["dependents"]), dependents=", ".join(tier["dependents"]) or "none",
        confirm="yes" if tier["tier"] in CONFIRM_TIERS else "no", rollback=ws["rollback"],
    )


def field(text: str, label: str) -> str | None:
    m = re.search(rf"^(?:- )?{label}: (.*)$", text, re.M)
    return m.group(1).strip() if m else None


def audit(state: dict) -> int:
    findings: list[str] = []

    print("1. which phase loads each listed template")
    skill = (HERE / "skill-mini.md").read_text(encoding="utf-8")
    phases, table = skill.split("## Templates", 1)
    for path in re.findall(r"^\| `([^`]+)` \|", table, re.M):
        loaded = re.findall(rf"^## (Phase [^\n]+)(?:(?!^## ).)*?{re.escape(path)}", phases, re.M | re.S)
        print(f"   {path:28} {', '.join(p.split(':')[0] for p in loaded) or 'NO PHASE'}")
        if not loaded:
            findings.append(f"{path} is listed as a template and loaded by no phase")

    print("\n2. status vocabulary: brief template against the state file")
    template = (HERE / "brief-template.md").read_text(encoding="utf-8")
    brief_vocab = set(re.search(r"^Status: \[(.*)\]$", template, re.M).group(1).replace(" ", "").split("|"))
    state_vocab = set(state["statuses"])
    for word in sorted(brief_vocab - state_vocab):
        print(f"   '{word}' — the brief can say it, the state file cannot hold it")
        findings.append(f"status '{word}' exists only in the brief template")
    for word in sorted(state_vocab - brief_vocab):
        findings.append(f"status '{word}' exists only in the state file")

    print("\n3. a hand-filled brief against what the state says now")
    filled = (HERE / "filled-brief.md").read_text(encoding="utf-8")
    letter = re.search(r"^# Workstream (\w):", filled, re.M).group(1)
    derived = render(letter, state)
    for label in ("Status", "Tier", "Dependents", "Confirmation required"):
        was, now = field(filled, label), field(derived, label)
        if was != now:
            print(f"   {label:22} hand-filled '{was}'   derived '{now}'")
            findings.append(f"workstream {letter}: {label} is stale in the hand-filled brief")
    if filled.split("## Rollback plan", 1)[1].strip() != state["workstreams"][letter]["rollback"]:
        print("   Rollback plan          the hand-filled steps differ from the state's")
        findings.append(f"workstream {letter}: rollback differs from the state's")

    print(f"\n{len(findings)} findings")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workstream", nargs="?", help="one letter, A to E (default: all)")
    ap.add_argument("--audit", action="store_true", help="orphan, vocabulary and stale-copy checks")
    a = ap.parse_args()
    state = load_state()
    if a.audit:
        return audit(state)
    letters = [a.workstream.upper()] if a.workstream else sorted(state["workstreams"])
    for letter in letters:
        if letter not in state["workstreams"]:
            ap.error(f"unknown workstream {letter}")
        print(render(letter, state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
