---
component: 30
title: Parallel Gap-Scan Subagent
type: subagent
instances:
  - 07-capability-taxonomy
  - 16-the-permission-ladder
related:
  - 08-workstream-hardening-orchestrator
  - 17-owned-scope-policy-remediation
  - 23-hardening-field-scanner
---

# Parallel Gap-Scan Subagent

> A small-model worker the hardening orchestrator dispatches to inventory missing container
> hardening fields — read-only by its own description, and by nothing else.

## What it is

A subagent definition bundled with the hardening orchestrator
([component 08](../skills/workstream-hardening-orchestrator/08-workstream-hardening-orchestrator.md)).
It scans the target repository's own roles for four missing hardening fields — non-root,
no privilege escalation, read-only root filesystem, dropped capabilities — and returns a
JSON inventory the orchestrator folds into the policy-remediation workstream and the first
checkpoint report. It runs on a small, cheap model, in parallel with the benchmark triage
subagent ([component 31](31-benchmark-triage-subagent.md)). In
[card 07](../../cards/07-capability-taxonomy.md)'s terms it is the right mechanism for the
job: bounded, read-only, parallel work whose intermediate results the parent does not need
to see.

## Trigger and routing

Dispatched by name, not routed by its description. The skill's entry file has a
sub-agents table naming it with its purpose, tool list and model, and an example dispatch
line for the quick-wins phase: scan the roles, given the owned-role list. Its description
says what it returns and that it runs alongside the triage subagent; it names no trigger
phrases and no exclusions, which is right for an agent nothing but its parent calls.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The owned-role list | yes | the parent, from the sprint state file — which the scope detector ([component 26](../skills/workstream-hardening-orchestrator/scripts/26-repo-scope-detector.md)) fills with every role it finds |
| The target repository's roles directory | yes | the working directory |

## Procedure

1. Take the owned-role list from the parent.
2. For each owned role, search its values and templates for the four fields.
3. Classify each gap by role, file, and fix type: through chart values where the chart
   exposes the field (preferred), through a template override otherwise.
4. Skip three roles listed as needing elevated access by design; flag the secrets store's
   injector webhook for special handling.
5. Return one JSON inventory: roles scanned, roles with gaps, and one record per gap with a
   priority.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Glob, Grep, Read | yes | the body's "Use" line — prose |
| Bash, Edit, Write | no | the body's "Do NOT use" line — prose only |
| Model | a small, cheap one | the frontmatter |
| Anything else the harness has | not mentioned | nothing; with no `tools:` key, a harness grants all of it |

The frontmatter has a name, a description and a model, and no tool list. Every limit in
the left column is a sentence in the body — [card 16](../../cards/16-the-permission-ladder.md)'s
lowest rung, in a component whose whole purpose is to be the read-only one.

## Outputs

A JSON inventory returned to the parent, not written to disk. The parent merges it into
the policy-remediation workstream's starting state and the checkpoint A report.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Read-only is a request | The subagent runs with Bash, Edit and Write available | Tool limits are prose in the body; the frontmatter has no `tools:` key, which a harness reads as "all tools". Observed |
| Bundled where the harness does not look | Dispatch by name finds no such agent, or the model pastes the file into a general-purpose agent, whose own tools and model apply instead | The definition sits in an agents directory inside the skill's own directory, not where a harness discovers subagents. Structural |
| Three skip lists | A role the field scanner exempts is scanned by the subagent; the guide special-cases two roles neither of them skips | The subagent's prose skips three roles, the field scanner ([component 23](../skills/workstream-hardening-orchestrator/scripts/23-hardening-field-scanner.md)) exempts four, the remediation guide ([component 17](../skills/workstream-hardening-orchestrator/references/17-owned-scope-policy-remediation.md)) names five, and nothing compares them. Observed |
| The scan is done twice, differently | The subagent's inventory and the scanner's disagree on the same repository | A scanner script exists, but the subagent is told not to use Bash, so it re-derives the scan with search tools and its own reading of "missing". Observed |
| "Owned" means everything | Roles the team does not own are scanned and reported | The owned-role list comes from a state file the scope detector fills with every role directory. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [07 Capability Taxonomy](../../cards/07-capability-taxonomy.md) | A subagent for bounded, parallel, read-mostly work on a cheaper model, returning only a summary to the parent |
| [16 The Permission Ladder](../../cards/16-the-permission-ladder.md) | Its read-only status is a sentence, not a grant — the gap between the prose rung and the configured one, in one file |

## Provenance

Instanced in the source system by one Markdown subagent definition of about 55 lines:
frontmatter with a name, a two-line description and a small model, then a task list, a
sample JSON inventory, scope rules with a skip list, and a two-line tool section. It sat
in an agents directory inside the hardening skill's own directory. The skill's entry file
describes dispatching it; nothing in the component records that it was dispatched, or
what it returned. This card claims neither.

## Prototype

Minimal runnable prototype in
[`../../skeletons/components/30-parallel-gap-scan-subagent/`](../../skeletons/components/30-parallel-gap-scan-subagent/).
Standard library, offline. It reads a fabricated definition the way a harness would,
reports the tools granted that the prose forbids, and lays the three skip lists side by
side; `--narrowed` adds the one frontmatter line that closes the first gap.

## What is deliberately missing

**A tool grant.** One line of frontmatter — the three read tools — would make the body's
limits true. The source had the words and not the line.

**One skip list.** The exception list belongs to the scanner script, and the subagent
belongs to running it — which needs a narrow command permission, not prose about Bash.

**In the prototype:** no model, no scan and no discovery; the definition is parsed
directly, as if a harness had found it.
