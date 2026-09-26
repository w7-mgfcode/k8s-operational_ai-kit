#!/usr/bin/env python3
"""Session-end capture hook. Reads a transcript on stdin, appends it to the
day's log, and exits 0 no matter what happens.

Three rules, all visible below: no model call, bounded time, never fail the
session.

Usage:
    echo "...transcript..." | python3 session_end.py [--daily-dir DIR]
"""
from __future__ import annotations
import argparse, json, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import extract, log  # noqa: E402

MIN_TURNS = 2                 # trivial-session floor
DEDUP_WINDOW_SECONDS = 30     # two hooks can fire for one session end


def main() -> None:
    start = time.time()
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("--daily-dir", default=str(Path(__file__).resolve().parent.parent / "daily"))
        args = ap.parse_args()

        daily = Path(args.daily_dir)
        dedup = Path(__file__).resolve().parent.parent / "last-flush.json"

        text = sys.stdin.read()
        content, turns = extract(text)

        if turns < MIN_TURNS:
            log("session-end", "SKIP", time.time() - start, f"<{MIN_TURNS} turns")
            print(f"SKIP: {turns} turns, below floor", file=sys.stderr)
            return

        fp = str(hash(content))
        try:
            prev = json.loads(dedup.read_text(encoding="utf-8"))
            if prev.get("fp") == fp and time.time() - prev.get("ts", 0) < DEDUP_WINDOW_SECONDS:
                log("session-end", "SKIP", time.time() - start, "duplicate")
                print("SKIP: duplicate within dedup window", file=sys.stderr)
                return
        except Exception:
            pass

        daily.mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        path = daily / f"{now:%Y-%m-%d}.md"
        if not path.exists():
            path.write_text(f"# Daily Log: {now:%Y-%m-%d}\n\n## Sessions\n\n", encoding="utf-8")
        with path.open("a", encoding="utf-8") as f:      # append. never "w".
            f.write(f"### Session ({now:%H:%M})\n\n{content}\n\n---\n\n")

        try:
            dedup.write_text(json.dumps({"fp": fp, "ts": time.time()}), encoding="utf-8")
        except Exception:
            pass

        log("session-end", "OK", time.time() - start, f"{len(content)} chars")
        print(f"OK: {len(content)} chars, {turns} turns -> {path.name}", file=sys.stderr)

    except Exception as e:                # fail open. always.
        log("session-end", "ERROR", time.time() - start, str(e))
        print(f"[session-end] suppressed: {e}", file=sys.stderr)
    finally:
        sys.exit(0)                       # the session must not notice


if __name__ == "__main__":
    main()
