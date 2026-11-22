#!/usr/bin/env python3
"""Read the actual ECO selector with Yosys and check selected guard inequalities with Z3."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from m3_guard_inputs import profiles
from predicates import DUT, parse


def detector_table(source, yosys="yosys"):
    """Return selector[override] for all 256 values, rejecting unspecified dependencies."""
    base = DUT.read_bytes()
    provenance = json.loads((DUT.parents[1] / "provenance.json").read_text())
    if hashlib.sha256(base).hexdigest() != provenance["rtl_sha256"]:
        raise ValueError("Original arbiter hash differs from provenance")
    selector = "if (priority_override != 8'b00000000) begin\n"
    prefix, suffix = base.decode().split(selector)
    # The monitored priority conditions, widths, reset and event context must
    # stay fixed. Accept the one unrelated, declared data-path control edit.
    data_control = suffix.replace("grant <= 8'b00000001;", "grant <= 8'b00000000;")
    tail = next((s for s in (suffix, data_control) if source.endswith(s)), None)
    if not source.startswith(prefix) or tail is None:
        raise ValueError("ECO outside the reviewed detector/data-control source map")
    clause = source[len(prefix):-len(tail)]
    match = re.fullmatch(r"if \(([^\n]+)\) begin\n", clause)
    if not match:
        raise ValueError("Could not identify the reviewed override selector")
    # Name the expression that actually selects the override branch. SV if
    # treats any nonzero vector as true, hence !! before storing it in one bit.
    probe = f"    (* keep *) wire m3_detector = !!({match[1]});\n"
    instrumented = prefix.replace("    always @", probe + "    always @", 1)
    instrumented += "if (m3_detector) begin\n" + tail
    with tempfile.TemporaryDirectory() as name:
        work = Path(name)
        (work / "arbiter.sv").write_text(instrumented)
        proc = subprocess.run([yosys, "-Q", "-T", "-p",
                               "read_verilog -sv arbiter.sv; hierarchy -check -top fixed_priority_arbiter; "
                               "proc; opt; eval -table priority_override -show m3_detector"],
                              cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              check=True, timeout=60)
    pairs = re.findall(r"^\s*8'([01]{8})\s*\|\s*1'([01])\s*$", proc.stdout, re.M)
    values = {int(bits, 2): flag == "1" for bits, flag in pairs}
    if len(pairs) != 256 or len(values) != 256:
        raise ValueError("Yosys could not determine all selector outputs from priority_override alone")
    return tuple(values[i] for i in range(256))


def certify_eco(table, *, rule_names=None, claim_names=None):
    """Return distinct(source, alternate) results for precisely the named obligations."""
    import z3
    if len(table) != 256 or any(type(value) is not bool for value in table):
        raise ValueError("Expected a 256-entry Boolean detector table")
    targets, rules, _ = profiles()
    families = {}
    families["rules"] = {name: (left, right) for name, left, right in rules}
    terms = {target["id"]: target["compact"] for target in targets}
    families["claims"] = {target["source_target"]: (target["compact"], terms[target["source_target"] + "/alternate"])
                          for target in targets if target["id"].endswith("/source")}
    selected = {}
    for family, names in [("rules", rule_names), ("claims", claim_names)]:
        names = list(families[family]) if names is None else list(names)
        if len(set(names)) != len(names) or set(names) - families[family].keys():
            raise ValueError(f"Unknown or duplicate {family}: {names}")
        selected[family] = names

    reset, req, override = z3.BitVec("reset_pin", 1), z3.BitVec("req", 8), z3.BitVec("priority_override", 8)
    mask = sum(1 << i for i in range(8) if table[1 << i])
    if all(table[i] == bool(i & mask) for i in range(256)):
        detector = (override & mask) != 0
    else:
        # Preserve an arbitrary two-state selector function of the override byte.
        detector = z3.Or(*[override == i for i, value in enumerate(table) if value])
    atoms = {"reset": reset == 1, "override_any": detector,
             "true": z3.BoolVal(True), "false": z3.BoolVal(False)}
    for prefix, port in [("req", req), ("override", override)]:
        atoms.update({f"{prefix}{i}": z3.Extract(i, i, port) == 1 for i in range(8)})

    def boolean(ast):
        if isinstance(ast, str):
            return atoms[ast]
        op = {"and": z3.And, "or": z3.Or, "not": z3.Not}[ast[0]]
        return op(*(boolean(child) for child in ast[1:]))

    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=30000)
    result = {"rules": {}, "claims": {}}
    for family, names in selected.items():
        for name in names:
            left, right = families[family][name]
            solver.push()
            solver.add(boolean(parse(left)) != boolean(parse(right)))
            status = solver.check()
            if status == z3.unknown:
                raise RuntimeError(f"Z3 returned unknown for {family}/{name}: {solver.reason_unknown()}")
            witness = None
            if status == z3.sat:
                model = solver.model()
                witness = {key: model.eval(port, model_completion=True).as_long()
                           for key, port in [("reset", reset), ("req", req), ("priority_override", override)]}
            result[family][name] = {"status": str(status), "witness": witness}
            solver.pop()
    return result


if __name__ == "__main__":
    from m3_eco_replay import variants
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="JSON file for all fixed versions")
    args = parser.parse_args()
    reports = {name: certify_eco(detector_table(source)) for name, source in variants().items()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(reports, indent=2) + "\n")
