# Skeleton — Sprint Contract Template

A sprint contract template, a writer that never opens it, and an audit of what falls
between them. The card is
[component 36](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/assets/36-sprint-contract-template.md);
the skill whose second phase fills it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
contract.template.md   a fabricated template: header, sprint scope, an axes table with a
                       description column, a five-point scale, an out-of-scope list and
                       six contract rules — slots in square brackets
axes.json              one fabricated sprint: a CSV importer graded on three axes
audit.py               a stand-in writer (builds from its own strings, template unopened),
                       a stand-in reader (keeps rows shaped `| name | N/5 |`), and four checks
```

## Try it

```bash
python3 audit.py          # four findings; exits 1
python3 audit.py --emit   # the contract the writer builds, to compare by eye; exits 0
```

**The shape.** The writer's contract has no scope section and no scale table, its axes
table has no description column, and it carries five rules where the template has six.
Whichever way a sprint's contract was made decides which shape its evaluator reads.

**The freeze.** The template's first rule says the contract is frozen once the build
starts. The audit writes the same sprint and version a second time with every threshold
lowered to 1. The write succeeds, no earlier copy remains, and the template's
`superseded` status is set by nothing. The audit does this in a temporary directory and
removes it.

**The weight.** The writer derives the weight from the threshold. The reader never looks
at it, so flipping every weight changes nothing it returns.

**The skipped rows.** Three axis rows are written: one filled, one whose name has a
hyphen, one still a placeholder. The reader keeps one and raises nothing. Only a contract
with no rows at all would stop it. Exit 1 marks these findings, not an error.

## What is deliberately missing

**The real writer and validator.** The stand-in writer and reader model one behaviour
each — build from inputs, parse rows by shape — and nothing else of their components
([47](../47-sprint-contract-writer/), [46](../46-evaluation-structure-validator/)).

**A state file.** In the source the contract's version and status sit in a file the
sprint loop also keeps; nothing here records them, which is part of why the freeze cannot
be checked.

**The fix, for the pattern.** The writer filling this template instead of its own
strings, a refusal to overwrite a contract whose build has started, a recorded hash the
evaluator compares, and a reader that reports every row it skips.
[Card 19](../../../cards/19-scope-lock-and-checkpoint-delivery.md) is the part of the
pattern this belongs to.
