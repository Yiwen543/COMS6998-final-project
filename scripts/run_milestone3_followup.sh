#!/usr/bin/env bash
# Reproduce the follow-up from a completed original six-arm run. No model API calls.
set -euo pipefail
if [[ $# != 2 ]]; then
    echo "Usage: bash scripts/run_milestone3_followup.sh ORIGINAL_M3_RUN NEW_OUTPUT_DIR" >&2
    exit 2
fi
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
original=$(cd -- "$1" && pwd)
mkdir -- "$2"
work=$(cd -- "$2" && pwd)
cd -- "$root"
export PYTHONDONTWRITEBYTECODE=1
export GUARD_PROOFS_FAST="$original/build/m3-target/release/guard_proofs_fast"

python3 -m unittest discover -s tests -p 'test_m3_rtl_gates.py' -v
python3 -m unittest discover -s tests -p 'test_m3_controller*.py' -v
python3 scripts/m3_stimulus_ablation.py --rtl-run "$original/rtl-certified" --output "$work/ablation"
python3 scripts/m3_controller_replay.py --fetch "$work/fixture"
python3 scripts/benchmark_m3_controller.py --fixture "$work/fixture" --binary "$GUARD_PROOFS_FAST" \
    --timeout-ms 2000 --repeats 6 --output "$work/controller"
python3 scripts/check_m3_controller_witnesses.py --fixture "$work/fixture" --run "$work/controller" \
    --output "$work/prefixes"
python3 scripts/m3_controller_replay.py --check-passivity "$work/fixture" --output "$work/passivity"
python3 scripts/check_m3_formal.py --output "$work/formal"
python3 scripts/audit_m3_online_usage.py --source-dir results/milestone3/online-usage --output "$work/online-usage"
