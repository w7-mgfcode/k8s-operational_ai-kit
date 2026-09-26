---
paths:
  - "ai-engineering-knowledge-cards/skeletons/**"
---

# The Skeleton Contract

Each card ships a minimal runnable prototype. "Runnable" is a promise to the
reader and is checkable — keep it true.

## Four constraints

1. **Standard library only.** No pip install, no requirements file, no venv.
   Current imports across all skeletons: `argparse hashlib json sys time`,
   `datetime`, `pathlib`. Adding a dependency breaks the promise.
2. **Offline.** No network, no API key, no billing. Model calls are stubbed
   behind a named function that prints instead — see `compile_one()` in
   `13-log-as-source-compilation/compile.py`. Replace the stub and the rest of
   the machinery is unchanged; that is the design.
3. **Runnable as committed.** Example data ships with the skeleton so the
   commands in its README work on a fresh clone with no setup.
4. **Generic.** No domain specifics, no real paths, no real hostnames.
   [`anonymization.md`](anonymization.md) applies to example data too.

## Every skeleton has a README that says three things

What each file is, a `## Try it` block of commands that actually run, and a
`## What is deliberately missing` section. The third is not optional — a gap that
is faithful to the source system is card content, and hiding it turns the
skeleton into a demo. Card 13's skeleton states its missing redaction stage and
points at card 18.

## Verify before committing

Run every command in the skeleton's README and check the exit code:

```bash
cd skeletons/13-log-as-source-compilation
python3 compile.py --status
python3 compile.py --dry-run --ignore-hour     # must exit 0
```

If a skeleton writes state when run, it must be idempotent or clean up after
itself. A skeleton that leaves the working tree dirty is a bug in the skeleton.

The card's Skeleton section links here; keep the directory name and the card
number in sync. See [`cards.md`](cards.md).
