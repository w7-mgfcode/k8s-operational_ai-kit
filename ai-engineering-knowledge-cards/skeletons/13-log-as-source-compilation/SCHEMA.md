# Knowledge Base Schema

This document is not for humans. It is read into the compiler prompt at every
run, so it is the compiler's specification. Changing it changes the build.

## Pipeline

```
daily/       = source    (raw session dumps — append-only, never edited)
model        = compiler  (extracts and organizes)
knowledge/   = output    (structured, cross-linked articles)
context/     = context   (small, hand-written, injected per session)
```

Mutability is the point: source is never edited, output is never hand-authored,
context is never generated.

## Categories

Categories are operational intent, not topic. Topic-based categories collapse
into one bucket when every article is about the same system.

| Category | Holds |
|---|---|
| `runbooks/` | Procedures. What you would hand to someone on call. |
| `incidents/` | Symptom, investigation path, root cause, resolution. |
| `decisions/` | A choice made, the alternatives, and why. |
| `tool-patterns/` | Reusable configuration idioms for a specific tool. |
| `debugging/` | Diagnostic techniques that generalize past one incident. |
| `connections/` | Insight linking 2+ articles that belongs to neither. |
| `answers/` | Questions asked of this base, and the answers, filed back. |

## Article format

```markdown
---
title: "Article title"
category: runbooks|incidents|decisions|tool-patterns|debugging|connections|answers
tags: [tag, tag]
sources: ["daily/YYYY-MM-DD.md"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Article title

Two to four sentences of summary.

## Key points
- Three to five bullets. The essence.

## Details
Commands, configuration, ordered steps.

## Related
- [[category/slug]] — how it connects

## Sources
- [[daily/YYYY-MM-DD.md]]
```

## Index row

```
| [[category/slug]] | category | one-line summary | source | YYYY-MM-DD |
```

## Compilation rules

1. Extract 3-7 distinct items per source file.
2. Prefer updating an existing article over creating a near-duplicate.
3. Cross-reference with `[[category/slug]]`.
4. Write operationally: commands, configs, steps. Not narrative.
5. Complete frontmatter on every article.
6. Every article links back to its source.
7. Update `index.md` and append to `log.md` after every run.
