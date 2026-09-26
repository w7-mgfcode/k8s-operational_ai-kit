# Pipeline — The Session-Memory Loop

Cards [12](../../../cards/12-lifecycle-hooks-as-capture-points.md),
[13](../../../cards/13-log-as-source-compilation.md),
[14](../../../cards/14-index-guided-retrieval.md) and
[15](../../../cards/15-structural-lint.md) are usually read as four patterns. They
are one engine, and the engine is the point.

```
   session boundary
         │
    [12] capture          automatic, fail-open, deliberately stupid
         │  append-only
         ▼
    [13] compile          explicit, expensive, hash-gated
         │  categorized, cross-linked, indexed
         ▼
    [14] retrieve         index-guided, no embeddings
         │  answers filed back ──┐
         ▼                       │
    [15] lint                    │ a filed answer becomes
         │  relationships intact │ source for the next compile
         └───────────────────────┘
```

## The design argument

Each stage exists because the one before it has a property the next must not
inherit.

**Capture must be dumb** so it can be automatic and never break a session. That
makes its output raw, redundant and unusable as knowledge.

**Compilation must be smart** to turn that into knowledge, which makes it slow and
expensive — so it cannot sit on the session boundary. It is gated on a content hash
and a cutoff hour, so most triggers do nothing.

**Retrieval must be cheap** or it will not be used. It reads the index compilation
produced rather than the corpus, which is only possible because compilation wrote
real summaries.

**Lint must need nothing** — no model, no network, no cost — because it is the only
stage with no intrinsic motivation to run. Its checks protect the relationships the
other three depend on.

The asymmetry to notice: stages 12 and 13 ran daily in the source system because
they were triggered automatically. Stages 14 and 15 were built just as carefully
and effectively never ran, because they required a person to decide to run them.
In a single-operator system, **automatic and never are the only two stable
frequencies.**

## Try it

```bash
./walkthrough.sh          # all four stages in order
./walkthrough.sh 13       # one stage
```

Each stage shells out to that card's own skeleton, unchanged. Nothing is
reimplemented here.

## What is deliberately missing

**The redaction gate.** Nothing sits between capture and compilation, so raw
transcript content reaches durable artifacts unscrubbed. This is faithful to the
source system, where the gate existed in a different subsystem and was never
carried across — see [card 18](../../../cards/18-the-redaction-boundary.md). Add it at
stage 12's output before pointing any of this at real sessions.

**A trigger for stages 14 and 15.** The walkthrough runs them because the script
says to. Nothing in the engine makes them run on their own, which is exactly why
they did not, and the honest version of this pipeline wires lint to fire after
every compile.
