# Skeleton — Conditional Sprint Triggers

The three sprint triggers as state machines that are checked on every change and
turned into a decision about which workstreams may start — set beside a report
that only prints the states, which is what the source did. The card is
[component 14](../../../component-cards/skills/workstream-hardening-orchestrator/references/14-conditional-sprint-triggers.md);
the skill that reads it is [component 08](../08-workstream-hardening-orchestrator/).

```
events.json   a fabricated two-day sprint: workstream starts and completions,
              and trigger state changes — some legal, some not
triggers.py   the reference's transition table as data, a decision function
              from trigger states to startable workstreams, a replay of the
              log, and --print-only, the source-style report
```

## Try it

```bash
python3 triggers.py               # replay with checks; exits 1
python3 triggers.py --print-only  # the same log, reported the source's way; exits 0
```

**The replay.** TLS is marked stable ten minutes after workstream A completes, with no
evidence and no window start — a claim, flagged. Workstream B starts twenty minutes
later while the schema is still unresolved: a bypass. Next morning someone sets the
schema trigger to `stable`, a state from another trigger, and the transition table
rejects it. The platform-conflict trigger goes to `pending_approval`, control-plane work
starts anyway, and when the approval arrives there is no legal transition to record it:
the reference gives `pending_approval` no way out. Last, TLS turns unstable with B
already running. The final block says what may start now. Five findings; exit 1.

**The print-only report** shows the same log as the source's status output would: three
strings in a table, including `approved`, which is not a state at all. Nothing is
rejected and nothing is refused. Exit 0 — that is the point.

## What is deliberately missing

**The state file.** Here the event log is replayed in memory; the source kept only the
latest strings in a YAML file, with no history to replay. Keeping the history is part of
the fix and is not built.

**Health evidence.** The skeleton flags a `stable` with no evidence; it does not gather
any. In the source the evidence came from commands an operator ran by hand.

**Checkpoints.** The reference also defines the three checkpoints and their deliverables;
[component 09](../09-checkpoint-status-report/) covers the report.

**The pattern's gap.** [Card 19](../../../cards/19-scope-lock-and-checkpoint-delivery.md)
fixes the conditions in advance; it does not by itself make anything evaluate them.
