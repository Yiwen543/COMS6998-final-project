# E01 actual B/C known-benchmark retest

The exact authorized R03 entry ran once, exited0 and completed in 177.995s. Independent P19 acceptance remains pending. No extra scoring, compilation, replay, API or Git mutation follows this execution.

| Arm / round | Correct controls | Ordinary safety definite pairs | Response finite pairs | Input finite pairs | Raw union types | Oracle unresolved |
|---|---|---|---|---|---|---|
| B2_raw / 1 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |
| C2_semantic / 1 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |
| B2_raw / 2 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |
| C2_semantic / 2 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |
| B2_raw / 3 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |
| C2_semantic / 3 | PASS18/18 | 106/106 | 20/20 | 0/10 | 11/12 | 38/162 |

The raw denominator is twelve fault types and144fault pairs per candidate, plus18correct controls. Nine types receive ordinary-safety credit; two (N02/N03) receive end-marker case-level finite credit marked UNATTRIBUTED, not category-specific monitor proofs. Safety106/106 is definite evidence; only68/106 is fully resolved because38pairs retain oracle unknown. Response20/20 is fully resolved. These categories overlap and must not be added as disjoint counts. No sample is silently dropped.

N10 is a mutant identifier, not a denominator of ten. Its twelve frozen reference outcomes are PASS and it has no eligible fault pair. The input-completion0/10 instead concerns N01: those ten cases also have safety FAIL and oracle unknown. N10 is not a newly found LLM failure; the reference is not repaired, unknowns do not become PASS and the raw12 denominator remains.

| Arm | Actual input | Actual output | Total | Conservative usage upper USD |
|---|---:|---:|---:|---:|
| B2_raw | 116529 | 7134 | 123663 | 0.758621 |
| C2_semantic | 127168 | 6747 | 133915 | 0.810750 |

C used 8.290273% more total tokens, with identical first-round and final outcomes; the conservative dollar upper is 6.871547% higher. Total257578tokens,6generation requests,0remote counts/retries/unknown usage. Reported cached-input tokens0 and reasoning1200 are subsets, not additional totals. Cost upperUSD1.569371 is not a provider invoice. No extra API call queried billing.

Each dispatch reservedUSD5.910168; ledger journal peak outstandingUSD7.207377, belowUSD20. Gross historical reservesUSD35.461008 reflect sequential reuse of released unused reservations, not spend or simultaneous commitments. Settled upperUSD1.569371, unresolved reserves0, unused reservation releaseUSD33.891637. A release is not a refund. Billing assumptions are the exact independently reviewed fixed model/tier/cache/region basis; no arbitrary provider price-drift guarantee is inferred.

One actual local pass used12compile roots (6Yosys/6Iverilog),990monitor replay roots and204444replayed cycles:18development replays/1380cycles plus972grading replays/203064cycles. These are monitors on frozen DUT observations, not new stimulus generation or new physical DUT executions. All1008child receipts are complete. No timeout, new DUT/native/formal/G1/cross-IP or tool-version query was added. Parent wall177.994570s includes cleanup; worker/grade/child timings overlap, are not CPU measurements and must not be summed as independent stage cost. CPU, memory and exhaustive child census remain unknown.

The source/registration/model/limits, Claude independent reference, GPT candidate roles, trace_done finalpost ABI and fixed public packets remained frozen. B receives public/raw feedback; C adds only the old verified E-graph package. Each arm has one independent session and three own-history rounds in B1,C1,C2,B2,B3,C3 order. Six candidates froze before the one common scoring pass; both finals select round3. No evaluation score was returned to a candidate. Source and prompt/release hashes are retained for independent inspection.

This is a retest of a previously published corpus, not a fresh hidden evaluation. Both arms saturate the currently observable type set in round1; this run supplies no extra C detection benefit and has higher C token cost. One trajectory per arm and no token-matched placebo limit causal/statistical interpretation. Passing18finite correct controls does not prove general monitor soundness, unbounded behavior,128cycle completion or E-graph semantic advantage. No formal proof was run for these new monitors.

A progress message initially associated N10 with input completion; saved-evidence inspection corrected that description above. The raw results were never relabeled. All historical negative outcomes,38unknowns per round, old formal timeouts, G1 limits and earlier scores remain unchanged.

The original exact command and escalation are in entry.json; output roots cannot be restarted. bindings.json pins the accepted review/EXECUTE, source/reg/preparation, actual ledger/release/grade/parent receipts. analysis.json and child-resource-summary.json derive from saved outputs only. snapshot-manifest.json uses repository-root-relative paths and binds this audit plus every actual run/supervision artifact. Staged credentials, environments and caches are excluded; the auditor never reads/hashes key contents. Key remains staged for the agreed completion policy. Next: existing P19 independently reviews saved evidence, then root handles separately authorized publication. Do not invoke new API/native/score/compile/replay merely to recover context.
