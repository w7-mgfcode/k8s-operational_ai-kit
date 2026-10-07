# Skeleton — Axis-Scored Evaluation Template

The form a grader fills in, filled three ways, and a structure check of the kind the loop runs
over the result. The card is
[component 34](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/assets/34-axis-scored-evaluation-template.md);
the skill that uses it is [component 32](../32-role-separated-sprint-loop-orchestrator/), and
the check is modelled on [component 46](../46-evaluation-structure-validator/).

```
template.md   a shortened evaluation template: summary, one scored section per axis with
              evidence, assessment and blockers, a blocking-issues summary, notes
contract.md   a fabricated contract: three axes named in snake_case, each with a threshold
scores.json   what a grader decided — scores, evidence, blockers, and each axis's display name
evaluate.py   fills the template; --check runs three fills through a structure check
```

## Try it

```bash
python3 evaluate.py            # the evaluation, filled with the contract's axis names; exits 0
python3 evaluate.py --check    # three fills through the check; exits 1
```

**The check.** Six findings; exit 1 marks them, not an error. Fill the template's
`[Axis Name]` slot with each axis's display name — what a reader of the template does — and
two of the three axes come back as unscored, because the contract writes `error_handling` and
the heading says `Error Handling`. Fill it with the contract's identifiers and the same
evaluation is valid. The third fill leaves every evidence slot as written and drops one blocker
from the summary, and the check calls it valid: it reads scores, labels and the summary, and
never the evidence or the per-axis blocker lines.

## What is deliberately missing

**The check's full rules.** The source's validator also warns when a blocker names no file and
rejects scores outside the scale. [Component 46](../46-evaluation-structure-validator/) has
that prototype; this one has only the rules the failures need.

**A model.** `fill()` assembles strings. The real step is a grader reading code.

**The fix, for the pattern.** One naming rule shared by the template and the contract, and
the check reading the sections it currently skips.
[Card 06](../../../cards/06-calibrated-degrees-of-freedom.md) is the part of the pattern a fixed
rubric belongs to; a rubric is only as fixed as what reads it.
