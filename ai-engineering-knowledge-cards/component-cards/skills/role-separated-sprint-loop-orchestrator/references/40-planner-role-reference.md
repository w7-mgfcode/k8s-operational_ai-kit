---
component: 40
title: Planner Role Reference
type: reference
instances:
  - 11-adversarial-role-separation
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 48-planning-subagent-definition
---

# Planner Role Reference

> The brief a planning agent reads before turning a request into a sprint spec — a
> six-box checklist for the spec, no program that ticks any of the boxes, and a required
> field its own role is told not to fill.

## What it is

A reference file the sprint-loop orchestrator
([component 32](../32-role-separated-sprint-loop-orchestrator.md)) loads in its first
phase. It defines the planner's job — expand an ambiguous request into an actionable,
testable spec and do nothing else — and gives the spec's shape, five rules for cutting
sprints, a section on writing acceptance targets with good and bad pairs, a checklist the
spec must meet before the user sees it, and a table of anti-patterns. About 115 lines. It
is the planning half of the separation in
[card 11](../../../../cards/11-adversarial-role-separation.md): the spec is what the
generator builds to and the evaluator later scores against.

## Trigger and routing

Loaded on demand. The skill's first phase tells the model to read it before planning, the
skill's role table lists it against the planner, and the planner's spawn prompt
([component 42](42-role-spawn-prompt-set.md)) tells the spawned agent to read it by a
relative path. It carries no trigger text of its own, and nothing loads it in any later
phase.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The user's request, verbatim | yes | the conversation |
| Repository context: file tree, key modules, existing patterns | yes | the planner's own reading |
| Files the request references or implies | yes | the planner's own reading |
| Constraints: time, scope, stack, deployment targets | yes | the user — and if any input is missing, the reference says to ask rather than guess |

## Procedure

1. Gather the four inputs; ask the user about anything missing or unclear.
2. Write the spec in the fixed shape: goal, constraints, a sprint breakdown, and an
   out-of-scope section. Each sprint has a scope, a file list, dependencies, acceptance
   targets and an estimated complexity.
3. Cut sprints by five rules: one logical unit each, dependency order, at most five,
   a file scope per sprint, and no implementation detail.
4. Write two to five acceptance targets per sprint — concrete, testable, scoped to the
   sprint.
5. Walk the six-item checklist: clear goal, every sprint complete, dependency order,
   no sprint over about ten files, a non-empty out-of-scope list, and *the user has
   reviewed and approved the spec*. The last box is the gate out of the phase.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Reading the repository | implied by the input list | nothing — the reference names no tools |
| Writing code or evaluating work | no | the role definition, as prose |
| Producing the spec file | expected | nothing grants it: the planning subagent's tool list ([component 48](../../../subagents/48-planning-subagent-definition.md)) has no write tool |
| Approval before the next phase | required | the orchestrator's instruction, and a free-text note in the state file |

## Outputs

One Markdown spec, returned to the orchestrator, which presents it to the user. Later
phases read the relevant sprint section; contract axes are negotiated separately, not
derived from it. Writing it needs no confirmation; leaving the phase needs the user's.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Required field, banned activity | The spec structure asks for an estimated complexity per sprint; the planner's definition and spawn prompt say not to judge feasibility or estimate effort | Two components state opposite things about one field, and nothing compares them. Observed |
| A checklist nothing runs | A spec with twelve files in one sprint, a forward dependency or no out-of-scope list reaches the user | Sprint count, files per sprint, dependency order and the out-of-scope list are all countable, and are boxes for the model to tick. Observed |
| The spec is never opened | A sprint's file scope is not compared with what the generator changes | The orchestrator's state keeps the spec's path; no script parses it, so its limits bind only if the model remembers them. Structural |
| Approval is a note | The phase is marked complete with nothing proving the user saw the spec | The last checklist item is recorded only as free text in a state update. Observed |
| Concreteness is judged by the planner | Vague targets ("clean", "well-structured") pass into the contract | The good and bad pairs teach the distinction, and no check can tell a vague target from a concrete one. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | A planner that implements and evaluates nothing, whose output is the contract's raw material |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | A file scope per sprint, a mandatory out-of-scope list, and user approval before work starts |

## Provenance

Instanced in the source system by one Markdown reference of about 115 lines in a skill's
references directory: a contents list, a role definition, input requirements, a spec
template, five decomposition rules, a section on acceptance targets with paired good and
bad examples, a six-item validation checklist and a five-row anti-pattern table. It
restates, in more detail, rules also found in the planning subagent's definition. The
source does not record how many specs it produced or how often the checklist caught one.
This card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/40-planner-role-reference/`](../../../../skeletons/components/40-planner-role-reference/).
Standard library, offline. It reads fabricated specs, runs the countable half of the
checklist, shows a vague spec passing it, and puts the required field beside the ban.

## What is deliberately missing

**A reader of the spec.** The component has no script that parses it; the prototype's
checker is the missing consumer, and it counts rather than judges.

**Recorded approval.** The last checklist item has no place to be recorded beyond a note.

**In the prototype:** no planner, no repository and no user — the specs are fixtures, and
the "conflict" is two strings in a file, standing for two real statements in two files.
