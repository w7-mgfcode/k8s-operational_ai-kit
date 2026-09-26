# Security

> What may be published, what may never be, and how it is enforced.
> This repository holds no credentials and runs no service. Its entire security surface is
> **disclosure**. Last generated: 2026-09-21.

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

It contains the un-anonymized kit: the organization name, two environment domains, 11 node
hostnames, three internal subnets, 16 raw session transcripts (one with credential-shaped
lines), runtime flush state, and 64 compiled articles about a specific installation.

- Gitignored. That single line is currently the only mechanical control on it.
- Never read into a card, a skeleton, a commit message, or a report.
- Never quoted, summarized or paraphrased. Its existence and exclusion may be stated; nothing
  further may be said about its contents.

**Why it is still on disk:** it is the provenance for every card. Deleting it would make the
claims unverifiable by the author. It is excluded, not destroyed.

## Enforcement

| Control | Catches | Does not catch |
| --- | --- | --- |
| `.gitignore` | `.legacy-assets/`, `**/.venv/`, `__pycache__/`, `*.pyc`, `.env*` | A file deliberately force-added |
| `check.py` anonymization pass | home-directory paths, IP addresses, internal domains, credential shapes | **A name.** An organization or person written in prose passes clean |
| Human review of the staged diff | names, paraphrase, anything contextual | Whatever the reviewer skims |

The gap is deliberate and must stay understood: **mechanical checks catch shapes, not
identities.** A card that names the employer in a sentence exits 0.

### Declared teaching exemptions

Card 18's skeleton demonstrates redaction, so it *must* contain credential-shaped strings, and
cards 16, 17 and 20 carry invented hostnames and addresses as examples. These paths are listed
in `ANON_EXEMPT` in `check.py`. Every string inside them is fabricated. Adding an exemption is a
deliberate act: it removes a file from the only automated control there is.

## Repository Hygiene

- **Two 136 MB virtualenvs** exist under `.claude/skills/excalidraw-diagram/references/.venv`
  and `.agents/skills/excalidraw-diagram/references/.venv`. Both are gitignored; before the
  first commit, confirm `git status` does not list them.
- **No secrets are required** to work in this repository. The three agent workflows reference
  `CLAUDE_CODE_OAUTH_TOKEN` and `OPENAI_API_KEY`; none is configured, which is the correct
  default. Their absence does not make the workflows inert — they still run and fail (see
  `RULES.md` § Known Open Items).
- **The repository is intended to be public.** Treat every file as though it already is.

## Before Publishing

```bash
python3 check.py                       # mechanical shapes
git diff --cached | grep -inE '<organization>|<username>|<domain>'   # names, by hand
git status --short                     # nothing unexpected staged
```

The second line cannot be automated without writing the masked strings into a public file,
which would defeat it. It is a human step, and it is the one that matters.
