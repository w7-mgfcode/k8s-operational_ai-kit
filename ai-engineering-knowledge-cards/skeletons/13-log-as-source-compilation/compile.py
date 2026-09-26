#!/usr/bin/env python3
"""Incremental compiler: daily/ (source) -> knowledge/ (output).

Stdlib only. The model call is stubbed behind `compile_one()` so the skeleton
runs offline and the incremental machinery — which is the actual pattern — can
be exercised and tested without spending anything.

Usage:
    python3 compile.py --dry-run
    python3 compile.py
    python3 compile.py --all          # ignore hashes, recompile everything
    python3 compile.py --status
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DAILY_DIR = ROOT / "daily"
KNOWLEDGE_DIR = ROOT / "knowledge"
SCHEMA_FILE = ROOT / "SCHEMA.md"
LEDGER_FILE = ROOT / "ledger.json"
INDEX_FILE = KNOWLEDGE_DIR / "index.md"
BUILD_LOG = KNOWLEDGE_DIR / "log.md"

# Compilation is attempted only after this local hour. Most triggers are no-ops.
COMPILE_AFTER_HOUR = 18

CATEGORIES = (
    "runbooks",
    "incidents",
    "decisions",
    "tool-patterns",
    "debugging",
    "connections",
    "answers",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def content_hash(path: Path) -> str:
    """Truncated content hash — the whole basis of incrementality."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_ledger() -> dict:
    if LEDGER_FILE.exists():
        try:
            return json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"compiled": {}, "total_cost": 0.0}


def save_ledger(ledger: dict) -> None:
    LEDGER_FILE.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def list_sources() -> list[Path]:
    return sorted(DAILY_DIR.glob("*.md")) if DAILY_DIR.exists() else []


def list_articles() -> list[Path]:
    out: list[Path] = []
    for category in CATEGORIES:
        out.extend(sorted((KNOWLEDGE_DIR / category).glob("*.md")))
    return out


def pending(ledger: dict, force: bool) -> list[Path]:
    """Sources whose hash differs from the ledger. This is the whole trick."""
    if force:
        return list_sources()
    out = []
    for src in list_sources():
        recorded = ledger["compiled"].get(src.name, {}).get("hash")
        if recorded != content_hash(src):
            out.append(src)
    return out


def build_prompt(source: Path) -> str:
    """Assemble the compiler's specification.

    Three things go in besides the source: the schema (so the output shape is
    specified rather than invented), the current index, and every existing
    article (so 'update rather than duplicate' is an instruction the model can
    actually act on). The last one is what makes cost grow with base size.
    """
    schema = SCHEMA_FILE.read_text(encoding="utf-8") if SCHEMA_FILE.exists() else ""
    index = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
    existing = "\n\n".join(
        f"### {a.relative_to(KNOWLEDGE_DIR)}\n{a.read_text(encoding='utf-8')}"
        for a in list_articles()
    ) or "(no articles yet)"

    return f"""You compile raw session logs into a structured knowledge base.

## Output schema (authoritative)
{schema}

## Current index
{index}

## Existing articles — prefer UPDATING one of these over creating a near-duplicate
{existing}

## Source to compile: {source.name}
{source.read_text(encoding="utf-8")}

## Rules
1. Extract 3-7 distinct knowledge items. Not fewer, not more.
2. Update an existing article when the subject already exists.
3. Cross-link with [[category/slug]]. Put genuinely cross-cutting insight in connections/.
4. Every article needs complete frontmatter and a link back to its source.
5. Update index.md and append a build-log entry.
"""


def compile_one(source: Path, prompt: str) -> float:
    """STUB — replace with a real model call.

    Must write files itself, so whatever runs it needs write permission in an
    unattended context. Verify that with a real headless run: an exit code of 0
    does not prove anything was written.

    Returns cost in USD.
    """
    print(f"  [stub] would compile {source.name} ({len(prompt):,} prompt chars)")
    return 0.0


def append_build_log(source: Path, cost: float) -> None:
    BUILD_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not BUILD_LOG.exists():
        BUILD_LOG.write_text("# Build Log\n\n", encoding="utf-8")
    with BUILD_LOG.open("a", encoding="utf-8") as f:
        f.write(f"## [{now_iso()}] compile | {source.name}\n")
        f.write(f"- Cost: ${cost:.4f}\n")
        f.write("- Articles created: (recorded by the compiler)\n")
        f.write("- Articles updated: (recorded by the compiler)\n\n")


def cmd_status(ledger: dict) -> None:
    sources = list_sources()
    articles = list_articles()
    todo = pending(ledger, force=False)
    print(f"sources:   {len(sources)}")
    print(f"articles:  {len(articles)}")
    print(f"pending:   {len(todo)} {[p.name for p in todo]}")
    print(f"spent:     ${ledger.get('total_cost', 0.0):.2f} cumulative")
    for category in CATEGORIES:
        n = len(list((KNOWLEDGE_DIR / category).glob("*.md")))
        flag = "  <-- empty" if n == 0 else ""
        print(f"  {category:<14} {n}{flag}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="ignore hashes, recompile everything")
    ap.add_argument("--dry-run", action="store_true", help="list what would compile")
    ap.add_argument("--status", action="store_true", help="show base health and stop")
    ap.add_argument("--ignore-hour", action="store_true", help="bypass the cutoff-hour gate")
    args = ap.parse_args()

    ledger = load_ledger()

    if args.status:
        cmd_status(ledger)
        return

    if not args.ignore_hour and datetime.now().hour < COMPILE_AFTER_HOUR:
        print(f"before cutoff hour {COMPILE_AFTER_HOUR}:00 — no-op (use --ignore-hour to override)")
        return

    todo = pending(ledger, args.all)
    if not todo:
        print("nothing to compile — every source hash matches the ledger")
        return

    print(f"{'[dry-run] ' if args.dry_run else ''}{len(todo)} source(s) to compile:")
    for src in todo:
        print(f"  - {src.name}")
    if args.dry_run:
        return

    for src in todo:
        print(f"compiling {src.name}...")
        cost = compile_one(src, build_prompt(src))
        ledger["compiled"][src.name] = {
            "hash": content_hash(src),
            "compiled_at": now_iso(),
            "cost_usd": cost,
        }
        # Cumulative, not the sum of current entries: recompiles are spend too,
        # and hiding that hides the cost of breaking the append-only rule.
        ledger["total_cost"] = ledger.get("total_cost", 0.0) + cost
        save_ledger(ledger)
        append_build_log(src, cost)

    print(f"done. cumulative spend ${ledger['total_cost']:.2f}")


if __name__ == "__main__":
    main()
