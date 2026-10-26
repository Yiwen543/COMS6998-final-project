#!/usr/bin/env python3
"""Run a blinded then unblinded, read-only Claude Code audit of a queue pilot.

Coverage and checker measurements remain those of the frozen simulator. The
reviewer can report discrepancies, but its opinion never changes counters.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from prepare_claude_queue_audit import prepare


ROOT = Path(__file__).resolve().parents[1]
MODEL = "claude-opus-5-5"


def invoke(prompt: str, output: Path, tools: str, budget: str, timeout: int) -> dict:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY missing from environment")
    command = ["claude", "--bare", "--print", "--model", MODEL,
               "--no-session-persistence", "--permission-mode", "dontAsk",
               "--tools", tools, "--max-budget-usd", budget,
               "--output-format", "json"]
    started = time.perf_counter()
    process = subprocess.run(command, input=prompt, text=True, capture_output=True,
                             cwd=ROOT, timeout=timeout, check=False)
    response = {"requested_model": MODEL, "command": command,
                "returncode": process.returncode,
                "wall_seconds": round(time.perf_counter() - started, 3),
                "stdout": process.stdout, "stderr": process.stderr}
    output.write_text(json.dumps(response, indent=2) + "\n", encoding="utf-8")
    if process.returncode:
        raise RuntimeError(f"Claude Code exited {process.returncode}; see {output}")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Claude Code did not return JSON; see {output}") from exc
    if payload.get("is_error"):
        raise RuntimeError(f"Claude Code reported an error; see {output}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-budget-usd", default="3.00")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    packet = prepare(source)
    (output / "blind-packet.json").write_text(json.dumps(packet, indent=2) + "\n")
    blind_prompt = (
        "Review this anonymous X/Y matched RTL-verification pilot as a skeptical "
        "methodologist. Recompute target costs from the cumulative rows. Compare "
        "X and Y within each fixed RTL version on line/branch/toggle coverage, "
        "API tokens, cycles, and simulator executions. Identify any arithmetic "
        "discrepancy, ceiling effect, uncertainty, or limitation. Do not infer "
        "which label received semantic feedback. Do not claim statistical significance. "
        "The packet alone cannot establish checker validity or feedback isolation. "
        "Return concrete findings and a concise verdict.\n\n"
        + json.dumps(packet, separators=(",", ":"))
    )
    (output / "blind-prompt.txt").write_text(blind_prompt)
    blind = invoke(blind_prompt, output / "blind-response.json", "",
                   args.max_budget_usd, args.timeout_seconds)
    (output / "blind-review.txt").write_text(str(blind.get("result", "")) + "\n")

    reveal_prompt = f"""You are independently auditing a completed RTL-verification pilot.
The previously hidden mapping is X=B (raw coverage) and Y=C (the same raw
coverage plus bounded egg-normalized equivalent activation guards). Stage 1 is
saved at {output / 'blind-review.txt'}. Do not change any file.

Inspect the frozen artifacts under {source}, plus:
- {ROOT / 'configs/queue_bc_pilot_gpt6sol.json'}
- {ROOT / 'scripts/queue_feedback.py'}
- {ROOT / 'scripts/run_queue_bc_pilot.py'}
- {ROOT / 'examples/heldout_queue/docs/specification.md'}
- {ROOT / 'examples/heldout_queue/verif/tb_queue_pilot.sv'}
- {ROOT / 'docs/heldout_queue_preflight.md'}

Check: (1) within-version DUT/checker/driver/seed/budget equality; (2) raw
coverage-array identity in corresponding B/C prompts and absence of solver
witnesses/reference vectors; (3) typed full guards, source spans, two-state
rewrite proof and separation of read/write behavior; (4) token/retry and replay
cycle/execution accounting; (5) reported C-versus-B result, target attainment,
and its limitations. Cite paths and exact rows for discrepancies. Distinguish
things you inspected from things you could not inspect. Treat checker failure
as a possible DUT defect, not automatically a test failure. The simulator's
saved counters and a separate replay are ground truth; your narrative is an
audit, not a coverage oracle. Return a concise structured audit with each
finding marked supported, discrepancy, or unresolved. Do not run commands or
edit files.
"""
    (output / "reveal-prompt.txt").write_text(reveal_prompt)
    reveal = invoke(reveal_prompt, output / "reveal-response.json", "Read,Glob,Grep",
                    args.max_budget_usd, args.timeout_seconds)
    (output / "reveal-review.txt").write_text(str(reveal.get("result", "")) + "\n")
    print(f"Claude Code audit saved: {output}")


if __name__ == "__main__":
    main()
