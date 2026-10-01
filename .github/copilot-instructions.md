# Copilot instructions

**Read `AGENTS.md` in the repository root. It is the single source of truth for
this repository's rules.** This file adds Copilot-specific mechanics, and repeats
only the five essentials below in case the pointer is not followed.

## The essentials, so you have them inline

- **This is a documentation and prototype repository.** Markdown pattern cards in
  `ai-engineering-knowledge-cards/cards/` and component cards in
  `ai-engineering-knowledge-cards/component-cards/`, one Python skeleton per card in
  `ai-engineering-knowledge-cards/skeletons/`. There is no application, no `package.json`, no build, no linter
  and no test framework. Do not suggest adding one.
- **Verify with `python3 check.py --run`.** It must exit 0 and leave the tree
  clean. This is exactly what `.github/workflows/ci.yml` runs.
- **Skeletons are standard library only.** Never suggest a `pip install` or a
  third-party import.
- **`.legacy-assets/` is off-limits.** Never read, quote or summarize it, and
  exclude it from every search.
- This repository is **public**. Never suggest committing a token, `.env`, or a
  virtualenv.

## Path-scoped rules

`.claude/rules/*.md` holds shared policy, despite the directory name. Copilot does
not auto-load it, so before editing a file, check `.claude/rules/README.md` and
read the rule whose glob matches. The index is the map.

## Commits

Conventional Commits with the scope taxonomy in `.claude/rules/git-workflow.md`.
Branch first; never commit directly to the default branch.
