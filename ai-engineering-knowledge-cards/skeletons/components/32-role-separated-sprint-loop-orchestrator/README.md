# Skeleton — Role-Separated Sprint Loop Orchestrator

A miniature of the loop the sprint skill drives — build, grade, gate, return the blockers —
and an audit of the places where the skill's own text promises more than anything holds. The
card is
[component 32](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/32-role-separated-sprint-loop-orchestrator.md).

```
fixtures.json   a fabricated sprint with a contract of three axes, two canned evaluations,
                the commands the skill text documents, the tools a general agent grants,
                and the sprint statuses a state recorder would offer
loop.py         run: the loop over the canned answers; audit: the gaps, one line each
```

## Try it

```bash
python3 loop.py run     # build, grade, gate, return one blocker, pass on the second try; exits 0
python3 loop.py audit   # seven findings; exits 1
python3 loop.py         # a subcommand is required; exits 2
```

The `[stub] call_model` lines on stderr stand where the skill spawns a subagent.

**The run.** The gate here is arithmetic over the contract: an axis below its threshold fails
the sprint, whatever the other axes score. It is the loop the pattern describes, working.

**The audit.** Exit 1 marks these findings, not an error. Three of the documented commands
are written without the subcommand the script they call requires, so all three exit 2. The
roles the prose says may not write are handed write tools by a general-purpose spawn. The
fallback for a failed spawn runs the role inline, so one context builds and grades. And one of
the three options offered to the owner at the iteration cap — accept the current state — has
no sprint status to be recorded in.

## What is deliberately missing

**A model and a spawn.** `call_model()` prints and returns a canned answer. The real skill
starts a subagent per role and cannot tell, from inside the loop, what tools it was given.

**The planning phase and the owner's approval.** The fixture starts at a frozen contract. The
real first phase expands a request into a spec and waits for the owner.

**The state file.** The loop keeps its counters in memory; the gate and recorder prototypes are
[component 44](../44-loop-gate-and-history-harness/) and
[component 45](../45-loop-state-recorder/).

**The fix, for the pattern.** One CLI form in the skill text, the gate reading the contract
rather than a field, tool grants in the spawn rather than in prose, and a status for the
owner's override. [Card 11](../../../cards/11-adversarial-role-separation.md) holds the part
of the pattern each one belongs to.
