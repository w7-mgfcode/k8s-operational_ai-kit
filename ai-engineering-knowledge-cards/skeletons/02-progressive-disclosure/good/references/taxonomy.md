# Commit taxonomy

Loaded only when a commit does not obviously fit. Grep for the type name.

## feat
A new capability visible to a user. Not a refactor that enables one.

## fix
A correction to behavior that was wrong. If nothing was wrong, it is a feat.

## breaking
Any change to a signature, a default, a wire format, or a file location that
an existing caller depends on. Renaming a flag is breaking. Adding an optional
flag is not.

## chore
Everything with no user-visible effect. If you are unsure between chore and
refactor, use chore — the distinction does not survive into the notes.
