#!/usr/bin/env python3
"""A harness's reading of a planning subagent file.

    python3 inspect_definition.py              the definition as written
    python3 inspect_definition.py --narrowed   the same file with a tools: key added

A harness applies the frontmatter key the repository's subagents rule names,
tools:. It does not read prose. This script reports three things: what the file
lists against what a harness grants, which listed tool can create the file the
role is told to produce, and whether the body forbids something its own output
shape requires.

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
            keys[current] = [] if k.group(2) in ("", ">") else k.group(2)
            if isinstance(keys[current], list) and k.group(2) == ">":
                keys[current] = ""
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
    print("granted through the documented spawn path (a general-purpose agent type): "
          + ", ".join(caps["harness_tools"]) + "   (this file is not consulted)")
    extra = sorted(set(granted) - set(listed))
    if extra:
        mismatches += 1
        print(f"  granted beyond the list: {', '.join(extra)}")
    print("  the spawn path ignores the file either way")
    mismatches += 1

    print("\nthe file this role is told to produce")
    produced = re.search(r"[Pp]roduce (\S+\.md)", section(text, "Job"))
    name = produced.group(1) if produced else "(none named)"
    can_write = [t for t in listed if t in caps["writes_files"]]
    print(f"  named output: {name}")
    print(f"  listed tools that can create it: {', '.join(can_write) or 'none'}")
    if "Write" not in listed:
        mismatches += 1
        print("  no write tool is listed; the only way to create the file is the shell,")
        print("  in a role whose body never lets it touch code")

    print("\nforbidden in the body, required by the output shape")
    never = section(text, "Never").lower()
    output = section(text, "Output").lower()
    overlap = False
    for concept, phrases in caps["concepts"].items():
        hit_never = [p for p in phrases if p in never]
        hit_out = [p for p in phrases if p in output]
        if hit_never and hit_out:
            overlap = True
            mismatches += 1
            print(f"  {concept}: forbidden by '{hit_never[0]}', required by '{hit_out[0]}'")
    if not overlap:
        print("  none")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
