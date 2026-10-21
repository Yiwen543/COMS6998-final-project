# Typed-guard preflight for held-out CVDP queue variants

This is the next **selection and semantic-validation** step for the proposal's
A/B/C study, not an LLM outcome. It was run without inspecting any model output
for this queue. The exact files and checks are in
[`results/heldout_queue_preflight/selection.json`](../results/heldout_queue_preflight/selection.json).

## What was selected

The original [`queue.sv`](../examples/heldout_queue/rtl/queue.sv) and
[`specification.md`](../examples/heldout_queue/docs/specification.md) are copied
verbatim from the pinned official CVDP `cvdp_agentic_queue_0007` cid012co record;
SHA-256 hashes and the source record are in
[`provenance.json`](../examples/heldout_queue/provenance.json). The separate
[`queue_variant.sv`](../examples/heldout_queue/rtl/queue_variant.sv) replaces
the repeated `clr_i` and `ena_i` conditions with double-negated forms. It has
the same default parameters and interface. The original file is unchanged.

The outcome-blind [`screen_cvdp_candidates.py`](../scripts/screen_cvdp_candidates.py)
inspected the cached 68-record official CVDP slice. It skipped 39 records with
zero or multiple RTL source files and six records that elaborated into multiple
modules, found no qualifying group in 22 supported single-module records, and
selected only this queue. Its exact rule, per-record
status, and dataset hash are saved in
[`screening.json`](../results/heldout_queue_preflight/screening.json).
This restricted result does not prove that the skipped or unsupported designs
lack semantic redundancy; some have distinct enclosing guards or event sets.
Thus the
selected pair is **two equivalent RTL versions of one IP**, not two independent
CVDP IPs. The next pilot can test syntax sensitivity within this IP; it cannot
establish cross-IP generalization.

The two selected groups are the `2'b01` read-only arms at source lines
55, 82, 124, 139, 154, 169 and `2'b10` write-only arms at lines
56, 89, 125, 140, 155, 170, in **each** version. Each arm's activation guard
includes the preceding reset, clear, and enable conditions, the earlier case
exclusions, and its own two-bit case value. The event context is
`posedge clk_i` plus `negedge rst_ni`. Under binary semantics, the read guard
reduces to `rst_ni && !clr_i && ena_i && {we_i,re_i} == 2'b01`; the write guard
has `2'b10` instead. They are not equivalent behavioral cases and remain in
different egg classes.

## Evidence and limits

[`typed_predicates.py`](../scripts/typed_predicates.py) reads **Yosys
pre-`proc` RTLIL**. It preserves widths and signedness on supported comparator
atoms, source hashes/spans, all enclosing `switch/case` arms, prior-arm
exclusions, and the process event set. It exports 49 mapped guards per version
and explicitly reports 18 unsupported or unmapped generated cases per version;
the latter are not treated as proved equivalent. Some Yosys `case` `src`
attributes point at the preceding line. The selected multi-bit labels are
therefore rebound by unique literal text within the Yosys switch source span,
then checked against the actual Verilator counter at the same original file,
line, type, and `case` outcome. Missing or ambiguous joins fail.

The six Boolean rewrite rules in the existing `egg` engine passed exhaustive
two-input truth tables and independent Z3 XOR-unsatisfiability checks. The
`$ne = !$eq` bridge was checked with binary bit-vectors of widths 1, 2, 4, and
16; Z3 also proved `2'b01` and `2'b10` disjoint. Bounded egg saturation stopped
after five iterations (`Some(Saturated)`) and merged the 12 read guards into
one class and the 12 write guards into another. Z3 independently proved all
11 pairwise comparisons against each group's reference guard (22 proofs).
A concrete legal binary input distinguishes the two groups. These checks
validate two-state Boolean equivalence; they do **not** assert four-state
X/Z equivalence or whole-RTL equivalence from egg alone.

Separately, Yosys `equiv_make`, `equiv_simple`, and four-step `equiv_induct`
proved all 166 matched equivalence cells between the two RTL versions
after `async2sync` was applied to **both** sides for sampled sequential SAT.
Both untouched RTL sources retain the same asynchronous reset event, and a
separate preclock reset simulation checks their behavior on assertion. The
formal result does not by itself cover every between-clock analog timing case.
See [`variant-equivalence.log`](../results/heldout_queue_preflight/variant-equivalence.log).

The shared six-cycle seed asserts reset for two cycles, then idles for four.
Verilator 5.050 recorded 12 distinct selected `line/case` counters at zero
hits per version (24 total). The original's full raw DUT denominators remain
41 line, 14 branch, 408 toggle, and 16 expression counters. The variant has
41 line, 14 branch, 408 toggle, and 40 expression counters: its extra Boolean
operators change Verilator's expression instrumentation. Coverage must be
compared **B versus C within a fixed version**, never by directly subtracting
raw expression percentages across versions. A separate non-seed run adds a
write-only and read-only cycle and makes all 24 selected counters positive,
showing these targets are reachable. Neither run contains LLM-generated
stimulus or a specification checker; functional coverage claims await the
fixed-driver pilot. Icarus also compiles and executes the preflight TB; it
warns that its simulator ignores `unique case` qualifiers, so Verilator is the
measurement tool.

## Reproduce

From the repository root, with Yosys, Verilator, Z3, Icarus, and the existing
Cargo-built egg executable installed:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/fetch_heldout_dataset.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/preflight_heldout.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_typed_predicates.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/screen_cvdp_candidates.py
```

The preflight command regenerates both typed extraction JSON files, the egg
graph, the equivalence proof log, the two simulator counter files, and the
selection manifest. The fetch command reuses an already hash-verified cache or
retrieves the exact public revision in
[`heldout-dataset-lock.json`](heldout-dataset-lock.json). The selected locations remain separate raw counters even
when their activation guards share an E-class. For the next A/B/C experiment,
freeze each version's checker, driver, denominator, seed, and model budget;
send B every raw uncovered point and C exactly the same raw points plus these
validated groups. Do not give C the separate reachability sequence, Z3
witness, or a solved stimulus. No B-versus-C benefit has been measured on this
held-out queue yet.
