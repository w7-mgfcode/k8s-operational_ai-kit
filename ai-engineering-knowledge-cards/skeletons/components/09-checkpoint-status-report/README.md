# Skeleton — Checkpoint Status Report Template

The report a hardening sprint is delivered in, filled from a sprint state the way the
model fills it, and a check of what the template lets through. The card is
[component 09](../../../component-cards/skills/workstream-hardening-orchestrator/assets/09-checkpoint-status-report.md);
the skill that fills it is [component 08](../08-workstream-hardening-orchestrator/).

```
template.md   a shortened report template: header, workstream rows, three trigger
              slots each listing its allowed words, four evidence lines — one with
              a pod count written into the text
state.json    a fabricated sprint state at checkpoint B, with the state file's own
              list of allowed trigger states and the pods the cluster really runs
render.py     fills the template to stdout; with --check, lists what is wrong with
              the result
```

## Try it

```bash
python3 render.py            # the rendered report; exits 0
python3 render.py --check    # the report, then its defects; exits 1
```

**The render.** It looks finished at a glance. Read the trigger table: the benchmark trigger
still shows its bracketed list of choices, because the state file says `pending_approval` and
the slot offers no such word. The health line still asks about all five pods, and the
violation counts were never supplied.

**The check.** Seven defects: five slots left as written, one trigger state the template has
no word for — it offers three of the five states the state file allows — and a pod count
that belongs to some other cluster. Nothing between filling and delivering looked for any of
them. Exit 1 marks that finding, not an error.

## What is deliberately missing

**Most of the template.** No risks, blockers, next actions or backlog; no checkpoint-letter
logic. The defects above need none of them.

**The fix.** Generating the trigger slots from the state file's vocabulary, taking the pod
count from the health check, and refusing to write a report with a bracket left in it. Each is
short; adding them here would hide what the card describes.

**The reporter.** The source's status script renders a different table shape and ignores its
checkpoint argument; [component 27](../27-sprint-state-reporter/) has that prototype.
