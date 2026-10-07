# Skeleton — Workstream Gate Runner

The per-workstream validation script the hardening orchestrator runs after every
change, and a check of what its gates let through. The card is
[component 28](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/28-workstream-gate-runner.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
fixture-repo/        a fabricated infrastructure repository at the start of a sprint:
                     two task files that are still stubs, an output directory from
                     an earlier sprint, and an empty one for the current sprint
plan.json            the current sprint's name and output directory
local-results.json   the exit codes the stubbed lint and syntax commands return
run_gates.py         the gate table for five workstreams; offline gates run, cluster
                     commands are printed and labelled read or write; --audit
```

## Try it

```bash
python3 run_gates.py --workstream A --plan plan.json                    # PASS; exits 0
python3 run_gates.py --workstream A --plan no-such-file.json            # PASS again; exits 0
python3 run_gates.py --workstream B --plan plan.json --cluster-access   # PASS, and a write to run; exits 0
python3 run_gates.py --audit                                            # eight findings; exits 1
```

The `[stub] run_local:` lines on stderr stand where the component opens a shell.

**Workstream A passes** with lint failing, because lint is never blocking, and
with its TLS gate satisfied by a task file that is still the stub the role was
scaffolded with — no work has been done. The second command passes too: the
plan argument is required and never opened.

**The audit** adds the rest. Workstream D's gate globs every dated output
directory and finds a triage table from a sprint two months old. Workstream E's
gate looks for a hygiene report that no step of the skill writes. And
workstream B's cluster "validation" list deletes a pod. Exit 1 marks those
findings, not an error.

## What is deliberately missing

**A shell.** `run_local()` prints the command and returns a recorded exit code.
The component runs the same commands through a shell in the target repository,
which is the point of one finding: a skill whose rule is to generate commands
for an operator runs some of them itself.

**Per-workstream substance.** The real gate table also lists a policy-report
delta and a benchmark re-scan, all as commands for the operator. They are
omitted; none of them is checked by the runner either.

**The fix, for the pattern.** Gates that read the plan for the current output
directory, a content check instead of a file-exists check, lint as blocking
where the catalogue says so, and destructive commands moved out of the
validation list into the rollback plan.
[Card 17](../../../cards/17-blast-radius-gating.md) is the part of the pattern
the last one belongs to.
