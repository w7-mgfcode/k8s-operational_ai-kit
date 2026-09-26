#!/usr/bin/env python3
"""Pre-fill the scope lock from what is actually there, and mark blocked items.

Starting from detected facts produces a better conversation than starting from
a blank form — and it stops a workstream being scoped against a prerequisite
that does not exist.

Usage:  python3 detect.py [--repo DIR]
"""
from __future__ import annotations
import argparse
from pathlib import Path

EXPECTED = {
    "roles/":           "component definitions",
    "inventories/":     "environment configuration",
    "charts/vendor/":   "third-party charts — never modify",
    "reports/bench.md": "benchmark report for workstream C",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent / "fixture-repo"))
    a = ap.parse_args()
    root = Path(a.repo)

    print(f"detecting in {root.name}/\n")
    missing = []
    for rel, why in EXPECTED.items():
        p = root / rel
        if p.exists():
            n = len(list(p.iterdir())) if p.is_dir() else 1
            print(f"  found    {rel:<18} {n} item(s)   ({why})")
        else:
            print(f"  MISSING  {rel:<18}            ({why})")
            missing.append((rel, why))

    owned = sorted(p.name for p in (root / "roles").glob("*")) if (root / "roles").exists() else []
    print(f"\nownership boundary — modifiable: {', '.join(owned) or 'none detected'}")
    vendor = root / "charts" / "vendor"
    if vendor.exists():
        print(f"                     off-limits: charts/vendor/ "
              f"({len(list(vendor.iterdir()))} chart(s))")
        print("  An agent fixing a violation inside a vendored chart will correctly")
        print("  identify the problem and incorrectly conclude it may edit it.")

    if missing:
        print("\npre-filling blocked_by for workstreams whose input is absent:")
        for rel, why in missing:
            print(f"  blocked_by: \"no file at {rel}\"  -> {why}")
    print("\nNothing is generated yet. This goes to the operator for approval.")


if __name__ == "__main__":
    main()
