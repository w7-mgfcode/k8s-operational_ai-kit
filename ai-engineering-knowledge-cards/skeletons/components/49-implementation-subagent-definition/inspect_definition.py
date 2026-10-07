#!/usr/bin/env python3
"""A harness's reading of an implementation subagent file.

    python3 inspect_definition.py              the definition as written
    python3 inspect_definition.py --narrowed   the same file with a tools: key added

Three things: what the file lists against what a harness grants, whether a write
grant can honour the file-scope sentence in the body, and whether two sentences
of the body overlap in what they ask for.

Exit codes: 0 = the definition is consistent. 1 = a mismatch (the
demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    keys: dict = {}
    current = None
    for line in (m.group(1).splitlines() if m else []):
        item = re.match(r"\s+- (.+)", line)
        if item and current is not None:
            keys[current].append(item.group(1).strip())
            continue
        k = re.match(r"([\w-]+):\s*(.*)", line)
        if k:
            current = k.group(1)
            keys[current] = "" if k.group(2) == ">" else ([] if k.group(2) == "" else k.group(2))
    return keys


def section(text: str, name: str) -> str:
    m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--narrowed", action="store_true",
                    help="simulate the fix: a tools: key copying the listed tools")
    a = ap.parse_args()

    text = (HERE / "agent.md").read_text()
    caps = json.loads((HERE / "capabilities.json").read_text())
    scope = json.loads((HERE / "scope.json").read_text())
    keys = parse_frontmatter(text)
    listed = list(keys.get("allowed-tools", []))
    if a.narrowed:
        keys["tools"] = list(listed)
    mismatches = 0

    print(f"frontmatter keys: {', '.join(keys)}")
    print(f"listed under allowed-tools: {', '.join(listed)}")
    if "tools" in keys:
        granted = list(keys["tools"])
        print(f"granted by a harness reading tools: {', '.join(granted)}")
    else:
        granted = list(caps["harness_tools"])
        print(f"granted by a harness reading tools: {', '.join(granted)}   (no tools: key — everything)")
    extra = sorted(set(granted) - set(listed))
    if extra:
        mismatches += 1
        print(f"  granted beyond the list: {', '.join(extra)}")
    print("granted through the documented spawn path (a general-purpose agent type): "
          + ", ".join(caps["harness_tools"]) + "   (this file is not consulted)")
    if set(caps["harness_tools"]) - set(listed):
        mismatches += 1
        print("  the spawn path grants what the file never listed")

    print("\nfile scope: the body's sentence against the grant")
    can_write = bool(set(granted) & set(caps["write_tools"]))
    in_scope = set(scope["sprint_files"])
    outside = 0
    for path in scope["attempted_writes"]:
        by_prose = "yes" if path in in_scope else "no"
        by_grant = "yes" if can_write else "no"
        flag = "   <- allowed by the grant, not by the prose" if (by_prose == "no" and by_grant == "yes") else ""
        outside += 1 if flag else 0
        print(f"  {path:22} prose allows: {by_prose:3}  grant allows: {by_grant:3}{flag}")
    if outside:
        mismatches += 1
        print("  a tool grant has no path dimension; the scope is a sentence the model is trusted with")

    print("\ntwo sentences of the body that overlap")
    never = section(text, "Never").lower()
    output = section(text, "Output").lower()
    found = False
    for concept, phrases in caps["concepts"].items():
        hit_never = [p for p in phrases if p in never]
        hit_out = [p for p in phrases if p in output]
        if hit_never and hit_out:
            found = True
            mismatches += 1
            print(f"  {concept}: banned as '{hit_never[0]}', required as '{hit_out[0]}'")
            print("  the body does not say where one stops and the other starts")
    if not found:
        print("  none")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
