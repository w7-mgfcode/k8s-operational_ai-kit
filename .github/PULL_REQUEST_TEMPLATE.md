<!--
Title format: <type>(<scope>): <description>, with (#<issue>) when there is one.
e.g. `feat(cards): add card 21 tool-result caching (#12)`
Scopes: cards · skeletons · docs · agents · ci
Full rules: .claude/rules/git-workflow.md
-->

## What changed

<!-- One or two sentences. The diff shows what; say why. -->

## Why

<!-- The context that is not obvious from the diff. -->

Closes #

<!--
Include `Closes #<issue>` when this PR implements a tracked issue — it is what
links the PR to the issue on merge. Delete the line if there is no issue.
-->

## Verification

- [ ] `python3 check.py --run` exits 0 and leaves `git status` clean
- [ ] Staged diff checked by hand for names the gate cannot catch
      (docs/_base/SECURITY.md § Before Publishing) — this repository is public
- [ ] If a card's `maturity` or a component card's `instances:` changed, `INDEX.md` changed with it
- [ ] New or changed `related:` edges exist in both directions

<!-- Name any gate you could not run, and why. Do not leave a box checked that
     you did not actually run. -->

Gates not run:

## Agent-context changes

- [ ] This PR changes no agent-context asset, **or** the commit body carries a
      `Context:` trailer naming what an agent will now see differently

<!-- Agent-context assets (.claude/rules/git-workflow.md): anything under
     .claude/ or .agents/, AGENTS.md, CLAUDE.md, .github/copilot-instructions.md.
     A new rule also needs its row in .claude/rules/README.md. -->

## Risk

- [ ] Reversible by revert
- [ ] Touches no file outside the stated scope
- [ ] Reads nothing from `.legacy-assets/`, or is a component-card extraction the owner authorized
