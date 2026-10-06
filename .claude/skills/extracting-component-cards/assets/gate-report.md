# Extraction plan — <generic skill title> (<legacy | local> mode)

> Chat only. This report carries originals; it is never written to a file in the
> repository, a commit message, or a PR.

## Bundle plan

| # | Source file | Type | Generic title | Card path | Skeleton |
|---|---|---|---|---|---|
| NN | `SKILL.md` | skill | … | `component-cards/skills/<slug>/NN-<slug>.md` | `skeletons/components/NN-<slug>/` |
| NN | `references/…` | reference | … | `…/references/NN-<slug>.md` | `…/NN-<slug>/` |

`related:` edges: …  ·  Instanced patterns per card: …

## Not becoming cards

| Source file | Why |
|---|---|
| … | … |

## Masking table

Each compound identifier is split: a path that holds a username, an organization and a
repository name is three rows, so the residue check searches for each part.

| # | Original | Class | Generic replacement | Found at |
|---|---|---|---|---|
| 1 | … | … | … | `file:line` |

Scanner candidates judged *not* identifying (kept as written): …

## Wiring this run will do

INDEX rows · reverse `related:` edges in … · the component-card count (N → M) in three
places · pending rows in `diagrams/README.md` for: …

---

**Approve this plan and masking table?** Nothing is written until you do. Any change
comes back here as a new version of this report.
