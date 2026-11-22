#!/usr/bin/env bash
# Run the proof applications on pinned inputs with the two Milestone 3 binaries.
set -euo pipefail

if [[ $# != 3 ]]; then
    echo 'Usage: bash scripts/run_m3_proof_applications.sh M3_BASE_RUN CONTROLLER_FIXTURE NEW_OUTPUT_DIR' >&2
    exit 2
fi
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
base_run=$(cd -- "$1" && pwd)
fixture=$(cd -- "$2" && pwd)
screen="$fixture/qualification/typed-v5/screen"
indexed="$base_run/build/m3-target/release/guard_proofs_fast"
baseline="$base_run/build/v1-target/release/guard_proofs_fast"
for file in "$indexed" "$baseline" "$screen/egg-input.json"; do
    [[ -f "$file" ]] || { echo "Missing required input $file" >&2; exit 1; }
done
mkdir -- "$3"
out=$(cd -- "$3" && pwd)
cd -- "$root"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/m3_controller_withdrawal.py --screen-dir "$screen" \
    --baseline-binary "$baseline" --binary "$indexed" --output "$out/proof-withdrawal"
python3 scripts/m3_controller_basis.py --fixture "$fixture" --binary "$indexed" --output "$out/proof-basis"
for policy in ordinary_forest proof_dependencies; do
    python3 scripts/m3_controller_basis.py --fixture "$fixture" --binary "$indexed" \
        --qualify "$policy" --output "$out/qualify-$policy"
done
python3 scripts/m3_proof_dependencies.py --input "$screen/egg-input.json" \
    --graph results/milestone3/engine/profile-2/reference.json --using-rule qfbv-g59-g83 \
    > "$out/qfbv-g59-g83.json"
python3 scripts/m3_eco_replay.py --output "$out/eco-replay"
python3 scripts/m3_eco_impact.py --binary "$indexed" --replay-evidence "$out/eco-replay/summary.json" \
    --output "$out/eco-impact"
python3 scripts/m3_coverage_waiver.py --binary "$indexed" --output "$out/coverage-waiver"
python3 scripts/m3_coverage_waiver.py --check-waiver "$out/coverage-waiver/waiver.json" \
    --rtl examples/arbiter/rtl/fixed_priority_arbiter.sv --coverage "$out/coverage-waiver/original/witness.dat"
