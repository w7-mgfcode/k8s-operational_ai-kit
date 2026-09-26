#!/usr/bin/env python3
"""Package a capability — and REFUSE if validation fails.

This refusal is the entire enforcement mechanism of the pattern. A validator
that can be skipped is advice; one whose failure blocks packaging is a rule.

Usage:  python3 package.py <dir> [--out DIR]
"""
from __future__ import annotations
import argparse, subprocess, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill_dir")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    d = Path(a.skill_dir)

    print(f"re-running validation on {d} ...")
    rc = subprocess.run([sys.executable, str(HERE / "validate.py"), str(d)]).returncode
    if rc != 0:
        print("\nREFUSING to package — validation failed.")
        print("This is not advice. The gate is the pattern.")
        sys.exit(1)

    out = Path(a.out) / f"{d.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(d.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(d.parent))

    summary = Path(a.out) / f"{d.name}.summary.txt"
    names = zipfile.ZipFile(out).namelist()
    summary.write_text(
        f"{d.name}\n{'=' * len(d.name)}\n\n{len(names)} file(s):\n"
        + "".join(f"  {n}\n" for n in names)
        + "\nValidation: PASS (re-run at package time)\n", encoding="utf-8")
    print(f"\npackaged {out}  ({len(names)} files)")
    print(f"summary  {summary}   <- what a reviewer reads instead of unzipping")


if __name__ == "__main__":
    main()
