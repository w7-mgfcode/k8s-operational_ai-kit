# Skeleton — Triage Table Renderer

Parsed benchmark findings rendered into the triage table, and a check of what
that table's dispositions actually record. The card is
[component 22](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/22-triage-table-renderer.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/),
the parser that feeds it is [component 24](../24-benchmark-report-parser/), and
the template whose legend it restates is [component 11](../11-benchmark-triage-table/).

```
parsed-findings.json  fabricated parser output: five failures, two warnings,
                      two passes, each with the parser's likely-NA flag
template-legend.md    the template's copy of the disposition legend
render.py             the table to stdout; with --check, dispositions by
                      origin, the "every failure dispositioned" gate, and the
                      two legends compared
```

## Try it

```bash
python3 render.py            # the table; exits 0
python3 render.py --check    # what the table records; exits 1
```

**The table.** Every disposition is NA or TBD. The two NA rows carry the
rationale "deprecated — not applicable" and read as decided. The first is right:
it asks for a plugin removed from Kubernetes. The second is not: its description
says the control moved to the policy engine — but the eighty-character cut
removes exactly that clause, so a reader sees "formerly enforced by" and nothing
after it. Rows also sort as text, so `1.2.12` lands above `1.2.7`.

**The check.** Two dispositions came from a pattern match, three are
placeholders, none from a person. The gate a reader would write — no failure
row with an empty disposition — passes anyway. Then the legend: three of the
four codes are explained in different words here and in the template.

Exit 1 marks those findings, not an error.

## What is deliberately missing

**YAML output.** The component's YAML path needs a third-party library and has
no fallback. A skeleton cannot import it, which is the failure in miniature.

**An output file.** The component writes into the sprint's output directory and
overwrites what is there; this one prints, so the repository stays clean.

**The pattern match itself.** The likely-NA flag is set by the parser;
[component 24](../24-benchmark-report-parser/)'s skeleton shows how it is set.

**The fix.** A suggestion column beside a disposition column only a human fills,
and a gate that counts human entries. Small, and absent from the source.
