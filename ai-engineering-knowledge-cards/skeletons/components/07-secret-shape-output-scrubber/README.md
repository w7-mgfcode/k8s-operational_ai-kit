# Skeleton — Secret-Shape Output Scrubber

The scrubber the investigator skill pipes every output through, and a check of
what its design removes by mistake and lets through. The card is
[component 07](../../../component-cards/skills/infrastructure-issue-investigator/scripts/07-secret-shape-output-scrubber.md);
the skill that runs it is [component 01](../01-infrastructure-issue-investigator/).

```
raw.txt       a fabricated session of command output: one Secret as YAML and as
              JSON, a pod's environment, an image digest, a config checksum and
              a commit — the same password appears three times
expect.json   what a correct scrub would remove, and the evidence it must keep
scrub.py      five ordered patterns, scrubbed text to stdout, audit lines to
              stderr; with --audit, the comparison against expect.json
```

## Try it

```bash
python3 scrub.py raw.txt            # scrubbed text and the audit log; exits 0
python3 scrub.py --audit raw.txt    # what went wrong, finding by finding; exits 1
```

**The first run.** Look at line 8 of the output first. The Secret's `data:` block
is gone, and the placeholder is glued to the next command — the block pattern
took the newlines with it. Then compare the audit log on stderr with the input:
the bearer token is on line 16, and the log says 13.

**The audit.** The password the YAML block hid is still there one line later,
in the JSON copy of the same Secret, and once more, decoded, inside the
connection URL. `CACHE_TOKEN` survives because the token pattern needs a word
boundary and an underscore is not one. Meanwhile the image digest, the config
checksum and the commit hash — evidence the plan exists to cite — are all
scrubbed. Two of the three went to the base64 pattern, so the hex pattern meant
for them only ever reaches a 32-character checksum.

Ten findings, and every one follows from one design choice: ordered pattern
matching over text whose format the patterns do not know. Exit 1 marks that
finding, not an error.

## What is deliberately missing

**Seven of the twelve patterns.** No kubeconfig documents, JWT shapes, cloud
access-key IDs, or separate patterns per keyword. Card 18's
[skeleton](../../../skeletons/18-the-redaction-boundary/) scrubs a whole
kubeconfig.

**The fixes.** Parsing JSON and scrubbing by key, exempting commit hashes and
digests by position, counting audit lines in the original input. Each is a few
lines; the source had none of them, and adding them here would hide what the
card describes.

**The caller.** In the skill, the model decides when to pipe through the
scrubber. Here you do, which is the same gap: nothing forces output through it.
