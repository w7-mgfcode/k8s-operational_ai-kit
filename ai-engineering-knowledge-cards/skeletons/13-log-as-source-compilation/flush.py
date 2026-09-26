#!/usr/bin/env python3
"""Append-only capture: session context -> daily/<date>.md.

Stdlib only. Never rewrites an existing block — the source is append-only by
construction, which is what makes the compiler's content hash meaningful.

Usage:
    echo "session text" | python3 flush.py
    python3 flush.py --context-file ctx.md
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DAILY_DIR = ROOT / "daily"
DEDUP_FILE = ROOT / "last-flush.json"
DEDUP_WINDOW_SECONDS = 30
MIN_CHARS_TO_FLUSH = 200  # skip trivial sessions


def is_duplicate(fingerprint: str) -> bool:
    """Two hooks can fire for one session end. Drop the second."""
    try:
        state = json.loads(DEDUP_FILE.read_text(encoding="utf-8"))
        if state.get("fingerprint") == fingerprint:
            return time.time() - state.get("timestamp", 0) < DEDUP_WINDOW_SECONDS
    except Exception:
        pass
    return False


def record(fingerprint: str) -> None:
    try:
        DEDUP_FILE.write_text(
            json.dumps({"fingerprint": fingerprint, "timestamp": time.time()}),
            encoding="utf-8",
        )
    except Exception:
        pass  # capture must never fail the session


def append(content: str) -> Path:
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    log = DAILY_DIR / f"{now:%Y-%m-%d}.md"
    if not log.exists():
        log.write_text(f"# Daily Log: {now:%Y-%m-%d}\n\n## Sessions\n\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:  # append. never "w".
        f.write(f"### Session ({now:%H:%M})\n\n{content}\n\n---\n\n")
    return log


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--context-file", help="file to flush (default: stdin)")
    args = ap.parse_args()

    text = (Path(args.context_file).read_text(encoding="utf-8")
            if args.context_file else sys.stdin.read()).strip()

    if len(text) < MIN_CHARS_TO_FLUSH:
        print(f"SKIP: under {MIN_CHARS_TO_FLUSH} chars", file=sys.stderr)
        return

    fingerprint = str(hash(text))
    if is_duplicate(fingerprint):
        print("SKIP: duplicate within dedup window", file=sys.stderr)
        return

    log = append(text)
    record(fingerprint)
    print(f"OK: {len(text)} chars -> {log.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
