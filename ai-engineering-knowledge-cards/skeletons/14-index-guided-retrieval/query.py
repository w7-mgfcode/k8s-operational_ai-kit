#!/usr/bin/env python3
"""Index-guided retrieval. No embeddings, no vector store.

The model reads the INDEX — not the corpus — selects a few documents, opens
only those, and synthesizes. Selection is stubbed behind `select()` so the
skeleton runs offline; the point is that the step is inspectable, which is
exactly what similarity search is not.

Usage:
    python3 query.py "why did monitoring stay green?"
    python3 query.py "..." --file-back
    python3 query.py --stats
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KB = ROOT / "knowledge"
INDEX = KB / "index.md"
ANSWERS = KB / "answers"
STATE = ROOT / "state.json"


def load_index() -> list[dict]:
    """Every row: link, category, summary, source, date. This is the whole
    retrieval surface — small enough to read entirely."""
    rows = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\[\[([^\]]+)\]\]\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m:
            rows.append({"link": m.group(1).strip(),
                         "category": m.group(2).strip(),
                         "summary": m.group(3).strip()})
    return rows


def select(question: str, rows: list[dict]) -> list[dict]:
    """STUB — replace with a model call that receives the question and the
    index and returns the links it chose.

    The stub scores summary-word overlap so the skeleton runs offline. A real
    implementation reasons over the summaries, which is why summary quality
    determines retrieval quality (see the card's Constraints).
    """
    stop = {"the", "a", "an", "did", "why", "what", "how", "is", "was", "in",
            "on", "and", "to", "of", "our", "we", "during"}
    terms = {w for w in re.findall(r"\w+", question.lower()) if w not in stop and len(w) > 2}
    scored = []
    for r in rows:
        words = set(re.findall(r"\w+", r["summary"].lower()))
        overlap = terms & words
        if overlap:
            scored.append((len(overlap), sorted(overlap), r))
    scored.sort(key=lambda t: -t[0])
    for n, matched, r in scored[:3]:
        r["why"] = f"matched on {', '.join(matched)}"
    return [r for _, _, r in scored[:3]]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("question", nargs="?")
    ap.add_argument("--file-back", action="store_true", help="file the answer back into the corpus")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    state = json.loads(STATE.read_text()) if STATE.exists() else {"query_count": 0}

    if args.stats:
        n_ans = len(list(ANSWERS.glob("*.md"))) if ANSWERS.exists() else 0
        print(f"queries run:   {state['query_count']}")
        print(f"filed answers: {n_ans}")
        if state["query_count"] == 0:
            print("\n  The source system's counter also stood at zero, for weeks,")
            print("  while the write path ran daily. See the card's Provenance.")
        return

    if not args.question:
        ap.error("a question is required (or --stats)")

    rows = load_index()
    print(f"index: {len(rows)} rows, read in full\n")

    chosen = select(args.question, rows)
    if not chosen:
        print("no documents selected — a vocabulary miss, which is this")
        print("pattern's accepted trade for inspectability.")
        return

    print("SELECTED — and you can see why, which similarity search cannot show:")
    for r in chosen:
        print(f"  {r['link']:<45} {r['why']}")

    print("\nOPENING only those documents:")
    total = 0
    for r in chosen:
        p = KB / f"{r['link']}.md"
        if p.exists():
            total += len(p.read_text(encoding="utf-8"))
            print(f"  {p.relative_to(KB)}")
        else:
            print(f"  {r['link']} -- BROKEN LINK (card 15 catches this)")
    print(f"\ncost: index ({INDEX.stat().st_size} B) + {len(chosen)} docs ({total} B),")
    print("not the whole corpus.")

    state["query_count"] += 1
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    if args.file_back:
        ANSWERS.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", args.question.lower()).strip("-")[:50]
        today = datetime.now(timezone.utc).date().isoformat()
        (ANSWERS / f"{slug}.md").write_text(
            f'---\ntitle: "{args.question}"\ncategory: answers\n'
            f'consulted: [{", ".join(r["link"] for r in chosen)}]\n'
            f'created: {today}\n---\n\n# {args.question}\n\n'
            f'[synthesized answer]\n\n## Consulted\n\n'
            + "".join(f"- [[{r['link']}]]\n" for r in chosen), encoding="utf-8")
        with INDEX.open("a", encoding="utf-8") as f:
            f.write(f"| [[answers/{slug}]] | answers | filed answer | query | {today} |\n")
        print(f"\nfiled back: answers/{slug} — indexed, so the base compounds")


if __name__ == "__main__":
    main()
