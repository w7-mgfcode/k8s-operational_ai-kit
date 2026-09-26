# Skeleton — The Redaction Boundary

```
redact.py             ordered patterns, dual-channel output
sample-output.txt     real-shaped tool output: env vars, a secret, a bearer
                      token, a whole kubeconfig
restricted_paths.py   the never-read list, applied to search results too
artifact-template.md  with the mandatory redaction-review block
```

## Try it

```bash
python3 redact.py < sample-output.txt
python3 redact.py --report < sample-output.txt
python3 restricted_paths.py
```

Run the first command and compare its output to the input. The **keys survive
and the values do not** — `password=«REDACTED»` still tells a reader that a
database password is set there, which is the diagnostic half, while removing
the part that matters.

The second command is the audit trail. Those lines belong in the artifact's
redaction-review block, which is what makes a conservative redactor tolerable:
if it removed something you needed, you can see that it did.

`restricted_paths.py` filters **search results**, not just direct reads. A grep
hit that quotes a line out of a vault file has already leaked it.

## What is deliberately missing

**Wiring.** This gate protects whatever is piped through it and nothing else.
That is precisely how the source system failed: the redactor existed, worked,
and was never carried across to the memory pipeline, so sixteen unredacted
transcripts accumulated — see
[card 12](../12-lifecycle-hooks-as-capture-points/) and
[card 13](../../cards/13-log-as-source-compilation.md).

**Novel formats.** Pattern matching cannot recognize a secret it has no pattern
for. There is a live example in `sample-output.txt`: the line

```
DSN=postgres://admin:s3cr3tvalue@db.internal:5432/app
```

passes through **untouched**. The key is `dsn`, the credential is embedded in a
URL, and no rule here looks for that shape. Diff the input against the output
and you will find it still there. Every redactor has a set of these; the
question is only whether you know what is in yours.

**The context.** The agent still read the secret. Redaction protects the
artifact, not the session that produced it.
