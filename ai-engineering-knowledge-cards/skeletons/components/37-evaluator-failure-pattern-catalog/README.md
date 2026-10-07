# Skeleton — Evaluator Failure-Pattern Catalog

The eight self-checks a failure-pattern catalog tells an evaluator to run on its own
output, run as code over a fabricated evaluation — beside what a structure-only validator
would have caught. The card is
[component 37](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/37-evaluator-failure-pattern-catalog.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
contract.md            a fabricated contract: three axes and their thresholds
evaluation-sloppy.md   a fabricated evaluation for a CSV importer, written to trip the
                       catalog: praise around a flaw, vague words, a hedged blocker, a
                       comparison with the last attempt, an uncited score
bands.json             a fabricated calibration table with a model answer beside it
check_catalog.py       the eight checks, a structure-only mode, and a calibration mode
```

## Try it

```bash
python3 check_catalog.py                   # seven of eight checks trip; exits 1
python3 check_catalog.py --structure-only  # a structure validator's view: all clear; exits 0
python3 check_catalog.py --calibration     # a model answer against its own bands; exits 1
```

**The eight checks.** Praise outnumbers flaws, a vague word sits in scoring text, a hedge
sits beside a blocker, a score has no `file:line`, a failing axis is named by no blocker,
the text compares with the last attempt, and praise sits inside a failing section. Only
the axes-scored check is clear. Each one is a few lines of code, which is the point: the
catalog hands them to the evaluator to run by eye.

**The structure view.** `--structure-only` keeps the three checks a structure validator
could plausibly make. It finds nothing: the failing axis has *a* blocking issue, so the
"some blocker exists" test passes, though no blocker names the axis. Exit 0 here is the
finding, not a success.

**The calibration.** The model answer scores five of eight scenarios tested as 2. The
bands, a fabricated table in the same shape as a scoring guide's, put 62.5% in band 3 and
leave 30–45% and 75–95% with no band at all.

## What is deliberately missing

**An evaluator independent of the output.** In the source the checks run inside the
evaluator's own context, on its own draft. Here a script runs them on a file; whether
anything in the loop would do that is what the card says is absent.

**Judgement.** Praise is found by word list and sentence count, which mislabels both ways.
The catalog's ten patterns are not all mechanical; a praise sandwich is a matter of
position and attention, and no regex here claims otherwise.

**The fix, for the pattern.** A runner outside the grader that executes the mechanical
checks and passes its result to the gate, a per-axis blocker mapping, and model answers
checked against the bands they sit beside.
[Card 11](../../../cards/11-adversarial-role-separation.md) is the pattern this belongs to.
