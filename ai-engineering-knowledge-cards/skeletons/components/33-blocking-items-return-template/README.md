# Skeleton — Blocking-Items Return Template

The report a failed sprint sends back to the builder, filled from a grader's evaluation the
way the model fills it, and a check of one that was saved by hand. The card is
[component 33](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/assets/33-blocking-items-return-template.md);
the skill that sends it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
template.md      a shortened return template: a rule line, one block per blocking item
                 with five fields, and two constraints
evaluation.md    a fabricated evaluation with three blocking issues and one non-blocking note
run.json         the sprint, the iteration, the contract's thresholds and the scores
saved-delta.md   a return as it might be saved by hand — close to right
delta.py         render: fill the template; --check: compare the saved return with the evaluation
```

## Try it

```bash
python3 delta.py            # the return rendered from the evaluation; exits 0
python3 delta.py --check    # the saved return against the evaluation; exits 1
```

**The render.** Three items, each carrying the axis, the score *and the threshold*, a location
and a fix. It is the document the builder reads on its next attempt.

**The check.** Five findings; exit 1 marks them, not an error. The saved return has three items
and the evaluation has three blockers, so a count passes — but one blocker was swapped for a
note the evaluation marked non-blocking. One slot was left as written. Every item shows the
builder the threshold it is graded against, which the role references tell it not to use; and
the last field asks for the minimum fix, from a grader told to name problems and not fixes.

## What is deliberately missing

**A generator for the return.** In the source no script writes it; the model copies items by
hand, and the check here is the comparison nothing there performs.

**The rest of the template.** The source's version also states the sprint scope rule at length
and asks the builder to record which items it addressed.

**The fix, for the pattern.** Items generated from the evaluation's blocker list rather than
retyped, the score and threshold left out of what the builder sees, and the last field limited
to what a passing result looks like. [Card 11](../../../cards/11-adversarial-role-separation.md)
holds the part of the pattern each one belongs to.
