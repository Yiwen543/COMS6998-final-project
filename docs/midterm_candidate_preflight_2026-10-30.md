# Midterm candidate preflight — 30 October 2026

This is the first outcome-blind step toward the November 6 midterm, **not** a
new A/B/C result. No OpenAI or Anthropic call was made. The original CVDP RTL
and supplied specifications are copied byte-for-byte and never repaired in place.

## Selection and provenance

The pinned NVIDIA CVDP v1.1.0 commercial-agentic slice has 68 records. The
new [screening record](../results/midterm_candidate_preflight/screening.json)
inspects every record's existing harness RTL, extracting supported Yosys
pre-`proc` guards separately per source module. Its deliberately restricted
criterion is two or more source-distinct, exactly matching *complete* guards
with the same process event set and at least two nested cases. Five task records
have potential groups: 64b/66b codec, HDBn codec, queue, and two linear-search
tasks. An absent group in this restricted screen does not mean the IP has no
semantic redundancy. The previously used queue is retained as a syntax-control
fixture. HDBn's candidate group is an enable path. We selected two **independent
IP designs** with different verification behavior:

| Original CVDP task | Why selected | Source files / supplied spec |
|---|---|---|
| `cvdp_agentic_64b66b_codec_0007` (cid013, medium) | Repeated decoder-valid/header guards and encoder control cases across distinct RTL locations; larger control/data paths | Four original modules and `docs/specification.md` |
| `cvdp_agentic_search_algorithm_0001` (cid012, medium) | Controller/datapath, memory writes, pause/resume, match collection and overflow; repeated pause guard at three datapath locations | Three original modules and `docs/specification.md` |

The exact dataset revision, record line/hash, and every copied file hash are in
[`midterm-candidate-lock.json`](midterm-candidate-lock.json). The original code
is Apache-2.0; the supplied specification is CC BY 4.0. CVDP fixtures are
*verification subjects*, not trusted golden implementations. The CVDP task
testbenches and patch fields were **not** copied into experimental fixtures or
used to design model feedback. Both full original top-level RTL sets compiled
under Icarus and passed Verilator lint before fixture creation.

## Semantic and coverage gate

[`preflight_midterm_candidates.py`](../scripts/preflight_midterm_candidates.py)
reuses the typed extractor, bounded Rust `egg` engine, Z3 checks, and raw
Verilator Coverage-3 parser. It keeps each module's E-classes separate; it does
not merge unrelated module-local signals merely because they share a name.
Every candidate group member is joined to an actual source-location counter.
For `if` lines that Verilator instruments as a branch rather than a line
counter, the join uses the unique true (`if`) branch point. Missing or ambiguous
joins remain explicitly marked; they are never promoted to qualifying groups.

| IP | Raw DUT-only seed coverage | Raw DUT-only calibration coverage | Seed-zero, source-mapped groups reached by separate calibration |
|---|---|---|---|
| 64b/66b codec | line 17/109, branch 16/96, toggle 23/2074, expr 3/32 | line 35/109, branch 37/96, toggle 1048/2074, expr 24/32 | 8 groups: decoder lines 45/76/122/135/151 and 46/136/152; encoder pairs 12/129, 14/130, 25/135, 26/136, 30/140, 31/141 |
| Linear search | line 20/32, branch 8/26, toggle 12/334, expr 5/18 | line 32/32, branch 25/26, toggle 123/334, expr 18/18 | 1 group: datapath pause lines 48/77/110 |

The codec has 16 *potential* groups; only the eight listed above pass both
source mapping and seed-zero/reachability calibration. Other groups remain in
the saved record with their mapping or calibration status. The search group is
real but simple: a B model may cover it immediately. Search line coverage
reaches its ceiling in the hand-written calibration sequence, so a 32/32 line
target would be a poor preregistered discriminator. No model-produced action
or B/C outcome has yet been inspected for these two IPs. Calibration vectors
are isolated in preflight testbenches and must never enter the experimental
prompts. The separate raw counters stay in the denominator even when guards
belong to one E-class. All claims are binary/two-state and restricted to the
supported Boolean path representation; this is not four-state or whole-design
equivalence.

These are **provisional** candidates. Linear search is a controller but has no
FIFO full/empty or simultaneous-read/write contract. It does not satisfy the
requested deeper FIFO stress case. The async FIFO remains a separate selection
gate. Current evidence cannot yet establish that raw-feedback B avoids
immediate saturation on either candidate.

## Initial open-source formal references

SymbiYosys (`sby` 0.70) was installed; Yosys 0.70+post and Z3 5.1.0 are
available. The first independently specified properties are intentionally
narrow. The codec decoder property checks the registered `sync_error` against
the previous valid input's 2-bit header. The search properties check
`match_count <= MAX_MATCHES` and a one-cycle `done` pulse for a four-entry,
two-result parameterization. Both harnesses assume reset asserted initially.
Each has a cover statement that is reached, avoiding a completely vacuous
passing assertion. The [formal result manifest](../results/midterm_candidate_preflight/formal-results.json)
records BMC, cover, and unbounded prove task status, exact property/harness
hashes, solver versions, separate logs, and hashed cover witness traces. All six final tasks pass. For
search, a first SMT k-induction attempt was inconclusive because induction
allowed unreachable states; ABC PDR subsequently proved the same properties.
This is **not** a claim that either complete IP or supplied specification is
proved correct.

There is a material specification-versus-RTL reset discrepancy to resolve
before freezing a full checker: the codec's top-level prose calls reset
synchronous, but decoder/encoder processes use `posedge rst_in`; the search
prose calls `srst` synchronous, but controller/datapath processes also use
`posedge srst`. Two independent Icarus preclock tests first create an active
observable state, then assert reset strictly between rising clock edges. The
decoder's `sync_error` and the search controller's `done` both clear *before*
the next clock edge. The tests and exact RTL hashes are saved in
[`reset-observations.json`](../results/midterm_candidate_preflight/reset-observations.json).
This is one reset-timing defect category per IP, not multiple categories per
repeated observation. Original files remain preserved. The full checker must
keep the stated synchronous-reset requirement and classify this discrepancy;
the experiment must not silently weaken or edit the checker.

## Next gates before any paid model trial

1. Implement and independently fault-test fixed specification-based checkers
   and JSON action drivers for each IP. Resolve the reset contract and every
   excluded behavior in writing. Keep the supplied benchmark testbenches out
   of prompts and checker derivation.
2. Use independent *development* trials to select reachable coverage targets
   not saturated by the common seed or a first raw-feedback round. Freeze IP,
   parameter values, checker, seed, denominator, target, model settings, and
   feedback lengths before held-out trials. Search may fail this gate; retain
   that outcome and select another independently screened IP if so.
3. Run matched A, B, C, and B+length-matched placebo sessions only after the
   first two gates. Record every API call, retry, token, replayed cycle,
   simulator execution, formal result, and target miss. Claude may audit the
   frozen evidence but cannot replace the raw coverage or formal reference.
4. The CVDP async FIFO was inspected as a later stateful/dual-clock candidate.
   Its pinned record supplies RTL and a detailed specification, but the
   current per-module Boolean frontend found no qualifying within-module
   cross-location guard group. Hierarchical port-alias reasoning and a
   dual-clock checker are needed before treating it as a C-feedback task.

## Reproduce without API access

From the repository root:

```sh
python3 scripts/prepare_midterm_candidates.py
python3 scripts/screen_midterm_candidates.py
python3 scripts/preflight_midterm_candidates.py
python3 scripts/run_midterm_formal.py
python3 scripts/check_midterm_reset.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_midterm_candidates.py' -v
```

The first command verifies existing files instead of overwriting them.
Preflight compilation lives under ignored `build/`; per-IP raw `.dat` files,
source/guard/e-class evidence, per-task formal logs, and JSON manifests are
under [`results/midterm_candidate_preflight/`](../results/midterm_candidate_preflight/).
