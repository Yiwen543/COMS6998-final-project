#!/usr/bin/env python3
"""Compare fresh-process indexed guard proofs to the frozen v1 spanning binary."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import time


MODES = ("spanning", "indexed")
STAGES = ("build", "saturation", "extraction", "explanation", "serialization", "total")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def json_file(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def equivalent_source_pairs(inputs, outputs):
    """Only the arbiter profile format declares a source/alternate pairing."""
    groups = {}
    for target, result in zip(inputs, outputs):
        name = target.get("source_target")
        if not isinstance(name, str):
            continue
        for form in ("source", "alternate"):
            if target["id"] == f"{name}/{form}":
                group = groups.setdefault(name, {})
                if form in group:
                    raise ValueError(f"duplicate {form} for {name}")
                group[form] = result["eclass"]
    if not groups:
        return None
    if any(len(group) != 2 for group in groups.values()):
        raise ValueError("incomplete source/alternate guard pair")
    return {
        "matched": sum(g["source"] == g["alternate"] for g in groups.values()),
        "total": len(groups),
    }


def observe(binary, mode, payload, expected_ids, rule_count, reference, directory, tag):
    stdout = stderr = b""
    try:
        start = time.perf_counter_ns()
        process = subprocess.run([binary, mode], input=payload, capture_output=True, timeout=60)
        wall_ms = (time.perf_counter_ns() - start) / 1e6
        stdout, stderr = process.stdout, process.stderr
        process.check_returncode()
        report = json.loads(stdout)
        timings = json.loads(stderr)
        if timings["mode"] != mode:
            raise ValueError(f"engine identified mode {timings['mode']!r}, expected {mode!r}")
        if report["stop_reason"] != "Some(Saturated)":
            raise ValueError(f"inconclusive stop {report['stop_reason']}")
        if [t["id"] for t in report["targets"]] != expected_ids:
            raise ValueError("target IDs or order differ from input")
        if report["ground_rule_count"] != rule_count:
            raise ValueError("ground rule count differs from input")
        if reference is None:
            (directory / "reference.json").write_bytes(stdout)
        report.pop("saturation_seconds")
        if reference is not None and report != reference:
            keys = sorted(k for k in reference.keys() | report.keys()
                          if k not in report or k not in reference or reference[k] != report[k])
            raise ValueError("output differs from v1 in " + ", ".join(keys))
        values = {"wall_ms": wall_ms}
        for stage in STAGES:
            seconds = timings[stage + "_seconds"]
            if not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds < 0:
                raise ValueError(f"invalid {stage} duration {seconds!r}")
            values[stage + "_ms"] = seconds * 1000
        return report, values
    except (ValueError, TypeError, KeyError, OSError, subprocess.SubprocessError) as exc:
        if isinstance(exc, subprocess.TimeoutExpired):
            stdout, stderr = exc.stdout or b"", exc.stderr or b""
        (directory / f"{tag}.stdout").write_bytes(stdout)
        (directory / f"{tag}.stderr").write_bytes(stderr)
        json_file(directory / "failure.json", {"observation": tag, "error": str(exc)})
        raise SystemExit(f"{directory}/{tag}: {exc}") from exc


def benchmark(index, path, binaries, repeats, out):
    directory = out / f"profile-{index}"
    directory.mkdir()
    payload = path.read_bytes()
    inputs = json.loads(payload)
    ids = [t["id"] for t in inputs["targets"]]
    rule_count = len(inputs["verified_rules"])
    info = {"profile": directory.name, "input": str(path), "sha256": sha256(payload),
            "targets": len(ids), "ground_rules": rule_count}
    json_file(directory / "input.json", info)
    reference = None
    for mode in MODES:
        report, _ = observe(binaries[mode], mode, payload, ids, rule_count,
                            reference, directory, f"warmup-{mode}")
        if mode == "spanning":
            reference = report
    pairs = []
    with (directory / "trials.jsonl").open("x") as stream:
        for trial in range(repeats):
            order = MODES if trial % 2 == 0 else MODES[::-1]
            pair = {}
            for position, mode in enumerate(order):
                _, durations = observe(binaries[mode], mode, payload, ids, rule_count,
                                       reference, directory, f"trial-{trial + 1}-{mode}")
                row = {"trial": trial + 1, "position": position + 1, "mode": mode, **durations}
                stream.write(json.dumps(row) + "\n")
                stream.flush()
                pair[mode] = durations
            pairs.append(pair)
    medians = {mode: {key: statistics.median(pair[mode][key] for pair in pairs)
                      for key in pairs[0][mode]} for mode in MODES}
    deltas = [pair["spanning"]["wall_ms"] - pair["indexed"]["wall_ms"] for pair in pairs]
    return {
        **info, "proof_edges": len(reference["rewrite_explanations"]),
        "source_pairs": equivalent_source_pairs(inputs["targets"], reference["targets"]),
        "matched_runs": 2 * repeats, "medians": medians,
        "paired_wall_wins": {"indexed": sum(v > 0 for v in deltas),
                             "spanning": sum(v < 0 for v in deltas), "ties": deltas.count(0)},
        "median_paired_ms_saved": statistics.median(deltas),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-binary", required=True, type=Path,
                        help="pristine fast-v1 guard_proofs_fast executable")
    parser.add_argument("--binary", required=True, type=Path, help="candidate guard_proofs_fast")
    parser.add_argument("--input", required=True, type=Path, action="append")
    parser.add_argument("--output", required=True, type=Path, help="new results directory")
    parser.add_argument("--repeats", type=int, default=12)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    binaries = {"spanning": args.baseline_binary.resolve(), "indexed": args.binary.resolve()}
    args.output.mkdir(parents=True, exist_ok=False)
    summary = {"repeats": args.repeats, "binary_sha256": {m: sha256(p.read_bytes())
                                                          for m, p in binaries.items()},
               "complete": False, "profiles": []}
    summary_path = args.output / "summary.json"
    json_file(summary_path, summary)
    for index, path in enumerate(args.input):
        summary["profiles"].append(benchmark(index, path, binaries, args.repeats, args.output))
        json_file(summary_path, summary)
    summary["complete"] = True
    json_file(summary_path, summary)
    print(summary_path)


if __name__ == "__main__":
    main()
