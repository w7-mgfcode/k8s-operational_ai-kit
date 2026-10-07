# Skeleton — Recovery Runbook Set

The lint the source runbooks never had: every step classified by what it does to
the cluster, and every change that nothing previews flagged. The card is
[component 16](../../../component-cards/skills/workstream-hardening-orchestrator/references/16-recovery-runbook-set.md);
the skill that carries the runbooks is [component 08](../08-workstream-hardening-orchestrator/).

```
runbooks.json   six fabricated runbooks — a stuck StatefulSet, a certificate that
                will not renew, a release rollback with and without a preview, a
                sealed secrets store, a cache flush behind a script
classify.py     classifies each step as read, guard, mutating, destructive or
                unknown, and flags unguarded changes and interactive steps
```

## Try it

```bash
python3 classify.py           # every step, with flags; exits 1
python3 classify.py --quiet   # the findings only; exits 1
```

**Read the first runbook top to bottom.** The StatefulSet is deleted in step 2
and the playbook is dry-run in step 3 — the preview arrives after the only step
that cannot be undone. That ordering is the shape of the source's stuck-update
runbook.

**Compare the two rollbacks.** The same `helm rollback` is flagged in one runbook
and not in the other; the difference is two steps that show what the target
revision contains before it is applied. Nothing in the source asked for those
steps, so some runbooks have them and most do not.

**The last runbook** shows the limit of the method: a script name says nothing
about what it deletes, so it comes out as unknown. Exit 1 marks the seven
findings, not an error.

## What is deliberately missing

**Per-object guards.** A guard step here covers everything after it in the same
runbook. A real lint would match the preview to the object it previews.

**Execution.** Nothing runs. The source never ran these commands either; the
skill's instruction not to is the only thing between them and the cluster, and
this prototype does not change that — it only makes the risk visible per step.

**The rest of the source.** No impact lines, no health suite, and no marker
format for the seal-state checker; [component 29](../29-seal-state-health-check/)
shows that coupling.
