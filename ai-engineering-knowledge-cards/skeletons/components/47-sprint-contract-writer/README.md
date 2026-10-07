# Skeleton — Sprint Contract Writer

A fresh writer with the flags the sprint-loop skill's contract script takes — sprint,
axes, thresholds, out-of-scope items, output path — and an audit of what it writes, and what
it writes over. The card is
[component 47](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/47-sprint-contract-writer.md);
the skill that runs it is [component 32](../32-role-separated-sprint-loop-orchestrator/), and
the script that reads what it writes is
[component 46](../46-evaluation-structure-validator/).

```
contract_writer.py            input validator, renderer and atomic write; --audit runs the
                              findings in a temporary directory and removes it
fixtures/template_outline.txt a short fabricated outline of the sections and columns a
                              contract template carries, for the shape comparison
```

## Try it

```bash
python3 -B contract_writer.py --audit                              # seven findings; exits 1
python3 -B contract_writer.py --sprint s1 \
  --axes '["correctness","error_handling"]' \
  --thresholds '{"correctness":4,"error_handling":3}' \
  --output unused.md                                               # two axes; refused, nothing written; exits 1
python3 -B contract_writer.py                                      # usage only; exits 2
```

**The second command** shows the one rule that fires: fewer than three axes is an error,
though its message calls three a recommendation. It refuses before anything is written.

**The audit** does the rest in a temporary directory. A contract is written, then written
again with every threshold at 1/5 — the second call succeeds, the version still reads 1, and
the directory holds one file. The output lacks two sections of the template outline and its
description column, its weights are a function of the thresholds, one out-of-scope item with
commas becomes three bullets, an axis listed twice is written twice, and an axis named with a
hyphen is written into a table the reader's pattern skips. Exit 1 marks those findings, not an
error.

## What is deliberately missing

**The reader.** The pattern a validator uses to see axis rows is restated here as a one-line
check; component 46's skeleton is deliberately not wired to this one.

**A refusing write.** A version check, a kept copy of the earlier contract and a superseded
status are the repair; none is applied.

**The template.** The outline is a few fabricated lines, not the template; the writer does not
read it, which is the finding.

**A shell, a model, a network.** None is used. The audit writes only to a temporary directory
it removes.
