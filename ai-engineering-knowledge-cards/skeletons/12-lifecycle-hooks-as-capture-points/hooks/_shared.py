"""Fail-open helpers. Nothing in here may ever raise."""
from __future__ import annotations
import json, time
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "hooks.log"
MAX_TURNS = 30
MAX_CHARS = 15_000


def log(hook: str, status: str, elapsed: float, detail: str = "") -> None:
    """Append one structured line. Swallows everything — a hook must never
    fail while recording its own failure."""
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"), "hook": hook,
                "status": status, "elapsed_ms": round(elapsed * 1000),
                "detail": detail,
            }) + "\n")
    except Exception:
        pass


def extract(text: str) -> tuple[str, int]:
    """Bound on BOTH axes, and truncate at a turn boundary so the output is
    never a fragment mid-sentence."""
    turns = [ln for ln in text.splitlines() if ln.strip()]
    recent = turns[-MAX_TURNS:]
    out = "\n".join(recent)
    if len(out) > MAX_CHARS:
        out = out[-MAX_CHARS:]
        nl = out.find("\n")
        if nl > 0:
            out = out[nl + 1:]
    return out, len(recent)
