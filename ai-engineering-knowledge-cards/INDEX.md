# Index

Twenty cards, ordered structural-first — which is also the order they build on
each other. Three views: by layer, by card, and by the question that brought you
here.
A fourth section lists the component cards: single artifacts that instance them.

## By layer

```
INSTRUCTION   01  One Contract, Many Routers
              04  Path-Scoped Rule Loading
              05  Instruction Provenance and Drift
              06  Calibrated Degrees of Freedom

ROUTING       02  Progressive Disclosure
              03  Description-as-Router
              07  Capability Taxonomy: Skill, Command, Subagent

SKILL         08  Interview Before Generation
              09  Scaffold, Validate, Package
              10  Behavioral Evaluation Harness

SUBAGENT      11  Adversarial Role Separation

MEMORY        12  Lifecycle Hooks as Capture Points
              13  Log-as-Source Knowledge Compilation
              14  Index-Guided Retrieval
              15  Structural Lint for Knowledge Bases

EXECUTION     16  The Permission Ladder
              17  Blast-Radius Gating
              18  The Redaction Boundary
              19  Scope Lock and Checkpoint Delivery

VALIDATION    20  Repository Projection Pipeline
```

## By card

| # | Card | Layer | Maturity | The idea in one line |
| --- | --- | --- | --- | --- |
| 01 | [One Contract, Many Routers](cards/01-one-contract-many-routers.md) | instruction | partial | One rulebook; every other agent file is a thin adapter that imports it |
| 02 | [Progressive Disclosure](cards/02-progressive-disclosure.md) | routing | proven | Three loading levels, so context cost scales with relevance rather than with inventory |
| 03 | [Description-as-Router](cards/03-description-as-router.md) | routing | proven | The description field is the routing table, not documentation |
| 04 | [Path-Scoped Rule Loading](cards/04-path-scoped-rule-loading.md) | instruction | partial | Rules attach to file globs, so conventions arrive only when they apply |
| 05 | [Instruction Provenance and Drift](cards/05-instruction-provenance-and-drift.md) | instruction | abandoned | Imported instructions describe a system you do not have, and nothing detects it |
| 06 | [Calibrated Degrees of Freedom](cards/06-calibrated-degrees-of-freedom.md) | skill | proven | Match instruction specificity to task fragility: prose, pseudocode, or a script |
| 07 | [Capability Taxonomy](cards/07-capability-taxonomy.md) | routing | proven | Skill, command and subagent are three routing mechanisms, not three names |
| 08 | [Interview Before Generation](cards/08-interview-before-generation.md) | skill | proven | Elicit the spec through a role-based interview before generating anything |
| 09 | [Scaffold, Validate, Package](cards/09-scaffold-validate-package.md) | skill | proven | A build pipeline for capabilities, where packaging refuses to run on a failed check |
| 10 | [Behavioral Evaluation Harness](cards/10-behavioral-evaluation-harness.md) | validation | partial | Routing is a claim about model behavior, so test it by replaying real prompts |
| 11 | [Adversarial Role Separation](cards/11-adversarial-role-separation.md) | subagent | proven | The agent that builds never grades its own work, against a contract fixed in advance |
| 12 | [Lifecycle Hooks as Capture Points](cards/12-lifecycle-hooks-as-capture-points.md) | memory | proven | Capture at session boundaries must be fail-open, fast, and stupid |
| 13 | [Log-as-Source Compilation](cards/13-log-as-source-compilation.md) | memory | partial | Transcripts are source, the model is a compiler, a content hash makes it incremental |
| 14 | [Index-Guided Retrieval](cards/14-index-guided-retrieval.md) | memory | partial | Read the index, pick the articles, answer — no embeddings, no vector store |
| 15 | [Structural Lint](cards/15-structural-lint.md) | validation | partial | Cheap mechanical checks on a knowledge base: broken links, orphans, outliers |
| 16 | [The Permission Ladder](cards/16-the-permission-ladder.md) | execution | proven | Allow, ask, deny — and the deny list is the only rung that is not advice |
| 17 | [Blast-Radius Gating](cards/17-blast-radius-gating.md) | execution | proven | Classify by dependent count, and check before the change rather than after |
| 18 | [The Redaction Boundary](cards/18-the-redaction-boundary.md) | execution | partial | One scrubbing gate between raw output and anything durable, biased to over-redact |
| 19 | [Scope Lock and Checkpoint Delivery](cards/19-scope-lock-and-checkpoint-delivery.md) | execution | proven | Freeze scope in a file before work starts; deliver at named checkpoints |
| 20 | [Repository Projection Pipeline](cards/20-repository-projection-pipeline.md) | validation | partial | Project a codebase into a knowledge pack, then detect when it goes stale |

## By question

| Symptom | Card |
| --- | --- |
| "My agent loads the wrong skill, or no skill at all." | [03](cards/03-description-as-router.md), then [10](cards/10-behavioral-evaluation-harness.md) |
| "My instruction file is too long and the agent ignores the middle of it." | [02](cards/02-progressive-disclosure.md), [04](cards/04-path-scoped-rule-loading.md) |
| "My rules reference files that do not exist." | [05](cards/05-instruction-provenance-and-drift.md) |
| "The agent keeps re-deriving the same thing across sessions." | [12](cards/12-lifecycle-hooks-as-capture-points.md) → [13](cards/13-log-as-source-compilation.md) |
| "I need retrieval but a vector store is overkill." | [14](cards/14-index-guided-retrieval.md) |
| "The agent approves its own work." | [11](cards/11-adversarial-role-separation.md) |
| "I am afraid to give an agent access to production." | [16](cards/16-the-permission-ladder.md), [17](cards/17-blast-radius-gating.md) |
| "Agent output might contain credentials." | [18](cards/18-the-redaction-boundary.md) |
| "My agent's scope creeps mid-task." | [19](cards/19-scope-lock-and-checkpoint-delivery.md) |
| "My generated documentation is stale and nobody noticed." | [20](cards/20-repository-projection-pipeline.md) |
| "I want to build a skill and do not know where to start." | [08](cards/08-interview-before-generation.md) → [09](cards/09-scaffold-validate-package.md) → [06](cards/06-calibrated-degrees-of-freedom.md) |

## Maturity

| Maturity | Count | Meaning |
| --- | --- | --- |
| `proven` | 11 | Ran in daily use and did what the card describes |
| `partial` | 8 | Implemented in part; each card names exactly which part is missing |
| `abandoned` | 1 | Card 05 — the pattern the source system failed to hold, documented because the failure is the lesson |

Nearly half are not `proven`. That is the honest distribution of a working system,
and flattening it would make every other claim here less believable.

## Component cards

A pattern card describes an idea; a component card describes one concrete
artifact — a skill, command, rule, subagent or hook, or a reference, asset or script a skill
loads — and which patterns it puts into practice. A skill's parts sit beneath its card, as they
do in the skill itself. Each ships its own prototype under
[`skeletons/components/`](skeletons/components/). Contract:
`.claude/rules/component-cards.md`.

| # | Component | Type | Instances | The idea in one line |
| --- | --- | --- | --- | --- |
| 01 | [Infrastructure Issue Investigator](component-cards/skills/infrastructure-issue-investigator/01-infrastructure-issue-investigator.md) | skill | 02 03 06 16 17 18 19 | Investigate read-only, rank fixes against the team's repo, write a plan — never apply it |
| 02 | [Remediation Ranking Rubric](component-cards/skills/infrastructure-issue-investigator/references/02-remediation-ranking-rubric.md) | reference | 06 17 19 | Seven weighted criteria turn a choice into arithmetic — exact sums over unaudited judgement |
| 03 | [Investigation Safety Rules](component-cards/skills/infrastructure-issue-investigator/references/03-investigation-safety-rules.md) | reference | 16 17 18 19 | Six rule sets keep an investigation read-only; three denied verbs are the only ones enforced |
| 04 | [Symptom-Class Diagnostic Playbook](component-cards/skills/infrastructure-issue-investigator/references/04-symptom-diagnostic-playbook.md) | reference | 02 06 16 18 | Exact read-only commands per symptom class — and every flaw in them repeated on every run |
| 05 | [Keyword-Narrowed Repository Search](component-cards/skills/infrastructure-issue-investigator/references/05-keyword-narrowed-repo-search.md) | reference | 02 05 14 18 | A keyword-to-path map narrows the search — until a role is renamed and it quietly finds nothing |
| 06 | [Remediation Plan Template](component-cards/skills/infrastructure-issue-investigator/assets/06-remediation-plan-template.md) | asset | 06 17 18 19 | A fixed shape makes a plan complete on paper — and nothing checks the paper |
| 07 | [Secret-Shape Output Scrubber](component-cards/skills/infrastructure-issue-investigator/scripts/07-secret-shape-output-scrubber.md) | script | 02 06 18 | Ordered patterns between raw output and the plan — they erase the evidence and miss the JSON copy |
| 08 | [Workstream Hardening Orchestrator](component-cards/skills/workstream-hardening-orchestrator/08-workstream-hardening-orchestrator.md) | skill | 02 03 05 06 07 16 17 19 | Five hardening workstreams behind tier gates, triggers and checkpoints — every gate held by instruction, none by the harness |
| 09 | [Checkpoint Status Report Template](component-cards/skills/workstream-hardening-orchestrator/assets/09-checkpoint-status-report.md) | asset | 06 19 | One delivery shape per checkpoint — with a state vocabulary narrower than the state file it reports |
| 10 | [Sprint State File Template](component-cards/skills/workstream-hardening-orchestrator/assets/10-sprint-state-file.md) | asset | 05 19 | Scope, statuses, triggers and checkpoints in one file — copied three times, and the copies disagree |
| 11 | [Benchmark Triage Table Template](component-cards/skills/workstream-hardening-orchestrator/assets/11-benchmark-triage-table.md) | asset | 06 17 19 | A disposition per benchmark failure, with decision rules nothing checks and a gap where etcd should be |
| 12 | [Workstream Tracking Brief](component-cards/skills/workstream-hardening-orchestrator/assets/12-workstream-tracking-brief.md) | asset | 17 19 | A per-workstream brief the skill lists and no phase ever fills |
| 13 | [Component Tier Table](component-cards/skills/workstream-hardening-orchestrator/references/13-component-tier-table.md) | reference | 16 17 | Blast-radius tiers by hand, kept twice — in prose and in the lookup script, and they disagree |
| 14 | [Conditional Sprint Triggers](component-cards/skills/workstream-hardening-orchestrator/references/14-conditional-sprint-triggers.md) | reference | 17 19 | Three if/then gates with documented state machines — that no code reads before a workstream starts |
| 15 | [Dry-Run-First Invocation Contract](component-cards/skills/workstream-hardening-orchestrator/references/15-dry-run-invocation-contract.md) | reference | 06 16 17 | Dry-run and apply as one command pair — written for one operator's machine, and nothing records the dry-run |
| 16 | [Recovery Runbook Set](component-cards/skills/workstream-hardening-orchestrator/references/16-recovery-runbook-set.md) | reference | 06 16 17 | Copy-ready recovery commands — destructive verbs guarded only by "never auto-execute" |
| 17 | [Owned-Scope Policy Remediation Guide](component-cards/skills/workstream-hardening-orchestrator/references/17-owned-scope-policy-remediation.md) | reference | 06 17 19 | Fix policy violations in owned roles only — measured per file, so one compliant file clears a role |
| 18 | [Installation Glossary](component-cards/skills/workstream-hardening-orchestrator/references/18-installation-glossary.md) | reference | 02 05 | Canonical terms the model must repeat verbatim — and installation facts that go stale with them |
| 19 | [Workstream Gate Catalogue](component-cards/skills/workstream-hardening-orchestrator/references/19-workstream-gate-catalogue.md) | reference | 06 17 19 | Pass criteria per workstream — that the gate runner implements differently, gate by gate |
| 20 | [Secrets-Store TLS and Auto-Unseal Guide](component-cards/skills/workstream-hardening-orchestrator/references/20-secrets-store-tls-unseal-guide.md) | reference | 06 17 19 | Four coordinated TLS edits behind a flag — and a rollback elsewhere that restores one of them |
| 21 | [Tier Lookup Gate](component-cards/skills/workstream-hardening-orchestrator/scripts/21-tier-lookup-gate.md) | script | 16 17 | Exit codes that say whether to confirm — and a typo exits 0, like a component safe to change |
| 22 | [Triage Table Renderer](component-cards/skills/workstream-hardening-orchestrator/scripts/22-triage-table-renderer.md) | script | 06 19 | Findings into a disposition table — where a regex verdict reads like a human decision |
| 23 | [Hardening Field Scanner](component-cards/skills/workstream-hardening-orchestrator/scripts/23-hardening-field-scanner.md) | script | 06 17 19 | Finds missing security-context fields by word — so a field set to the insecure value counts as present |
| 24 | [Benchmark Report Parser](component-cards/skills/workstream-hardening-orchestrator/scripts/24-benchmark-report-parser.md) | script | 06 17 | Classifies benchmark findings by control prefix — and etcd failures need no approval |
| 25 | [Static Rollback Planner](component-cards/skills/workstream-hardening-orchestrator/scripts/25-static-rollback-planner.md) | script | 16 17 19 | Fixed rollback steps per workstream — whatever actually changed, and restoring one file of four |
| 26 | [Repository Scope Detector](component-cards/skills/workstream-hardening-orchestrator/scripts/26-repo-scope-detector.md) | script | 19 20 | Pre-fills the sprint from the repository's shape — and marks every role as owned |
| 27 | [Sprint State Reporter](component-cards/skills/workstream-hardening-orchestrator/scripts/27-sprint-state-reporter.md) | script | 19 | Renders sprint state per checkpoint — the checkpoint argument changes nothing, and nothing is evaluated |
| 28 | [Workstream Gate Runner](component-cards/skills/workstream-hardening-orchestrator/scripts/28-workstream-gate-runner.md) | script | 16 17 19 | Runs a workstream's gates — and last sprint's output passes this sprint's gate |
| 29 | [Seal-State Health Checker](component-cards/skills/workstream-hardening-orchestrator/scripts/29-seal-state-health-check.md) | script | 06 16 | Generates seal-status commands and parses their output — but not the output its own commands produce |
| 30 | [Parallel Gap-Scan Subagent](component-cards/subagents/30-parallel-gap-scan-subagent.md) | subagent | 07 16 | A small-model scanner run in parallel — its tool limits are prose, so the harness grants everything |
| 31 | [Benchmark Triage Subagent](component-cards/subagents/31-benchmark-triage-subagent.md) | subagent | 07 16 | Parses and triages in parallel — forbidden to write, granted the shell that writes |
| 32 | [Role-Separated Sprint Loop Orchestrator](component-cards/skills/role-separated-sprint-loop-orchestrator/32-role-separated-sprint-loop-orchestrator.md) | skill | 02 03 06 07 11 19 | Six phases split building from grading behind a frozen contract — its documented commands fail, and its gate never reads the verdict |
| 33 | [Blocking-Items Return Template](component-cards/skills/role-separated-sprint-loop-orchestrator/assets/33-blocking-items-return-template.md) | asset | 11 19 | Returns only the blockers to the builder — with the scores and thresholds the builder is told not to look at |
| 34 | [Axis-Scored Evaluation Template](component-cards/skills/role-separated-sprint-loop-orchestrator/assets/34-axis-scored-evaluation-template.md) | asset | 06 11 | A fixed shape for an axis-by-axis grade — whose axis names do not match the contract's, so a faithful grade fails validation |
| 35 | [Run Outcome Report Template](component-cards/skills/role-separated-sprint-loop-orchestrator/assets/35-run-outcome-report-template.md) | asset | 11 19 | One summary shape for a whole run — with a status vocabulary of its own, and metrics nothing records |
| 36 | [Sprint Contract Template](component-cards/skills/role-separated-sprint-loop-orchestrator/assets/36-sprint-contract-template.md) | asset | 11 19 | The bar fixed before the work — in a shape the contract writer never emits |
| 37 | [Evaluator Failure-Pattern Catalog](component-cards/skills/role-separated-sprint-loop-orchestrator/references/37-evaluator-failure-pattern-catalog.md) | reference | 02 11 | Ten named evaluator failures, read before every grade — and a self-check the grader runs on itself, by hand |
| 38 | [Evaluator Role Reference](component-cards/skills/role-separated-sprint-loop-orchestrator/references/38-evaluator-role-reference.md) | reference | 02 11 | Flaw-first, conservative, absence-is-failure — with three formats for one blocking-issue shape |
| 39 | [Generator Role Reference](component-cards/skills/role-separated-sprint-loop-orchestrator/references/39-generator-role-reference.md) | reference | 11 | No self-scoring, no defence, no disclaimers — and a required known-gaps section that is a disclaimer |
| 40 | [Planner Role Reference](component-cards/skills/role-separated-sprint-loop-orchestrator/references/40-planner-role-reference.md) | reference | 11 19 | Capped sprints with testable targets — forbidden to estimate, and required to estimate complexity |
| 41 | [Axis Scoring Guide](component-cards/skills/role-separated-sprint-loop-orchestrator/references/41-axis-scoring-guide.md) | reference | 06 11 | A scale, thresholds and calibration anchors — with a gap between the bands, and a not-applicable axis scored as a 5 |
| 42 | [Role Spawn Prompt Set](component-cards/skills/role-separated-sprint-loop-orchestrator/references/42-role-spawn-prompt-set.md) | reference | 07 11 | Copy-ready prompts for each role — that skip the catalog and run on a general agent with every tool |
| 43 | [Worked Loop Walkthroughs](component-cards/skills/role-separated-sprint-loop-orchestrator/references/43-worked-loop-walkthroughs.md) | reference | 06 11 | Two exact-call walkthroughs — in a command form the skill does not use, with output the code cannot print |
| 44 | [Loop Gate and History Harness](component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/44-loop-gate-and-history-harness.md) | script | 11 19 | Gate and history over one state file — it passes any sprint with no per-axis record, and force-init erases the history |
| 45 | [Loop State Recorder](component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/45-loop-state-recorder.md) | script | 11 19 | Phase, sprint and iteration records — any phase from any phase, and a later pass reopens an escalated sprint |
| 46 | [Evaluation Structure Validator](component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/46-evaluation-structure-validator.md) | script | 06 11 | Checks every axis is scored and consistent with its threshold — shape, never substance, and a hyphenated axis vanishes |
| 47 | [Sprint Contract Writer](component-cards/skills/role-separated-sprint-loop-orchestrator/scripts/47-sprint-contract-writer.md) | script | 06 11 19 | Writes the frozen contract — and overwrites it, thresholds and all, without a trace |
| 48 | [Planning Subagent Definition](component-cards/subagents/48-planning-subagent-definition.md) | subagent | 07 11 16 | A read-and-shell planner told to write a spec — and forbidden the estimate its own template requires |
| 49 | [Implementation Subagent Definition](component-cards/subagents/49-implementation-subagent-definition.md) | subagent | 07 11 16 | The only role granted write tools — told to hand off silently, and to list its known gaps |
| 50 | [Evaluation Subagent Definition](component-cards/subagents/50-evaluation-subagent-definition.md) | subagent | 07 11 16 | A grader forbidden to modify files — granted the shell that can, and spawned on an agent with every tool |

## Compound pipelines

Cards 12 → 13 → 14 → 15 are one engine, not four independent patterns. The
sequential walkthrough is at
[`skeletons/pipelines/session-memory-loop/`](skeletons/pipelines/session-memory-loop/);
each card's own modular skeleton stays in its own directory.

## Diagrams

Every Excalidraw source, with its render where one exists, is in
[`diagrams/`](diagrams/README.md) — one index, in subfolders that mirror the cards.
