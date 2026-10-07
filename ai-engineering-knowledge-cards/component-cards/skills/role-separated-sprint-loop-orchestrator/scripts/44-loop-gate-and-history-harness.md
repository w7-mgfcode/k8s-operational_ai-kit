---
component: 44
title: Loop Gate and History Harness
type: script
instances:
  - 11-adversarial-role-separation
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 35-run-outcome-report-template
  - 43-worked-loop-walkthroughs
  - 45-loop-state-recorder
---

# Loop Gate and History Harness

> The script that reports where a sprint loop stands — start, history, and a gate verdict
> over one state file — and whose gate cannot tell a recorded failure from a pass.

## What it is

A standard-library Python script with three subcommands over one JSON state file: `init`
writes a fresh run, `history` prints the recorded entries, and `gate` reports `pass`,
`fail`, `escalate` or `pending` for the active sprint. It is the part of the sprint-loop
skill ([component 32](../32-role-separated-sprint-loop-orchestrator.md)) that its own table
describes as enforcing phase order and iteration caps. Its docstring adds that it reads and
writes state through the state recorder ([component 45](45-loop-state-recorder.md)); it
carries its own copy of the load and save code instead. It has no command that moves a
phase, so the order it claims to enforce is not something it can see.

## Trigger and routing

Executed, never loaded. The skill's entry file lists it in its scripts table with the
purpose "orchestrate sprint loop, enforce phase order and iteration caps", gives a
start-a-workflow command and a view-history command in its quick reference, and never
calls the gate subcommand in its phase text — phase 5 compares scores in prose. The
documented commands pass flags with no subcommand, which the script's parser rejects. The
subcommand form, and the only calls to `gate`, are in the worked walkthroughs
([component 43](../references/43-worked-loop-walkthroughs.md)).

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Subcommand: `init`, `history` or `gate` | yes | the calling phase |
| `--state` path | `history` and `gate` | the calling phase; a path that does not exist is read as an empty run |
| `--task`, `--spec`, `--workspace`, `--max-iterations`, `--output-dir` | `init` only; the task is required, the cap defaults to 3 | the user's request and the plan |
| `--force` | no | the operator, to start over on a run in progress |
| The state file | for `gate` and `history` | written by `init` and by the state recorder |

## Procedure

1. **`init`.** Load the state file in the output directory. If its phase is not the initial
   one and `--force` was not given, print an error document and stop — with exit 0.
   Otherwise overwrite the task, cap and paths, set the phase to planning, and reset the
   sprints and the history to empty. Write atomically: a temporary file in the same
   directory, then a rename.
2. **`history`.** Load the state file and print its history list, or a "no history" message.
3. **`gate`.** Load the state. With no active sprint, print an error and exit 1. With no
   evaluation recorded for the sprint, report `pending`. Otherwise take the latest
   evaluation, read its per-axis list, and set `all_pass` to true when every entry in that
   list has a true `pass` flag. If not all pass and the iteration count has reached the
   cap, report `escalate`; if not all pass, `fail`; otherwise `pass`.
4. Print one JSON document. Every verdict, including `fail` and `escalate`, exits 0.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read the state file | any path given | nothing; a missing path reads as a fresh, empty state |
| Write the state file | `init` only, atomically | the script; `--force` overwrites a run in progress |
| Create the output directory | yes | the script |
| Network, subprocesses, a shell | not used | the script's code has no path to them |
| Phase order | claimed in the skill's table and the docstring | nothing; the script has no transition table and no command that sets a phase |

## Outputs

One JSON document on stdout per call. `init` writes the state file; the other subcommands
write nothing. Exit 0 for every outcome except a gate with no active sprint, which exits 1,
and a parser error, which exits 2. The verdict is in the text, not the exit code.

## Failure modes

Every row is read off the script; the first four were also reproduced by running it.

| Failure | Symptom | Root cause |
|---|---|---|
| A recorded failure passes the gate | After the recorder logs a failed iteration, `gate` prints `pass` and "sprint complete" | The gate reads a per-axis list in the latest evaluation; the recorder writes a result and a scores object and never that list, and the "every entry passes" test over an empty list is true. Observed |
| The flag is trusted over the number | An axis scored below its contract threshold but flagged as passing yields `pass` | The gate takes no contract and compares nothing; it reads a boolean someone else set. Structural |
| A failing verdict exits 0 | A caller that branches on the exit code treats `fail` and `escalate` as success | Only the no-active-sprint path exits non-zero. Observed |
| Refusal exits 0 | `init` on a run in progress prints an error and exits 0 | The function returns the state instead of exiting. Observed |
| Force erases the record | `init --force` leaves an empty history | The reset assigns an empty list, against the skill's rule that history is append-only. Observed |
| A mistyped path is an empty run | `history` on a wrong path reports no entries and no error | Loading returns a fresh state when the file is absent. Observed |
| The documented commands fail | The skill's start and history commands exit 2 with an argument error | The skill documents flags with no subcommand and a `--show-history` flag; the script defines three subcommands and no such flag. Observed |
| Phase order is claimed, not kept | Nothing refuses a phase out of sequence | The script has no command that moves a phase and no transition table; the recorder's check is membership in a list of names. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | The "gate mechanically" step, written as a script — and the card's claim that the gate is arithmetic is the part that does not hold, because the arithmetic is a read of a flag |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | An iteration cap that escalates instead of relaxing the bar, and a history meant to be append-only — undone by the force flag |

## Provenance

Instanced in the source system by one standard-library Python script of about 230 lines in
the skill's scripts directory: three subcommands, a state load and an atomic save, and a
gate check. It carries inline script metadata for a script runner, declaring a minimum
Python version and no dependencies. Nothing in the component records a run of it or what a
gate printed; this card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/44-loop-gate-and-history-harness/`](../../../../skeletons/components/44-loop-gate-and-history-harness/).
Standard library, offline. A fresh harness with the same three subcommands over fabricated
state files; `--audit` runs it in a temporary directory and reports eight findings, from the
recorded failure that passes to the subcommand nothing calls.

## What is deliberately missing

**A gate that compares.** Reading the contract's thresholds and the recorded scores, and
deciding from them, would make the verdict arithmetic. The flag it reads today can be set
by anyone, to anything.

**A verdict in the exit code.** Distinct non-zero codes for `fail`, `escalate` and
`pending` would let a caller branch without parsing text.

**A force that archives.** Starting over could move the old history aside instead of
emptying it.

**In the prototype:** no recorder, no contract and no phase machinery; the state files are
fabricated, and the gate's flaw is reproduced rather than fixed.
