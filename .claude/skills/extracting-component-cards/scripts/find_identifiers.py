#!/usr/bin/env python3
"""List candidate identifiers in a skill directory, for the masking table.

    python3 find_identifiers.py <skill-dir>

Prints JSON: one entry per distinct candidate, with its class and every
file:line it appears on. Classes are shapes — absolute and home paths, email
addresses, IPv4 addresses and CIDRs, internal-looking domains, other hostnames,
URLs, the skill's own name, and capitalised words that are not on the public
technology list. A shape scan cannot judge a name: a person still reads the
source, and the masking table is what the owner approves, not this output.

The output contains originals. It belongs in the chat and in a scratch file
outside the repository — never in a tracked file.

Exit codes: 0 = scanned (with or without candidates), 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_PARTS = {"__pycache__", ".venv", "node_modules", ".git"}
INTERNAL_TLDS = "local|internal|corp|lan|intra|home|private"
# Assembled from parts so this file does not itself match check.py's shapes.
SHAPES = [
    ("home-path", re.compile(r"(?:/" + r"home|/" + r"Users)/[A-Za-z0-9._-]+[^\s'\"`)]*")),
    ("tilde-path", re.compile(r"~/[A-Za-z0-9._/-]+")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("ip-or-cidr", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b")),
    ("internal-domain", re.compile(r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:" + INTERNAL_TLDS + r")\b", re.I)),
    ("url", re.compile(r"https?://[^\s'\"`)>]+")),
    ("hostname", re.compile(r"\b[a-z][a-z0-9-]*\d[a-z0-9-]*(?:\.[a-z0-9-]+)+\b")),
]
# Public names the anonymization rule keeps, plus words every skill uses.
KEEP = {
    "kubernetes", "ansible", "helm", "vault", "prometheus", "grafana", "loki", "mimir",
    "tempo", "kyverno", "cilium", "longhorn", "claude", "python", "git", "github",
    "markdown", "yaml", "json", "bash", "docker", "linux", "openai", "anthropic",
    # Kubernetes kinds and states, Python exceptions, agent tool names: public vocabulary.
    "crashloopbackoff", "imagepullbackoff", "oomkilled", "failedmount", "serviceaccount",
    "cronjob", "configmap", "statefulset", "daemonset", "networkpolicy", "persistentvolumeclaim",
    "clusterrole", "rolebinding", "clusterrolebinding", "customresourcedefinition", "crds",
    "policyexception", "policyviolation", "ids", "oserror", "keyboardinterrupt", "valueerror",
    "keyerror", "typeerror", "websearch", "webfetch", "notebookedit", "askuserquestion",
}
PROPER = re.compile(r"(?<![\w./-])([A-Z][a-z]+(?:[A-Z][a-z0-9]+)+|[A-Z]{2,}[a-z]+\w*)(?![\w-])")


def text_files(root: Path):
    for f in sorted(root.rglob("*")):
        if f.is_file() and not SKIP_PARTS & set(f.relative_to(root).parts):
            try:
                yield f, f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir")
    a = ap.parse_args()
    root = Path(a.skill_dir).resolve()
    if not (root / "SKILL.md").is_file():
        ap.error(f"{root} has no SKILL.md")

    found: dict[tuple[str, str], list[str]] = defaultdict(list)
    names = {root.name}
    m = re.search(r"^name:\s*(\S+)", (root / "SKILL.md").read_text(encoding="utf-8"), re.M)
    if m:
        names.add(m.group(1))

    for f, text in text_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(text.splitlines(), 1):
            where = f"{rel}:{n}"
            for name in names:
                if name in line:
                    found[("component-name", name)].append(where)
            for cls, rx in SHAPES:
                for hit in rx.findall(line):
                    found[(cls, hit)].append(where)
            for word in PROPER.findall(line):
                if word.lower() not in KEEP:
                    found[("capitalised-name", word)].append(where)

    out = [{"identifier": ident, "class": cls, "count": len(w), "where": w[:10]}
           for (cls, ident), w in sorted(found.items(), key=lambda kv: (kv[0][0], -len(kv[1])))]
    print(json.dumps({"skill_dir": str(root), "candidates": out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
