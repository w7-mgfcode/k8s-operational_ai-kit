# Skeleton — Investigation Safety Rules

Five of the investigator skill's six safety rule sets, turned into functions and run
against fabricated inputs — first the cases each rule was written for, then one case
it was not. The card is
[component 03](../../../component-cards/reference/03-investigation-safety-rules.md);
the skill that loads the rules is
[component 01](../01-infrastructure-issue-investigator/).

```
guard.py      the prod guard, the command deny list, web-query hygiene, restricted
              paths and secret scrubbing, each as a small function
inputs.json   fabricated contexts, commands, draft queries, search hits and output
              lines, split into "cases" and "probes"
```

## Try it

```bash
python3 guard.py            # every rule on its intended cases; exits 0
python3 guard.py --audit    # one probe per gap; exits 1
```

**The first run** is the rules working as written: development and production
contexts classified correctly, destructive verbs denied, installation names stripped
from a query, restricted files left closed, credential values scrubbed with their
keys kept.

**The audit** is eleven probes getting through:

- A context named for development that points at production is classified as
  development. The guard reads names, not clusters.
- Six commands that change the cluster — `run`, `exec`, `label`,
  `rollout restart`, `create`, `set image` — are on no list. The deny list names the
  verbs someone remembered; an allow list of read verbs refuses all six without
  having to remember anything.
- "Strip every proper noun" run literally keeps the lowercase workload and namespace
  names and removes the error string and the public component name the rule says to
  keep. The filter that works needs a list of installation names, which the rules do
  not have.
- A search hit inside a vault file is correctly not opened — and its matched line,
  with the password in it, is already in the search result.
- The rules say long base64 strings are redacted after known secret keys; the skill's
  own script redacts any such string, anywhere. On a checksum the script is right to
  be cautious and wrong on the facts; on a base64-encoded connection string under an
  unrecognized key, the rules as written leak it.

Exit 1 marks those findings. Nothing here crashes on purpose.

## What is deliberately missing

**The sixth rule set.** Confirmation points — one yes/no per event, never batched —
govern the conversation, not data. There is nothing to run.

**The harness.** Three of the fifteen denied verbs were also blocked by the harness
in the source system, which made those three the only real controls. This prototype
has no harness; every rule here is as advisory as it was there.

**A redactor worth using.** The scrubbing functions are just enough to show the
rules and the script disagreeing. [Card 18](../../../cards/18-the-redaction-boundary.md)'s
skeleton is the fuller version, with its own documented misses.
