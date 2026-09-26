---
component: 03
title: Investigation Safety Rules
type: reference
instances:
  - 16-the-permission-ladder
  - 17-blast-radius-gating
  - 18-the-redaction-boundary
  - 19-scope-lock-and-checkpoint-delivery
related:
  - 01-infrastructure-issue-investigator
  - 04-symptom-diagnostic-playbook
  - 05-keyword-narrowed-repo-search
  - 06-remediation-plan-template
---

# Investigation Safety Rules

> Six rule sets that keep a cluster investigation read-only, quiet and reviewable —
> all of them written as instructions, three verbs of them enforced.

## What it is

A reference file loaded by the investigator skill
([component 01](../skill/01-infrastructure-issue-investigator.md)) and applied in
every phase that touches the cluster, the repository or the web. It holds six rule
sets: a production guard, secret scrubbing, restricted paths, web-query hygiene, a
tool deny list, and a list of confirmation points. About 125 lines, no code — the
scrubbing it describes is implemented by a script beside it.

## Trigger and routing

Loaded by the investigator skill in its intake, diagnose and research phases — the
skill's reference table names it for all three — and cited again by the hard rules at
the end of the skill's entry file. It opens with one instruction that frames the
rest: when in doubt, stop and ask.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| The resolved kubeconfig path and context name | yes | the intake phase |
| Command output | yes | the diagnose phase, before it is carried forward |
| Repository search results | yes | the research phase |
| Draft web queries | yes | the research phase |
| The next action needing consent | yes | whichever phase is about to act |

## Procedure

1. **Prod guard.** Classify the target from the kubeconfig path and context name:
   a development marker means development; an intermediate-environment marker means
   guarded; a production marker, *or no marker at all*, means production. The context
   name wins when path and name disagree. Anything but development prints a loud
   warning, requires a typed confirmation, and stays read-only after it; the plan
   records that the guard was confirmed.
2. **Secret scrubbing.** Every output that will be carried between phases or written
   into the plan goes through the redaction script first. Patterns cover password,
   token, bearer, API-key, secret and credential assignments, secret data blocks,
   whole kubeconfig documents, and long base64 strings after known secret keys.
   Redacted text goes to stdout, one `REDACTED:` line per hit to stderr, and every plan
   carries a review block listing what was removed.
3. **Restricted paths.** Never open Ansible Vault files, secrets directories, env
   files, `.git/`, or `~/.kube/` beyond the one resolved kubeconfig — even when a search
   matches them. Record the path, do not open it, and advise a manual check.
4. **Web-query hygiene.** Never put cluster or namespace names in a query. Strip every
   proper noun that identifies the installation; keep versions, verbatim error
   messages, component names and upstream resource types.
5. **Tool deny list.** Fifteen commands the skill never runs: the kubectl write verbs
   (`delete`, `apply`, `patch`, `edit`, `replace`, `scale`, `drain`, `cordon`,
   `uncordon`), the Helm release verbs, and Ansible. A step that would need one belongs
   in the plan's steps, for a human to run.
6. **Confirmation points.** Ask separately before: any command against a non-development
   context, delegating diagnosis to a broader troubleshooting skill, choosing an
   option the user did not pick, each rework round, writing the plan, and writing it to
   the alternative location. Never batch them.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| `kubectl delete`, `helm uninstall`, `helm rollback` | no | the harness deny list, and this file |
| the other twelve denied commands | no | this file only |
| every command not on the list | not stated | nothing — see Failure modes |
| reading restricted paths | no | this file only |
| web search | yes, sanitized | this file only |

## Outputs

None of its own. It shapes other outputs: redacted command text, a guard line and a
redaction-review block in the plan, advisory notes for unopened files, and six
separate questions to the user.

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Writes that are not on the list | A diagnostic runs `kubectl run`, `exec`, `label`, `annotate`, `create`, `set` or `rollout restart` in a "read-only" investigation | Read-only is expressed as fifteen forbidden commands. Anything unnamed is allowed by default. Observed: the skill's own certificate diagnostics use `kubectl run` ([component 01](../skill/01-infrastructure-issue-investigator.md)) |
| The guard trusts a name | A context repointed at production but still carrying a development name is treated as development | Classification is by substring of names; the cluster itself is never asked what it is. Structurally inevitable |
| Hygiene without a list | Lowercase workload and namespace names survive; capitalized error strings and component names are stripped | "Strip every proper noun that identifies your infra" gives the model no list of those names and no filter to apply. Readable off the rule |
| Search leaks what the path rule protects | The matched line from a restricted file is already in the model's context | The rule forbids opening the file after a search matched it; the match is the leak. Observed in [card 18](../../cards/18-the-redaction-boundary.md) as well |
| Rules and script disagree | A non-secret checksum is redacted by the script; a base64 credential under an unrecognized key is left alone by the rules | The rule limits base64 redaction to known secret keys; the script beside it redacts any long base64 run. Observed by comparing the two files |
| Only three verbs are controls | Every other rule holds exactly as long as the model follows instructions | Twelve of fifteen denied commands, and all of the other five rule sets, have no enforcement outside the model ([card 16](../../cards/16-the-permission-ladder.md)) |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [16 The Permission Ladder](../../cards/16-the-permission-ladder.md) | A deny list where three rungs are enforced by the harness and twelve are advice — the ladder's central distinction, inside one file |
| [17 Blast-Radius Gating](../../cards/17-blast-radius-gating.md) | The prod guard escalates by environment class, and an unqualified name falls to the strictest class |
| [18 The Redaction Boundary](../../cards/18-the-redaction-boundary.md) | Scrub before anything is carried forward, dual-channel output, a mandatory review block, and a restricted-path list |
| [19 Scope Lock and Checkpoint Delivery](../../cards/19-scope-lock-and-checkpoint-delivery.md) | Six named confirmation points, each its own question, never batched |

## Provenance

Instanced in the source system by one reference file of about 125 lines inside the
investigator skill, beside a 150-line standard-library redaction script that
implements its scrubbing section. Three of its fifteen denied commands were also on
the harness deny list; the file marks which. Nothing in it records whether any rule
was ever tripped in use, and this card claims no such history.

## Prototype

Minimal runnable prototype in
[`../../skeletons/components/03-investigation-safety-rules/`](../../skeletons/components/03-investigation-safety-rules/).
Standard library, offline. Five of the six rule sets as functions, run on the cases
they were written for, and with `--audit` on one probe per gap.

## What is deliberately missing

**Enforcement.** The mechanical versions are short: an allow list of read verbs
checked before any command runs, a list of installation names applied to every
outbound query, a restricted-path filter applied to search results before the model
sees them, and asking the cluster for its identity instead of reading its name. The
source had none of them.

**One source of truth for scrubbing.** The rule text and the script describe
different behaviour. One should be generated from, or tested against, the other.

**In the prototype:** no harness, so every rule is as advisory as in the source; the
confirmation points are described, not run.
