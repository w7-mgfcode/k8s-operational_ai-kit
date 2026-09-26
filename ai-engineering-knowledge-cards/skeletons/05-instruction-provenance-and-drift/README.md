# Skeleton — Instruction Provenance and Drift

This is the only skeleton whose subject is a failure. It reproduces, in
miniature, what the source kit actually contained.

```
rules/commit-format.md       written here. carries a provenance line.
rules/testing-IMPORTED.md    imported. governs a package layout that is absent.
rules/security-IMPORTED.md   imported. cites a vision doc and a schema that
                             do not exist.
audit.py                     resolves every cited path; reports a truth %
src/, tests/                 the repository these rules supposedly govern
```

## Try it

```bash
python3 audit.py        # exits 1 — two rules resolve almost nothing
```

Read the two imported files first and try to spot the problem by eye. You
cannot, and that is the entire lesson: they are the **best-written files here**,
because someone wrote them carefully for a system where they were true. They
demand tests in a directory that does not exist, forbid writes to a file that
does not exist, and reference a vision document that does not exist.

An agent does not notice. It applies them, and produces work in the wrong shape,
with justification, indefinitely.

## What is deliberately missing

**A trigger.** The audit runs when you run it. Repository restructures widen the
gap, so the check belongs in the same change that restructures.

**Semantic checking.** Only paths are resolved. A rule that cites nothing and is
simply wrong about this project passes clean at 100%.

**The deletion step.** Detection is the easy half. The successor to the source
system found eight inherited rule files carrying 36 dead globs, with roughly
three quarters of cited paths unresolvable, and rebuilt the set from scratch —
repair was not the answer.
