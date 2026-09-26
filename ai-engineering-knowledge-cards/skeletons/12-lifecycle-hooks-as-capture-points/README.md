# Skeleton — Lifecycle Hooks as Capture Points

```
hooks/session_start.py   injects memory as JSON — nothing else on stdout
hooks/session_end.py     appends the transcript, exits 0 no matter what
hooks/_shared.py         bounded extraction + a logger that swallows everything
fault_inject.py          proves fail-open by breaking the filesystem calls
memory/                  the small curated files the start hook injects
daily/                   append-only capture lands here (card 13's source)
```

## Try it

```bash
printf 'user: why did monitoring stay green?\nassistant: the workloads keep\ntheir credentials and only fail on restart.\n' | python3 hooks/session_end.py
python3 hooks/session_start.py | head -c 400; echo
python3 fault_inject.py          # must report fail-open holds
cat hooks.log
```

The second run of the same input inside 30 seconds is dropped by the dedup
window — try it twice.

## What is deliberately missing

**Redaction.** Capture is raw by design, which is what makes it reliable and
what makes its output unpublishable. Anything a session contained lands in
`daily/` verbatim. See [card 18](../../cards/18-the-redaction-boundary.md); the
gate belongs between `extract()` and the write.

**A liveness check.** Fail-open means a broken hook is silent, and an empty log
is indistinguishable from a quiet week. Nothing here notices if capture stops.
