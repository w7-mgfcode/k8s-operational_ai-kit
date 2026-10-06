---
paths:
  - "ai-engineering-knowledge-cards/component-cards/**"
  - "ai-engineering-knowledge-cards/templates/COMPONENT_CARD_TEMPLATE.md"
  - "ai-engineering-knowledge-cards/skeletons/components/**"
---

# The Component Card Contract

A pattern card (`cards/`, see [`cards.md`](cards.md)) describes an idea. A
component card describes **one concrete artifact** — a skill, command, rule,
subagent, hook, or a reference, asset or script a skill loads — and shows which
patterns it puts into practice. The two are separate contracts; do not force one shape onto
the other.

[`COMPONENT_CARD_TEMPLATE.md`](../../ai-engineering-knowledge-cards/templates/COMPONENT_CARD_TEMPLATE.md) is the shape. `check.py` enforces it.

## Layout

The tree mirrors the anatomy of what it describes. A skill is a directory, so its
card opens one, and what the skill loads sits beneath it — ownership is the path,
not a cross-reference ([card 02](../../ai-engineering-knowledge-cards/cards/02-progressive-disclosure.md)).
Every other type is a single file under its plural name.

```text
component-cards/
├── skills/<skill>/
│   ├── NN-<skill>.md                  type: skill — the directory is the card's slug
│   ├── references/NN-<slug>.md        type: reference — read on demand
│   ├── assets/NN-<slug>.md            type: asset — filled in or copied, not read
│   └── scripts/NN-<slug>.md           type: script — executed, not read
├── commands/NN-<slug>.md              type: command
├── rules/NN-<slug>.md                 type: rule
├── subagents/NN-<slug>.md             type: subagent
└── hooks/NN-<slug>.md                 type: hook
skeletons/components/NN-<slug>/        one prototype per component card, flat
```

Create a directory only when a card lands in it. `NN` is unique across the whole
tree, not per skill or per type. The skeleton directory name equals the card's
filename stem, wherever the card sits.

## Frontmatter

Five keys, always, in this order:

| Key | Value |
| --- | --- |
| `component` | Two digits, matching the filename prefix. |
| `title` | A generic name. **Never the source component's own name** — named personal tooling is a masked class. |
| `type` | One of `skill` `reference` `asset` `script` `command` `rule` `subagent` `hook`, and consistent with where the card sits in the layout above. A `reference` is a document a skill reads on demand — a rubric, a catalogue; an `asset` is a file it fills in or copies — a template; a `script` is code it runs. All three name their skill in `related:`. |
| `instances` | Pattern-card slugs from `cards/`. At least one — a component that instances no pattern does not belong here. |
| `related` | Other component-card slugs, or `[]`. Every edge runs both ways, and a reference, asset or script lists the skill it sits under. |

Pattern cards' `related:` lists pattern-card slugs only. The edge from a pattern
to a component is not written back; `instances:` is the one direction.

## Structure

Eleven `##` headings, in the template's order. Failure modes are observed or
structurally inevitable — the same rule as pattern cards. A failure you can read
directly off the source artifact (a verb its own deny list forgot) counts as
observed.

## Anonymization

Stricter than for pattern cards, because a component card is closer to the source.
Everything in [`anonymization.md`](anonymization.md) applies, and additionally:

- The source component's name, and the names of its sibling components, are
  replaced with generic descriptions.
- Worked examples from the source are not reused, even with names changed — they may
  be real incidents. Fabricate a new one.
- Environment ladders, repository layouts and role names are generalized, not
  renamed one-for-one.
- A `skills/<skill>/` directory takes the skill card's generic slug, never the
  source skill's directory name. The `references/` `assets/` `scripts/` split is
  the public skill anatomy, not the source's, and stays.

Extraction from `.legacy-assets/` for a component card requires the user to
authorize one named directory, and a masking table reviewed by the user **before**
any file is written. It is never a default.

## Prototype

Everything in [`skeletons.md`](skeletons.md) applies: stdlib only, offline,
runnable as committed, README with `## Try it` and `## What is deliberately
missing`. Cluster, web and model calls are replaced with fixture data or a named
stub function that prints. Links from a component skeleton README reach the cards
through `../../../`.

Related: [`cards.md`](cards.md), [`skeletons.md`](skeletons.md),
[`git-workflow.md`](git-workflow.md).
