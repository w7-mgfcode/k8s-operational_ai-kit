#!/usr/bin/env python3
"""Owned-scope policy remediation — the guide's file-level inventory beside a
per-container one, then the two scope questions the guide leaves open.

    python3 inventory.py               all three sections; exits 1
    python3 inventory.py --method file the file-level inventory only; exits 0

File-level is the guide's offline method: a file is clean for a field if the
field's name appears anywhere in it. Per-container splits each manifest into
its containers and reads each field's value. The two disagree wherever one
container is hardened and its neighbour is not, and wherever a field is set to
the unsafe value.

Exit codes: 0 = no disagreement shown. 1 = the methods, the exception lists or
the scope disagree (the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROLES = HERE / "roles"

# field -> the value that counts as hardened, as a regex over the field's block
FIELDS = {
    "runAsNonRoot": r"runAsNonRoot:\s*true\b",
    "allowPrivilegeEscalation": r"allowPrivilegeEscalation:\s*false\b",
    "readOnlyRootFilesystem": r"readOnlyRootFilesystem:\s*true\b",
    "capabilities": r"drop:\s*\n\s*-\s*ALL\b",
}


def role_files() -> list[Path]:
    return sorted(p for p in ROLES.rglob("*") if p.suffix in (".yaml", ".yml"))


def file_level(text: str) -> set[str]:
    """The guide's method: which field names are absent from the file."""
    return {f for f in FIELDS if f not in text}


def containers(text: str) -> list[tuple[str, str]]:
    """Split a manifest at each '- name:' list item; a values file is one unit."""
    parts = re.split(r"^\s*- name:\s*(\S+)\s*$", text, flags=re.M)
    if len(parts) == 1:
        return [("(values)", text)]
    return list(zip(parts[1::2], parts[2::2]))


def per_container(text: str) -> dict[str, set[str]]:
    return {name: {f for f, rx in FIELDS.items() if not re.search(rx, body)}
            for name, body in containers(text)}


def compare(owned: list[str], show_only_file: bool) -> int:
    disagreements = 0
    print("inventory — which hardening fields are missing")
    print(f"  {'file':48} {'file-level':12} per-container")
    for p in role_files():
        role = p.relative_to(ROLES).parts[0]
        text = p.read_text()
        flat = file_level(text)
        rel = p.relative_to(HERE).as_posix()
        if show_only_file:
            print(f"  {rel:48} {len(flat)} missing")
            continue
        deep = per_container(text)
        worst = max((len(v) for v in deep.values()), default=0)
        mark = "  DISAGREE" if worst and not flat else ""
        disagreements += bool(mark)
        print(f"  {rel:48} {len(flat)} missing    "
              + ", ".join(f"{c}: {len(v)}" for c, v in deep.items()) + mark)
    return disagreements


def exceptions(scope: dict) -> int:
    lists = scope["exceptions"]
    every = sorted(set().union(*lists.values()))
    print("\nexception lists — one per source artifact")
    print(f"  {'role':20} " + " ".join(f"{k:9}" for k in lists))
    split = 0
    for role in every:
        marks = [("yes" if role in v else "-") for v in lists.values()]
        odd = len(set(marks)) > 1
        split += odd
        print(f"  {role:20} " + " ".join(f"{m:9}" for m in marks) + ("  DISAGREE" if odd else ""))
    return split


def ownership(scope: dict) -> int:
    every = sorted(d.name for d in ROLES.iterdir() if d.is_dir())
    extra = sorted(set(every) - set(scope["owned"]))
    print("\nscope — the detector treats every role as owned")
    for role in extra:
        print(f"  {role:20} enters the inventory, though no one on the team owns it")
    return len(extra)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--method", choices=["file", "both"], default="both")
    a = ap.parse_args()
    scope = json.loads((HERE / "scope.json").read_text())
    if a.method == "file":
        compare(scope["owned"], True)
        return 0
    problems = compare(scope["owned"], False) + exceptions(scope) + ownership(scope)
    print(f"\n{problems} disagreements across the inventory, the exception lists and the scope")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
