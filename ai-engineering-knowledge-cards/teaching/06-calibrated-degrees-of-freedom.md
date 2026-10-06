---
card: 06
title: Calibrated Degrees of Freedom
layer: skill
maturity: proven
source: ../cards/06-calibrated-degrees-of-freedom.md
---

# Calibrated Degrees of Freedom

> Match how specifically you instruct to how fragile the task is: prose where many routes are valid, a script where one wrong step is expensive.

**Status:** proven — inherited from published authoring guidance rather than
invented. The source system's contribution was applying the calculus to
infrastructure work, where a wrong variant costs an outage rather than a retry.

## 1. Why

Both extremes fail, and each looks like the opposite problem.

**Over-constrain** a task needing judgment and the agent follows the script off a
cliff — the procedure does not fit, but it is what the instructions said, so it runs
and the mismatch is reported as success.

**Under-constrain** a fragile task and the agent improvises a plausible variant each
time. Usually fine; occasionally catastrophic. This is the dangerous one, because the
variance is invisible until it isn't: an agent that builds a slightly different
command each run works until the day it builds a destructive one.

**Without it:** fragile steps drift between runs and flexible steps are executed
rigidly — and both look correct from inside the session.

## 2. Core Idea

Three levels, chosen **per step, not per capability**:

| Freedom | Form | Use when |
|---|---|---|
| High | Prose, heuristics | Several approaches valid; the right one depends on unpredictable context |
| Medium | Template, pseudocode | A preferred pattern exists, variation acceptable |
| Low | A script, few parameters | Fragile, or the sequence must not vary |

Terrain, not policy: an open field admits many routes; a narrow bridge over a drop
needs guardrails.

## 3. Architecture

```
  within ONE capability
  ──────────────────────────────────────────────────
  1  scope / intake        HIGH    prose
  2  analysis              HIGH    heuristics + reference
  3  transformation        MEDIUM  template + parameters
  4  validation            LOW     script, fixed flags
  5  packaging             LOW     script, refuses on failure
  ──────────────────────────────────────────────────
     freedom decreases as consequence increases
```

## 4. How It Works

1. Judge the **task**, not the skill — assigning one level to a whole capability is the commonest way to get this wrong.
2. Ask what a wrong variant costs. Cheap and visible tolerates freedom; expensive or silent demands a script.
3. **Repeated regeneration is the signal.** If the agent writes the same twenty lines every run, those lines are a file.
4. Use templates where the reader will compare output across runs: reports, briefs, plans.
5. Leave open steps genuinely open, and say so — otherwise an agent optimising for compliance invents a rigidity nobody intended.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Honest failure-cost estimate | The whole calibration rests on it | Uniform freedom; wrong in both directions |
| A runtime that executes scripts unread | Low freedom is only cheap if so | Scripts become prose, losing determinism and costing context |
| Willingness to write code in a capability | Low freedom means real error handling | Fragile steps stay prose because prose is faster to write |
| Feedback from real runs | Calibration is empirical | Day-one guess persists forever |

## 6. Decisions That Matter

- **Freedom is assigned per step.** Intake wants prose; packaging wants a script. Most capabilities legitimately mix all three.
- **Prescriptive prose is the worst of both** — it constrains without guaranteeing, and is partially ignored.
- **Stops paying for itself** when scripts outgrow maintenance. A capability with nine scripts has a software project inside it, and each one then needs tests, an owner, and a reason to still exist.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Script the fragile step | Determinism; no drift between runs | Cannot adapt — the rigidity preventing drift also prevents recovery |
| Prose the open step | Adapts to context the author could not predict | Silent variance if the step was actually fragile |
| Scripts executed unread | Cheap and deterministic | They are code: they break on environment change, and you must read them exactly when they misbehave |

**Most common failure:** regenerated boilerplate — the same code appears in
transcript after transcript, and the signal to write a script went unacted on.

## 8. What To Remember

1. Calibrate per step; one level per capability is the standard mistake.
2. Cost of a wrong variant sets the level — the same calculus as blast radius (card 17).
3. Repeated regeneration is the clearest signal a script is owed.
4. Check: every destructive or irreversible step is low freedom and scripted.

## 9. Lecture Cue

- **Start with:** the agent that constructs a slightly different command each run — fine, fine, fine, destructive.
- **Draw:** the five-phase gradient, freedom falling as consequence rises.
- **Discuss:** prescriptive prose, and why it is worse than either extreme.
- **Point at the evidence:** the source system's skill-building pipeline is the clean instance — creation from a template, validation by a script with fixed checks, packaging by a script that *refuses to run on a failed validation*. Its operational skills show the same gradient for a different reason: investigation is prose because symptoms vary; anything touching a live cluster is a fixed command with fixed flags.
- **End with:** calibration is empirical — revise it after real runs, not before.

**Sits between:** card 02 (decides what L3 material should be) → **this** → card 09 (its clearest instance) · card 17 (same calculus, infrastructure)

---
Source: `../cards/06-calibrated-degrees-of-freedom.md` · Skeleton: `../skeletons/06-calibrated-degrees-of-freedom/`
