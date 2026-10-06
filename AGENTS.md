# AGENTS.md

Universal agent brief for **k8s-operational_ai-kit** — the shared, cross-tool source of truth
for any AI coding agent working in this repository. Plain Markdown, no frontmatter. Every token
here loads on every request, so it carries only what an agent would get wrong without it.

## Project Overview

This repository publishes **AI Engineering Knowledge Cards**: twenty engineering patterns
extracted from a private agent kit that operated a production Kubernetes platform, rewritten so
they teach the pattern and identify nothing. Each card ships a minimal runnable prototype.
Six **component cards** (`ai-engineering-knowledge-cards/component-cards/`) each describe one concrete artifact that instances
those patterns, under their own contract, `.claude/rules/component-cards.md`.

It is a **documentation and prototype repository**. There is no application, no service, no
deployment. The product is the cards, their skeletons, and the honesty of both.

Its defining constraint: the source material is real, private, and on disk. Everything published
here passes an anonymization boundary that is enforced at edit time, not at review time.

## Tech Stack

- **Content** — Markdown. Cards, skeleton READMEs, deep-dive docs.
- **Prototypes** — Python 3, **standard library only**. No dependencies, no virtualenv, no
  package manager. `python3 --version` ≥ 3.9; developed against 3.14.
- **Validation** — `check.py` at the repository root. Standard library, no network, no cost.
- **CI** — GitHub Actions. `ci.yml` runs the same `check.py`. The three agent workflows need
  secrets that are not configured, and fail when they run. See
  `docs/_base/RULES.md` § Known Open Items.
- **Deliberately absent** — no `Makefile`, no `package.json`, no `pyproject.toml`, no linter,
  no formatter, no test framework. Do not add one without being asked.

## Setup

```bash
git clone <repo> && cd k8s-operational_ai-kit
python3 check.py          # no install step — there is nothing to install
```

## Build & Test Commands

Use these exact strings.

```bash
python3 check.py           # contracts, links, imports, anonymization  (~1s)
python3 check.py --run     # the above, plus execute every skeleton    (~20s)
python3 check.py --quiet   # failures only; use in scripts
```

There is no build. There is no separate test suite — the skeletons are the tests, and
`--run` executes them.

## Validation Gates

`python3 check.py` is the single gate. It must exit 0 before every commit, and CI runs the same
command on every push and pull request. Seven checks:

| Check | Enforces |
| --- | --- |
| cards | 13 `##` headings, the 6 frontmatter keys in order, number matches filename, valid `layer` and `maturity`, Provenance present, every `related:` edge resolves and runs both ways |
| component cards | 11 `##` headings, the 5 frontmatter keys in order, number unique and matching filename, `type` matches its place in the layout (a skill's references, assets and scripts nest under it), every `instances:` slug is a card, every `related:` edge resolves, runs both ways and includes the owning skill, a skeleton under `skeletons/components/` |
| links | every relative Markdown link under `ai-engineering-knowledge-cards/` resolves (`templates/` is exempt — its `NN-` placeholders are the point). Links elsewhere are not checked |
| skeletons | every card has a skeleton directory whose README has `## Try it` and a *deliberately missing* section |
| imports | every skeleton script imports standard library only |
| anonymization | no home-directory path, IP address, `.local`/`.internal`/`.corp`/`.lan` domain or credential shape in any file git would publish, outside the declared teaching exemptions. It cannot catch a name |
| execution (`--run`) | every top-level skeleton script (pattern and component) runs without crashing, and the gate cleans up what it wrote. Nested scripts and the `pipelines/` walkthrough are not run |

Exit codes inside skeletons: **0** = ran, **1** = ran and demonstrated a failure *on purpose*,
**2** = requires arguments. Only a crash is a failure. Several skeletons exit 1 by design.

## Architecture & Conventions

- **Three layers.** `ai-engineering-knowledge-cards/cards/` holds the patterns (and
  `ai-engineering-knowledge-cards/component-cards/` the artifacts that instance them),
  `ai-engineering-knowledge-cards/skeletons/` holds one runnable prototype
  per card, `.claude/rules/` holds the contracts both obey. A change to a contract changes every
  artifact under it.
- **The card contract is binding.** Thirteen sections in the template's order, six frontmatter
  keys, `instanced_by` generic rather than a real path. `.claude/rules/cards.md` is normative;
  `templates/CARD_TEMPLATE.md` is the shape.
- **`maturity: partial` is not a defect.** It means the source system implemented part of the
  pattern and the card says which part. Never upgrade a `partial` to `proven` to make a card
  read better. Never write a Failure-modes table containing only hypotheticals.
- **Skeletons are promises.** Standard library, offline, runnable as committed, generic. Model
  calls are stubbed behind a named function that prints. A skeleton that leaves the working tree
  dirty is a bug in the skeleton.
- **Deliberate gaps are content.** Every skeleton README ends with what is missing. A gap
  faithful to the source system belongs in the README; hiding it turns the skeleton into a demo.
- **Cross-reference, do not restate.** Cards link to each other by number; rules link to each
  other; nothing is stated twice.

## Testing Requirements

- A new card requires a skeleton directory, or `check.py` fails.
- A new skeleton requires a README with `## Try it` and *What is deliberately missing*, and every
  command in that `## Try it` block must actually run from a fresh clone.
- A skeleton that writes state must clean up after itself or be idempotent.
- Changing `templates/CARD_TEMPLATE.md` or a file in `.claude/rules/` means re-running
  `python3 check.py --run`, because it changes the contract every card obeys.

## Safety

**Hard rules — never violate:**

- **`.legacy-assets/` is never a source.** It holds the un-anonymized kit. Never read it into a
  card, a skeleton, a commit message, or a report; never quote, summarize or paraphrase it. You
  may state that it exists and is excluded. The one exception is component-card extraction,
  and only under the conditions in `.claude/rules/anonymization.md` — a directory the user names
  and a masking table the user approves before anything is written.
- **Never reintroduce a masked identifier** — organization names, operator usernames, absolute
  paths from the source system, internal domains, hostnames and their naming scheme, internal
  IPs and CIDRs, the source repository name, project codenames, named personal tooling, the
  operator's timezone. `check.py` catches the mechanical shapes; it cannot catch a name.
- **Never commit a virtualenv, `__pycache__`, `.env`, a token or a credential.** This repository
  is public. A ~140 MB virtualenv exists under the excalidraw skill and is
  gitignored — verify before staging.
- **Never add a dependency to a skeleton.** Standard library only is the contract, not a
  preference.
- **Never commit directly to `main`** unless explicitly asked. Branch first.

**Stop and ask before:**

- Deleting or rewriting a card, or changing a card's `maturity`.
- Editing `.claude/rules/` — those files govern every other agent that reads this repo.
- Anything that would publish, push, or otherwise make the repository externally visible.

## Git & PR Conventions

Conventional Commits, one logical unit per commit. Types, the single scope taxonomy
(`cards` `skeletons` `docs` `agents` `ci`), branch naming, and the required `Context:` trailer
are defined once in **`.claude/rules/git-workflow.md`** — read it rather than guessing.

`main` is the default branch, locally and on GitHub; `ci.yml` runs the gate on every push and
pull request to it. Work happens on a `<type>/<scope>-<slug>` branch and reaches `main` by PR.

## Deep-Dive Docs

Load on demand; do not read them all.

| Doc | Read when |
| --- | --- |
| `docs/_base/ARCHITECTURE.md` | Changing the layer structure, or reasoning about what a contract change breaks |
| `docs/_base/RULES.md` | You need the full constraint matrix and which rule owns which path |
| `docs/_base/SECURITY.md` | Anything touching the anonymization boundary or what may be published |
| `docs/_base/DEV_GUIDE.md` | Adding a card or a skeleton, end to end |
| `docs/_base/REPO_MAP_INDEX.md` | Navigating the repository, or finding which file answers a question |

`ai-engineering-knowledge-cards/INDEX.md` is the reader-facing map of the cards themselves —
by layer, by card, and by the question that brought someone here.
