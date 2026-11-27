#!/usr/bin/env python3
"""Measure three predefined output-port sensitivity controls on the complete AXIS frame design."""
import argparse
from dataclasses import asdict, dataclass
import gzip
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

from egg_frame_faults import TRACES, counts, hashbytes, load_corpus as load_previous, require, save
from egg_frame_observe import score_corpus
from egg_frame_replay import CHECKER, DRIVER, MAPPING, SOURCES, WRAPPER, check_file, run_suite
from egg_frame_terms import REFERENCES


PREVIOUS = Path(__file__).resolve().parents[1] / "results/milestone3/frame-faults"
PORTS_END = "input wire h_ready);"


@dataclass(frozen=True)
class Control:
    name: str
    property: str
    public_pin: str
    instance_port: str
    logic: str


CONTROLS = (
    Control("D01", "data_hold", "m_data", "m_axis_tdata", """
wire [7:0] clean_m_data;
reg flip_stalled_lsb = 1'b0;
always @(posedge clk) begin
    if (rst || !m_valid || m_ready)
        flip_stalled_lsb <= 1'b0;
    else
        flip_stalled_lsb <= ~flip_stalled_lsb;
end
assign m_data = clean_m_data ^ {7'b0, flip_stalled_lsb};
"""),
    Control("D02", "pad_flag", "h_pad", "m_axis_hdr_pad", """
wire clean_h_pad;
assign h_pad = clean_h_pad ^ (h_valid && h_original_length == 16'd4);
"""),
    Control("D03", "clamped_length", "h_length", "m_axis_hdr_length", """
wire [15:0] clean_h_length;
assign h_length = h_valid && h_original_length > 16'd8 ? 16'd7 : clean_h_length;
"""),
)
DESIGNS = ("original", *(c.name for c in CONTROLS))


def changed_wrapper(original, ctrl):
    port = f".{ctrl.instance_port}({ctrl.public_pin})"
    require(original.count(PORTS_END) == original.count(port) == 1, f"nonunique RTL anchor: {ctrl.name}")
    return original.replace(PORTS_END, PORTS_END + "\n" + ctrl.logic).replace(
        port, f".{ctrl.instance_port}(clean_{ctrl.public_pin})")


def load_corpus(directory):
    """Read native rows and frozen checker output for each (design, trace) tuple."""
    root = Path(directory)
    s = json.loads((root / "summary.json").read_text())
    data = (root / "observations.jsonl.gz").read_bytes()
    require(s["complete"] and hashbytes(data) == s["corpus_sha256"], "incomplete or changed diagnostic corpus")
    corpus = {}
    for line in gzip.decompress(data).splitlines():
        case = json.loads(line)
        key = case.pop("design"), case.pop("trace")
        require(key not in corpus, f"duplicate {key}")
        corpus[key] = case
    require(set(corpus) == {(d, t) for d in DESIGNS for t in TRACES}, "missing or extra diagnostic case")
    return corpus


def check_pin_changes(control, original, variant):
    """Independently reconstruct every PRE/POST port value from the original observation."""
    flip = 0
    changed = 0
    for ref, got in zip(original, variant, strict=True):
        require(ref["cycle"] == got["cycle"] and ref["inputs"] == got["inputs"], "drive schedule changed")
        inputs = ref["inputs"]
        for phase in ("pre", "post"):
            pins = dict(ref[phase])
            if phase == "post":
                flip = 1 - flip if not inputs["rst"] and ref["pre"]["m_valid"] == 1 and not inputs["m_ready"] else 0
            old = pins[control.public_pin]
            if control.name == "D01":
                pins[control.public_pin] = old ^ flip if old != -1 else -1
            elif pins["h_valid"] == 1:
                length = pins["h_original_length"]
                require(length >= 0, f"unresolved valid header length at {ref['cycle']}")
                if control.name == "D02" and length == 4:
                    pins[control.public_pin] = old ^ 1 if old != -1 else -1
                elif control.name == "D03" and length > 8:
                    pins[control.public_pin] = 7
            require(pins == got[phase], f"{control.name}: extra or missing port change on {phase} {ref['cycle']}")
            changed += old != pins[control.public_pin]
    return changed


def run(args):
    fixture, out = args.fixture.resolve(), args.output.resolve()
    old = load_previous(PREVIOUS)
    old_summary = json.loads((PREVIOUS / "summary.json").read_bytes())
    wrapper = check_file(fixture, WRAPPER).decode()
    overrides = {c.name: {WRAPPER: changed_wrapper(wrapper, c)} for c in CONTROLS}
    plan = {"scope": "Post-generation port sensitivity controls on the pinned wrapper; original RTL retained.",
            "upstream_commit": MAPPING["commit"], "wrapper": WRAPPER, "wrapper_sha256": MAPPING["sha256"][WRAPPER],
            "controls": [{**asdict(c), "wrapper_sha256": hashbytes(overrides[c.name][WRAPPER].encode())} for c in CONTROLS],
            "design_order": DESIGNS, "traces": TRACES, "stimulus_sha256": old_summary["stimulus_sha256"],
            "reference_checker_sha256": MAPPING["sha256"][CHECKER], "references": REFERENCES}
    save(out / "plan.json", plan)
    cases, builds, port_changes = {}, {}, {}
    by_id = {c.name: c for c in CONTROLS}
    with TemporaryDirectory(prefix="frame-port-") as work, tarfile.open(out / "native-replays.tar.gz", "x:gz") as archive:
        for design in DESIGNS:
            dest = Path(work) / design
            mods = overrides.get(design, {})
            report = run_suite(fixture, dest, overrides=mods)
            hashes = {name: MAPPING["sha256"][name] for name in (DRIVER, *SOURCES, CHECKER)}
            hashes.update({name: hashbytes(text.encode()) for name, text in mods.items()})
            require(report["sha256"] == hashes and report["overrides"] == sorted(mods), "wrong compiled sources")
            require(report["physical_replays"] == len(TRACES) and set(report["traces"]) == set(TRACES), "missing replay")
            builds[design] = {k: report[k] for k in ("sha256", "iverilog", "overrides", "min_tail", "physical_replays")}
            for name in TRACES:
                path = dest / name
                rows = json.loads(gzip.decompress((path / "rows.json.gz").read_bytes()))
                ref = json.loads((path / "checker.json").read_bytes())
                require(ref["verdict"] in ("PASS", "FAIL", "UNRESOLVED") and ref["checked_rows"] == len(rows),
                        f"ungradable case {design}/{name}")
                require(hashbytes((path / "vectors.txt").read_bytes()) == plan["stimulus_sha256"][name],
                        f"stimuli changed: {design}/{name}")
                cases[design, name] = {"rows": rows, "checker": ref}
                if design == "original":
                    require(cases[design, name] == old[design, name] and ref["verdict"] == "PASS",
                            f"positive control changed: {name}")
                    archive.add(path / "vectors.txt", arcname=f"stimuli/{name}.txt")
                else:
                    port_changes[design, name] = check_pin_changes(by_id[design], old["original", name]["rows"], rows)
                archive.add(path / "replay.log", arcname=f"{design}/{name}/replay.log")
    score = score_corpus(cases, REFERENCES)
    case_results, positives = {}, {}
    for (design, name), case in cases.items():
        ref = case["checker"]
        scores = score["cases"][design][name]["properties"]
        observed = {p: {"reference_alarms": v["reference_alarms"], "unknown": v["unknown"],
                        "first_reference_alarm": v["first_reference_alarm"]} for p, v in scores.items()}
        case_results.setdefault(design, {})[name] = {
            "checker_verdict": ref["verdict"], "checker_failure_counts": counts(ref["failures"]),
            "checker_unknown_counts": counts(ref["unknown"]), "changed_pin_samples_pre_plus_post": port_changes.get((design, name), 0),
            "observed_cycles": len(case["rows"]), "eligible_pre_samples": len(case["rows"]) - 1, "properties": observed}
        totals = positives.setdefault(design, {p: 0 for p in REFERENCES})
        for p, values in observed.items():
            totals[p] += values["reference_alarms"]
    raw = "".join(json.dumps({"design": d, "trace": t, **c}, separators=(",", ":")) + "\n" for (d, t), c in cases.items())
    corpus_file = out / "observations.jsonl.gz"
    corpus_file.write_bytes(gzip.compress(raw.encode(), mtime=0))
    save(out / "builds.json", builds)
    save(out / "cases.json", case_results)
    summary = {"complete": True, "designs": DESIGNS, "native_replays": sum(b["physical_replays"] for b in builds.values()),
               "observed_cycles": sum(len(c["rows"]) for c in cases.values()),
               "eligible_pre_samples": sum(len(c["rows"]) - 1 for c in cases.values()),
               "reference_alarms_by_design": positives, "stimulus_sha256": plan["stimulus_sha256"],
               "intended_positive_controls": {c.name: positives[c.name][c.property] > 0 for c in CONTROLS},
               "corpus_sha256": hashbytes(corpus_file.read_bytes()),
               "native_archive_sha256": hashbytes((out / "native-replays.tar.gz").read_bytes())}
    save(out / "summary.json", summary)
    require(load_corpus(out) == cases, "scorer corpus roundtrip failed")
    print(json.dumps(summary["reference_alarms_by_design"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new destination")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        run(args)
    except Exception as exc:
        save(args.output / "failure.json", {"error": str(exc)})
        raise
