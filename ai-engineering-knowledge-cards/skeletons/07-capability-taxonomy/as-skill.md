---
name: dependency-audit
description: >
  Audits a repository's declared dependencies against what is actually
  imported, reporting unused declarations and undeclared imports. Triggers on:
  "audit our dependencies", "what are we importing that isn't declared",
  "find unused packages", "check the dependency manifest". Do NOT use for:
  upgrading versions (use /upgrade-deps), resolving conflicts, or auditing
  transitive dependencies.
---

# Dependency Audit (as a SKILL)

Fires automatically when the model judges the request to match.

**Cost:** the description above is resident in every session, forever, whether
or not anyone audits anything.

**Why a skill:** the value is that it fires when someone describes the problem
without knowing this capability exists.
