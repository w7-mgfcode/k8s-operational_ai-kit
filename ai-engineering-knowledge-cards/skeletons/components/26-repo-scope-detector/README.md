# Skeleton — Repository Scope Detector

The scope-lock step that reads a repository's layout and pre-fills the sprint's
starting state, plus a list of everything the pre-fill decided without asking.
The card is
[component 26](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/26-repo-scope-detector.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
fixture-repo/          a fabricated infrastructure repository: four roles, one of
                       them a vendored wrapper; numbered phase playbooks; an
                       inventory with version pins and an encrypted-variables
                       file; a TLS task stub holding only comments; a benchmark
                       report under reports/; OWNERS, the roles the team maintains
state-template.json    the sprint state as the skill's own template shapes it —
                       the second of the three copies the card describes
detect.py              detection and pre-fill, the state to stdout; with --audit,
                       the decisions it made silently
```

`detect.py` writes nothing. The component writes the state to a file, and the
card covers the overwrite that follows from that.

## Try it

```bash
python3 detect.py                  # the pre-filled state as JSON; exits 0
python3 detect.py --audit          # what the pre-fill decided; exits 1
```

**The state.** Five workstreams, three triggers, three checkpoints. Workstream
A has no blockers, B is blocked for a missing stub, D for a missing report, and
every role is in C's owned list. It reads as a finished scope lock.

**The audit.** Seven decisions, none of them put to the user:

- The vendored ingress wrapper is in scope because every role is.
- Workstream A is unblocked because its stub exists, and the stub holds only a
  TODO.
- Checkpoints B and C are due "tomorrow", a string that stays true forever.
- Workstream B waits on one trigger here and on two in the template.
- The checkpoints have no deliverables, although the template lists them.
- D is blocked although a report sits under `reports/`, one directory away from
  the only place the detector looks.

Exit 1 marks those decisions, not an error.

## What is deliberately missing

**Writing the state.** The component writes a YAML file (or JSON, without a
YAML library) to a path it is given, with no check for an existing sprint. Here
the state goes to stdout so the gate never dirties the tree.

**The Makefile and CI checks.** The component also records whether a Makefile
and one CI configuration file exist. They feed no blocker and are left out.

**The fixes.** An ownership list asked for at scope lock, stubs judged by
content, checkpoint targets computed as dates, one shared plan structure, and
locations from configuration instead of code. Each is small. Adding them would
hide what the card describes.

**The pattern's gap.** Card [19](../../../cards/19-scope-lock-and-checkpoint-delivery.md)
freezes a scope the user agreed to. A pre-fill this complete leaves the user
little to agree to except what it already decided.
