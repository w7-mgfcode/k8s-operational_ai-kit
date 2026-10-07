# Skeleton — Secrets-Store TLS and Auto-Unseal Guide

Workstream A's TLS change applied to a fabricated repository, rolled back two
ways, and probed two ways. The card is
[component 20](../../../component-cards/skills/workstream-hardening-orchestrator/references/20-secrets-store-tls-unseal-guide.md);
the skill that loads it is [component 08](../08-workstream-hardening-orchestrator/),
and the planner whose rollback it compares is [component 25](../25-static-rollback-planner/).

```
rollout.py   a repository as a dict of five files and a "last commit" dict;
             the TLS edits, the guide's four-step rollback, the planner's
             one-file restore, and a readiness probe with and without
             certificate verification
```

## Try it

```bash
python3 rollout.py                 # rollbacks and probe; exits 1
python3 rollout.py --only rollback # the two rollbacks; exits 1
python3 rollout.py --only probe    # the probe alone; exits 1
```

**The rollbacks.** The change touches a feature flag, the listener, the
cluster-join addresses and the probes, and fills a TLS task file. The guide's
rollback reverts the four and leaves only the certificate request behind. The
planner's command restores the one task file — so the listener, the join
addresses and the probes all keep TLS. Commit the change before finding it
unstable, and restoring from the last commit changes nothing at all.

**The probe.** The certificate the fabricated task file requests leaves out one
replica's peer name. The guide's probe skips verification and reports that
replica ready; a probe that checks issuer and name does not. A self-signed
certificate from a failed issue passes the same way.

Exit 1 marks those findings, not an error.

## What is deliberately missing

**Auto-unseal.** The transit seal, the encrypted token and the Shamir migration
need a store to demonstrate anything; the card describes them. The structural
point — removing manual unseal needs one last manual unseal — is not something
a fixture can show more clearly than a sentence.

**The sibling deployment's file.** The guide points at a file with live tokens
and forbids copying it. A fabricated version would teach nothing a restricted
path would not.

**The fifteen-minute window.** No time passes here; [component 29](../29-seal-state-health-check/)'s
skeleton shows the one-snapshot health check the window depends on.

**The fix.** A rollback generated from the edits, or one flag every TLS setting
reads, and a probe that uses the consumers' CA bundle. Each is small; the source
had none.
