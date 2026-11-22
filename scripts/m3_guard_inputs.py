#!/usr/bin/env python3
"""Certify two fixed guard profiles from the checked-in eight-way arbiter."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from predicates import DUT, extract, fold


def solver_preamble():
    lines = [
        "(set-logic QF_BV)",
        "(declare-const reset_pin (_ BitVec 1))",
        "(declare-const req (_ BitVec 8))",
        "(declare-const priority_override (_ BitVec 8))",
        "(define-fun reset () Bool (= reset_pin #b1))",
        "(define-fun override_any () Bool (distinct priority_override #x00))",
    ]
    for prefix, port in [("req", "req"), ("override", "priority_override")]:
        for i in range(8):
            lines.append(f"(define-fun {prefix}{i} () Bool (= ((_ extract {i} {i}) {port}) #b1))")
    return "\n".join(lines)


def oracle(kind, index):
    # x & -x isolates the lowest set bit, independently of the RTL if/ternary chain.
    port = "req" if kind == "req" else "priority_override"
    activation = "(= priority_override #x00)" if kind == "req" else "(distinct priority_override #x00)"
    winner = f"(= (bvand {port} (bvneg {port})) #x{1 << index:02x})"
    return f"(and (= reset_pin #b0) {activation} {winner})"


def profiles():
    override_bits = fold("or", [f"override{i}" for i in range(8)])
    targets = []
    rules = [("override-nonzero", override_bits, "override_any")]
    checks = []
    for target in extract():
        name, kind, index = target["id"], target["kind"], target["index"]
        source = target["compact"]
        if kind == "req":
            alternate = source.replace("override_any", override_bits)
        else:
            # The winning override bit implies that the port is nonzero.
            lower = fold("or", [f"override{i}" for i in range(index)])
            alternate = f"(and (not reset) (and override{index} (not {lower})))"
            rules.append((f"{name}-activation", source, alternate))
        for form, expr in [("source", source), ("alternate", alternate)]:
            identifier = f"{name}/{form}"
            targets.append({
                "id": identifier, "compact": expr, "source_target": name,
                "source": target["source"], "line": target["line"],
                "event_context": {k: target[k] for k in ("event", "reset_context", "width", "logic")},
            })
            checks.append((identifier, expr, oracle(kind, index)))
    checks.extend((f"rule/{name}", left, right) for name, left, right in rules)
    return targets, rules, checks


def certify(checks, z3):
    script = [solver_preamble()]
    for name, left, right in checks:
        script.extend([f"; {name}", "(push 1)", f"(assert (distinct {left} {right}))",
                       "(check-sat)", "(pop 1)"])
    smt = "\n".join(script) + "\n"
    result = subprocess.run([z3, "-in", "-smt2"], input=smt, text=True, capture_output=True,
                            check=True, timeout=60)
    statuses = result.stdout.splitlines()
    if len(statuses) != len(checks):
        raise ValueError(f"Z3 returned {len(statuses)} answers for {len(checks)} queries")
    proofs = {}
    for (name, _, _), status in zip(checks, statuses):
        if status != "unsat":
            raise ValueError(f"Failed guard certificate {name}: {status}")
        proofs[name] = status
    return smt, proofs


def json_bytes(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()


def generate(out, z3):
    targets, rules, checks = profiles()
    smt, proofs = certify(checks, z3)
    verified = [{"name": name, "left": left, "right": right, "proof_status": proofs[f"rule/{name}"]}
                for name, left, right in rules]
    files = {
        "control.json": json_bytes({"targets": targets, "verified_rules": []}),
        "ground.json": json_bytes({"targets": targets, "verified_rules": verified}),
        "certificates.smt2": smt.encode(),
    }
    manifest = {
        "scope": "Current inputs at a sampled rising clock edge. Two-state reset and unsigned 8-bit ports.",
        "rtl_sha256": hashlib.sha256(DUT.read_bytes()).hexdigest(),
        "sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
        "source_targets": len({t["source_target"] for t in targets}),
        "forms": len(targets),
        "ground_rules": len(verified),
        "z3": subprocess.check_output([z3, "--version"], text=True, timeout=10).strip(),
        "checks": proofs,
    }
    out.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        (out / name).write_bytes(data)
    (out / "manifest.json").write_bytes(json_bytes(manifest))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--z3", default="z3", help="Z3 executable")
    args = parser.parse_args()
    generate(args.output, args.z3)
