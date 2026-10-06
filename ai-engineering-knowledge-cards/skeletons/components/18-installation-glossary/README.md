# Skeleton — Installation Glossary

A glossary whose rows carry measurements, a state they have drifted from, and a
second dictionary that disagrees with the first. The card is
[component 18](../../../component-cards/skills/workstream-hardening-orchestrator/references/18-installation-glossary.md);
the skill that loads the glossary is [component 08](../08-workstream-hardening-orchestrator/).

```
glossary.md     a fabricated glossary in the source's shape — term tables, and a
                header that says to use every term exactly
dictionary.md   the second dictionary that ships beside it, as the intake
                package's did
state.json      what is true today, as the version pins and a cluster read would
                report it
staleness.py    extracts versions, counts, endpoints, deadlines and times from
                each definition, checks them against state.json, and compares the
                two dictionaries term by term
```

## Try it

```bash
python3 staleness.py           # stale facts and conflicting terms; exits 1
python3 staleness.py --facts   # what the glossary actually measures; exits 0
```

**Start with `--facts`.** Seven of nine "terms" carry a number, a version, an
endpoint or a date. Only two are definitions in the plain sense. That is the
shape of the source file.

**Then the full run.** Four facts are stale: the node count, a version pin, the
number of applications that read secrets, and an end-of-life date that moved.
Under a header that says to use these terms exactly, each would be repeated in
every report the skill writes. Four terms are also defined differently in the
two dictionaries — one of them, the role tag, in a way that matters: "must equal"
and "usually" are different rules. Exit 1 marks the findings.

## What is deliberately missing

**The real state.** `state.json` is a fixture. A real check would read the
repository's version-pin file and a cluster's node and consumer counts.

**Facts the shapes miss.** An address pool, a replica policy written in words, a
team that changed name — anything without a recognisable shape passes. The
prototype reports what it can check, and the gap is the argument for keeping
measurements out of a glossary in the first place.

**One dictionary.** The prototype shows the two disagree; it does not merge them.
