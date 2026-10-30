#!/usr/bin/env python3
"""Compare live and offline replay's original DUT counters and checker rows."""
import argparse
import json

from coverage import load
from pilot_feedback import point_id
from run_divider_fixed import ROOT, SOURCE


def indexed(path, source):
    return {point_id(point): point["hits"] for point in load(path, source, include_descendants=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", default="results/divider_abcp_frozen_live_20261030")
    parser.add_argument("--replay", default="results/divider_abcp_frozen_replay_20261030")
    args = parser.parse_args()
    live = (ROOT / args.live).resolve()
    replay = (ROOT / args.replay).resolve()
    rel = str(SOURCE.relative_to(ROOT))
    compared = 0
    for arm in "ABPC":
        for rep in range(1, 4):
            for name in ["seed", *(f"round{r}-attempt1" for r in range(1, 5))]:
                base = (live / arm / f"rep{rep}"), (replay / arm / f"rep{rep}")
                if indexed(base[0] / f"{name}.dat", rel) != indexed(base[1] / f"{name}.dat", rel):
                    raise AssertionError(f"Coverage counter mismatch: {arm} rep{rep} {name}")
                original = json.loads((base[0] / f"{name}.json").read_text())
                reproduced = json.loads((base[1] / f"{name}.json").read_text())
                if original["checker"] != reproduced["checker"] or original["coverage"] != reproduced["coverage"]:
                    raise AssertionError(f"Checker/summary mismatch: {arm} rep{rep} {name}")
                compared += 1
    result = {"status": "matched", "comparisons": compared,
              "scope": "60 seed/round simulations; every original DUT point and hit count, checker and coverage summary",
              "live": str(live.relative_to(ROOT)), "replay": str(replay.relative_to(ROOT))}
    (replay / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
