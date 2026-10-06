#!/usr/bin/env python3
"""PreToolUse guard for Bash: .legacy-assets/ is readable, never written.

The Edit deny rule in .claude/settings.json covers Claude Code's own file
tools, not shell commands. This hook closes the obvious shell paths: a
redirect into the tree, a write, move or delete verb naming it, `git add`
and friends, `git clean -x`, and any of those run from inside the tree.

It matches command text, not effects. A script that opens a file there
itself passes. See .claude/rules/permissions.md.

Exit 2 blocks the command and shows stderr to the agent. Malformed input
exits 0: a broken guard must not block every shell command.
"""

from __future__ import annotations

import json
import re
import sys

TREE = re.compile(r"\.legacy-assets(?:/|\b)")
# Verbs that change whatever path they are given.
WRITERS = re.compile(r"(?:^|\s)(?:rm|rmdir|mv|touch|mkdir|ln|chmod|chown|truncate|tee|unzip|patch)\s")
IN_PLACE = re.compile(r"(?:^|\s)(?:sed|perl)\s(?:[^|]*\s)?-\w*i")
GIT_WRITE = re.compile(r"(?:^|\s)git\s(?:.*\s)?(?:add|rm|mv|restore|checkout)\s")
GIT_CLEAN_IGNORED = re.compile(r"(?:^|\s)git\s+clean\s(?:.*\s)?-\w*[xX]")
REDIRECT = re.compile(r"(?<![0-9&])>>?\s*([^\s&|;]+)")
COPY = re.compile(r"(?:^|\s)cp\s.*\s(\S+)\s*$")


def into_tree(target: str, inside: bool) -> bool:
    """A write target lands in the tree if it names it, or is relative while the
    command runs inside it."""
    if TREE.search(target):
        return True
    return inside and not target.startswith(("/", "~", "&"))


def reason(command: str, cwd: str) -> str | None:
    if GIT_CLEAN_IGNORED.search(command):
        return "git clean -x/-X deletes ignored files, and .legacy-assets/ is ignored"
    inside = bool(re.search(r"/\.legacy-assets(?:/|$)", cwd)) or \
        bool(re.search(r"(?:^|\s)cd\s+\S*\.legacy-assets", command))
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        segment = segment.strip()
        for m in REDIRECT.finditer(segment):
            if m.group(1) != "/dev/null" and into_tree(m.group(1), inside):
                return f"redirect into .legacy-assets/: {segment}"
        if WRITERS.search(segment) or IN_PLACE.search(segment) or GIT_WRITE.search(segment):
            if TREE.search(segment) or inside:
                return f"writes, moves, deletes or stages under .legacy-assets/: {segment}"
        copy = COPY.search(segment)
        if copy and into_tree(copy.group(1), inside):
            return f"copies into .legacy-assets/: {segment}"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload["tool_input"]["command"]
        cwd = payload.get("cwd", "")
    except (ValueError, KeyError, TypeError):
        return 0
    why = reason(command, cwd)
    if why:
        print(f"Blocked: .legacy-assets/ may be read, never written or tracked. {why}",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
