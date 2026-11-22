"""Re-solve every target separately and physically replay each returned reset-to-hit prefix."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import time

from benchmark_m3_controller import ARMS, TRACES, digest, finite_samples, require, save
from m3_controller_replay import SCREEN, TOP, check_file, replay
from m3_controller_solver import FiniteTraceSolver


def audit(fixture, run, out):
    summary = json.loads((run / "summary.json").read_bytes())
    records = json.loads((run / "records.json").read_bytes())
    setup = summary["setup"]
    require(summary["complete"] and digest(records) == setup["records_sha256"],
            "incomplete run or changed original sample corpus")
    targets = json.loads(check_file(fixture, SCREEN / "egg-input.json"))["targets"]
    expected = json.loads((run / "answers.json").read_bytes())
    trials = [json.loads(row) for row in (run / "trials.jsonl").read_text().splitlines()]
    require(all(sum(row["arm"] == arm for row in trials) == summary["repeats"] for arm in ARMS)
            and all(row["answers_sha256"] == digest(expected) for row in trials),
            "recorded answers must agree with both measured arms")

    # An actual 148-call control. The paired benchmark never pays for these extra queries.
    samples, coordinates = finite_samples(records)
    solver = FiniteTraceSolver(samples, setup["timeout_ms_per_query"])
    start = time.perf_counter()
    answers = {}
    for target in targets:
        index = solver.first_hit(target["compact"])
        answers[target["id"]] = None if index is None else coordinates[index]
    elapsed = time.perf_counter() - start
    require(answers == expected, "unshared solves differ from normalized arms")
    by_prefix = defaultdict(list)
    for name, hit in answers.items():
        if hit is not None:
            by_prefix[tuple(hit)].append(name)
    simulator = run / "build" / "obj" / ("V" + TOP)
    evidence = []
    checked_edges = 0
    for (trace, cycle), ids in sorted(by_prefix.items()):
        # Replay the original actions from reset through the witness, with no future suffix.
        record = replay(fixture, simulator, trace, out / f"{trace}-{cycle}", cycles=cycle + 1)
        require(record["rows"] == records[trace]["rows"][:cycle + 1] and
                record["atom_rows"] == records[trace]["atom_rows"][:cycle + 1],
                "witness prefix disagrees with the measured RTL trajectory")
        require(cycle in record["eligible_cycles"] and
                all(record["rows"][cycle][record["target_ids"].index(name)] == "1" for name in ids),
                "solver-selected witness did not trigger its original target")
        checker = record["checker"]
        require(checker["verdict"] == "PASS" and not checker["failures"] and not checker["unknown"]
                and checker["checked_rows"] == cycle + 1, "prefix checker did not pass")
        checked_edges += cycle + 1
        evidence.append({"trace": trace, "cycle": cycle, "target_ids": ids,
                         "mapped_native_hits": {name: record["mapped_hits"][name] for name in ids},
                         "checked_edges": cycle + 1, "checker": checker,
                         "outputs_sha256": record["outputs_sha256"]})
    return {"scope": "Supplementary post-run validation on the fixed reset-to-cycle prefixes",
            "corpus": list(TRACES), "ungrouped_queries": len(answers), "ungrouped_solver_loop_s": elapsed,
            "timeout_ms_per_query": setup["timeout_ms_per_query"], "solver_unknowns": 0,
            "answers_sha256": digest(answers), "simulator_sha256": hashlib.sha256(simulator.read_bytes()).hexdigest(),
            "finite_hits_replayed": sum(map(len, by_prefix.values())),
            "finite_misses": sum(hit is None for hit in answers.values()), "prefix_replays": len(evidence),
            "checked_edges": checked_edges, "evidence": evidence}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        save(args.output / "summary.json", audit(args.fixture.resolve(), args.run.resolve(), args.output.resolve()))
    except Exception as error:
        save(args.output / "failure.json", {"error": repr(error)})
        raise
