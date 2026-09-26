# Skeleton — Infrastructure Issue Investigator

The phases of a read-only planning skill, run end to end against fixture data. The
card is [component 01](../../../component-cards/skill/01-infrastructure-issue-investigator.md).

```
investigate.py      the seven phases; web search and the brainstorm model call are
                    named stubs that print
cluster.json        fabricated read-only command output for one namespace: a
                    Deployment crash-looping on OOMKilled, with a fake password and
                    a fake token in its output
repo.json           a fabricated infrastructure-as-code repository: branch, file
                    paths, recent commits — including one restricted vault file
candidates.json     what the brainstorm call would return: four scored options,
                    two of which tie
rubric.json         seven weighted criteria; their order is the tie-break order
plan-template.md    the plan the last phase renders, with its redaction-review block
```

## Try it

```bash
python3 investigate.py                    # full run on dev; prints the plan, writes nothing
python3 investigate.py --cluster prod     # prod guard trips; exits 1
python3 investigate.py --symptom tls      # a "diagnostic" the deny list misses; exits 1
python3 investigate.py --save plans       # asks before writing; answer anything but y to skip
```

**The full run.** Watch phase 2b: the password and token in `cluster.json` never
reach the plan — the redaction-review block names what was taken out, so a
reader can tell something was there. Phase 3 prints the web query after
hygiene: the cluster, namespace and workload names are gone before anything
would leave the machine. The restricted vault file is listed and not opened.

**The ranking.** Options A and D tie at 21/24; A wins on criterion order because
reuse comes first. Now read the signals the plan quotes: a 512 MB cache inside a
256 Mi memory limit. D fixes the cause; A buys headroom. The rubric is honest about
what it optimizes — fit with the repository — and root cause is not one of its
seven criteria. That is why the rank gate asks a human, and why the gate is not
optional.

**The prod guard.** Anything that does not resolve to `dev` stops at intake unless
`--confirm-prod` is passed, and stays read-only after it is.

**The TLS symptom.** The source skill's own diagnostic catalogue contained a probe
that runs a throwaway `curl` pod. `run` is not on the deny list, because the list
names the write verbs someone remembered. An allow list of read verbs catches it.
The script stops there on purpose — this is [card 16](../../../cards/16-the-permission-ladder.md)'s
point that only an enforced rung counts, observed in one component.

## What is deliberately missing

**The cluster, the web and the model.** Every command reads `cluster.json`, web
search is a stub that prints its query, and the brainstorm step loads
`candidates.json` instead of generating options. The scores in that file are what
a model would have proposed; the script only weights and ranks them.

**Human judgement at the gates.** The real skill stops at every gate and asks, one
question at a time. Here the rank gate is auto-acknowledged, which is exactly
the wrong default for the tie above — the prototype shows where the question goes,
not the answer to it.

**The rework loop.** The source allowed up to three rounds of revising the plan and
then force-saved it with the open concerns listed. There is no loop here.

**A real redactor.** Three patterns, enough for the fixture. The full version,
and the formats it cannot recognize, are [card 18](../../../cards/18-the-redaction-boundary.md)'s
skeleton.

**Execution.** Neither this prototype nor the component it models changes anything.
The plan is the output; applying it happens elsewhere, under a permission ladder.
