#!/usr/bin/env python3
"""Investigation safety rules, applied mechanically to fabricated inputs.

    python3 guard.py           apply each rule to the cases it was written for
    python3 guard.py --audit   probe each rule with one case it was not

Five of the six rule sets: prod guard, command deny list, web-query hygiene,
restricted paths, secret scrubbing. The sixth — unbatched confirmation points —
is a conversation rule and has nothing to run.

Exit codes: 0 = every rule held. 1 = --audit got at least one probe past a rule
(the demonstration).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 1. Prod guard: classify by substring of the context name or kubeconfig path.
def classify(ctx: dict) -> str:
    name = f"{ctx['context']} {ctx['kubeconfig']}"
    if "prod" in name:
        return "prod"
    if "dev" in name:
        return "dev"
    if any(e in name for e in ("staging", "test", "qa")):
        return "guarded"
    return "prod"  # unqualified falls to the strictest class

# 2. The deny list as written: fifteen verbs, three of them harness-enforced.
DENY = {"delete", "apply", "patch", "edit", "replace", "scale", "drain", "cordon",
        "uncordon", "helm install", "helm upgrade", "helm uninstall", "helm rollback",
        "ansible-playbook", "ansible"}
ALLOW = {"get", "describe", "logs", "top", "auth"}

def verb(cmd: str) -> str:
    parts = cmd.split()
    return " ".join(parts[:2]) if parts[0] == "helm" else parts[0]

# 3. Query hygiene as instructed: strip proper nouns. As a filter: strip a name list.
def strip_proper_nouns(q: str) -> str:
    return " ".join(w for w in q.split() if not w[:1].isupper())

def strip_names(q: str, names: list[str]) -> str:
    return " ".join(w for w in q.split() if w not in names)

# 4. Restricted paths: never open these, even when a search matches them.
RESTRICTED = ["*vault*.yml", "*/secrets/*", ".env", ".envrc", ".git/*"]

# 5. Scrubbing. The rules say: base64 >= 40 chars *after known secret keys*.
# The skill's script instead redacts any such run, anywhere.
# No leading \b: the rules match the key as a substring, so db_password is caught.
KEYED = re.compile(r"(?i)(password|token|secret|credential|api[_-]?key)(\w*\s*[:=]\s*)(\S+)")
B64_AFTER_KEY = re.compile(r"(?i)\b((?:\w*(?:password|token|secret|key))\s*[:=]\s*)([A-Za-z0-9+/]{40,}={0,2})")
B64_ANYWHERE = re.compile(r"([A-Za-z0-9+/]{40,}={0,2})")

def scrub_as_written(text: str) -> str:
    text = KEYED.sub(lambda m: m.group(1) + m.group(2) + "«REDACTED»", text)
    return B64_AFTER_KEY.sub(lambda m: m.group(1) + "«REDACTED»", text)

def scrub_as_scripted(text: str) -> str:
    text = KEYED.sub(lambda m: m.group(1) + m.group(2) + "«REDACTED»", text)
    return B64_ANYWHERE.sub("«REDACTED»", text)


def section(title: str) -> None:
    print(f"\n── {title} " + "─" * max(0, 58 - len(title)))


def run(data: dict, part: str) -> int:
    gaps = 0
    names = data["installation_names"]

    section("1 prod guard")
    for ctx in data["contexts"][part]:
        got = classify(ctx)
        wrong = (got == "dev") != (ctx["actually"] == "dev")
        gaps += wrong
        print(f"  {ctx['context']:12} -> {got:8} actually {ctx['actually']:8}"
              + (f"  GAP: {ctx['why']}" if wrong else ""))

    section("2 command deny list")
    for cmd in data["commands"][part]:
        v = verb(cmd)
        denied, allowed = v in DENY, v in ALLOW
        slipped = not denied and not allowed
        gaps += slipped
        status = "denied" if denied else ("read" if allowed else "NOT DENIED — writes to the cluster")
        tool = "" if cmd.startswith("helm") else "kubectl "
        print(f"  {status:36} {tool}{cmd}")
    if part == "probes":
        print("  an allow list of read verbs would have refused every NOT DENIED line")

    section("3 web-query hygiene")
    for q in data["queries"][part]:
        told = strip_proper_nouns(q)
        filt = strip_names(q, names)
        leaked = [n for n in names if n in told.split()]
        gaps += bool(leaked) and part == "probes"
        print(f"  draft:        {q}")
        print(f"  as filtered:  {filt}")
        if part == "probes":
            print(f"  as instructed ('strip proper nouns'): {told}")
            dropped = [w for w in q.split() if w[:1].isupper()]
            print(f"  GAP: leaks {leaked}, and drops {dropped} — the error string and "
                  "public component the rule says to keep")

    section("4 restricted paths")
    for hit in data["search_hits"][part]:
        blocked = any(fnmatch.fnmatch(hit["path"], g) for g in RESTRICTED)
        print(f"  {'not opened' if blocked else 'readable':11} {hit['path']}")
        if blocked and part == "probes":
            gaps += 1
            print(f"  GAP: the search already returned the line: {hit['line']!r}")

    section("5 secret scrubbing")
    for item in data["output"][part]:
        raw = item["line"]
        w, s = scrub_as_written(raw), scrub_as_scripted(raw)
        print(f"  input:    {raw}")
        print(f"  rules:    {w}")
        print(f"  script:   {s}")
        if w != s:
            gaps += 1
            which = "the rules leak a secret" if item["secret"] else "the script redacts a non-secret"
            print(f"  GAP: the rules and the script disagree — {which}")
    return gaps


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", action="store_true", help="probe each rule's gap")
    a = ap.parse_args()
    data = json.loads((HERE / "inputs.json").read_text())

    gaps = run(data, "probes" if a.audit else "cases")
    print()
    if gaps:
        print(f"  {gaps} probe(s) got past a rule. Each rule above is an instruction the "
              "model is trusted to follow; only the harness-enforced deny entries are controls.")
        sys.exit(1)
    print("  every rule held on the cases it was written for")


if __name__ == "__main__":
    main()
