# Skeleton — Generator Role Reference

An implementer's hand-off notes checked against the rules a role reference gives them,
and the file scope compared three ways — over fabricated fixtures. The card is
[component 39](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/39-generator-role-reference.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
sprint-spec.md            a fabricated one-sprint spec with a three-file scope
implementation-notes.md   the implementer's notes: changes, assumptions, known gaps and
                          files modified
changed-files.txt         what the working tree shows as changed — one file more than the
                          notes report
wordings.json             four statements of what the implementer may do with the contract
audit_notes.py            the notes lint, the scope comparison, and the wording table
```

## Try it

```bash
python3 audit_notes.py            # one banned phrase, one file outside scope; exits 1
python3 audit_notes.py --wording  # four statements, three different answers; exits 1
```

**The notes.** All four required sections are present. One line in *Known Gaps* says the
reader could be improved by streaming — a disclaimer, which the same document bans — and
the line above it is an unfinished item the spec asked for, which the section exists to
hold. The lint separates them by wording alone.

**The scope.** The spec lists three files and the notes report the same three, so the
notes look clean. The working tree shows a fourth changed file. Nothing in the loop
compares the notes, the spec and the tree; the implementer wrote the only record.

**The wording.** The role reference lets the implementer steer by the contract; the
build-phase text and the spawn prompt forbid referencing it; the template says nothing on
steering. Exit 1 marks the disagreement, not an error.

## What is deliberately missing

**A diff.** `changed-files.txt` stands in for the working tree. A real comparison would
read version control, which the component's loop never does for this purpose.

**The retry path.** The delta report an implementer receives on a later iteration, and the
scores and thresholds the return template puts in it, are not modelled
([component 33](../33-blocking-items-return-template/)).

**The fix, for the pattern.** A scope check that reads the tree and the spec rather than
the implementer's own list, one wording of the contract rule, and a *Known Gaps* section
defined as unfinished spec items only.
[Card 11](../../../cards/11-adversarial-role-separation.md) is the pattern this belongs to.
