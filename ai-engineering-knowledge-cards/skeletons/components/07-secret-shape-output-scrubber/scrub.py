#!/usr/bin/env python3
"""Secret-shape output scrubber — ordered patterns, scrubbed text on stdout,
one audit line per hit on stderr. Then a check of what that design gets wrong.

    python3 scrub.py raw.txt           scrub, as the skill pipes every output
    kubectl … | python3 scrub.py       the same, from stdin
    python3 scrub.py --audit raw.txt   compare the result with expect.json

The rules run one after another over the text the previous rule left, which is
the mechanism the component uses. --audit shows four consequences of it:
evidence scrubbed as if it were a secret, secrets that no rule recognises, a
rule that an earlier rule shadows, and audit lines that point at the wrong line.

Exit codes: 0 = scrubbed. 1 = --audit found what the scrubber gets wrong
(the demonstration). 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLACEHOLDER = "[REDACTED]"


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern
    group: int = 0          # the group to replace; 0 replaces the whole match


# Most specific first. Each rule sees the text the rules above it produced.
RULES = (
    # The indented key: value lines under a Secret's data: block. The group
    # takes each line's newline with it, so the block collapses into one token.
    Rule("secret-block", re.compile(r"^(?:data|stringData):[ \t]*\n((?:[ \t]+[\w.-]+:[ \t]*\S.*\n?)+)", re.M), 1),
    Rule("bearer", re.compile(r"(?i)bearer\s+[\w.-]{10,}")),
    # key: value or key=value. "password" matches anywhere in a name; the
    # others need a word boundary, which an underscore prefix does not give.
    Rule("keyword", re.compile(
        r"(?i)(?:password|\b(?:token|secret|credential|api[_-]?key))[ \t]*[:=][ \t]*\"?([^\s\"',}]+)"), 1),
    Rule("long-base64", re.compile(r"(?<=[:=\s\"])([A-Za-z0-9+/]{40,}={0,2})"), 1),
    Rule("hex", re.compile(r"(?<=[:=\s\"])([a-fA-F0-9]{32,})"), 1),
)


@dataclass
class Hit:
    rule: str
    reported: int           # the line the audit log prints
    removed: str            # what was replaced — kept for --audit, never printed


def scrub(text: str) -> tuple[str, list[Hit]]:
    hits: list[Hit] = []
    for rule in RULES:
        current = text

        def replace(m: re.Match, rule: Rule = rule, current: str = current) -> str:
            line = current.count("\n", 0, m.start(rule.group)) + 1
            hits.append(Hit(rule.name, line, m.group(rule.group)))
            start, end = m.span(rule.group)
            return m.string[m.start():start] + PLACEHOLDER + m.string[end:m.end()]

        text = rule.pattern.sub(replace, current)
    return text, hits


def line_of(text: str, needle: str) -> int | None:
    at = text.find(needle)
    return None if at < 0 else text.count("\n", 0, at) + 1


def short(value: str) -> str:
    return value[:4] + "…"


def audit(raw: str) -> int:
    clean, hits = scrub(raw)
    expect = json.loads((HERE / "expect.json").read_text())
    findings = 0

    print("hits, as the stderr audit log reports them")
    print("  rule          reported   actually   removed")
    for h in hits:
        actual = line_of(raw, h.removed)
        what = expect["evidence"].get(h.removed, "secret" if h.rule != "secret-block" else "secret block")
        drift = "" if actual == h.reported else "  line drifted"
        findings += bool(drift)
        print(f"  {h.rule:12}  line {h.reported:<5}  line {actual:<5}  {what}{drift}")

    print("\nsecrets that survived")
    for value, label in expect["secrets"].items():
        where = line_of(clean, value)
        if where:
            findings += 1
            print(f"  {short(value):8} output line {where:<3} {label}")

    print("\nevidence that was scrubbed")
    for value, label in expect["evidence"].items():
        by = next((h.rule for h in hits if h.removed == value), None)
        if by:
            findings += 1
            note = "  (a hex string, removed before the hex rule ran)" if by != "hex" and \
                re.fullmatch(r"[0-9a-f]+", value) else ""
            print(f"  {short(value):8} {label:16} by {by}{note}")

    print(f"\n{findings} findings — every one follows from ordered pattern matching")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="input to scrub (default: stdin)")
    ap.add_argument("--audit", action="store_true", help="compare the result with expect.json")
    a = ap.parse_args()

    try:
        raw = Path(a.file).read_text() if a.file else sys.stdin.read()
    except OSError as exc:
        ap.error(f"cannot read input: {exc}")

    if a.audit:
        return audit(raw)
    clean, hits = scrub(raw)
    sys.stdout.write(clean)
    for h in hits:
        print(f"REDACTED: {h.rule} at line {h.reported}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
