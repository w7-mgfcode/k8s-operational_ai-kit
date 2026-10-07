# Skeleton — Benchmark Report Parser

The first step of the benchmark-triage workstream: result lines in, classified
findings out, with an approval flag on control-plane failures. The card is
[component 24](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/24-benchmark-report-parser.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
report.md     a fabricated CIS benchmark run: five sections, PASS/FAIL/WARN lines,
              one line written without brackets
expect.json   what a reviewer knows that the parser does not: which section is
              etcd, and which pre-marked control actually applies
parse.py      two result-line patterns tried in order, prefix classes, approval
              flag on control-plane FAILs, applicability guessed from the text;
              with --audit, what that design gets wrong
```

## Try it

```bash
python3 parse.py              # findings as JSON; exits 0
python3 parse.py --audit      # the classification checked; exits 1
```

**The JSON.** Seven FAILs, two of them flagged for platform-team approval, five
counted as actionable. It looks complete, and the triage table renderer would
take it as it is.

**The audit.** The two etcd FAILs are classed `other` with
`requires_approval: false`, because the etcd section is on no prefix list. Both
are certificate settings on the cluster's datastore, about as control-plane as a
finding gets, and the table would offer them for implementation without asking
the platform team. The second parsing branch matched nothing: the first
pattern's brackets are optional, so the unbracketed line it was written for had
already been taken. And of the two controls pre-marked not applicable, one names
the admission plugin that *replaced* the deprecated policy, which still applies.

Exit 1 marks those findings, not a parsing error.

## What is deliberately missing

**YAML output.** The component can emit YAML through a third-party parser,
which it imports at the point of use with no fallback. A standard-library
skeleton cannot import it; the card records the gap.

**A section map.** The fix is to classify by the report's own section headings,
which the parser already reads and stores, instead of by a hand-kept prefix
list. It is left out so the gap stays visible.

**The renderer.** Findings go on to the triage table
([component 22](../22-triage-table-renderer/)); this skeleton stops at the JSON.

**The pattern's gap.** Card [17](../../../cards/17-blast-radius-gating.md) asks
for authority to scale with what a change touches. Here the scale is a prefix
list, and a missing prefix silently lowers the bar.
