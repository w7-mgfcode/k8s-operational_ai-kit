#!/usr/bin/env python3
"""Structural lint for a knowledge base. Six checks, all deterministic.

No model, no network, no cost — which matters, because this is the stage with
no intrinsic motivation to run. Errors block. Warnings inform.

Usage:
    python3 lint.py                      # lints the broken corpus shipped here
    python3 lint.py --base ../13-log-as-source-compilation/knowledge
    python3 lint.py --errors-only
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = ("runbooks", "incidents", "decisions", "tool-patterns",
              "debugging", "connections", "answers")
REQUIRED_FIELDS = ("title", "category", "created")
SIZE_MIN, SIZE_MAX = 40, 2000      # words, excluding frontmatter
STATE = Path(__file__).resolve().parent / "lint-state.json"


def articles(base: Path) -> list[Path]:
    out: list[Path] = []
    for c in CATEGORIES:
        out.extend(sorted((base / c).glob("*.md")))
    return out


def body_words(text: str) -> int:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:]
    return len(text.split())


def lint(base: Path) -> list[dict]:
    issues: list[dict] = []
    arts = articles(base)
    index = base / "index.md"
    index_text = index.read_text(encoding="utf-8") if index.exists() else ""
    indexed = set(re.findall(r"\[\[([^\]]+)\]\]", index_text))

    def add(sev, check, f, detail):
        issues.append({"severity": sev, "check": check, "file": f, "detail": detail})

    for a in arts:
        rel = a.relative_to(base)
        slug = str(rel.with_suffix("")).replace("\\", "/")
        text = a.read_text(encoding="utf-8")

        # 1. link resolution
        for link in re.findall(r"\[\[([^\]]+)\]\]", text):
            if link.startswith("daily/"):      # points outside the corpus by design
                continue
            if not (base / f"{link}.md").exists():
                add("error", "broken_link", str(rel), f"[[{link}]] does not resolve")

        # 4. frontmatter completeness
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{field}:", text, re.M):
                add("error", "frontmatter", str(rel), f"missing required field: {field}")

        # 3. index coverage (documents -> index)
        if slug not in indexed:
            add("error", "index_coverage", str(rel), "document missing from index")

        # 5. size outliers
        w = body_words(text)
        if w < SIZE_MIN:
            add("warning", "size_outlier", str(rel), f"{w} words — likely a stub")
        elif w > SIZE_MAX:
            add("warning", "size_outlier", str(rel), f"{w} words — likely unsplit")

        # 6. source attribution
        if "## Sources" not in text:
            add("warning", "attribution", str(rel), "no Sources section")

    # 2. orphan detection
    all_text = {a: a.read_text(encoding="utf-8") for a in arts}
    for a in arts:
        slug = str(a.relative_to(base).with_suffix("")).replace("\\", "/")
        inbound = sum(1 for o, t in all_text.items() if o != a and f"[[{slug}]]" in t)
        if inbound == 0:
            add("warning", "orphan", str(a.relative_to(base)), "no inbound links")

    # 3. index coverage (index -> documents)
    for link in indexed:
        if not (base / f"{link}.md").exists():
            add("error", "index_coverage", "index.md", f"row points at missing [[{link}]]")

    return issues


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=str(Path(__file__).resolve().parent / "knowledge"))
    ap.add_argument("--errors-only", action="store_true")
    args = ap.parse_args()

    base = Path(args.base)
    if not base.exists():
        print(f"no such knowledge base: {base}", file=sys.stderr)
        sys.exit(2)

    issues = lint(base)
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    for i in errors:
        print(f"ERROR   {i['check']:<16} {i['file']:<44} {i['detail']}")
    if not args.errors_only:
        for i in warnings:
            print(f"warning {i['check']:<16} {i['file']:<44} {i['detail']}")

    n = len(articles(base))
    print(f"\n{n} documents — {len(errors)} error(s), {len(warnings)} warning(s)")
    for c in CATEGORIES:
        k = len(list((base / c).glob("*.md")))
        if k == 0:
            print(f"  {c}: empty  <-- curation signal, not a failure")

    # A linter's output is meaningless without a date attached.
    try:
        prev = json.loads(STATE.read_text()).get("last_run")
        if prev:
            print(f"\nprevious run: {prev}")
    except Exception:
        pass
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    STATE.write_text(json.dumps({"last_run": now, "errors": len(errors)}, indent=2))
    print(f"this run:     {now}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
