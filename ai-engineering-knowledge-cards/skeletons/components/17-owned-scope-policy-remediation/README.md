# Skeleton — Owned-Scope Policy Remediation Guide

The guide's offline inventory beside one that reads containers and values, and
the two scope questions the guide leaves to chance. The card is
[component 17](../../../component-cards/skills/workstream-hardening-orchestrator/references/17-owned-scope-policy-remediation.md);
the skill whose workstream uses it is [component 08](../08-workstream-hardening-orchestrator/).

```
roles/          a fabricated role tree: a two-container deployment with one
                container hardened, a values file that sets every field to the
                unsafe value, a clean role, two node-level agents, and a role
                vendored from an upstream chart
scope.json      the roles the team owns, and three exception lists — as the
                guide, the scanner script and the scan subagent each kept one
inventory.py    file-level and per-container inventories side by side, the
                exception lists compared, and the scope the detector would use
```

## Try it

```bash
python3 inventory.py                 # all three sections; exits 1
python3 inventory.py --method file   # the guide's method alone; exits 0
```

**Run the guide's method alone first.** Two of six files look clean. Then run
both: the API deployment is clean only because its first container mentions every
field — the sidecar below it has none. The worker's values file mentions every
field and sets each one to the unsafe value. The guide's method asks whether a
word appears in a file, so both pass.

**The exception lists.** Three roles are exceptions everywhere; three more are
exceptions in one list only, so whether they are fixed or excused depends on
which artifact the model happens to read.

**The scope.** The vendored ingress role enters the inventory because the
source's scope detector lists every role as owned; the guide's "ask the user if
unsure" never gets the chance to fire. Exit 1 marks the six disagreements.

## What is deliberately missing

**Real manifest parsing.** Containers are split at `- name:` lines and fields
read with regular expressions. The standard library has no YAML parser, and
rendered chart values are not modelled at all.

**Policy reports.** The cluster-aware half of the guide — what the policy engine
actually reports — is absent. So is the guide's other blind spot: offline, only
the four fields it names can be checked, whatever the deployed policies say.

**The fixes.** The prototype measures; it does not edit roles, prioritise or
validate.
