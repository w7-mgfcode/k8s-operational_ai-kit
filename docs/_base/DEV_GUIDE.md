# Developer Guide

> How to add a card, add a skeleton, and get the gate to pass.
> Stub generated 2026-09-21 — extend freely; this file is never overwritten by tooling.

## Prerequisites

`python3` on PATH. Nothing else. There is no install step.

```bash
python3 check.py     # confirms your clone is sound
```

## Adding a Card

1. **Pick the number and slug.** Next free `NN`, slug matching the title.
   `cards/NN-<slug>.md`.
2. **Copy the template.** `templates/CARD_TEMPLATE.md` is the shape — thirteen `##` sections in
   its order, six frontmatter keys in its order.
3. **Fill `instanced_by` generically.** `<component type>/<generic component name>`. Never a
   real path from the source system.
4. **Set `maturity` honestly.** `partial` if the source system implemented part of the pattern,
   and then say precisely which part in Provenance. Do not round up.
5. **Write Failure modes from observation.** Every row is something that happened or is
   structurally inevitable. A table of hypotheticals fails the card's purpose, not just its
   contract.
6. **Add `related:` edges both ways.** If card 07 relates to yours, add yours to card 07.
7. **Create the skeleton** (below). `check.py` fails a card without one.
8. **Update `INDEX.md`** — the by-card table, the by-question table if it fits, and the maturity
   counts. Nothing checks this for you.
9. `python3 check.py --run`.

## Adding a Skeleton

Directory name must equal the card's filename stem: `skeletons/NN-<slug>/`.

Four constraints, from `.claude/rules/skeletons.md`:

- **Standard library only.** No install, no requirements file.
- **Offline.** Model calls stubbed behind a named function that prints instead — see
  `compile_one()` in `skeletons/13-log-as-source-compilation/compile.py`.
- **Runnable as committed.** Example data ships with it; the README's commands work on a fresh
  clone.
- **Generic.** No real paths, hostnames or domains.

The README needs three things: what each file is, a `## Try it` block of commands that actually
run, and a *What is deliberately missing* section. The third is not optional — a gap faithful
to the source system is card content, and hiding it turns the skeleton into a demo.

**Make failure visible where it teaches.** Several skeletons ship deliberately broken input so
the reader sees the check fail: card 15's corpus has four planted defects, card 05's rule set
resolves 10% of its cited paths, card 18 leaves one credential shape un-redacted on purpose.
Exiting 1 is fine. Crashing is not.

**Clean up.** If your skeleton writes state, make it idempotent or remove it. Add generated
artifacts to `skeletons/.gitignore` and to `RUN_ARTIFACTS` in `check.py`.

## Running the Gate

```bash
python3 check.py           # ~1s   contracts, links, imports, anonymization
python3 check.py --run     # ~20s  the above, plus executing every skeleton
python3 check.py --quiet   # failures only
```

Reading the output: **0** means the script ran, **1** means it ran and demonstrated a failure on
purpose, **2** means it needs arguments and was not exercised. Only a crash is reported as a
failure.

## Common Failures

| Message | Cause |
| --- | --- |
| `N '##' headings, contract requires 13` | A section was dropped or an extra one added |
| `frontmatter keys [...] != [...]` | Keys out of order, or one missing |
| `no matching skeleton directory` | Directory name does not equal the card's filename stem |
| `README has no '## Try it' section` | Heading text must match exactly |
| `non-stdlib import` | A dependency crept into a skeleton |
| `broken link -> ../../cards/...` | Under `skeletons/pipelines/` you are one level deeper — use `../../../cards/` |
| An anonymization hit in a new file | Either genuinely wrong, or teaching material that needs an `ANON_EXEMPT` entry — prefer fixing the file |

## Committing

Conventional Commits with the scope taxonomy in `.claude/rules/git-workflow.md`
(`cards` `skeletons` `docs` `agents` `ci`). Scope is chosen by blast radius, not file count: a
one-line edit to `CARD_TEMPLATE.md` is `cards`, because it changes the contract every card obeys.

A `Context:` trailer is required when the commit touches `.claude/` or `AGENTS.md` — it records
what an agent reading the repo later will now see differently, in the agent's terms rather than
the diff's.

Branch first. The default branch is not a place to commit directly.
