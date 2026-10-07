"""A mechanical version of the planner reference's validation gate.

    python3 check_spec.py                 # all three fixture specs
    python3 check_spec.py spec_good.md    # one spec
    python3 check_spec.py --rules rules.json   # the structure against the role's own bans

Checks only what a program can read: sections present, sprint count, targets per
sprint, files per sprint, dependency order, a non-empty out-of-scope list. Whether a
target is concrete, and whether the user approved, are not things it can see.

Exit codes: 0 = mechanically complete, 1 = a finding was shown on purpose.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_SPRINTS = 5
MAX_FILES = 10
TARGETS = (2, 5)


def parse(text: str) -> dict:
    spec = {"goal": "", "out_of_scope": [], "sprints": []}
    section, sprint, field = "", None, ""
    for line in text.splitlines():
        if line.startswith("## "):
            section, sprint = line[3:].strip().lower(), None
            continue
        if line.startswith("### Sprint"):
            sprint = {"title": line[4:].strip(), "fields": {}, "targets": []}
            spec["sprints"].append(sprint)
            continue
        if section == "goal" and line.strip():
            spec["goal"] += line.strip() + " "
        elif section == "out of scope" and line.startswith("- "):
            spec["out_of_scope"].append(line[2:].strip())
        elif sprint is not None:
            m = re.match(r"- \*\*([^:*]+):\*\*\s*(.*)", line)
            if m:
                field = m.group(1).strip().lower()
                sprint["fields"][field] = m.group(2).strip()
            elif line.startswith("  - ") and field == "acceptance targets":
                sprint["targets"].append(line[4:].strip())
    return spec


def findings(spec: dict) -> list:
    out = []
    if not spec["goal"].strip():
        out.append("no goal statement")
    if not 1 <= len(spec["sprints"]) <= MAX_SPRINTS:
        out.append(f"{len(spec['sprints'])} sprints (limit {MAX_SPRINTS})")
    if not spec["out_of_scope"]:
        out.append("out-of-scope list missing or empty")
    for i, s in enumerate(spec["sprints"], 1):
        name = f"sprint {i}"
        for need in ("scope", "files", "dependencies", "acceptance targets"):
            if need not in s["fields"]:
                out.append(f"{name}: no {need}")
        n = len(s["targets"])
        if not TARGETS[0] <= n <= TARGETS[1]:
            out.append(f"{name}: {n} acceptance targets (want {TARGETS[0]}-{TARGETS[1]})")
        files = [f for f in s["fields"].get("files", "").split(",") if f.strip()]
        if len(files) > MAX_FILES:
            out.append(f"{name}: {len(files)} files in scope (limit about {MAX_FILES})")
        for ref in re.findall(r"Sprint (\d+)", s["fields"].get("dependencies", "")):
            if int(ref) >= i:
                out.append(f"{name}: depends on sprint {ref}, which is not earlier")
    return out


def check_file(path: Path) -> int:
    spec = parse(path.read_text(encoding="utf-8"))
    found = findings(spec)
    print(f"{path.name}: {len(spec['sprints'])} sprints")
    for f in found:
        print(f"  FINDING  {f}")
    if not found:
        print("  mechanically complete — concreteness of targets and user approval not checked")
    return 1 if found else 0


def check_rules(path: Path) -> int:
    rules = json.loads(path.read_text(encoding="utf-8"))
    print(f"required fields come from: {rules['sources']['required_sprint_fields']}")
    print(f"bans come from:            {rules['sources']['forbidden_activities']}")
    clash = 0
    for field, activity in rules["field_needs_activity"].items():
        if activity in rules["forbidden_activities"]:
            print(f"  CONFLICT  '{field}' is required, and filling it means to {activity}, which is banned")
            clash += 1
    return 1 if clash else 0


def main(argv: list) -> int:
    if argv[:1] == ["--rules"]:
        return check_rules(Path(argv[1]) if len(argv) > 1 else HERE / "rules.json")
    names = argv or ["spec_good.md", "spec_bad.md", "spec_vague.md"]
    return max(check_file(HERE / n) for n in names)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
