#!/usr/bin/env python3
"""Check only what is mechanically decidable. Exit non-zero on error.

A validator that renders opinions produces noise, and noise trains people to
stop reading it.

Usage:  python3 validate.py <dir>
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

BODY_LIMIT = 500          # lines
DESC_LIMIT = 1024         # chars


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill_dir")
    a = ap.parse_args()
    d = Path(a.skill_dir)
    errors: list[str] = []
    warnings: list[str] = []

    skill = d / "SKILL.md"
    if not skill.exists():
        print(f"FAIL — no SKILL.md in {d}"); sys.exit(1)

    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("missing opening frontmatter delimiter")
        fm, body = "", text
    else:
        parts = text.split("---", 2)
        if len(parts) < 3:
            errors.append("missing closing frontmatter delimiter")
            fm, body = "", text
        else:
            fm, body = parts[1], parts[2]

    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    if not name:
        errors.append("frontmatter missing required field: name")
    elif name.group(1) != d.name:
        errors.append(f"name '{name.group(1)}' does not match folder '{d.name}'")

    desc = re.search(r"^description:\s*(.*(?:\n\s+.*)*)", fm, re.M)
    if not desc:
        errors.append("frontmatter missing required field: description")
    else:
        dv = " ".join(desc.group(1).split())
        if len(dv) > DESC_LIMIT:
            errors.append(f"description {len(dv)} chars, limit {DESC_LIMIT}")
        if re.match(r"^(I |you |we )", dv, re.I):
            errors.append("description must be third person")
        if "TODO" in dv:
            warnings.append("description still contains TODO")
        if "Do NOT" not in dv and "do not use" not in dv.lower():
            warnings.append("description has no exclusion list — see card 03")

    lines = len(body.strip().splitlines())
    if lines > BODY_LIMIT:
        errors.append(f"body {lines} lines, limit {BODY_LIMIT}")

    if (d / "README.md").exists():
        errors.append("README.md is forbidden inside a capability")

    for p in (d / "references").rglob("*"):
        if p.is_file() and len(p.relative_to(d / "references").parts) > 2:
            errors.append(f"reference nested too deep: {p.relative_to(d)}")

    for e in errors:
        print(f"  [ERROR] {e}")
    for w in warnings:
        print(f"  [WARN]  {w}")
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"PASS — {len(warnings)} warning(s)" if warnings else "PASS — all checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
