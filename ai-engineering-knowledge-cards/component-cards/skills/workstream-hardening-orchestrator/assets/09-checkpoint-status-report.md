---
component: 09
title: Checkpoint Status Report Template
type: asset
instances:
  - 06-calibrated-degrees-of-freedom
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 10-sprint-state-file
---

# Checkpoint Status Report Template

> The form a hardening sprint is delivered in at each checkpoint — five workstream rows,
> three trigger states and the evidence behind them — with a vocabulary narrower than the
> state file it reports on, and nothing that checks it was filled.

## What it is

A Markdown template of about sixty lines that the hardening skill
([component 08](../08-workstream-hardening-orchestrator.md)) fills at checkpoints A, B and C.
It has a header (sprint, date, environment), a status table with one row per workstream, a
table of the three trigger states, a validation-evidence block, open risks, blockers, next
actions, and a next-sprint backlog that applies only at the last checkpoint. It is the
delivery half of [card 19](../../../../cards/19-scope-lock-and-checkpoint-delivery.md): the
document a reader gets instead of a running commentary.

## Trigger and routing

Listed in the skill's template table and named by the quick-win phase ("produce the
checkpoint report") and by the handoff phase, which writes it into the sprint's dated
documentation directory. The handoff phase also runs the state reporter
([component 27](../scripts/27-sprint-state-reporter.md)) with a checkpoint letter, but that
script renders its own table shape, not this template, and ignores the letter — so the
template is filled by the model, with the script's output as one input.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Workstream statuses and validation results | yes | the sprint state file ([component 10](10-sprint-state-file.md)) and the gate runner's JSON |
| Trigger states | yes | the state file's trigger section |
| Lint and syntax-check results | yes | the gate runner |
| Before and after counts for policy violations and benchmark failures | yes | the field scanner and the benchmark parser |
| Open risks, blockers, backlog | yes | the model's judgement over the sprint so far |

## Procedure

1. Fill the header: checkpoint letter, sprint name, date, environment.
2. One row per workstream, A to E: name, status, validation result from a closed list
   (passed, failed, pending), free-text notes.
3. One row per trigger, with a state taken from the list printed in the slot.
4. Evidence: pass or fail for lint and syntax check; secrets-store health stated as "all
   pods healthy or issues", with the pod count written into the line; policy violations and
   benchmark failures as before → after (delta); hygiene items as identified / cleaned.
5. Open risks with severity and mitigation; blockers with what they affect and the action
   needed; a checklist of next actions.
6. At checkpoint C only, the backlog: item, priority, reason deferred.

## Tools and permissions

None. It is text the model fills. Writing the result is part of the skill's handoff phase
and is not confirmed separately.

## Outputs

One Markdown report per checkpoint in the sprint's dated documentation directory, next to
the triage table. It is the only artifact of the sprint written for a reader rather than for
the next phase.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Slots saved unfilled | A delivered report still reads `[status]` or `[before] → [after]` in a row | The template is bracketed placeholders, and nothing checks that all were replaced before the report is written. Structural |
| A trigger state with no slot | The benchmark trigger is `pending_approval` or `deferred` in the state file, and the report's slot offers neither | The template lists three states for that trigger; the state file and the triggers reference allow five. Observed |
| One installation's replica count | The health line asks whether "all" of a fixed number of secrets-store pods are healthy, whatever the cluster runs | The pod count was written into the template text. Observed |
| Script and template diverge | Running the reporter with a checkpoint letter gives the same three tables for A, B and C, with no evidence, risks or blockers | The reporter accepts the letter and never uses it, and its Markdown has none of the template's evidence sections; the template is filled by hand beside it. Observed |
| One result, two places | A workstream row says *passed* while the evidence block shows the syntax check failing | Validation appears once per workstream row and again as evidence, and nothing compares them. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | A fixed shape with closed vocabularies for status, validation and trigger state, and free text only for notes, risks and actions |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | One report per named checkpoint, with a backlog for what did not make the window |

## Provenance

Instanced in the source system by one Markdown file of about sixty lines in the hardening
skill's templates directory: a header, eight sections, and every value a bracketed slot. Its
trigger vocabulary and its pod count were copied from the sprint it was written for. Nothing
in the component records how many reports it produced, or whether any was delivered at the
checkpoint it names.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/09-checkpoint-status-report/`](../../../../skeletons/components/09-checkpoint-status-report/).
Standard library, offline. It renders a shortened template from a fabricated sprint state and,
with `--check`, finds the slots left unfilled, a trigger state the template has no word for,
and a pod count that is not the cluster's.

## What is deliberately missing

**A check before delivery.** Leftover slots, a state outside the vocabulary and a row that
disagrees with the evidence are each a few lines to detect. The source wrote whatever the model
filled in.

**One vocabulary.** Generating the trigger slots from the state file's own list of states would
make the narrow-vocabulary failure impossible.

**Counts from the cluster.** The pod count belongs in the health check's output, not in the
template.

**In the prototype:** no risks, blockers or backlog sections, and no date or letter logic; the
render is printed, not written.
