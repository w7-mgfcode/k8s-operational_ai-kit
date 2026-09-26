#!/usr/bin/env python3
"""Create a capability from a validated name. Nothing is authored freehand.

Usage:  python3 scaffold.py <name> [--out DIR]
"""
from __future__ import annotations
import argparse, re, sys, textwrap
from pathlib import Path

RESERVED = ("anthropic", "claude")


def name_errors(name: str) -> list[str]:
    e = []
    if len(name) > 64: e.append(f"over 64 chars ({len(name)})")
    if name != name.lower(): e.append("must be lowercase")
    if not re.match(r"^[a-z][a-z0-9-]*$", name): e.append("letters, digits and hyphens only, starting with a letter")
    if "--" in name: e.append("no consecutive hyphens")
    if name.endswith("-"): e.append("no trailing hyphen")
    for r in RESERVED:
        if r in name: e.append(f"reserved word: {r}")
    return e


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    # Reject before creating anything — a bad name is cheapest to catch here.
    errs = name_errors(a.name)
    if errs:
        for e in errs:
            print(f"ERROR  name: {e}", file=sys.stderr)
        sys.exit(1)

    d = Path(a.out) / a.name
    if d.exists():
        print(f"ERROR  {d} already exists", file=sys.stderr); sys.exit(1)

    # The empty directories are instructional: they tell the author where each
    # loading level lives. See card 02.
    for sub in ("scripts", "references", "assets"):
        (d / sub).mkdir(parents=True, exist_ok=True)

    (d / "SKILL.md").write_text(textwrap.dedent(f"""\
        ---
        name: {a.name}
        description: >
          TODO: what this does, what it produces, the phrases that should
          trigger it, and what it must NOT be used for. Under 1024 chars.
          See card 03 — this field is the routing table.
        ---

        # {a.name.replace("-", " ").title()}

        ## Overview

        TODO

        ## Workflow

        1. TODO
        """), encoding="utf-8")
    print(f"scaffolded {d}/")
    print("  SKILL.md  scripts/  references/  assets/")


if __name__ == "__main__":
    main()
