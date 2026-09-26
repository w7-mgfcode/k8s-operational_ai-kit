---
component: 02
title: Remediation Ranking Rubric
type: reference
instances:
  - 06-calibrated-degrees-of-freedom
  - 17-blast-radius-gating
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 01-infrastructure-issue-investigator
---

# Remediation Ranking Rubric

> A weighted, seven-criterion scoring sheet that turns "which fix should we do?" into
> arithmetic — exact in its sums, and only as good as the judgement it is fed.

## What it is

A reference file loaded by one phase of a planning skill
([component 01](../skill/01-infrastructure-issue-investigator.md)). It defines how
candidate fixes for an infrastructure incident are scored: seven criteria, each
scored 0, 1 or 2 against written anchors, multiplied by a weight and summed; a
fixed tie-break; one mandated table layout; and a gate after the table. It is about
a hundred lines long and contains no code.

## Trigger and routing

Loaded by the investigator skill in its rank phase, after brainstorming has produced
three to six candidates and before any plan is written. It is never routed to
directly; the skill's reference table names it as the file for that phase and no
other ([card 02](../../cards/02-progressive-disclosure.md) — the rubric costs nothing
until ranking starts).

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Candidate fixes | yes | the brainstorm phase: 3–6 options, each with mechanism, scope, reversibility and the repo artifact it would reuse |
| The infrastructure repository | yes | for reuse, dependencies and existing roles |
| The current branch | yes | for the workstream criterion |
| The agent kit's rule set | yes | for the conventions criterion |

## Procedure

1. Score every candidate on every criterion, 0/1/2, using the anchors:

   | # | Criterion | Weight | 2 means | 0 means |
   |---|---|---|---|---|
   | 1 | Reuse | ×3 | an existing role does it with values changes only | net-new role or bespoke workflow |
   | 2 | Workstream fit | ×2 | on-theme with the current branch | would need a different branch |
   | 3 | Blast radius | ×2 | namespace-scoped, target workload only | cluster-wide: webhook, CRD, global RBAC, node |
   | 4 | Reversibility | ×2 | documented rollback and a meaningful dry run | destructive without a state restore |
   | 5 | Conventions | ×1 | no rule needs an exception | two or more exceptions |
   | 6 | Dependencies | ×1 | only what is already installed | new, niche or unmaintained |
   | 7 | Environment promotion | ×1 | promotes up the ladder with values only | safe in one environment only |

2. Multiply and sum. The maximum is 24.
3. Break ties in criterion order: higher reuse wins, then workstream, then blast
   radius, and so on.
4. Render the result as one fixed table — rank, option, reuse, blast radius,
   reversibility, score on /12 (the /24 total halved), and a reason — in exactly that
   shape.
5. Add a two-sentence rationale for the top option, then ask whether to proceed with
   it or pick another. **Do not continue without an explicit answer.**

## Tools and permissions

None of its own. It is read by the model inside a skill whose permissions it
inherits; scoring it requires reading the repository and the current branch, which
the skill already does read-only.

## Outputs

A ranked table on screen, a rationale, and a question. Nothing is written. The
chosen option is what the skill's plan phase receives.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Fit outranks cause | A fix that buys headroom outranks one that removes the cause | Reuse and workstream carry 5 of the 12 weight points, blast radius and reversibility 4, and nothing scores whether an option addresses the evidence. Structural — shown in the prototype, where adding that one criterion moves the win |
| One weight decides it | The winner changes when a single weight moves by one | Close totals plus a tie-break on the heaviest criterion. Structural: with seven criteria and 0–2 bands, near-ties are common, and the weights were set once, by hand |
| The inputs are unaudited | Two runs on the same evidence can rank differently | Every 0/1/2 is assigned by the model against prose anchors, with no citation required for any score. The arithmetic is exact; its inputs are not |
| The display invents ties | Different totals render as the same /12 score, or a half point appears the layout does not allow | The /12 column halves a /24 total; any odd total becomes a half, and rounding it merges neighbours. Readable directly off the scoring section |
| Conventions measured against the wrong rules | A fix is scored on commit format and test rules while its real constraints are the target repository's own | The conventions criterion reads the agent kit's rule set, not the conventions of the infrastructure repository the fix lands in. Observed in the criterion's own text |
| The example never shows a trade-off | Readers learn the arithmetic but not the tie-break | The rubric's worked example has a winner scoring full marks on all seven criteria; the rule most likely to matter in practice is never exercised |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../cards/06-calibrated-degrees-of-freedom.md) | The model's judgement is narrowed to three anchored bands per criterion, fixed weights, a fixed tie-break and one mandated output shape — freedom removed where consistency matters, left where it cannot be removed (assigning the score) |
| [17 Blast-Radius Gating](../../cards/17-blast-radius-gating.md) | Blast radius is a weighted criterion with three named bands — namespace, shared controller, cluster-wide — applied before any change exists |
| [19 Scope Lock and Checkpoint Delivery](../../cards/19-scope-lock-and-checkpoint-delivery.md) | The rubric ends in a checkpoint: an explicit yes, or another pick, before the plan phase starts |

## Provenance

Instanced in the source system by one reference file of about a hundred lines inside
the investigator skill: seven criterion sections with anchor tables, a scoring
section, a tie-break rule, one worked example, and the mandated display. Its seven
criteria encode the source team's priorities — reuse the existing automation, stay on
the current workstream, keep changes small and reversible — and the weights were set
once, by hand. The component records no calibration: nothing in it says the weights
were tested against past decisions.

## Prototype

Minimal runnable prototype in
[`../../skeletons/components/02-remediation-ranking-rubric/`](../../skeletons/components/02-remediation-ranking-rubric/).
Standard library, offline. It ranks five fabricated fixes, shows what the /12 display
does to them, and with `--stress` perturbs every weight and adds the missing
root-cause criterion.

## What is deliberately missing

**A root-cause criterion.** Nothing in the rubric asks whether an option addresses
the evidence the diagnose phase gathered. The gate after the table is the only
place that question gets asked, and it is asked of a human who has just been shown a
winner.

**Calibration.** The weights are opinions written down once. A rubric used for real
decisions would be replayed against past incidents and their outcomes; this one
never was.

**Evidence per score.** A version that required a one-line citation for each 0/1/2
would make the inputs auditable. The source required none.

**In the prototype:** the scores are fixed in a file rather than assigned by a model,
and the mandated table and rationale are reduced to plain columns.
