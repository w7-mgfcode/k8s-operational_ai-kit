# Skeleton — Axis Scoring Guide

A scoring guide's calibration table and its "not applicable" rule, audited the way a
reader would apply them. The card is
[component 41](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/41-axis-scoring-guide.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
bands.json     a fabricated calibration table: two axes with bands, two with none,
               and the pass threshold for each
calibrate.py   gap finder, band lookup, and the two readings of "not applicable"
```

## Try it

```bash
python3 calibrate.py --audit                              # gaps and bare axes; exits 1
python3 calibrate.py --coverage 0.6                       # falls in the score-3 band; exits 0
python3 calibrate.py --coverage 0.35                      # falls in no band; exits 1
python3 calibrate.py --not-applicable --threshold 4       # a free 5, passing; exits 1
python3 calibrate.py --not-applicable --threshold 4 --excluded   # left out of the gate; exits 0
```

**The gaps.** Bands are written as ranges, and the ranges do not touch: a measurement
between two of them has no score, and the evaluator picks one with nothing to anchor it.
Two axes have checks and evidence lists but no bands at all.

**The free pass.** Scoring an axis that does not apply as the top score satisfies any
threshold, and a validator reading only the number cannot tell it from earned work.
`--excluded` is the other reading: the axis leaves the gate and claims nothing.
Exit 1 marks the findings, not an error.

## What is deliberately missing

**The real numbers.** The bands, units and thresholds here are fabricated; the guide's
own are in the card. Only the shape of the gaps is faithful.

**An evaluator.** Nothing here measures coverage or decides applicability; both are
inputs on the command line.

**The fix, for the pattern.** Contiguous bands, an anchor for every axis, and an
explicit excluded state instead of a score. [Card 06](../../../cards/06-calibrated-degrees-of-freedom.md)
is the part of the pattern a calibrated scale belongs to.
