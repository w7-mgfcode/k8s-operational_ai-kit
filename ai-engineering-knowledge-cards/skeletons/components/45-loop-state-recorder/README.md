# Skeleton — Loop State Recorder

A fresh recorder with the three subcommands the sprint-loop skill's state script has —
phase, sprint, iteration — and an audit of what it records without asking. The card is
[component 45](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/45-loop-state-recorder.md);
the skill that calls it is [component 32](../32-role-separated-sprint-loop-orchestrator/),
and the script that reads what it writes is
[component 44](../44-loop-gate-and-history-harness/).

```
recorder.py              phase, sprint and iteration over one JSON state file; --audit runs
                         the findings in a temporary directory and removes it
fixtures/thresholds.json the contract thresholds the recorder is never given
```

## Try it

```bash
python3 -B recorder.py --audit                                  # eight findings; exits 1
python3 -B recorder.py phase --state run.json --phase nonsense  # an unknown phase; writes nothing; exits 1
python3 -B recorder.py                                          # usage only; exits 2
```

**The audit** drives the recorder through a run in a temporary directory. A fresh run goes
from its initial phase straight to generation. A sprint is escalated after three failures and
then reopened by one pass, with the counter at 4 of 3. A pass is stored beside scores that
are below every threshold, because the scores are never read. A mistyped path starts a new
run, a status of `banana` is accepted, a corrupt file raises, and the flags-only call a skill
might document exits 2. `override` is not a result the parser accepts, so accepting a failed
sprint can only be written down as a pass. Exit 1 marks those findings, not an error.

**The second command** shows the one check there is: a phase name must be one of seven. It is
rejected before the state file is touched, so nothing is written.

## What is deliberately missing

**A transition table and terminal states.** The repair — each phase naming what may precede
it, an escalated sprint accepting only a recorded human decision — is not applied; its absence
is the card.

**The gate.** Reading these entries and deciding from them is component 44's job, and its
skeleton is deliberately not wired to this one.

**A shell, a model, a network.** None is used. The audit writes only to a temporary directory
it removes.
