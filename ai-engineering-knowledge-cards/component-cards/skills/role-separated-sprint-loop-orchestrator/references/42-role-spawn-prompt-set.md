---
component: 42
title: Role Spawn Prompt Set
type: reference
instances:
  - 07-capability-taxonomy
  - 11-adversarial-role-separation
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 37-evaluator-failure-pattern-catalog
  - 48-planning-subagent-definition
  - 49-implementation-subagent-definition
  - 50-evaluation-subagent-definition
---

# Role Spawn Prompt Set

> Four copy-ready prompts, one per role-and-iteration, for spawning the planner, the
> builder and the grader as separate agents — that skip the grader's most-stressed file,
> spawn every role as a general agent with every tool, and are checked by no one.

## What it is

A reference file of about 170 lines holding four fenced prompts: the planner's, the
generator's, the generator's on a retry iteration, and the evaluator's. Each has a role
preamble, a line telling the agent to read its role reference, bracketed slots for the
context to inject, a numbered task and a block of critical rules. A usage paragraph says
to copy the prompt, fill the brackets and spawn through the agent tool as a general-purpose
agent. It is how the sprint-loop orchestrator
([component 32](../32-role-separated-sprint-loop-orchestrator.md)) turns three role
documents into three isolated agents, the mechanism in
[card 07](../../../../cards/07-capability-taxonomy.md).

## Trigger and routing

Listed in the skill's reference table as copy-paste prompts, and mentioned in its roles
section. No phase's read list names it: the planning, generation and evaluation phases each
say which role references to read first, and this is not among them.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The user's request, repository context, constraints | planner | pasted from the conversation |
| The sprint's spec section | generator, evaluator | the approved spec |
| The contract | generator, evaluator | the sprint's contract file, pasted or referenced |
| The delta report and previous notes | generator on a retry | earlier iterations |
| The work to evaluate and the generator's notes | evaluator | the working tree and the generator's output |
| A workspace path | generator | the orchestrator |

## Procedure

1. Pick the prompt for the role and iteration.
2. Replace every bracketed slot with its content, or with an instruction to read it.
3. Spawn through the agent tool as a general-purpose agent.
4. The agent reads its role reference by the relative path in its first lines, does the
   numbered task, and obeys the critical rules.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Agent type | general-purpose, "unless your environment has custom agent types" | the usage paragraph — and the harness then grants that type's whole tool set |
| Role tool limits (the grader reads, does not write) | stated in the three subagent definitions | not applied: the prompts spawn a general agent, and the definitions sit inside the skill, not where a harness finds agents |
| "Never score yourself", "do not suggest fixes" | per role | the prompt's own text — prose |
| Reading role references | by relative path | the filesystem, from whatever directory the agent starts in |

## Outputs

A prompt string handed to the agent tool; the spawned agent's report is the output. The
planner returns a spec, the generator implementation notes, the evaluator an evaluation —
each to the orchestrator, none written by the prompt set itself.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| The grader never loads the failure catalog | The evaluator grades without the list of named leniency patterns the skill says to read before every evaluation | The evaluator prompt names the evaluator reference and the scoring guide, not the catalog ([component 37](37-evaluator-failure-pattern-catalog.md)). Observed |
| Read-only is a request | The evaluator subagent can write and edit files | Every prompt spawns a general-purpose agent, which carries every tool; the role's narrower list is unused. Observed |
| Relative read paths | The agent reports a missing role reference, or reads a different file of that name | The prompts say to read `references/…` relative to wherever the agent starts, which is the target workspace unless it happens to be the skill's directory. Structural |
| Handed the criteria, told not to use them | The generator prompt has a contract slot and a rule against referencing evaluation criteria | One prompt carries both instructions; the generator reference permits reading the contract and forbids self-scoring, a different rule. Observed |
| Unfilled slots go out | A prompt reaches an agent with a literal bracketed placeholder where the contract belongs | Slots are brackets in a template, and nothing checks that they were replaced. Structural |
| Forbidden estimate | The planner prompt tells the agent not to evaluate feasibility, while the spec shape it must produce has an estimated complexity per sprint | The prompt and the planner reference ([component 40](40-planner-role-reference.md)) disagree. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [07 Capability Taxonomy](../../../../cards/07-capability-taxonomy.md) | Each role spawned as its own agent in a fresh context — isolation as the mechanism |
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | A role preamble, a "sole job" line and critical rules per role, so no agent performs two |

## Provenance

Instanced in the source system by one Markdown reference of about 170 lines in a skill's
references directory: a contents list, a usage paragraph and four fenced prompts. The
source does not record how often the prompts were used as written or edited first. This
card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/42-role-spawn-prompt-set/`](../../../../skeletons/components/42-role-spawn-prompt-set/).
Standard library, offline. It renders fabricated prompts to a stubbed spawn, lints the
set against a phase table, and refuses unfilled slots under `--strict`.

## What is deliberately missing

**A real spawn.** The prototype's spawn function prints. Whether relative paths resolve
from the skill or the workspace is harness behaviour, modelled here as the workspace.

**A typed subagent.** The one change that would apply the role's tool list is spawning
the role by its definition; the prompt set does not, and neither does the prototype.

**In the prototype:** shortened prompts of its own, not the component's.
