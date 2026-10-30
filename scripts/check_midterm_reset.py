#!/usr/bin/env python3
"""Record preclock reset observations without altering original CVDP RTL."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/midterm_candidate_preflight"
BUILD = ROOT / "build/midterm_reset"
CASES = [
    ("heldout_codec64", "tb_decoder_reset_preclock",
     ["decoder_data_control_64b66b.sv"]),
    ("heldout_linear_search", "tb_search_reset_preclock",
     ["linear_search_ctrl.sv"]),
]


def run(argv, log):
    result = subprocess.run([str(x) for x in argv], cwd=ROOT,
                            text=True, capture_output=True, timeout=30)
    log.write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {argv}\n{result.stderr[-700:]}")
    return result.stdout


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    results = []
    for slug, top, sources in CASES:
        base = ROOT / "examples" / slug
        rtl = [base / "rtl" / name for name in sources]
        tb = base / "verif" / f"{top}.sv"
        vvp = BUILD / f"{slug}.vvp"
        run(["iverilog", "-g2012", "-s", top, "-o", vvp, *rtl, tb],
            OUT / f"{slug}-reset-compile.log")
        text = run(["vvp", vvp], OUT / f"{slug}-reset-sim.log")
        if f"ASYNC_RESET_OBSERVED {'codec decoder' if slug == 'heldout_codec64' else 'search controller'}" not in text:
            raise AssertionError(f"Reset marker absent: {slug}")
        results.append({"ip": slug, "scope": "specified synchronous reset versus observed preclock assertion",
                        "observed": "output cleared before next rising clock edge",
                        "rtl_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in rtl},
                        "testbench_sha256": hashlib.sha256(tb.read_bytes()).hexdigest()})
    (OUT / "reset-observations.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
