# FIFO stress pilot: Claude pre-outcome audit disposition

Claude Code 2.1.310, requested and returned `claude-opus-5-5`, reviewed the
candidate with Read/Glob/Grep only before any A/P/C live trial. Its original
[review](../results/sfifo_stress_claude_preaudit_20261030/review.txt) is
preserved unchanged. It recommended **no-go as initially specified**. The
following repairs were made before freezing any formal run.

| Finding | Disposition and check |
| --- | --- |
| Fixed checker capacity not inspected; stale docstring | `run_sfifo_stress_fixed.py` passes `capacity=16` explicitly. `sfifo_fixture.py` now documents parameterized capacity. Original FIFO, stress variant and independent behavioral control passed 318 public-I/O checks in each of Icarus and Verilator directed runs; the data-order mutant fails. |
| Four counters are two equivalent events | Primary target is explicitly two late events, represented by four distinct original Verilator branch/`if` source counters at lines 91/161 and 96/179. Both pairs pass egg grouping and Z3 pair checks, are zero-hit in seed, and positive-hit in separate calibration. Original counters remain separate and the full raw denominator is retained. |
| Line 129's similar guard was omitted by the extractor | The current pre-`proc` frontend does not prove its *complete activation guard* equivalent to the 96/179 group, because priority case atoms remain opaque. It is therefore not promoted into C's e-class or the primary target. Its original raw counter remains in B and C and in the branch denominator. This is a stated extraction limitation, not an unreachable or nonequivalent claim. |
| Line coverage saturated in B round 1 | Line is retained as a raw descriptive measure, not a target. The primary target uses four late branch source counters. |
| Model-visible spec revealed near-full/wrap and E-graph terminology | The model-visible `docs/specification.md` now states only public FIFO behavior. Variant provenance and synthetic redundancy are in a separate README, withheld from all four prompts. The full RTL remains visible equally to A/B/P/C. |
| C group selection used calibration reachability | C feedback now includes source-mapped, Z3-checked currently uncovered groups without filtering on calibration hits. Calibration is used only for DUT selection. The four groups shown here are unchanged. |
| P provenance unresolved | `run_sfifo_stress_experiment.py` constructs the hypothetical C message from **P's own** `history`, `prior`, trace and raw points at each attempt, then replaces only the egg field. Unit tests check common B fields and absence of egg content. Retry prompts are rematched. The OpenAI `input_tokens.count` endpoint is authoritative; mismatch beyond two tokens fails closed. Count calls and wall time are separate from model generation usage. |
| 20/24 branch threshold chosen after B plateau | Removed. The target is solely the four late source counters selected by structural preflight, not the observed B branch count. All 24 raw branch points are still reported. |
| Five rounds give little slack over a 32-cycle lower bound | Six rounds of at most eight new cycles give 48 new cycles. Every execution replays the four-cycle seed plus accepted history and new batch; the model cannot edit the reset/clock driver. Missed targets remain in the result. This remains a demanding small pilot and could show a floor effect. |
| Equivalence proof scope overstated | Yosys `equiv_simple` proved all 157 paired cells. `equiv_induct` had zero cells left. The fixed 8-bit, depth-16, two-state state-correspondence scope is now explicit in the README and screen; it is not a four-state, all-parameter, or full-specification proof. |
| Candidate selection/generalization | This is an independent FIFO IP relative to the divider, but **a synthetic stress variant of a previously examined ZipCPU FIFO**, not a second naturally redundant CVDP benchmark. It tests the feedback mechanism; it cannot establish generalization to natural RTL. The earlier screens covered the pinned CVDP slices and the original FIFO; their negative gates remain reported. |

The prospective [config](../configs/sfifo_stress_abpc_frozen.json) defines
three repetitions per arm, six rounds and eight new cycles per round. The
[checker/feedback tests](../tests/test_sfifo_stress_feedback.py) and
[preflight](../results/midterm_candidate_preflight/sfifo-stress/screen.json)
pass after these changes. The frozen manifest will record hashes before the
first formal A/B/P/C model call. No positive E-graph outcome is assumed.
