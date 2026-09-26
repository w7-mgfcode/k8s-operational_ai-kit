# Skeleton — Scope Lock and Checkpoint Delivery

```
scope-lock.yaml       frozen before work: in scope, OUT of scope, environment,
                      ownership boundary, checkpoints with gates
detect.py             pre-fills it from the real tree; marks blocked workstreams
fixture-repo/         a small tree to detect against
HANDOFF-template.md   with the dead-ends section
HANDOFF-good.md       an actionable handoff
HANDOFF-bad.md        the usual kind
check_handoff.py      enforces next-step-#1
```

## Try it

```bash
python3 detect.py
python3 check_handoff.py HANDOFF-good.md    # exits 0
python3 check_handoff.py HANDOFF-bad.md     # exits 1
```

`detect.py` marks workstream C blocked because its input file does not exist.
Scoping work against a prerequisite nobody checked for is how a sprint plan
contains an item that was never possible.

It also prints the ownership boundary, which is the field people leave out. An
agent fixing a policy violation inside a vendored chart will correctly identify
the violation and incorrectly conclude it may edit the chart. Nothing stops
that except stating the boundary.

Compare the two handoffs. The bad one is not lazy — it is what a handoff looks
like when written at the end of a session by someone who wants to stop. "Continue
the TLS work" is a topic. The good one names a command, a file, a line and a
hypothesis, and its dead-ends section saves the next session an hour.

## What is deliberately missing

**The checkpoint gate.** `scope-lock.yaml` declares gates and nothing enforces
them. A checkpoint that reports without blocking is a progress bar.

**Amendment tracking.** Nothing detects that work drifted outside `in_scope`,
which is the failure the lock exists to prevent — the lock is a statement, not
a control.
