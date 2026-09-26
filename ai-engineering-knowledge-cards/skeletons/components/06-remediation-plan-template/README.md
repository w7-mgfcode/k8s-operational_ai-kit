# Skeleton — Remediation Plan Template

A plan template, a renderer that fills it from an investigation, and the checks the
source template never had. The card is
[component 06](../../../component-cards/reference/06-remediation-plan-template.md);
the skill that renders it is
[component 01](../01-infrastructure-issue-investigator/).

```
template.md          a fabricated, shortened plan template: frontmatter, context,
                     root cause, chosen option, steps, rollback, verification,
                     blast radius, environment progression, redaction review
investigation.json   what the earlier phases hand over — the OOM incident from
                     component 01, with the reviewer overriding the rubric's pick
bad-plan.md          a plan as the template allows it to come out, with eight
                     defects planted in it
plan.py              renders, checks, or both
```

## Try it

```bash
python3 plan.py                          # render and check; exits 0
python3 plan.py --print                  # ... and show the plan
python3 plan.py --check bad-plan.md      # eight defects; exits 1
```

**The rendered plan** passes. Read its Chosen Option: D, not A. The ranking rubric
([component 02](../02-remediation-ranking-rubric/)) put A first on a tie-break; the
reviewer at the rank gate picked the option that addresses the evidence, and the plan
names A as rejected with the reason. That is the gate doing its job, recorded where
the next person will see it.

**The bad plan** is what the template produces when nobody checks the output, and
every defect in it is one the template's shape permits:

- two `<…>` placeholders never filled in;
- frontmatter saying one cluster and option, the body saying another — the template
  asks for each fact twice;
- `confirmed` root cause with no real evidence under it;
- a progression table whose later rows say "same";
- a rollback section with no steps;
- an empty redaction review, which should list what was scrubbed or say
  "none detected".

Each check is a few lines. The source had none of them, so a saved plan was as good
as the attention of whoever filled it in.

## What is deliberately missing

**The operator-specific blocks.** The source template carried a block for supplying
the vault password through a named helper command and a local-execution block with a
kubeconfig naming pattern — machine-specific, and masked here rather than
fabricated.

**The rework loop and the save step.** The source allowed three rounds of revision,
then force-saved with open concerns listed, after asking where to write. This renders
to memory and writes nothing.

**References and open questions.** Omitted from the template to keep it short; they
carry no checkable structure.
