#!/usr/bin/env python3
"""Run the six frozen full-frame AXI faults on common stimuli and preserve native observations."""
import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

from m3_controller_replay import MAPPING, check_file


ADJUSTER = "public/rtl/axis_frame_length_adjust.v"
WRAPPER = "public/rtl/axis_frame_length_adjust_fifo.v"
TRACES = ("length_sweep", "backpressure", "reset_epoch")
DEVELOPMENT = ("original", "F02", "F05")
HELD_OUT = ("F01", "F03", "F04", "F06")
VERDICTS = ("PASS", "FAIL", "UNRESOLVED", "INVALID_INPUT")
# Category names from the independent frozen-v2 checker, including categories with zero events.
CATEGORIES = (
    "assumption_violation", "completion", "completion_unresolved", "data_last", "data_payload",
    "data_premature", "data_spurious", "data_stability", "data_unresolved", "drain_tail_short",
    "malformed", "no_initial_reset", "out_of_scope", "reset_clear", "status_payload",
    "status_premature_or_spurious", "status_stability", "status_unresolved",
    "x_input", "x_payload", "x_reset", "x_transfer", "x_valid",
)


@dataclass(frozen=True)
class Fault:
    id: str
    change: str
    source: str
    line: int
    before: str
    after: str


FAULTS = (
    Fault("F01", "Fill inserted pad bytes with ones", ADJUSTER, 398,
          "m_axis_tdata_int = {DATA_WIDTH{1'b0}};", "m_axis_tdata_int = {DATA_WIDTH{1'b1}};"),
    Fault("F02", "Flag an exact-maximum frame as truncated in TRANSFER", ADJUSTER, 338,
          "status_frame_truncate_next = word_cnt > long_counter_reg;",
          "status_frame_truncate_next = word_cnt >= long_counter_reg;"),
    Fault("F03", "Suppress the final TLAST when emitting a truncated frame", ADJUSTER, 447,
          "m_axis_tlast_int = s_axis_tlast;", "m_axis_tlast_int = 1'b0;"),
    Fault("F04", "Count an offered byte during stalled TRANSFER", ADJUSTER, 171,
          "frame_ptr_next = frame_ptr_reg;",
          "frame_ptr_next = frame_ptr_reg + ((state_reg == STATE_TRANSFER && s_axis_tvalid && !s_axis_tready) ? 16'd1 : 16'd0);"),
    Fault("F05", "Consume the header FIFO using the data sink ready", WRAPPER, 228,
          ".m_axis_tready(m_axis_hdr_ready),", ".m_axis_tready(m_axis_tready),"),
    Fault("F06", "Disconnect synchronous reset on the header FIFO", WRAPPER, 214,
          ".rst(rst),", ".rst(1'b0),"),
)
DESIGNS = ("original", *(f.id for f in FAULTS))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def hashbytes(data):
    return hashlib.sha256(data).hexdigest()


def edit(fixture, fault):
    source = check_file(fixture, fault.source).decode()
    lines = source.splitlines(keepends=True)
    original = lines[fault.line - 1]
    require(original.strip() == fault.before, f"{fault.id}: frozen RTL anchor no longer matches")
    lines[fault.line - 1] = original.replace(fault.before, fault.after)
    return "".join(lines)


def counts(events):
    actual = Counter(e["category"] for e in events)
    require(set(actual) <= set(CATEGORIES), f"unclassified reference categories {set(actual) - set(CATEGORIES)}")
    return {category: actual[category] for category in CATEGORIES}


def load_corpus(directory):
    """Offline scoring data keyed by (design_id, trace_name). Each value has rows and checker."""
    directory = Path(directory)
    summary = json.loads((directory / "summary.json").read_text())
    raw = directory / "observations.jsonl.gz"
    require(summary["complete"] and hashbytes(raw.read_bytes()) == summary["corpus_sha256"], "incomplete or changed corpus")
    corpus = {}
    with gzip.open(raw, "rt") as stream:
        for line in stream:
            case = json.loads(line)
            key = (case.pop("design"), case.pop("trace"))
            require(key not in corpus, f"duplicate observation {key}")
            corpus[key] = case
    require(set(corpus) == {(d, t) for d in DESIGNS for t in TRACES}, "missing/extra observation case")
    return corpus


def collect(args):
    from egg_frame_replay import CHECKER, DRIVER, SOURCES, run_suite
    from runpy import run_path

    fixture, out = args.fixture.resolve(), args.output.resolve()
    checker_path = "reference/frozen-v2/checker.py"
    check_file(fixture, checker_path)
    check_rows = run_path(str(fixture / checker_path))["check_rows"]
    sources = {name: hashbytes(check_file(fixture, name)) for name in MAPPING["sha256"] if name.startswith("public/rtl/")}
    by_id = {f.id: f for f in FAULTS}
    manifest = {
        "upstream_commit": MAPPING["commit"], "original_sources": sources,
        "checker": {"source": checker_path, "sha256": MAPPING["sha256"][checker_path]},
        "faults": [{**asdict(f), "variant_sha256": hashbytes(edit(fixture, f).encode())} for f in FAULTS],
        "design_order": DESIGNS, "traces": TRACES, "development": list(DEVELOPMENT),
        "development_probe_ids": {"A": "F02", "B": "F05"}, "held_out": list(HELD_OUT),
        "endpoint": "Any definite failure on any eligible trace detects that variant; keep all case verdicts and unknowns.",
        "stimulus": "Identical driver directives, independent consumer-ready schedule and reset. The driver holds offered data until each DUT accepts it.",
    }
    save(out / "plan.json", manifest)
    cases, schedules, builds = {}, {}, {}
    with TemporaryDirectory(prefix="frame-negative-") as work, gzip.open(out / "observations.jsonl.gz", "xt") as stream, \
            tarfile.open(out / "native-replays.tar.gz", "x:gz") as archive:
        for design in DESIGNS:
            target = Path(work) / design
            fault = by_id.get(design)
            overrides = {} if fault is None else {fault.source: edit(fixture, fault)}
            run = run_suite(fixture, target, overrides=overrides)
            expected = {name: MAPPING["sha256"][name] for name in (DRIVER, *SOURCES, CHECKER)}
            expected.update({name: hashbytes(text.encode()) for name, text in overrides.items()})
            require(run["sha256"] == expected and run["overrides"] == sorted(overrides), f"{design}: wrong build inputs")
            require(set(run["traces"]) == set(TRACES) and run["physical_replays"] == len(TRACES),
                    f"{design}: incomplete native replays")
            builds[design] = {k: run[k] for k in ("iverilog", "sha256", "overrides", "physical_replays", "min_tail")}
            cases[design] = {}
            for trace in TRACES:
                folder = target / trace
                with gzip.open(folder / "rows.json.gz", "rt") as f:
                    rows = json.load(f)
                checker = json.loads((folder / "checker.json").read_text())
                require(checker == check_rows(rows, require_drained=True, min_tail=128),
                        f"{design}/{trace} does not reproduce with the frozen reference")
                require(checker["verdict"] in VERDICTS, f"invalid verdict for {design}/{trace}")
                require(checker["checked_rows"] == len(rows) or checker["verdict"] == "INVALID_INPUT",
                        f"incomplete grading for {design}/{trace}")
                if design == "original":
                    require(checker["verdict"] == "PASS" and not checker["unknown"], f"bad positive control {trace}")
                directives = (folder / "vectors.txt").read_bytes()
                require(schedules.setdefault(trace, directives) == directives, f"changed schedule for {design}/{trace}")
                if design == "original":
                    archive.add(folder / "vectors.txt", arcname=f"stimuli/{trace}.txt", recursive=False)
                archive.add(folder / "replay.log", arcname=f"{design}/{trace}/replay.log", recursive=False)
                stream.write(json.dumps({"design": design, "trace": trace, "rows": rows, "checker": checker},
                                        separators=(",", ":")) + "\n")
                cases[design][trace] = {
                    "cycles": len(rows), "verdict": checker["verdict"], "checked_rows": checker["checked_rows"],
                    "failure_counts": counts(checker["failures"]), "unknown_counts": counts(checker["unknown"]),
                    "first_failure": next(iter(checker["failures"]), None),
                    "first_unknown": next(iter(checker["unknown"]), None),
                }
    status = {d: dict(Counter(c["verdict"] for c in cases[d].values())) for d in DESIGNS}
    detected = [d for d in by_id if status[d].get("FAIL", 0)]
    survived = [d for d in by_id if status[d].get("PASS", 0) == len(TRACES)]
    inconclusive = sorted(set(by_id) - set(detected) - set(survived))
    checks = {name: hashbytes(check_file(fixture, name)) for name in sources}
    require(sources == checks, "original fixture changed")
    summary = {
        "complete": True, "designs": list(DESIGNS), "traces": list(TRACES),
        "native_replays": len(DESIGNS) * len(TRACES), "stimulus_sha256": {k: hashbytes(v) for k, v in schedules.items()},
        "corpus_sha256": hashbytes((out / "observations.jsonl.gz").read_bytes()),
        "native_archive_sha256": hashbytes((out / "native-replays.tar.gz").read_bytes()),
        "mutation_count": len(by_id), "detected": detected, "survived_all_three": survived,
        "inconclusive": inconclusive, "case_verdicts_by_design": status,
        "failures_by_design": {d: {k: sum(c["failure_counts"][k] for c in cases[d].values()) for k in CATEGORIES} for d in DESIGNS},
        "unknowns_by_design": {d: {k: sum(c["unknown_counts"][k] for c in cases[d].values()) for k in CATEGORIES} for d in DESIGNS},
    }
    save(out / "builds.json", builds)
    save(out / "cases.json", cases)
    save(out / "summary.json", summary)
    load_corpus(out)
    print(json.dumps({k: summary[k] for k in ("native_replays", "mutation_count", "detected", "survived_all_three", "inconclusive")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True, help="pristine hash-verified AXIS controller fixture")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        collect(args)
    except Exception as exc:
        save(args.output / "failure.json", {"error": str(exc)})
        raise
