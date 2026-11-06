# G1 public qualification profile v1 — R01 preparation

Status: **PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW**. No native compiler,
simulator, solver, version probe or real G1 job has run in R01. Existing tools
were located and their resolved root binary bytes pinned by read-only inspection.
All labels are producer hand calculations, pending independent P10. No actual
waveform exists yet; expected-waveform-contract.json is an expectation document.

This is a public SV language/representation control package, not a FIFO DUT,
Claude replacement oracle, candidate monitor or B/C experiment. G0 remains a
separately accepted synthetic metadata adapter and is not used to accept G1.
The old 36-generation cohort is complete and unchanged. Its 11/11 ceiling,
C's9.85711% extra tokens and unresolved formal evidence are not repaired here.

## Exact material

`inputs/controls.json` gives every QC00–QC15 its D01 purpose, widths/signedness,
full guard, reset/initial contract, pre/post expected rows, eligibility and hand
derivation. `inputs/stimulus.json` enumerates four input cycles; no RNG/seed is
used. Common widths: a/b/q/sum4=4, full5=5, signed_a=signed4, logical cycle=3,
active/ok=1. The sum4 assignment truncates to4; no unsized data operand is used.

`sources/common.sv` contains only a toy4-bit counter and fixed combinational
language controls. Initialq0, synchronous active-high reset, one posedge clock.
QC11 deliberately changes reset polarity as its sole registered negative.
Physical pre q=[0,0,1,2], post q=[0,1,2,3]; QC11 q remains0. Inputs are stable
before each edge. Native harness cycle0–3 uses those same pins, then idle through
step7; saturation prevents wrap. Each native harness has exactly one assertion
and one activation cover, with no induction/prove/unbounded mode.

| Controls | Predetermined distinction |
|---|---|
| QC00/01 | Active tautology vs deliberately false obligation after reset |
| QC02/03 | Explicit low4 truncation equality vs0extended overflow difference at15+1 |
| QC04/05 | signed4 negativity matches msb vs unsigned<0 substitution |
| QC06/07 | Complete valid/en/!reset/a!=0 guard vs never-active guard |
| QC08/09 | Native registered-pre binding vs deliberately post-claimed offset |
| QC10/11 | Fixed reset/initial context vs deliberate polarity mutation |
| QC12/13 | Logical X equality / case-equality unknown detection: four-state equivalence unsupported |
| QC14/15 | Final-post metadata transport only vs trace_done0/vacuous completion projection |

Native assertion enable/check and sampled_cycle/q/active/ok register at the same
posedge. A native failed-state number may be one state later than its source
pre observation. The runner binds the registered sample, not live q at the
reported step. Physical pre/post are distinct raw rows and VCD samples.
QC09 also records the intentionally mismatched phase claim as REJECT; that
metadata negative does not change raw physical phases or infer a DUT fault.

QC07 and QC15 can have BMC PASS with activation cover NOT_REACHED and get no
obligation/completion credit. QC12/13 preserve Icarus4-state expected facts but
Verilator/native two-state results remain diagnostic/unsupported for four-state
equivalence. Nothing establishes a common cause for the historical74 witnesses.
QC14 marker exists only in the observer at finalpost; it is no control input and
adds no clock. Native marker0 is a safety projection, never128-cycle completion.

## One resource pool and fixed schedule

Registration: `test2/configs/g1_qualification_registration_v1.json`.
`job-plan.json` freezes90 logical root jobs, ordered8setup versions,2shared
physical builds, then eachQC's Yosys prep/BMC/cover/Icarus/Verilator jobs.

- Compilation:18 planned logical batch jobs =16Yosys prep +1Icarus suite build
  +1Verilator suite build, under32 maximum/20s each. Shared builds contain all16
  control instances; each run prints only its selected instance. Internal ivl,
  make/C++ and other descendants consume the same job deadline and global wall.
  Verbose build logs and best-effort process-group PID observations are saved.
  This is **logical batch-job accounting**, not a claim that18 OS compiler
  processes exist; P10 must explicitly assess this interpretation before tools.
- Native:16BMC +16activation cover, total32, depth8,10s each, Z3 backend.
- Physical:16Icarus +16Verilator runs, four cycles each=128 reserved cycles;
  hard caps32runs/1024cycles/32perrun/2s each. No fallback to a single simulator.
- Setup:8version/help queries,2s each, plus binary verification inside the same
  execution timer. Verilator's installed root script is pinned; runtime library,
  compiler and OS dependency identity is not a complete supply-chain attestation.
- Global:1200s, starting before actual tool hashing/version/setup/build work.
  Work stops5s early for cleanup, hashing and output serialization. Root deadlines
  reserve0.25s for process-group cleanup. Late/failed cleanup is retained and halts.

The single `execution-state.json` is exclusive, persisted before dispatch and
cannot be reset/restarted by the runner. Failures/timeouts consume reservations;
there are no retries or second profiles. Raw statuses, invalid/unqualified
parses, NOT_RUN remainder and NOT_REACHED cover survive. Unexpected supported
results, tool absence, timeout/error or cap breach halt qualification. A leftover
budget is not permission for extra controls. Post-review has zero new-job grant.

`runtime.py` contains the only process launcher. It uses no shell and an explicit
non-secret environment; it does not read or stage credentials. Parent and child
costs are included in root/global elapsed time. PID sampling is expressly not
exhaustive. Local memory is not measured; no unreported cost is set to zero.
Output hashing/serialization elapsed is recorded, with the final mutable budget
ledger authoritative if a late halt occurs. The immutable result manifest omits
that final ledger to avoid a closing hash cycle.

## Technical execution gate

No EXECUTE receipt exists in R01. After independent P10, the coordinator supplies
a non-secret receipt with record_kind=G1_EXECUTE_AFTER_READONLY_P10, stage=EXECUTE,
registration/source_manifest/user_authorization/r01_manifest SHA256, and exact
p10_review_path/SHA256. P10 JSON must have status PASS or PASS_WITH_LIMITS,
phase beginning P10, input_identity.producer_manifest_sha256 and
input_identity.registration_sha256. The runner checks all frozen source inputs
before allocating the one pool. This local coordination binding is not a general
human/provider authentication mechanism.

Only a subsequent coordinator EXECUTE handoff uses the already granted G1
authorization. R01 stops here, without invoking the runner. No API/count/key,
network, install, old oracle, G2–G5, commit or push is included.

## Preparation verification and provenance

Pure Python mocks are budget/refusal checks only, not G1 qualification or native
replay. First12 pass are preserved in mock-attempt1; final14 pass in
mock-attempt2. Their source hashes/logs/commands are frozen with R01. First-run
source bytes were restored from recorded edits and match all5 saved hashes;
they were not originally copied at execution. An initial separator-newline
restoration mismatch is retained as a preparation-helper incident, not a product
test failure. No failed result or source version was erased.

The actual native parser, subprocess lifecycle and dual-simulator syntax/ABI
have **not been exercised**. Python AST checks and mocks cannot establish them.
P10 checks source/math/labels and the resource definition before any execution;
post-execution review checks saved physical/native chain evidence. Hallmark was
read and applied only to material honesty/fixed-input review organization; no UI
workflow/scripts or Hallmark correctness pass is claimed. All original P04,
P05/P06, P05-N1, F1/selected-sample/128/H1/H2/L1/billing limits remain open.
