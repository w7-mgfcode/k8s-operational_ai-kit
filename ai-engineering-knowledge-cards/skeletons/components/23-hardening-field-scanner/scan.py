#!/usr/bin/env python3
"""Hardening field scanner — the component's method beside a value-aware one.

    python3 scan.py               both methods over roles/, side by side
    python3 scan.py --presence    the component's method alone, as JSON

The component pools every file in a role and asks whether each security-context
field *name* appears anywhere. The second method reads each container's block,
checks each value, and leaves out roles the team does not own (owned.json).
Where the two disagree, the first is the one the sprint would have worked from.

Exit codes: 0 = the methods agree on every role. 1 = they disagree on at least
one (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROLES = HERE / "roles"

# Seven names listed, four judged — the shape of the component's own list.
FIELDS = ["runAsNonRoot", "allowPrivilegeEscalation", "readOnlyRootFilesystem",
          "capabilities", "runAsUser", "runAsGroup", "fsGroup"]
JUDGED = FIELDS[:4]

# What a hardened container must say, field by field.
REQUIRED = {"runAsNonRoot": "true", "allowPrivilegeEscalation": "false",
            "readOnlyRootFilesystem": "true"}

CONTAINER = re.compile(r"^([ \t]*)- name:[ \t]*(\S+)[ \t]*$", re.M)
DROP = re.compile(r"\bdrop:\s*(\[[^\]]*\]|(?:\s*-\s*\S+)+)")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def role_files(role: Path) -> list[Path]:
    return sorted(p for p in role.rglob("*")
                  if p.is_file() and p.suffix in {".yml", ".yaml", ".j2"})


# --- the component's method: field names, pooled per role -------------------

def by_presence(role: Path, exceptions: set[str]) -> tuple[str, list[str]]:
    if role.name in exceptions:
        return "exception", []
    found: set[str] = set()
    for f in role_files(role):
        text = f.read_text()
        found |= {n for n in FIELDS if re.search(rf"\b{n}\b", text)}
    missing = sorted(set(JUDGED) - found)
    return ("violation" if missing else "clean"), [f"{m} missing" for m in missing]


# --- the alternative: values, per container, owned roles only ----------------

def containers(text: str) -> list[tuple[str, str]]:
    """Each '- name: x' list entry and the lines indented beneath it."""
    out = []
    for m in CONTAINER.finditer(text):
        indent, rest = len(m.group(1)), text[m.end():]
        end = len(rest)
        for line in re.finditer(r"^([ \t]*)\S", rest, re.M):
            if len(line.group(1)) <= indent:
                end = line.start()
                break
        out.append((m.group(2), rest[:end]))
    return out


def value_gaps(block: str) -> list[str]:
    gaps = []
    for name, want in REQUIRED.items():
        m = re.search(rf"\b{name}:\s*(\S+)", block)
        if not m:
            gaps.append(f"{name} unset")
        elif m.group(1).lower() != want:
            gaps.append(f"{name}={m.group(1)}")
    drop = DROP.search(block)
    if not drop or "ALL" not in drop.group(1):
        gaps.append("capabilities.drop lacks ALL")
    return gaps


def by_value(role: Path, owned: set[str], exceptions: set[str]) -> tuple[str, list[str]]:
    if role.name not in owned:
        return "not owned", ["out of scope for workstream C"]
    if role.name in exceptions:
        return "exception", []
    blocks = [c for f in role_files(role) for c in containers(f.read_text())]
    if not blocks:
        return "violation", ["no container settings: the chart's defaults decide"]
    detail = [f"{name}: {', '.join(g)}" for name, block in blocks if (g := value_gaps(block))]
    return ("violation" if detail else "clean"), detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--presence", action="store_true",
                    help="print the component's method alone, as JSON")
    a = ap.parse_args()

    owned = set(load("owned.json")["owned"])
    lists = load("exceptions.json")
    scanner_exceptions = set(lists["scanner"])
    roles = sorted(d for d in ROLES.iterdir() if d.is_dir())

    if a.presence:
        report = {r.name: dict(zip(("verdict", "detail"), by_presence(r, scanner_exceptions)))
                  for r in roles}
        print(json.dumps(report, indent=2))
        return 0

    disagree = 0
    print(f"{'role':18} {'by field name, per role':26} by value, per container, owned only")
    for r in roles:
        p, _ = by_presence(r, scanner_exceptions)
        v, detail = by_value(r, owned, scanner_exceptions)
        flag = "" if p == v else "   <- disagree"
        disagree += p != v
        print(f"{r.name:18} {p:26} {v}{flag}")
        for d in detail:
            print(f"{'':45}   {d}")

    print(f"\nfields listed: {len(FIELDS)}, judged: {len(JUDGED)} — "
          f"never judged: {', '.join(FIELDS[len(JUDGED):])}")

    print("\nelevated-access lists that disagree")
    for name in sorted(set().union(*(set(v) for k, v in lists.items() if not k.startswith("_")))):
        on = [k for k, v in lists.items() if not k.startswith("_") and name in v]
        if len(on) != 3:
            print(f"  {name:16} on {', '.join(on)} only")

    print(f"\n{disagree} of {len(roles)} roles judged differently")
    return 1 if disagree else 0


if __name__ == "__main__":
    sys.exit(main())
