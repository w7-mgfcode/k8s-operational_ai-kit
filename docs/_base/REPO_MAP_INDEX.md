# Repository Map Index

> Where things live, and which file answers which question.
> **Hand-written, not generated.** No generator exists in this repository; the structured KB one
> would read (`docs/_kB/repo-map/`) was never built, because its only possible input is the
> excluded legacy tree. Last reviewed: 2026-10-01.

## Navigation

| Path | What it answers | Load when |
| --- | --- | --- |
| `AGENTS.md` | Stack, commands, gates, conventions, safety — the cross-tool brief | Always. Every agent, every session |
| `CLAUDE.md` | Claude-specific operating index; imports `AGENTS.md` | Always, in Claude Code |
| `check.py` | What is enforced and how | Before committing; when a check fails |
| `.claude/rules/README.md` | Which rule governs which path | Adding a rule; working as a non-Claude agent |
| `.claude/rules/*.md` | The normative contracts | When your path matches the glob |
| `.claude/agents/*.md` | The three subagents: codebase-analyst, research-agent, code-reviewer | Delegating analysis or review |
| `.github/` | `ci.yml` (the gate in CI), three agent workflows (secrets unset), `copilot-instructions.md` | Changing CI or the Copilot adapter |
| `docs/_base/ARCHITECTURE.md` | Layer structure, ownership, blast radius | Changing a contract or the structure |
| `docs/_base/RULES.md` | Full constraint matrix, what is deliberately absent, open items | Needing the whole picture |
| `docs/_base/SECURITY.md` | What may be published; how the boundary is enforced and where it leaks | Anything publishable |
| `docs/_base/DEV_GUIDE.md` | Adding a card or skeleton, end to end | Doing the work |
| `docs/_base/REPO_MAP_INDEX.md` | This table | Lost |

## The Published Project

| Path | What it answers | Load when |
| --- | --- | --- |
| `ai-engineering-knowledge-cards/README.md` | What the repository is, for a reader arriving cold | Framing, positioning |
| `ai-engineering-knowledge-cards/INDEX.md` | The cards by layer, by card, and by symptom | Finding the right card |
| `.../cards/NN-*.md` | One pattern each, 13 sections | Studying or editing a pattern |
| `.../skeletons/NN-*/` | One runnable prototype per card | Seeing the pattern work, or fail |
| `.../skeletons/pipelines/session-memory-loop/` | Cards 12→13→14→15 as one engine | Understanding how the memory patterns compose |
| `.../component-cards/<type>/NN-*.md` | One concrete artifact each, 11 sections | Studying or editing a component |
| `.../skeletons/components/NN-*/` | One prototype per component card | Seeing a component work, or fail |
| `.../templates/CARD_TEMPLATE.md` | The card shape | Authoring a card |
| `.../templates/COMPONENT_CARD_TEMPLATE.md` | The component-card shape | Authoring a component card |
| `.../teaching/NN-*.md` | Condensed teaching versions of cards (untracked, no contract yet) | Preparing a seminar |
| `.../docs/ANONYMIZATION.md` | What was masked, in what quantity, under which rule | Auditing the boundary |
| `.../docs/README-OUTLINE.md` | The planning outline the README was built from | Historical; superseded by README.md |

## By Question

| Question | Go to |
| --- | --- |
| What command do I run before committing? | `AGENTS.md` § Validation Gates |
| Why did `check.py` fail? | `docs/_base/DEV_GUIDE.md` § Common Failures |
| May I publish this sentence? | `docs/_base/SECURITY.md`, then `.claude/rules/anonymization.md` |
| What breaks if I edit the card template? | `docs/_base/ARCHITECTURE.md` § Blast Radius |
| How do I name this commit? | `.claude/rules/git-workflow.md` |
| Which card covers my problem? | `ai-engineering-knowledge-cards/INDEX.md` § By question |
| What is `.legacy-assets/` and may I read it? | `docs/_base/SECURITY.md` — the answer is no |
| What is knowingly unfinished? | `docs/_base/RULES.md` § Known Open Items |

## Excluded From the Map

| Path | Why |
| --- | --- |
| `.legacy-assets/` | Un-anonymized source. Gitignored. Never a source for published output |
| `**/.venv/` | Two 136 MB vendored virtualenvs under the excalidraw skill |
| `.agents/`, `.claude/commands/`, `.claude/skills/*` | Vendored agent tooling, gitignored; only `knowledge-card-summarizer` is project-authored |
| `docs/_kB/` | Read-only KB input by convention; only an unrelated note exists here |
