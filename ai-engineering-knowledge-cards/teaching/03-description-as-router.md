---
card: 03
title: Description-as-Router
layer: routing
maturity: proven
source: ../cards/03-description-as-router.md
---

# Description-as-Router

> The `description` field is not documentation — it is the routing table, and the only part of a skill the model sees before deciding whether to load it.

**Status:** proven — roughly a dozen skills follow the same shape, with a trigger
harness replaying recorded prompts to assert which one fired.

## 1. Why

Past about five skills, descriptions begin to overlap. Two that both mention
"Kubernetes troubleshooting" compete for the same requests, and the model picks
between them on wording accidents.

**The author cannot see this happening.** The skill that should have fired simply
doesn't, and the session proceeds with a generic answer that looks plausible.

**Without it:** the wrong skill fires on ambiguous phrasing, or none fires, and
neither failure announces itself. The author finds out weeks later, when the agent
answers generically a question a skill was built for.

## 2. Core Idea

Treat the field as a **routing contract with three obligatory parts**: a capability
statement, a positive trigger list, and an exclusion list that **names the sibling to
use instead**.

Marketing copy ("helps you work with Kubernetes") routes badly. A contract routes
correctly and — more importantly — *declines* correctly.

## 3. Architecture

```
       user request
            │
 ┌──────────▼────────────┐
 │  ROUTING LAYER        │  name + description of EVERY installed skill
 │  (this card)          │  always resident · ~100 words each
 └──────────┬────────────┘
            │ selects at most one
 ┌──────────▼────────────┐
 │  SKILL BODY           │  loaded only after selection (card 02)
 └──────────┬────────────┘
 ┌──────────▼────────────┐
 │  BUNDLED RESOURCES    │  loaded or executed on demand
 └───────────────────────┘
```

## 4. How It Works

1. State the capability first, third person. The verb matters — *investigates*, *orchestrates*, *diagnoses* each imply a different output shape.
2. List positive triggers as **real user phrasings**, not keywords — five to eight sentences someone would actually type, harvested from real use.
3. List exclusions, **each naming the alternative**. The valuable ones are the near-misses: the neighbouring skill, not the obviously unrelated task.
4. Disambiguate homonyms outright — a product name that is also a common word will capture the wrong domain silently.
5. Declare autonomy and invocation mode in the same field, so expectation is set *before* the skill loads.
6. Verify empirically (card 10) — this is a prediction about model behaviour, not a property of the text.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| A length budget (~1024 chars) | Forces density; every clause competes | Long prose dilutes the trigger signal, reads as boilerplate |
| Knowledge of siblings | Exclusions must name real alternatives | Vague disclaimers that route nothing |
| A mechanical validator | Checks length, person, presence of both lists | Contracts drift into prose as the set grows |
| A behavioural harness | The only real verification | Collisions found by accident, in production |

## 6. Decisions That Matter

- **The exclusion list is what makes the boundary machine-readable.** *"Do NOT use for: tracing-backend-specific symptoms (use the tracing-backend doctor)"* is not politeness — it hands the router a disambiguation rule it could not otherwise infer.
- **Density over readability is correct here.** The field is optimised for a model's selection decision, not for a human browsing a catalogue. Human-facing explanation belongs in the card, not the field.
- **Stops scaling** when you can no longer write a new skill's exclusion list without re-reading every existing description. Then group, or retrieve candidates instead of loading all of them.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Always-resident routing table | Selection needs nothing loaded | Twenty skills is a permanent tax on every request |
| Exclusions naming siblings | Precise, machine-readable boundaries | Couples skills together — renaming one silently invalidates another's exclusion, and nothing enforces it |
| Triggers harvested from real use | Accurate phrasings | Encode one person's idiom; weaker for everyone else |

**Most common failure:** the silent non-trigger — the agent answers generically and
the user never learns a skill existed, because triggers were written as keywords
rather than as sentences someone would type.

## 8. What To Remember

1. The description is the only thing the router sees. Everything else is invisible until it fires.
2. Declining correctly matters as much as firing correctly.
3. At fifteen skills the cost of a new skill is no longer local — you must edit its neighbours.
4. Check: no two skills share a trigger phrase; overlapping domains name each other in exclusions.

## 9. Lecture Cue

- **Start with:** two skills that both say "Kubernetes troubleshooting", and a coin flip the author cannot observe.
- **Draw:** the routing layer above the body — and emphasise that everything below the first box is invisible at decision time.
- **Discuss:** referential integrity. The routing table has it; nothing enforces it. Ask what breaks when a skill is renamed.
- **Use the homonym example:** a skill diagnosing a distributed-tracing backend whose name is also a common word for a time-tracking app. Its description says so outright, because homonym collisions are invisible until someone asks about the other meaning.
- **End with:** the description is a prediction about model behaviour, so it is only verified by running prompts (card 10).

**Sits between:** card 02 (this is its level 1) · card 07 (skills route by description, commands by name) → **this** → card 10 (the only real verification)

---
Source: `../cards/03-description-as-router.md` · Skeleton: `../skeletons/03-description-as-router/`
