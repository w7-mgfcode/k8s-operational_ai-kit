# Architecture

> Layer structure, ownership boundaries, and what a change to each layer breaks.
> Heuristic mode: written from the tree, not from a structured KB. Last reviewed: 2026-10-01.

## System Boundaries

### What this repository owns

- The twenty knowledge cards, the seven component cards, and the contracts they obey.
- One runnable skeleton per card, plus one compound pipeline walkthrough.
- The anonymization policy and its audit record.
- The agent-context layer: `.claude/rules/`, `.claude/agents/`, the one project-authored skill
  (`.claude/skills/knowledge-card-summarizer/`), `AGENTS.md`, `CLAUDE.md`,
  `.github/copilot-instructions.md`. Other skills and commands are vendored and gitignored.
- The validation gate, `check.py`, and the CI that runs it (`.github/workflows/ci.yml`).

### What it consumes

| Dependency | Interface | Change process |
| --- | --- | --- |
| `.legacy-assets/` | Read-only, gitignored, **never a source for published output**, except component-card extraction under `.claude/rules/anonymization.md` | Frozen. Excluded from the repository by `.gitignore`; see SECURITY.md |
| Python 3 standard library | `python3` on PATH | None — no dependency file; CI pins 3.12, no minimum is enforced |
| GitHub Actions | `.github/workflows/` | Edit the workflow; `ci.yml` runs the same gate as local |

### What depends on this repository

Nothing programmatic. The consumers are readers and the agents editing it. That means the
blast radius of a change is **comprehension**, not runtime — a wrong card misleads, it does not
crash.

## Layer Structure

```
k8s-operational_ai-kit/
├── AGENTS.md            universal agent brief      ← contract for agents
├── CLAUDE.md            thin Claude layer, @imports AGENTS.md
├── check.py             the single validation gate
├── .claude/rules/       path-scoped contracts      ← governs everything below
├── docs/_base/          deep dives (this file)
└── ai-engineering-knowledge-cards/
    ├── README.md        public framing
    ├── INDEX.md         reader-facing map: by layer, by card, by question
    ├── cards/           20 patterns, 13 sections each
    ├── component-cards/ one artifact per card, nested under the skill that owns it — 11 sections each
    ├── skeletons/       20 prototypes + pipelines/ + components/
    ├── templates/       CARD_TEMPLATE.md, COMPONENT_CARD_TEMPLATE.md
    ├── teaching/        condensed teaching cards (12 of 20) — format set by the
    │                    knowledge-card-summarizer skill, not checked by check.py
    └── docs/            ANONYMIZATION.md, README-OUTLINE.md
```

## Components

| Component | Type | Path | Contract |
| --- | --- | --- | --- |
| Cards | Markdown, fixed schema | `cards/*.md` | `.claude/rules/cards.md` |
| Skeletons | Python 3 stdlib + README | `skeletons/<card-slug>/` | `.claude/rules/skeletons.md` |
| Component cards | Markdown, fixed schema | `component-cards/skills/<skill>/**/*.md`, `component-cards/<type>s/*.md` | `.claude/rules/component-cards.md` |
| Component skeletons | Python 3 stdlib + README | `skeletons/components/<card-stem>/` | `.claude/rules/component-cards.md` + `skeletons.md` |
| Pipeline walkthrough | Bash orchestrator | `skeletons/pipelines/session-memory-loop/` | Same, plus idempotency — not executed by `check.py --run` |
| Rules | Markdown with `paths:` frontmatter | `.claude/rules/*.md` | Indexed in its own README |
| Gate | Python 3 stdlib | `check.py` | Exits 0, cleans up after `--run` |

## Blast Radius

Ranked by what a change forces downstream — the same reasoning card 17 applies to
infrastructure.

| Change | Radius | Consequence |
| --- | --- | --- |
| `templates/CARD_TEMPLATE.md` or `.claude/rules/cards.md` | **critical** | Every one of 20 cards must be re-checked; the section count is mechanically enforced |
| `templates/COMPONENT_CARD_TEMPLATE.md` or `.claude/rules/component-cards.md` | **high** | Every component card and its skeleton; `check.py` enforces the section count and `instances:` targets |
| `.claude/rules/skeletons.md` | **critical** | Every skeleton README and script is re-scoped |
| `.claude/rules/anonymization.md` | **critical** | Changes what may be published; invalidates the audit record if loosened |
| `check.py` | **high** | The only gate. A weakened check is silent |
| `.claude/rules/git-workflow.md` | **high** | Governs every commit, and the `Context:` trailer for agent assets |
| A single card | **medium** | Its `related:` neighbours may now be wrong in both directions |
| A single skeleton | **low** | Self-contained, unless the pipeline walkthrough calls it |
| `README.md` / `INDEX.md` | **low** | Navigation only — but `INDEX.md` restates each card's maturity, which drifts |

**The one non-obvious coupling:** `INDEX.md` carries a maturity column, a maturity count, and each
component card's `instances:`. Changing that front matter without updating `INDEX.md` leaves the
two disagreeing, and `check.py` does not catch it.

## Change Flow

```
branch → edit → python3 check.py --run → exit 0 and clean tree → commit (+ Context: trailer
if agent assets changed) → PR → ci.yml runs the same gate → merge
```

There is no staging, no artifact, no release. Merged is published.

## Observability

None, and none is warranted. The repository has no runtime. The only signal is `check.py`'s
exit code, locally and in CI.
