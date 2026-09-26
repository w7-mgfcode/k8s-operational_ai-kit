#!/usr/bin/env python3
"""Infrastructure issue investigator — the phases of a read-only planning skill,
run against fixture data instead of a cluster.

    intake -> diagnose -> redact -> research (web || repo) -> brainstorm
           -> rank -> plan

Nothing here touches a cluster, the network or a model. `cluster.json` stands in
for read-only command output, `repo.json` for the infrastructure-as-code
repository, and `candidates.json` for what the brainstorm model call returns.

Exit codes: 0 = a plan was produced. 1 = a guard stopped the run on purpose
(prod guard, or a diagnostic verb the deny list failed to catch).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The source skill enforced read-only access with a deny list of write verbs.
DENY = ("delete", "apply", "patch", "edit", "replace", "scale", "drain",
        "cordon", "uncordon", "install", "upgrade", "uninstall", "rollback")
# The alternative: name the verbs that are allowed and refuse everything else.
ALLOW = ("get", "describe", "logs", "top", "auth")

# Symptom class -> read-only commands, beyond the baseline every run starts with.
BASELINE = ["get events --sort-by=.lastTimestamp", "get pods", "get deploy,sts,ds,job,cronjob"]
PLAYBOOK = {
    "pod-lifecycle": ["describe pod {pod}", "logs {pod} --previous --tail=200",
                      "top pods --sort-by=memory"],
    # Mirrors the source: a TLS probe that looks diagnostic but creates a pod.
    "tls": ["get certificate,certificaterequest",
            "run curl --rm -i --image=curl -- curl -vI https://{svc}"],
}
# Symptom class -> where repo research narrows first.
NARROW = {"pod-lifecycle": ["roles/*app*/**", "inventories/*/group_vars/*"],
          "tls": ["roles/cert*/**", "roles/*tls*/**"]}
# Lines worth quoting in the plan, after redaction.
SIGNAL = re.compile(r"OOMKilled|Restart Count|memory:|PASSWORD|token=|cache")
RESTRICTED = ["*vault*.yml", "*/secrets/*", ".env", ".envrc"]

REDACTIONS = [
    ("password", re.compile(r"(?i)(password\w*\s*[:=]?\s*)(\S+)")),
    ("token", re.compile(r"(?i)\b(token\s*[:=]\s*)([A-Za-z0-9._-]{8,})")),
    ("secret", re.compile(r"(?i)\b(secret\s*[:=]\s*)(\S+)")),
]


def rule(title: str) -> None:
    print(f"\n── {title} " + "─" * max(0, 60 - len(title)))


# ── phase 1 ──────────────────────────────────────────────────────────────────
def intake(a: argparse.Namespace) -> str:
    rule("1 intake")
    if not a.cluster or not a.namespace:
        print("  gate: cluster and namespace are required before anything runs")
        sys.exit(2)
    guarded = "dev" not in a.cluster
    print(f"  cluster={a.cluster}  namespace={a.namespace}  symptom={a.symptom}")
    if guarded and not a.confirm_prod:
        print(f"  PROD GUARD TRIPPED: '{a.cluster}' does not resolve to dev.")
        print("  Re-run with --confirm-prod to continue, still strictly read-only.")
        sys.exit(1)
    status = "confirmed" if guarded else "not-triggered"
    print(f"  prod guard: {status}")
    return status


# ── phase 2 ──────────────────────────────────────────────────────────────────
def verb_of(cmd: str) -> str:
    return cmd.split()[0]


def diagnose(a: argparse.Namespace, cluster: dict) -> list[tuple[str, str]]:
    rule("2 diagnose (read-only)")
    cmds = BASELINE + PLAYBOOK[a.symptom]
    names = {"pod": "checkout-7d9f6c5b8-x2k4q", "svc": "checkout.shop.svc"}
    captured = []
    for tmpl in cmds:
        cmd = tmpl.format(**names)
        v = verb_of(cmd)
        if v in DENY:
            print(f"  refused by deny list: {cmd}")
            continue
        if v not in ALLOW:
            # The deny list let this through. It is a write, not a read.
            print(f"  deny list: allowed   allow list: BLOCKED   -> kubectl {cmd}")
            print(f"  '{v}' is not a write verb the deny list names, but it creates "
                  "an object in the cluster.")
            print("  A skill that trusted its deny list would have run it. Stopping.")
            sys.exit(1)
        out = cluster["outputs"].get(cmd)
        print(f"  kubectl -n {a.namespace} {cmd}" + ("" if out else "   (no fixture)"))
        if out:
            captured.append((cmd, out))
    if not captured:
        print("  gate: no signal captured and no user override")
        sys.exit(1)
    return captured


def redact(captured: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[str]]:
    rule("2b redact before carrying anything forward")
    safe, review = [], []
    for cmd, out in captured:
        for name, pat in REDACTIONS:
            for m in pat.finditer(out):
                review.append(f"{name} in `{cmd}`")
            out = pat.sub(lambda m: m.group(1) + "«REDACTED»", out)
        safe.append((cmd, out))
    for line in review:
        print(f"  REDACTED: {line}")
    print(f"  {len(review)} value(s) scrubbed; listed again in the plan's review block")
    return safe, review


# ── phase 3 ──────────────────────────────────────────────────────────────────
def web_search(query: str) -> list[str]:
    """Stub. The real skill calls a web-search tool here."""
    print(f"  [stub] web_search({query!r}) -> not called; offline skeleton")
    return []


def hygienic_query(a: argparse.Namespace, signal: str) -> str:
    q = f"{a.cluster} {a.namespace} checkout kubernetes container {signal}"
    for name in (a.cluster, a.namespace, "checkout"):
        q = q.replace(name, "")
    q = " ".join(q.split())
    assert a.namespace not in q and a.cluster not in q
    return q


def research(a: argparse.Namespace, safe: list[tuple[str, str]], repo: dict) -> dict:
    rule("3 research: web || repo")
    text = "\n".join(out for _, out in safe)
    signal = "OOMKilled" if "OOMKilled" in text else "CrashLoopBackOff"
    web_search(hygienic_query(a, signal))

    hits, skipped = [], []
    for path in repo["files"]:
        if not any(fnmatch.fnmatch(path, g) for g in NARROW[a.symptom]):
            continue
        if any(fnmatch.fnmatch(path, r) for r in RESTRICTED):
            skipped.append(path)
        else:
            hits.append(path)
    prior = [c for c in repo["commits"] if any(c["path"] == h for h in hits)]
    print(f"  branch: {repo['branch']}")
    for h in hits:
        print(f"  repo:   {h}")
    for s in skipped:
        print(f"  repo:   {s}  -- restricted, not opened; check manually")
    for c in prior:
        print(f"  prior:  {c['hash']} {c['subject']}")
    return {"signal": signal, "hits": hits, "skipped": skipped, "prior": prior,
            "branch": repo["branch"]}


# ── phase 4 + 5 ──────────────────────────────────────────────────────────────
def brainstorm() -> list[dict]:
    """Stub. The real skill asks the model for 3-6 scored candidates here."""
    rule("4 brainstorm")
    print("  [stub] model call -> candidates.json")
    cands = json.loads((HERE / "candidates.json").read_text())["candidates"]
    if len(cands) < 3:
        print("  gate: fewer than three options")
        sys.exit(1)
    return cands


def rank(cands: list[dict]) -> list[dict]:
    rule("5 rank")
    crit = json.loads((HERE / "rubric.json").read_text())["criteria"]
    for c in cands:
        c["total"] = sum(c["scores"][k["key"]] * k["weight"] for k in crit)
        # Tie-break in criterion order: reuse first, then workstream, and so on.
        c["order"] = tuple(c["scores"][k["key"]] for k in crit)
    ranked = sorted(cands, key=lambda c: (c["total"], c["order"]), reverse=True)
    print("  | # | Option | Reuse | Blast | Reversible | Score |")
    print("  |---|--------|-------|-------|------------|-------|")
    for i, c in enumerate(ranked, 1):
        reuse = ("no", "partial", "yes")[c["scores"]["reuse"]]
        print(f"  | {i} | {c['id']}: {c['title']} | {reuse} | {c['scope']} | "
              f"{c['reversible']} | {c['total'] / 2:g}/12 |")
    top, second = ranked[0], ranked[1]
    if top["total"] == second["total"]:
        print(f"  tie at {top['total']}/24 between {top['id']} and {second['id']}: "
              f"{top['id']} wins on the first differing criterion")
    print("  gate: the user acknowledges #1 or picks another -> auto-acknowledged here")
    return ranked


# ── phase 6 + 7 ──────────────────────────────────────────────────────────────
def plan(a, guard, safe, review, found, ranked) -> str:
    rule("6 plan")
    text = "\n".join(out for _, out in safe)
    confirmed = "OOMKilled" in text and "Restart Count" in text
    top = ranked[0]
    fill = {
        "date": date.today().isoformat(), "cluster": a.cluster, "namespace": a.namespace,
        "branch": found["branch"], "option": top["id"], "guard": guard,
        "status": "confirmed" if confirmed else "hypothesis",
        "evidence": "\n".join(f"- `{cmd}`" for cmd, _ in safe),
        "signals": "\n".join(f"    {ln.strip()}" for ln in text.splitlines()
                              if SIGNAL.search(ln)),
        "repo": "\n".join(f"- `{h}`" for h in found["hits"]) or "- none",
        "restricted": "\n".join(f"- `{s}` not opened" for s in found["skipped"]) or "- none",
        "title": top["title"], "artifact": top["artifact"],
        "rejected": "\n".join(f"- {c['id']}: {c['title']} ({c['total'] / 2:g}/12)"
                              for c in ranked[1:]),
        "review": "\n".join(f"- {r}" for r in review) or "- none detected",
    }
    doc = (HERE / "plan-template.md").read_text()
    for k, v in fill.items():
        doc = doc.replace("{" + k + "}", v)
    print(doc)
    return doc


def save(a, doc: str) -> None:
    rule("7 save")
    name = f"{date.today().isoformat()}-{a.cluster}-{a.namespace}-plan.md"
    if not a.save:
        print(f"  would write {name}; pass --save DIR to be asked")
        return
    target = Path(a.save) / name
    try:
        answer = input(f"  write {target}? [y/N] ")
    except EOFError:
        answer = ""
    if answer.strip().lower() != "y":
        print("  not written: saving always needs an explicit yes")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc)
    print(f"  wrote {target}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cluster", default="dev")
    ap.add_argument("--namespace", default="shop")
    ap.add_argument("--symptom", choices=sorted(PLAYBOOK), default="pod-lifecycle")
    ap.add_argument("--confirm-prod", action="store_true")
    ap.add_argument("--save", metavar="DIR")
    a = ap.parse_args()

    cluster = json.loads((HERE / "cluster.json").read_text())
    repo = json.loads((HERE / "repo.json").read_text())

    guard = intake(a)
    safe, review = redact(diagnose(a, cluster))
    found = research(a, safe, repo)
    ranked = rank(brainstorm())
    save(a, plan(a, guard, safe, review, found, ranked))


if __name__ == "__main__":
    main()
