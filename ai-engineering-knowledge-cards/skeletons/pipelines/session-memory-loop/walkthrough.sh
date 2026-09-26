#!/usr/bin/env bash
# Sequential walkthrough of the session-memory engine: cards 12 -> 13 -> 14 -> 15.
#
# Each stage runs the card's own modular skeleton, in place, in order. Nothing is
# reimplemented here — this script is the wiring diagram, executable.
#
# Runs are idempotent: every artifact written is removed on exit, so the tree
# is as clean afterwards as it was before. Pass --keep to inspect what was made.
#
# Usage:  ./walkthrough.sh          run all stages, clean up
#         ./walkthrough.sh 13       run one stage
#         ./walkthrough.sh --keep   run all stages, leave the artifacts
set -u

SK="$(cd "$(dirname "$0")/../.." && pwd)"
C12="$SK/12-lifecycle-hooks-as-capture-points"
C13="$SK/13-log-as-source-compilation"
C14="$SK/14-index-guided-retrieval"
C15="$SK/15-structural-lint"

KEEP=0
[ "${1:-}" = "--keep" ] && { KEEP=1; shift; }

rule() { printf '\n\033[1m── %s ──\033[0m\n' "$1"; }
note() { printf '   %s\n' "$1"; }

# Everything the run creates. Removed on exit unless --keep.
cleanup() {
  [ "$KEEP" = "1" ] && { printf '\n   (--keep: artifacts left in place)\n'; return; }
  rm -f "$C12"/daily/*.md "$C12"/hooks.log "$C12"/last-flush.json \
        "$C13"/daily/2*-*-*.md "$C14"/state.json "$C15"/lint-state.json 2>/dev/null
  # the seed source for card 13 is committed; restore it if we clobbered it
  git -C "$SK" checkout -- 13-log-as-source-compilation/daily 2>/dev/null || true
  printf '\n   (cleaned up — tree restored)\n'
}
trap cleanup EXIT

stage12() {
  rule "CARD 12 — capture at the session boundary"
  note "A hook extracts the transcript and appends it. Fail-open, no model call."
  printf 'user: the sync operator stopped reconciling after we enabled TLS\nassistant: it has no CA in its trust bundle. distribute the CA cluster-wide\nrather than mounting it per client, because every client needs it. note that\nrunning workloads keep their credentials and only fail on restart.\n' \
    | python3 "$C12/hooks/session_end.py" --daily-dir "$C13/daily"
  note "Source is append-only. The compiler's hash is meaningful because of that."
}

stage13() {
  rule "CARD 13 — compile source into a knowledge base"
  note "Content hash decides what compiles. Unchanged source costs nothing."
  ( cd "$C13" && python3 compile.py --dry-run --ignore-hour )
  note "The model call is stubbed. The incremental machinery is what this shows."
}

stage14() {
  rule "CARD 14 — retrieve by reading the index, not the corpus"
  ( cd "$C14" && python3 query.py "which faults only surface on restart?" )
  note "Selection is inspectable: you can read which documents it chose and why."
}

stage15() {
  rule "CARD 15 — lint the relationships the other stages created"
  ( cd "$C15" && python3 lint.py --base "$C13/knowledge" )
  note "Errors block. Warnings inform. No model needed for any of it."
}

case "${1:-all}" in
  12|1) stage12 ;;
  13|2) stage13 ;;
  14|3) stage14 ;;
  15|4) stage15 ;;
  all)  stage12; stage13; stage14; stage15
        rule "LOOP CLOSED"
        note "capture -> compile -> retrieve -> lint, and a filed answer re-enters"
        note "the corpus as source for the next compilation." ;;
  *) echo "usage: $0 [12|13|14|15|all]" >&2; exit 2 ;;
esac
