---
paths:
  - "ai-engineering-knowledge-cards/cards/**"
  - "ai-engineering-knowledge-cards/templates/**"
  - "ai-engineering-knowledge-cards/docs/**"
---

# The Card Contract

A card is one pattern, thirteen fixed sections, every claim traceable to
something that actually ran. `../templates/CARD_TEMPLATE.md` is the contract; all
twenty cards conform exactly, and `check.py` keeps that true.

## Frontmatter

Six keys, always, in this order:

| Key | Value |
| --- | --- |
| `card` | Two digits, matching the filename prefix. |
| `title` | A noun phrase, not a verb phrase. "Description-as-Router", not "Routing by description". |
| `layer` | One of: `instruction` `routing` `skill` `subagent` `memory` `execution` `validation`. |
| `maturity` | One of: `proven` `partial` `abandoned`. |
| `instanced_by` | `<component type>/<generic component name>` — generic, never a real path. |
| `related` | Other card slugs. A card with no `related` is an orphan; say why or add the edge. |

## Structure

Thirteen `##` headings, in the template's order. The filename is `NN-<slug>.md`
and the slug matches `title`. Verify before committing:

```bash
grep -c '^## ' cards/NN-*.md          # must be 13
```

## `maturity: partial` is not a defect

It means the source system implemented part of the pattern and not the rest, and
the card says exactly which part. **The gaps are the most instructive content in
the repository.** Do not smooth one over, do not upgrade a `partial` to `proven`
to make a card read better, and do not write a Failure modes table that contains
only hypotheticals — every row is observed or structurally inevitable.

Card 13 is the reference: `maturity: partial`, with the missing redaction stage
named in the card, in the skeleton README, and in the skeleton's own output.

## Provenance

The Provenance section describes the real components generically and states
exactly what was missing. Where a pattern was inherited from published work
rather than invented, say so. Nothing here is claimed as a product or a
general-purpose framework.

Every sentence is subject to [`anonymization.md`](anonymization.md).
Each card's skeleton is subject to [`skeletons.md`](skeletons.md).
