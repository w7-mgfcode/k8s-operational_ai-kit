---
name: release-notes
description: >
  Generates release notes from a commit range, grouping changes by type and
  flagging breaking changes. Triggers on: "write release notes", "what changed
  since the last tag", "draft the changelog entry". Do NOT use for: writing a
  single commit message, summarizing a pull request, or version bumping.
---

# Release Notes

## Overview

Turn a commit range into grouped, readable release notes.

## Workflow

1. Resolve the commit range. If none is given, use the last tag to HEAD.
2. Classify each commit by type. The taxonomy and the edge cases are in
   `references/taxonomy.md` — load it when a commit does not obviously fit.
3. Detect breaking changes by running `scripts/detect_breaking.py`. Do not
   read the script; run it and use its output.
4. Render using `assets/template.md`.
5. Flag anything the classifier marked `unknown` for human review.

## Validation

Every commit in the range appears exactly once in the output, or is listed
under "unclassified".
