# WBXBAR conditional index and ordinary-operation screen — 4 November 2026

**Outcome: conditional semantics and static source mapping pass; ordinary-operation
discrimination fails.** Eight candidate groups, six nontrivial, contain 17 distinct
original source counters. Every one of these counters is reached by ordinary
transactions. No Claude checker, GPT development trial, or C trial was commissioned.
API calls, tokens and cost are zero. This does not establish a DUT functional defect
or any positive/negative C-versus-B performance effect.

This is a separately registered extension of the same original WBXBAR configuration,
not a new independent IP or a modification of the old screen. See
[`configs/wbxbar_conditional_index_v1.json`](../configs/wbxbar_conditional_index_v1.json)
and the machine-recomputed [audit](../results/wbxbar_conditional_20261104/validation.json).
The installed context-compression, Karpathy, verification-before-completion and
Caveman skills governed maintenance only; no skill text entered experimental prompts.

## 1. Fixed scope and controls

- Repository baseline: `50d7ee83d61989017e28e981420cd58f4c5f0787`; work remains uncommitted.
- Original upstream: `ZipCPU/wb2axip@2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`.
- Original sources: `wbxbar.v`, `addrdecode.v`, `skidbuffer.v`; no RTL edits.
- WBXBAR SHA-256: `d3fd1f2d7fb8909c2c2950c666e04c97d704c501c867201aedab5011ee106d2e`.
- New preregistration SHA-256:
  `7d72cedd06a695ba01c76062a871ffe4aab7f1030e277c21a27a73fbda1b1146`.
- Parent scope SHA-256:
  `efa89c6703c8f0281355e6eae8004e05fb265dd85c0dd4ac5f077daf4ecf4393`.
- Parameters: NM=2, NS=2, AW=8, DW=32, SLAVE_ADDR=4096, SLAVE_MASK=61680,
  LGMAXBURST=3, OPT_TIMEOUT=16, OPT_STARVATION_TIMEOUT=1, OPT_DBLBUFFER=1,
  OPT_LOWPOWER=1. Clock `i_clk`; synchronous active-high `i_reset`.
- Original B budget unchanged: 3 repetitions × 6 rounds × at most 64 new physical
  cycles, plus 8 seed cycles. Model `gpt-6.1-sol`, low reasoning, input cap 32,000,
  output cap 16,384, 120-second timeout, one retry. These are registered limits,
  **not a live run**.
- Static gate remains ≥3 source-distinct groups, ≥2 nontrivial, each ≥2 mapped
  seed-zero counters. All selected counters must remain zero in the ordinary union.
  Subsequent gates still require three independently checked multistep event families
  and the original B acceptance criteria. None was weakened.

## 2. Why the first range assertion failed, and what is proved

The former free-state translation allowed a 2-bit `mindex[N]` to take value 3 when
indexing the 3-bit `request[N]`. Replacing this with zero, silently assuming a range,
or treating `m_stall` as a free primary input would be unsound.

The preregistered stronger trial, `mgrant[N] => mindex[N] <= 2`, **fails in the
base case at step 3**. An unmapped request can select the pseudo-slave
`grant[N][NS]` while the index is unspecified. In that branch the actual source
sets `m_stall` directly; it does not use `request[N][mindex[N]]`. This counterexample
refutes the overbroad assertion, not the DUT's specification.

The source at `wbxbar.v:886–891` first tests `grant[N][NS]`, then
`mgrant[N] && request[N][mindex[N]]`. The certified implication is therefore:

```text
For each N ∈ {0,1}:
  (!grant[N][2] && mgrant[N]) => unsigned(mindex[N]) <= 2
```

This actual activation condition was included in the preregistration. The later
`o_merr` override remains in the complete combinational definition; it is not
needed to weaken the proved range implication. No input/protocol assumptions,
forced reset sequence or invented index initialization were added. The proof uses
original initial assignments and transitions, with other state initially arbitrary.

Final SymbiYosys results:

| Obligation/control | Result | Interpretation |
|---|---|---|
| Conditional range, base case + temporal induction | PASS | Inductive safety property of the fixed transition model |
| Range plus request/grant onehot0, grant-active and selected-index helpers | PASS | Extra validation; helpers are not imported into later equality queries |
| Unconditional `index <= 2` | FAIL, expected | Prevents inventing unconditional initialization/range |
| `selected => index == 0` | FAIL, expected | Demonstrates rejection of an intentionally false active property |
| Ten activation covers | PASS | Both masters can activate indices 0/1/2, and genuinely selected indices 0/1 |

The helper relating the selected grant to the index also uses the actual `selected`
condition; the stronger mgrant-only helper was not certified or imported. Cover
witnesses are private proof controls and never become model stimulus. `cover` is
not a specification-based functional correctness proof.

The final proof logs show base-case success and successful induction at step 18
within the registered depth-20 limit. Each final cover is reached at step 3. SBY
`prove` combines base and induction; a bounded no-counterexample result alone would
not have met this gate ([SBY task modes](https://symbiyosys.readthedocs.io/en/latest/reference.html)).

Evidence: [`formal-final`](../results/wbxbar_conditional_20261104/formal-final),
[`domain-certificate.json`](../results/wbxbar_conditional_20261104/domain-certificate.json).
The first failed property and intermediate proof version remain in `formal-v1`
and `formal-v2`; their snapshots preserve the producer code used at those stages.

## 3. Conditional semantics, egg and exact source counters

`wbxbar_conditional_semantics.py` extends only the exact original line-888 select,
checking request/index widths, unsignedness, array direction, master identity and
certificate hash. Out-of-domain selects remain arbitrary. The AST and independent
Yosys encoding use different arbitrary bits, so a missing domain cannot accidentally
prove equivalence by sharing undefined values.

Only the certified implication is imported. The full state, clock/reset contexts,
priority and downstream guards remain represented. The SMT environment is SAT;
all **109** constructed definition-mismatch queries are UNSAT, including `m_stall`.
A negative test removes the two per-master domain assertions: `m_stall` then has
a SAT mismatch. Altered bounds, lemmas and file hashes are rejected.

The follow-up uses the existing real Rust `egg` engine, not a manually written
semantic summary: six Z3-validated Boolean rules and 18 independently proven typed
ground equalities, bounded to 20 iterations / 20,000 nodes / 5 seconds. This run
saturates in 7 iterations, with 524 eclasses and 869 enodes (~0.045 seconds).
Pair queries: 31 UNSAT, 3,789 SAT, zero unknown. Ground rules remain scoped to
this certified configuration/domain and are not unconditional reusable laws.

Source admission after physical-counter aggregation:

| Quantity | Result |
|---|---:|
| Extracted supported targets after event-context withholding | 248 |
| Aggregate physical-counter targets | 125 |
| Exact mappings | 91 |
| Unresolved opposite-polarity mappings | 34 |
| Seed-zero candidate groups | 8 |
| Nontrivial candidate groups | 6 |
| Original DUT counter denominator | 2,845 |

Sixteen targets under explicit level-sensitive event lists, such as
`always @(r_regrant,regrant)`, are withheld rather than mislabeled as clock edges
or `always_comb`. Four procedural loop-variable/co-driver translation diagnostics
remain reported; no unsafe free combinational value survives the definition audit.
Unsupported expressions, event contexts and opposite-polarity mappings are not
admitted as semantic targets. **Their original coverage locations remain in the
raw denominator.**

The source mapper audits generated C++ specialization/membership. Where Verilator
shares a physical counter across generated instances, its complete activation is
their disjunction; an individual instance hit is not invented. Different original
source locations retain separate counters even when egg proves equivalence.
Both semantic encodings share Slang: this is not frontend-independent, four-state
equivalence, or whole-IP functional verification.

## 4. Ordinary-operation exclusion

The fixed JSON transport driver has per-master queues and holds CYC through
responses and STB/payload through acceptance. An independent Python replay checks
all JSON inputs and transport ledgers. Slaves respond promptly in order, with
no engineered stalls, timeouts or competing ownership. It is **not a golden-output
checker** and does not certify the DUT's functional behavior.

Forty-four predefined cases cover isolated mapped/unmapped reads/writes, varying
byte masks, one-master 2/4/7-beat bursts, isolated slave errors, normal
release/reacquire and concurrent accesses to different slaves. Each starts from
the same eight-cycle reset/quiescence seed and ends with 64 counted idle cycles.
All 88 Verilator/Icarus executions complete; meaningful pin traces agree. Inactive
undefined payload is excluded from comparison; active unknown payload is rejected.
Every execution preserves the original 2,845 counter identities.

All eight groups are hit even without sophisticated traffic: six by an isolated
mapped read, two by an isolated unmapped read. The following first case means
the first matching case in registered order, not the first physical hit cycle.

| Eclass | Nontrivial | Original WBXBAR source lines | First ordinary case |
|---|---|---|---|
| 184 | yes | 482, 574, 673 | isolated mapped read |
| 190 | yes | 494, 571 | isolated unmapped read |
| 238 | yes | 559, 666 | isolated mapped read |
| 272 | yes | 562, 668 | isolated mapped read |
| 286 | yes | 565, 671 | isolated mapped read |
| 289 | no | 569, 886 | isolated unmapped read |
| 320 | yes | 684, 687 | isolated mapped read |
| 453 | no | 917, 1033 | isolated mapped read |

The audit retains each identity, raw hit count per run, total over separate runs
and first ordinary witness. Equivalent counters can have different hit totals:
eclass 184's three counters total 1,888 / 1,888 / 3,776. Equality therefore never
replaces actual source execution accounting.

Ordinary union coverage (DUT only, hits > 0 across separate runs):

| Verilator counter kind | Covered / denominator |
|---|---:|
| line | 82 / 86 |
| branch | 78 / 88 |
| expr | 278 / 321 |
| toggle | 1,304 / 2,350 |

These are tool-defined counters: line points are instrumented code blocks, branch
points are emitted control outcomes, expression points are emitted expression
outcomes, and toggle points are instrumented bit transitions. They are not counts
of textual lines, all mathematically possible branches, or specification properties.
The sum is 1,742 / 2,845, but mixing kinds is not the primary research metric.
Counters start fresh each execution; seed/reset activity is included consistently.
The union is a selection screen, not an appended LLM session or pilot cost curve.

**Ordinary gate: FAIL; surviving groups: zero.** No independently checked multistep
calibration, Claude checker or B/C was run. The intended contention/drain,
timeout/restart and abort/ownership-transfer events are not claimed to be verified.
Making those sequences longer would not repair these already-easy source targets.

## 5. Accounting, tests and limitations

All saved attempts remain available: 11 formal tasks (including the first failed
overbroad assertion and expected negative controls), two semantic-screen attempts
(the first stopped on noncanonical sensitivity context), eight successful frontend
invocations, four DUT binary compilations, two eight-cycle inventory simulations
and 88 ordinary simulations. Total saved DUT executions: **90**; physical cycles:
**6,728** (16 inventory + 6,712 ordinary, counting both simulators). These are
screening costs, not B trial costs.

Recorded sums: formal tasks ~15.58 s, compilation ~43.25 s, simulation ~2.09 s;
two screen attempts ~36.31 s include overlapping substage times. Do not add all
these numbers as end-to-end wall time. Unit-fixture tool calls appear in their
test logs and are not DUT pilot calls. A pre-launch helper-generation orchestration
error was fixed before screen-v1; it is not a DUT or semantic-proof failure.

Fresh audit: **42 tests pass**, including 11 new conditional-domain/transport
tests and 31 regressions. It verifies 310 provenance entries, recomputes ordinary
coverage from every saved raw file, replays transport ledgers, and confirms old
SPI freezes and previous candidate evidence are unchanged. The new mutation checks
reject invalid JSON widths/types/seed, changed payload/acceptance ledger, missing
cycles and unknown active outputs. This is transport/proof validation, not a
substitute for a separately authored specification checker.

Versions: Python 3.13.9; Verilator 5.050; Icarus 12.0; Yosys 0.70+309;
Slang 12.1.0+42710c788; SBY v0.70-9-g79fc9ed; **formal bundled Z3 4.15.5**;
**combinational/system Z3 5.1.0**; Rust/Cargo 1.99.0; egg 0.11.0.
Exact commands, tool strings, source/checker-free role status, hashes and timings
are in the audit. There is no checker hash because none was commissioned here.

## 6. Reproduction and permitted next step

From the repository, audit current artifacts and run focused regressions:

```sh
.venv/bin/python scripts/audit_wbxbar_conditional.py
```

To rerun the final formal obligations into a new directory (each command is separate):

```sh
.venv/bin/python scripts/prove_wbxbar_index.py prepare --output build/wbxbar-range-replay --activation selected
.venv/bin/python scripts/prove_wbxbar_index.py run --output build/wbxbar-range-replay --task prove
.venv/bin/python scripts/prove_wbxbar_index.py run --output build/wbxbar-range-replay --task strengthened
.venv/bin/python scripts/prove_wbxbar_index.py run --output build/wbxbar-range-replay --task false_active
.venv/bin/python scripts/prove_wbxbar_index.py run --output build/wbxbar-range-replay --task unconditional
.venv/bin/python scripts/prove_wbxbar_index.py run --output build/wbxbar-range-replay --task activation
```

Current certified semantics and ordinary traffic can be reproduced without changing
the certificate or historical evidence:

```sh
.venv/bin/python scripts/screen_wbxbar_conditional.py --output build/wbxbar-semantic-replay
.venv/bin/python scripts/probe_wbxbar_ordinary.py --output build/wbxbar-ordinary-replay
```

Each output directory must be new. The ordinary runner intentionally uses the
certified `screen-v2` baseline. Replacing the certificate, source, proof or scope
requires a separately registered version; the certificate producer refuses to
overwrite existing evidence.

Keep this configuration rejected. Reuse the conditional-domain proof adapter
where justified, but screen future public IPs for **event-specific source predicates**:
completion after contention drains, recovery after a real timeout/abort, or resource
release conditioned on prior state. Do not merely add source volume, duplicate
guards, shorten the budget, or relax ordinary exclusion. Any extension of the 34
unresolved mappings or 16 withheld contexts requires independent exact mapping/
timing evidence and a new screen before model investment. Only a candidate that
passes those gates proceeds to Claude's specification-only checker, GPT's driver
and calibration, unchanged-budget B, and finally C if B qualifies.
