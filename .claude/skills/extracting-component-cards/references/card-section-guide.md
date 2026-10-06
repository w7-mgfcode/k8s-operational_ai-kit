# Card Section Guide

How to fill a component card from a skill artifact. The template
(`ai-engineering-knowledge-cards/templates/COMPONENT_CARD_TEMPLATE.md`) says what each
section holds; this file says where in the source to find it, and what components
01–07 taught about doing it honestly.

## Contents

- [Where each section comes from](#where-each-section-comes-from)
- [Failure modes](#failure-modes)
- [Provenance](#provenance)
- [Prototype and skeleton](#prototype-and-skeleton)
- [Graph edges and the INDEX line](#graph-edges-and-the-index-line)
- [Local mode](#local-mode)

## Where each section comes from

| Section | Skill card (SKILL.md) | Reference / asset / script |
|---|---|---|
| What it is | The body's opening and its phase list | What the file is for, and which skill phase uses it |
| Trigger and routing | The `description` field: triggers, exclusions, named siblings | The SKILL.md line that loads or runs it, and in which phase |
| Inputs | What each phase needs before it starts | For a script: its arguments and stdin; for an asset: the slots it expects |
| Procedure | The phases and their gates, in order | The steps the file prescribes, or the script's control flow |
| Tools and permissions | `allowed-tools`, tool tables, deny lists — and whether the harness or only the text enforces each | What the script touches (files, network, subprocesses), read from its code |
| Outputs | What the skill writes, where, and whether it asks first | Stdout, stderr, exit codes, files written |
| Patterns it instances | Match against the pattern cards in `cards/`; at least one | Same |

Read the whole artifact before writing any section. A card written section by section
while reading repeats the source's order instead of explaining it.

## Failure modes

Every row is **observed** — readable directly off the artifact — or **structural** —
inevitable given its design. Never a hypothetical. Label each root cause with which.

Kinds that recurred in components 01–07, as prompts, not as copy:

- **Advice that looks like a control.** A deny list in prose, a "never" the harness does
  not enforce. Say which rows are enforced and which are trusted to the model.
- **Order dependence.** A rule or pattern list applied in sequence, where an early entry
  shadows a later one or rewrites the text the next one reads.
- **Format blindness.** A check written for one shape (YAML, `key: value`) that the same
  data in another shape (JSON, a URL) walks past.
- **Stale lookup tables.** A keyword or path map that silently returns nothing after a
  rename.
- **One fact, two places.** Frontmatter and body, or two templates, that can disagree and
  nothing compares.
- **Unchecked slots.** A template whose placeholders can be saved unfilled.

If you cannot find a real failure, the card has fewer rows. Do not invent one to fill
the table.

## Provenance

Describe the source generically: its size in lines, its parts, where it sat ("in the
skill's references directory"), and what its design inherited. Then state what the
source does **not** record — how often it ran, what it produced — and claim none of it.
No name, path or example from the masking table appears here; this is the section most
tempted to.

## Prototype and skeleton

- A **fresh implementation**. Never copy the source's code or patterns, even renamed.
- Fixtures are **fabricated**, and shaped to make the card's failure modes visible.
  A worked example from the source is never reused — it may be a real incident.
- Standard library, offline, runnable as committed. Exit **1** is how a skeleton shows a
  failure on purpose; say so in its README.
- Keep fixtures clear of the shapes `check.py` flags in every published file: home-directory
  paths, IPv4 addresses, `.local`/`.internal`/`.corp`/`.lan` domains, a bearer token of 20+
  characters, an `api_key=` value of 12+. Prefer a shorter fake over an `ANON_EXEMPT` entry.
- The README's `## Try it` commands must actually run, and its *What is deliberately
  missing* names both the gap to the real component and the gap to the pattern.
- Links from the skeleton README to cards go through `../../../`.

## Graph edges and the INDEX line

- `instances:` — the pattern cards the artifact puts into practice. A component that
  instances none does not belong in `component-cards/`.
- `related:` — the skill card relates to every part; each part relates to its skill and to
  the siblings it actually works with. Every edge runs both ways (`check.py` enforces it).
- The INDEX row's last column is one line: what it does, then the catch.
  *"A keyword-to-path map narrows the search — until a role is renamed and it quietly finds
  nothing."*

## Local mode

The skill is one this repository authors — tracked in git under `.claude/skills/`.
Vendored skills are refused by `inventory.py`: they are other projects' work, gitignored
because nobody here vetted them. The flow is the same, including the masking table, since
an authored skill can still quote a path or a name. Provenance says it is a skill in this
repository's agent layer; its own name is public already, so it may stay if the owner
agrees at the gate.
