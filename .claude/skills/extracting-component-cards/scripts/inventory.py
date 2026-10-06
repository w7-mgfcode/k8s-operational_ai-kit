#!/usr/bin/env python3
"""Map a skill directory to the component cards it becomes.

    python3 inventory.py <skill-dir> [--repo <repo-root>]

Legacy mode takes a skill under .legacy-assets/; local mode takes a project-authored
skill under .claude/skills/ — one git tracks. Vendored skills are refused.

Prints JSON: the mode (legacy or local), the next free component number, and one
entry per file with its card type and number. Files that are not a SKILL.md or
under references/, assets/ or scripts/ come back as "unmapped": each needs a card
or an explicit exclusion before the plan gate.

It proposes no slug or title. Every name it could derive is the source's own,
and that is a masked class — the generic names are chosen at the gate.

Exit codes: 0 = inventoried, 2 = usage error or not a skill directory.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

BUNDLED = {"references": "reference", "assets": "asset", "scripts": "script"}
SKIP_PARTS = {"__pycache__", ".venv", "node_modules", ".git"}


def mode_of(skill: Path, repo: Path) -> str | None:
    rel = skill.relative_to(repo).parts if skill.is_relative_to(repo) else ()
    if rel[:1] == (".legacy-assets",):
        return "legacy"
    if rel[:2] == (".claude", "skills"):
        return "local"
    return None


def tracked(path: Path, repo: Path) -> bool:
    """Local mode documents project-authored skills only — the ones git tracks."""
    try:
        out = subprocess.run(["git", "ls-files", "--", str(path)], cwd=repo,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    return bool(out.strip())


def next_number(repo: Path) -> int:
    used = []
    for card in (repo / "ai-engineering-knowledge-cards" / "component-cards").rglob("*.md"):
        m = re.search(r"^component:\s*(\d+)", card.read_text(encoding="utf-8"), re.M)
        if m:
            used.append(int(m.group(1)))
    return max(used, default=0) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir")
    ap.add_argument("--repo", default=".", help="repository root (default: cwd)")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    skill = Path(a.skill_dir).resolve()
    if not (skill / "SKILL.md").is_file():
        ap.error(f"{skill} has no SKILL.md")
    mode = mode_of(skill, repo)
    if mode is None:
        ap.error("the skill must sit under .legacy-assets/ (legacy) or .claude/skills/ (local)")
    if mode == "local" and not tracked(skill / "SKILL.md", repo):
        ap.error("a vendored (untracked) skill is not a component-card source; "
                 "local mode documents project-authored skills only")

    number = next_number(repo)
    artifacts = []
    for f in sorted(p for p in skill.rglob("*") if p.is_file()):
        rel = f.relative_to(skill)
        if SKIP_PARTS & set(rel.parts):
            continue
        if rel.as_posix() == "SKILL.md":
            kind = "skill"
        elif len(rel.parts) > 1 and rel.parts[0] in BUNDLED:
            kind = BUNDLED[rel.parts[0]]
        else:
            kind = "unmapped"
        artifacts.append({"path": rel.as_posix(), "type": kind,
                          "lines": len(f.read_bytes().splitlines())})

    # The skill card takes the first number; its parts follow in path order.
    artifacts.sort(key=lambda x: (x["type"] != "skill", x["path"]))
    for art in artifacts:
        if art["type"] != "unmapped":
            art["number"] = f"{number:02d}"
            number += 1
    print(json.dumps({"mode": mode, "skill_dir": str(skill), "artifacts": artifacts,
                      "unmapped": sum(a["type"] == "unmapped" for a in artifacts)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
