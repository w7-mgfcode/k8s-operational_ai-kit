"""A small stand-in for the loop's command-line tool, with three subcommands.

    python3 loop_tool.py init   --state S --task T
    python3 loop_tool.py sprint --state S --id X
    python3 loop_tool.py record --state S --result pass|fail
    python3 loop_tool.py gate   --state S

Its gate is honest: it reports pending until a result is recorded, then that result.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "sprint", "record", "gate"):
        p = sub.add_parser(name)
        p.add_argument("--state", required=True)
    sub.choices["init"].add_argument("--task", required=True)
    sub.choices["sprint"].add_argument("--id", required=True)
    sub.choices["record"].add_argument("--result", required=True, choices=["pass", "fail"])
    a = ap.parse_args()
    path = Path(a.state)
    state = json.loads(path.read_text()) if path.exists() else {"results": [], "sprint": None}
    if a.cmd == "init":
        state = {"task": a.task, "results": [], "sprint": None}
        out = {"status": "initialized"}
    elif a.cmd == "sprint":
        state["sprint"] = a.id
        out = {"sprint": a.id}
    elif a.cmd == "record":
        state["results"].append(a.result)
        out = {"recorded": a.result, "count": len(state["results"])}
    else:
        if not state["sprint"]:
            print(json.dumps({"error": "no active sprint"}))
            return 1
        out = {"gate": state["results"][-1] if state["results"] else "pending"}
    path.write_text(json.dumps(state))
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
