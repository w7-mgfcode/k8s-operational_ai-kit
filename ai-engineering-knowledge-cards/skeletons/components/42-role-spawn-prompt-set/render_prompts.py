"""Render a role's spawn prompt and lint the prompt set against the skill's phase table.

    python3 render_prompts.py --lint                         # four kinds of finding
    python3 render_prompts.py --role evaluator --context context_full.json
    python3 render_prompts.py --role evaluator --context context_partial.json
    python3 render_prompts.py --role evaluator --context context_partial.json --strict

Exit codes: 0 = rendered clean, 1 = a finding was shown on purpose, 2 = arguments needed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASES = json.loads((HERE / "phases.json").read_text(encoding="utf-8"))
SLOT = re.compile(r"\{(\w+)\}")


def spawn_subagent(kind: str, prompt: str) -> None:
    """Stands where the component calls the agent tool; prints instead."""
    print(f"[stub] spawn_subagent(type={kind!r}) with a {len(prompt)}-character prompt")


def load(role: str) -> str:
    return (HERE / "prompts" / PHASES["phases"][role]["prompt"]).read_text(encoding="utf-8")


def render(role: str, context: dict, strict: bool) -> int:
    template = load(role)
    unfilled = sorted(set(SLOT.findall(template)) - set(context))
    prompt = SLOT.sub(lambda m: str(context.get(m.group(1), m.group(0))), template)
    print(prompt)
    if unfilled and strict:
        print(f"REFUSED: slots left unfilled: {', '.join(unfilled)}")
        return 1
    spawn_subagent(PHASES["spawn_type"], prompt)
    if unfilled:
        print(f"note: {', '.join(unfilled)} went out as literal text; the component has no check for this")
    return 0


def lint() -> int:
    found = 0
    for role, spec in PHASES["phases"].items():
        text = load(role)
        read = {Path(p).name for p in re.findall(r"references/([\w./-]+\.md)", text)}
        for need in spec["must_load"]:
            if need not in read:
                print(f"{role}: the phase table requires {need}; the prompt never asks for it")
                found += 1
        for p in sorted(read):
            if not (HERE / "workspace" / "references" / p).exists() and (HERE / "skill" / "references" / p).exists():
                print(f"{role}: 'references/{p}' exists under the skill, not under the workspace the agent starts in")
                found += 1
        for slot, phrase in PHASES["slots_given_forbidden_use"].items():
            if "{" + slot + "}" in text and phrase.lower() in text.lower():
                print(f"{role}: is handed the {slot} and told '{phrase}'")
                found += 1
        extra = set(PHASES["harness_tools"]) - set(PHASES["role_tools"][role])
        if extra:
            print(f"{role}: spawned as {PHASES['spawn_type']}, so it holds {len(extra)} tools its role list omits")
            found += 1
    print(f"{found} findings")
    return 1 if found else 0


def main(argv: list) -> int:
    if not argv or argv == ["--lint"]:
        return lint()
    if argv[0] == "--role" and "--context" in argv:
        role = argv[1]
        ctx = json.loads((HERE / argv[argv.index("--context") + 1]).read_text(encoding="utf-8"))
        return render(role, ctx, "--strict" in argv)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
