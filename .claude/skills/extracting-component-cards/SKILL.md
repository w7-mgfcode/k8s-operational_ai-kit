---
name: extracting-component-cards
description: Turn one agent skill into a complete component-card bundle in ai-engineering-knowledge-cards/component-cards/ — a card and a runnable skeleton per artifact (the skill, each reference, asset and script), wired into INDEX.md, sibling cards and the restated counts — behind an owner-approved plan and masking table, then verify, commit, and on a final confirmation push and open a PR. Works on a skill under .legacy-assets/ or .claude/skills/. Use when asked to extract a skill into component cards, write component cards for a skill, document a skill as a component-card bundle, add a skill to component-cards with its references and scripts, or turn a .claude/skills skill into component cards. Not for a teaching card (knowledge-card-summarizer), a pattern card in cards/ (by hand, DEV_GUIDE), creating or upgrading the skill itself (skill-creator, evolving-legacy-skills), a diagram (excalidraw-diagram), or a wording fix to an existing component card (edit directly).
---

# Extracting Component Cards

One named skill in, one wired component-card bundle out. This is the repository's only
route from source material into published files, so it runs behind two owner gates: the
plan and masking table before anything is written, and publication before anything is
pushed.

The rules this skill executes live elsewhere — read them, do not restate them:
`.claude/rules/anonymization.md` (extraction conditions), `.claude/rules/component-cards.md`
(layout, frontmatter, eleven sections), `.claude/rules/skeletons.md`, and
`.claude/rules/git-workflow.md`.

## Modes

| Mode | The owner names | Masking table | Notes |
|---|---|---|---|
| **legacy** | a skill directory under `.legacy-assets/` | required | Read freely; never write, move or delete anything there |
| **local** | a project-authored skill under `.claude/skills/` | required | Only skills git tracks; a vendored (gitignored) skill is refused |

`scripts/inventory.py` detects the mode from the path. Anything else is refused.

## Workflow

Run the scripts with `python3` from the repository root.

### 1. Intake

1. Confirm the owner named one skill directory. Do not search for one.
2. Check `INDEX.md`'s component table: if this skill already has a bundle, stop and ask
   whether to extend it rather than duplicate it.
3. `python3 <this-skill>/scripts/inventory.py <skill-dir>` → mode, next free component
   number, every file with its card type and number.

**Gate:** every file is either mapped to a card or listed under "Not becoming cards" with a
reason (`unmapped` in the inventory means a decision is owed).

### 2. Analyze

Read every artifact in full. For each, gather what its card needs, using
`references/card-section-guide.md` — which source part feeds which section, how to find
failure modes, what Provenance may say. Keep these notes in context; never write them to
the repository.

**Gate:** each failure mode is observed or structural, and labelled; each card instances
at least one pattern card that exists in `cards/`.

### 3. Plan and mask — one combined gate

1. `python3 <this-skill>/scripts/find_identifiers.py <skill-dir>` → candidates by shape.
   It finds paths, addresses, domains and the skill's own name; it cannot judge a name.
   Read the source for the rest: organizations, people, codenames, sibling component names,
   timezones, environment naming.
2. Split every compound identifier into its parts — a path with a username, an organization
   and a repository becomes three rows.
3. Choose generic titles and slugs. Never the source component's own name or its siblings'.
4. Fill `assets/gate-report.md` and show it **in chat**: bundle plan, files not becoming
   cards, masking table, wiring this run will do.
5. Save the approved rows as `{"rows": [{"original": …, "replacement": …}]}` to a file
   **outside the repository** (the session scratchpad) for phase 6.

**Gate:** the owner explicitly approves. Any change produces a new report and a new
approval. Nothing is written before it.

### 4. Write

1. Branch `feat/cards-component-NN-<slug>` from `origin/main`. If another session shares the
   checkout, use a git worktree.
2. One card per artifact from `ai-engineering-knowledge-cards/templates/COMPONENT_CARD_TEMPLATE.md`:
   the skill card at `component-cards/skills/<slug>/NN-<slug>.md`, its parts beneath it in
   `references/`, `assets/`, `scripts/`. Resolve `<up>` for each depth.
3. One skeleton per card at `skeletons/components/NN-<slug>/` — a fresh standard-library
   implementation over fabricated fixtures, with `## Try it` and *What is deliberately
   missing*. See the guide's skeleton section.

**Gate:** apply the masking table while writing — no original enters a file, even
temporarily.

### 5. Wire

Edit only these, outside the new card and skeleton directories:

- reverse `related:` edges in the sibling component cards named in the plan;
- `ai-engineering-knowledge-cards/INDEX.md` — one component-table row per new card;
- the component-card count in `AGENTS.md`, `docs/_base/ARCHITECTURE.md` and
  `.claude/agents/codebase-analyst.md`;
- `ai-engineering-knowledge-cards/diagrams/README.md` — a pending row per diagram the run
  did not draw. Diagrams are not drawn here; list them as follow-ups.

Never edit `.claude/rules/`, `check.py`, the templates, or pattern cards in `cards/`.

**Gate:** `python3 <this-skill>/scripts/wire_check.py` exits 0.

### 6. Verify and deliver

1. `python3 check.py --run` exits 0 and the tree is clean.
2. Run every command in each new skeleton README's `## Try it` block.
3. `python3 <this-skill>/scripts/residue_check.py --table <scratch-table.json> --changed-since origin/main`
   exits 0. A hit means an original reached a file: fix it before anything else.
4. Commit by logical unit with the scope taxonomy — the cards and skeletons as `feat(cards)`;
   a `Context:` trailer if anything under `.claude/` changed.
5. Show the final diff summary — files, cards, skeletons, wiring — and ask: **"Publish?"**
   The repository is public; this is the last look before history is permanent.
6. On yes: push, and open a PR from `.github/PULL_REQUEST_TEMPLATE.md`, recording that the
   extraction was authorized and the residue check passed. Never quote the masking table.

**Gate:** the owner says yes to publication. Without it, stop with the commits local.

## Never

- Write anything before the phase 3 approval, or push before the phase 6 confirmation.
- Put an original in a file, commit message, PR body or code comment. Originals live in
  the chat report and the scratch table only.
- Reuse a worked example from the source, or copy its code into a skeleton.
- Upgrade a failure mode from hypothetical to observed to fill a table.

## Resources

- `scripts/inventory.py` — skill directory → mode, numbers, card types
- `scripts/find_identifiers.py` — masking-table candidates by shape (output holds originals: chat only)
- `scripts/residue_check.py` — every original in the table, searched in the new files; reports row numbers, never values
- `scripts/wire_check.py` — INDEX rows and the three restated counts
- `references/card-section-guide.md` — source part → card section, failure-mode kinds, Provenance, skeleton rules, local mode
- `assets/gate-report.md` — the shape of the phase 3 chat report
