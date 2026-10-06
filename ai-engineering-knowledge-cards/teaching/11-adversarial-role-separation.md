---
card: 11
title: Adversarial Role Separation
layer: subagent
maturity: proven
source: ../cards/11-adversarial-role-separation.md
---

# Adversarial Role Separation

> The agent that produced the work cannot be the agent that grades it — and the rubric must be fixed before the work starts, or it will be negotiated afterwards.

**Status:** proven — three role subagents, four supporting scripts, four output
templates. Generator/evaluator separation is established practice; the operational
detail here is the contribution.

## 1. Why

Ask a model to assess its own output and it reports success — not through
dishonesty, but through the mechanism that makes it helpful: it is completing a
document in which its own work is the subject, and the favourable completion fits.

The failure is **specific and catalogable**, which is most of the defence:

| Pattern | What it looks like |
|---|---|
| **Score inflation** | "handles most cases well, 4/5" — where *most* hides that specified cases are unhandled |
| **Hedge-as-pass** | "might need some attention, but the approach is sound" — a blocker disguised as a suggestion |
| **Praise sandwich** | a critical flaw framed between two positives, so attention anchors on the praise |

Each converts a failure into a passing grade while remaining literally accurate.
None is caught by asking the model to be more critical — the instruction and the
behaviour live at different levels.

**Without it:** every sprint passes, quality drifts down invisibly, and the first
real signal is a production defect the evaluation approved.

## 2. Core Idea

Three separations, all required:

**Role** — planner, generator, evaluator; no agent does two. **Context** — the
evaluator runs fresh, so it cannot inherit the generator's reasoning about why a
shortcut was fine. **Temporal** — the contract is written *before* implementation,
because a rubric agreed afterwards is shaped by the result.

## 3. Architecture

```
  request
     │
     ▼
 ┌─────────┐  spec + sprints   ┌──────────┐
 │ PLANNER │ ────────────────▶ │ CONTRACT │  axes · thresholds · OUT-OF-SCOPE
 └─────────┘                   └────┬─────┘  ← frozen BEFORE implementation
      ┌─────────────────────────────┤
      ▼                             ▼
 ┌───────────┐  code         ┌────────────┐
 │ GENERATOR │ ────────────▶ │ EVALUATOR  │  fresh context · flaw-first
 └─────▲─────┘               └──────┬─────┘
       │  delta report          ┌───▼───┐
       └──────────────────────  │ GATE  │──▶ pass: next sprint
              fail              └───────┘    repeated fail: ESCALATE
```

## 4. How It Works

1. Planner produces spec, sprints and acceptance targets — it neither implements nor evaluates. A human approves before anything is built.
2. Contract per sprint: 3–7 axes with thresholds **and an out-of-scope list**, which stops the evaluator expanding the target after seeing the work.
3. Generator implements and reports what it did. **It does not self-score** — removing the step removes the opportunity.
4. Evaluator loads the anti-sycophancy catalog, scores each axis, cites locations. The instruction is not "be harsh" but *"report the gap, not the intention."*
5. The gate is **arithmetic, not judgment** — which is what stops a failure being argued away.
6. Cap the iterations and escalate to a human. Never lower a threshold to pass.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Real context isolation | Evaluator cannot inherit rationalisations | Separation in name only |
| Contract frozen pre-implementation | Rubric cannot be shaped by the result | The bar moves to where the work landed |
| Out-of-scope list | Controls evaluation creep *and* gold-plating | Evaluator invents criteria; generator over-builds |
| Named failure catalog | Sycophancy must be recognisable | "Be critical" yields politeness with harsher adjectives |
| Iteration cap + escalation | Loops do not terminate on their own | Infinite retry, or silent threshold erosion |

## 6. Decisions That Matter

- **The evaluation is itself validated.** A script checks that every axis was scored and that blocking issues exist wherever a score is below threshold — so an evasive or malformed evaluation is detected rather than accepted.
- **Evaluation is deliberately low-freedom** (card 06) — a fixed rubric — because judgment is the unreliable part.
- **Grows more valuable as work gets harder to reverse**; stops paying on small reversible changes. Same calculus as card 17.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Three separate agents | Independence is structural, not requested | Planning pass + contract + evaluation per iteration; for a small change this exceeds the change |
| Flaw-first evaluator | Finds what a cooperative reviewer won't | Overcorrects — a suite of trivial blockers wastes as much time as a rubber stamp |
| Fixed thresholds | Cannot be argued away | Arbitrary at first; the early sprints mostly calibrate them |

**Most common failure:** role collapse — the loop stalls, and letting the generator
"just address the feedback directly" quietly restores self-assessment.

## 8. What To Remember

1. Self-assessment fails structurally, not morally — remove the opportunity, don't request honesty.
2. A rubric written after the work is a rubric shaped by the work.
3. The out-of-scope list protects both directions.
4. Check: nothing passes by narrative — the gate is arithmetic, and no path lowers a threshold.

## 9. Lecture Cue

- **Start with:** "handles most cases well, 4/5" — and ask what *most* is hiding.
- **Draw:** the three roles with the contract above them, and the escalation arrow that does **not** loop back.
- **Discuss:** anything unmeasured is unprotected. An evaluator scoring five axes is blind to the sixth.
- **Point at the best artifact:** the anti-sycophancy reference — named patterns, each with *what it looks like / why it fails / correct behaviour*, read before every evaluation. It opens by stating evaluator sycophancy is the single largest threat to the workflow's integrity. **That is the correct assessment: every other part of the machinery exists to make that one failure detectable.**
- **End with:** the accumulated evaluation history is the real artifact — it shows which axes repeatedly fail, which is information about the generator, not about any sprint.

**Sits between:** card 07 (its strongest case for subagents) → **this** → card 19 (same principle, operational) · card 10 (both refuse self-assessment)

---
Source: `../cards/11-adversarial-role-separation.md` · Skeleton: `../skeletons/11-adversarial-role-separation/`
