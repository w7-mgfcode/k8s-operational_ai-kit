# Skeleton — Loop Gate and History Harness

A fresh harness with the three subcommands the sprint-loop skill's gate script has — start,
history, gate — over fabricated state files, and an audit of what its gate lets through. The
card is
[component 44](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/44-loop-gate-and-history-harness.md);
the skill that runs it is [component 32](../32-role-separated-sprint-loop-orchestrator/), and
the script that writes the state it reads is
[component 45](../45-loop-state-recorder/).

```
loop_gate.py            init, history and gate over one JSON state file; --audit runs the
                        findings in a temporary directory and removes it
fixtures/recorded.json  a run of a small CSV-import sprint, one failed iteration recorded
                        the way a recorder writes it: a result and scores, no per-axis list
fixtures/flagged.json   an evaluation with a per-axis list, one axis flagged passing at 1
fixtures/failing.json   an evaluation with a per-axis list, one axis flagged failing
fixtures/thresholds.json  the contract thresholds the gate is never given
```

## Try it

```bash
python3 -B loop_gate.py gate --state fixtures/recorded.json     # says pass; exits 0
python3 -B loop_gate.py history --state fixtures/recorded.json  # three entries; exits 0
python3 -B loop_gate.py --audit                                 # eight findings; exits 1
python3 -B loop_gate.py                                         # usage only; exits 2
```

**The first command is the finding.** `recorded.json` holds one iteration whose result is
`fail`, and the gate reports `pass` and "all axes pass". The recorder's entry has a result and
scores; the gate looks for a per-axis list, finds none, and "every entry passes" is true of an
empty list.

**The audit** adds the rest: a flag that outranks a score, a `fail` verdict that exits 0, a
refusal that exits 0, a force flag that empties the history, a mistyped path that reads as an
empty run, a flags-only invocation the parser rejects, and the absence of any command that
moves a phase. Exit 1 marks those findings, not an error.

## What is deliberately missing

**The recorder.** This harness reads state; the script that writes it is component 45's
skeleton, and the two are deliberately not wired together here — the mismatch between what one
writes and the other reads is the finding.

**A fixed gate.** A gate that read the contract's thresholds and the recorded scores, and put
the verdict in the exit code, is the repair; it is not applied.

**A shell, a model, a network.** None is used. The audit reads fixtures and writes only to a
temporary directory it removes.
