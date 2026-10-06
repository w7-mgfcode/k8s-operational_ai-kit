---
component: 14
title: Conditional Sprint Triggers
type: reference
instances:
  - 17-blast-radius-gating
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 10-sprint-state-file
---

# Conditional Sprint Triggers

> Three if-then gates that decide which workstreams may start — documented as state
> machines, stored as free strings, and evaluated by nobody but the model reading them.

## What it is

A reference file the hardening orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)) reads before its
medium-effort phase. It defines three triggers, each a question with a small state
machine: is the unseal-key schema for auto-unseal agreed; is secrets-store TLS stable
after workstream A; do the benchmark's control-plane items conflict with the platform's
direction. For each it lists the states, the action each state requires, how the
question is resolved or evaluated, and the allowed transitions. It also defines the
three delivery checkpoints and the block of the sprint state file
([component 10](../assets/10-sprint-state-file.md)) where trigger states are stored.
About 120 lines.

## Trigger and routing

Loaded on demand in phase 3. The skill tells the model to evaluate the first two
triggers before workstream B and the third before workstream D's control-plane items,
and links this file for "the full state machine". The failure-handling table in the
skill maps three failures back to the three triggers.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Current trigger states | yes | the state file's trigger block |
| Whether the team agreed the unseal-key schema | for trigger 1 | people, outside the skill |
| Secrets-store health over time | for trigger 2 | an operator running generated commands |
| Platform-team response on control-plane items | for trigger 3 | people, outside the skill |

## Procedure

1. **Unseal-key schema.** `resolved` lets workstream B start; `unresolved` pauses B and
   lets C, D and E continue, to be revisited at checkpoint B. Transitions: unresolved
   to resolved or to deferred.
2. **TLS stability.** `pending` while workstream A runs; `stable` once every replica is
   healthy and unsealed, secret sync still works for its consumers, sidecar injection
   still works, the audit log shows no error spike, and all of that has held for
   fifteen minutes; `unstable` means roll A back behind its flag and do not start B.
   Transitions run pending to stable or unstable, unstable back to pending after a
   fix, and stable to unstable on regression.
3. **Platform conflict.** `no_conflict` implements the approved controls; `conflict`
   documents them as deferred with a rationale; `pending_approval` waits while
   non-control-plane items continue.
4. **Checkpoints.** A at end of day one, B at midday day two, C at end of day two, each
   with a list of expected deliverables.
5. **Record** every state change in the state file's trigger block.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Reading and updating trigger states | yes | the skill's instructions |
| Starting workstream B with a trigger unresolved or unstable | no | the skill's instructions only |
| An illegal transition, such as unresolved straight to a TLS state | — | nothing; the state is a free string |
| Declaring TLS stable | after fifteen minutes of health | the operator's judgement; nothing records the window |

## Outputs

None of its own. The states it defines are written into the state file and shown on the
checkpoint report ([component 09](../assets/09-checkpoint-status-report.md)).

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| A decision nobody computes | The status output lists workstream B beside its `unresolved` schema trigger and says nothing about whether B may start | The reference says the status script reads the trigger states to decide which workstreams may proceed; the script only prints them ([component 27](../scripts/27-sprint-state-reporter.md)). Observed |
| Transitions on paper | A trigger moves from `unresolved` to `stable`, or to a misspelled state, and nothing objects | The transitions are documented as text. Trigger states are edited by hand in the state file, and the status script's only update option writes any string into a workstream's status. Observed |
| Stability is a claim | `stable` is recorded with no health evidence and no start time for the fifteen-minute window | The criterion is an operator judgement over generated commands; nothing stores the observations it rests on. Structural |
| States the report cannot show | A platform-conflict trigger in `pending_approval` or `deferred` has no box on the checkpoint report | The report template lists three of the trigger's five states. Observed |
| Dead-end states | A schema agreed after deferral, or a platform approval that arrives, cannot be recorded by any listed transition | The first trigger's transitions end at `deferred`; the third trigger's `pending_approval` has no transition out. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [17 Blast-Radius Gating](../../../../cards/17-blast-radius-gating.md) | The highest-impact workstream may start only after its predecessor is proven stable, with rollback as the defined response to instability |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | Conditions that pause or defer work are decided before the sprint starts, and three named checkpoints carry fixed deliverables |

## Provenance

Instanced in the source system by one reference file of about 120 lines in the skill's
references directory: three trigger definitions with state tables and transition lists,
three checkpoint definitions and the YAML block that stores the states. The same trigger
descriptions are repeated in the state file template and in two scripts that build the
state file. Nothing in the source records how a trigger was evaluated in practice; this
card claims nothing about it.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/14-conditional-sprint-triggers/`](../../../../skeletons/components/14-conditional-sprint-triggers/).
Standard library, offline. It replays a fabricated sprint event log through an explicit
transition table, rejects the illegal transitions, computes which workstreams may start,
and sets that beside a print-only report of the same states.

## What is deliberately missing

**Evaluation.** A trigger is a decision; the source stored its answer and left the
decision to the reader. A function from trigger states to startable workstreams is a few
lines, and is the prototype's main content.

**Transition checks.** A table of allowed transitions, consulted on every update,
rejects the unrecorded jump and the typo alike.

**Evidence for stability.** Recording when the window started and the health
observations taken within it would turn "stable" from a claim into a record.

**In the prototype:** no checkpoints, no state file on disk — the event log is the
state's history, replayed in memory.
