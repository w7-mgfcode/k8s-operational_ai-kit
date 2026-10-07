# Skeleton — Workstream Hardening Orchestrator

The sprint loop the hardening skill describes — scope lock, tier-gated confirmation,
operator hand-off, checkpoints — run as code, and a check of the state file the source
skill would leave behind. The card is
[component 08](../../../component-cards/skills/workstream-hardening-orchestrator/08-workstream-hardening-orchestrator.md).

```
sprint.json      a fabricated sprint state: five workstreams in three priority bands,
                 the deep-work slice of D, three triggers and three checkpoints —
                 with workstream B already marked in progress
tiers.json       a fabricated tier table for generic components, and the one
                 component that always asks
orchestrate.py   the loop: confirm() and hand_to_operator() are named stubs that
                 print; --audit compares the state file with its own triggers
```

## Try it

```bash
python3 orchestrate.py            # the sprint as the skill describes it; exits 0
python3 orchestrate.py --audit    # the state file against its triggers; exits 1
```

**The run.** Workstream A asks before it touches the secrets store, because that component
always asks; C asks once, because its component is medium; E only notifies. No cluster
command runs — each one is printed as a dry-run and apply pair for an operator. B is paused,
because the transit schema is unresolved, and so is the control-plane slice of D. This
prototype enforces both pauses. The source skill wrote them as prose.

**The audit.** The same `sprint.json` already has B in progress. A reporter built like the
source's prints the table and has nothing to say about it; the audit, reading the same file
with the skill's own rules, finds B past an open trigger. The table that follows says where
each rule lived in the source: five of six in prose, and the one in code runs commands
rather than refusing them. Exit 1 marks that finding, not an error.

## What is deliberately missing

**Remediation.** Nothing edits a role. The workstreams' content — TLS, unseal, policy
fields, benchmark triage, hygiene — lives in the reference and script cards, each with its
own skeleton.

**The subagents and the scripts.** Tier lookup, scope detection, triage and validation are
inlined here as a dictionary lookup and a loop; components 21 to 29 and 30 to 31 have
their own prototypes.

**A real confirmation.** `confirm()` always says yes. In the source, the model asks in chat
and nothing records the answer; here, nothing records it either.

**Enforcement in the source's sense.** The pauses this loop applies are what the card's
*What is deliberately missing* asks for. The audit is there to show what the source did
without them.
