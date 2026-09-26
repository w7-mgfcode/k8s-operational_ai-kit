#!/usr/bin/env python3
"""Keyword-narrowed repository search — map a symptom to likely paths, search only
there, and pull the signals a ranking needs. Then check the map against the repo.

    python3 search.py                                   narrow and search for the default symptom
    python3 search.py --symptom "message queue backlog growing"
    python3 search.py --drift                           audit the keyword table itself

Searches a fabricated file list, not a real checkout. Exit codes: 0 = searched.
1 = --drift found a stale pattern or a keyword collision (the demonstration).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELEGATE_DIRS = 5  # above this many candidate role directories, hand off to a subagent


def match(files: list[str], globs: list[str]) -> list[str]:
    return [f for f in files if any(fnmatch.fnmatch(f, g) for g in globs)]


def keywords_in(symptom: str, narrow: dict) -> list[str]:
    s = symptom.lower()
    return [k for k in narrow if k in s]  # substring, as the source specifies


def search(repo: dict, kw: dict, symptom: str) -> None:
    files, restricted = repo["files"], kw["restricted"]
    hits = keywords_in(symptom, kw["narrow"])
    print(f"symptom:  {symptom!r}")
    print(f"keywords: {', '.join(hits) or 'none'}")

    if hits:
        globs = sorted({g for k in hits for g in kw["narrow"][k]})
        scope = match(files, globs)
        print(f"narrowed: {', '.join(globs)}")
        if not scope:
            print("  the narrowed patterns match no file in the repository.")
            print("  The source says to fall back only when no keyword matches — here one")
            print("  did, so it would search nothing. Falling back anyway, and saying so.")
            scope = match(files, kw["default_scope"])
    else:
        scope = match(files, kw["default_scope"])
        print("narrowed: no keyword, default scope")

    roles = {f.split("/")[1] for f in scope if f.startswith("roles/")}
    if len(roles) > DELEGATE_DIRS:
        print(f"  {len(roles)} candidate role directories: the source delegates to an "
              "exploration subagent here (continuing inline for the demo)")

    print()
    opened = []
    for f in scope:
        if any(fnmatch.fnmatch(f, r) for r in restricted):
            print(f"  not opened  {f}  (restricted — record the path, check by hand)")
        else:
            opened.append(f)
            print(f"  read        {f}")

    prior = [c for c in repo["commits"] if c["path"] in opened]
    print(f"\nbranch:   {repo['branch']}")
    for c in prior:
        print(f"prior:    {c['hash']} {c['subject']}")
    print(f"signals:  {len(roles)} role(s), {len(prior)} prior fix(es), "
          f"{len(scope) - len(opened)} restricted match(es)")


def drift(repo: dict, kw: dict) -> int:
    files, problems = repo["files"], 0

    print("── patterns that match nothing ─────────────────────────────")
    for k, globs in kw["narrow"].items():
        dead = [g for g in globs if not match(files, [g])]
        for g in dead:
            problems += 1
            renamed = [c for c in repo["commits"] if "rename" in c["subject"]]
            hint = f"  (see {renamed[0]['hash']}: {renamed[0]['subject']})" if renamed and k == "queue" else ""
            print(f"  '{k}' -> {g}: no file matches{hint}")

    print("\n── keywords that collide ───────────────────────────────────")
    keys = list(kw["narrow"])
    for a in keys:
        for b in keys:
            if a != b and a in b:
                problems += 1
                print(f"  '{a}' is inside '{b}': every '{b}' symptom also narrows by '{a}'")
    probe = "pvc pending after helm upgrade on node pool b"
    hits = keywords_in(probe, kw["narrow"])
    print(f"\n  {probe!r}")
    union = match(files, sorted({g for k in hits for g in kw["narrow"][k]}))
    areas = sorted({f.split("/")[1] for f in union if f.startswith("roles/")})
    print(f"  matches {len(hits)} keywords ({', '.join(hits)}); the table does not say which "
          f"narrowing wins, so the search takes the union: {len(union)} file(s) from "
          f"{len(areas)} unrelated area(s) ({', '.join(areas)}), none ranked above the others")
    problems += len(hits) > 2

    print("\n── workstream read from the branch name ────────────────────")
    for branch in (repo["branch"], "main", "fix-1234"):
        on_theme = any(w in branch for w in ("shop", "stability", "oom", "memory"))
        print(f"  {branch:22} workstream fit: {'scored' if on_theme else '0 — the name says nothing'}")

    print(f"\n{problems} problem(s) in the keyword table. None of them shows up when a search "
          "succeeds; all of them show up as a search that quietly found less, or more.")
    return 1 if problems else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--symptom", default="checkout pods OOMKilled after cache change")
    ap.add_argument("--drift", action="store_true", help="audit the keyword table")
    a = ap.parse_args()
    repo = json.loads((HERE / "repo.json").read_text())
    kw = json.loads((HERE / "keywords.json").read_text())
    if a.drift:
        sys.exit(drift(repo, kw))
    search(repo, kw, a.symptom)


if __name__ == "__main__":
    main()
