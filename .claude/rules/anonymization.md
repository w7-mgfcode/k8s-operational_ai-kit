---
paths:
  - "ai-engineering-knowledge-cards/**"
  - ".gitignore"
---

# The Anonymization Boundary

This repository publishes patterns extracted from a private agent kit that
operated a real Kubernetes platform. The source material is on disk, gitignored,
and un-anonymized. `ai-engineering-knowledge-cards/docs/ANONYMIZATION.md` is the
binding policy and the audit record; this rule is how it is enforced at edit time.

## The rule

Public technology names stay. Anything that points at a *specific installation*
of them goes. A card must teach the pattern well enough to implement, and
identify nothing.

**Keep:** Kubernetes, Ansible, Helm, Vault, Prometheus, Grafana, Loki, Mimir,
Tempo, Kyverno, Cilium, Longhorn. Keep orders of magnitude where the magnitude
carries engineering meaning ("roughly two dozen workloads", "about three weeks of
daily use").

**Remove:** organization names, operator usernames, absolute paths from the
source system, internal domains, node hostnames and any description of their
naming scheme, internal IPs and CIDRs, the source repository name, project
codenames, internal abbreviations, named personal tooling, the operator's
timezone.

## `.legacy-assets/` is never a source

It holds the un-anonymized kit: the organization name, two environment domains,
11 node hostnames, three internal subnets, 16 raw session transcripts (one with
credential-shaped lines), runtime flush state, and 64 compiled articles about a
specific installation.

- **Never read it into a card, a skeleton, a commit message, or a report.**
- Never quote it, summarize it, or paraphrase it. Describing the *mechanism* that
  processed those logs is card 13's job and is already done.
- You may state that it exists and that it is excluded. That is the whole of what
  may be said about its contents.

**One exception: component-card extraction.** A component card describes one
artifact from the source kit, so writing one means reading that artifact. It is
permitted only when all of these hold:

1. The user names **one directory** in `.legacy-assets/` for this card. Nothing
   outside it is listed, searched or opened. Do not `cd` into the tree: the
   harness auto-loads rule files from the directories it walks.
2. Before any file is written, the agent reports a masking table (every
   identifier found, with its generic replacement) and the proposed generic
   name, and the user approves it. Originals appear in that chat report only.
3. The output obeys [`component-cards.md`](component-cards.md): the source's own
   name and its worked examples are not reused, and failure modes stay observed
   or structurally inevitable.
4. Before committing, the new files are searched for every original identifier
   from the approved table.

Without a named directory and an approved table, the rule above applies
unchanged.

## What must never enter the repository

- `.legacy-assets/` — gitignored. That one line is currently the only control.
- Any vendored virtual environment. The same 136 MB / 641-file venv currently
  exists **twice** — under `.claude/skills/excalidraw-diagram/references/.venv`
  and under `.agents/skills/excalidraw-diagram/`. Both `.claude/` and `.agents/`
  are untracked but not ignored, so `git add .` would commit ~272 MB of
  third-party packages. Add `**/.venv/`, `__pycache__/` and `*.pyc` to
  `.gitignore` before the first commit.
- Any `.env`, token, or credential. This repository is intended to be public.

## Before publishing

Grep the staged diff for the masked classes above. The log at
`ai-engineering-knowledge-cards/docs/ANONYMIZATION.md` records
occurrence counts per class (152 organization-name hits, ~85 domains, ~40
hostnames); if a card reintroduces one, the count is no longer true and the audit
record is no longer honest.

Related: [`cards.md`](cards.md), [`skeletons.md`](skeletons.md),
[`git-workflow.md`](git-workflow.md).
