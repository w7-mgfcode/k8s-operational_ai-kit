# Skeleton — Index-Guided Retrieval

```
query.py       reads the index, selects, opens only what it selected
knowledge/     a small indexed corpus (shared shape with card 13's output)
state.json     the query counter — created on first run
```

## Try it

```bash
python3 query.py "which faults only surface on restart?"          # a hit
python3 query.py "why did monitoring stay green?"                 # a miss
python3 query.py "what is the trust chain?" --file-back
python3 query.py --stats
```

The second command finds nothing, and that is the honest demonstration: the
corpus *does* answer that question, in the document about restart-delayed
failures, but the question is phrased in vocabulary the summaries do not use.
Embeddings would have bridged it. This is the trade — inspectability for
recall — and it is worth seeing fail before you adopt it.

Note what the first command prints: **which documents were selected and why.**
That intermediate is readable. It is the thing similarity search cannot give
you, and it is the reason this approach is debuggable at small corpus sizes.

`--file-back` writes the answer into the corpus and adds its index row, so the
base gets better at questions it has already been asked.

## What is deliberately missing

**The model call.** `select()` scores word overlap instead of reasoning over
summaries. Replace it and nothing else changes — but note that the stub's
weakness is the real implementation's weakness too: a document with a lazy
summary is unreachable either way. Retrieval accuracy is set at write time.

**A two-stage selection.** The whole index goes into one step. Past a few
hundred rows that stops fitting, and the next move is category-then-document —
before reaching for embeddings.

**A reason to run.** Nothing triggers this. In the source system that was fatal:
the counter never left zero.
