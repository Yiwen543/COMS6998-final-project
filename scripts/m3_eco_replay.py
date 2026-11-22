#!/usr/bin/env python3
"""Bounded ECO controls on the pinned arbiter; replay exact two-state counterexamples."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from m3_guard_inputs import profiles
from predicates import DUT, _atom_tables, _truth_table, extract, parse


DETECTOR = "priority_override != 8'b00000000"


def replace_one(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"expected exactly one source anchor: {old}")
    return text.replace(old, new)


def variants():
    """Fixed ECO names and full, uninstrumented source. The repository DUT stays immutable."""
    extract()  # Reuse the pinned source hash and priority-map checks.
    source = DUT.read_text()
    cases = {"baseline": source}
    for bit in range(8):
        mask = 255 ^ (1 << bit)
        cases[f"omit_override_bit_{bit}"] = replace_one(source, DETECTOR, f"|(priority_override & 8'h{mask:02x})")
    cases["equivalent_reduction_or"] = replace_one(source, DETECTOR, "|priority_override")
    cases["grant_data_control"] = replace_one(source, "grant <= 8'b00000001;", "grant <= 8'b00000000;")
    return cases


def evaluate_obligations(name):
    forms, rules, _ = profiles()
    atoms = _atom_tables().copy()
    if name.startswith("omit_override_bit_"):
        omitted = int(name.rsplit("_", 1)[1])
        atoms["override_any"] = 0
        for i in range(8):
            if i != omitted:
                atoms["override_any"] |= atoms[f"override{i}"]

    def test(left, right):
        lhs, rhs = (_truth_table(parse(expr), atoms) for expr in (left, right))
        diff = lhs ^ rhs
        if not diff:
            return {"status": "unsat", "differing_assignments": 0, "witness": None}
        first_bit = diff & -diff
        index = first_bit.bit_length() - 1
        return {"status": "sat", "differing_assignments": diff.bit_count(),
                "witness": {"reset": index >> 16, "req": index & 255, "priority_override": (index >> 8) & 255},
                "left": bool(lhs & first_bit), "right": bool(rhs & first_bit)}

    expressions = {form["id"]: form["compact"] for form in forms}
    claims = {form["source_target"]: test(form["compact"], expressions[form["source_target"] + "/alternate"])
              for form in forms if form["id"].endswith("/source")}
    return {"claims": claims, "rules": {name: test(left, right) for name, left, right in rules}}


def monitored_twin(source):
    # When req and override have the same winning bit, both paths can produce the
    # same outputs. Record entry into the actual existing if/else branches.
    source = replace_one(source, "module fixed_priority_arbiter(", "module sampled_arbiter(")
    process = "always @(posedge clk or posedge reset) begin"
    source = replace_one(source, process, "integer branch_id;\n    " + process + "\n        branch_id <= -1;")
    source = replace_one(source, "grant <= priority_override;", "branch_id <= 8; grant <= priority_override;")
    for i in range(8):
        anchor = f"if (req[{i}]) begin"
        source = replace_one(source, anchor, anchor + f" branch_id <= {i};")
    return source


BENCH = """module eco_replay;
    reg clk, reset;
    reg [7:0] req, priority_override;
    wire [7:0] grant, sampled_grant;
    wire valid, sampled_valid;
    wire [2:0] grant_index, sampled_index;
    fixed_priority_arbiter rtl(clk,reset,req,priority_override,grant,valid,grant_index);
    sampled_arbiter monitor(clk,reset,req,priority_override,sampled_grant,sampled_valid,sampled_index);
    integer fd, rows, scan, rst_int, req_int, over_int;
    initial begin
        fd = $fopen("vectors.txt", "r");
        if (!fd) $fatal(1, "missing vectors");
        clk = 0; reset = 1; req = 0; priority_override = 0;
        #1; clk = 1; #1; clk = 0; #1;
        rows = 0;
        while (!$feof(fd)) begin
            scan = $fscanf(fd, "%d %d %d\\n", rst_int, req_int, over_int);
            if (scan == 3) begin
                reset = rst_int; req = req_int; priority_override = over_int;
                #1; clk = 1; #1;
                $display("OBS %0d %b %b %b %b %b %b %0d", rows,reset,req,priority_override,
                         grant,valid,grant_index,monitor.branch_id);
                if ({grant,valid,grant_index} !== {sampled_grant,sampled_valid,sampled_index})
                    $fatal(1, "probe changed output");
                clk = 0; #1; rows = rows + 1;
            end
            else if (!$feof(fd)) $fatal(1, "invalid vector");
        end
        $display("DONE %0d", rows);
        $finish;
    end
endmodule
"""


def pin_tuple(witness):
    return witness["reset"], witness["req"], witness["priority_override"]


def replay(source, vectors, log):
    with tempfile.TemporaryDirectory() as work:
        folder = Path(work)
        (folder / "dut.sv").write_text(source)
        (folder / "monitor.sv").write_text(monitored_twin(source))
        (folder / "tb.sv").write_text(BENCH)
        (folder / "vectors.txt").write_text("".join(f"{rst} {req} {ov}\n" for rst, req, ov in vectors))
        subprocess.run(["iverilog", "-g2012", "-s", "eco_replay", "-o", "sim.vvp", "dut.sv", "monitor.sv", "tb.sv"],
                       cwd=folder, check=True, capture_output=True, timeout=60)
        run = subprocess.run(["vvp", "sim.vvp"], cwd=folder, text=True, capture_output=True, timeout=60)
        log.write_text(run.stdout + run.stderr)
        run.check_returncode()
    lines = run.stdout.splitlines()
    if f"DONE {len(vectors)}" not in lines:
        raise ValueError(f"incomplete physical replay, see {log}")
    observations = []
    for ln in (line for line in lines if line.startswith("OBS ")):
        _, row, rst, req, over, grant, valid, index, path = ln.split()
        # Refuse unknowns, retaining original x/z strings in the raw transcript.
        if any(set(bits) - {"0", "1"} for bits in (rst, req, over, grant, valid, index)):
            raise ValueError(f"unknown physical pin observation, see {log}")
        if int(row) != len(observations) or tuple(int(n, 2) for n in (rst, req, over)) != vectors[int(row)]:
            raise ValueError(f"unexpected input ordering in {log}")
        observations.append({"grant": int(grant, 2), "valid": int(valid, 2), "index": int(index, 2),
                             "path": int(path)})
    if len(observations) != len(vectors):
        raise ValueError(f"missing observations in {log}")
    return observations


def guard_active(target, obs):
    kind, index = target.split("_")
    if kind == "req":
        return obs["path"] == int(index)
    return obs["path"] == 8 and obs["index"] == int(index)


def check_witness(name, rst, obs, base, left, right):
    if name == "override-nonzero":
        # The left side spells out the original reduction, the right side is the edited selector.
        if rst:
            raise ValueError("the top-level detector is masked by reset on this replay")
        measured = (base["path"] == 8, obs["path"] == 8)
    else:
        target = name.removesuffix("-activation")
        measured = (guard_active(target, obs), guard_active(target, base))
    if measured != (left, right) or left == right:
        raise ValueError(f"{name}: RTL source/alternate witness disagreement: {measured}")


def experiment(out):
    sources = variants()
    cases = {name: evaluate_obligations(name) for name in sources}
    vectors = {(0, 1, 0), (0, 0, 0), (1, 0, 0)}
    for case in cases.values():
        for family in case.values():
            vectors.update(pin_tuple(r["witness"]) for r in family.values() if r["witness"] is not None)
    vectors = sorted(vectors, key=lambda pins: (pins[0], pins[2], pins[1]))
    indices = {v: i for i, v in enumerate(vectors)}
    baseline = None
    for name, source in sources.items():
        changed = replay(source, vectors, out / f"{name}.log")
        if name == "baseline":
            baseline = changed
        assertions = cases[name]
        for family in ("rules", "claims"):
            for target, test in assertions[family].items():
                if test["witness"] is None:
                    continue
                pins = pin_tuple(test["witness"])
                row = indices[pins]
                check_witness(target, pins[0], changed[row], baseline[row], test["left"], test["right"])
                test["replay_row"] = row
        rows = [i for i, (old, new) in enumerate(zip(baseline, changed, strict=True))
                if any(old[key] != new[key] for key in ("grant", "valid", "index"))]
        assertions.update(source_sha256=hashlib.sha256(source.encode()).hexdigest(), output_change_rows=rows,
                          path_change_rows=[i for i in range(len(vectors)) if baseline[i]["path"] != changed[i]["path"]])
        if name == "equivalent_reduction_or" and (rows or assertions["path_change_rows"]):
            raise ValueError("equivalent source syntax changed the physical replay")
        if name == "grant_data_control":
            i = indices[(0, 1, 0)]
            if not (baseline[i]["grant"] == 1 and changed[i]["grant"] == 0 and not assertions["path_change_rows"]):
                raise ValueError("unrelated req[0] grant-data defect was not reproduced")
    report = {"scope": "Fixed pinned RTL edits and two-state guard obligations at the active clock edge",
              "iverilog": subprocess.check_output(["iverilog", "-V"], text=True, stderr=subprocess.DEVNULL,
                                                  timeout=10).splitlines()[0],
              "legal_assignments": 131072, "vectors_reset_req_override": vectors,
              "physical_processes": len(sources), "sampled_rows_per_process": len(vectors),
              "raw_log_format": "OBS row reset req override grant valid grant_index branch_id; pins and outputs binary; "
                                "branch_id -1 for reset/idle, 0..7 for req branches, 8 for override arm",
              "cases": cases}
    (out / "summary.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new directory for raw Icarus logs and oracle")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    experiment(args.output)
