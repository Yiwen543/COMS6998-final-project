# Queue stimulus-efficiency ablation — offline design v1

Status: **draft; live disabled; new budget not approved; no runnable new experiment claimed**.
Prepared 2026-11-07 against actual HEAD `034a5a8db63f38878148aaac15ea69dbc150d29a`.
This is the original stimulus-generation track: one published queue IP in two equivalent source forms.
It is separate from `test2`'s fixed-stimulus candidate-monitor study; their samples, targets and ROI must not be pooled.

## Question and controlled comparison

Does a compact structural description, then a certified equivalent-guard description, reduce the resources needed by an LLM to reach a fixed raw DUT coverage target?

| Arm | Candidate information |
| --- | --- |
| baseline | Per-form full RTL, public contract, ordinary raw uncovered counters/source snippets/case selectors, own accepted actions and bounded latest feedback |
| yosys | Identical common packet plus deterministic Yosys structural digest, at most 2,048 UTF-8 bytes |
| yosys_egg | Identical Yosys packet plus cached certified complete-guard groups, at most 2,048 additional UTF-8 bytes |

These are proposed packets, not built or token-qualified artifacts. Structural and guard appendices persist each round; the old C groups disappeared after its first generated batch. Preserve complete typed guards, source membership, provenance and clock/reset context; exceed a cap ⇒ stop qualification, never truncate semantics. Keep read/write groups separate and every source counter distinct. Baseline already receives RTL structure and Yosys-assisted case-selector joins, so Yosys is an additional compact organization of facts. The three-arm comparison estimates whole feedback-package effects; it does not isolate semantic information from prompt length. No fourth placebo is implicitly added.

All arms use the same DUT binding, parameters, independent reference/property versions, raw counter definitions, model settings and resource ceilings. No candidate sees another session/form's RTL or history, reference implementation, prior pilot actions/results, private directed calibration, solver witnesses, or maintainer skills/instructions. Freeze exact allowlists and payload hashes before live.

## Common contract, authors and remaining ambiguity

The sole operating-domain authority is [queue_efficiency_contract_v1.json](../queue_efficiency_contract_v1.json), SHA256 `229ab3b3d99c597bba92a367e7697ef39bc1c039098b395382773cff9b94cc64`, alongside its bound public spec. DEPTH=4, DBITS=32 and effective capacity 3 are **explicit narrow benchmark assumptions**, not a proof of complete original CVDP conformance. Use that contract's simultaneous-read/write domain, exclusions and unknown handling; do not invent a competing legal subset. Almost flags are recorded, not functionally graded. Exact pre/post-edge and asynchronous-reset sampling ABI remains pending infrastructure and independent acceptance.

The initial independent property v1 excluded simultaneous enabled R/W, which conflicts with source points needed for the full line/branch target. V1 is preserved; the same isolated author completed contract-aligned static v2 in `docs/designs/queue_property_author_v2/`. P21 reports no explicit internal contract contradiction and that the exclusion conflict is removed. This is **NOT_IMPLEMENTED / NO_EXECUTE**, not a tested monitor or physical reachability evidence. Bind the v2 obligations SHA256 `7a40800c4e7aa52520a01081f44c60dc5eb6911d808582007a4f92afc8cc9655` and input-receipt SHA256 `18dc3766cc9a419aedc9eec5cbbd7acd16212f2d60c9290f5bb7f9ade6850c4a`; ABI and independent controls remain pending.

| Role | Actual state and allowed inputs |
| --- | --- |
| Infrastructure producer | Driver, codec, coverage, ledger and call orchestration only; does not author oracle/property truth logic |
| Property author | Distinct fresh Codex agent `/root/queue_property_author`; static public-spec/contract v2 complete, frozen ABI still pending; no DUT, old checker, golden implementation, egg or candidate outcomes; no tested executable monitor |
| Golden author | Future independent `claude-opus-5-5`; same spec/contract/ABI, no property implementation or forbidden inputs; not called |
| Reviewer | Existing separate P21 Codex reviewer; neither author; final technical and actual Hallmark critique pending |

`scripts/queue_reference.py` contains private directed calibration stimulus, not a golden model. The old `tb_queue_pilot.sv` combines an abstract model and checks; the saved Claude cross-review was a review, not evidence of Claude authorship. Reuse diagnostic/sampling infrastructure only after separation and ABI qualification. Behavioral control models and injected failures are qualification controls, not real DUT mutants, RTL coverage, or independent oracle truth.

## Fixed workload, endpoint and stopping

Two forms × three arms × three independent sessions = **18 sessions**, at most four logical rounds/session and four new action cycles/round. Candidate output is JSON stimulus only: 1–4 actions, exact six fields, binary integer controls, unsigned 32-bit integer data; reject booleans, malformed and illegal/unsupported actions without silently repairing them. The six-cycle seed is fixed (two reset cycles, four disabled idle cycles). Identifier 6998 describes the historical setup, not a provider random seed.

Primary target: **line 41/41 AND branch 14/14 AND toggle ≥344/408**. Report expression counters separately: original 16, variant 40. Keep all 408 toggle directions in the denominator; the saved 64 missing directions are not an unrestricted unreachability proof. Freeze raw point identities and contract compatibility before live; instrumentation changes require a new registration, not denominator adjustment.

Check the target at round 0 and after each qualified simulation. A round-0 hit means zero generation calls/tokens and a non-discriminating endpoint, not permission to change the target. Stop a session at its first hit; mark later slots `NOT_RUN_TARGET_ALREADY_MET`. Round-major scheduling with rotating arm order and alternating form order is fixed in `plan.json` before any new candidate outcomes.

Report schema/functional validity and attainment rates first, then final raw coverage and unresolved/abort states, then actual input/output tokens, calls, physical simulation/replay cycles and wall cost to target. Right-censor unreached/aborted runs, retain every incurred cost, and show restricted cost with attainment rather than a success-only mean. Secondary line-only cost remains separate. Branch ROI is new raw branch points above seed 6 per 1,000 actual input+output tokens; rounds are adaptive history, not independent replicates. Three sessions/arm and two forms of one IP do not support a general or statistical benefit claim.

## What the saved pilot establishes

`old-pilot-summary.json` is fresh static arithmetic over saved data, **not a rerun**. Historical model was `gpt-6-sol`; all new arms propose `gpt-6.1-sol`, so this is not literal old-model replication. Old execution ran all four rounds even after target attainment; all 956,722 actual tokens remain recorded.

| Saved measurement | Value |
| --- | --- |
| Sessions / accepted generation calls / retries | 12 / 48 / 0 |
| Actual input / output / total tokens | 944,948 / 11,774 / 956,722 |
| Cached input / reasoning output (subsets, not additions) | 357,911 / 5,889 |
| Per-call input min / median / max | 9,367 / 13,468.5 / 42,716 |
| Recorded full-run wall time | 247.301 s; historical, not a new prediction |
| Seed, both forms | line 13/41; branch 6/14; toggle 6/408 |
| All saved final sessions | line 41/41; branch 14/14; toggle 344/408 |

| Endpoint and form | B mean prefix tokens | C mean prefix tokens | C vs B |
| --- | ---: | ---: | ---: |
| Original registered line-only, original form | 74,890.67 | 73,738.33 | −1.539% |
| Original registered line-only, variant | 70,271.67 | 66,377.00 | −5.542% |
| **Retrospective** proposed joint target, original | 74,890.67 | 73,738.33 | −1.539% |
| **Retrospective** proposed joint target, variant | 77,982.00 | 69,693.67 | −10.629% |

The joint rows are new retrospective calculations, not the original preregistered score or new experimental evidence. The line-only index comparisons have two C-earlier/four ties; joint comparisons have three C-earlier/three ties. Index alignment does not pair provider randomness. Preserve all post-target calls and fees; do not present the prefix metric as an actually early-stopped historical bill.

## Reuse and resource proposal

DUT, spec, old checker, feedback and driver hashes match the old queue configuration. **Current `egraph/src/main.rs` and `scripts/typed_predicates.py` do not match the historical frozen versions.** Read-only historical Git objects at `66051b681d3f75e0e68370271a743e637820ac1b` match the saved bindings. Do not restore/rebuild or run the old runner against current engines. Reuse the bound saved extraction, egg and semantic-proof data as cached treatment; exact source-to-packet mapping still needs qualification. The 22 old two-state combinational proofs do not validate current engine code or four-state/sequential behavior. The saved 166-cell whole-form equivalence is limited to its sampled binary methodology. No new egg/Z3/G1 jobs are proposed.

| Proposed resource | Ceiling / qualification |
| --- | --- |
| GPT | `gpt-6.1-sol`, low, Standard/default; max output 4,096; 90 s/request; SDK retries 0 |
| Generation dispatches | 72 normal + at most one transient transport retry/session (18) = 90 |
| Invalid JSON / illegal actions | Consume a paid normal round; no free repair; preserve failure |
| Claude golden | Initial author + at most one bounded revision; max 2 calls, provider-enforced 8,192 output cap; target author cost ≤$1 is a forecast, not a separate hard guarantee |
| Paid dispatches / remote token-count calls | At most 92 / 0; no claim counting would be free |
| Main round simulation / replay | ≤72 roots / 1,152 cycles including repeated seed/history |
| Separate seed / private bounded smoke | ≤2 roots/12 cycles; ≤2 roots/44 cycles using existing private vectors; never prompted; no general reachability claim |
| Reference/property controls | 6–9 fixed observation cases; ≤18 independent checker evaluations, no simulator/build; exact positive/negative/unknown labels require independent authors/reviewer |
| Total local simulation / compilation | Draft ≤76 roots/1,208 cycles; two DUT observer builds; Verilator only, consistent with old coverage; not executed or automatically authorized by this draft |
| Structural processing / proof | ≤2 Yosys commands; 0 new egg/Z3/G1 jobs; pending exact local job list |

Keep the implementation small: a fixed observation ABI and separate golden/property postprocessors suffice. Controls may deliberately corrupt an observation to verify FAIL/UNKNOWN handling; such synthetic findings are not DUT defects, physical witnesses or RTL coverage. Do not add a second simulator, per-rule SV mutants, or a new qualification framework for this pilot.

The API proposal is **expected $4–7, hard combined ceiling $15, pending new user approval**; the old $20 does not transfer. Parent price basis is `docs/audits/queue_ablation_budget_2026-11-07/price-basis-and-estimate.json`, SHA256 `30fb95c89f8e137d633d0e89a90fc67bda2958a4061259b7f3b8e0bcdcdfa3b5`. It uses official price checks recorded there, historical mean usage plus a planning allowance of 1,000 extra input tokens on Yosys-bearing requests, not new actual measurements. At 72 attempts: 1,465,422 input +17,661 output tokens; cache-write pricing plus 10% margin estimates $4.2241815 for generation. At 90: 1,831,778 +22,077, estimated $5.2802365. Golden authorship adds separate cost within the same total ceiling; actual invoices and Codex maintenance/subscription charges are unknown, not zero.

Use one shared mixed-provider ledger, reserving 5,842,584 microUSD per GPT dispatch and 5,680,224 per Claude dispatch against full-context conservative pricing. Settle only trustworthy provider-specific model/tier/category/usage; unknown usage retains the full reservation. Insufficient funds stop before dispatch: $15 does not guarantee all 92 attempts complete. The 64k local input admission/actual-usage qualification target is **not** a server hard input cap; overshoots retain response, usage and cost, halt, and cannot qualify.

Rough effort: 2–4 h offline implementation, 0.5–1 h independent review/analysis; expected online 10–30 min, proposed hard 60 min including cleanup, not a completion promise. Retain existing staged credentials through the future ablation and review; this stage neither reads/stats/hashes keys nor asks for restaging. Continue using hidden terminal staging only if a newly authorized phase actually needs it.

## Acceptance gates and exact next task

1. Independent review of these four documents and the shared contract/target compatibility; P21's current checkpoint is not final acceptance.
2. Freeze the observation ABI and obtain qualified, separately authored golden and property artifacts/controls. Do not let infrastructure silently fill truth logic.
3. Build the small deterministic appendices and a new thin three-arm runner with true early stop, censoring, prompt isolation and shared ledger; leave old frozen runners/results unchanged.
4. Freeze exact local jobs, versions, counter identities, packets and schedule; run only separately authorized bounded offline qualification, preserving unknowns and negative controls.
5. Obtain new explicit API budget approval after concrete gates pass; only then dispatch and independently audit every result/cost. No target tuning against C.

Only four design files are added here: this plan, `plan.json`, `old-pilot-summary.json`, and `reuse-inventory.json`. No experiment, compile, simulator, solver, API, installation, Git write or shared handoff/status update was performed for this preparation.
