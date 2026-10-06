---
component: 07
title: Secret-Shape Output Scrubber
type: script
instances:
  - 02-progressive-disclosure
  - 06-calibrated-degrees-of-freedom
  - 18-the-redaction-boundary
related:
  - 01-infrastructure-issue-investigator
  - 03-investigation-safety-rules
  - 06-remediation-plan-template
---

# Secret-Shape Output Scrubber

> The investigator skill's only code: ordered patterns between raw command output and
> the plan — biased to over-redact, and blind to any format it has no pattern for.

## What it is

A standard-library Python filter the investigator skill
([component 01](../01-infrastructure-issue-investigator.md)) runs on command output
before carrying it into a later phase or writing it into the plan. It reads stdin,
applies a fixed list of secret-shaped patterns one after another, and writes the
scrubbed text to stdout and one audit line per hit to stderr. It is the concrete gate
behind [card 18](../../../../cards/18-the-redaction-boundary.md), and the only part of
the skill that is code rather than instruction.

## Trigger and routing

Not routed by a description; it is executed, never loaded. The skill's entry file lists
it in a one-row scripts table with its interface, and tells the model to pipe every
output that will be carried forward through it — in the diagnose phase, and again
before anything is written to disk. The scrubbing section of the safety rules
([component 03](../references/03-investigation-safety-rules.md)) restates the same
requirement. Nothing in the harness routes output through it: every call is one the
model remembered to make.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Raw command output on stdin | yes | the diagnose phase's read-only commands, and repository search results |
| Arguments | no | none are accepted; the pattern list is fixed in the script |

## Procedure

1. Read all of stdin. If it cannot be read, report that on stderr and exit non-zero.
2. Apply each pattern in a fixed order, most specific first: whole kubeconfig
   documents, the indented key-value lines under a Secret's `data:` or `stringData:`,
   bearer headers, password, token, API-key, secret and credential assignments, long
   base64 runs, JWT-shaped strings, cloud access-key IDs, long hex strings. Each pattern
   runs over the text the previous one produced.
3. Replace either the whole match or only its value group with a fixed placeholder, so
   a key survives and tells the reader what was there.
4. Record each hit as a pattern name and a line number, counted in the text as that
   pattern saw it.
5. Write the scrubbed text to stdout and one `REDACTED: <pattern> at line <n>` line per
   hit to stderr. Exit 0, whether or not anything matched.

## Tools and permissions

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| Read stdin, write stdout and stderr | yes | the script |
| Files, network, subprocesses | no | the script — it contains no such call |
| Being called at all | required | the skill's instructions only; the harness does not force output through it |

## Outputs

Scrubbed text on stdout, which the skill carries forward in place of the raw output.
Audit lines on stderr, which the plan's redaction-review block
([component 06](../assets/06-remediation-plan-template.md)) lists, so a reader can see
what was removed. The exit code is 0 for clean input and for input with hits alike;
only stderr tells them apart.

## Failure modes

Every row below is read directly off the script.

| Failure | Symptom | Root cause |
|---|---|---|
| Evidence is scrubbed | A plan that should cite a commit or an image digest shows the placeholder where the hash was | Any run of forty or more base64-alphabet characters after a separator is removed, and full commit hashes and image digests are in that alphabet. Observed |
| One pattern is shadowed by another | The long-hex pattern never fires on a commit hash or a digest; it fires on a 32-character config checksum, which is not a secret either | Hex is a subset of base64, and the base64 pattern runs first. The hex pattern only ever sees 32 to 39 characters. Structural |
| The same secret leaks in JSON | A value removed from `-o yaml` output passes untouched in `-o json` output of the same object | The data-block pattern matches YAML indentation only, and every keyword pattern expects the separator straight after the key — JSON quotes the key. A JSON value survives unless its base64 runs to forty characters or more. Observed |
| Prefixed names pass | `DB_PASSWORD` is scrubbed; `CACHE_TOKEN` and `APP_SECRET` are not | Token, secret, credential and API-key require a word boundary before the key, and an underscore is a word character. Password has no boundary, so the inconsistency is in the patterns. Observed |
| Credentials inside URLs pass | A connection string carries its password into the plan | No pattern recognises `user:password@host`; there is no keyword in front of the value. Observed |
| A block collapses its lines | The placeholder is glued to the following line, and every later audit line names the wrong line | The data-block replacement takes the block's newlines with it, and each later pattern counts lines in the already-collapsed text. Observed |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [02 Progressive Disclosure](../../../../cards/02-progressive-disclosure.md) | Executed, never read: its patterns cost no context, and only its output enters the conversation |
| [06 Calibrated Degrees of Freedom](../../../../cards/06-calibrated-degrees-of-freedom.md) | Scrubbing is too fragile to leave to prose, so it is code — the same input gives the same output, and the pattern list can be reviewed as a list |
| [18 The Redaction Boundary](../../../../cards/18-the-redaction-boundary.md) | The gate itself: ordered patterns, dual-channel output, biased to over-redact — and the pattern's novel-format, partial-mangling and unwired-path failures in concrete form |

## Provenance

Instanced in the source system by one standard-library Python script of about 150 lines
in the investigator skill's scripts directory: twelve compiled patterns in a fixed
order, a substitution loop and a stdin-to-stdout entry point. Its own documentation
calls it intentionally conservative and points at the plan's review block as the
place over-redaction is caught. Nothing in it records how often it ran, what it
removed, or whether anything passed it; this card claims none of that.

## Prototype

Minimal runnable prototype in
[`../../../../skeletons/components/07-secret-shape-output-scrubber/`](../../../../skeletons/components/07-secret-shape-output-scrubber/).
Standard library, offline. It scrubs a fabricated session of command output with five
of the patterns in the same sequential design, and with `--audit` compares the result
with a list of what should have been removed and what should have been kept.

## What is deliberately missing

**Scrubbing by structure.** Three of the six failures — scrubbed evidence, the JSON
leak and URL credentials — come from matching text without knowing its format. JSON can be parsed and scrubbed by key with the
standard library; YAML cannot, which is one honest reason the source matched text.

**An allow-list for evidence.** Commit hashes and image digests have known shapes in
known positions. Exempting them is a few lines, and it stops the scrubber removing the
evidence the plan exists to cite.

**Audit lines that point at the input.** Counting lines in the original text, not in
the text an earlier pattern rewrote.

**A hard gate.** The scrubber filters only what it is given. Nothing makes the model
pipe output through it; card 18's unwired-path failure applies unchanged.

**In the prototype:** five patterns instead of twelve — no kubeconfig documents, JWTs
or cloud access-key IDs. Card 18's skeleton scrubs a whole kubeconfig.
