# Skeleton — Workstream Gate Catalogue

The sprint's gates as the reference writes them down, beside the same gates as
the runner encodes them, and a diff of the two. The card is
[component 19](../../../component-cards/skills/workstream-hardening-orchestrator/references/19-workstream-gate-catalogue.md);
the skill that reads it is [component 08](../08-workstream-hardening-orchestrator/),
and the runner it disagrees with is [component 28](../28-workstream-gate-runner/).

```
catalogue.json        the document half: one record per gate — kind, blocking,
                      wait, and the criterion in words. Fabricated
runner.json           the code half: the same gates as the runner checks them,
                      plus which files the skill's scripts actually write
runbook-excerpt.json  the recovery runbook set's own copy of the post-apply checks
diff_gates.py         joins the halves on workstream and gate, reports every
                      difference and every checked file nothing produces
```

## Try it

```bash
python3 diff_gates.py                  # all workstreams; exits 1
python3 diff_gates.py --workstream B   # the restart test alone; exits 1
```

**Lint first.** Three rows say the same thing: the document makes lint blocking,
the runner does not, so a role with lint errors validates as PASS. The sprint
reference says "treat it as blocking"; the code that decides PASS never read it.

**Then the three gates that cannot hold.** C's criterion — fewer violations than
at the start — has no row in the runner at all. D's criterion is about the
triage table's content and the runner checks that the file exists. E's runner
row checks a hygiene report that nothing in the skill writes, so it fails on a
fresh sprint and passes on any report left from an earlier one.

**The restart wait** is a smaller thing with the same cause: written twice, it
drifted to two numbers.

The health suite at the end is identical in both documents today. The script
says so and does not count it — the failure is that nothing would notice when
it stops being true. Exit 1 marks the disagreements, not an error.

## What is deliberately missing

**Running anything.** Gates here are records; no lint, no dry-run, no cluster.
The disagreement is visible without executing a gate, which is the point.

**The fix.** One table read by both the document renderer and the runner would
make this script unnecessary. Adding it here would hide what the card describes.

**The stale-file pass.** The runner's existence check matches a report from any
earlier sprint; [component 28](../28-workstream-gate-runner/)'s skeleton shows it.

**The constraint list.** The source's ten hard constraints, copied from another
document, are left out rather than fabricated.
