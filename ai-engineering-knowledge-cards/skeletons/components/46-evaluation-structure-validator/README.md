# Skeleton — Evaluation Structure Validator

A fresh validator for the check the sprint-loop skill runs on an evaluator's report —
every contract axis scored, every label consistent with its threshold, every failing axis
backed by an issue — over a fabricated contract and reports for a small CSV-import sprint,
and an audit of what the check passes and fails wrongly. The card is
[component 46](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/46-evaluation-structure-validator.md);
the skill that runs it is [component 32](../32-role-separated-sprint-loop-orchestrator/), and
the script that writes the contract it reads is
[component 47](../47-sprint-contract-writer/).

```
check_evaluation.py           contract parser, evaluation parser, validator; --audit builds
                              variants in a temporary directory and removes it
fixtures/contract.md          three axes with thresholds, as a contract table
fixtures/evaluation_ok.md     a report with one failing axis, one issue and a file reference
fixtures/evaluation_praise.md a report with every field present and nothing in it
```

## Try it

```bash
python3 -B check_evaluation.py --contract fixtures/contract.md --evaluation fixtures/evaluation_ok.md      # valid; exits 0
python3 -B check_evaluation.py --contract fixtures/contract.md --evaluation fixtures/evaluation_praise.md  # valid too; exits 0
python3 -B check_evaluation.py --audit                                                                     # eight findings; exits 1
python3 -B check_evaluation.py                                                                             # usage only; exits 2
```

**The second command is the finding about substance.** The praise report says "looks fine"
for evidence and cites no file, and it is as valid as the first. Every field the validator
checks is present.

**The audit** builds the rest: an honest report rejected for writing an axis in words, a
hyphenated axis that disappears from the contract, two failing axes covered by one issue, a
file reference satisfied by "e.g.", a bullet list of issues that counts as none, an axis
declared not applicable and scored 5, and the same weak report failing against the agreed
contract and passing against a lowered one. Exit 1 marks those findings, not an error.

## What is deliberately missing

**The writer.** The contract the validator reads is written by component 47, whose skeleton
is deliberately not wired to this one; the axis names it accepts and the names this parser
sees are allowed to disagree.

**A substance check.** Counting praise against flaws, looking for hedging words, and
requiring a line reference on every score are all mechanical. None is here, because the
source's validator has none.

**A shell, a model, a network.** None is used. The audit writes only to a temporary directory
it removes.
