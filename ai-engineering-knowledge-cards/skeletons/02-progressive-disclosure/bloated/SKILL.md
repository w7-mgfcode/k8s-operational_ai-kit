---
name: release-notes-bloated
description: A helpful skill for release notes and changelogs and version stuff.
---

# Release Notes

## Overview

Turn a commit range into grouped, readable release notes.

## Commit taxonomy

### feat
A new capability visible to a user. Not a refactor that enables one.

### fix
A correction to behavior that was wrong. If nothing was wrong, it is a feat.

### breaking
Any change to a signature, a default, a wire format, or a file location that
an existing caller depends on. Renaming a flag is breaking. Adding an optional
flag is not.

### chore
Everything with no user-visible effect. If you are unsure between chore and
refactor, use chore — the distinction does not survive into the notes.

## Detecting breaking changes

Read each commit subject. If it matches the pattern of a type, optional scope
in parentheses, an exclamation mark, and a colon, it is breaking. Also treat a
commit as breaking if its body contains the phrase BREAKING CHANGE in any case,
with either a space or a hyphen between the words. Count these, then list each
one on its own line, indented by two spaces, in the order encountered.

## Template

Render the output as a level-one heading reading "Release" followed by the
version, then a level-two heading for breaking changes, then one for features,
then one for fixes.

## Workflow

1. Resolve the commit range. If none is given, use the last tag to HEAD.
2. Classify each commit using the taxonomy above.
3. Detect breaking changes using the procedure above.
4. Render using the template described above.
5. Flag anything unclassified for human review.
