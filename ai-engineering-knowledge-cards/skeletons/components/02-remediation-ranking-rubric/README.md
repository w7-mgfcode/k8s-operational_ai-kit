# Skeleton — Remediation Ranking Rubric

The rubric on its own, and a stress test of how far its answer can be trusted. The
card is [component 02](../../../component-cards/skills/infrastructure-issue-investigator/references/02-remediation-ranking-rubric.md);
the skill that loads the rubric is
[component 01](../01-infrastructure-issue-investigator/).

```
rubric.json       seven criteria, each with three written anchors (0/1/2) and a
                  weight; their order is the tie-break order
candidates.json   five fabricated fixes for one OOM incident, scored as a model
                  would score them, plus a root_cause field the rubric never reads
rank.py           ranks, renders the /12 display, and with --stress perturbs it
```

## Try it

```bash
python3 rank.py              # the ranking as the rubric produces it; exits 0
python3 rank.py --stress     # the same ranking under small changes; exits 1
```

**The first run.** A and D tie at 21/24, and A wins on reuse, the first criterion
where they differ. Then look at the last column. The rubric renders scores on
/12 by halving; a 21 becomes 10.5, which the fixed display shape has no place for.
Round it and A, D and E all read 10/12 — three options the /24 scores separate
look identical. (Python rounds half to even, so 10.5 becomes 10; round half up
and you get a different wrong picture, with 11 against 10.)

**The stress run.** Each weight is moved by one, in each direction. Three of those
fourteen single-step changes hand the win to D. Then the one criterion the rubric
does not have — does the option address the evidence? — is added at the same
weight as reuse, and D and E overtake A by six and five points. A fix that raises
a limit around a cache that overflows it was never the best answer; it was the
answer the weights preferred.

That is the argument for the gate that follows the rubric in the skill: the
table goes to a human with the tie and the runner-up visible, and nothing
proceeds on the rubric's say-so. Exit 1 here marks that finding, not an error.

## What is deliberately missing

**The judgement.** Every 0/1/2 in `candidates.json` is fixed. In the real skill a
model assigns them from the written anchors with no citation required, which is
where most of the rubric's uncertainty actually lives — perturbing weights, as
`--stress` does, is the part that can be computed.

**The rendered table and rationale.** The source mandated one table layout and a
two-sentence rationale for the top pick; this prints plain columns.

**The repository checks behind the scores.** Reuse, workstream, dependencies and
conventions are scored in the source by reading the infrastructure repository
and the current branch. Here they are numbers in a file.
