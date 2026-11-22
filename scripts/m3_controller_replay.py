#!/usr/bin/env python3
"""Rebuild the pinned AXI controller and sample its typed guards on legal traces."""

import argparse
import hashlib
import json
import re
import runpy
import subprocess
import tempfile
from pathlib import Path
from urllib.request import urlopen

from predicates import parse


MAPPING = json.loads(Path(__file__).with_name("m3_controller_replay_manifest.json").read_text())
SCREEN = Path("qualification/typed-v5/screen")
TRACES = ("basic", "boundary_pressure", "reset_reuse")
TOP = "tb_natural_inventory"
INPUTS = ("rst", "s_valid", "s_data", "s_last", "m_ready", "h_ready")
OUTPUTS = ("s_ready", "m_data", "m_valid", "m_last", "h_valid", "h_pad", "h_truncate",
           "h_length", "h_original_length")


def check_file(fixture, name):
    data = (fixture / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != MAPPING["sha256"][str(name)]:
        raise ValueError(f"Hash mismatch in {name}")
    return data


def fetch(output):
    """Fetch immutable bytes, verify every SHA-256, then publish the directory."""
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    url = f'https://raw.githubusercontent.com/{MAPPING["repository"]}/{MAPPING["commit"]}/{MAPPING["fixture"]}'
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        stage = Path(tmp) / "verified"
        for name in MAPPING["sha256"]:
            dest = stage / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urlopen(f"{url}/{name}", timeout=30) as response:
                dest.write_bytes(response.read())
            check_file(stage, name)
        stage.rename(output)


def typed_sv(node):
    """Lower the 52 upstream Slang atoms. Every typed node has an explicit width/sign."""
    kind = node["kind"]
    if kind == "truth_conversion":
        return f"(({typed_sv(node['operand'])}) != 0)"
    if kind == "case_two_state_eq":
        return f"({typed_sv(node['left'])} == {typed_sv(node['right'])})"
    width = node["type"]["width"]
    cast = "$signed" if node["type"]["signed"] else "$unsigned"
    if kind == "NamedValue":
        symbol = node["symbol"]
        if not re.fullmatch(r"dut(?:\.[a-zA-Z_]\w*)+", symbol):
            raise ValueError(f"Unexpected non-hierarchical symbol {symbol}")
        expr = "dut." + symbol
    elif kind == "constant":
        expr = f"{width}'h{node['value'] % (1 << width):x}"
    elif kind == "Conversion":
        expr = typed_sv(node["operand"])
    elif kind == "UnaryOp" and node["op"] == "BitwiseNot":
        expr = f"~({typed_sv(node['operand'])})"
    elif kind == "BinaryOp":
        op = {"Equality": "==", "Subtract": "-", "LogicalShiftRight": ">>",
              "GreaterThan": ">", "LessThanEqual": "<="}[node["op"]]
        expr = f"({typed_sv(node['left'])} {op} {typed_sv(node['right'])})"
    elif kind == "ConditionalOp":
        expr = f"({typed_sv(node['condition'])} ? {typed_sv(node['left'])} : {typed_sv(node['right'])})"
    elif kind == "Concatenation":
        expr = "{" + ", ".join(typed_sv(v) for v in node["operands"]) + "}"
    elif kind == "Replication":
        expr = "{" + str(node["count"]) + "{" + typed_sv(node["value"]) + "}}"
    else:
        raise ValueError(f"Unsupported typed operation {kind}")
    return f"{cast}({width}'({expr}))"


def guard_sv(ast, atoms):
    if isinstance(ast, str):
        if ast in ("true", "false"):
            return "1'b1" if ast == "true" else "1'b0"
        return f"m3_atoms[{atoms[ast]}]"
    op, *args = ast
    if op == "not":
        return f"(!{guard_sv(args[0], atoms)})"
    symbol = {"and": "&&", "or": "||"}[op]
    return f"({guard_sv(args[0], atoms)} {symbol} {guard_sv(args[1], atoms)})"


def probed_driver(fixture):
    targets = json.loads((fixture / SCREEN / "egg-input.json").read_bytes())["targets"]
    definitions = json.loads((fixture / SCREEN / "extraction.json").read_bytes())
    if targets != definitions["targets"]:
        raise ValueError("Target/form/order mismatch between frozen input and extraction")
    if len(targets) != 148 or len(definitions["atoms"]) != 52:
        raise ValueError("Unexpected controller schema")
    atoms = {k: i for i, k in enumerate(sorted(definitions["atoms"]))}
    probes = [f"wire [0:{len(atoms)-1}] m3_atoms;", f"wire [0:{len(targets)-1}] m3_targets;"]
    for name, i in atoms.items():
        probes.append(f"assign m3_atoms[{i}] = {typed_sv(definitions['atoms'][name])};")
    for i, target in enumerate(targets):
        if target["event_context"] not in (["combinational"], ["PosEdge:clk"]):
            raise ValueError(f"Unsupported event {target['event_context']}")
        probes.append(f"assign m3_targets[{i}] = {guard_sv(parse(target['compact']), atoms)};")
    driver = (fixture / "public/driver.sv").read_text()
    anchor = '   $display("PRE '
    if driver.count(anchor) != 1 or driver.count("string path;") != 1:
        raise ValueError("Unknown driver sampling location")
    driver = driver.replace("string path;", "string path;\n" + "\n".join(probes))
    return driver.replace(anchor, '   $display("GUARDS %0d %b %b",cycle,m3_atoms,m3_targets);\n' + anchor)


def build(fixture, work, *, probes=True):
    """Build the original RTL with the probed or pristine driver in a new directory."""
    fixture, work = Path(fixture).resolve(), Path(work).resolve()
    for name in MAPPING["sha256"]:
        check_file(fixture, name)
    work.mkdir(parents=True, exist_ok=False)
    tb = fixture / "public/driver.sv"
    if probes:
        tb = work / "m3_driver.sv"
        tb.write_text(probed_driver(fixture))
    obj = work / "obj"
    # Ensure coverage is flushed explicitly for this Verilator version.
    main_cpp = work / "m3_main.cpp"
    main_cpp.write_text("""#include "Vtb_natural_inventory.h"
#include "verilated.h"
#include "verilated_cov.h"
int main(int argc, char** argv) {
    VerilatedContext context;
    context.commandArgs(argc, argv);
    Vtb_natural_inventory dut(&context);
    while (!context.gotFinish()) {
        dut.eval();
        if (!dut.eventsPending()) break;
        context.time(dut.nextTimeSlot());
    }
    dut.final();
    context.coveragep()->write();
    return context.gotFinish() ? 0 : 2;
}
""")
    rtl = sorted((fixture / "public/rtl").glob("*.v"))
    # Compile only manifest-verified RTL, including when an external fixture path is supplied.
    expected = sorted(fixture / s for s in MAPPING["sha256"] if s.startswith("public/rtl/"))
    if rtl != expected:
        raise ValueError("Unexpected RTL file set")
    command = ["verilator", "--cc", "--exe", "--build", "-j", "2", "--timing", "-Wno-fatal",
               "--coverage-line", "--coverage-toggle", "--coverage-expr", "--top-module", TOP,
               "--Mdir", obj, tb, fixture / "public/task_top_v3.sv", *rtl, main_cpp]
    with (work / "build.log").open("w") as log:
        job = subprocess.run(command, cwd=work, stdout=log, stderr=subprocess.STDOUT, timeout=240)
    if job.returncode:
        raise RuntimeError(f"Controller build failed; inspect {work / 'build.log'}")
    return obj / ("V" + TOP)


def counters(coverage, fixture):
    """Read all counters from the pinned original RTL; retain native hit counts."""
    raw = []
    dut_sources = {str(fixture / p): MAPPING["fixture"] + "/" + p for p in MAPPING["sha256"]
                   if p.startswith("public/rtl/") or p == "public/task_top_v3.sv"}
    for line in coverage.read_text().splitlines()[1:]:
        row = re.fullmatch(r"C '(.*)' (\d+)", line)
        if not row:
            raise ValueError("Malformed Verilator coverage record")
        fields = dict(part.split("\x02", 1) for part in row[1].split("\x01") if part)
        if fields.get("f") not in dut_sources:
            continue
        raw.append({"source": dut_sources[fields["f"]], "line": int(fields["l"]),
                    "column": int(fields.get("n", 0)), "type": fields["t"],
                    "outcome": fields.get("o", ""), "hierarchy": fields["h"].removeprefix("TOP."),
                    "span": fields.get("S"), "page": fields.get("page"), "hits": int(row[2])})
    if not raw:
        raise ValueError("No original RTL coverage records")
    screen = json.loads(check_file(fixture, SCREEN / "screen.json"))
    if len(raw) != screen["raw_dut_denominator"]:
        raise ValueError(f"Frozen controller has {screen['raw_dut_denominator']} raw counters, found {len(raw)}")
    mappings = screen["mappings"]
    keys = ("source", "line", "column", "type", "outcome", "hierarchy")
    lookup = {}
    for point in raw:
        lookup.setdefault(tuple(point[k] for k in keys), []).append(point["hits"])
    mapped = {}
    for name, mapping in mappings.items():
        if mapping["status"] == "unresolved":
            mapped[name] = None
        else:
            matches = lookup.get(tuple(mapping["point"][k] for k in keys), [])
            if len(matches) != 1:
                raise ValueError(f"Expected exactly one raw counter for {name}, found {len(matches)}")
            mapped[name] = matches[0]
    return raw, mapped


def replay(fixture, binary, trace, work, cycles=None, *, probes=True):
    """Return pre-edge guard matrices, public observations/checks and DUT coverage."""
    fixture, binary, work = map(lambda p: Path(p).resolve(), (fixture, binary, work))
    if trace not in TRACES:
        raise ValueError(f"Unknown trace {trace}")
    dataset = json.loads(check_file(fixture, f"public/development/{trace}.json"))
    actions = dataset["actions"]
    if cycles is not None:
        if not 1 <= cycles <= len(actions):
            raise ValueError("Prefix must start at reset and fit the frozen schedule")
        actions = actions[:cycles]
    work.mkdir(parents=True, exist_ok=False)
    vector_file = work / "vectors.txt"
    keys = ("reset", "offer", "data", "last", "data_ready", "status_ready")
    vector_file.write_text("".join(" ".join(str(a[k]) for k in keys) + "\n" for a in actions))
    coverage = work / "coverage.dat"
    proc = subprocess.run([binary, f"+VECTORS={vector_file}", f"+verilator+coverage+file+{coverage}"],
                          cwd=work, text=True, capture_output=True, timeout=60)
    (work / "replay.log").write_text(proc.stdout + proc.stderr)
    if proc.returncode or f"DRIVER_COMPLETE {len(actions)}" not in proc.stdout.splitlines():
        raise RuntimeError(f"Incomplete controller replay; inspect {work / 'replay.log'}")
    records = {k: [] for k in ("PRE", "POST", "QUEUE")}
    if probes:
        records["GUARDS"] = []
    observed = []
    for line in proc.stdout.splitlines():
        words = line.split()
        if words and words[0] in records:
            rows = records[words[0]]
            if int(words[1]) != len(rows):
                raise ValueError(f"Nonconsecutive {words[0]} rows")
            rows.append(words[2:])
            if words[0] != "GUARDS":
                observed.append(line)
    if any(len(v) != len(actions) for v in records.values()):
        raise ValueError("Missing physical observation")
    for atoms, targets in records.get("GUARDS", []):
        if not re.fullmatch("[01]{52}", atoms) or not re.fullmatch("[01]{148}", targets):
            raise ValueError("Missing binary guard observation")
    public_rows = []
    for i, (pre, post) in enumerate(zip(records["PRE"], records["POST"])):
        if len(pre) != len(INPUTS) + len(OUTPUTS) or len(post) != len(OUTPUTS):
            raise ValueError("Incomplete pre/post output observations")
        public_rows.append({"cycle": i, "inputs": dict(zip(INPUTS, map(int, pre[:len(INPUTS)]))),
                            "pre": dict(zip(OUTPUTS, map(int, pre[len(INPUTS):]))),
                            "post": dict(zip(OUTPUTS, map(int, post)))})
    checker_path = "reference/frozen-v2/checker.py"
    check_file(fixture, checker_path)
    checker = runpy.run_path(str(fixture / checker_path))["check_rows"]
    verdict = checker(public_rows, require_drained=cycles is None and dataset["require_drained"])
    raw, mapped = counters(coverage, fixture)
    measurements = {"trace": trace, "cycles": len(actions), "eligible_cycles": list(range(1, len(actions))),
                    "raw_counters": raw, "mapped_hits": mapped, "checker": verdict,
                    "outputs_sha256": hashlib.sha256(("\n".join(observed) + "\n").encode()).hexdigest()}
    if not probes:
        return measurements
    extraction = json.loads(check_file(fixture, SCREEN / "extraction.json"))
    ids = [t["id"] for t in extraction["targets"]]
    rows = [r[1] for r in records["GUARDS"]]
    # A recorded positive at a mapped guard must activate its original source
    # counter. Native counters may also count transients between PRE samples.
    for i, target in enumerate(ids):
        if mapped[target] == 0 and any(row[i] == "1" for row in rows[1:]):
            raise ValueError(f"PRE witness for {target} contradicts its zero raw DUT counter")
    return {**measurements, "atom_ids": sorted(extraction["atoms"]), "atom_rows": [r[0] for r in records["GUARDS"]],
            "target_ids": ids, "rows": rows}


def check_passivity(fixture, output):
    """Compare the entire DUT inventory and public pin/queue history with a pristine driver."""
    def public_log(path):
        lines = path.read_text().splitlines()
        return [s for s in lines if s.startswith(("PRE ", "POST ", "QUEUE ", "DRIVER_COMPLETE "))]

    output.mkdir(parents=True, exist_ok=False)
    binaries = {use_probes: build(fixture, output / name, probes=use_probes)
                for use_probes, name in [(False, "pristine"), (True, "probed")]}
    traces = []
    for trace in TRACES:
        plain = replay(fixture, binaries[False], trace, output / "pristine" / trace, probes=False)
        probed = replay(fixture, binaries[True], trace, output / "probed" / trace)
        for key, expected in plain.items():
            if probed[key] != expected:
                raise ValueError(f"Passive probe changed {key} for {trace}")
        # Compare the public records themselves as well as their packaged digest.
        plain_log = public_log(output / "pristine" / trace / "replay.log")
        if plain_log != public_log(output / "probed" / trace / "replay.log"):
            raise ValueError(f"Passive probe changed a public pin or queue record on {trace}")
        raw = json.dumps(plain["raw_counters"], separators=(",", ":"), sort_keys=True).encode()
        traces.append({"trace": trace, "cycles_per_driver": plain["cycles"],
                       "native_counters_compared": len(plain["raw_counters"]),
                       "native_counters_sha256": hashlib.sha256(raw).hexdigest(),
                       "public_records_compared": len(plain_log), "public_pre_post_queue_sha256": plain["outputs_sha256"],
                       "mapped_source_guards": sum(n is not None for n in plain["mapped_hits"].values()),
                       "unresolved_source_guards": [k for k, n in plain["mapped_hits"].items() if n is None],
                       "reference_checker": plain["checker"]})
    manifest = Path(__file__).with_name("m3_controller_replay_manifest.json").read_bytes()
    report = {"upstream_commit": MAPPING["commit"], "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
              "verilator": subprocess.check_output(["verilator", "--version"], text=True).strip(),
              "native_counts_and_observations_identical": True, "physical_replays": 2 * len(TRACES), "traces": traces}
    (output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    action = cli.add_mutually_exclusive_group(required=True)
    action.add_argument("--fetch", type=Path, metavar="NEW_FIXTURE_DIR")
    action.add_argument("--check-passivity", type=Path, metavar="FIXTURE_DIR")
    cli.add_argument("--output", type=Path, help="new output directory for a passivity comparison")
    args = cli.parse_args()
    if (args.fetch and args.output) or (args.check_passivity and not args.output):
        cli.error("--output must be used with --check-passivity")
    if args.fetch:
        fetch(args.fetch)
    else:
        check_passivity(args.check_passivity, args.output)
