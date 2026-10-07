# Skeleton — Benchmark Triage Table Template

The triage table the hardening orchestrator's benchmark workstream produces, and
the check of it that the source never ran. The card is
[component 11](../../../component-cards/skills/workstream-hardening-orchestrator/assets/11-benchmark-triage-table.md);
the skill that uses it is [component 08](../08-workstream-hardening-orchestrator/).

```
template.md     a shortened triage template: header, failed-controls table,
                legend, four decision rules in prose, summary slots
filled.md       a fabricated filled table for eight failed controls — the kind
                of file that reaches a checkpoint after a few hand edits
check_table.py  reads the legend from template.md, carries the prose rules as
                constants, checks every row and recomputes the summary
```

## Try it

```bash
python3 check_table.py            # checks filled.md; exits 1
python3 check_table.py filled.md  # the same, with the path spelled out
```

**Reading the output.** Eight findings, in four kinds. One control-plane row is
set to `implement` with no approval anywhere — and the checker can only search the
rationale for the word, because the template gives approval no column. The etcd
row (section 2) is classified `other` and governed by none of the four rules. One
row is still `TBD`, one is a pre-filled `NA` with a placeholder rationale, and one
uses a disposition, `later`, that is not in the legend. Finally the summary
disagrees with the rows on three of its five counts.

The source's benchmark gate tested only that a triage file existed, so this table
would have passed it. Exit 1 marks the findings, not an error.

## What is deliberately missing

**The renderer and its second legend.** The source wrote the table from code with
its own copy of the legend and rules; see
[component 22](../22-triage-table-renderer/). Here the table is a fixture, so the
two-copies failure is described in the card rather than reproduced.

**Rules as data.** The checker transcribes the prose rules by hand, which is the
same drift risk one step removed. The fix the card points at — rules the template
and the checker both read — is not built here.

**Warnings, owners and targets.** Only the failed-controls table is checked; the
warnings table and the owner and sprint-target columns are not.

**The pattern's gap.** [Card 17](../../../cards/17-blast-radius-gating.md) gates by
dependent count; this template gates by benchmark section, a proxy that leaves
section 2 out.
