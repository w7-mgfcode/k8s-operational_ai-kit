#!/usr/bin/env python3
"""The cheapest secret to redact is the one never read.

Filters search results as well as direct reads — a grep hit that quotes a line
from a forbidden file has already leaked it.

Usage:  python3 restricted_paths.py
"""
from __future__ import annotations
import fnmatch

RESTRICTED = [
    "**/*vault*.yml", "**/*-vault.yml", "**/secrets/**",
    ".env", ".env.*", ".envrc", "**/.git/**", "**/.kube/**",
]

CANDIDATES = [
    "roles/app/tasks/main.yml",
    "inventories/prod/group_vars/all/30-vault.yml",
    "services/api/secrets/db.yaml",
    ".env.production",
    "docs/architecture.md",
    "/home/op/.kube/config",
]


def restricted(path: str) -> str | None:
    for pat in RESTRICTED:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, pat.replace("**/", "*/")) \
           or fnmatch.fnmatch("/" + path, "*/" + pat.lstrip("*/")):
            return pat
    return None


print("simulating a grep that matched these files:\n")
for p in CANDIDATES:
    pat = restricted(p)
    if pat:
        print(f"  BLOCKED  {p}")
        print(f"           matched {pat} — note the path, do NOT open it,")
        print( "           advise a manual check")
    else:
        print(f"  ok       {p}")
