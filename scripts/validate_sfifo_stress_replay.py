#!/usr/bin/env python3
"""Compare every original FIFO DUT counter and checker on live vs replay."""
import argparse
import json

from coverage import load
from pilot_feedback import point_id
from run_sfifo_stress_fixed import ROOT, SOURCE


def indexed(path, source):
    return {point_id(point): point["hits"] for point in load(path, source, include_descendants=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", default="results/sfifo_stress_abpc_frozen_live_20261030")
    parser.add_argument("--replay", default="results/sfifo_stress_abpc_frozen_replay_20261030")
    args = parser.parse_args()
    live = (ROOT / args.live).resolve()
    replay = (ROOT / args.replay).resolve()
    config = json.loads((live / "config.json").read_text())
    rel = str(SOURCE.relative_to(ROOT))
    compared = 0
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            for name in ["seed", *(f"round{r}-attempt1" for r in range(1, config["rounds"] + 1))]:
                first, second = live / arm / f"rep{rep}", replay / arm / f"rep{rep}"
                if indexed(first / f"{name}.dat", rel) != indexed(second / f"{name}.dat", rel):
                    raise AssertionError(f"Original DUT coverage mismatch: {arm} rep{rep} {name}")
                original = json.loads((first / f"{name}.json").read_text())
                reproduced = json.loads((second / f"{name}.json").read_text())
                if original["checker"] != reproduced["checker"] or original["coverage"] != reproduced["coverage"]:
                    raise AssertionError(f"Checker/coverage summary mismatch: {arm} rep{rep} {name}")
                compared += 1
    result = {"status": "matched", "comparisons": compared,
              "scope": "every original DUT source point and hit count, checker and coverage summary; replay has no model calls",
              "live": str(live.relative_to(ROOT)), "replay": str(replay.relative_to(ROOT))}
    (replay / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
