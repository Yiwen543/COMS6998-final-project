# Experiment evidence index

All coverage counters in these directories are original DUT counters. Live,
development, mock and replay results have different roles and are not pooled.
Each dated report in `docs/` defines its own frozen source, budget and target.

| Evidence | Directory | Role |
| --- | --- | --- |
| Starter arbiter | `step1/` | Deterministic integration and exhaustive reference ceiling |
| Initial model pilots | `pilot_live_20261020/`, `fifo_live_20261020/`, `ttc_live_20261020/` | Historical matched A/B/C live runs |
| Queue milestone | `queue_bc_gpt6sol_20261026/` | Milestone 1 B/C live result, replay comparison and Claude audit |
| Candidate screens | `heldout_queue_preflight/`, `midterm_candidate_preflight/` | Source mapping, reachability, proof and selection evidence |
| Divider trial | `divider_abcp_frozen_live_20261030/`, `divider_abcp_frozen_replay_20261030/` | Frozen A/B/P/C live run and model-free replay |
| FIFO stress trial | `sfifo_stress_abpc_frozen_live_20261030/`, `sfifo_stress_abpc_frozen_replay_20261030/` | Frozen A/B/P/C live run and model-free replay |
| Other `*_development_*`, `*_mock_*`, `*_replay_*` | Named directories | Selection/debugging or validation only; not additional independent live repetitions |

Keep rendered prompts, model call envelopes, actions, raw `.dat` coverage,
summaries, proof logs, replay validation and audit dispositions. Compiler output
under `verilator-build/` and plotting/cache directories are disposable and
ignored by Git. Run `make clean-generated` from the repository root after local
tests; it does not delete the evidence listed above.
