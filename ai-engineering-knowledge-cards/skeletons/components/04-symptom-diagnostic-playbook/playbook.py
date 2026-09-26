#!/usr/bin/env python3
"""Symptom-class diagnostic playbook — pick the command block for a symptom, and
lint the catalogue the block comes from.

    python3 playbook.py                                  render for the default symptom
    python3 playbook.py --symptom "pvc stuck, tls errors, helm upgrade failed"
    python3 playbook.py --lint                           check every command in the catalogue

Rendering prints commands; it never runs them. Exit codes: 0 = rendered.
1 = --lint found at least one defect (the demonstration).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILL = {"{ctx}": "dev-east", "{ns}": "shop", "{pod}": "checkout-0",
        "{pvc}": "data-checkout-0", "{release}": "shop", "{svc}": "checkout"}
DELEGATE_AT = 3  # symptoms spanning this many classes go to a broader skill

READ_VERBS = {"kubectl": {"get", "describe", "logs", "top", "auth", "events"},
              "helm": {"list", "status", "history", "get"}}
CONTEXT_FLAG = {"kubectl": "--context", "helm": "--kube-context"}
SECRET_BEARING = [(re.compile(r"helm .*get values"), "release values can hold secrets"),
                  (re.compile(r"get secrets?\b.*-o (yaml|json)"), "prints secret data")]


def render(cmd: str) -> str:
    # Plain replacement, not str.format: jsonpath expressions contain braces.
    for k, v in FILL.items():
        cmd = cmd.replace(k, v)
    return cmd


def classify(symptom: str, classes: dict) -> list[str]:
    words = re.findall(r"[a-z0-9]+", symptom.lower())
    return [name for name, c in classes.items() if any(k in words for k in c["keywords"])]


def show(cat: dict, symptom: str) -> None:
    matched = classify(symptom, cat["classes"])
    print(f"symptom: {symptom!r}")
    print(f"classes: {', '.join(matched) or 'none — baseline only'}")
    if len(matched) >= DELEGATE_AT:
        print(f"\n{len(matched)} classes: too broad for one block. Recommend the broader "
              "troubleshooting skill for diagnosis, then return here for research and ranking.")
        return
    print("\n# baseline")
    for c in cat["baseline"]:
        print("  " + render(c))
    for name in matched:
        print(f"\n# {name}")
        for c in cat["classes"][name]["commands"]:
            print("  " + render(c))
    skipped = [n for n in cat["classes"] if n not in matched]
    print(f"\nnot loaded: {', '.join(skipped)}")


def lint_one(cmd: str, declared: set[str]) -> list[str]:
    found = []
    stages = [s.strip() for s in cmd.split("|")]
    head = stages[0].split()
    tool, rest = head[0], [w for w in head[1:] if not w.startswith("-") and "{" not in w]
    if tool in CONTEXT_FLAG and CONTEXT_FLAG[tool] not in head:
        found.append(f"no {CONTEXT_FLAG[tool]}: runs against whatever context is current")
    if tool in READ_VERBS and rest and rest[0] not in READ_VERBS[tool]:
        found.append(f"'{rest[0]}' is not a read verb: this command changes the cluster")
    for s in stages[1:]:
        t = s.split()[0]
        if t not in declared:
            found.append(f"pipes to '{t}', which the playbook never declares")
        if t == "grep" and "{ns}" in s:
            found.append("filters by namespace substring: 'shop' also matches 'shop-staging'")
    for pat, why in SECRET_BEARING:
        if pat.search(cmd):
            found.append(f"{why}: safe only if the redactor actually runs on it")
    return found


def lint(cat: dict) -> int:
    declared = set(cat["declared_tools"])
    blocks = [("baseline", cat["baseline"])] + [(n, c["commands"]) for n, c in cat["classes"].items()]
    total = 0
    for name, cmds in blocks:
        for cmd in cmds:
            problems = lint_one(cmd, declared)
            total += len(problems)
            mark = "ok  " if not problems else "FAIL"
            print(f"{mark} [{name}] {cmd}")
            for p in problems:
                print(f"       - {p}")
    print(f"\n{total} defect(s). Every baseline command pins its context; no class-block "
          "command does. The care taken on the lines that always run did not reach the "
          "lines that run only sometimes.")
    return 1 if total else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--symptom", default="checkout pods crashlooping, OOMKilled")
    ap.add_argument("--lint", action="store_true", help="check the whole catalogue")
    a = ap.parse_args()
    cat = json.loads((HERE / "catalogue.json").read_text())
    if a.lint:
        sys.exit(lint(cat))
    show(cat, a.symptom)


if __name__ == "__main__":
    main()
