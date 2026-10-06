# Skeleton — Symptom-Class Diagnostic Playbook

A diagnostic command catalogue, the step that picks one block of it for a symptom,
and a linter that reads every block. The card is
[component 04](../../../component-cards/skills/infrastructure-issue-investigator/references/04-symptom-diagnostic-playbook.md);
the skill that loads the playbook is
[component 01](../01-infrastructure-issue-investigator/).

```
catalogue.json   a fabricated four-class catalogue: a baseline that always runs and
                 one command block per symptom class. Written for this skeleton,
                 not copied — but built with the source playbook's kinds of defect
                 on purpose, so the linter has something real to find
playbook.py      classifies a symptom, renders the matching block, or lints it all
```

## Try it

```bash
python3 playbook.py                                                  # one class; exits 0
python3 playbook.py --symptom "pvc stuck, tls errors, helm upgrade failed"   # three; delegates
python3 playbook.py --lint                                           # 16 defects; exits 1
```

**The first run** is the playbook doing its job: an OOM symptom selects one class, the
baseline and that class's three commands are rendered, and the other three classes are
never loaded ([card 02](../../../cards/02-progressive-disclosure.md) — the catalogue
costs a block, not the whole file).

**The second** spans three classes, which is the source's threshold for handing
diagnosis to a broader troubleshooting skill instead of stacking blocks.

**The lint** reads commands the first run never showed. Every baseline line pins
`--context`; not one class-block line does, so the commands chosen *because of the
symptom* run against whatever kubectl context happens to be current — not
necessarily the cluster the prod guard classified. The certificate block contains a
`run`, which creates a pod. A namespace filter by `grep` matches every namespace
that contains the name. One command pipes to `jq`, which the playbook never
declares. And `helm get values` is flagged because it can print secrets, making it
safe only if the redactor is actually wired to its output.

Every one of those kinds of defect is in the source playbook. The planted counts
here are this catalogue's own.

## What is deliberately missing

**Execution.** Nothing runs; `playbook.py` prints commands. The point is what the
catalogue would have done, which is visible without a cluster.

**Most of the catalogue.** Four classes instead of ten, three commands each instead of
four to seven.

**Class selection by a model.** The source left classification to the model reading
the symptom. Here it is keyword matching, which is cruder and easier to inspect.

**The fix, applied.** A catalogue that passed its own lint would template the context
into every line from one variable and run each block through a read-verb allow list
at load time. This one is left failing so the lint can show it.
