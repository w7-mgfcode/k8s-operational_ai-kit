---
card: 05
title: Instruction Provenance and Drift
layer: instruction
maturity: abandoned
source: ../cards/05-instruction-provenance-and-drift.md
---

# Instruction Provenance and Drift

> Instructions copied from another repository describe a system you do not have — and because agents execute instructions rather than consult them, nothing about the failure looks like a failure.

**Status:** abandoned — this card documents a pattern the source system **failed to
hold**. The failure is more instructive than the success would have been, and it is
the commonest defect in instruction layers that were assembled rather than written.

## 1. Why

Ordinary documentation drift is annoying: a stale README wastes a reader's time and
is caught the moment someone follows it. Instruction drift differs *in kind*, because
of who the reader is.

An agent does not evaluate whether its instructions describe reality. It applies
them. A rule demanding test files under a directory that does not exist raises no
error — it produces work in the wrong shape, with justification, indefinitely.

The artifacts that cause this are usually the **best-written files present**, because
someone authored them for a system where they were true.

**Without it:** the instruction layer becomes archaeology — strata of imported
guidance, each plausible, none verified, all executed.

## 2. Core Idea

Every instruction artifact needs traceable provenance and a reconciliation step: an
answer to *"where did this come from, and what in it is true here?"*

Reconcile **mechanically, not by reading** — plausibility is exactly what got the
artifact accepted in the first place.

## 3. Architecture

```
  ORIGIN                    RECONCILIATION              RESULT
  ──────                    ──────────────              ──────
  written here        ──▶   n/a                   ──▶   true
  imported, checked   ──▶   globs resolved,       ──▶   true
                            claims re-verified
  imported, unchecked ──▶   none                  ──▶   SILENT FALSEHOOD
  generated, not re-run ─▶  none                  ──▶   decays to the above
                                                            │
                                     copied onward ◀────────┘
                                  (chain lengthens, evidence disappears)
```

## 4. How It Works

The failure, step by step — this is what to watch for:

1. An artifact is copied in because it is good and adjacent.
2. It is not reconciled — reconciling is tedious and the artifact reads as authoritative.
3. **It becomes load-bearing by position.** Being in the rules directory *is* the claim of applicability.
4. It decays asymmetrically: the artifact does not change, the repository does.
5. It is inherited again, wholesale, by the next repository.

The corrective: record provenance at import, resolve every path and glob
mechanically, and re-run that check **in the same change** that restructures the repo.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Provenance note per artifact | Distinguishes "written here" from "arrived here" | Every file looks equally endorsed |
| Mechanical path resolution | Plausibility cannot be judged by reading | Drift found by accident, if ever |
| Trigger tied to restructuring | The gap widens on change, not on time | Checked once at import, never again |
| Willingness to delete | The right action for foreign material is usually removal | Kept "just in case", still authoritative |

## 6. Decisions That Matter

- **Copying is genuinely good.** This is not an argument against reuse — reuse is how a kit becomes capable quickly. The mistake is skipping reconciliation, not the copying.
- **Reconciliation never happens unless it is mechanical and attached to something that happens anyway.** It produces no new capability and its success is invisible.
- **There is no gradual fix.** The realistic intervention is periodic and destructive: resolve everything, delete what does not resolve, rewrite the rest.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Import a proven artifact | Immediate capability | Position is mistaken for endorsement |
| Record provenance | Makes origin auditable | The note ages too — "reconciled at import" is a dated claim worth less each month |
| Delete unreconciled material | Restores truth | Feels lossy; the value was real, it just did not travel |

**Most common failure:** the foreign rule set — rules governing module names, test
layouts and vision documents that do not exist here.

## 8. What To Remember

1. Agents execute instructions; they do not evaluate them.
2. Being in the rules directory is not evidence that a rule applies.
3. The best-written file in the layer is the most likely import.
4. Check: resolve every cited path and glob, and report a truth **percentage** per file.

## 9. Lecture Cue

- **Start with:** a rule that is beautifully written, internally coherent, and about a different repository.
- **Draw:** the origin-to-result table, then the loop arrow where a successor inherits the whole directory.
- **Discuss:** why reconciliation never happens voluntarily — it creates nothing and its success is invisible.
- **Name the abandonment, with numbers:** the source kit held five rule files governing a Python CLI tool it was not, three review reports on an unrelated service, and nineteen vendored subagent definitions nothing ever invoked. It was *not* careless — it contained an excellent internal document explaining path-scoped rules (card 04) and built validators for its own skills (cards 09, 10). **It understood the principle and never turned it on the instruction layer, because nothing made that layer's correctness measurable.** A later audit of the successor found 8 inherited rule files, 36 dead globs, roughly three quarters of cited paths unresolvable — and the set was rebuilt rather than repaired.
- **End with:** the failure was three months old and entirely invisible until something resolved the paths.

**Sits between:** card 01 (its absence left the vacancy) · card 04 (supplies the check) → **this** → card 15 (same validation class, applied to knowledge)

---
Source: `../cards/05-instruction-provenance-and-drift.md` · Skeleton: `../skeletons/05-instruction-provenance-and-drift/`
