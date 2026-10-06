# Anonymization Log

This repository is derived from a real agent kit used daily in platform-engineering
work. The engineering content is preserved; the identity of the source system is not.
This log records what was removed and the rule applied, so the process can be audited
without access to the source.

## Rule

Public technology names stay. Anything that points at a *specific installation* of
them goes. A card should teach the pattern well enough to implement, and identify
nothing.

## Preserved

Architecture, component relationships, workflows, control and decision logic, design
patterns, decision points, constraints, trade-offs, failure modes, engineering
principles, conceptual terminology. Public tool names (Kubernetes, Ansible, Helm,
Vault, Prometheus, Grafana, Loki, Mimir, Tempo, Kyverno, Cilium, Longhorn). Orders of
magnitude, where the magnitude carries engineering meaning ("roughly two dozen
workloads", "about three weeks of daily use").

## Masked

| Class | Occurrences found | Rule applied |
|---|---|---|
| Employer / organization name | 152 | Removed. Cards say "the source system". |
| Operator username, home-directory paths | 48 | Removed. No absolute path from the source appears in any card. |
| Internal domains (two environment domains, an auth host, an object-store endpoint) | ~85 | Removed. Cards say "the cluster's secret store", "the object-store backend". |
| Node hostnames (11 distinct, structured naming scheme) | ~40 | Removed entirely. The naming scheme itself is identifying and is not described. |
| Internal IP addresses and CIDRs (3 distinct subnets) | ~20 | Removed. Cards do not describe network topology. |
| Source repository name | 42 | Replaced with "the platform repository". |
| Second organization name, found in an archived skill | 6 | Removed. |
| Project codename, found in a hardening guide | 19 | Removed. |
| Internal project/system abbreviations | ~50 | Removed. Where the concept mattered, it is described generically. |
| Third-party tool bound to personal workflow (credential manager) | 23 | Generalized to "a credential manager". |
| Operator timezone | 2 | Generalized to "a configured local timezone". |
| Third-party upstream issue and PR numbers in a permission allowlist | 9 | Not reproduced. |
| Secret-shaped strings in raw session logs | see below | Not reproduced. The logs are not published, quoted, or summarized. |

## Component cards

Component cards describe single artifacts from the source kit, so they sit closer to it
than pattern cards and carry a stricter rule. Each is written only after the owner names
the artifact and approves a masking table — every identifier found, with its generic
replacement. On top of the classes above, the source component's own name and its
siblings' names are replaced with generic titles, and its worked examples are not reused:
every example in a component card and its skeleton is fabricated. The commit for component
07 records its table; the earlier six do not, and are listed as an open item for review.

## Excluded from the repository entirely

- **Raw session logs** (16 files, ~1.4 MB). These are unredacted transcripts. One
  contains credential-shaped lines. They are the *source* of the knowledge but are not
  publishable, and nothing in this repository quotes or summarizes their content. Cards
  describe only the mechanism that processed them.
- **Runtime state** (session flush artifacts, dedup state, hook logs). Same reasoning.
- **Compiled knowledge articles** (64 articles). Every one is about a specific
  installation — its incidents, its topology, its decisions. The *pipeline* that
  produced them is card 13; the articles themselves are not reproducible in anonymized
  form without becoming meaningless.
- **A vendored virtual environment** (541 MB of third-party packages). Not the author's
  work and not relevant.

## What "partial" means on a card

Cards carry a `maturity` field. `partial` is used when the source system implemented
part of the pattern and not the rest, and the card says exactly which part. This is
deliberate: the gaps are the most instructive content in the repository, and smoothing
them over would make the cards a sales pitch rather than an engineering record.

## What is not claimed

Nothing here is a product, and nothing is presented as a general-purpose framework.
These are patterns observed in one system, built by one engineer, over a period of
daily use. Where a pattern was inherited from published work rather than invented, the
card says so.
