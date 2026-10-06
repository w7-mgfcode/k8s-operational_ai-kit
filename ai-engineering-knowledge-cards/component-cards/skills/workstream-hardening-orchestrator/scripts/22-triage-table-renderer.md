---
component: 22
title: Triage Table Renderer
type: script
instances:
  - 06-calibrated-degrees-of-freedom
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 11-benchmark-triage-table
  - 24-benchmark-report-parser
  - 31-benchmark-triage-subagent
---

# Triage Table Renderer

> A script that turns parsed benchmark findings into the table a human triages — and
> pre-fills the only decision it can make, "not applicable", from a regular expression.

## What it is

A standard-library Python script in workstream D of the hardening orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)). It reads the JSON the
benchmark report parser ([component 24](24-benchmark-report-parser.md)) writes and
renders a Markdown triage table: one row per failing CIS control with columns for
disposition, rationale, owner and sprint target, a shorter table for warnings, a
legend of the four dispositions, and the decision rules. It is the code that produces
the shape the triage table template ([component 11](../assets/11-benchmark-triage-table.md))
describes, and the file the sprint's benchmark gate looks for.

## Trigger and routing

Executed, never loaded. The skill's entry file runs it in phase 2 straight after the
parser, writing into the sprint's dated output directory; the benchmark triage subagent
([component 31](../../../subagents/31-benchmark-triage-subagent.md)) runs the same
pair when the skill fans out. The scripts table lists it with a Markdown or YAML
format option.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| `--findings <path>` | yes | the parser's JSON: summary counts and a findings list, each with control ID, status, description, classification, a likely-not-applicable flag and, for failures, an approval flag |
| `--output <path>` | yes | the sprint's output directory |
| `--format md\|yaml` | no, Markdown by default | the caller |

## Procedure

1. Load the findings; treat every top-level key but the list as the summary.
2. Write a header with the report path and the pass, fail, warn, control-plane and
   actionable counts.
3. For each failure, sorted by control ID: disposition **NA** with the rationale
   "deprecated" if the parser flagged it likely not applicable, otherwise **TBD** with a
   to-do; append "needs approval" to the classification of control-plane items; cut the
   description at eighty characters; leave owner and target as TBD.
4. For each warning: every column TBD.
5. Append the disposition legend — implement, defer, NA, TBD — and the decision rules.
6. Create the output directory if needed, write the file, and print a one-line JSON
   summary with failure, warning and TBD counts.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read the findings file | yes | the script |
| Create directories and write the output file, overwriting it | yes, without asking | the script |
| A third-party YAML library | needed for `--format yaml` | nothing — the import fails if it is absent |
| Network, subprocesses | no | the script — it contains no such call |

## Outputs

A Markdown file — or YAML with the same rows — at the output path, and a JSON summary
on stdout. The file is the deliverable checkpoint A lists as "the triage table", and
the artifact the workstream-D gate checks for.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Two of four dispositions | No row ever reads implement or defer | The renderer emits only NA or TBD; the legend lists four codes and the code can produce two. Observed |
| A heuristic reads as a decision | A row marked NA with the rationale "deprecated" looks triaged, and a control still enforced another way is dropped from the actionable count | NA comes from a pattern match on the description in the parser, and is printed with a rationale as if someone had decided it. Observed |
| Every row is "dispositioned" | A gate requiring every failure dispositioned passes with no human decision | TBD and NA both fill the column; the gate runner ([component 28](28-workstream-gate-runner.md)) only checks that the file exists. Observed, across two files |
| No YAML without a library | `--format yaml` stops with an import error on a machine without it | The YAML path imports a third-party parser unconditionally, though the skill says its scripts fall back to JSON. Observed |
| One legend, two wordings | The template and the rendered table explain NA and defer differently | The legend and rules are written here and again in the template ([component 11](../assets/11-benchmark-triage-table.md)). Observed |
| Descriptions cut mid-clause | A row's description stops before the part that says what to change | A fixed eighty-character cut, with no marker. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | Rendering is code, so every triage starts from the same table — but the one judgement it makes is delegated to a regular expression, at the lowest freedom for the most context-dependent call |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | The table is the named deliverable for checkpoint A, and the scope boundary for workstream D: what is implemented, deferred or out |

## Provenance

Instanced in the source system by one Python script of about 150 lines in the skill's
scripts directory: a Markdown renderer, a YAML renderer and an entry point. The
Markdown path is standard library; the YAML path is not. Nothing in the component
records how many tables it rendered or how many TBD rows a human later filled in; this
card claims none of that.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/22-triage-table-renderer/`](../../../../skeletons/components/22-triage-table-renderer/).
Standard library, offline. It renders fabricated findings into the same table shape, and
with `--check` counts dispositions by where they came from and runs an
"every failure dispositioned" gate over the result.

## What is deliberately missing

**A difference between "suggested" and "decided".** A pre-filled NA belongs in a
suggestion column, with the disposition column left for a human. A gate can then count
human decisions.

**All four codes.** Worker-node failures with no approval requirement are candidates for
"implement"; control-plane failures pending approval are candidates for "defer". The
rules to pre-suggest both are already in the legend.

**One legend.** Rendering the template, instead of restating it, removes one copy.

**In the prototype:** Markdown only — a YAML path would need the library the card says
is missing — and no output file; the table goes to stdout.
