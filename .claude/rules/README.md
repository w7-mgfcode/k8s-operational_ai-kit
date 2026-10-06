# Tier 2 — On-Demand Rules

Each rule file carries a `paths:` frontmatter glob. Claude Code auto-loads the
rule when it touches a matching file, so domain conventions stay out of the
always-on context until needed (progressive disclosure — the "Select" strategy
of WISC).

**Not every agent has path-glob loading.** Claude Code does; Copilot, via
`.github/copilot-instructions.md`, does not, and any future Codex or Gemini
router will not either. Those agents are told to consult this index and read the
matching rule by hand. That makes this table load-bearing, not decorative — a
rule missing from it is invisible to every agent except Claude Code.

| File | Auto-loads when touching | Covers |
| --- | --- | --- |
| `anonymization.md` | `ai-engineering-knowledge-cards/**`, `.gitignore` | The masking rule; `.legacy-assets/` is readable, never written or tracked, and published only through component-card extraction; what must never enter the repo |
| `cards.md` | `ai-engineering-knowledge-cards/cards/**`, `ai-engineering-knowledge-cards/templates/CARD_TEMPLATE.md`, `ai-engineering-knowledge-cards/docs/**` | Six frontmatter keys, thirteen sections, what `maturity: partial` means, provenance |
| `skeletons.md` | `ai-engineering-knowledge-cards/skeletons/**` | Stdlib-only, offline, runnable as committed, deliberate gaps stated |
| `component-cards.md` | `ai-engineering-knowledge-cards/component-cards/**`, `ai-engineering-knowledge-cards/templates/COMPONENT_CARD_TEMPLATE.md`, `ai-engineering-knowledge-cards/skeletons/components/**` | Five frontmatter keys, eleven sections, one artifact per card, cards nested under the skill that owns them, stricter anonymization, legacy extraction only by named authorization |
| `subagents.md` | `.claude/agents/**` | Three distinct roles; `tools:` is a narrowing; cite or admit; this repo's real shape |
| `skills.md` | `.claude/skills/**`, `.agents/**` | Vendored not managed, and gitignored; the broken MCP config; one place per skill; `allowed-tools`; routing descriptions |
| `permissions.md` | `.claude/settings.json`, `.claude/hooks/**` | The one boundary `settings.json` serves: read-allow, Edit deny, the Bash guard hook, `claudeMdExcludes` — and what none of them covers |
| `git-workflow.md` | `.claude/**`, `.agents/**`, `.github/**`, `ai-engineering-knowledge-cards/**`, `AGENTS.md`, `CLAUDE.md`, `check.py`, `docs/_base/**`, `.gitignore` | Types, the one scope taxonomy, the `Context:` trailer, prohibitions |

## Adding a rule

1. Create `.claude/rules/<concern>.md` with a `paths:` frontmatter listing the
   globs that should trigger it.
2. Keep it information-dense: real file paths, real patterns, concrete
   anti-patterns, and the failure mode each rule prevents.
3. Add a row to this table. **This step is not optional** — see above.
4. Log the addition in the commit's `Context:` section (see `git-workflow.md`).

**Verify every glob matches a file that exists right now.** A glob that matches
nothing is a rule that never loads. This set was rebuilt in September 2026 after
an audit found that eight inherited rules carried 36 dead globs between them and
that 74% of their cited paths did not resolve — they had been imported from a
different repository and described a React site this project does not have.

A rules file that lies to the agent is worse than none.

## Deferred

Concerns that are real but have nothing to govern yet. Each returns as a rule in
the same change that creates its target — not before.

- **Agent-instruction layer** — the one-rulebook / thin-adapter doctrine. Its
  target now exists: root `AGENTS.md`, with `CLAUDE.md` and
  `.github/copilot-instructions.md` as adapters. The rule is **owed, not yet
  written**. `.claude/commands/` exists but is vendored and gitignored; there is
  still no `.gemini/` and no `.codex/`.
- **CI gates** — `.github/workflows/ci.yml` runs `python3 check.py --run` plus a
  clean-tree check on push and pull request to `main`. The rule is **owed, not
  yet written**. The three agent workflows fail without their secrets.
- **Structural lint** — card 15, applied to this repository. `check.py` now
  covers frontmatter and link resolution for cards. It does not check index
  coverage, orphans, or that `INDEX.md`'s maturity column matches the cards.
