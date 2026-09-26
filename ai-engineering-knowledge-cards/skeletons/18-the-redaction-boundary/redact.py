#!/usr/bin/env python3
"""Scrub credential-shaped strings. Conservative by design.

Over-redaction costs a question. Under-redaction is irreversible once the
artifact exists. Clean content to stdout, one report line per removal to
stderr, so the gate works in a pipeline and still produces an audit trail.

Usage:  python3 redact.py < sample-output.txt > clean.txt
        python3 redact.py --report < sample-output.txt
"""
from __future__ import annotations
import argparse, re, sys

MARK = "«REDACTED»"

# Specific structured patterns FIRST. A general pattern matching first would
# half-mangle a block it should have removed whole.
RULES: list[tuple[str, re.Pattern[str], int]] = [
    ("config-block",
     re.compile(r"(apiVersion:\s*v1\s*\nkind:\s*Config[\s\S]*?)(?=\n[A-Za-z][\w-]*:\s*(?!\s)|\Z)"), 1),
    ("secret-data-block",
     re.compile(r"(^\s*(?:data|stringData):\s*\n)((?:[ \t]+[\w.\-]+:\s*\S.*\n?)+)", re.M), 2),
    ("bearer", re.compile(r"(?i)(bearer\s+)([A-Za-z0-9._\-]{10,})"), 2),
    # Note the [\w.\-]* prefix: DB_PASSWORD must match. A bare \bpassword
    # does NOT, because '_' is a word character, so there is no boundary
    # after 'DB_'. That near-miss is how real credentials survive a redactor.
    ("password", re.compile(r"(?i)\b([\w.\-]*password)(\s*[:=]\s*\"?)([^\s\"',}]+)"), 3),
    ("token", re.compile(r"(?i)\b([\w.\-]*token)(\s*[:=]\s*\"?)([A-Za-z0-9._\-]{8,})"), 3),
    ("api-key", re.compile(r"(?i)\b([\w.\-]*api[_\-]?key)(\s*[:=]\s*\"?)([^\s\"',}]+)"), 3),
]


def redact(text: str) -> tuple[str, list[tuple[str, int]]]:
    hits: list[tuple[str, int]] = []
    for name, pat, group in RULES:
        def sub(m: re.Match[str]) -> str:
            line = text[:m.start()].count("\n") + 1
            hits.append((name, line))
            # Replace the VALUE, keep the KEY — the field name is diagnostic
            # information and is not the secret.
            return m.group(0)[: m.start(group) - m.start()] + MARK
        text = pat.sub(sub, text)
    return text, hits


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true", help="print only the audit trail")
    a = ap.parse_args()

    clean, hits = redact(sys.stdin.read())
    if not a.report:
        sys.stdout.write(clean)
    for name, line in hits:
        print(f"REDACTED: {name} at line {line}", file=sys.stderr)
    if a.report:
        print(f"\n{len(hits)} removal(s). Reproduce this list in the artifact's"
              f"\nredaction-review block — it is what makes over-redaction"
              f"\ncorrectable instead of silent.", file=sys.stderr)


if __name__ == "__main__":
    main()
