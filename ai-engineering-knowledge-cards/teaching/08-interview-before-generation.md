---
card: 08
title: Interview Before Generation
layer: skill
maturity: proven
source: ../cards/08-interview-before-generation.md
---

# Interview Before Generation

> Do not generate from a one-line request. Elicit the specification first, through a structured interview that knows which questions are mandatory at this complexity and which can be defaulted.

**Status:** proven — instanced end to end: eight brief sections, three personas, a
three-tier model, a fast path, and a validation script gating the handoff.

## 1. Why

Every build request arrives underspecified, and not through any fault of the
requester. They know what they want the thing to *do*; they have not thought about
its failure modes, its boundaries, or what it must refuse.

**Generation is cheap and revision is not.** A generated artifact carries an
authority its specification never had — once it exists as a file, subsequent work
edits it rather than asking whether it should have been built that way.

Nobody opens with *"and it must never run against production."* That requirement
exists, fully formed, and surfaces only when asked.

**Without it:** the first generated version defines the design, its unstated
constraints are discovered by violation, and each revision costs more than the
interview would have.

## 2. Core Idea

Insert elicitation between request and generation, with four properties that make it
more than "asking some questions":

**Fixed section model** (completeness is checkable, not a feeling) · **role-based
questioning** (a workflow designer and a safety reviewer ask different things) ·
**complexity tiering** (don't interrogate a simple thing) · **explicit defaulting**
(the user is told which defaults were applied).

## 3. Architecture

```
  raw request ──▶  INTERVIEW  ──▶  brief  ──▶  GENERATION ──▶ artifact
                       │                        (card 09)
        ┌──────────────┴──────────────┐
        │ domain analyst   identity, triggers, boundaries
        │ workflow architect  phases, tools, outputs
        │ safety auditor   constraints, restricted paths
        └──────────────┬──────────────┘
                       ▼
             COMPLETENESS GATE — a script, not a judgment
             required sections filled for the estimated tier
```

## 4. How It Works

1. Accept any input shape — sentence, URL, keyword, partial brief. The entry point is exactly where variation is expected (card 06).
2. Record the raw idea **verbatim before interpreting**; the requester's framing often carries the real requirement.
3. Pre-fill from any supplied source. Every pre-filled field is one fewer question.
4. Estimate a tier from signals, not by asking. The tier decides which sections are required, optional or defaulted.
5. Switch persona by section; ask **2–4 questions per exchange, each with a reason**.
6. Fast path for partial briefs: report what was found, ask only about gaps.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Fixed section model | Makes completeness checkable | "Enough information" becomes a judgment, made optimistically |
| Tier rules | Stops simple things being interrogated | Uniform questioning; users abandon |
| Completeness validator | Human judgment here is unreliable | Briefs pass with critical sections empty |
| Explicit default reporting | Silent defaults look like decisions | Assumptions discovered after generation |
| A generator that consumes the brief | The brief is an input format, not a document | An elaborate interview producing a file nobody reads |

## 6. Decisions That Matter

- **The tier table is the load-bearing part.** It states per section and tier whether a field is required, optional, defaulted or recommended — and defines each term precisely. That precision is what lets a *script* decide completeness instead of a person.
- **Defaults are decisions.** Tier-appropriate defaults are still choices made by the system, and announcing one does not mean it was read.
- **Stops paying for itself** when artifacts get small enough that generating and discarding beats specifying. Then shrink the interview to the two or three questions whose answers cannot be guessed.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Interview before generating | Catches constraints nobody volunteers | Costs time up front, and its benefit is invisible — the bad artifact that was never generated leaves no trace |
| Three personas | Genuinely different notions of sufficiency | Become theatre if all three ask similar questions in different voices |
| Estimate tier early | Avoids over-questioning | Estimated when the least is known; a misjudged tier defaults a safety section that needed real answers |

**Most common failure:** interview fatigue — too many questions per exchange, no
reason given for any of them, so the user abandons or answers perfunctorily.

## 8. What To Remember

1. Requesters do not volunteer constraints; the safety section exists to ask.
2. Completeness must be decided by a script, because optimism is the default human answer.
3. Never re-ask what was already supplied — that is the fastest way to lose engagement.
4. Check: every applied default is named to the user *before* generation.

## 9. Lecture Cue

- **Start with:** "and it must never run against production" — a requirement that exists fully formed and will never be volunteered.
- **Draw:** request → interview → brief → generation, and put the completeness gate on the arrow as a script.
- **Discuss:** the brief is a second artifact. When the generated thing changes, its brief is stale immediately and nothing keeps them in sync — is that acceptable?
- **Note the maturity curve:** early, the interview teaches the requester what specification means. Later they internalise the section model and the fast path becomes the main path. **The safety section is the part nobody ever internalises** — which is why it stays mandatory.
- **End with:** generation is cheap, revision is not, and a file argues for itself.

**Sits between:** *(front end)* → **this** → card 09 (consumes the brief) · card 19 (same move, applied to execution)

---
Source: `../cards/08-interview-before-generation.md` · Skeleton: `../skeletons/08-interview-before-generation/`
