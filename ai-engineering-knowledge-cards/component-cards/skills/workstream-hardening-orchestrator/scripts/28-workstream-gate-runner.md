---
component: 28
title: Workstream Gate Runner
type: script
instances:
  - 16-the-permission-ladder
  - 17-blast-radius-gating
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 10-sprint-state-file
  - 19-workstream-gate-catalogue
---

# Workstream Gate Runner

> The script that decides whether a workstream passed: a fixed table of offline gates and
> cluster commands — whose gates check that a file exists, not that this sprint made it.

## What it is

A standard-library Python script the hardening orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)) runs after each workstream and
once more for all five in the final validation phase. For the named workstream it runs a
short list of offline gates — local lint and syntax commands, file-existence checks — and,
in cluster-aware mode, prints the cluster commands an operator should run. It is the
executable form of the gate catalogue
([component 19](../references/19-workstream-gate-catalogue.md)), and the only script in the
skill that runs a command itself.

## Trigger and routing

Executed, never loaded. The skill's entry file runs it at the end of workstream A, lists it
for every workstream in its quick-reference table ("run after each workstream"), and loops
it over all five in the final validation phase. Each call passes the workstream letter and
the sprint state file ([component 10](../assets/10-sprint-state-file.md)).

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Workstream: A to E | yes | the calling phase |
| Path to the sprint state file | yes | the calling phase — and never opened |
| Cluster-access flag | no | the scope-lock answer |
| Repository path | no; the current directory by default | the calling phase |

## Procedure

1. Look up the workstream in a table fixed in the script. Each entry holds offline gates
   and cluster gates.
2. Run each offline gate. A **file gate** globs a path pattern under the repository and
   passes if anything matches. A **command gate** runs the command through a shell in the
   repository with a two-minute timeout and passes on exit 0.
3. Sort the results into passed and failed. A command gate carries a blocking flag; lint
   is marked non-blocking, syntax blocking. File gates count as blocking.
4. In cluster-aware mode, list each cluster gate's command with a note to run it manually.
5. Print one JSON document. Exit 0 if no blocking gate failed, 1 otherwise.

The gates, by workstream: A and B — lint, syntax, and the existence of the TLS or unseal
task file; C — lint and syntax; D — a triage table under any dated output directory; E — a
hygiene report under any dated output directory. Cluster gates: secrets-store status per
pod and certificate state; for B a pod restart test; policy reports; benchmark job logs;
pod, release and node health.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Local lint and syntax commands, through a shell | yes, executed by the script | nothing — the skill's never-run rule names cluster and deploy tools, not local ones |
| Glob the repository | yes | the script |
| Cluster commands | printed for an operator, never run | the script's code: it has no path that executes them |
| Deleting a pod | printed as a "validation" command | nothing; an operator who runs the list runs the deletion |

## Outputs

One JSON document on stdout: the workstream, the passed and failed gates with up to 500
characters of each command's output, the commands to run manually, and an overall PASS or
FAIL. The exit code mirrors the overall result. Nothing is written to disk.

## Failure modes

Every row is read directly off the script.

| Failure | Symptom | Root cause |
|---|---|---|
| The plan is never read | A nonexistent state-file path validates exactly like the real one | The argument is required and passed into the validator, which never opens it. Observed |
| An earlier sprint passes today's gate | Workstream D passes on a triage table produced by a previous sprint | File gates glob every dated output directory, not the current sprint's. Observed |
| A gate that passes before work starts | Workstream A's TLS gate passes on a repository where nothing has been done | The gate checks that the TLS task file exists, and that file is the stub the scope detector ([component 26](26-repo-scope-detector.md)) requires to be present before the sprint starts. The same holds for B. Observed |
| Lint never fails anything | Lint fails and the overall result is PASS | Lint is marked non-blocking, while the gate catalogue says lint is treated as blocking for the sprint. Observed |
| A missing tool reads as a failed gate | A machine without the build tool reports the lint gate failed, not skipped | Commands run through a shell, which exists, so the "tool not found" branch never fires; the shell's own exit code is a plain failure. Observed |
| The runner runs things | Two commands execute on the operator's machine during "validation" | Local gates go through a shell; the skill's two-layer rule — generate, never run — holds only for the cluster gates. Observed |
| A write in the validation list | Workstream B's cluster gates include deleting a secrets-store pod | The restart test is a deletion followed by a status check, listed beside read-only checks with the same "run manually" note. Observed |
| A gate with no producer | Workstream E fails until someone writes a hygiene report by hand | No script, template or phase of the skill produces the file the gate looks for. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [16 The Permission Ladder](../../../../cards/16-the-permission-ladder.md) | Two rungs in one table: local commands run, cluster commands are printed — and the printed list includes a write, so the rung is a label |
| [17 Blast-Radius Gating](../../../../cards/17-blast-radius-gating.md) | Validation as the check after a change; the destructive restart test is the change the card says to gate before, filed under checking after |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | Per-workstream gates that a checkpoint can cite — and the stale-glob and stub gates are evidence that does not belong to this sprint's scope |

## Provenance

Instanced in the source system by one standard-library Python script of about 210 lines
in the hardening skill's scripts directory: a gate table for five workstreams, a file
check, a shell runner, and a JSON report. Its gate list is a subset of the gate catalogue
reference, with different numbers in places — the restart test waits half as long.
Nothing in the component records a validation run or its results; this card claims none.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/28-workstream-gate-runner/`](../../../../skeletons/components/28-workstream-gate-runner/).
Standard library, offline. It runs the gate table over a fabricated repository at the
start of a sprint, with the shell replaced by a stub that prints, and with `--audit`
reports eight findings, from the unread plan to the pod deletion.

## What is deliberately missing

**Gates scoped to the sprint.** Reading the state file for the current output directory
would fix the stale glob and give the required argument a reason to exist.

**Content checks.** A stub and a finished task file pass the same existence test; a
triage table with every row undecided passes the same test as a finished one. Each gate
needs one assertion about what the file says.

**Separation of checks from changes.** The restart test is a deliberate disruption with a
blast radius of its own. It belongs in a plan with a confirmation, not in a list an
operator runs to see whether things are fine.

**In the prototype:** no shell, no cluster, and only the gates that carry a finding; the
recorded lint exit code is chosen to fail.
