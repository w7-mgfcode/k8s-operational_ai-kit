---
component: 18
title: Installation Glossary
type: reference
instances:
  - 02-progressive-disclosure
  - 05-instruction-provenance-and-drift
related:
  - 08-workstream-hardening-orchestrator
---

# Installation Glossary

> A terminology file that tells the model to use its terms exactly — and whose terms are
> mostly facts about one installation, frozen on the day it was written.

## What it is

A reference file the hardening orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)) carries so its output uses the
team's vocabulary. A few dozen terms in tables by area — cluster, configuration-management
mechanics, networking, storage, identity and secrets, observability, the sprint itself, the
application domain — and a list of risk identifiers with one-line descriptions. Its header
says to use these exact terms in all skill output. In practice most rows are not definitions
but measurements: node counts, addresses, a virtual IP, version pins, an address pool, a
deadline for a component's end of life, a cron time, the number of applications that read
secrets.

## Trigger and routing

Listed in the skill's reference table as the canonical terms with project-specific meanings.
No phase links to it. It is read when the model wants a term, which for a file that also holds
the installation's addresses and counts means it is the most likely place for the model to
pick those up.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The installation's documentation | at authoring time | the intake package the skill was generated from |
| Anything at run time | no | the file is static; nothing refreshes it |

## Procedure

There is none at run time; the file is read, not executed. Its implied procedure is two
lines in its header: look a term up here, and use it exactly as written.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Being read into context | yes, whole | the harness — a reference loads in full when opened |
| Being checked against the cluster or the repository | — | nothing; no script reads it |

## Outputs

None of its own. Its terms, and its facts, appear in whatever the skill writes: checkpoint
reports, workstream briefs, generated commands.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Facts drift silently | A report states a version, node count or consumer count that was true when the glossary was written | Measurements are filed as definitions, and nothing compares them with the repository's version-pin file or the cluster. Structural — [card 05](../../../../cards/05-instruction-provenance-and-drift.md)'s failure in one file |
| "Exactly" spreads the drift | The stale value is repeated verbatim in every artifact the skill produces | The header instructs exact reuse; a wrong fact is copied with the same authority as a right term. Structural |
| Two glossaries | A term means one thing here and something slightly different in the intake package that sits beside the skill | The package the skill was generated from carries its own terminology dictionary. Both ship with the skill; nothing compares them. Observed |
| One count, four places | The number of applications that read secrets appears here, in the tier table, in the secrets-store guide and in the trigger definitions | Each file restates it; none points at a single source. Observed |
| Identifiers concentrate here | The file holds more installation detail — addresses, hostnames, team prefixes, a password-helper alias — than any other part of the skill | A glossary invites "what is X" answers, and the answers were copied from the installation's documentation. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [02 Progressive Disclosure](../../../../cards/02-progressive-disclosure.md) | Terms kept out of the entry file and loaded only on demand — the right placement for a vocabulary, and a cheap one |
| [05 Instruction Provenance and Drift](../../../../cards/05-instruction-provenance-and-drift.md) | Instructions that describe a system as it was, imported wholesale, with nothing that detects when it changed |

## Provenance

Instanced in the source system by one reference file of about ninety lines in the skill's
references directory: term tables in eight areas and a risk-identifier list. Its rows were
condensed from a longer terminology dictionary in the intake package the skill was generated
from, which still sits beside it. This card reproduces none of the rows. The file records no
date of its own, so nothing in it says when its facts were true.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/18-installation-glossary/`](../../../../skeletons/components/18-installation-glossary/).
Standard library, offline. It pulls the checkable facts out of a fabricated glossary, compares
them with a fabricated current state, and lists the terms a second dictionary defines
differently.

## What is deliberately missing

**Definitions separated from measurements.** A glossary entry should say what a term means;
how many, which version and at what address belong in files that are generated from the
source of truth, or checked against it.

**A staleness check.** Even without separation, extracting version-shaped and count-shaped
values and diffing them with the repository's pins takes one short script; the prototype is
that script.

**One dictionary.** The intake package's dictionary should have been the source this file is
generated from, or deleted once it was.

**In the prototype:** the "current state" is a fixture, not the repository or a cluster, and
only versions, counts, ports and dates are recognised as facts.
