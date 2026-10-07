---
component: 24
title: Benchmark Report Parser
type: script
instances:
  - 06-calibrated-degrees-of-freedom
  - 17-blast-radius-gating
related:
  - 08-workstream-hardening-orchestrator
  - 11-benchmark-triage-table
  - 22-triage-table-renderer
  - 31-benchmark-triage-subagent
---

# Benchmark Report Parser

> Turns a CIS benchmark report into findings with a class and an approval flag, and
> files the etcd section under "other", where nothing needs approval.

## What it is

A standard-library Python script, the first step of workstream D, CIS benchmark
triage. It reads a Markdown kube-bench report and turns each result line into a
finding with control ID, status, description and section. It classes each finding by
control-ID prefix as control plane, worker node, policy or other, and guesses from
the description whether the finding is likely not applicable. A control-plane FAIL is
marked as requiring platform-team approval, the check behind the sprint's third
trigger. Its JSON feeds the triage table renderer
([component 22](22-triage-table-renderer.md)), which fills the triage table
([component 11](../assets/11-benchmark-triage-table.md)).

## Trigger and routing

It is executed, not routed. In the quick-wins phase the orchestrator
([component 08](../08-workstream-hardening-orchestrator.md)) runs it on the newest
benchmark report found at scope lock. The benchmark triage subagent
([component 31](../../../subagents/31-benchmark-triage-subagent.md)) runs the same
command when the skill fans the workstream out in parallel.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Report path | yes | the scope-lock detection, or the user |
| Output format | no | JSON by default; YAML on request |
| Output path | no | stdout when absent |
| FAIL-only flag | no | drops the other findings and keeps the totals |

## Procedure

1. If the report does not exist, print an error object and exit 1.
2. Read the report line by line. A heading line sets the current section.
3. Match each line against a pattern with optional brackets around the status, then a
   dotted control ID, then the description. On a match, count the status, class the
   control and test applicability. A FAIL also gets the approval flag.
4. Otherwise, match a second pattern: the same shape without brackets. It never
   matches anything the first pattern missed.
5. Class by prefix: the control-plane sub-areas of section 1 and all of section 3 are
   control plane, section 4 is worker node, section 5 is policy, everything else is
   other.
6. Mark a finding *likely not applicable* if its description matches one of three
   regular expressions. They target the deprecated pod security policy and one kubelet
   feature gate.
7. Total PASS, FAIL, WARN and INFO, the control-plane FAILs and the actionable FAILs
   (FAILs not marked likely-NA). Print JSON, or YAML through a third-party library.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read the report | yes | the script |
| Write one output file | only when an output path is given | the script |
| Network, subprocesses, cluster | no | the script — it contains no such call |
| Deciding a finding's disposition | no, it only classes and flags | the triage table and the human who fills it |

## Outputs

One JSON object (or YAML) with the totals and a list of findings. The script exits 0
when it parsed, and 1 only when the report is missing; a report with no recognisable
lines parses to zero findings and still exits 0.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| etcd failures need no approval | FAILs from the etcd section are classed `other` with no approval flag, and the triage table offers them for implementation without the platform team | Section 2 of the benchmark is on no prefix list; only sections 1 and 3 count as control plane. Observed |
| A second parser that never runs | Two copies of the result-line logic, and an edit to the second changes nothing | The first pattern's brackets are optional, so it already matches every unbracketed line the second was written for. Observed |
| Not applicable by keyword | A control is pre-marked not applicable because its description names a pattern word, including the admission plugin that *replaced* the deprecated policy | Applicability is three regular expressions over free text. The one aimed at the deprecated policy in the admission-plugins argument also matches its successor's name. Observed |
| YAML output has no fallback | `--format yaml` stops with an import error on a machine without the library | The entry file says every script falls back to JSON without it; this one imports the library at the point of use and has no fallback. Observed |
| A guess becomes a count | *Actionable FAILs* excludes everything pre-marked likely-NA, so the headline number shrinks before anyone has triaged | The heuristic flag feeds the summary directly. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | Parsing a fixed report format is code, and disposition is left to a human. The applicability regexes move part of that human judgement into code at the lowest freedom, where nobody reviews it |
| [17 Blast-Radius Gating](../../../../cards/17-blast-radius-gating.md) | Approval scales with what a finding touches: control-plane changes go to the platform team. The scale is a prefix list, and a missing prefix lowers the bar without a trace |

## Provenance

The source system held this as one standard-library Python script of about 160
lines in the skill's scripts directory. It holds two module-level tables (the
control-plane prefixes and three applicability patterns), a classifier, the two
parsing branches and a command-line entry point. Its usage text names a report
file from a single day. Nothing records how many reports it parsed or what was done
with its findings, and this card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/24-benchmark-report-parser/`](../../../../skeletons/components/24-benchmark-report-parser/).
Standard library, offline. It parses a fabricated benchmark report with the same
two-branch, prefix-class design. With `--audit` it shows the etcd FAILs without
approval, the second branch's zero hits and a live control pre-marked not applicable.

## What is deliberately missing

**Classing by section.** The parser already reads each section heading and stores
it on every finding. Classing by that heading instead of a hand-kept prefix list
would put etcd where it belongs.

**Applicability by control ID.** Which controls do not apply to a platform is a short
list a person maintains by ID. A regex over descriptions turns that judgement into a
side effect of wording.

**One parsing branch.** Deleting the dead branch changes no output.

**In the prototype:** no YAML output (the library is not standard), no FAIL-only
flag and no output file.
