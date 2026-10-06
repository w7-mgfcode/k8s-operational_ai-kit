# Skeleton — Component Tier Table

The two copies of one blast-radius classification, compared, and a tier derived
from each component's dependent count to set beside the tier it was given by hand.
The card is
[component 13](../../../component-cards/skills/workstream-hardening-orchestrator/references/13-component-tier-table.md);
its script copy belongs to [component 21](../21-tier-lookup-gate/), and the skill
is [component 08](../08-workstream-hardening-orchestrator/).

```
tiers.md     a fabricated prose tier table: four tiers, a shared-failure table,
             a confirmation table — the reference the model reads
tiers.json   the lookup script's built-in copy of the same classification,
             maintained separately
compare.py   parses both, reports every disagreement, lists the shared systems
             the lookup cannot answer for, and derives tiers from counts
```

## Try it

```bash
python3 compare.py            # all three checks; exits 1
python3 compare.py --derive   # only the count-derived tiers; exits 1
```

**Check 1** finds a component only the script knows, three dependent lists that
differ — one of them next to a separate count of 24 that matches neither list — and
the HIGH tier's confirmation worded differently in each copy. **Check 2** asks the
script's copy about the four shared external systems the prose lists as single
points of failure; it has a row for none of them. **Check 3** applies a stated
counting rule to the prose table's own dependents column: the network layer cannot
be counted at all ("all pods"), and six other tiers do not follow from their counts —
a two-dependent component sits above a three-dependent one.

The threshold rule is this skeleton's choice, not the source's; the source had no
rule. Change `THRESHOLDS` and the disagreements move, but some remain, because the
tiers were written first. Exit 1 marks the findings.

## What is deliberately missing

**The fix.** One data file read by both the model and the lookup, and tiers computed
from a dependency graph — [card 17](../../../cards/17-blast-radius-gating.md)'s
[skeleton](../../../skeletons/17-blast-radius-gating/) keeps its matrix as data for
this reason. Building it here would hide the drift the card describes.

**The sprint section.** The source mapped each workstream to a tier, two of them to
ranges like "MEDIUM-HIGH" that no confirmation rule defines. Not reproduced.

**Confirmation as behaviour.** The confirmation rules are compared as wording; nothing
here asks anyone anything, which is also true of the source.
