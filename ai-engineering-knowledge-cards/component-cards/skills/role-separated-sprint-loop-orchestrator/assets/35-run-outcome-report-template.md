---
component: 35
title: Run Outcome Report Template
type: asset
instances:
  - 11-adversarial-role-separation
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 44-loop-gate-and-history-harness
  - 45-loop-state-recorder
---

# Run Outcome Report Template

> The document a sprint-loop run ends with — a run status, a table per sprint, metrics — in a
> vocabulary of its own, with figures that nothing in the state records.

## What it is

A Markdown template of about sixty-five lines that the sprint-loop skill
([component 32](../32-role-separated-sprint-loop-orchestrator.md)) fills at the end. It has a
header (completion time, a run status of three values, sprint and iteration totals), a summary
table with one row per sprint, a detail section per sprint — final axis scores against
thresholds, changes made, issues resolved, and for an escalated sprint the unresolved blockers
and a reason — an escalation section, three workflow metrics, and a list of modified files. It
is the delivery document of
[card 19](../../../../cards/19-scope-lock-and-checkpoint-delivery.md), and the owner's last view
of what [card 11](../../../../cards/11-adversarial-role-separation.md)'s loop did.

## Trigger and routing

Named in the skill's template table and in phase 6, on a pass of the last sprint or on
escalation. No script writes it. The state recorder
([component 45](../scripts/45-loop-state-recorder.md)) and the gate-and-history script
([component 44](../scripts/44-loop-gate-and-history-harness.md)) hold what it reports on, and
the model retypes the relevant parts.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Sprint statuses, iteration counts, evaluation history | yes | the state file |
| Final scores and thresholds per sprint | for the detail tables | the last evaluation and the sprint contract |
| Changes made and issues resolved | for the detail sections | the builder's notes and the evaluations |
| Files modified | yes | the builder's notes, per sprint |
| Wall time | "if tracked" | nothing in the skill |

## Procedure

1. Fill the header from the state: totals, then a run status.
2. Fill one table row and one detail section per sprint.
3. For an escalated sprint, list its unresolved blockers and why the cap was reached.
4. Fill the metrics, then the modified-files list.
5. Present it to the owner, with the three options on an escalation.

*Gate:* the owner's decision on an escalation; nothing checks the report itself.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Writing the report | the orchestrating model | nothing — no script, no validator |
| Statuses drawn from the three-word list | required | the template's own placeholder text — prose |
| Metrics computed from the state | implied | nothing; no script computes them |

## Outputs

One Markdown file for the whole run. It is presented to the owner and written without a
separate confirmation.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Five vocabularies for one fact | The run is `passed` in the report, `complete` in the state, `pass` at the gate, `active` in the contract | The report, the state recorder, the gate, and the contract template each define their own word list, with no mapping. Observed |
| A status nothing produces | `partially_passed` is in the template; no state value corresponds to it, and an escalated run with some passes fits it as well as `escalated` | The template defines three statuses and no rule for choosing between them. Observed |
| An override reads as a pass | An accepted-with-open-blockers sprint is reported `passed` | The state records it as an ordinary pass with a free-text note, since it has no status for acceptance ([component 45](../scripts/45-loop-state-recorder.md)). Observed |
| Columns with no source | "Blocking issues resolved" cannot be filled from the state | The state keeps scores and results per iteration, not blocker lists. Observed |
| Metrics nothing records | Wall time is "if tracked" and no script tracks it; "most-iterated axis" needs scores for every iteration, which are optional when an iteration is recorded | The skill lists the metrics; the recorder takes scores as an optional argument and has no end time. Observed |
| Totals retyped by hand | The report's totals can disagree with the state | No script generates it and nothing compares. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | The record of what the loop did — iterations, escalations, unresolved blockers — held for the human who decides |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | One delivery shape at the end of the run, with escalation as an explicit section |

## Provenance

Instanced in the source system by one plain-text template of about sixty-five lines, the
longest of the four in the skill's assets directory. It has a header, a table, a repeating
per-sprint section, an optional escalation section, three metric lines and a file list. Nothing
in the component records how many reports were written. This card claims none.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/35-run-outcome-report-template/`](../../../../skeletons/components/35-run-outcome-report-template/).
Standard library, offline. It renders a shortened report from a fabricated run state and lists
what the form cannot express about that run.

## What is deliberately missing

**A mapping between the vocabularies.** One list of sprint statuses used by all four files would
remove the first two failures; the template alone cannot.

**A status for acceptance.** The owner's third option at the cap — accept the current state —
has no word in the report or the state.

**In the prototype:** the per-sprint detail tables, the escalation section and the file list
are omitted, and the wall time is derived from timestamps, which the source does not do.
