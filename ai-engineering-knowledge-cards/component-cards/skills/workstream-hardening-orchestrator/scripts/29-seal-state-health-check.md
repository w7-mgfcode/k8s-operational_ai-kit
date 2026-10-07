---
component: 29
title: Seal-State Health Checker
type: script
instances:
  - 06-calibrated-degrees-of-freedom
  - 16-the-permission-ladder
related:
  - 08-workstream-hardening-orchestrator
  - 16-recovery-runbook-set
  - 20-secrets-store-tls-unseal-guide
---

# Seal-State Health Checker

> Two halves of one health check: one generates the commands an operator runs against the
> secrets store, the other parses their output — and neither reads what the other produces.

## What it is

A standard-library Python script with two modes, used in the hardening orchestrator's two
secrets-store workstreams ([component 08](../08-workstream-hardening-orchestrator.md)).
Generate mode prints, as JSON, the commands an operator should run: seal status on each
pod, pod and certificate listings, and the manual unseal procedure. Parse mode reads saved
output and reports, per pod, whether it is sealed and whether the set as a whole is
healthy. It is the script behind "check the secrets store is unsealed" in the TLS and
auto-unseal guide ([component 20](../references/20-secrets-store-tls-unseal-guide.md)).

## Trigger and routing

Executed, never loaded. The skill's scripts table lists it with both modes, and its
quick-reference table names generate mode for "check the secrets store's health". The
guide and the gate catalogue both call for a seal-state check after every secrets-store
change; neither names this script, and the recovery runbook
([component 16](../references/16-recovery-runbook-set.md)) gives its own loop for the same
check.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Mode: generate or parse | yes | the calling step |
| Saved status output | for parse | a file the operator saved after running commands |
| Output path | no | the calling step; stdout otherwise |
| Namespace and pod names | — | constants in the script: one namespace, three pods |

## Procedure

**Generate.**
1. For each of the three fixed pods, emit a status command with a hint on what to look for.
2. Emit a pod listing and a certificate listing.
3. Emit an unseal command per pod, interactive, with a note to repeat it once per key share.
4. Print or write the result as JSON, with a note that every command is for manual execution.

**Parse.**
1. Split the input on lines of the form `=== <pod> ===`.
2. In each section, read whether the pod is sealed, HA-enabled and active or standby, and
   its version.
3. If no section was found, return not healthy with a warning that the expected markers
   were missing.
4. Otherwise healthy means: no pod sealed, and the number unsealed equal to the length of
   the fixed pod list. Print or write the result as JSON.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read a saved output file; write the result | yes | the script |
| Cluster commands | generated for an operator, never run | the script's code — it has no path that executes them |
| Unseal commands | generated in the same output as read-only checks | nothing; the operator decides which to run |

## Outputs

JSON on stdout or at the output path. Generate: two lists, health checks and the unseal
procedure. Parse: per-pod fields, sealed and unsealed counts, a healthy flag and a
one-line summary. The exit code is 0 in both modes whatever the result — an unhealthy
secrets store exits like a healthy one.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| The two modes do not meet | Output from running the generated commands parses as "could not parse" | Generate mode emits one command per pod; their output carries no per-pod markers. Parse mode accepts only marked sections, and only the recovery runbook's loop prints the marker. Observed |
| A larger set is never healthy | Four healthy pods report "4/3 unsealed — action required" | The pod list is a constant of three, and healthy requires the unsealed count to equal its length. Observed |
| Writes beside reads | The health check output contains three interactive unseal commands | Generate mode always appends the unseal procedure to the read-only checks, in one JSON document. Observed |
| Health is in the text only | A caller that checks the exit code sees success for a sealed store | Neither mode sets a non-zero exit for an unhealthy result. Observed |
| A pod with no answer is not counted | A pod whose section holds an error instead of a status table counts neither sealed nor unsealed | The seal-state match is optional per section. The set still reads unhealthy, but the summary names no pod. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | Seal state is parsed by code, not judged by the model reading raw output — the low-freedom choice, undone by the two halves being written against different shapes |
| [16 The Permission Ladder](../../../../cards/16-the-permission-ladder.md) | The generate-not-run rung, held by code here; the unseal commands sit on the same rung as the reads, so the ladder's levels are flattened in the output |

## Provenance

Instanced in the source system by one standard-library Python script of about 160 lines
in the hardening skill's scripts directory: a command generator, a regex parser over
marked sections, and a two-mode command line. The namespace and the three pod names are
constants. Nothing in the component records a parse of real output, or which format
operators actually saved; this card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/29-seal-state-health-check/`](../../../../skeletons/components/29-seal-state-health-check/).
Standard library, offline. It generates commands for a fabricated three-pod store and
parses three fabricated captures — unmarked, marked, and a healthy four-pod set — so the
format mismatch and the fixed count show on one screen.

## What is deliberately missing

**One output shape.** A generator whose commands print their own marker, or a parser that
recognises each status table without one — either closes the gap between the modes.

**The pod list from the cluster.** Reading the replica count instead of a constant, so a
scaled set is judged against itself.

**An exit code.** Non-zero when unhealthy, so the validation runner
([component 28](28-workstream-gate-runner.md)) or a person could gate on it.

**In the prototype:** HA mode and version parsing are left out; they change no finding.
