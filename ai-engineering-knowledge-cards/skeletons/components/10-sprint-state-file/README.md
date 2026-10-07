# Skeleton — Sprint State File Template

One sprint structure written three times — a template and two builders — and a diff of
the three. The card is
[component 10](../../../component-cards/skills/workstream-hardening-orchestrator/assets/10-sprint-state-file.md);
the skill whose phases read the file is [component 08](../08-workstream-hardening-orchestrator/).

```
template.json   the fabricated template: header, five workstreams, three triggers,
                three checkpoints with deliverables, risk and backlog lists — and a
                usage line saying the initialise command builds from it
builders.py     the two builders in the source's design, each its own dictionary
                literal: one as the repository detector writes it, one as the
                status script's initialise command does
drift.py        loads all three and lists where they disagree
```

## Try it

```bash
python3 drift.py                 # the three copies, compared; exits 1
python3 builders.py --init       # what the initialise command creates; exits 0
```

**The diff.** Workstream B needs two triggers in the template and one in both builders, so a
sprint created by either script lets B start once the transit schema is agreed, whether or not
TLS is stable. Workstream C's owned roles are empty in the template and, from the detector,
every role it found — including `vendor-ingress`, which nobody on the team owns. Trigger
history, notes, violation counts, risks and backlog exist only in the template. Both builders
leave every checkpoint without deliverables and write "tomorrow" as the second and third
deadlines.

**The usage line.** The template says the initialise command builds from it. `drift.py`
checks whether `builders.py` ever names the template file: it does not. Editing the
template changes no sprint. Exit 1 marks that finding, not an error.

**The initialise command.** `python3 builders.py --init` prints the sprint it would create,
dated today. Without `--init` it exits 2.

## What is deliberately missing

**YAML.** The source template is YAML with its vocabularies in comments. The standard library
cannot parse YAML, so this one is JSON with the vocabularies under `_states`. The source's own
readers made the same substitution without the YAML library, and failed on the YAML template.

**Writing the file.** Nothing here is saved; the builders return dictionaries and `--init`
prints one.

**The fix.** Load the template and fill it, validate states against `_states` on every write,
and compute absolute checkpoint dates at the scope lock. Each is short; adding them here would
hide what the card describes.
