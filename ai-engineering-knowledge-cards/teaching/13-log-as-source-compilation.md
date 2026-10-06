---
card: 13
title: Log-as-Source Knowledge Compilation
layer: memory
maturity: partial
source: ../cards/13-log-as-source-compilation.md
---

# Log-as-Source Knowledge Compilation

> Treat raw transcripts as immutable source, the model as a compiler, and the knowledge base as build output — then make the build incremental with a content hash.

**Status:** partial — the redaction gate was never wired in, the read path was built
but never used, and the lint ran once on day one and never again.

## 1. Why

An engineer debugs a hard failure on Tuesday; three weeks later the same symptom
appears elsewhere. Writing the article at the moment of resolution is the obvious fix
and it never happens — the incident is closed and the engineer is tired. **Any design
that depends on discipline at that moment fails.**

**Without it:** operational knowledge decays to zero within weeks.

## 2. Core Idea

Split capture from curation: capture is automatic, cheap and dumb; curation is
explicit, expensive and deferred. Four stages, **four different mutability rules** —
that is the whole pattern.

## 3. Architecture

```
  daily/      SOURCE   append-only, never edited        ◀── hooks (card 12)
      │
      ▼  hash changed AND past cutoff hour?  ──no──▶ no-op
      │  yes
  [model]     COMPILER  reads schema + index + all existing articles
      │
      ▼
  knowledge/  OUTPUT   never hand-authored              ──▶ retrieval (14), lint (15)
      │
  memory/     CONTEXT  never generated, hand-curated

      ⋯ redaction gate (card 18) belongs here — MISSING ⋯
```

## 4. How It Works

1. Append a timestamped block to today's log. Nothing ever rewrites a block.
2. Read the output schema into the compiler prompt — **the schema is the spec**, not human documentation.
3. Compile one source file with the whole existing base in context, so "update, don't duplicate" is an instruction the model can actually obey.
4. Bound extraction to 3–7 items — unbounded, it either summarizes the day or shatters it.
5. Hash each source; recompile only on change, only past a cutoff hour. Most triggers are no-ops.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Append-only source | The only complete record | Nothing accumulates |
| Output schema | The compiler's specification | Every run invents a new article shape |
| Full-base context | Enables update-over-create | Near-duplicates multiply |
| Content-hash ledger | Makes the build incremental | Every trigger recompiles everything, at full cost |
| Redaction gate | Source is a raw transcript | Credentials become durable, cross-linked artifacts |

## 6. Decisions That Matter

- **Categorize by operational intent, not topic** — every article concerns the same platform, so topic buckets collapse into one.
- **Manual invocation over automation** — a run that silently spends money and writes to a knowledge base is worse than one that does not run.
- **Stops paying for itself** when a day's compilation costs more than hand-writing the two articles that day produced.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Defer curation to a compiler | Capture never depends on discipline | The model, not the engineer, decides what mattered |
| Carry the whole base in context | Update-over-create works | Quadratic growth — each article makes every future run dearer |
| Append-only source | Immutable, auditable provenance | Grows without bound; no rotation |

**Most common failure:** the headless run completes, reports its cost, and writes
nothing — it lacked write permission. Exit zero is not proof of output.

## 8. What To Remember

1. Different mutability rules per stage *are* the architecture.
2. The schema is read by the compiler, not just by humans.
3. A content hash is what separates a pipeline from a money fire.
4. Verify unattended writes with a real headless run that produces real files.

## 9. Lecture Cue

- **Start with:** Tuesday's incident, recurring three weeks later.
- **Draw:** the four directories and their mutability rules — one box per stage.
- **Discuss:** deferred curation trades the engineer's judgment for reliability of capture.
- **Name the gap:** the redaction gate was specified and never wired in, so the source
  still holds whatever the sessions held. The taxonomy hardened too — of 64 articles,
  one category holds a single entry, another is empty. The gaps are the interesting part.
- **End with:** capture must be dumb; curation must be explicit.

**Sits between:** card 12 (produces the source) → **this** → card 14 (consumes the index)

---
Source: `../cards/13-log-as-source-compilation.md` · Skeleton: `../skeletons/13-log-as-source-compilation/`
