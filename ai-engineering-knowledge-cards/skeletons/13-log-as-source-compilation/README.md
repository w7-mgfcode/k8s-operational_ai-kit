# Skeleton — Log-as-Source Knowledge Compilation

A runnable, offline miniature of the pipeline. Stdlib only, no model calls.

```
SCHEMA.md      the compiler's specification (read into the prompt, not just for humans)
flush.py       append-only capture with a dedup window
compile.py     incremental compiler: hash ledger, cutoff hour, dry-run, status
daily/         SOURCE  — one example session
knowledge/     OUTPUT  — three example articles, index, build log
ledger.json    which source produced which output, at what cost
```

## Try it

```bash
python3 compile.py --status                     # base health; note the empty categories
python3 compile.py --dry-run --ignore-hour      # no-op: every hash matches
echo "a long enough session to clear the floor..." | python3 flush.py
python3 compile.py --dry-run --ignore-hour      # now one source is pending
```

The two dry-runs are the point. Nothing recompiles until a source's content
hash changes, so the expensive stage is driven by content, not by scheduling.

## What is deliberately stubbed

`compile_one()` prints instead of calling a model. Replace it with a real call
and the rest of the machinery is unchanged. When you do, verify the write
permissions with a real unattended run: the source system's first compilation
exited cleanly and wrote nothing, because a headless agent lacked write access.

## What is deliberately missing

No redaction stage sits between `daily/` and the compiler. That gap is faithful
to the source system and is the subject of card 18. Add it before pointing this
at anything real — the source is a raw transcript and contains whatever the
session contained.
