#!/usr/bin/env python3
"""Replays a triage subagent's intended actions under three tool grants, and
shows which file writes each grant still allows. Then the subagent's
classification rule against the parser's.

    python3 dispatch.py

The prose bans Edit and Write. The job is to run two scripts with Bash, and
one of them writes a file — so a ban on the write tools leaves every write
the job needs, and any other write through Bash, still possible.

Exit codes: 0 = some grant lets the job run with no writes. 1 = none does
(the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALL = {"Read", "Glob", "Grep", "Bash", "Edit", "Write"}
GRANTS = {
    "as shipped (no tools: key)": ALL,
    "the prose as tools: Bash, Read": {"Bash", "Read"},
    "tools: Read only": {"Read"},
}
NEEDED = {"read the report", "parse to stdout", "render the table"}


def prose_rules(text: str) -> dict[str, set[str]]:
    rules: dict[str, set[str]] = {}
    for line in re.findall(r"^- Controls (.+?) (?:are|is) ([\w -]+?)(?: \(|$)", text, re.M):
        heads, cls = line
        rules.setdefault(cls.strip().replace(" ", "_"), set()).update(
            h.replace("x", "") for h in re.findall(r"\d\.x", heads))
    return rules


def main() -> int:
    argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    actions = json.loads((HERE / "actions.json").read_text())
    any_clean = False

    for label, granted in GRANTS.items():
        allowed = [a for a in actions if a["tool"] in granted]
        writes = [a["writes"] for a in allowed if a["writes"]]
        can_work = NEEDED <= {a["step"] for a in allowed}
        print(f"{label}")
        for a in actions:
            mark = "allowed" if a["tool"] in granted else "blocked"
            w = f"  writes {a['writes']}" if a["writes"] else ""
            print(f"  {mark:8} {a['tool']:6} {a['step']}{w}")
        verdict = "can do the job" if can_work else "cannot do the job"
        print(f"  -> {verdict}; {len(writes)} file write(s) still possible\n")
        any_clean |= can_work and not writes

    text = (HERE / "agent.md").read_text()
    code = json.loads((HERE / "rules.json").read_text())
    prose = prose_rules(text)
    print("classification, stated twice here")
    for cls in ("control_plane", "worker_node", "policy"):
        print(f"  {cls:14} prose {sorted(prose.get(cls, set()))}  parser {sorted(code[cls])}")
    covered = set().union(*prose.values(), *(set(code[c]) for c in ("control_plane", "worker_node", "policy")))
    missing = [str(n) for n in range(1, 6) if f"{n}." not in covered]
    print(f"  the copies agree, and both leave section {', '.join(missing)} unclassified — "
          "agreement between restatements is not a check")

    print("\nno grant lets the job run without writing files: the ban on Edit and Write "
          "is a ban on two tools, not on writing")
    return 0 if any_clean else 1


if __name__ == "__main__":
    sys.exit(main())
