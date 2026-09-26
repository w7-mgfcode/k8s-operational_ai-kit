#!/usr/bin/env python3
"""Project a repository into a knowledge pack. Every claim carries a citation.

A claim with a path can be re-tested mechanically. A claim without one can only
be read for plausibility — which is how bad documentation survives.

Usage:  python3 map.py [--repo DIR] [--out pack.json]
"""
from __future__ import annotations
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path

MARKERS = {
    "Chart.yaml": "helm-chart", "Dockerfile": "container",
    "pyproject.toml": "python-package", "package.json": "node-package",
    "main.yml": "automation-role",
}


def scan(root: Path) -> dict:
    components: dict[str, dict] = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name not in MARKERS:
            continue
        comp = p.parent.name
        components.setdefault(comp, {
            "kind": MARKERS[p.name],
            "evidence": [],       # citations. the whole point.
            "depends_on": [],
        })["evidence"].append(str(p.relative_to(root)))

    # Dependencies are DERIVED from configuration, not asserted by a human.
    # That is what stops the blast-radius map going stale (card 17).
    for name, c in components.items():
        for ev in c["evidence"]:
            text = (root / ev).read_text(encoding="utf-8", errors="ignore")
            for other in components:
                if other != name and re.search(rf"\b{re.escape(other)}\b", text):
                    if other not in c["depends_on"]:
                        c["depends_on"].append(other)

    unknowns = []
    for name, c in components.items():
        if not c["depends_on"]:
            unknowns.append(f"{name}: no dependencies found — UNKNOWN whether "
                            f"it truly has none or the markers do not express them")
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": root.name,
        "components": components,
        "unknowns": unknowns,
    }


def blast_radius(pack: dict) -> dict:
    """Derived, not asserted. Regenerates with the pack, so it cannot go stale
    independently of it."""
    counts = {n: 0 for n in pack["components"]}
    for c in pack["components"].values():
        for dep in c["depends_on"]:
            counts[dep] = counts.get(dep, 0) + 1
    tier = lambda n: "critical" if n >= 3 else "high" if n == 2 else "medium" if n == 1 else "low"
    return {n: {"dependents": k, "tier": tier(k)} for n, k in counts.items()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent / "fixture-repo"))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "pack.json"))
    a = ap.parse_args()

    pack = scan(Path(a.repo))
    pack["blast_radius"] = blast_radius(pack)
    Path(a.out).write_text(json.dumps(pack, indent=2) + "\n", encoding="utf-8")

    print(f"{len(pack['components'])} component(s), every claim cited:\n")
    for n, c in sorted(pack["components"].items()):
        br = pack["blast_radius"][n]
        print(f"  {n:<14} {c['kind']:<16} tier={br['tier']:<8} dependents={br['dependents']}")
        for ev in c["evidence"]:
            print(f"                 evidence: {ev}")
    if pack["unknowns"]:
        print("\nmarked UNKNOWN rather than inferred:")
        for u in pack["unknowns"]:
            print(f"  {u}")
    print(f"\nwrote {Path(a.out).name}")


if __name__ == "__main__":
    main()
