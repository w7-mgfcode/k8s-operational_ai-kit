#!/usr/bin/env python3
"""Search new and changed files for every original in the approved masking table.

    python3 residue_check.py --table <table.json> --paths <file> [<file> ...]
    python3 residue_check.py --table <table.json> --changed-since origin/main

The table is JSON: {"rows": [{"original": "...", "replacement": "..."}, ...]}.
It holds originals, so it must live outside the repository; the script refuses
a table inside the working tree. Matching is case-insensitive substring.

A hit is reported as file:line and the table row number — never the matched
value, so this output is safe to paste into a PR or a commit message.

Exit codes: 0 = no original found, 1 = residue found, 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(out).resolve()
    except (OSError, subprocess.CalledProcessError):
        return None


def changed_since(ref: str) -> list[Path]:
    diff = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AMR", ref],
                          capture_output=True, text=True, check=True).stdout.split()
    new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                         capture_output=True, text=True, check=True).stdout.split()
    return [Path(p) for p in sorted(set(diff + new))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--paths", nargs="+")
    group.add_argument("--changed-since", metavar="REF")
    a = ap.parse_args()

    table = Path(a.table).resolve()
    root = repo_root()
    if root and table.is_relative_to(root):
        ap.error("the table holds originals: keep it outside the repository")
    try:
        rows = json.loads(table.read_text(encoding="utf-8"))["rows"]
        originals = [(i, r["original"].lower()) for i, r in enumerate(rows, 1) if r["original"].strip()]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(f"cannot read table: {exc}")

    try:
        paths = [Path(p) for p in a.paths] if a.paths else changed_since(a.changed_since)
    except subprocess.CalledProcessError as exc:
        ap.error(f"git failed: {exc}")

    hits = 0
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            low = line.lower()
            for row, original in originals:
                if original in low:
                    print(f"{path}:{n}: original from table row {row}")
                    hits += 1
    print(f"{len(paths)} files, {len(originals)} originals, {hits} hits", file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
