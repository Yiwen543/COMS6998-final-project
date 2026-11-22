#!/usr/bin/env bash
# Rebuild the two engines and run the frozen Milestone 3 comparison.
set -euo pipefail

if [[ $# != 1 ]]; then
    echo "Usage: bash scripts/run_milestone3.sh NEW_OUTPUT_DIR" >&2
    exit 2
fi
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
base=71e99c4cbef9768abc1b20d4d344eaee8594db59
mkdir -- "$1"
cd -- "$1"
work=$PWD
export PYTHONDONTWRITEBYTECODE=1
mkdir -p build/v1
git -C "$root" archive "$base" egraph/Cargo.toml egraph/Cargo.lock egraph/src results/step1 | tar -x -C build/v1
for tool in rustc cargo python3 verilator z3; do
    "$tool" --version
done | tee versions.txt

CARGO_TARGET_DIR="$work/build/v1-target" cargo build --locked --release \
    --manifest-path build/v1/egraph/Cargo.toml --bin guard_proofs_fast
CARGO_TARGET_DIR="$work/build/m3-target" cargo build --locked --release \
    --manifest-path "$root/egraph/Cargo.toml" --bin guard_proofs_fast
binaries=(--baseline-binary "$work/build/v1-target/release/guard_proofs_fast"
          --binary "$work/build/m3-target/release/guard_proofs_fast")

python3 "$root/scripts/m3_guard_inputs.py" --output arbiter-inputs
python3 "$root/scripts/fetch_m3_reference.py" --output reference-inputs
python3 "$root/scripts/benchmark_m3_engine.py" "${binaries[@]}" --repeats 12 \
    --input arbiter-inputs/control.json --input arbiter-inputs/ground.json \
    --input reference-inputs/controller.json --input reference-inputs/spi.json \
    --input reference-inputs/i2c.json --output engine
for profile in source certified; do
    python3 "$root/scripts/benchmark_m3_rtl.py" "${binaries[@]}" --repeats 6 \
        --profile "$profile" --reference-dir "$work/build/v1/results/step1" --output "rtl-$profile"
done
