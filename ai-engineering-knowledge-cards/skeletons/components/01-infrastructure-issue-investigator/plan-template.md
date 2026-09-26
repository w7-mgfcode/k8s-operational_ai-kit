---
cluster: {cluster}
namespace: {namespace}
date: {date}
workstream: {branch}
ranked_option: {option}
prod_guard: {guard}
---

# Remediation plan — {namespace} on {cluster}

## Root cause

**Status:** {status}

Commands run (read-only):
{evidence}

Signals, as carried forward after redaction:

{signals}

Repository references:
{repo}

Restricted matches:
{restricted}

## Chosen option

**{option}: {title}** — artifact `{artifact}`

Not chosen:
{rejected}

## Steps

1. Dry run the change against the lowest environment and read the diff.
2. Apply to the lowest environment.
3. Re-run the diagnose phase; expect no new restarts for ten minutes.

## Rollback

Revert the commit and re-apply; confirm the previous state with the same read-only
commands.

## Blast radius

Namespace-scoped unless the chosen option says otherwise.

## Environment progression

Lowest environment first; promote only after it has been green for a full day.

## Redaction review

{review}
