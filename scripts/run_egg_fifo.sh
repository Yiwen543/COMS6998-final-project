#!/usr/bin/env bash
# Audit the assertion formulas, check actual RTL, and replay solver witnesses.
set -euo pipefail

if [[ $# != 2 ]]; then
    echo 'Usage: bash scripts/run_egg_fifo.sh CONTROLLER_FIXTURE NEW_OUTPUT_DIR' >&2
    exit 2
fi
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
fixture=$(cd -- "$1" && pwd)
mkdir -- "$2"
out=$(cd -- "$2" && pwd)
cd -- "$root"
export PYTHONDONTWRITEBYTECODE=1
cargo_dir="$out/build-egg"
CARGO_TARGET_DIR="$cargo_dir" cargo build --locked --release \
    --manifest-path egraph/Cargo.toml --bin egg_assertion_forms
python3 scripts/egg_fifo_assertion_forms.py --binary "$cargo_dir/release/egg_assertion_forms" \
    --output "$out/forms"
rtl="$fixture/public/rtl/axis_fifo.v"
python3 scripts/egg_fifo_formal.py --rtl "$rtl" --output "$out/formal"
python3 - "$out" <<'PY'
import json
from pathlib import Path
import sys

out = Path(sys.argv[1])
certified = json.loads((out / "forms/assertion-contract.json").read_bytes())
formal = json.loads((out / "formal/summary.json").read_bytes())
if formal["forms"] != certified:
    raise SystemExit("the Boolean certificate and the formal assertion formulas differ")
PY
python3 scripts/egg_fifo_replay.py --rtl "$rtl" --formal-run "$out/formal" --output "$out/replay"
