#!/usr/bin/env python3
"""A harness's reading of a subagent file — which tools it grants, against
which tools the file's own prose forbids. Then the file's skip list against the
two other lists that say the same thing.

    python3 dispatch.py                  the definition as written
    python3 dispatch.py --narrowed       the same file with a tools: line added

A harness applies frontmatter. It does not read prose. Without a tools: key it
grants the agent every tool it has, and the body's "Do NOT use" line is an
instruction the model is trusted with ([card 16]).

Exit codes: 0 = nothing granted that the prose forbids, and the lists agree.
1 = a mismatch (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    keys = {}
    for line in (m.group(1).splitlines() if m else []):
        k = re.match(r"(\w+):\s*(.*)", line)
        if k:
            keys[k.group(1)] = k.group(2)
    return keys


def prose_list(text: str, label: str) -> set[str]:
    m = re.search(rf"^{label}:\s*(.+)$", text, re.M)
    return {t.strip() for t in m.group(1).split(",")} if m else set()


def skip_list(text: str) -> set[str]:
    m = re.search(r"^## Skip\n(.*?)(?=^## )", text, re.M | re.S)
    return set(re.findall(r"^- (\S+)", m.group(1), re.M)) if m else set()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--narrowed", action="store_true",
                    help="simulate the fix: a tools: key listing what the prose allows")
    a = ap.parse_args()

    text = (HERE / "agent.md").read_text()
    lists = json.loads((HERE / "lists.json").read_text())
    keys = frontmatter(text)
    if a.narrowed:
        keys["tools"] = ", ".join(sorted(prose_list(text, "Use")))
    mismatches = 0

    granted = ({t.strip() for t in keys["tools"].split(",")} if "tools" in keys
               else set(lists["harness_tools"]))
    banned = prose_list(text, "Do NOT use")
    print(f"frontmatter keys: {', '.join(keys)}")
    print(f"granted by the harness: {', '.join(sorted(granted))}"
          + ("" if "tools" in keys else "   (no tools: key — everything)"))
    print(f"forbidden by the prose: {', '.join(sorted(banned))}")
    both = granted & banned
    if both:
        mismatches += 1
        print(f"  granted and forbidden: {', '.join(sorted(both))} — only the model's compliance stands between")
    else:
        print("  nothing granted that the prose forbids")

    print("\nroles skipped as needing elevated access, in three places")
    copies = {"this agent's prose": skip_list(text),
              "the field scanner": set(lists["scanner_exceptions"]),
              "the remediation guide": set(lists["guide_special_handling"])}
    every = set().union(*copies.values())
    for role in sorted(every):
        marks = "  ".join(("x" if role in s else ".") for s in copies.values())
        print(f"  {role:18} {marks}")
    print(f"  {'':18} {'  '.join(str(i) for i in range(1, len(copies) + 1))}   "
          + "; ".join(f"{i} = {n}" for i, n in enumerate(copies, 1)))
    if len({frozenset(s) for s in copies.values()}) > 1:
        mismatches += 1
        print("  the three lists disagree; nothing compares them")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
