"""The two builders the source carries beside its template — one in the
repository detector, one in the status script's initialise command. Each is a
fresh dictionary literal, as in the source; neither opens template.json.

Imported by drift.py. Running it directly with --init prints what the
initialise command would create.
"""

from __future__ import annotations

import json
import sys
from datetime import date


def _workstreams(owned_roles: list[str]) -> dict:
    return {
        "A": {"name": "secrets-store TLS", "status": "not_started", "band": "quick_win",
              "depends_on": [], "requires_trigger": []},
        "B": {"name": "secrets-store auto-unseal", "status": "not_started", "band": "medium_effort",
              "depends_on": ["A"], "requires_trigger": ["transit_schema"]},
        "C": {"name": "admission-policy remediation", "status": "not_started", "band": "quick_win",
              "depends_on": [], "requires_trigger": [], "owned_roles": owned_roles},
        "D": {"name": "CIS benchmark triage", "status": "not_started", "band": "quick_win",
              "depends_on": [], "requires_trigger": [], "report_path": ""},
        "E": {"name": "cluster hygiene", "status": "not_started", "band": "medium_effort",
              "depends_on": [], "requires_trigger": []},
    }


def _checkpoints(today: str) -> dict:
    return {
        "A": {"target": f"{today} end of day", "status": "pending", "deliverables": []},
        "B": {"target": "tomorrow midday", "status": "pending", "deliverables": []},
        "C": {"target": "tomorrow end of day", "status": "pending", "deliverables": []},
    }


def build_from_detector(roles_found: list[str], today: str) -> dict:
    """The scope-lock copy: owned roles are every role directory it found."""
    return {
        "sprint": {"name": f"hardening-{today}", "created": today, "environment": "dev",
                   "cluster_access": False, "output_dir": f"docs/hardening-{today}", "repo_path": "."},
        "detected": {"roles_count": len(roles_found)},
        "workstreams": _workstreams(list(roles_found)),
        "triggers": {"transit_schema": {"state": "unresolved"},
                     "tls_stable": {"state": "pending"},
                     "platform_conflict": {"state": "pending"}},
        "checkpoints": _checkpoints(today),
    }


def build_from_init(today: str) -> dict:
    """The status script's copy: the same shape again, minus detection."""
    plan = build_from_detector([], today)
    del plan["detected"]
    del plan["sprint"]["repo_path"]
    return plan


if __name__ == "__main__":
    if sys.argv[1:] != ["--init"]:
        print("usage: python3 builders.py --init", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(build_from_init(date.today().isoformat()), indent=2))
