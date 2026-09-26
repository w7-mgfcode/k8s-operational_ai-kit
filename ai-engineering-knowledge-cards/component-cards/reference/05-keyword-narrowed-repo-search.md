---
component: 05
title: Keyword-Narrowed Repository Search
type: reference
instances:
  - 02-progressive-disclosure
  - 05-instruction-provenance-and-drift
  - 14-index-guided-retrieval
  - 18-the-redaction-boundary
related:
  - 01-infrastructure-issue-investigator
  - 03-investigation-safety-rules
---

# Keyword-Narrowed Repository Search

> A hand-written map from symptom keywords to the repository paths most likely to hold
> the fix — cheap, predictable retrieval that goes quietly wrong the day a role is
> renamed.

## What it is

A reference file loaded by the investigator skill
([component 01](../skill/01-infrastructure-issue-investigator.md)) in its repository
research phase. It tells the model where in the team's infrastructure-as-code
(Ansible) repository to look for existing automation and prior fixes: a default
search scope, a table of fourteen symptom keywords mapped to narrower path patterns,
the git history probes to run on what it finds, the signals to extract, the paths
never to open, and when to hand a wide scan to a read-only exploration subagent.

## Trigger and routing

Loaded only in the repo half of the research phase, which runs in parallel with web
research. Inside the file, routing is by keyword: if the symptom contains one of the
table's keywords, the search narrows to that row's paths; if it contains none, it
searches the default scope. Every search is rooted at the repository's path and must
exclude the restricted list.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Symptom text | yes | intake |
| Repository root | yes | an absolute path written into the file |
| Current branch and history | yes | `git` against that root |

## Procedure

1. **Scope.** Search role tasks, defaults and templates, then playbooks, then
   inventory group and host variables — in that order, skipping vendored collections
   and caches.
2. **Narrow.** If the symptom contains a keyword from the table — a component name,
   a resource type, a class of failure — restrict the search to that row's paths
   first. With no keyword, use the default scope across the repository.
3. **Probe history.** For the one to three candidate role directories found, read
   recent commits touching them, what the last commit changed, the current branch,
   commits ahead of the main branch, and commit subjects mentioning the keyword.
4. **Extract signals.** Existing role and its purpose, prior fix (hash and subject),
   current branch, up to five open TODO markers, and the Ansible tags in the narrowed
   task files.
5. **Exclude.** Never open vault files, secrets directories, env files or `.git/`; if a
   match falls in one, record only the filename and line number.
6. **Delegate** to a read-only exploration subagent when more than five candidate role
   directories match, when a vague symptom returns more than a hundred matches, or
   when the user asks for deep repository context. It returns a digest; the main
   conversation stays small.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Glob, grep, read inside the repository | yes, minus the restricted list | this file and [component 03](03-investigation-safety-rules.md) — instructions only |
| `git log`, `git show --stat`, `git branch --show-current` | yes | this file |
| Anything that writes to the repository | not mentioned | nothing here; the skill as a whole plans and does not write |
| An exploration subagent | yes, above the thresholds | this file |

## Outputs

A research digest for the ranking phase: candidate roles, prior fixes, the current
branch, a handful of TODOs and tags, and a list of restricted paths that matched but
were not opened. These feed the rubric's reuse and workstream criteria
([component 02](02-remediation-ranking-rubric.md)).

## Failure modes

| Failure | Symptom | Root cause |
|---|---|---|
| Machine-bound | The search runs for one operator and fails for anyone else | The repository root is an absolute home-directory path, written into the file twice. Observed |
| Stale rows search nothing | A symptom whose keyword matches returns no paths, and no fallback runs | The keyword table hard-codes role-name patterns. When a role is renamed, its row matches nothing, and the fallback rule only covers the case where *no keyword* matched. Structurally inevitable ([card 05](../../cards/05-instruction-provenance-and-drift.md)) |
| Keywords collide | A storage symptom also narrows by an unrelated keyword; a symptom naming several components narrows to all of them | Matching is by substring of the symptom; short keywords sit inside longer ones, and nothing says which row wins when several match. Structural |
| Two copies of the restricted list | The list here and the one in the safety rules can drift apart | The exclusions are restated rather than referenced; the two copies already differ by one entry, which happens not to matter for a repository search. Observed |
| "Record only the filename" arrives too late | The matched line from a restricted file is already in context | A search tool returns the matching line with the path; the instruction applies after the leak. Same failure as [component 03](03-investigation-safety-rules.md) |
| Workstream fit read from a name | A fix on a branch called `main` or named after a ticket scores zero for fitting the current work | The branch name is the only workstream signal. Structural |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [02 Progressive Disclosure](../../cards/02-progressive-disclosure.md) | Loaded only for the repository half of one phase |
| [05 Instruction Provenance and Drift](../../cards/05-instruction-provenance-and-drift.md) | Role-name patterns that describe the repository as it was when the table was written, with nothing to detect when it stops being true |
| [14 Index-Guided Retrieval](../../cards/14-index-guided-retrieval.md) | A small hand-kept map chooses where to look before any search runs — no embeddings, no vector store, and the index's quality is the retrieval's quality |
| [18 The Redaction Boundary](../../cards/18-the-redaction-boundary.md) | The restricted-path list applied to repository search, with its known gap at the search result |

## Provenance

Instanced in the source system by one reference file of about 110 lines inside the
investigator skill. Its fourteen-row keyword table was written against one
repository's role layout and names the components that installation ran; that
table is not reproduced here. Nothing in the file records when the table was last
checked against the repository.

## Prototype

Minimal runnable prototype in
[`../../skeletons/components/05-keyword-narrowed-repo-search/`](../../skeletons/components/05-keyword-narrowed-repo-search/).
Standard library, offline, against a fabricated file list and keyword table. It
narrows and searches, hits a row made stale by a role rename, and with `--drift`
audits the table: dead patterns, colliding keywords, a multi-keyword symptom, and
branch names that carry no workstream.

## What is deliberately missing

**A drift check.** Every row of the table is checkable against the repository in a
few lines: does each pattern match at least one file? The source never ran one, so a
renamed role turned into a search that silently found nothing.

**A fallback for empty narrows.** "If the narrowed search is empty, widen to the
default scope and say so" is one sentence the source did not have.

**One restricted list.** Referencing the safety rules' list instead of restating it
would remove a copy that can drift.

**In the prototype:** no real files, grep or git; the subagent hand-off is printed, not
performed.
