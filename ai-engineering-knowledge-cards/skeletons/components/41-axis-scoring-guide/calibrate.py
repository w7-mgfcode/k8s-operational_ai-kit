"""Audit a table of calibration bands the way a scoring guide's reader would use it.

    python3 calibrate.py --audit                       # gaps and axes with no anchors
    python3 calibrate.py --coverage 0.4                # which band a measured fraction falls in
    python3 calibrate.py --not-applicable --threshold 4            # "not applicable" scored as 5
    python3 calibrate.py --not-applicable --threshold 4 --excluded # the same axis left out of the gate

Exit codes: 0 = a score was found or the gate was unaffected, 1 = the gap, or the free
pass, was shown on purpose, 2 = arguments needed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent / "bands.json").read_text(encoding="utf-8"))


def gaps(bands: list) -> list:
    """Ranges between the lowest and highest band that no band covers."""
    out, edge = [], None
    for b in sorted(bands, key=lambda b: b["low"]):
        if edge is not None and b["low"] > edge + 0.011:
            out.append((round(edge, 2), round(b["low"], 2)))
        edge = max(edge or 0.0, b["high"])
    return out


def audit() -> int:
    found = 0
    for name, axis in DATA["axes"].items():
        if not axis["bands"]:
            print(f"{name}: no calibration anchors — the score is a judgement with nothing to compare to")
            found += 1
            continue
        for lo, hi in gaps(axis["bands"]):
            print(f"{name}: no band covers {lo:.2f} to {hi:.2f} ({axis['unit']})")
            found += 1
    print(f"{found} findings")
    return 1 if found else 0


def lookup(value: float) -> int:
    for b in DATA["axes"]["test_coverage"]["bands"]:
        if b["low"] <= value <= b["high"]:
            print(f"{value:.2f} falls in the band for score {b['score']}")
            return 0
    print(f"{value:.2f} falls in no band; the evaluator must choose a score unaided")
    return 1


def not_applicable(threshold: int, excluded: bool) -> int:
    if excluded:
        print("axis excluded from the gate: no score, no evidence claimed, gate unaffected")
        return 0
    top = DATA["scale"][-1]
    print(f"axis scored {top} as 'not applicable'; threshold {threshold}: "
          f"{'PASS' if top >= threshold else 'FAIL'} — the top score, with no code examined")
    return 1


def main(argv: list) -> int:
    if not argv or argv == ["--audit"]:
        return audit()
    if argv[0] == "--coverage" and len(argv) > 1:
        return lookup(float(argv[1]))
    if argv[0] == "--not-applicable" and "--threshold" in argv:
        return not_applicable(int(argv[argv.index("--threshold") + 1]), "--excluded" in argv)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
