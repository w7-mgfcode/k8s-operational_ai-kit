---
component: 38
title: Evaluator Role Reference
type: reference
instances:
  - 02-progressive-disclosure
  - 11-adversarial-role-separation
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 34-axis-scored-evaluation-template
  - 37-evaluator-failure-pattern-catalog
  - 41-axis-scoring-guide
  - 46-evaluation-structure-validator
  - 50-evaluation-subagent-definition
---

# Evaluator Role Reference

> The grader's whole job in one document — flaw first, score low when unsure, treat missing
> evidence as failure — written in three shapes for the one thing it asks for most.

## What it is

A reference of about 170 lines in the sprint-loop skill's references directory
([component 32](../32-role-separated-sprint-loop-orchestrator.md)). It defines the evaluator
role: a five-rule anti-sycophancy mandate with an "auditor, not colleague" mental model; a
six-step protocol; the 1–5 scale with discipline notes; criteria for what is blocking and
what is not, and the four things every blocking issue must say; an output structure; three
calibration examples; and a six-row table of anti-patterns. It is the role half of
[card 11](../../../../cards/11-adversarial-role-separation.md), loaded only when a sprint
reaches evaluation, as [card 02](../../../../cards/02-progressive-disclosure.md) prescribes.

## Trigger and routing

Loaded by instruction in the skill's evaluate phase, alongside the scoring guide
([component 41](41-axis-scoring-guide.md)) and the failure-pattern catalog
([component 37](37-evaluator-failure-pattern-catalog.md)). The evaluator's spawn prompt
([component 42](42-role-spawn-prompt-set.md)) tells the subagent to read it, and the
evaluation subagent definition ([component 50](../../../subagents/50-evaluation-subagent-definition.md))
restates its mandate in a shorter form. No description routes to it.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Sprint spec | yes | the plan phase |
| Contract | yes | the contract phase ([component 36](../assets/36-sprint-contract-template.md)) |
| Every file the generator modified | yes | listed in the generator's implementation notes |
| The generator's implementation notes | yes | the previous phase |

## Procedure

1. Read the spec, to know what was meant to be built.
2. Read the contract, for the exact axes and thresholds.
3. Read every modified file.
4. For each axis: gather evidence, compare it with the acceptance targets, assign a score,
   and, if the score is under the threshold, name the blocking issue.
5. Compile the evaluation in the template shape ([component 34](../assets/34-axis-scored-evaluation-template.md)).
6. Run the evaluation validator ([component 46](../scripts/46-evaluation-structure-validator.md))
   on it.

## Tools and permissions

None of its own. The limits it states apply to a subagent that holds the shell.

| Verb | Allowed | Enforced by |
|---|---|---|
| Read the implementation | yes | the evaluation subagent's grant |
| Modify any repository file | no | the reference's "does not" list — prose |
| Suggest a code fix | no | the same list — prose |
| Raise or lower a threshold | no | the scoring guide and the contract's rule; nothing locks the contract |
| Run the validator (step 6) | yes | needs the shell the subagent definition grants |

## Outputs

One evaluation document, in the output structure it defines, saved as the sprint's
evaluation file. The validator reads it; the gate does not.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Three shapes for one issue | A blocking issue is written as one line, as a bold line plus a follow-on, or as four labelled lines, depending on which document the evaluator followed; the one-line shape has no "what passing looks like" | The reference's output block, the evaluation template and the scoring guide each define the shape; the reference requires four elements and its own block carries three. Observed |
| A contract version nothing compares | An evaluation whose header names one contract version is validated against a contract on disk at another, and passes | The template has a contract-version line; the reference's output structure omits it; the validator reads the contract file it is given and never the header. Observed |
| Problems, not solutions — with a field for the fix | An evaluator describes what passing looks like in terms close to a fix, and the return template ([component 33](../assets/33-blocking-items-return-template.md)) then asks for the "minimum fix needed" | The ban on suggesting fixes and the required "what passing would look like" are one clause apart, with only "without prescribing implementation" between them. Observed |
| The checked runs the check | An evaluation is validated by the party that wrote it, or by the orchestrator, depending on which document is read | Step 6 tells the evaluator to run the validator on its own output; the skill's phase text has the orchestrator run it after the evaluator. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [02 Progressive Disclosure](../../../../cards/02-progressive-disclosure.md) | A role document read at the one phase that needs it, not carried by planning or generation |
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | The evaluator's mandate and protocol — and the places where its document, template and guide each define the same artifact |

## Provenance

Instanced in the source system by one Markdown file of about 170 lines in the sprint-loop
skill's references directory, with a table of contents, and one sibling reference per role.
Its mandate is restated, shorter, in the subagent definition and the spawn prompt. Nothing in
the component records how many evaluations followed it or how they scored.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/38-evaluator-role-reference/`](../../../../skeletons/components/38-evaluator-role-reference/).
Standard library, offline, fabricated fixtures. It writes one blocking issue in the three
shapes and shows which required element each carries, then runs a structure check on an
evaluation that declares a different contract version than the one on disk.

## What is deliberately missing

**One shape, defined once.** The other two documents link to it instead of restating it.

**A recorded contract version.** Written where the evaluation and the gate can compare it.

**One owner for the validator step.** Either the evaluator or the orchestrator, not both.

**In the prototype:** no model reads the reference, and the mandate's behavioural rules —
lead with flaws, score low when unsure — are not modelled. Only the places where the text
can be set against a file are.
