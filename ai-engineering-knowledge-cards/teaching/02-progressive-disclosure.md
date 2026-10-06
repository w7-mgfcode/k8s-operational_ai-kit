---
card: 02
title: Progressive Disclosure
layer: routing
maturity: proven
source: ../cards/02-progressive-disclosure.md
---

# Progressive Disclosure

> Split a capability into three loading levels so context cost scales with what is relevant, not with how much you have installed.

**Status:** proven — applied consistently across the source system's skill layer,
with a validator enforcing the body limit mechanically.

## 1. Why

The context window is a shared resource. A capability that loads entirely whenever
it exists makes every other capability more expensive, used or not.

The obvious failure is cost. The subtler one is worse: past a certain length a model
stops reliably honouring instructions buried mid-document. A rule can be present,
correct, and ignored — and the author's instinct is to add emphasis, which lengthens
the document, which worsens the problem.

**Without it:** instructions are present but not obeyed, and the natural corrective
makes it worse.

## 2. Core Idea

Three levels, three loading rules. Level 3 is effectively unbounded for one reason
worth stating aloud: **a script can be executed without being read**. Its cost is its
output, not its source.

## 3. Architecture

```
  ALWAYS RESIDENT   ┌──────────────────────────┐
                    │ L1  name + description   │  ~100 words · card 03 governs it
                    └───────────┬──────────────┘
                      triggers  │
  ON TRIGGER        ┌───────────▼──────────────┐
                    │ L2  body — procedure only│  < ~5k words
                    └───────────┬──────────────┘
                      calls for │
  ON DEMAND    ┌───────────┬────┴─────┬─────────────┐
               ▼           ▼          ▼             unbounded
         references/    scripts/   assets/
         READ into    EXECUTED,   copied into
          context     never read   the output
```

## 4. How It Works

1. Level 1 carries routing information and nothing else — its only job is deciding whether L2 loads.
2. Level 2 carries procedure: workflow, decision points, gates. Schemas, catalogs and background move down.
3. Split level 3 by **how the file is used**, not by topic — the distinction tells the agent what to *do* with it.
4. A fact lives at exactly one level. Duplication means the body carries weight it does not need, and the copies drift.
5. For a long reference, put grep patterns in the body instead of "read this file."

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| L1 routing contract | Decides whether anything else loads | Perfect structure that never triggers (card 03) |
| L2 body | The procedure itself | — |
| `references/` | Knowledge read on demand | Body bloats back into a monolith |
| `scripts/` | Determinism, executed not read | L3's unbounded budget collapses into L2's cost |
| A *checked* body limit | Limits that are not measured are not limits | Gradual drift back to one big file |

## 6. Decisions That Matter

- **Execution over reading is where the saving actually comes from.** A deterministic check as fifty lines of Python costs its output; the same check as prose costs its full length on every trigger.
- **The split is a guess made early** — deciding what is "procedural" before the capability has been used is guesswork, and moving content between levels later is a real edit.
- **Stops paying for itself** when bodies get so small the indirection outweighs the saving. That means merge the capability into a neighbour, not that the pattern is wrong.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Three levels | Marginal cost of a capability drops sharply | Three places to look; harder to review end to end |
| Scripts executed unread | Cheapest possible level 3 | Opaque — when it misbehaves you must read it after all, at the worst moment |
| Metadata always resident | Routing works without loading anything | A standing tax; at high counts L1 alone is significant |

**Most common failure:** body bloat — reference material added to L2 because it was
convenient, until instructions in its middle stop being honoured.

## 8. What To Remember

1. Cost should scale with relevance, not with installation count.
2. The attentional failure is the real one; the token cost is the visible one.
3. `references` / `scripts` / `assets` splits by *use*, not by subject.
4. Check: every reference file is loaded by some path through the body — unreferenced files are dead weight.

## 9. Lecture Cue

- **Start with:** loading database conventions while editing a stylesheet.
- **Draw:** the three levels with their loading triggers, and thicken the arrow to `scripts/` — that is where the saving lives.
- **Discuss:** the opacity trade — a script you never read is cheapest until it is wrong.
- **Note the observed weakness:** here it was the *reverse* of the usual one. References so thorough that the body became a table of contents — cheap, but the capability could no longer be followed end to end.
- **End with:** at forty capabilities, level 1 is the binding constraint, and the next move is grouping.

**Sits between:** card 03 (governs L1's content) → **this** → card 04 (same principle, triggered by path) · card 06 (decides prose vs script)

---
Source: `../cards/02-progressive-disclosure.md` · Skeleton: `../skeletons/02-progressive-disclosure/`
