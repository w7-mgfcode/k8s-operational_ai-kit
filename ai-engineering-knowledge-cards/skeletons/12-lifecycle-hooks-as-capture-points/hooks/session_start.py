#!/usr/bin/env python3
"""Session-start injection hook. Reads the small curated memory files and emits
context as JSON on stdout — and NOTHING else on that channel, because the
runtime parses it.

Usage:
    python3 session_start.py
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import log  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUDGET_CHARS = 20_000      # ~2.5% of a 200k window. State the budget as a share.


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8") if p.exists() else ""
    except Exception:
        return ""


def main() -> None:
    start = time.time()
    try:
        parts = []
        for name in ("SOUL.md", "USER.md", "MEMORY.md"):
            body = read(ROOT / "memory" / name).strip()
            if body:
                parts.append(f"## {name[:-3].title()}\n{body}")

        daily = sorted((ROOT / "daily").glob("*.md")) if (ROOT / "daily").exists() else []
        if daily:
            tail = "\n".join(read(daily[-1]).strip().splitlines()[-30:])
            if tail:
                parts.append(f"## Recent Daily Log\n{tail}")

        ctx = "\n\n---\n\n".join(parts)
        if len(ctx) > BUDGET_CHARS:
            ctx = ctx[:BUDGET_CHARS]
            ctx = ctx[:ctx.rfind("\n")]        # truncate at a line boundary

        if not ctx.strip():
            log("session-start", "SKIP", time.time() - start, "empty")
            sys.exit(0)

        # CRITICAL: only valid JSON on stdout. Diagnostics go to stderr.
        json.dump({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": ctx}}, sys.stdout)
        log("session-start", "OK", time.time() - start, f"{len(ctx)} chars")
    except Exception as e:
        log("session-start", "ERROR", time.time() - start, str(e))
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
