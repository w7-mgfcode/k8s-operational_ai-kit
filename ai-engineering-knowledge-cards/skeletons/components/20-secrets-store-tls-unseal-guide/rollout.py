#!/usr/bin/env python3
"""Secrets-store TLS guide — the change, two rollbacks, and the probe.

    python3 rollout.py                 the whole demonstration
    python3 rollout.py --only rollback the two rollbacks
    python3 rollout.py --only probe    the probe with and without verification

A fabricated repository is a dict of file -> content; "git" is a dict of the
last committed contents. Workstream A edits four files and fills one task file.
The guide's rollback reverts all four. The rollback planner's command restores
one file from the last commit. The difference is printed as residual state.

Exit codes: 0 = both rollbacks leave the repository as it started and the
probe tells a bad certificate from a good one. 1 = they do not (the
demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

BASELINE = {
    "inventory/security-vars.yml": "store_tls_enabled: false\n",
    "roles/secrets-store/tasks/server-values.yml": "listener: {tls: off}\n",
    "roles/secrets-store/tasks/cluster-join.yml": "join: [http://store-0.peers, http://store-1.peers]\n",
    "roles/secrets-store/tasks/probes.yml": "probe: {scheme: http}\n",
    "roles/secrets-store/tasks/tls.yml": "# empty: TLS not configured yet\n",
}

TLS_EDITS = {
    "inventory/security-vars.yml": "store_tls_enabled: true\n",
    "roles/secrets-store/tasks/server-values.yml": "listener: {tls: on, cert: /tls/crt, key: /tls/key}\n",
    "roles/secrets-store/tasks/cluster-join.yml": "join: [https://store-0.peers, https://store-1.peers]\n",
    "roles/secrets-store/tasks/probes.yml": "probe: {scheme: https, verify: false}\n",
    "roles/secrets-store/tasks/tls.yml": "certificate: {issuer: cluster-ca, names: [store, store-0.peers]}\n",
}

# The guide's rollback: flag off, then revert listener, join addresses, probes.
GUIDE_ROLLBACK = [
    "inventory/security-vars.yml",
    "roles/secrets-store/tasks/server-values.yml",
    "roles/secrets-store/tasks/cluster-join.yml",
    "roles/secrets-store/tasks/probes.yml",
]
# The planner's git command: restore the TLS task file from the last commit.
PLANNER_RESTORE = ["roles/secrets-store/tasks/tls.yml"]


def residual(tree: dict[str, str]) -> list[str]:
    return [f for f in sorted(tree) if tree[f] != BASELINE[f]]


def guide_rollback(tree: dict[str, str]) -> dict[str, str]:
    out = dict(tree)
    for f in GUIDE_ROLLBACK:
        out[f] = BASELINE[f]
    return out


def planner_restore(tree: dict[str, str], head: dict[str, str]) -> dict[str, str]:
    out = dict(tree)
    for f in PLANNER_RESTORE:
        out[f] = head[f]
    return out


def show(label: str, tree: dict[str, str]) -> int:
    left = residual(tree)
    print(f"  {label}")
    if not left:
        print("    back to baseline")
    for f in left:
        print(f"    still changed: {f:46} {tree[f].strip()}")
    return len(left)


def rollback_demo() -> int:
    print("workstream A applied: five files changed\n")
    applied = {**BASELINE, **TLS_EDITS}
    bad = 0

    print("change not yet committed (last commit = baseline)")
    bad += show("guide's rollback", guide_rollback(applied)) > 1
    bad += show("planner's restore-from-last-commit", planner_restore(applied, BASELINE)) > 0

    print("\nchange committed, then found unstable (last commit = the change)")
    show("guide's rollback", guide_rollback(applied))
    bad += show("planner's restore-from-last-commit", planner_restore(applied, applied)) > 0

    print("\n  The guide's rollback leaves only the certificate request, which is harmless.")
    print("  The planner restores one file, or nothing — the listener and probes keep TLS.")
    return bad


@dataclass(frozen=True)
class Cert:
    names: tuple[str, ...]
    issuer: str


TRUSTED = {"cluster-ca"}


def probe(cert: Cert, host: str, verify: bool) -> bool:
    """A readiness probe over TLS. Without verification, any handshake passes."""
    if not verify:
        return True
    return cert.issuer in TRUSTED and host in cert.names


def probe_demo() -> int:
    print("\nreadiness probe, host store-1.peers")
    cases = [
        ("certificate covering every replica", Cert(("store", "store-0.peers", "store-1.peers"), "cluster-ca")),
        ("certificate missing this replica", Cert(("store", "store-0.peers"), "cluster-ca")),
        ("self-signed fallback after a failed issue", Cert(("localhost",), "self")),
    ]
    wrong = 0
    print(f"  {'served':44} {'no verify':10} {'verify'}")
    for label, cert in cases:
        loose, strict = probe(cert, "store-1.peers", False), probe(cert, "store-1.peers", True)
        wrong += loose != strict
        print(f"  {label:44} {'ready' if loose else 'FAIL':10} {'ready' if strict else 'FAIL'}")
    print(f"\n  {wrong} bad certificates the guide's probe reports as ready")
    return wrong


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=["rollback", "probe"])
    a = ap.parse_args()

    bad = 0
    if a.only in (None, "rollback"):
        bad += rollback_demo()
    if a.only in (None, "probe"):
        bad += probe_demo()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
