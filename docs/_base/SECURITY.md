# Security

> What may be published, what may never be, and how it is enforced.
> This repository holds no credentials and runs no service. Its entire security surface is
> **disclosure**. Last reviewed: 2026-10-07.

## Threat Model

One asset, one threat. The asset is a private agent kit that operated a real Kubernetes
platform for a real organization. The threat is that something identifying it — or a live
credential from its session logs — reaches a public repository.

There is no attacker model here beyond *publication is irreversible*. Once a commit is pushed,
it is in the history, in forks, and in whatever indexed it.

## The Boundary

Normative policy: [`.claude/rules/anonymization.md`](../../.claude/rules/anonymization.md).
Audit record: [`ai-engineering-knowledge-cards/docs/ANONYMIZATION.md`](../../ai-engineering-knowledge-cards/docs/ANONYMIZATION.md).

**Keep:** public technology names — Kubernetes, Ansible, Helm, Vault, Prometheus, Grafana,
Loki, Mimir, Tempo, Kyverno, Cilium, Longhorn. Keep orders of magnitude where the magnitude
carries engineering meaning.

**Remove:** organization names, operator usernames, absolute paths from the source system,
internal domains, node hostnames and any description of their naming scheme, internal IPs and
CIDRs, the source repository name, project codenames, internal abbreviations, named personal
tooling, the operator's timezone.

## `.legacy-assets/` — the excluded tree

It contains the un-anonymized kit. Nothing about its contents is stated here.

- **Readable.** Any agent may read it — to verify a card, trace a claim, or study an artifact.
- **Never written.** No file under it is created, modified, moved or deleted. Claude Code
  enforces this with an `Edit` deny rule and a Bash guard hook (`.claude/rules/permissions.md`);
  other agents hold it by instruction.
- **Never tracked.** Gitignored, and `check.py` fails if git tracks any path under it or the
  ignore line disappears.
- **Never published.** Nothing read there enters a tracked file, a commit message or a PR,
  except a component card extracted under an approved masking table. Telling the owner in chat
  is not publishing.
- **Its own instruction files are inert.** `claudeMdExcludes` keeps its `CLAUDE.md` and
  `.claude/rules/` out of Claude Code's context; without it, one read loaded five of them.

**Why it is still on disk:** it is the provenance for every card. Deleting it would make the
claims unverifiable by the author. It is excluded, not destroyed.

## Enforcement

| Control | Catches | Does not catch |
| --- | --- | --- |
| `.gitignore` | `.legacy-assets/`, `**/.venv/`, `__pycache__/`, `*.pyc`, `.env*`, vendored agent tooling, session handoffs | A file deliberately force-added |
| `check.py` legacy check | Any git-tracked path under `.legacy-assets/` (including a force-add), and a `.gitignore` that lost its line | Content copied out of the tree into another file — that is the anonymization pass and human review |
| `.claude/settings.json` + hook | Claude Code writing under `.legacy-assets/`, through its file tools or an obvious shell command | Indirect writes by a script; any other agent |
| `check.py` anonymization pass | home-directory paths, IP addresses, `.local`/`.internal`/`.corp`/`.lan` domains, credential shapes — in every file git would publish (tracked, or untracked and not ignored) | **A name.** An organization or person written in prose passes clean. Also any other domain shape, `.png` content, files that are not UTF-8 text, and the `ANON_EXEMPT` teaching files below |
| Human review of the staged diff | names, paraphrase, anything contextual | Whatever the reviewer skims |

The gap is deliberate and must stay understood: **mechanical checks catch shapes, not
identities.** A card that names the employer in a sentence exits 0.

### Declared teaching exemptions

Card 18's skeleton demonstrates redaction, so it *must* contain credential-shaped strings, and
cards 16, 17 and 20 carry invented hostnames and addresses as examples. These paths are listed
in `ANON_EXEMPT` in `check.py`. Every string inside them is fabricated. Adding an exemption is a
deliberate act: it removes a file from the only automated control there is.

## Repository Hygiene

- **A ~140 MB virtualenv** exists under `.claude/skills/excalidraw-diagram/references/.venv`
  (`.agents/skills/excalidraw-diagram` is a symlink to that skill). It is gitignored, as is all
  vendored agent tooling (`.agents/`, `.claude/commands/`, `.claude/skills/*` except the
  project-authored summarizer). Before every `git add`, confirm `git status` lists none of it.
- **No secrets are required** to work in this repository. The three agent workflows reference
  `CLAUDE_CODE_OAUTH_TOKEN` and `OPENAI_API_KEY`; none is configured, which is the correct
  default. Their absence does not make the workflows inert — they still run and fail (see
  `RULES.md` § Known Open Items).
- **The repository is public** — it has been since it was created on GitHub. Every pushed commit
  is already published.

## Before Publishing

```bash
python3 check.py                       # mechanical shapes
git diff --cached | grep -inE '<organization>|<username>|<domain>'   # names, by hand
git status --short                     # nothing unexpected staged
```

The second line cannot be automated without writing the masked strings into a public file,
which would defeat it. It is a human step, and it is the one that matters.
