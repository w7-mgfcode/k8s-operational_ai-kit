# Skeleton — Seal-State Health Checker

The secrets-store health script the hardening orchestrator uses in its two
secrets-store workstreams, and a check of how its two modes fit together. The
card is
[component 29](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/29-seal-state-health-check.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
captured-plain.txt    what running the generated commands one by one prints:
                      three status tables, no section markers
captured-marked.txt   the same three tables, each under an '=== <pod> ===' line
captured-four.txt     four healthy pods, with markers
health.py             generate: the commands for the operator, as JSON
                      parse FILE: seal state per pod, as JSON
                      no arguments: the demonstration over all three fixtures
```

## Try it

```bash
python3 health.py generate                    # five checks and three unseal commands; exits 0
python3 health.py parse captured-marked.txt   # healthy; exits 0
python3 health.py parse captured-plain.txt    # "could not parse"; exits 0
python3 health.py                             # the demonstration; exits 1
```

**The two halves do not meet.** The commands generate mode prints produce
`captured-plain.txt`, and parse mode cannot read it: it splits on section
markers that only the recovery runbook's loop prints. A healthy set of four
pods reads as `4/3 pods unsealed` and not healthy, because the pod list is
fixed at three. And generate mode puts three interactive unseal commands in
the same output as the read-only checks.

Parse mode exits 0 healthy or not, as the component does. The demonstration
exits 1 to mark its findings.

## What is deliberately missing

**A cluster.** The status tables are fabricated in the format the secrets
store's CLI prints; nothing connects to anything.

**HA mode, version and the raw-output echo** the component also parses. They
do not change any finding.

**The fix.** Generate commands that print their own marker (or parse by
command), take the pod list from the cluster or the plan instead of a constant,
return non-zero when unhealthy, and put the unseal procedure in the runbook
([component 16](../16-recovery-runbook-set/)) rather than beside the checks.
