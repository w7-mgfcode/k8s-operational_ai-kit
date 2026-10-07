# Skeleton — Role Spawn Prompt Set

Copy-ready prompts for the three roles, and a check of what they do against the phase
table of the skill that owns them. The card is
[component 42](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/42-role-spawn-prompt-set.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
prompts/       three fabricated prompts with {slot} placeholders, one per role
skill/         stand-ins for the skill's reference files — contents are placeholders
workspace/     the directory a spawned agent starts in; it holds no references
phases.json    what each phase must load, the role's tool list, and what the spawn grants
context_*.json one filled context and one with the contract slot missing
render_prompts.py   renders a prompt to a stubbed spawn; --lint audits the set
```

## Try it

```bash
python3 render_prompts.py --lint                                     # nine findings across three roles; exits 1
python3 render_prompts.py --role evaluator --context context_full.json     # renders; exits 0
python3 render_prompts.py --role evaluator --context context_partial.json  # a literal slot goes out; exits 0
python3 render_prompts.py --role evaluator --context context_partial.json --strict   # refused; exits 1
```

The `[stub] spawn_subagent` lines stand where the component calls the agent tool.

**The lint.** The evaluator prompt omits one file its phase requires (the failure catalog). Its relative reads
point at a skill directory the spawned agent does not start in. The implementer prompt is
handed the contract and told not to use evaluation criteria. All three roles are spawned
as one general kind, so each holds tools its own role list leaves out.

**The slot.** Without `--strict`, an unfilled placeholder is sent as the text
`{contract}`. The component's prompts are checked by no one; `--strict` is the check.

## What is deliberately missing

**The real prompts.** These are short and fabricated; the card describes the real ones.

**A real spawn.** `spawn_subagent()` prints. Whether a given harness resolves
relative paths from the skill directory or the workspace is the harness's behaviour,
modelled here as the workspace.

**The fix, for the pattern.** Prompts that name every file their phase requires,
absolute paths or inlined content, a typed subagent carrying a tool list, and a render
step that refuses unfilled slots — the last is the only one `--strict` demonstrates.
[Card 07](../../../cards/07-capability-taxonomy.md) is the part of the pattern that
the typed subagent belongs to.
