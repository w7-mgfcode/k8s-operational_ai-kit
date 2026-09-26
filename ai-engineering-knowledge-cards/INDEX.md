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
artifact — a skill, command, rule, subagent, hook or reference file — and which patterns it puts
into practice. Each ships its own prototype under
[`skeletons/components/`](skeletons/components/). Contract:
`.claude/rules/component-cards.md`.

| # | Component | Type | Instances | The idea in one line |
| --- | --- | --- | --- | --- |
| 01 | [Infrastructure Issue Investigator](component-cards/skill/01-infrastructure-issue-investigator.md) | skill | 02 03 06 16 17 18 19 | Investigate read-only, rank fixes against the team's repo, write a plan — never apply it |
| 02 | [Remediation Ranking Rubric](component-cards/reference/02-remediation-ranking-rubric.md) | reference | 06 17 19 | Seven weighted criteria turn a choice into arithmetic — exact sums over unaudited judgement |
| 03 | [Investigation Safety Rules](component-cards/reference/03-investigation-safety-rules.md) | reference | 16 17 18 19 | Six rule sets keep an investigation read-only; three denied verbs are the only ones enforced |
| 04 | [Symptom-Class Diagnostic Playbook](component-cards/reference/04-symptom-diagnostic-playbook.md) | reference | 02 06 16 18 | Exact read-only commands per symptom class — and every flaw in them repeated on every run |

## Compound pipelines

Cards 12 → 13 → 14 → 15 are one engine, not four independent patterns. The
sequential walkthrough is at
[`skeletons/pipelines/session-memory-loop/`](skeletons/pipelines/session-memory-loop/);
each card's own modular skeleton stays in its own directory.
