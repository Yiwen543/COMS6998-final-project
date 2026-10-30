#!/usr/bin/env python3
"""Rebuild every saved prompt's feedback boundary from its own prior run."""
from __future__ import annotations

import argparse
import json

from coverage import load
from run_midterm_fixed import ROOT, sha
from run_sfifo_stress_fixed import SOURCE
from sfifo_fixture import validate_actions
from sfifo_stress_feedback import messages_for
from token_placebo import NEUTRAL_PREFIX


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default="results/sfifo_stress_abpc_frozen_live_20261030")
    args = parser.parse_args()
    run = (ROOT / args.run).resolve()
    config = json.loads((run / "config.json").read_text())
    frozen = json.loads((ROOT / "docs/sfifo-stress-frozen-pilot-2026-10-30.json").read_text())
    mismatched = [name for name, expected in frozen["files_sha256"].items()
                  if sha(ROOT / name) != expected]
    if mismatched:
        raise AssertionError(f"Frozen hash mismatch: {mismatched}")
    screen = json.loads((ROOT / "results/midterm_candidate_preflight/sfifo-stress/screen.json").read_text())
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    if len(calls) != config["repetitions"] * config["rounds"] * len(config["arms"]):
        raise AssertionError("Unexpected model call count; retry-aware audit needed")
    rel = str(SOURCE.relative_to(ROOT))
    count_rows = [json.loads(line) for line in (run / "placebo-token-counts.jsonl").read_text().splitlines()]
    counts = {(x["repetition"], x["round"], x["attempt"]): x for x in count_rows}
    checked = 0
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            folder = run / arm / f"rep{rep}"
            history = []
            prior = json.loads((folder / "seed.json").read_text())
            previous_name = "seed"
            semantic = json.loads((folder / "semantic.json").read_text()) if arm in ("P", "C") else None
            for round_no in range(1, config["rounds"] + 1):
                call = next(x for x in calls if (x["arm"], x["repetition"], x["round"]) ==
                            (arm, rep, round_no))
                if call["requested_model"] != config["model"] or call["returned_model"] != config["model"]:
                    raise AssertionError("Requested/returned model mismatch")
                if call["attempt"] != 1 or not call.get("accepted"):
                    raise AssertionError("Unexpected failed/retried call")
                saved = json.loads((run / call["prompt"]).read_text())
                actual = json.loads(saved[1]["content"])
                points = load(folder / f"{previous_name}.dat", rel, include_descendants=True)
                log = (folder / f"{previous_name}.sim.log").read_text()
                expected = json.loads(messages_for("C" if arm == "P" else arm,
                    history, prior, log, points, semantic, screen if semantic else None,
                    round_no, config["max_new_cycles"])[1]["content"])
                if arm == "P":
                    del expected["egg_normalization"]
                    filler = actual.pop("neutral_token_matched_appendix", None)
                    if (not isinstance(filler, str) or
                            not filler.startswith(NEUTRAL_PREFIX) or
                            any(chunk != "x" for chunk in filler[len(NEUTRAL_PREFIX):].split())):
                        raise AssertionError("Placebo filler contains unexpected content")
                    count = counts[(rep, round_no, 1)]
                    if (count["absolute_delta"] > config["placebo_tolerance_tokens"] or
                            call["usage"]["input_tokens"] != count["placebo_input_tokens"]):
                        raise AssertionError("Placebo input-token mismatch")
                if actual != expected:
                    raise AssertionError(f"Feedback or own-history mismatch: {arm} rep{rep} round{round_no}")
                if "calibration" in saved[1]["content"].lower():
                    raise AssertionError("Calibration leakage into prompt")
                actions = validate_actions({"actions": call["actions"]}, config["max_new_cycles"],
                                           require_initial_reset=False)
                history.extend(actions)
                previous_name = f"round{round_no}-attempt1"
                prior = json.loads((folder / f"{previous_name}.json").read_text())
                checked += 1
    result = {"status": "passed", "frozen_file_hashes_checked": len(frozen["files_sha256"]),
              "generation_calls_checked": checked,
              "placebo_count_rows_checked": len(count_rows),
              "scope": "own-trajectory prompt reconstruction, A/B/C/P isolation, raw and egg evidence, legal actions, model IDs, exact P usage and no calibration text"}
    (run / "boundary-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
