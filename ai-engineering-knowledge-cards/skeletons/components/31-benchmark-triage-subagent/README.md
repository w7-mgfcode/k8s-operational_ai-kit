# Skeleton — Benchmark Triage Subagent

The subagent the hardening orchestrator dispatches to turn a benchmark report
into a triage table, replayed under three tool grants. The card is
[component 31](../../../component-cards/subagents/31-benchmark-triage-subagent.md);
the skill that dispatches it is [component 08](../08-workstream-hardening-orchestrator/).

```
agent.md       a fabricated subagent definition in the component's shape: Bash
               and Read allowed in prose, Edit and Write forbidden, and the
               classification rule restated
actions.json   what the subagent sets out to do: read, parse, parse to a file,
               render the table, and one direct write
rules.json     the parser's classification table, as code holds it
dispatch.py    each action allowed or blocked under each grant, the writes left
               possible, and the two copies of the classification rule
```

## Try it

```bash
python3 dispatch.py    # three grants, then the rule twice; exits 1
```

**As shipped**, with no `tools:` key, everything is allowed, the direct write
included. **With the prose turned into a grant** — Bash and Read — the direct
write is blocked and two writes remain: a redirect, and the renderer the job
depends on. The ban blocks the two tools whose names it lists; Bash writes
files just as well. **With Read alone**, nothing writes, and nothing gets done.

**The rule.** The subagent's prose and the parser's table agree. Both leave CIS
section 2 unclassified, which is the parser's flaw
([component 24](../24-benchmark-report-parser/)) restated, not caught: two
copies that agree are not a check.

Exit 1 marks that no grant lets the job run without writing files.

## What is deliberately missing

**The scripts.** The parser and renderer are
[component 24](../24-benchmark-report-parser/) and
[component 22](../22-triage-table-renderer/); here they are names in a replay.

**A real narrowing.** What would contain the writes is the output path, not the
tool list: the orchestrator passes the path, and the renderer refuses any
other. The source had neither; [card 16](../../../cards/16-the-permission-ladder.md)
covers why a tool list is the wrong unit.
