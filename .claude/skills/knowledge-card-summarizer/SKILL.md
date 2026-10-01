---
name: knowledge-card-summarizer
description: Compress a detailed knowledge card into a short, visually structured teaching card that serves as both a student reference and a lecturer's speaking aid. Use when asked to summarize, condense, brief, simplify, restructure, or "explain" a knowledge card, or to turn one into a seminar handout, lecture aid, teaching card, slide outline, or concept briefing. Reads from ai-engineering-knowledge-cards/cards/ and writes ai-engineering-knowledge-cards/teaching/. Do not use to author a new card, to edit a source card, or to summarize prose that is not a knowledge card.
---

# Knowledge Card Summarizer

Turn one card into a teaching artifact. Not a shorter document — a different one,
reordered for understanding rather than for implementation.

> Understand deeply. Compress aggressively. Preserve the concept.

## Before writing anything

Read the whole source card. Do not summarize while reading; the card's own section
order is written for an implementer, and the teaching order is different.

Then answer these internally. If any is unclear, the card has not been understood:
what it is · why it exists · how it works · its parts · how they relate · which
decisions mattered · what it costs · what a learner must retain.

## The source contract

Every card in `cards/` carries six frontmatter keys (`card`, `title`, `layer`,
`maturity`, `instanced_by`, `related`) and exactly thirteen `##` sections in a fixed
order. That structure is guaranteed — use it as the extraction map rather than
re-deriving the card's shape each time.

| Source section | Feeds |
|---|---|
| `maturity` + **Provenance** | the Status line — see the rule below |
| **Why it exists**, and its `**Without it:**` line | §1 Why — that line is the sharpest problem statement in the card; quote or tighten it, never dilute it |
| **What this pattern is** | §2 Core Idea |
| **Where it belongs** + **Diagram** | §3 Architecture — merge both into one diagram |
| **How it works** | §4 How It Works |
| **What it depends on** | §5 Key Components |
| **How it evolves** | §6 Decisions — especially the point where the pattern stops paying for itself |
| **Constraints and trade-offs** + **Failure modes** | §7 Trade-offs |
| **How to validate an implementation** | §8 Remember — carry one mechanical check |
| **How it interacts with other patterns** + `related:` | §9 Lecture Cue — where this sits in the series |
| **Skeleton** | the footer pointer |

## Three rules specific to this repository

**1. Never compress away a stated gap.** `maturity: partial` means the source system
implemented part of the pattern and not the rest, and the card says which part. Those
gaps are the most instructive content in the repository. A teaching card that drops
them becomes a sales pitch. Carry the gap into the Status line verbatim enough to
still be true, and give the lecturer a cue to discuss it.

**2. Anonymization is already done — do not redo it.** The source cards were written
against `ai-engineering-knowledge-cards/docs/ANONYMIZATION.md` and are already clean.
Re-anonymizing invents distance that damages the concept. The binding policy is
`.claude/rules/anonymization.md`; do not restate it here and never read
`.legacy-assets/` for context. If a card still names something identifying, that is a
defect in the card — report it, do not silently launder it.

**3. Preserve the card's position in the graph.** `related:` edges and the interacts
table are what let a lecturer say "this follows from card 02." A teaching card with no
neighbours teaches an isolated trick instead of an architecture.

## Compression target

Sources run roughly 200–250 lines. A teaching card lands at **80–120** — about
**2–2.5x** compression. The nine-section structure, three tables and a diagram put a
floor near 90 lines; pushing below it starts deleting mechanism rather than noise.

*Measured against card 13 (254 → 103, 2.5x). One data point — if several cards land
consistently outside this band, correct the band rather than forcing the cards.*

Every section earns its place. For each, ask: does removing this reduce
understanding? If no, remove it.

## Output

Write `ai-engineering-knowledge-cards/teaching/NN-<slug>.md`, matching the source
filename exactly. Use `assets/TEACHING_CARD_TEMPLATE.md` as the skeleton.

One artifact serves both readers — do not produce two documents:

- **Student** answers: what is this · how does it work · what are the parts · what do I remember
- **Lecturer** answers: where do I start · what do I draw · which trade-off do I discuss · what is the takeaway

The card supports the lecture. It does not replace it — leave room to expand verbally.

## Language

Precise and declarative. "A separates B from C," not "this is basically a mechanism
that helps provide separation between." Terminology consistent with the source card;
if the source names a concept, do not rename it.

## Do not

- Invent a conclusion the source does not support.
- Add metadata, scoring, taxonomies or schemas — the output is a teaching card, not a record.
- Draw a diagram that decorates rather than explains.
- Edit the source card. This skill reads `cards/` and writes `teaching/`, never the reverse.

## References

Load as needed:

- `references/extraction.md` — the CORE / SUPPORTING / DETAIL / NOISE taxonomy and the keep-or-cut priority
- `references/visual-language.md` — diagram conventions, when a diagram earns its place, worked examples
- `references/quality-gate.md` — the checklist to run before writing the file
