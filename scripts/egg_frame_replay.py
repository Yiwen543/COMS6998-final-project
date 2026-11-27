#!/usr/bin/env python3
"""Drive the full pinned frame adjuster through native Icarus and its frozen reference checker."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import tempfile

from m3_controller_replay import INPUTS, OUTPUTS, MAPPING, TOP, check_file


DRIVER = "public/driver.sv"
WRAPPER = "public/task_top_v3.sv"
CHECKER = "reference/frozen-v2/checker.py"
SOURCES = [WRAPPER, *sorted(f for f in MAPPING["sha256"] if f.startswith("public/rtl/"))]
MIN_TAIL = 128


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def scenarios():
    """Each action is one clock, in driver order reset, offer, data, last, data_ready, status_ready."""
    reset = (1, 0, 0, 0, 0, 0)
    quiet = (0, 0, 0, 0, 1, 1)

    def frames(lengths, tag, ready):
        actions = []
        for frame, length in enumerate(lengths, tag):
            for pos in range(length):
                data = (43 * frame + length * 3 + pos * 29 + pos * pos) % 256
                m, h = ready(len(actions))
                actions.append((0, 1, data, int(pos + 1 == length), int(m), int(h)))
        return actions

    def pressure(t):
        return t % 29 >= 13, t % 37 >= 22

    sweep = [reset] * 2 + frames(range(1, 13), 1, lambda _: (1, 1)) + [quiet] * 170
    lengths = [3, 4, 5, 7, 8, 9, 1, 12, 2, 10, 6, 11] * 2
    pressure_beats = frames(lengths, 21, pressure)
    pressure_tail = [(0, 0, 0, 0, *map(int, pressure(t)))
                     for t in range(len(pressure_beats), len(pressure_beats) + 55)]
    blocked = [reset] * 2 + pressure_beats + pressure_tail + [quiet] * 210

    # Accumulate complete transactions while neither sink drains, then accept a
    # prefix without TLAST. Reset discards both the queued replies and that prefix.
    pre = frames([4, 9, 3], 71, lambda _: (0, 0)) + [(0, 1, b, 0, 0, 0) for b in (0xA1, 0x02, 0xFE)]
    epoch = ([reset] * 2 + pre + [(0, 0, 0, 0, 0, 0)] * 8 + [reset] * 2 +
             frames([12, 1, 8, 4, 7], 111, pressure) + [quiet] * 176)
    return {"length_sweep": sweep, "backpressure": blocked, "reset_epoch": epoch}


def pin(word):
    # Decimal %0d prints x/z for a fully or partially unknown signal. Preserve
    # the text in the raw log; the public checker represents X/Z as -1.
    return -1 if word.lower() in ("x", "z") else int(word)


def parse_log(text, actions):
    pre, post, queue = [], [], []
    captures = {"PRE": pre, "POST": post, "QUEUE": queue}
    for line in text.splitlines():
        bits = line.split()
        if bits and bits[0] in captures:
            entries = captures[bits[0]]
            if int(bits[1]) != len(entries):
                raise ValueError(f"nonconsecutive {bits[0]} index")
            entries.append([pin(w) for w in bits[2:]])
    n = len(actions)
    if f"DRIVER_COMPLETE {n}" not in text.splitlines() or any(len(records) != n for records in captures.values()):
        raise ValueError("incomplete native driver log")
    rows = []
    pending = []
    head = 0
    for i, (before, after) in enumerate(zip(pre, post, strict=True)):
        pins = dict(zip(INPUTS, before[:len(INPUTS)], strict=True))
        rst, offer, data, last, mr, hr = actions[i]
        if (pins["rst"], pins["m_ready"], pins["h_ready"]) != (rst, mr, hr):
            raise ValueError(f"driver inputs differ from programmed schedule at edge {i}")
        if rst:
            pending.clear()
            head = 0
        elif offer:
            pending.append((data, last))
        present = head < len(pending)
        expected = pending[head] if present else (0, 0)
        if (pins["s_valid"], pins["s_data"], pins["s_last"]) != (int(present), *expected):
            raise ValueError(f"source changed or lost an offered beat at edge {i}")
        # The testbench pops on a definite transfer only. Its post-edge queue
        # counters let us distinguish an offered beat from an accepted beat.
        head += present and before[len(INPUTS)] == 1
        if queue[i] != [head, len(pending)]:
            raise ValueError(f"driver queue disagrees with observed handshake at edge {i}")
        rows.append({"cycle": i, "inputs": pins,
                     "pre": dict(zip(OUTPUTS, before[len(INPUTS):], strict=True)),
                     "post": dict(zip(OUTPUTS, after, strict=True))})
    return rows, queue[-1]


def coverage(rows):
    accepted_lengths, epochs, mid_resets = [], [], []
    counts = Counter()
    stalls = Counter()
    partial = complete = data_done = status_done = 0
    high_water = 0
    for row in rows:
        x, y = row["inputs"], row["pre"]
        if x["rst"]:
            if not row["cycle"] or not rows[row["cycle"]-1]["inputs"]["rst"]:
                if row["cycle"]:
                    mid_resets.append({"step": row["cycle"], "accepted_partial_length": partial,
                                       "input_complete": complete, "data_frames_consumed": data_done,
                                       "status_headers_consumed": status_done,
                                       "pre_m_valid": y["m_valid"], "pre_h_valid": y["h_valid"]})
                epochs.append({"first_reset": row["cycle"], "complete_input_lengths": []})
            partial = complete = data_done = status_done = 0
            continue
        input_fire = x["s_valid"] == y["s_ready"] == 1
        data_fire = y["m_valid"] == x["m_ready"] == 1
        hdr_fire = y["h_valid"] == x["h_ready"] == 1
        m_stall = y["m_valid"] == 1 and x["m_ready"] == 0
        h_stall = y["h_valid"] == 1 and x["h_ready"] == 0
        stalls["s_blocked"] += x["s_valid"] == 1 and y["s_ready"] == 0
        stalls["data_blocked"] += m_stall
        stalls["header_blocked"] += h_stall
        stalls["both_blocked"] += m_stall and h_stall
        stalls["header_fired_with_data_blocked"] += hdr_fire and m_stall
        stalls["data_fired_with_header_blocked"] += data_fire and h_stall
        counts["input_beats"] += input_fire
        counts["output_beats"] += data_fire
        counts["output_tlast_handshakes"] += data_fire and y["m_last"] == 1
        counts["header_handshakes"] += hdr_fire
        if input_fire:
            partial += 1
            if x["s_last"] == 1:
                accepted_lengths.append(partial)
                epochs[-1]["complete_input_lengths"].append(partial)
                complete += 1
                partial = 0
        data_done += data_fire and y["m_last"] == 1
        status_done += hdr_fire
        high_water = max(high_water, complete - min(data_done, status_done))
    quiet = 0
    for row in reversed(rows):
        x = row["inputs"]
        if (x["rst"], x["s_valid"], x["m_ready"], x["h_ready"]) != (0, 0, 1, 1):
            break
        quiet += 1
    return {"accepted_lengths": accepted_lengths, "epochs": epochs, "mid_resets": mid_resets,
            "completed_input_frames": len(accepted_lengths),
            "length_histogram": dict(sorted(Counter(accepted_lengths).items())),
            "handshakes": dict(counts), "stall_cycles": dict(stalls), "ready_high_quiet_tail": quiet,
            "max_complete_inputs_awaiting_data_or_header": high_water}


def run_suite(fixture, out, *, overrides=None):
    """Build from checked sources in isolation. overrides maps design paths to complete SV text."""
    fixture, out = Path(fixture).resolve(), Path(out).resolve()
    overrides = {} if overrides is None else overrides
    bad = set(overrides) - set(SOURCES)
    if bad or any(not isinstance(value, str) for value in overrides.values()):
        raise ValueError(f"expected complete text overrides of known design paths, got {sorted(bad)}")
    originals = {path: check_file(fixture, path) for path in (DRIVER, *SOURCES, CHECKER)}
    source = {path: overrides[path].encode() if path in overrides else data for path, data in originals.items()}
    checker = runpy.run_path(str(fixture / CHECKER))["check_rows"]
    out.mkdir(parents=True, exist_ok=False)
    report = {"upstream_commit": MAPPING["commit"], "fixture": MAPPING["fixture"],
              "sha256": {path: hashlib.sha256(data).hexdigest() for path, data in source.items()},
              "overrides": sorted(overrides), "physical_replays": 0, "min_tail": MIN_TAIL,
              "iverilog": subprocess.check_output(["iverilog", "-V"], text=True, stderr=subprocess.DEVNULL).splitlines()[0],
              "traces": {}}
    with tempfile.TemporaryDirectory() as work:
        work = Path(work)
        for name in (DRIVER, *SOURCES):
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(source[name])
        build = subprocess.run(["iverilog", "-g2012", "-s", TOP, "-o", "frame.vvp", DRIVER, *SOURCES],
                               cwd=work, capture_output=True, text=True, timeout=60)
        (out / "compile.log").write_text(build.stdout + build.stderr)
        build.check_returncode()
        for name, actions in scenarios().items():
            if len(actions) > 512:
                raise ValueError("schedule exceeds frozen driver's 512-row capacity")
            dest = out / name
            dest.mkdir()
            vectors = "".join(" ".join(map(str, action)) + "\n" for action in actions)
            (dest / "vectors.txt").write_text(vectors)
            res = subprocess.run(["vvp", work / "frame.vvp", "+VECTORS=vectors.txt"], cwd=dest,
                                 capture_output=True, text=True, timeout=60)
            (dest / "replay.log").write_text(res.stdout + res.stderr)
            res.check_returncode()
            rows, (head, tail) = parse_log(res.stdout, actions)
            raw = json.dumps(rows, separators=(",", ":")).encode() + b"\n"
            (dest / "rows.json.gz").write_bytes(gzip.compress(raw, mtime=0))
            verdict = checker(rows, require_drained=True, min_tail=MIN_TAIL)
            save(dest / "checker.json", verdict)
            report["traces"][name] = {"cycles": len(rows), "checker": verdict, "coverage": coverage(rows),
                                      "driver_unaccepted_at_end": tail-head,
                                      "rows_sha256": hashlib.sha256(raw).hexdigest(),
                                      "vectors_sha256": hashlib.sha256(vectors.encode()).hexdigest()}
            report["physical_replays"] += 1
    coverage_by_name = {name: record["coverage"] for name, record in report["traces"].items()}
    pressure = coverage_by_name["backpressure"]
    epoch = coverage_by_name["reset_epoch"]
    report["scenario_coverage"] = {
        "ordered_full_length_sweep": coverage_by_name["length_sweep"]["accepted_lengths"] == list(range(1, 13)),
        "source_stalls_and_multiple_frames_outstanding":
            pressure["stall_cycles"]["s_blocked"] > 0 and pressure["max_complete_inputs_awaiting_data_or_header"] > 1,
        "both_output_stalls_and_independent_transfers": all(pressure["stall_cycles"][key] > 0 for key in
            ("both_blocked", "header_fired_with_data_blocked", "data_fired_with_header_blocked")),
        "pending_outputs_and_partial_input_at_reset_then_postreset_frames":
            any(r["accepted_partial_length"] > 0 and r["pre_m_valid"] == r["pre_h_valid"] == 1
                for r in epoch["mid_resets"]) and len(epoch["epochs"]) > 1 and bool(epoch["epochs"][-1]["complete_input_lengths"]),
        "complete_input_delivery_and_quiet_tail": all(
            rec["driver_unaccepted_at_end"] == 0 and rec["coverage"]["ready_high_quiet_tail"] >= MIN_TAIL
            for rec in report["traces"].values()),
    }
    save(out / "summary.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True, help="pinned axis_length_fifo_v1 fixture")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    args = parser.parse_args()
    report = run_suite(args.fixture, args.output)
    outcomes = {key: value["checker"]["verdict"] for key, value in report["traces"].items()}
    print(json.dumps(outcomes))
    raise SystemExit(int(any(status != "PASS" for status in outcomes.values()) or
                         not all(report["scenario_coverage"].values())))
