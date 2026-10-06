# Extraction: what to keep, what to cut

## Four categories

**CORE** — required to understand the concept. Always preserve.
The mechanism, the failure it prevents, the relationships between parts.

**SUPPORTING** — improves understanding. Keep only where it materially helps.
One worked example, one named failure mode, one scaling limit.

**IMPLEMENTATION DETAIL** — configuration, commands, paths, identifiers, line
counts, exact file names. Cut unless the concept is unintelligible without it.
A teaching card says "a content hash drives the rebuild," not
`hashlib.sha256(path.read_bytes()).hexdigest()[:12]`.

**NOISE** — repetition, hedging, incidental history, prose that restates a heading.
Always cut.

## Priority when space runs out

```
CONCEPT  >  RELATIONSHIPS  >  REASONING  >  EXAMPLES  >  IMPLEMENTATION DETAIL
```

Cut from the right. A card that keeps its examples and loses its relationships has
been shortened, not taught.

## The test

For every retained sentence: **does removing this reduce understanding?**
If no, remove it. Apply to your own output, not just the source.

## What survives compression in practice

These are the parts of a source card that carry the most teaching value per line,
and should be the last things cut:

| Keep | Because |
|---|---|
| The `Without it:` line | It is the problem stated as an observable symptom — the single best opening for a lecture |
| The stated gap on a `partial` card | The gaps are the most instructive content; see SKILL.md rule 1 |
| The scaling limit from **How it evolves** | "At fifty components this stops paying for itself" is the sentence students remember |
| One row of **Failure modes** | Concrete failure beats abstract caution |
| The `related:` edges | They turn a trick into an architecture |

## What to cut first

- Provenance prose beyond the maturity clause
- The validation checklist, except one mechanical check worth quoting
- Dependency table rows that restate the architecture diagram
- Any sentence whose content is already in the diagram
