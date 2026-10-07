---
component: 36
title: Sprint Contract Template
type: asset
instances:
  - 11-adversarial-role-separation
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 32-role-separated-sprint-loop-orchestrator
  - 34-axis-scored-evaluation-template
  - 39-generator-role-reference
  - 41-axis-scoring-guide
  - 46-evaluation-structure-validator
  - 47-sprint-contract-writer
---

# Sprint Contract Template

> The bar a sprint is graded against, written down before the build starts — in a template
> whose first rule says "frozen", while the script that writes contracts never opens it and
> overwrites a contract without a trace.

## What it is

A plain-text template of 49 lines, shaped as Markdown, in the sprint-loop skill's templates
directory ([component 32](../32-role-separated-sprint-loop-orchestrator.md)). It defines the
contract one sprint is graded against: a header with sprint id, version and status; a scope
section with a spec reference and a one-sentence goal; a table of evaluation axes, each with
a threshold out of 5, a weight and a description; the pass condition; a five-point scale; an
out-of-scope list; and six contract rules. It is [card 19](../../../../cards/19-scope-lock-and-checkpoint-delivery.md)'s
scope lock applied to grading, and the artifact that makes
[card 11](../../../../cards/11-adversarial-role-separation.md)'s "fixed before the work"
concrete.

## Trigger and routing

The skill's template table lists it for defining axes and thresholds before implementation,
and its contract phase is the one that fills it. The contract writer
([component 47](../scripts/47-sprint-contract-writer.md)) names it in its own description as
a structural guide. Downstream, the evaluation validator
([component 46](../scripts/46-evaluation-structure-validator.md)) parses the axes table out
of whatever contract file it is handed, however that file was made; the generator and
evaluator role references ([39](../references/39-generator-role-reference.md),
[38](../references/38-evaluator-role-reference.md)) tell each role how to treat it.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Sprint id | yes | the plan phase's sprint breakdown |
| Spec reference and goal | yes | the approved spec |
| Three to seven axes, each with a threshold from 1 to 5 | yes | contract negotiation; defaults are in the scoring guide ([component 41](../references/41-axis-scoring-guide.md)) |
| Weight and description per axis | yes in the template | chosen by hand, or derived from the threshold by the writer |
| Out-of-scope items | yes | negotiation; the template ships two placeholders |
| Version and status | yes | version starts at 1 |

## Procedure

1. Copy the template, or have the contract writer produce a contract from arguments.
2. Fill the scope section from the approved spec.
3. Choose axes and thresholds; list what is out of scope.
4. Save it in the sprint's directory. Build starts; the first rule says the contract is now
   frozen.
5. To change it, write a new version number, get the owner's approval, and mark the old
   one superseded.

## Tools and permissions

None of its own. Its six rules are the only limits, and all of them are sentences.

| Rule | Allowed | Enforced by |
|---|---|---|
| Frozen once the build starts | no edits | the rule's wording only |
| A change needs a new version and approval | one path to change | the rule's wording only |
| Generator may read it, must not score itself against it | read yes, self-score no | the generator's instructions |
| Evaluator scores strictly against it | no raising or lowering | the evaluator's instructions |
| Out-of-scope items are not penalised | exemption by list only | the evaluator's instructions |

## Outputs

One contract file per sprint, in that sprint's directory, read by the generator, the
evaluator and the validator. Writing it asks for no confirmation; only changing it later is
said to need the owner's approval.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| A template the writer never opens | A contract from the writer has no scope section, no scale table and no description column, and carries five rules where the template has six; a hand-filled one has all of them | The writer builds its text from its own strings and names the template only in its description; nothing compares the two shapes. Observed |
| "Frozen" is a sentence | The writer, run again for the same sprint with lower thresholds, succeeds at the same version number and no earlier copy remains; the validator then grades against whatever is on disk | No lock, hash or refusal to overwrite exists, and no script ever sets the `superseded` or `archived` status the template defines. Observed |
| A weight that changes nothing | Setting every weight to the other value changes no score, verdict or gate | The writer derives the weight from the threshold and the validator reads only the axis name and the threshold. Observed |
| A row that silently is not there | A contract with one axis name containing a hyphen, or one threshold left as a placeholder, is validated against one axis fewer, and the evaluator may leave that axis unscored with no error | The validator keeps only rows whose first cell is word characters and whose second is a digit over five, and skips the rest without reporting them; only a contract with no matching rows at all is refused. Observed for the hyphen; structural for the placeholder |
| Two readings of one rule | The generator is told it may read the contract, and elsewhere that it must not reference the evaluation criteria while building | The template's fourth rule, the skill's generate phase and the spawn prompts word the same constraint three ways ([component 39](../references/39-generator-role-reference.md)). Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [11 Adversarial Role Separation](../../../../cards/11-adversarial-role-separation.md) | The rubric agreed before the work, with an out-of-scope list that stops the grade expanding after the fact |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | Definition fixed before work, with a version and a stated route for changing it — and nothing holding the lock |

## Provenance

Instanced in the source system by one plain-text file of 49 lines in the sprint-loop skill's
templates directory: a header, a scope section, an axes table with four columns, a scale
table, an out-of-scope list and six numbered rules. It is one of four templates the skill
ships. Nothing in the component records how many contracts were created from it or by which
route.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/36-sprint-contract-template/`](../../../../skeletons/components/36-sprint-contract-template/).
Standard library, offline, fabricated fixtures. It holds a template, a stand-in writer that
never opens it and a stand-in reader shaped like the validator's, and audits four things:
the shape difference, a second write that lowers every threshold, a weight column nothing
reads, and axis rows the reader drops without a word.

## What is deliberately missing

**One source for the shape.** The writer filling this template, or the template generated
from the writer, removes the first failure.

**A freeze that holds.** A refusal to overwrite once the build has started and a recorded
hash the evaluator compares — [card 19](../../../../cards/19-scope-lock-and-checkpoint-delivery.md)'s
lock, not its wording.

**A reader that reports.** Every row a validator skips should be named, so an axis cannot
vanish by being mis-typed.

**In the prototype:** the writer and reader model one behaviour each, and the template is
Markdown with bracketed slots exactly because nothing fills it.
