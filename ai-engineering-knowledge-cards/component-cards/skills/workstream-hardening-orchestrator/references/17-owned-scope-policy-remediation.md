---
component: 17
title: Owned-Scope Policy Remediation Guide
type: reference
instances:
  - 06-calibrated-degrees-of-freedom
  - 17-blast-radius-gating
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 08-workstream-hardening-orchestrator
  - 23-hardening-field-scanner
  - 30-parallel-gap-scan-subagent
---

# Owned-Scope Policy Remediation Guide

> How to fix admission-policy violations one owned role at a time — with an inventory that
> checks whether a word appears in a file, not whether a container is hardened.

## What it is

A reference file for the hardening orchestrator's admission-policy workstream
([component 08](../08-workstream-hardening-orchestrator.md), workstream C). The cluster's
policy engine runs in audit mode, so violations are reported and not blocked; this guide says
how to reduce them without touching anything the team does not own. It draws the scope line
(roles in this repository, not third-party chart internals), lists four common
container-hardening gaps with the values that fix them, gives a five-step workflow — inventory,
filter to owned roles, prioritise, fix role by role, validate — and names the roles that need
documented exceptions instead of fixes.

## Trigger and routing

Linked from the first step of workstream C, in both its quick-win half (build the inventory,
apply the first fixes) and its medium-effort half (role-by-role remediation). Two other
components implement parts of it: the field scanner script
([component 23](../scripts/23-hardening-field-scanner.md)) runs the inventory, and the
gap-scan subagent ([component 30](../../../subagents/30-parallel-gap-scan-subagent.md)) does
the same scan in parallel when the skill fans out.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The role tree | yes | the infrastructure repository's roles directory |
| The owned-role list | yes | scope lock; the guide says to ask the user when a role's ownership is unclear |
| Policy reports | cluster-aware mode only | commands the skill generates for the operator |
| The exception list | yes | a table in this guide |

## Procedure

1. **Inventory.** Offline: list the role files that do not mention each hardening field.
   Cluster-aware: generate the policy-report commands for the operator.
2. **Filter to owned roles.** Drop third-party chart pods, system namespaces and workloads an
   external team manages.
3. **Prioritise** by a fixed table: non-root first, then privilege escalation, then dropped
   capabilities, then a read-only root filesystem — the last flagged as needing careful testing.
4. **Fix role by role.** Prefer the chart's values; fall back to a template override. After
   each role: lint, syntax check, and a dry-run of that role's tag.
   *Gate: all three pass before the next role.*
5. **Validate.** Offline, the inventory count drops; in cluster-aware mode, the policy reports
   for owned namespaces show fewer violations and no new ones elsewhere.

Exceptions — a reboot daemon, a node-level log collector, the benchmark scanner, the
secrets-store injector, a distroless metrics component — are documented rather than forced.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Reading and searching the role tree | yes | the skill's instructions |
| Editing owned roles' values and templates | yes, role by role | the skill's instructions; each change goes through the dry-run contract |
| Editing third-party chart internals | no | the skill's instructions only |
| Policy-report queries | generated for the operator | the skill's instructions |
| Changing the policy engine from audit to enforce | not in scope | not mentioned; nothing prevents a role fix from being followed by one |

## Outputs

A violation inventory, per-role fixes as changes to the repository, and violation counts
before and after that the checkpoint report records. In the source, the counts were fields in
the sprint state file; the guide does not say where the inventory itself is kept.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Presence, not posture | A role whose template sets the field on one container and omits it on another passes; so does a role that sets the field to the unsafe value | The offline inventory asks which files lack a word. One mention anywhere in the file counts for every container in it, and the word says nothing about its value. Structural |
| Three exception lists | A role is an exception in the guide and a violation in the scanner, or skipped by the subagent and flagged by the guide | This guide names five exceptions; the scanner script hard-codes four, one of them absent here; the subagent skips three and flags a fourth for special handling. Nothing reconciles them. Observed |
| "Ask the user" never fires | Vendored roles enter the inventory as owned | The guide's boundary is a question for the user, but the scope detector ([component 26](../scripts/26-repo-scope-detector.md)) fills the owned-role list with every role it finds, so there is nothing left to ask. Observed |
| The inventory checks the guide's fields, not the cluster's policies | Violations of a deployed policy the guide does not list are invisible offline | The guide states that the policies actually deployed are not defined in the repository. The offline method can only check the four fields it knows. Observed |
| Priority by assumption | Fixes start with the field the guide calls most common, whatever the inventory found | The priority table carries frequency labels written in advance, not counts from the inventory. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | The fixes are exact values; the choice between a values override and a template override is left to judgement |
| [17 Blast-Radius Gating](../../../../cards/17-blast-radius-gating.md) | One role per change, each followed by lint, syntax and its own dry-run, so a regression is traceable to one role |
| [19 Scope Lock and Checkpoint Delivery](../../../../cards/19-scope-lock-and-checkpoint-delivery.md) | The owned-role boundary is the scope lock for this workstream; before-and-after counts are its checkpoint evidence |

## Provenance

Instanced in the source system by one reference file of about 150 lines in the skill's
references directory: a current-state summary, scope rules, four violation types with fix
snippets, a five-step workflow with offline and cluster-aware variants, a note on a shared
library role through which namespace-level changes must go, and an exception table. It does
not record how many violations were found or fixed, and this card claims neither.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/17-owned-scope-policy-remediation/`](../../../../skeletons/components/17-owned-scope-policy-remediation/).
Standard library, offline. It runs the file-level inventory and a per-container inventory side
by side over a fabricated role tree, compares three exception lists, and shows a vendored role
entering scope when every role is treated as owned.

## What is deliberately missing

**A per-container check.** Splitting each manifest into containers and reading each field's
value removes both halves of the first failure; the prototype does it in about twenty lines.

**One exception list.** Kept once, with a reason per role, and read by the guide, the scanner
and the subagent alike.

**An ownership source.** A file that marks vendored roles, so "owned" is data the detector
reads instead of a question it skips.

**In the prototype:** manifests are reduced to a line-based shape, no chart values are
rendered, and the policy reports are absent.
