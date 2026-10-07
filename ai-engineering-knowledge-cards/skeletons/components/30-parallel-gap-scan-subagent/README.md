# Skeleton — Parallel Gap-Scan Subagent

A harness's view of the subagent the hardening orchestrator dispatches to scan
roles for missing hardening fields. The card is
[component 30](../../../component-cards/subagents/30-parallel-gap-scan-subagent.md);
the skill that dispatches it is [component 08](../08-workstream-hardening-orchestrator/).

```
agent.md      a fabricated subagent definition in the component's shape: name,
              description and model in frontmatter; tool limits and a skip list
              in the body
lists.json    the tools a harness has, and the two other skip lists — the field
              scanner's and the remediation guide's
dispatch.py   what the harness grants against what the prose forbids, and the
              three skip lists side by side
```

## Try it

```bash
python3 dispatch.py              # granted and forbidden; three lists disagree; exits 1
python3 dispatch.py --narrowed   # with a tools: line; the grant is fixed, the lists are not; exits 1
```

**The grant.** With no `tools:` key in the frontmatter, the harness grants
everything it has, and the three tools the body says not to use are among
them. The body's limits are words the model is trusted with —
[card 16](../../../cards/16-the-permission-ladder.md)'s lowest rung.
`--narrowed` adds the one line that turns the same words into a grant, and the
overlap disappears.

**The lists.** The roles the subagent skips, the roles the field scanner treats
as exceptions, and the roles the remediation guide says need special handling
are three lists of the same fact, and no two agree. `--narrowed` does not touch
them, so it still exits 1.

## What is deliberately missing

**The scan itself.** The subagent's work — reading role files for four fields —
is the field scanner's, and its skeleton is
[component 23](../23-hardening-field-scanner/).

**Discovery.** The component's file sat inside the skill's own directory, not
where a harness looks for subagents. This skeleton parses the file directly,
as if it had been found.

**A model.** The definition names a small, cheap model. Nothing here calls one.
