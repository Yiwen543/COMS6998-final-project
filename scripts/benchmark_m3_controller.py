#!/usr/bin/env python3
"""Time guard-obligation sharing and original AXIS RTL replay on three fixed traces."""
import argparse
from collections import defaultdict
from functools import cache
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import time

from predicates import parse


TRACES = {"basic": 48, "boundary_pressure": 64, "reset_reuse": 64}
ARMS = ("structural", "indexed")
OBSERVATIONS = ("cycles", "eligible_cycles", "target_ids", "rows", "atom_ids", "atom_rows",
                "outputs_sha256", "raw_counters", "mapped_hits", "checker")
RULES = 281
TARGETS = 148


def require(test, message):
    if not test:
        raise ValueError(message)


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def structural_keys(payload):
    """Orient grounded equalities once; reduce actual ASTs bottom-up to fixed points."""
    @cache
    def boolean(tree):
        if isinstance(tree, str):
            return tree
        op = tree[0]
        args = tuple(boolean(child) for child in tree[1:])
        a = args[0]
        if op == "not":
            if a == "false":
                return "true"
            if isinstance(a, tuple):
                if a[0] == "not":
                    return a[1]
                # Both original De Morgan rules, in the same direction as egg.
                return ("and" if a[0] == "or" else "or", boolean(("not", a[1])), boolean(("not", a[2])))
        if op == "and":
            if a == "true":
                return args[1]
            if args[1] == "true":
                return a
        return (op, *args)

    @cache
    def order(tree):
        if isinstance(tree, str):
            return 1, tree
        children = [order(child) for child in tree[1:]]
        return 1 + sum(size for size, _ in children), "(" + " ".join([tree[0], *(s for _, s in children)]) + ")"

    # Retain all stated equalities, including multiple equal RHSs for one LHS.
    # Union only explicit endpoints; structural rewriting below builds no e-graph.
    parent = {}

    def root(term):
        while term in parent:
            if parent[term] in parent:
                parent[term] = parent[parent[term]]
            term = parent[term]
        return term

    for rule in payload["verified_rules"]:
        require(rule["proof_status"] == "unsat", f"uncertified rule {rule['name']}")
        left, right = [root(boolean(parse(rule[k]))) for k in ("left", "right")]
        if left != right:
            preferred, other = sorted((left, right), key=order)
            parent[other] = preferred

    @cache
    def rewrite(tree):
        tree = root(tree)
        if isinstance(tree, str):
            return tree
        normalized = boolean((tree[0], *(rewrite(child) for child in tree[1:])))
        return root(normalized)

    @cache
    def normal_form(tree):
        current = boolean(tree)
        seen = set()
        while current not in seen:
            seen.add(current)
            nxt = rewrite(current)
            if nxt == current:
                return current
            current = nxt
        raise ValueError("cyclic structural normalization; inconclusive")

    return [normal_form(parse(t["compact"])) for t in payload["targets"]]


def indexed_keys(payload, binary):
    job = subprocess.run([binary, "indexed"], input=json.dumps(payload).encode(),
                         capture_output=True, check=True, timeout=60)
    result = json.loads(job.stdout)
    timings = json.loads(job.stderr)
    require(timings["mode"] == "indexed", f"wrong egg mode {timings['mode']}")
    require(result["stop_reason"] == "Some(Saturated)", f"egg inconclusive: {result['stop_reason']}")
    require(result["ground_rule_count"] == RULES, "egg dropped certified rules")
    require([t["id"] for t in result["targets"]] == [t["id"] for t in payload["targets"]], "egg target IDs")
    return [t["eclass"] for t in result["targets"]], {
        "proof_edges": len(result["rewrite_explanations"]),
        "proof_sha256": digest(result["rewrite_explanations"]),
        "engine_timing": timings,
    }


def plan(targets, keys):
    # The corpus, eligible samples and earliest-hit objective are common. Each
    # atom is already fully instance-qualified by the frozen elaboration.
    groups = defaultdict(list)
    for target, key in zip(targets, keys, strict=True):
        context = (tuple(target["event_context"]), tuple(target["original_event_context"]), target["instance_scope"])
        groups[(context, key)].append(target)
    return list(groups.values())


def check_observation(record, ids, trace):
    require(record["cycles"] == TRACES[trace], f"truncated trace {trace}")
    require(record["eligible_cycles"] == list(range(1, TRACES[trace])), f"unexpected eligibility {trace}")
    require(record["target_ids"] == ids, f"unmatched physical targets {trace}")
    checker = record["checker"]
    require(checker["verdict"] == "PASS" and checker["checked_rows"] == TRACES[trace] and
            checker["failures"] == [] and checker["unknown"] == [], f"unqualified checker on {trace}: {checker}")
    require(len(record["atom_ids"]) == len(set(record["atom_ids"])) == 52, "invalid atom inventory")
    for rows, width in [(record["rows"], TARGETS), (record["atom_rows"], 52)]:
        require(len(rows) == TRACES[trace] and all(len(row) == width and set(row) <= {"0", "1"} for row in rows),
                f"invalid sampled truth {trace}")
    return {k: record[k] for k in OBSERVATIONS}


def finite_samples(records):
    samples, coordinates = [], []
    for name in TRACES:
        record = records[name]
        for cycle in record["eligible_cycles"]:
            coordinates.append([name, cycle])
            samples.append(dict(zip(record["atom_ids"], (v == "1" for v in record["atom_rows"][cycle]), strict=True)))
    require(len(coordinates) == 173, "wrong finite domain size")
    return samples, coordinates


def scan(records, ids):
    earliest = {target_id: None for target_id in ids}
    for name in TRACES:
        record = records[name]
        for cycle in record["eligible_cycles"]:
            for target_id, value in zip(ids, record["rows"][cycle], strict=True):
                if value == "1" and earliest[target_id] is None:
                    earliest[target_id] = [name, cycle]
    return earliest


def trial(arm, binary, fixture, simulator, folder, records, ids, timeout, state):
    from m3_controller_replay import replay
    from m3_controller_solver import FiniteTraceSolver
    start = time.perf_counter()
    payload = json.loads((fixture / "qualification/typed-v5/screen/egg-input.json").read_bytes())
    require(len(payload["verified_rules"]) == RULES and [t["id"] for t in payload["targets"]] == ids, "input changed")
    details = None
    if arm == "indexed":
        keys, details = indexed_keys(payload, binary)
    else:
        keys = structural_keys(payload)
    groups = plan(payload["targets"], keys)
    planned = time.perf_counter()
    samples, coords = finite_samples(records)
    solver = FiniteTraceSolver(samples, timeout_ms=timeout)
    answers = {}
    group_ids = []
    state["issued_queries"] = 0
    for members in groups:
        names = [t["id"] for t in members]
        group_ids.append(names)
        state["current_obligation"] = names[0]
        state["issued_queries"] += 1
        hit = solver.first_hit(members[0]["compact"])
        require(hit is None or 0 <= hit < len(coords), "out-of-domain solver witness")
        for name in names:
            answers[name] = coords[hit] if hit is not None else None
    require(state["issued_queries"] <= TARGETS, "solver call budget exceeded")
    state.pop("current_obligation")
    solved = time.perf_counter()
    fresh = {}
    for name in TRACES:
        fresh[name] = check_observation(replay(fixture, simulator, name, folder / name), ids, name)
    replayed = time.perf_counter()
    # Never grade with a rewritten guard: inspect every original target separately.
    oracle = scan(fresh, ids)
    require(answers == oracle, "canonical witness or finite miss differs from original RTL guard scan")
    require(fresh == records, "fresh RTL replay changed atom, guard, output, checker, or coverage observations")
    for members in group_ids:
        cols = [ids.index(name) for name in members]
        for record in fresh.values():
            require(all(len({record["rows"][cycle][col] for col in cols}) == 1
                        for cycle in record["eligible_cycles"]), f"full guard truth differs in reused group {members}")
    end = time.perf_counter()
    return {
        "arm": arm, "queries": state["issued_queries"], "avoided_vs_unique_target_calls": TARGETS - state["issued_queries"],
        "physical_replays": len(TRACES), "eligible_samples": len(coords), "groups": group_ids,
        "answers": answers, "engine": details, "wall_ms": (end - start) * 1000,
        "planning_ms": (planned - start) * 1000, "solving_ms": (solved - planned) * 1000,
        "replay_ms": (replayed - solved) * 1000, "grading_ms": (end - replayed) * 1000,
    }


def benchmark(args):
    from m3_controller_certificates import verify_rules
    from m3_controller_replay import build, replay
    out = args.output
    fixture = args.fixture.resolve()
    screen = fixture / "qualification/typed-v5/screen"
    start = time.perf_counter()
    certificate = verify_rules(screen)
    verified = time.perf_counter()
    ids = [t["id"] for t in json.loads((screen / "egg-input.json").read_bytes())["targets"]]
    require(len(ids) == len(set(ids)) == TARGETS, "unexpected original inventory")
    simulator = build(fixture, out / "build")
    built = time.perf_counter()
    records = {name: check_observation(replay(fixture, simulator, name, out / "common" / name), ids, name)
               for name in TRACES}
    acquired = time.perf_counter()
    oracle = scan(records, ids)
    scanned = time.perf_counter()
    save(out / "records.json", records)
    save(out / "certificate.json", certificate)
    setup = {"certify_ms": (verified - start) * 1000, "compile_ms": (built - verified) * 1000,
             "acquire_ms": (acquired - built) * 1000, "scan_only_ms": (scanned - acquired) * 1000,
             "records_sha256": digest(records), "input_sha256": hashlib.sha256((screen / "egg-input.json").read_bytes()).hexdigest(),
             "egg_binary_sha256": hashlib.sha256(args.binary.read_bytes()).hexdigest(), "timeout_ms_per_query": args.timeout_ms}
    save(out / "setup.json", setup)
    rows = []
    for repetition in range(args.repeats):
        order = ARMS if repetition % 2 == 0 else ARMS[::-1]
        for position, arm in enumerate(order):
            folder = out / f"trial-{repetition + 1}-{arm}"
            folder.mkdir()
            state = {"arm": arm, "trial": repetition + 1}
            try:
                row = trial(arm, args.binary.resolve(), fixture, simulator, folder, records, ids, args.timeout_ms, state)
            except Exception as exc:
                save(folder / "inconclusive.json", {**state, "error": repr(exc)})
                raise
            require(row["answers"] == oracle, "common observer differs from fresh replay")
            if repetition == 0:
                save(out / f"{arm}-groups.json", row["groups"])
            save(folder / "answers.json", row["answers"])
            row["groups_sha256"] = digest(row.pop("groups"))
            row["answers_sha256"] = digest(row.pop("answers"))
            row.update(trial=repetition + 1, position=position + 1)
            rows.append(row)
            with (out / "trials.jsonl").open("a") as handle:
                handle.write(json.dumps(row) + "\n")
    summary = {"complete": True, "repeats": args.repeats, "eligible_samples": 173, "targets": TARGETS,
               "finite_hits": sum(v is not None for v in oracle.values()), "finite_misses": sum(v is None for v in oracle.values()),
               "solver_unknowns": 0, "measurement_replays": len(rows) * len(TRACES), "setup_replays": len(TRACES),
               "setup": setup, "arms": {}}
    for arm in ARMS:
        arm_rows = [row for row in rows if row["arm"] == arm]
        require(len({row["groups_sha256"] for row in arm_rows}) == 1, "unstable normalization")
        summary["arms"][arm] = {
            "queries_per_trial": arm_rows[0]["queries"],
            "avoided_per_trial": arm_rows[0]["avoided_vs_unique_target_calls"],
            "groups_sha256": arm_rows[0]["groups_sha256"],
            "medians_ms": {k[:-3]: statistics.median(row[k] for row in arm_rows)
                           for k in ("wall_ms", "planning_ms", "solving_ms", "replay_ms", "grading_ms")},
        }
    summary["incremental_queries_saved_by_egg"] = (summary["arms"]["structural"]["queries_per_trial"] -
                                                   summary["arms"]["indexed"]["queries_per_trial"])
    save(out / "answers.json", oracle)
    save(out / "summary.json", summary)
    print(out / "summary.json")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fixture", required=True, type=Path, help="pinned axis_length_fifo_v1 directory")
    p.add_argument("--binary", required=True, type=Path, help="indexed guard_proofs_fast binary")
    p.add_argument("--output", required=True, type=Path, help="new result directory")
    p.add_argument("--timeout-ms", default=2000, type=int)
    p.add_argument("--repeats", default=6, type=int)
    args = p.parse_args()
    if min(args.repeats, args.timeout_ms) < 1:
        p.error("repeats and timeout must be positive")
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        benchmark(args)
    except Exception as exc:
        save(args.output / "failure.json", {"complete": False, "error": repr(exc)})
        raise
