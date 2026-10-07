---
component: 49
title: Implementation Subagent Definition
type: subagent
instances:
  - 07-capability-taxonomy
  - 11-adversarial-role-separation
  - 16-the-permission-ladder
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 39-generator-role-reference
  - 42-role-spawn-prompt-set
---

# Implementation Subagent Definition

> The builder's role as a standalone subagent file — the only role in the loop listed write
> tools, with a file scope that is a sentence and a ban on caveats that sits beside a known-gaps section.

## What it is

A subagent definition bundled with the sprint-loop skill
([component 32](../skills/role-separated-sprint-loop-orchestrator/32-role-separated-sprint-loop-orchestrator.md)).
It is the loop's second role: it implements one sprint's deliverables inside the file scope
the specification names, then returns notes on what it changed. It never scores, approves
or defends its own work — the rule the whole loop is built on. It is the short form of the
generator role reference
([component 39](../skills/role-separated-sprint-loop-orchestrator/references/39-generator-role-reference.md)), and the one role of the
three that can change the repository, which is why its limits matter most.

## Trigger and routing

Dispatched by name from the skill's build phase, once per sprint and again on each retry.
Its description says what it produces and that it never grades itself; it names no
triggers and no exclusions. As with the other two definitions, the skill's table lists the
file and its tools, and the documented spawn prompts
([component 42](../skills/role-separated-sprint-loop-orchestrator/references/42-role-spawn-prompt-set.md)) use a general-purpose agent
type, so the file's tool list is not what the spawned agent runs with. See
[component 31](31-benchmark-triage-subagent.md) for a read-limited agent that holds the
shell anyway.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The sprint's section of the specification | yes | the parent, from the planner's output |
| The contract | yes | the parent — which also says to hold evaluation criteria out of the work |
| Repository context | yes | the agent's own read tools |
| A return report | on retries only | the parent, after a failed evaluation |

## Procedure

1. Read every input in full.
2. Implement the deliverables, inside the sprint's file scope, matching the repository's
   existing patterns, with atomic changes and no drive-by refactoring.
3. Write tests only where the acceptance targets name them.
4. Record assumptions where the specification was ambiguous, rather than stopping to ask.
5. Return notes: changes made, assumptions, known gaps, files modified — and no comment on
   quality.
6. On a retry, address every blocking item in the return report and nothing else.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read, Glob, Grep | listed | an `allowed-tools` key — a skill-side grant name |
| Write, Edit, Bash | listed | the same key |
| Writing outside the sprint's file scope | forbidden | a sentence in the body; a tool grant has no path in it |
| Scoring or approving its own work | forbidden | the body's never list only |
| Everything else the harness has | not mentioned | nothing; no `tools:` key means all |

## Outputs

An implementation-notes document returned to the parent, and the changes themselves in the
working tree. The notes go to the evaluator with the work, which is why the body bans
self-congratulation: the notes are a channel into the grader's context.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| The grant is under the wrong key | A harness that discovered the file would apply no narrowing | The tool list sits under `allowed-tools`, not `tools:`. Observed |
| The spawn path never applies the file | The builder runs with whatever the general-purpose agent has — web tools included | The documented prompts name a general-purpose type; the file sits in the skill's own directory, not where a harness discovers subagents. Observed |
| Scope is a sentence | A write outside the sprint's files is allowed, and noticed only if someone reads the diff | The grant is Write and Edit with no path; the body's file-scope rule is not checked by anything. Structural |
| Two sentences that overlap | The builder omits a known gap to obey the ban, or adds a caveat and breaks the rule | The never list bans a caveat about what could be improved; the output shape requires known gaps. The line between them is drawn in the role reference, not in this file. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [07 Capability Taxonomy](../../cards/07-capability-taxonomy.md) | The subagent as a unit of delegated work with its own context, once per sprint |
| [11 Adversarial Role Separation](../../cards/11-adversarial-role-separation.md) | The no-self-review rule: the role that builds does not grade, and says so first |
| [16 The Permission Ladder](../../cards/16-the-permission-ladder.md) | The one role that writes has its scope as advice — the lowest rung, where the most is at stake |

## Provenance

Instanced in the source system by one Markdown subagent definition of about 60 lines:
frontmatter with a name, a multi-line description and a six-tool list, then sections for its
single responsibility, a no-self-review rule marked as its most important, implementation
rules, retry rules and an output shape. It sat in an agents directory inside the skill's own
directory, and repeats in brief what a longer role reference says. Nothing in the component
records how often it was dispatched or what it built. This card claims neither.

## Prototype

Minimal runnable prototype in
[`../../skeletons/components/49-implementation-subagent-definition/`](../../skeletons/components/49-implementation-subagent-definition/).
Standard library, offline. It reads a fabricated definition the way a harness would,
checks four attempted writes against the sprint's file scope and against the grant, and
lays the two overlapping sentences side by side; `--narrowed` adds the frontmatter line
that fixes the grant and nothing else.

## What is deliberately missing

**A scope in the grant.** The write tools carry no path. A permission rule or a hook
outside the definition would give the sentence a harness to hold it
([card 16](../../cards/16-the-permission-ladder.md)'s deny rung); the source had the
sentence alone.

**One definition of a known gap.** The role reference separates a thing left undone from a
remark about what could be better. This file does not, and a spawn that skips the reference
gets both rules and no boundary.

**In the prototype:** no model, no build and no writes; the attempted writes are a list,
checked, never performed.
