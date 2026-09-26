#!/usr/bin/env python3
"""Report what each loading level costs, and find unreferenced resources.

Usage:  python3 levels.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BODY_LIMIT_WORDS = 5000
DESC_LIMIT_CHARS = 1024


def split(skill: Path) -> tuple[str, str]:
    text = skill.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return fm, body
    return "", text


def report(d: Path) -> int:
    skill = d / "SKILL.md"
    fm, body = split(skill)
    desc = fm.split("description:", 1)[1] if "description:" in fm else ""
    res = [p for p in d.rglob("*") if p.is_file() and p.name != "SKILL.md"]

    print(f"\n=== {d.name}")
    print(f"L1 metadata   {len(desc.strip()):>6} chars   ALWAYS RESIDENT")
    print(f"L2 body       {len(body.split()):>6} words   loads on trigger")
    print(f"L3 resources  {len(res):>6} files   loads on demand (scripts: executed)")

    issues = 0
    if len(desc.strip()) > DESC_LIMIT_CHARS:
        print(f"   ERROR L1 over {DESC_LIMIT_CHARS} chars"); issues += 1
    if "Triggers on" not in desc and "Do NOT" not in desc:
        print( "   ERROR L1 has no trigger or exclusion list — see card 03"); issues += 1
    if len(body.split()) > BODY_LIMIT_WORDS:
        print(f"   ERROR L2 over {BODY_LIMIT_WORDS} words"); issues += 1
    for p in res:
        rel = p.relative_to(d).as_posix()
        if p.suffix == ".py" or p.suffix == ".md":
            if rel not in body and p.name not in body:
                print(f"   WARN  L3 {rel} is never referenced by the body — dead weight")
                issues += 1
    if not res:
        print( "   WARN  no L3 at all: everything is in the body")
        issues += 1
    return issues


bad = report(ROOT / "good") + report(ROOT / "bloated")
print(f"\n{bad} issue(s)")
print("\nBoth skills do the same job. The bloated one pays its full cost on")
print("every trigger and states its taxonomy where a reference belongs.")
sys.exit(0)
