# Skeleton — Description-as-Router

```
colliding/          two descriptions that both claim "cluster problems"
corrected/          the same two capabilities with the contract applied
trigger-cases.json  three routing prompts to predict by hand; card 10's
                    harness replays its own five cases against corrected/
```

## Try it

```bash
cat colliding/*.md
cat corrected/*.md
python3 ../10-behavioral-evaluation-harness/harness.py     # replays against corrected/
```

Read `colliding/` first and predict which one fires on *"figure out why the
pods are crashing and then fix them"*. You cannot, and neither can the model —
both descriptions claim diagnosis, neither declines anything, and the choice
comes down to wording accidents that shift between sessions.

Now read `corrected/`. The boundary is explicit and **mutual**: one plans and
excludes executing, the other executes and excludes diagnosing, and each names
the other by name. That reciprocity is what turns two descriptions into a
routing table.

The third case in `trigger-cases.json` is deliberately ambiguous. It is the one
worth re-running after any description edit, because it is the case that breaks
first when a neighbour's triggers change.

## What is deliberately missing

**Referential integrity.** `corrected/log-investigator.md` excludes
`storage-doctor` and `cluster-audit`, and neither exists here. Nothing checks
that an exclusion names a real sibling, so renaming or deleting a capability
silently invalidates every exclusion pointing at it. The routing table has
referential integrity that nothing enforces.

**The length and person checks.** A description can drift past the character
budget or slip into first person and still route — until it does not.
[Card 09's validator](../09-scaffold-validate-package/) implements those checks;
they are not repeated here.

**Real routing.** These are files. The only way to know whether they route as
intended is to replay prompts through an actual runtime — which is
[card 10](../10-behavioral-evaluation-harness/), which fails two of its
five cases against `corrected/`: one prompt fires a skill when nothing
should, and the ambiguous one fires nothing.
