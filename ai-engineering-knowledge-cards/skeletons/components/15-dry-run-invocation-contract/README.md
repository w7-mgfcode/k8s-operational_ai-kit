# Skeleton — Dry-Run-First Invocation Contract

The command shape every change in the hardening sprint goes through, and the one
control the source never had: a record that the check run happened. The card is
[component 15](../../../component-cards/skills/workstream-hardening-orchestrator/references/15-dry-run-invocation-contract.md);
the skill that carries it is [component 08](../08-workstream-hardening-orchestrator/).

```
contract.json             the invocation contract, operator values as ${VARIABLES}
contract-hardcoded.json   the same contract as one operator wrote it for themselves
                          (fabricated values)
session.json              a fabricated sprint session: check and apply runs in order
invoke.py                 builds the check/apply pair, replays the session against an
                          in-memory ledger of check runs, audits both contracts
```

## Try it

```bash
python3 invoke.py                                  # session + audit; exits 1
python3 invoke.py --pair registry                  # one role's pair; exits 0
python3 invoke.py --audit contract-hardcoded.json  # exits 1
python3 invoke.py --audit contract.json            # exits 0
```

**The pair.** The two lines are identical except for the last flag. That is the
contract's good idea, and also why the rule is fragile: the apply is one deleted
flag away from the check.

**The session.** Four of seven runs are refused. One apply has no check at all.
One check misspells the tag — the real tool would select no tasks, report no
changes and succeed, which is a dry-run that checked nothing. The apply that
follows it has no matching check either. The last apply adds a variable the
check never saw. In the source each of these goes to the operator, because "check
first, no exceptions" is a sentence, not a ledger.

**The audit.** The contract with `${VARIABLES}` works for anyone. The other one
names one operator's key, kubeconfig and password helper — the shape the source
reference had. Exit 1 marks the findings, not an error.

## What is deliberately missing

**Execution.** `run_playbook()` prints. The source never ran these commands
either; it generated them for an operator, and so does this.

**A durable ledger.** Here it lives for one process. A real one would be written
by a wrapper around the tool and read back before every apply, which is the
change that makes the rule enforceable rather than advised.

**The rest of the reference.** Build targets, CI stages, phase order and the
new-role checklist are not modelled. The lint question — blocking or not, which
the reference and the gate catalogue answer differently — is
[component 19](../19-workstream-gate-catalogue/)'s to show.
