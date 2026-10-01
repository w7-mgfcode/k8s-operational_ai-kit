#!/usr/bin/env python3
"""Repository validation gate. Standard library only, no network, no cost.

Enforces the contracts this repository has — .claude/rules/cards.md,
.claude/rules/component-cards.md and .claude/rules/skeletons.md — plus the
anonymization boundary. Run it before
every commit; CI runs the same command.

Usage:
    python3 check.py              # contracts + links + imports + anonymization
                                  # (anonymization scans every file git would
                                  # publish, not only the cards tree)
    python3 check.py --run        # also execute every skeleton (slower)
    python3 check.py --quiet      # failures only
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "ai-engineering-knowledge-cards"
CARDS = PROJECT / "cards"
SKELETONS = PROJECT / "skeletons"
COMPONENT_CARDS = PROJECT / "component-cards"
COMPONENT_SKELETONS = SKELETONS / "components"

# --- card contract (.claude/rules/cards.md) --------------------------------
FRONTMATTER_KEYS = ["card", "title", "layer", "maturity", "instanced_by", "related"]
HEADING_COUNT = 13
LAYERS = {"instruction", "routing", "skill", "subagent", "memory", "execution", "validation"}
MATURITIES = {"proven", "partial", "abandoned"}

# --- component-card contract (.claude/rules/component-cards.md) ------------
COMPONENT_KEYS = ["component", "title", "type", "instances", "related"]
COMPONENT_HEADING_COUNT = 11
COMPONENT_TYPES = {"skill", "command", "rule", "subagent", "hook", "reference"}

# --- anonymization boundary (.claude/rules/anonymization.md) ---------------
# Generic shapes, not the masked strings themselves — this file is public too.
FORBIDDEN = [
    (r"/home/[a-z]", "absolute path from an operator's home directory"),
    (r"/Users/[a-z]", "absolute path from an operator's home directory"),
    (r"\b\d{1,3}(\.\d{1,3}){3}\b", "IP address"),
    (r"\b[a-z0-9-]+\.(local|internal|corp|lan)\b", "internal domain"),
    (r"(?i)\b(bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]\s*\S{12,})", "credential"),
]
# Paths that legitimately contain these shapes as teaching material.
ANON_EXEMPT = {
    "skeletons/18-the-redaction-boundary/sample-output.txt",
    "skeletons/18-the-redaction-boundary/README.md",
    "skeletons/18-the-redaction-boundary/redact.py",
    "skeletons/18-the-redaction-boundary/restricted_paths.py",
    "skeletons/18-the-redaction-boundary/artifact-template.md",
    "skeletons/17-blast-radius-gating/matrix.json",
    "skeletons/16-the-permission-ladder/policy-personal.json",
    "skeletons/20-repository-projection-pipeline/map.py",
}
# Directory names never scanned when git is unavailable (an exported tree).
NOT_PUBLISHED = {".git", ".legacy-assets", ".venv", "__pycache__"}

STDLIB_OK = {
    "argparse", "ast", "collections", "dataclasses", "datetime", "fnmatch",
    "functools", "hashlib", "io", "itertools", "json", "math", "os", "pathlib",
    "re", "shutil", "subprocess", "sys", "tempfile", "textwrap", "time",
    "typing", "unittest", "uuid", "zipfile", "__future__",
}


class Report:
    def __init__(self, quiet: bool) -> None:
        self.errors: list[str] = []
        self.quiet = quiet

    def fail(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def ok(self, line: str) -> None:
        if not self.quiet:
            print(f"  {line}")

    def section(self, name: str) -> None:
        if not self.quiet:
            print(f"\n{name}")


def frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---"):
        return [], text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [], text
    keys = re.findall(r"^([a-z_]+):", parts[1], re.M)
    return keys, parts[2]


def check_cards(r: Report) -> None:
    r.section("cards")
    files = sorted(CARDS.glob("*.md"))
    if not files:
        r.fail("cards", "no cards found")
        return
    related: dict[str, set[str]] = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        keys, body = frontmatter(text)
        rel = f.relative_to(PROJECT)
        block = re.search(r"^related:\n((?:\s+- .*\n?)*)", text, re.M)
        related[f.stem] = set(re.findall(r"- (\S+)", block.group(1))) if block else set()

        if keys[: len(FRONTMATTER_KEYS)] != FRONTMATTER_KEYS:
            r.fail(str(rel), f"frontmatter keys {keys[:6]} != {FRONTMATTER_KEYS}")

        n = len(re.findall(r"^## ", body, re.M))
        if n != HEADING_COUNT:
            r.fail(str(rel), f"{n} '##' headings, contract requires {HEADING_COUNT}")

        num = re.search(r"^card:\s*(\d+)", text, re.M)
        if not num or not f.name.startswith(f"{int(num.group(1)):02d}-"):
            r.fail(str(rel), "card number does not match the filename prefix")

        layer = re.search(r"^layer:\s*(\S+)", text, re.M)
        if not layer or layer.group(1) not in LAYERS:
            r.fail(str(rel), f"layer must be one of {sorted(LAYERS)}")

        mat = re.search(r"^maturity:\s*(\S+)", text, re.M)
        if not mat or mat.group(1) not in MATURITIES:
            r.fail(str(rel), f"maturity must be one of {sorted(MATURITIES)}")

        if not re.search(r"^## Provenance\s*$", body, re.M):
            r.fail(str(rel), "missing Provenance section")

    # related: is a graph, not a list of mentions — every edge resolves and
    # runs both ways (docs/_base/DEV_GUIDE.md, Adding a Card, step 6).
    for stem, targets in sorted(related.items()):
        for t in sorted(targets):
            if t not in related:
                r.fail(f"cards/{stem}.md", f"related '{t}' is not a card in cards/")
            elif stem not in related[t]:
                r.fail(f"cards/{stem}.md", f"related '{t}' does not list this card back")

    r.ok(f"{len(files)} cards, contract satisfied, related: edges symmetric")


def check_component_cards(r: Report) -> None:
    r.section("component cards")
    files = sorted(COMPONENT_CARDS.rglob("*.md"))
    pattern_cards = {c.stem for c in CARDS.glob("*.md")}
    seen: dict[int, str] = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        keys, body = frontmatter(text)
        rel = str(f.relative_to(PROJECT))

        if keys[: len(COMPONENT_KEYS)] != COMPONENT_KEYS:
            r.fail(rel, f"frontmatter keys {keys[:5]} != {COMPONENT_KEYS}")

        n = len(re.findall(r"^## ", body, re.M))
        if n != COMPONENT_HEADING_COUNT:
            r.fail(rel, f"{n} '##' headings, contract requires {COMPONENT_HEADING_COUNT}")

        num = re.search(r"^component:\s*(\d+)", text, re.M)
        if not num or not f.name.startswith(f"{int(num.group(1)):02d}-"):
            r.fail(rel, "component number does not match the filename prefix")
        elif int(num.group(1)) in seen:
            r.fail(rel, f"component number already used by {seen[int(num.group(1))]}")
        else:
            seen[int(num.group(1))] = rel

        kind = re.search(r"^type:\s*(\S+)", text, re.M)
        if not kind or kind.group(1) not in COMPONENT_TYPES:
            r.fail(rel, f"type must be one of {sorted(COMPONENT_TYPES)}")
        elif kind.group(1) != f.parent.name:
            r.fail(rel, f"type '{kind.group(1)}' does not match directory '{f.parent.name}'")

        block = re.search(r"^instances:\n((?:\s+- .*\n)+)", text, re.M)
        slugs = re.findall(r"- (\S+)", block.group(1)) if block else []
        if not slugs:
            r.fail(rel, "instances must list at least one pattern card")
        for slug in slugs:
            if slug not in pattern_cards:
                r.fail(rel, f"instances '{slug}' is not a card in cards/")

        d = COMPONENT_SKELETONS / f.stem
        readme = d / "README.md"
        if not readme.exists():
            r.fail(rel, f"no skeletons/components/{f.stem}/README.md")
            continue
        rtext = readme.read_text(encoding="utf-8")
        if not re.search(r"^## Try it\s*$", rtext, re.M):
            r.fail(f"skeletons/components/{f.stem}", "README has no '## Try it' section")
        if not re.search(r"^## What is deliberately missing", rtext, re.M):
            r.fail(f"skeletons/components/{f.stem}",
                   "README has no 'What is deliberately missing' section")
    r.ok(f"{len(files)} component cards, contract satisfied")


def check_links(r: Report) -> None:
    r.section("links")
    n = 0
    for f in list(PROJECT.rglob("*.md")):
        # templates/ holds fill-in forms whose NN- placeholders are the point.
        if f.parent.name == "templates":
            continue
        text = f.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith(("http", "#", "mailto:")):
                continue
            target = (f.parent / link.split("#")[0]).resolve()
            n += 1
            if not target.exists():
                r.fail(str(f.relative_to(PROJECT)), f"broken link -> {link}")
    r.ok(f"{n} internal links resolve")


def check_skeletons(r: Report) -> None:
    r.section("skeletons")
    missing = 0
    for card in sorted(CARDS.glob("*.md")):
        d = SKELETONS / card.stem
        if not d.is_dir():
            r.fail(str(card.relative_to(PROJECT)), "no matching skeleton directory")
            missing += 1
            continue
        readme = d / "README.md"
        if not readme.exists():
            r.fail(f"skeletons/{card.stem}", "no README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        if not re.search(r"^## Try it\s*$", text, re.M):
            r.fail(f"skeletons/{card.stem}", "README has no '## Try it' section")
        if not re.search(r"^## What is deliberately missing", text, re.M):
            r.fail(f"skeletons/{card.stem}",
                   "README has no 'What is deliberately missing' section")
    r.ok(f"{len(list(CARDS.glob('*.md'))) - missing} skeletons with a conforming README")


def check_imports(r: Report) -> None:
    r.section("imports")
    scripts = sorted(SKELETONS.rglob("*.py"))
    for p in scripts:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as e:
            r.fail(str(p.relative_to(PROJECT)), f"syntax error: {e}")
            continue
        local = {q.stem for q in p.parent.rglob("*.py")}
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module.split(".")[0]]
            for m in mods:
                if m not in STDLIB_OK and m not in local:
                    r.fail(str(p.relative_to(PROJECT)),
                           f"non-stdlib import '{m}' breaks the skeleton contract")
    r.ok(f"{len(scripts)} scripts, standard library only")


def publishable_files() -> list[Path]:
    """Every file git would publish: tracked, plus untracked and not ignored."""
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        paths = [ROOT / p for p in out.split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        paths = [p for p in ROOT.rglob("*")
                 if not NOT_PUBLISHED & set(p.relative_to(ROOT).parts)]
    return sorted(p for p in paths
                  if p.is_file() and p.relative_to(ROOT).parts[0] != ".legacy-assets")


def check_anonymization(r: Report) -> None:
    r.section("anonymization")
    hits = 0
    exempt = {f"{PROJECT.name}/{p}" for p in ANON_EXEMPT}
    files = publishable_files()
    for f in files:
        if f.suffix == ".png":
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel in exempt:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in FORBIDDEN:
            for m in re.finditer(pattern, text):
                line = text[: m.start()].count("\n") + 1
                r.fail(f"{rel}:{line}", f"{label} — see .claude/rules/anonymization.md")
                hits += 1
    if not hits:
        r.ok(f"{len(files)} publishable files, no identifier of a masked class found")


# Artifacts the skeletons write when run with defaults. The gate must not
# dirty the tree — see .claude/rules/skeletons.md.
RUN_ARTIFACTS = [
    "20-repository-projection-pipeline/pack.json",
    "15-structural-lint/lint-state.json",
    "14-index-guided-retrieval/state.json",
    "12-lifecycle-hooks-as-capture-points/hooks.log",
    "12-lifecycle-hooks-as-capture-points/last-flush.json",
]


def run_skeletons(r: Report) -> None:
    r.section("skeleton execution")
    ran = needs_args = 0
    dirs = [d for d in sorted(SKELETONS.iterdir())
            if d.is_dir() and d.name not in ("pipelines", "components")]
    if COMPONENT_SKELETONS.is_dir():
        dirs += [d for d in sorted(COMPONENT_SKELETONS.iterdir()) if d.is_dir()]
    for d in dirs:
        for script in sorted(d.glob("*.py")):
            try:
                # DEVNULL, not inherit: several skeletons read stdin and would
                # block forever waiting on a terminal that is not there.
                p = subprocess.run([sys.executable, str(script)],
                                   stdin=subprocess.DEVNULL, capture_output=True,
                                   text=True, cwd=d, timeout=30,
                                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            except subprocess.TimeoutExpired:
                r.fail(f"{d.relative_to(PROJECT)}/{script.name}", "timed out after 30s")
                continue
            # 0 = ran. 1 = ran and demonstrated a failure, which several
            # skeletons do on purpose. 2 = argparse usage error, i.e. the
            # script requires arguments and was not exercised here.
            if p.returncode == 2:
                needs_args += 1
                continue
            ran += 1
            if p.returncode not in (0, 1):
                r.fail(f"{d.relative_to(PROJECT)}/{script.name}",
                       f"crashed with exit {p.returncode}: {p.stderr.strip()[:120]}")

    for rel in RUN_ARTIFACTS:
        (SKELETONS / rel).unlink(missing_ok=True)
    for stale in (SKELETONS / "12-lifecycle-hooks-as-capture-points" / "daily").glob("*.md"):
        stale.unlink()

    r.ok(f"{ran} scripts ran clean, {needs_args} require arguments "
         f"(exercised by their README, not here)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true", help="also execute every skeleton")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    a = ap.parse_args()

    r = Report(a.quiet)
    check_cards(r)
    check_component_cards(r)
    check_links(r)
    check_skeletons(r)
    check_imports(r)
    check_anonymization(r)
    if a.run:
        run_skeletons(r)

    print()
    if r.errors:
        for e in r.errors:
            print(f"FAIL  {e}")
        print(f"\n{len(r.errors)} failure(s)")
        sys.exit(1)
    print("OK — all contracts satisfied")


if __name__ == "__main__":
    main()
