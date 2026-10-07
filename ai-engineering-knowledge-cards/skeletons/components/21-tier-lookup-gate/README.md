# Skeleton — Tier Lookup Gate

The pre-change tier lookup, with the component's exit-code contract, run over a
fabricated tier table. The card is
[component 21](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/21-tier-lookup-gate.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/),
and the reference that holds the same table in prose is
[component 13](../13-component-tier-table/).

```
tiers.json      a fabricated table: eleven components, a tier and dependents
                each, and one hand-set dependents count
fixture-repo/   one role directory that exists but is not in the table
lookup.py       the lookup and its exit codes — 1 confirm, 2 review, 0 the
                rest; with no arguments, a table of lookups
```

## Try it

```bash
python3 lookup.py                                               # the demonstration; exits 1
python3 lookup.py --component secrets-store                     # high: exits 1, "confirm"
python3 lookup.py --component cert-isuer                        # a typo: exits 0, "proceed"
python3 lookup.py --component search-index --repo-path fixture-repo  # exits 2, "review"
python3 lookup.py --list                                        # usage error; exits 2
python3 lookup.py --list --component any                        # the table; exits 0
```

**The typo.** `cert-isuer` is one letter away from a critical component. The
gate does not know it, says so in its JSON, and exits 0 — the same code a
low-tier component gets. A caller that reads the exit code proceeds.

**The unknown role.** `search-index` exists in the repository. Without
`--repo-path` it is just as not-found as the typo. The review code, 2, is only
reachable with the path, and the skill never passes it.

**`--list`.** It exits 2 with a usage error on purpose: the component declares
the component argument required, so its own list flag cannot run alone. Passing
any component name gets past it.

**The count.** The store reports two dozen dependents and lists three. Every
other entry derives its count from its list; this one was typed in.

The no-argument run exits 1 because two lookups would proceed without anyone
being able to assess them. That is the finding, not an error.

## What is deliberately missing

**Impact text and change authority.** The component carries a sentence and an
approval line per entry; the exit code is the part that gates.

**The fix.** Exiting non-zero for a name the table does not know is one line.
It is left out so the failure stays visible.

**A measured tier.** Card 17's [skeleton](../../../skeletons/17-blast-radius-gating/)
classifies by counting dependents. This table, like the source's, asserts them.

**A reader of the exit code.** Nothing in the skill acts on it but the model.
