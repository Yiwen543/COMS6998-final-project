# 01_question

Our project asks whether semantic feedback can help large language models verify RTL more efficiently and correctly. Raw coverage tells us which source points remain unhit, but it may not explain their relationship. An E-graph compactly groups expressions that are equivalent within a checked semantic scope. Our proposal is to add those relationships to the feedback loop, then measure coverage efficiency, monitor correctness, and fault detection. We keep two distinctions clear: coverage is not correctness, and a semantic group never replaces the original RTL coverage counters.

---

# 02_prototype

Here is our implemented prototype. Python coordinates frozen specifications and RTL, GPT generation, compilation, tool checks, and feedback for the next round. A Rust egg pipeline builds restricted E-graph groups; typed guards and Z3 checks protect widths and activation context. We study two different tasks. The original track generates stimulus sequences and measures actual RTL coverage. Test two holds stimuli fixed and generates passive SystemVerilog monitors for hidden faults. Icarus and Verilator supply physical simulation, while Yosys and SMT supply formal diagnostics. Claude's independent reference remains separate from GPT's candidates. Our equivalence checks cover restricted two-state guards, not general sequential or four-state correctness. Mingyuan will explain the comparison.

---

# 03_methodology

Our baseline B receives raw coverage and common development feedback. C receives everything in B plus verified E-graph guard groups. In the latest test-two cohort, we fixed the DUT, Claude checker, stimuli, and model: gpt-six-point-one-sol with low reasoning. Each arm had three independent sessions and six rounds, with the same input and output caps. We generated and froze all thirty-six candidates before hidden grading. Hidden faults, evaluation traces, and reference code never entered candidate prompts. We also saved actual token usage, compilation failures, and unresolved outcomes. Equal caps do not mean equal spending. Without a token-matched placebo, this cohort compares the complete feedback package, not pure semantic causation.

---

# 04_queue_results

Our first result is an exploratory stimulus-generation pilot on one queue IP in two RTL forms, using gpt-six-sol. The graph shows mean input-plus-output tokens to reach all forty-one emitted line or case points. B versus C used about seventy-five versus seventy-four thousand tokens on the original, and seventy versus sixty-six thousand on the syntax variant. C reached the target one round earlier in two of six index-matched comparisons; four tied. All twelve runs ended at the same line, branch, and toggle coverage shown below. This is a small, mixed efficiency signal, not a causal result: the selected guard members were already hit after round one. Yiwen will present test two.

---

# 05_test2_results

In the latest fixed-stimulus controller study, all six final monitors passed correct-DUT controls and detected all eleven observable fault types. The twelfth type remained unobserved and stays in the raw denominator. Across all rounds, B used about seven hundred forty-one thousand tokens and C about eight hundred fourteen thousand: nine-point-eight-six percent more, with no extra final fixed-trace kills. Formal results need a separate interpretation. Of five hundred forty checks, three hundred sixty-one timed out. The fail modes shown here must not be pooled as detected faults. Ninety-four BMC failures yielded twenty physical alarm reproductions and seventy-four unresolved witnesses. C covered more mutant types in an earlier-prefix diagnostic, seven versus three, but this is not same-sample oracle confirmation or a proof of one-hundred-twenty-eight-cycle completion.

---

# 06_analysis

The main contribution so far is a working, reproducible pipeline with frozen candidates, independent grading, replay, and explicit coverage and cost accounting. The evidence does not yet establish a general E-graph advantage: the queue signal is small, and the latest monitor endpoint is saturated. For the November ninth P-two submission, we propose three steps. First, use unsaturated held-out temporal obligations that separate safety from finite completion. Second, add a token-matched placebo to isolate semantic value. Third, qualify the formal-to-physical mapping, especially four-state behavior, while preserving unknowns. Controlled R-zero, R-one, and R-two recovery comparisons remain planned. Our feedback question is: should we prioritize temporal completion, or the semantics-only ablation?
