#!/usr/bin/env python3
"""A harness's reading of an evaluation subagent file.

    python3 inspect_definition.py              the definition as written
    python3 inspect_definition.py --narrowed   the same file with a tools: key added

Three things: what the file lists against what a harness grants; which of the
role's shell commands write, against a grant that has no path in it; and the
file the role is told to write, against the sentence that says it changes
nothing. The commands are fabricated and are classified, never run.

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
    fixture = json.loads((HERE / "commands.json").read_text())
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
        print("  the spawn path grants the write tools the file left out")

    print("\nthe role's shell commands, classified")
    shell = "Bash" in granted
    patterns = [re.compile(p) for p in caps["shell_writes"]]
    review = fixture["review_file"]
    for cmd in fixture["commands"]:
        writes = any(p.search(cmd) for p in patterns)
        own_output = writes and review in cmd
        if not writes:
            verdict = "reads"
        elif own_output:
            verdict = "writes (its own output)"
        else:
            verdict = "writes (changes the repository)"
            if shell:
                mismatches += 1
        print(f"  {verdict:34} granted: {'yes' if shell else 'no ':3}  {cmd}")
    print("  the grant is the same word for the output and for the damage; the path is the only difference")

    print("\nthe file it must write, against the sentence that it changes nothing")
    job = section(text, "Job")
    never = section(text, "Never")
    wrote = re.search(r"write the\s+result to (\S+\.md)", job.replace("\n", " "))
    print(f"  told to write: {wrote.group(1) if wrote else '(none)'}")
    print(f"  also told: {re.search(r'Change any file[^.\n]*', never).group(0)}")
    if wrote and "Write" not in listed:
        mismatches += 1
        print("  no write tool is listed, so the output goes through the shell")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
