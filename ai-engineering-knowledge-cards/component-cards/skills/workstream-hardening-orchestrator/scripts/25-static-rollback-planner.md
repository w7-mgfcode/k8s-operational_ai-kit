---
component: 25
title: Static Rollback Planner
type: script
instances:
  - 16-the-permission-ladder
  - 17-blast-radius-gating
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 10-sprint-state-file
  - 20-secrets-store-tls-unseal-guide
---

# Static Rollback Planner

> Prints a fixed rollback recipe per workstream. The recipe is the same whatever was
> changed, and its git commands restore one file while discarding uncommitted work.

## What it is

A standard-library Python script that prints a rollback plan for one of the sprint's
five workstreams: a trigger, ordered steps, operator commands for the cluster and git
commands. The plans are a constant table in the script, one entry per workstream.
From the sprint state file ([component 10](../assets/10-sprint-state-file.md)) it
reads only the workstream's status and whether the sprint has cluster access. Its
docstring says it generates rollback steps "based on what was changed"; nothing in
it looks at a change.

## Trigger and routing

It is executed, not routed, and in practice it is barely reached. The orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)) lists it in its scripts
table and its quick reference ("before risky changes"). No phase runs it. The entry
file's failure table answers an unstable TLS rollout with "roll back" and names no
script; the TLS guide ([component 20](../references/20-secrets-store-tls-unseal-guide.md))
carries its own rollback steps in prose.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Workstream, A to E | yes | the model |
| Sprint state file path | yes | [component 10](../assets/10-sprint-state-file.md); read for status and the cluster flag only |
| Output path | no | stdout when absent |

## Procedure

1. Look up the workstream's fixed plan.
2. Load the state file as YAML if a YAML library is importable, else as JSON. On a
   missing file, fall back to status "unknown" and no cluster access.
3. Emit the trigger, the current status and the steps. Add the cluster commands only
   with cluster access, otherwise a note to roll back at the git level. Always add
   the git commands.
4. Print the JSON, or write it to the output path.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read the state file | yes | the script |
| Write one output file | only when an output path is given | the script |
| Run git, kubectl, helm | no — they are printed for the operator | the script contains no subprocess call |
| Emit `git checkout HEAD -- <path>`, which overwrites working-tree edits | yes, without a warning | nothing |

## Outputs

One JSON object: the workstream, its plan name, the trigger, the current status, the
steps, the cluster commands or a note, and the git commands. It always exits 0,
including for a plan that cannot apply.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| The plan ignores the change | Two different TLS attempts get the same rollback, word for word | Plans are constants keyed by workstream; the state file contributes a status and a flag. The docstring promises steps "based on what was changed". Observed |
| One file of four | After the git rollback, the install task, the values and the feature-flag variable still carry the change | The TLS plan restores only the TLS task file, while the TLS guide ([component 20](../references/20-secrets-store-tls-unseal-guide.md)) changes the main install task, the security variables file and the probe settings as well. Observed |
| A restore that restores nothing | The checkout succeeds and the broken configuration stays | Once the change is committed, HEAD contains it, and `git checkout HEAD -- <file>` only drops uncommitted edits. Only the benchmark workstream's plan uses a revert. Observed |
| Uncommitted work discarded | Edits in progress in a role are gone | Two plans check out single files from HEAD, and the remediation plan checks out a whole role directory; none of them warns. Observed |
| Error handling that raises | With no YAML library and no state file, the script stops with an attribute error instead of falling back | The except clause names the YAML library's error class. That name is evaluated only once an error is raised, and the library is the one thing absent. Observed, read off the code |
| A gate nobody runs | No rollback plan is ever produced before a risky change | No phase calls the script; it appears only in reference tables. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [16 The Permission Ladder](../../../../cards/16-the-permission-ladder.md) | Every command is printed for an operator, never run, which keeps the *ask* rung with a human. A command that discards work goes out on that rung with no deny and no warning |
| [17 Blast-Radius Gating](../../../../cards/17-blast-radius-gating.md) | Meant to prepare the way back before a risky change; the way back is written before the change is known |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | One plan per locked workstream, and the TLS plan answers the sprint's TLS-stability trigger |

## Provenance

The source system held this as one standard-library Python script of about 220
lines in the skill's scripts directory. Most of it is the five-entry plan table;
the rest is a loader for the state file and a command-line entry point. Nothing
records that a plan it printed was ever executed, or what a rollback looked like in
practice, and this card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/25-static-rollback-planner/`](../../../../skeletons/components/25-static-rollback-planner/).
Standard library, offline. It prints the constant recipe for a workstream. With
`--audit` it replays the TLS recipe's git commands, on paper, against a fabricated
change log of two attempts and reports six gaps. It never runs git.

## What is deliberately missing

**A plan derived from the change.** The files a workstream touched are one `git diff`
away from the sprint's starting commit. Committed files want a revert; uncommitted
ones want a warning before anything overwrites them.

**A deny on discarding.** A working-tree checkout is the one destructive verb the
script emits. A real version would print it only after confirming there are no
uncommitted edits, or not print it at all.

**Being called.** A rollback plan prepared before a risky change needs a phase that
runs it. The entry file lists the script and never invokes it.

**In the prototype:** no state file is read, no cluster commands are printed, and
the load-failure path is described rather than reproduced, since reproducing it
would need a non-standard library.
