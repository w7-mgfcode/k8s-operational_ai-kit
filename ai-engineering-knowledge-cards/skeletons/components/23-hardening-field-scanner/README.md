# Skeleton — Hardening Field Scanner

The inventory that seeds the admission-policy workstream, run two ways over the
same roles: by field name pooled per role, as the component does it, and by
value per container over owned roles only. The card is
[component 23](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/23-hardening-field-scanner.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
roles/            six fabricated roles: one hardened, one naming every field with
                  the insecure value, one with a hardened container and a bare
                  sidecar, one that overrides nothing, one vendored wrapper, one
                  node-level collector that must run privileged
owned.json        the roles the team maintains — workstream C's boundary
exceptions.json   the elevated-access list as three parts of the skill keep it
scan.py           both methods side by side; --presence prints the first alone
```

## Try it

```bash
python3 scan.py               # both methods; exits 1 where they disagree
python3 scan.py --presence    # the component's method alone, as JSON; exits 0
```

**The comparison.** Three of six roles come out differently. The batch runner
is clean by field name: every field is there, and every value is the insecure
one. The web frontend is clean because its main container is hardened; the
sidecar beside it sets nothing, and pooling the role's files hides it. The
vendored ingress wrapper lands in the violation list workstream C would work
from, although the team does not own it. Only the role with no container
settings at all is caught by both.

**Below the table.** Seven field names are listed and four are judged; user,
group and filesystem-group IDs are never checked. And the three
elevated-access lists name five roles between them and agree on two.

Exit 1 marks the disagreement — the demonstration, not an error.

## What is deliberately missing

**A YAML parser.** Container blocks are found with line patterns, which is the
standard library's honest limit and the reason the component searched text. A
values file that nests containers differently, or lists environment variables
as `- name:` entries, would confuse both methods.

**The fix-type guess.** The component also guesses whether a role can be fixed
through Helm values or needs a template edit. The guess rests on the same word
search, so it is left out rather than reproduced.

**Cluster evidence.** The real check of a hardening gap is the admission
engine's policy report. Neither method here, nor the component, reads one;
both inspect the repository and infer.

**The pattern's gap.** Card [17](../../../cards/17-blast-radius-gating.md)
scopes changes by who they affect. Here the scope — owned roles — is an input
the component never takes, so the value method has to supply it.
