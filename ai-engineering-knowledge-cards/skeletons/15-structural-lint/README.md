# Skeleton — Structural Lint

```
lint.py           six deterministic checks; errors block, warnings inform
knowledge/        a DELIBERATELY BROKEN corpus, so the failure output is visible
lint-state.json   last-run timestamp — created on first run
```

The corpus ships broken on purpose. A linter you have only ever seen pass is a
linter you have not tested.

## Try it

```bash
python3 lint.py                 # exits 1 — four planted defects
python3 lint.py --errors-only
python3 lint.py --base ../13-log-as-source-compilation/knowledge   # exits 0
```

Planted defects, one per check that can fail here: a broken cross-link to a
document that was never written, an index row pointing at a deleted document, a
document missing from the index, and a stub that is an orphan, undersized and
unattributed at once.

The empty-category lines at the end are not failures. They are the curation
signal — in the source system one category held a single document and another
held none, and nobody looked, because the linter ran once and never again.

## What is deliberately missing

**The contradiction check.** Detecting that two documents disagree needs a model
to read the whole corpus. It belongs behind a flag, it costs money per run, and
that is precisely why it is the check that never gets run. Nothing here
implements it.

**Authority.** This reports. It blocks nothing, and it is wired to nothing.
Exiting non-zero only matters if something is reading the exit code — see the
pipeline walkthrough at [`../pipelines/session-memory-loop/`](../pipelines/session-memory-loop/).
