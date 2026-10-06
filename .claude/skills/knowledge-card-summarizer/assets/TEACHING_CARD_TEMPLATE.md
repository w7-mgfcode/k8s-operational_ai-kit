---
card: NN
title: <same title as the source card>
layer: <same layer>
maturity: <same maturity — never upgrade it>
source: ../cards/NN-<slug>.md
---

# <Concept Name>

> <One sentence a student can quote. What it does, in plain language.>

**Status:** <proven | partial | abandoned — exactly the source's `maturity`. If
partial, the gap in one clause, e.g. "partial: no redaction stage between capture and
compile". If abandoned, what was given up and why, in one clause.>

## 1. Why

<The problem, 2–3 lines. Lead with the source's `Without it:` line — it is already
the sharpest statement of the failure.>

**Without it:** <observable symptom>

## 2. Core Idea

<1–3 short declarative statements. Mechanism, not benefit.>

## 3. Architecture

```
<one diagram: the pattern in its stack, or its control flow — not both>
```

## 4. How It Works

1. <trigger>
2. <what it reads>
3. <what it decides>
4. <what it writes or hands off>

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| … | … | … |

## 6. Decisions That Matter

- **<decision>** — <what it forecloses>
- **<scaling limit>** — <the point where the pattern stops paying for itself>

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| … | … | … |

**Most common failure:** <the one failure mode worth naming out loud>

## 8. What To Remember

1. …
2. …
3. …

<3–5 maximum. One of them carries a mechanical check the reader can run.>

## 9. Lecture Cue

- Start with: <the problem>
- Draw: <the one relationship worth putting on the board>
- Discuss: <the main trade-off>
<if partial:>
- Name the gap: <what was never built, and why that is the interesting part>
<if abandoned:>
- Name the failure: <why the source system could not hold the pattern — that is the lesson>
- End with: <the design principle>

**Related:** card NN — <relationship, from the source's interacts row> · card NN — <…>
<one entry per `related:` slug, all of them; no builds-on order unless the source states one>

---
Source: `../cards/NN-<slug>.md` · Skeleton: `../skeletons/NN-<slug>/`
