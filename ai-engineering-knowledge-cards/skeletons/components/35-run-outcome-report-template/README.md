# Skeleton — Run Outcome Report Template

The report a sprint-loop run ends with, rendered from a fabricated state the way the model
fills it, and a list of what the form cannot say about that run. The card is
[component 35](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/assets/35-run-outcome-report-template.md);
the skill that writes it is [component 32](../32-role-separated-sprint-loop-orchestrator/), and
the state it reads is the recorder's, in [component 45](../45-loop-state-recorder/).

```
state.json    a fabricated run of three sprints: one passed on its second try, one escalated
              with some iterations unscored, and one passed on a recorded override
vocab.json    the five word lists the loop's files use for one fact
outcome.py    render: the report from the state; --check: the gaps
```

## Try it

```bash
python3 outcome.py            # the report; exits 0
python3 outcome.py --check    # five findings; exits 1
```

**The report.** It reads as complete: a status, a table, a wall time. The third sprint says
*passed*.

**The check.** Exit 1 marks the findings, not an error. That *passed* is an override — the only
record is a sentence in a notes field, and the state's result for it is the same `pass` a real
pass writes. The run's status fits both *escalated* and *partially passed*, and nothing defines
the second. The blocker-count column has no source, because the state keeps no blocker list.
"Most-iterated axis" needs scores for every iteration, and two of the five iterations have none.
And five word lists name one fact, with no mapping between them.

## What is deliberately missing

**The per-sprint detail.** The real template also has a per-sprint score table against the
thresholds, a list of changes and issues resolved, an escalation section and a files-modified
list. They add length and no new finding.

**The wall-time rule.** The template says "if tracked"; this prototype derives it from
timestamps to show it can be, which the source does not do.

**The fix, for the pattern.** One status vocabulary shared by the files, a status for an
accepted override, and a report generated from the state instead of retyped from it.
[Card 19](../../../cards/19-scope-lock-and-checkpoint-delivery.md) holds the part of the
pattern that delivery at a checkpoint belongs to.
