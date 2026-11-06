# Milestone 1 result report - GPT-6 Sol queue B/C pilot

**Run date:** 26 October 2026. **Source commit:** `66051b681d3f75e0e68370271a743e637820ac1b`. **Primary artifact:** [`results/queue_bc_gpt6sol_20261026/`](../results/queue_bc_gpt6sol_20261026/). The run used the exact `gpt-6-sol` model through the official OpenAI Responses API; every returned model identifier was `gpt-6-sol`.

## Question and experimental boundary

The proposal asks whether E-graph semantic feedback helps an LLM verify RTL more efficiently than text-only or raw coverage feedback. This milestone isolates the primary **C versus B** comparison on one CVDP queue IP and an independently equivalence-checked syntax variant. B receives the specification, RTL, common seed, checker logs, and raw uncovered DUT counters. C receives all that plus bounded Rust `egg` groups of source-distinct, typed, complete activation guards. The fixed SystemVerilog driver accepts only validated JSON cycle actions. The model cannot edit the DUT, checker, simulator settings, or coverage parser. The directed reference ceiling and solver witnesses are withheld from both prompts. This experiment measures stimulus refinement under a supplied checker, **not** free-form SystemVerilog testbench/assertion generation or CVDP pass@1.

The preregistered target is 41/41 actual Verilator DUT line/case counters. Each arm/version has three independent repetitions and four refinement rounds with at most four new actions per round, low reasoning effort, 4,096 output-token cap, 90-second timeout, and at most two retries. Each round starts a fresh simulator process and replays the same six-cycle initialization plus all accepted actions; every executed cycle and simulator call is counted. The two RTL files are versions of **one** IP, not independent designs. The original DUT and specification are frozen; the checker separately models queue occupancy and front data, reset, clear, and enable hold under a **three-valid-item contract**. This contract matches the RTL's full threshold for DEPTH=4, while the prose does not independently specify a numeric capacity and calls DEPTH the number of entries. A fourth write is excluded. Ambiguous almost-full/empty timing is not scored during ordinary operation. Thus the checker is independently implemented and fault-tested for this narrower contract, not a proof of full-spec correctness.

## Live measurements

| Version | Arm | First target rounds, reps 1-3 | Mean API tokens to target | Mean cycles to target | Mean simulations to target | Final coverage, all reps |
|---|---|---|---:|---:|---:|---|
| Original | B raw | 3, 4, 4 | 74,891 | 56.7 | 3.67 | line 41/41, branch 14/14, toggle 344/408 |
| Original | C egg | 3, 4, 3 | 73,738 | 49.3 | 3.33 | line 41/41, branch 14/14, toggle 344/408 |
| Variant | B raw | 3, 3, 3 | 70,272 | 42.0 | 3.00 | line 41/41, branch 14/14, toggle 344/408 |
| Variant | C egg | 2, 3, 3 | 66,377 | 36.0 | 2.67 | line 41/41, branch 14/14, toggle 344/408 |

C reached the target one round earlier in **2/6** paired repetitions and tied in **4/6**; B reached earlier in none. The paired mean C-minus-B target cost was **-1,152 API tokens** on the original and **-3,895 API tokens** on the variant; it used an average **7.3** and **6.0** fewer cumulative executed cycles, respectively. C's first-round prompt cost was higher by exactly 1,508 input tokens on the original and 1,552 on the variant, since it included semantic groups. At the fixed four-round endpoint all arms reached the same line/branch/toggle totals, and no checker-detected defect category appeared. Across 24 paired round endpoints, C had more toggle points in 9, fewer in 3, and the same count in 12. Paired action batches were identical in only 1/24 rounds, so identical final coverage does not mean identical generated stimuli.

The live run used **48 model calls**, all accepted on the first attempt, **zero retries**, 944,948 API-reported input tokens and 11,774 output tokens (956,722 total). It executed 48 arm-specific simulations and 768 replay-counted cycles; two compilations, two common-seed simulations, and two separate reference-ceiling simulations are reported separately. The complete live runner took 247.3 seconds on this host, including setup and plotting. First-round B/C prompts were checked in all six matched pairs: the common system and user information were byte-equivalent after removing C's sole `egg_normalization` field. Later prompt contents naturally diverge when earlier generated actions and measured coverage diverge. Cached and reasoning token subcounts are included within API totals, never added again.

These are descriptive pilot observations, **not** evidence of a statistically significant or generalizable E-graph effect. The apparent C advantage in this model/run is small and is absent at final coverage; a previous matched `gpt-6.1-sol` queue pilot reached the same target in round 3 for every B and C repetition and cost C more tokens. Model response stochasticity, one IP with two syntax variants, and a target close to the coverage ceiling limit causal confidence. All 12 selected read/write counters per version were already covered after round 1, so C's later semantic groups were empty. The observed earlier target crossings cannot be specifically attributed to these equivalent guards. The next experiment needs multiple independent designs, harder reachable targets, and a length-matched placebo semantic appendix.

## Independent validation and Claude Code audit

The separate replay used the saved accepted actions, recompiled the fixed sources, and reproduced **48/48** round rows across **33 stable fields** each, as well as **52/52 byte-identical raw Verilator coverage files** (including common seed and reference ceiling). Four queue checker/isolation tests and four typed predicate/source-provenance tests passed. The `egg` pipeline has 49 extracted targets and 18 explicitly unsupported expressions per version; selected equivalent guards are independently Z3 checked under stated two-state combinational semantics, with event/reset context kept separate. All source locations and unmatched raw counters remain in the denominator. A coverage hit is never transferred to another source line because guards are equivalent.

**Claude Code independent review:** completed with CLI 2.1.310 and the returned `claude-opus-5-5` model. An earlier CLI 2.1.126 attempt failed because that version does not support Opus 5.5; it produced no audit. The blinded pass independently recomputed all 12 target-cost rows and found no arithmetic discrepancy. Its claim of a pre-feedback round-1 imbalance was corrected: round 1 already carries the B/C treatment. The unblinded pass confirmed the narrow observed C advantage, pointed out that the selected guard groups disappear after round 1, and challenged checker capacity and fourth-slot assumptions. We checked each against the frozen specification, RTL, checker, live vectors, raw counters, and separate replay. The reviewer did **not** itself run replay or inspect `.dat` files; its narrative is not the measurement oracle. The row-by-row adjudication is in [`claude_audit_v2/disposition.md`](../results/queue_bc_gpt6sol_20261026/claude_audit_v2/disposition.md). The CLI reported about $0.21 for the blind pass and $1.67 for the unblinded pass; those audit costs are separate from GPT-6 Sol stimulus tokens and simulator costs. It identified a presentation issue: the generated `REPORT.md` rounds mean simulator counts to integers; the exact CSV and the table above retain 3.67/3.33 and 3.00/2.67.

## Reproducibility

- Frozen settings and SHA-256s: [`configs/queue_bc_pilot_gpt6sol.json`](../configs/queue_bc_pilot_gpt6sol.json) and [`metadata.json`](../results/queue_bc_gpt6sol_20261026/metadata.json).
- Per-call outputs and rendered prompts: [`calls.jsonl`](../results/queue_bc_gpt6sol_20261026/calls.jsonl) and `prompt-*.json` alongside it. Per-round counters and costs: [`rounds.csv`](../results/queue_bc_gpt6sol_20261026/rounds.csv), [`target_costs.csv`](../results/queue_bc_gpt6sol_20261026/target_costs.csv), and raw `.dat` files in each RTL directory.
- Plots: [`original`](../results/queue_bc_gpt6sol_20261026/comparison-original.png) and [`variant`](../results/queue_bc_gpt6sol_20261026/comparison-variant.png), each showing line coverage versus tokens, cycles, simulator executions, and wall time.
- Replay proof: [`replay-verification.json`](../results/queue_bc_gpt6sol_20261026/replay-verification.json). Prompt isolation: [`prompt-isolation.json`](../results/queue_bc_gpt6sol_20261026/prompt-isolation.json). Saved 22 independent Z3 group-member checks: [`semantic-proof.json`](../results/queue_bc_gpt6sol_20261026/semantic-proof.json). Tool versions: Verilator 5.050, Icarus 12.0, Yosys 0.70+post, Rust/Cargo 1.99.0, Python 3.13.9, OpenAI SDK 2.54.0, Matplotlib 3.11.2. The source commit is recorded above; this milestone adds uncommitted scripts/configuration/result artifacts on top of it.

From the repository root, replay without API access:

```sh
.venv/bin/python scripts/run_queue_bc_pilot.py --mode replay \
  --config configs/queue_bc_pilot_gpt6sol.json \
  --replay-calls results/queue_bc_gpt6sol_20261026/calls.jsonl \
  --output build/queue_gpt6sol_replay_new
python3 scripts/verify_queue_live_replay.py \
  --live results/queue_bc_gpt6sol_20261026 \
  --replay build/queue_gpt6sol_replay_new \
  --output build/queue_gpt6sol_replay_new/verification.json
```

To start a **new paid live run** with the same limits, use an unused output directory and keys already exported in that terminal (never put key values in commands or files):

```sh
.venv/bin/python scripts/run_queue_bc_pilot.py --mode live \
  --config configs/queue_bc_pilot_gpt6sol.json \
  --output results/queue_bc_gpt6sol_new
.venv/bin/python scripts/run_claude_queue_audit.py \
  --source results/queue_bc_gpt6sol_new \
  --output results/queue_bc_gpt6sol_new/claude_audit \
  --max-budget-usd 3.00
python3 scripts/export_queue_semantic_proof.py \
  --result results/queue_bc_gpt6sol_new \
  --output results/queue_bc_gpt6sol_new/semantic-proof.json
```

The Claude audit needs Claude Code 2.1.280 or newer and `ANTHROPIC_API_KEY`; the live generator needs `OPENAI_API_KEY`. An API key and model access were verified for this run, but the temporary 0600 handoff file was deleted after completion. The PDF authoring script is [`write_milestone1_pdf.py`](../scripts/write_milestone1_pdf.py); it uses the Codex bundled ReportLab runtime and requires a short human-checked audit disposition in `--review`.

The draft literature and methodology matrix is in [`milestone_2026-10-26.md`](milestone_2026-10-26.md). CVDP and LLM4Cov evaluate their own benchmark protocols with pass/coverage outcomes; ROVER, ASPEN, SmoothE, and e-boost primarily evaluate optimization or extraction quality. Those numbers cannot be imported as evidence that our C arm helps verification. The November 6 midterm should present the actual trajectories and audit, and the November 9 Milestone 2 should preregister independent held-out IPs plus the A text-only control.

## Next steps: formal validation

Before using each new IP in the B/C comparison, we will add open-source formal checks alongside simulation. Yosys equivalence checking will compare the frozen RTL with any transformed variant under documented clock and reset assumptions. SymbiYosys with an SMT solver will check specification-derived properties such as reset behavior, occupancy bounds, and absence of overflow or underflow for legal inputs. We will save proof status, bounds, assumptions, and counterexamples, and report any property that remains unproven. These checks will strengthen confidence in the IP's usability and formal consistency; they will not turn high coverage or bounded proofs into a claim of complete correctness.
