# Skeleton — Evaluator Role Reference

Two places where an evaluator role reference and the files around it disagree, shown over
fabricated fixtures: one blocking issue written in the three shapes the loop prescribes,
and an evaluation that names a contract version nothing compares. The card is
[component 38](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/38-evaluator-role-reference.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
issue-formats.json   one fabricated blocking issue, written in the shape of the role
                     reference's output block, of the evaluation template, and of the
                     scoring guide; and the four elements the document says every
                     blocking issue must carry
contract-v2.md       a fabricated contract at version 2
evaluation-v1.md     a fabricated evaluation whose header says it was written against
                     contract version 1
reconcile.py         the two checks
```

## Try it

```bash
python3 reconcile.py --formats   # one shape lacks a required element; exits 1
python3 reconcile.py --version   # the structure check is clean, the versions differ; exits 1
python3 reconcile.py             # no option given; exits 2
```

**The shapes.** The role reference says every blocking issue carries what is wrong, where,
which axis and what passing looks like. Its own output block has three of the four. The
template has all four across two lines, and the scoring guide has all four on four
labelled lines. A counter of numbered items sees one issue in each.

**The version.** The evaluation header says version 1; the contract on disk says version 2.
The structure check — every axis scored, every label consistent with its threshold — passes
against the file on disk, and nothing reads the header. Exit 1 marks that the two disagree
and nothing noticed, not an error.

## What is deliberately missing

**The reference itself.** Its mandate, calibration examples and protocol are prose for a
model to follow; there is nothing to run. This skeleton checks only the two places where
its text can be set against something else.

**The step that runs the validator.** The role reference tells the evaluator to run the
validator on its own output, and the skill tells the orchestrator to. Neither is modelled.

**The fix, for the pattern.** One shape for a blocking issue, defined once and linked from
the other two, and a contract version recorded where the evaluation and the gate can both
compare it. [Card 11](../../../cards/11-adversarial-role-separation.md) is the pattern this
belongs to.
