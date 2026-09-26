# Skeleton — Calibrated Degrees of Freedom

One capability — incident response — at all three levels. The level is chosen
per step, not per capability.

```
high-freedom.md     triage    prose. many routes are valid.
medium-freedom.md   record    template. structure fixed, content free.
low-freedom.py      rollback  script. two parameters. fragile and irreversible.
fixture-state.json  example state for the script
```

## Try it

```bash
python3 low-freedom.py --component api --env staging      # exits 0
python3 low-freedom.py --component billing --env staging  # exits 1, two FAILs
python3 low-freedom.py --component api --env production   # exits 1, protected
```

Then read `high-freedom.md` and notice what it refuses to do: it never says
which command to run. That is not an omission. Triage depends on context the
author cannot see, and a script here would march an agent through a fixed
sequence that does not fit the incident.

Now read `low-freedom.py` and notice the inverse: no judgment, no adaptation,
five checks in a fixed order. A rollback with a schema migration in between is
destructive in a way that is expensive and silent, so the step gets no freedom
at all.

**The gradient tracks the cost of a wrong variant** — the same calculus as
[card 17](../../cards/17-blast-radius-gating.md).

## What is deliberately missing

**Marking in the format.** Nothing in these files tells a reviewer which parts
are binding and which are advisory. In a real capability all three live in one
skill, and a reader must infer the level from the form.

**Revision from observation.** These levels were chosen when the capability was
written, which is when the least was known. The card's validation list asks
whether the levels were ever revised from real runs; here, they have not been.
