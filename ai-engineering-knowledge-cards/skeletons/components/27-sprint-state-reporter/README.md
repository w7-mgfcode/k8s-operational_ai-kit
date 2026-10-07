# Skeleton — Sprint State Reporter

The script the hardening orchestrator calls for every checkpoint report, and a
check of what it passes through without looking. The card is
[component 27](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/27-sprint-state-reporter.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
state.json   a fabricated sprint state: five workstreams, three triggers, three
             checkpoints — mid-sprint, with workstream A still in progress
status.py    renders the state as a table, Markdown or JSON; --update applies a
             status change in memory; --audit reports what the reporter never checks
```

## Try it

```bash
python3 status.py                                   # the table view; exits 0
python3 status.py --format markdown --checkpoint C  # the checkpoint C report; exits 0
python3 status.py --update B --status done-ish      # accepted; nothing is saved; exits 0
python3 status.py --audit                           # four findings; exits 1
```

**The reports.** Run the second command again with `--checkpoint A`. The output
is the same, byte for byte: the argument is accepted and never read, so the end
of the sprint and its first evening get one report. The table view, the default,
does not show the triggers at all.

**The audit.** `done-ish` is not in the documented status vocabulary and is
accepted anyway. Then the two lines that matter: the report says workstream B
has no blockers, while B waits on A and on two unresolved triggers; and it shows
D as complete while the platform-approval trigger that gates D is still pending.
Nothing in the reporter compares a workstream with its dependencies or
triggers. Exit 1 marks those findings, not an error.

## What is deliberately missing

**Writing the state file.** The component rewrites the file in place on every
update. Here `--update` prints the change and saves nothing, so the fixture
stays as committed.

**The initializer.** The component can also create a fresh state file from a
structure in its own code, without reading the template asset that documents
it. [Component 10](../10-sprint-state-file/) shows what that duplication drifts
into.

**The fix.** A status enum on update, a checkpoint filter on render, and a
`blocked_by` column computed from dependencies and trigger states — a few dozen
lines, none of which the source had. Adding them here would hide what the card
describes; [card 19](../../../cards/19-scope-lock-and-checkpoint-delivery.md)
describes what checkpoint delivery needs from them.
