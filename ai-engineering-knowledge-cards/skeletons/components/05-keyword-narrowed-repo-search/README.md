# Skeleton — Keyword-Narrowed Repository Search

A symptom-keyword → path table, the search it narrows, and an audit of the table
against the repository it describes. The card is
[component 05](../../../component-cards/skills/infrastructure-issue-investigator/references/05-keyword-narrowed-repo-search.md);
the skill that loads the search patterns is
[component 01](../01-infrastructure-issue-investigator/).

```
repo.json       a fabricated infrastructure-as-code repository: branch, fifteen file
                paths (two of them restricted vault files), four recent commits —
                one of which renamed a role
keywords.json   a fabricated keyword table, default scope and restricted list,
                written for this skeleton; one entry is stale and several keywords
                collide, on purpose
search.py       narrows, searches, extracts signals; --drift audits the table
```

## Try it

```bash
python3 search.py                                            # narrowed search; exits 0
python3 search.py --symptom "message queue backlog growing"  # a stale entry; exits 0
python3 search.py --drift                                    # audit the table; exits 1
```

**The first run** is the pattern working: "OOMKilled" selects a narrow slice of the
repository, the two vault files in that slice are listed and not opened, and the
search hands back the branch and two prior fixes — the inputs the ranking rubric's
reuse and workstream criteria need.

**The second** hits the stale entry. The queue keyword still points at the role's
old name, so the narrowed search matches nothing. The source's rule is to fall back
to the default scope only when *no keyword* matches; here one did. The prototype
falls back anyway and says so, and the fallback is broad enough to cross the
delegation threshold. The commit that caused it is right there in the history:
`refactor(queue): rename rabbitmq role to message-broker`. Nothing connected the
rename to the table — [card 05](../../../cards/05-instruction-provenance-and-drift.md)'s
failure, in one row.

**The drift audit** checks every pattern against the file list and finds two that
match nothing, one keyword contained in another (`pv` in `pvc`), a symptom that
triggers four narrowings with no rule for which wins, and the workstream criterion
reading nothing from a branch called `main`. The closing line is the point: a
table like this never fails loudly. It finds less, or more, and the ranking
downstream cannot tell.

## What is deliberately missing

**A real search.** Paths are matched against a list; no file is opened or grepped, so
the "search hits contain the restricted line" leak from
[component 03](../../../component-cards/skills/infrastructure-issue-investigator/references/03-investigation-safety-rules.md)
cannot happen here — which is also why this skeleton cannot show it.

**Git.** History is four entries in `repo.json`. The source ran six kinds of `git log`
probe against the real checkout.

**The subagent.** Past the threshold the source delegated the scan; this prints that
it would and carries on.

**The audit, in the source.** `--drift` is thirty lines. The source had no equivalent,
so a stale row stayed stale until someone noticed a search coming back empty.
