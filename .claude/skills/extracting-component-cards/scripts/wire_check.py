#!/usr/bin/env python3
"""Check the wiring check.py does not: INDEX rows and the restated card count.

    python3 wire_check.py [--repo <repo-root>]

For every component card on disk: INDEX.md links it. The component-card count
restated in AGENTS.md, docs/_base/ARCHITECTURE.md and
.claude/agents/codebase-analyst.md matches the number of cards. related: edges
are not checked here — check.py already fails a dangling or one-way edge.

Exit codes: 0 = wired, 1 = something is missing or stale, 2 = usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen", "twenty"]
# file, regex capturing the stated count, as it is phrased in that file
COUNTS = [
    ("AGENTS.md", r"(\w+) \*\*component cards\*\*"),
    ("docs/_base/ARCHITECTURE.md", r"the (\w+) component cards"),
    (".claude/agents/codebase-analyst.md", r"(\d+) artifacts, 11 sections"),
]


def as_int(word: str) -> int | None:
    if word.isdigit():
        return int(word)
    return WORDS.index(word.lower()) if word.lower() in WORDS else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    project = repo / "ai-engineering-knowledge-cards"
    if not (project / "INDEX.md").is_file():
        ap.error(f"{repo} is not this repository's root")

    cards = sorted(p for p in (project / "component-cards").rglob("*.md")
                   if re.search(r"^component:\s*\d+", p.read_text(encoding="utf-8"), re.M))
    problems = []
    index = (project / "INDEX.md").read_text(encoding="utf-8")
    for card in cards:
        link = card.relative_to(project).as_posix()
        if f"]({link})" not in index:
            problems.append(f"INDEX.md: no row linking {link}")

    for rel, rx in COUNTS:
        text = (repo / rel).read_text(encoding="utf-8")
        m = re.search(rx, text)
        stated = as_int(m.group(1)) if m else None
        if stated != len(cards):
            shown = m.group(1) if m else "no count found"
            problems.append(f"{rel}: states {shown}, there are {len(cards)} component cards")

    for p in problems:
        print(p)
    print(f"{len(cards)} component cards, {len(problems)} wiring problems", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
