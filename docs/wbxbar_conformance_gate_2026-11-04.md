# WBXBAR conformance gates before a new B/C run — 4 November 2026

**Follow-up completed:** the separately registered
[reference-checker freeze and replay](wbxbar_reference_replay_2026-11-04.md)
passes the 42-batch pin/counter audit and preserves 895 historical files.
All six final functional verdicts remain unresolved. No new B/C run was launched;
the detailed development record below retains each stage's original limitations.

This separately registered phase addresses three remaining limitations in the
[revised cancellation checker](wbxbar_cancel_contract_2026-11-04.md). It does not
change old results or authorize live B/C merely because a model says “ready”.
The original 3 repetitions × 6 rounds × 64 new cycles, eight seed cycles,
`gpt-6.1-sol`, low reasoning, input 32,000/output 16,384 token caps remain fixed.

## What must change

| Limitation | Required method | Evidence needed before a new experiment |
|---|---|---|
| Cancellation propagation | Separate public requirements from fixed-version behavior. Track accepted, canceled, forwarded and completed obligations. Do not equate idle pins with empty buffers. | Independently authored safety obligations, explicit assumptions, useful nonvacuity, negative controls, and a valid certificate before any implementation-specific bound is used. |
| Ambiguous ownership | Preserve feasible transaction associations, or a proven sound abstraction; check properties locally instead of stopping the whole epoch. | Identical-transaction, later-disambiguation and fault-during/after-ambiguity controls; resource-bound exhaustion must be explicit unresolved, not arbitrary pruning or pass. |
| Cross-slave forward order | Check supported response order, payload and ownership separately from the order requests appear at different slaves. | A legal or conservatively unresolved early-forward/ordered-retirement control, plus observable incorrect retirement/data controls. An unsupported inferred order must not alone establish a DUT defect. |

Identical public transactions may be inherently indistinguishable: no checker
algorithm can recover an absent transaction ID from identical observations. The
contract must distinguish consistency with permitted external behavior from proof
of actual hidden ownership. A candidate-hypothesis implementation must explain
which properties are universal over remaining candidates, which results are only
existential trace consistency, and how uncertainty is propagated. Merely finding
one convenient assignment must not silently establish a stronger claim.

Changing stimulus to insert unique tags, allowing only one outstanding request,
or resetting after every ambiguity would change the experiment. None is added
as an undisclosed primary-driver restriction. Any future such control requires
separate registration and equal treatment in B and C. Idle or drain cycles always
consume the fixed physical-cycle budget.

## Offline progress already executed

Registration: `configs/wbxbar_conformance_gate_v1.json`, SHA-256
`d957119caa1405b628caf50e7ffd90f81fb890484f04036da9ce5858f925f5f6`.
Original v4 freeze, checker and earlier pilot hashes still match.

A proof-only observer on the original fixed RTL and parameters established:

> If both masters' CYC inputs are low at the preceding sampled rising edge,
> slave-side CYC and STB are low at the current sampled rising edge.

The SBY `prove` task passed base case and temporal induction, with no input
assumptions. The stronger zero-delay assertion failed at step 4 as an expected
negative control; two nonvacuity covers were reached. This does **not** prove
internal buffers empty, old requests incapable of resurfacing after restart,
a universal Wishbone cancellation latency, or complete IP correctness. Cover and
negative witnesses use unconstrained inputs and are not claimed to be legal
protocol test vectors. The observer changes neither DUT files nor coverage.

The [SBY task definitions](https://symbiyosys.readthedocs.io/en/latest/reference.html)
distinguish bounded checking, unbounded safety proof and cover. A bounded run
without a counterexample cannot be relabelled a full proof. This phase used the
installed bundled tools: SBY v0.70-9-g79fc9ed, Yosys 0.70+309 (bd3168b1a), and
Z3 4.15.5. Commands, source hashes, exact assumptions and logs are in
`results/wbxbar_conformance_gate_20261104/boundary-v1/`.

Seven new public-pin synthetic scenarios (196 rows) were constructed independently
of actual DUT trajectories. Evaluating the unchanged v4 checker shows:

- Early cross-slave forwarding followed by ordered responses is marked
  `dut_violation` (two diagnostics), illustrating the inferred-order restriction.
  Its proposed acceptance semantics still require independent source review.
- Incorrect retirement/data is also rejected, so removing the order inference
  must preserve actual data and response checking.
- Five ambiguity scenarios remain unresolved, including later distinct work,
  a later read-data corruption and an unaccepted forwarded address. The latter
  two demonstrate why whole-epoch ownership-check suspension is insufficient.
  No environment-assumption violations were reported for these seven fixtures.

These are checker-development controls, never experimental model stimulus or
E-graph targets. They expose gaps in the old tested scope; they do not rewrite
its 69-control results or create new DUT-defect claims.

## Role sequence and admission conditions

1. Claude independently designs the clause matrix, ownership reference semantics,
   formal obligations and proposed control classifications from public sources.
   The first call is read-only design, not a checker patch. Its packet excludes
   executable DUT, actual traces, B/C results, coverage targets and the new
   implementation-characterization proof result.
2. Review the design for soundness and bounded implementation scope. Claude then
   authors the checker and specification assertions; GPT integrates transport,
   controls and tooling without silently editing functional expected-output logic.
3. Execute independent positive/mutation/ambiguity controls and relevant formal
   obligations. Distinguish proven, bounded-only, failed, unresolved and unsupported
   results. Preserve true DUT counterexamples rather than weakening checks.
4. Obtain a fresh independent code/evidence review and freeze the new contract,
   checker, driver, coverage denominator, feedback selection and budgets.
5. Replay existing saved actions under that freeze. Require the same pins/counters,
   inspect property-level uncertainty and ensure no remaining checker/infrastructure
   defect or unsupported assumption is driving the verdicts. Incomplete batches
   remain pending, not failures or automatic passes.
6. Only after those gates pass, register and execute fresh independent B/C sessions
   with the original resource limits and identical common feedback. Obtain new keys
   via the existing hidden staging scripts at the appropriate stage.

“Meets the standard” does not mean every signal or hidden behavior is proven. It
means the claimed measurement/checker scope has executable, validated obligations;
unknown properties are local and explicit, and cannot be mistaken for a checked
pass or an unsupported defect. If essential measurement claims remain dependent
on unknown behavior, B/C stays blocked. This is not permission to relabel all
hard cases out of scope after seeing outcomes.

The old 17 WBXBAR targets are still known-easy. A reliable rerun can validate the
repaired feedback pipeline; it does not make those targets more discriminating
or guarantee a C advantage. A separate effectiveness benchmark needs the original
ordinary-operation exclusion and independent B difficulty screen.

## First Claude design and integration review

The single specification-only design call completed using exact
`claude-opus-5-5`, low effort, tools disabled and a $4 CLI budget. It took
114.44 seconds and reported $0.623196. Token accounting is 4 uncached input +
81,724 cache-creation input + 10,728 output = **92,456** tokens; 3,455 thinking
tokens are already included in output. No stimulus-generation calls were made.
The staged credential was deleted after the call.

The proposal retains feasible ownership histories instead of choosing one owner,
checks responses against those histories, and distinguishes observable trace
consistency from hidden identity. It also proposes formal obligations for routing,
request multiplicity, response data/order, reset and cancellation. These are
**design proposals, not implemented or proven properties**.

The first wrapper exited 1 because `ready_for_implementation` contained an
explanatory string, not a boolean. The prompt had listed the key without explicitly
specifying its type. The API itself succeeded. The full original response and
wrapper are preserved, and the decoded design was saved without coercing the
string to `true`. A formatting retry would add no scientific evidence and was not
made. The wrapper now retains such text while withholding automatic readiness.

Integration review raised seven substantive questions for an independent reviewer:

1. One clean candidate among other unknown candidates cannot automatically certify
   all properties or actual ownership. Separate existential trace consistency,
   universal checked properties and unresolved obligations.
2. Equal payloads do not justify merging transactions at different FIFO positions;
   canonicalization must preserve order edges, references and multiplicity.
3. Components can share master/slave ordering and cancellation dependencies even
   when payload identities differ. Partitioning and resource fallback need a sound
   dependency boundary.
4. Formal ghost tags cannot assume the correct correspondence they purport to
   prove. Define assignment, observability and quantification independently.
5. A quiet-interval bound does not permit forgetting canceled identities before
   restart. Repeated aborts must not alias a one-bit epoch tag.
6. ERR assertions must retain the contract's unknown timeout cases; finite ghost
   counters need explicit overflow treatment for unbounded claims.
7. Removing cross-slave forward-order inference must not silently remove supported
   same-slave side-effect or response-order requirements. Review changed control
   classifications before replay.

The reviewer also receives exact corrections to three read-data constants
misquoted in the design prose; original traces and model output are unchanged.
These integration questions are not substitute checker rules authored by GPT.

The fresh review packet is 139,048 bytes and contains public specification,
the proposed design, all seven synthetic scenarios and an existing synthetic
live/canceled-identity ambiguity case. It excludes DUT RTL, actual experiment
trajectories, coverage rankings and version-specific proof outcomes. Seven offline
tests passed: original hashes, lossless role packet contents, prompt-tamper
rejection, exact usage accounting, non-boolean readiness handling, no automatic
live permission, and key cleanup on mocked success/failure. Tests made no API or
simulator calls. The independently authorized review has completed; it cannot
by itself freeze a checker or authorize B/C.

The fresh reviewer returned **`ready_for_implementation: false`**. It identified
five blocking design findings: verdict semantics, unsupported symmetry reduction,
incomplete dependency partitioning, inconsistent resource fallback and circular
ghost-association risk. It also requested corrections to ERR/timeout properties,
restart/epoch handling, orphan-response treatment and legacy control labels.
The exact review is retained in `design-review-v1/review.json`. This was one
tool-free `claude-opus-5-5` call: 46.81 seconds, $0.511626, 89,882 tokens
(4 uncached input + 85,730 cache-creation input + 4,148 output). Together the first
design and review cost $1.134822 / 182,338 tokens. Their credentials were deleted.

The reviewer is evidence to assess, not an infallible oracle. Its R8 discussion
questions whether the live request matches the canceled identity. Direct extraction
from the synthetic pins shows that the accepted requests at cycles 7 and 12 and
the forward at 14 all have address 6, SEL 5 and data `0x23456781`; their enabled
lane bits are `0x00450081`. R6's proposed directional ERR rules still need live-work,
timeout and simultaneous-event guards. R5 must also distinguish existential trace
matching from a universally quantified association property. These issues are
explicitly included for the design author to resolve from public sources.

Five additional synthetic scenarios cover A-B-A FIFO positions, differently
associated equal requests, overlapping ambiguous/distinct work, later data change
and two aborts before an identical restart. The unchanged v4 checker reports no
input-assumption violations on them; that does not approve their final semantic
labels. Its two overlap cases both remain unresolved, including the data-change
case. There are **81 complete controls / 2,227 rows** in the revision packet:
69 preserved historical controls + seven earlier new controls + five additions.
Lossless vector encoding reduces the author prompt to 120,482 bytes. All 81 traces
round-trip exactly. Ten offline transport/integrity tests pass; no new simulator
or stimulus-model calls were used.

The separately authorized design revision and fresh review completed in
`design-revision-v1/`. The revision withdraws symmetry quotienting and component
partitioning; it keeps explicit histories, monotone software epoch numbers and
explicit unresolved-on-limit behavior. It also distinguishes reference-membership
checking from proof of hidden ownership. All 81 cases received assessments. The
fresh review again returned **`ready_for_implementation: false`**.

The main remaining issues concern an ERR while a request is still stalled and
unaccepted; preserving an earlier valid-prefix DUT diagnostic when later input
becomes invalid; payload checking restricted to identity-bearing byte lanes;
inferred inactive-CYC response rules; useful formal negative controls; and reporting
the fraction of checking suspended after resource exhaustion. Possible starvation
does not establish that a particular ERR is legal; it must not become a guessed
timing oracle.

The review's F6 cycle correction is itself wrong. Full raw rows and lossless decode
both give master acceptances at 6/10/14, slave acceptance at 16, slave ACK at 17 and
master ACK at **18** for `new_epoch/two_aborts_then_identical_restart`. No trace was
changed to match the prose. The next packet includes mechanically extracted
**pre-edge** event ledgers to prevent post-edge observations being counted as new
transfers. It also flags that K6 active-cycle retirement does not automatically
establish an independent violation for an inactive-CYC raw output.

This pair used exact `claude-opus-5-5`: author $1.129866 / 105,635 tokens /
367.37 seconds; review $0.488801 / 74,010 tokens / 84.87 seconds. The four completed
design/review calls total **$2.753489 / 361,983 tokens**. Thinking-token subsets are
not added again. Credentials were deleted after the pair. There are still zero
new functional checker implementations, stimulus-generation calls or B/C executions.

Seven more synthetic controls now exercise unaccepted stalled ERR versus ACK,
valid-prefix data checking before a later input error, and irrelevant versus enabled
payload changes during stall. The 88-case exact-patch packet is 129,560 bytes;
all old rows remain unchanged. Thirteen offline checks pass, including exact patch
preconditions, preservation of all control names, lossless decoding, event timing,
bounded calls and no automatic live permission. These test integration, not a new
functional checker.

The exact-patch pair in `design-patch-v1/` has completed: 14 exact JSON-value patches
and seven added control assessments were applied without GPT editing expected
semantics. Its reviewer accepts the revised valid-prefix handling, identity masks,
resource reporting and explicit exclusions, but still returns **not ready** for
implementation. Two findings remain around unexplained ERR association:

- With older live work and a held unaccepted request, an ERR may not be forced to
  retire the oldest accepted entry. That choice could make a later genuine ACK
  appear corrupt. The possible interpretations and their uncertainty must remain.
- The final acceptance edge and CYC-withdrawal edge need explicit response
  qualification. The latter may already overlap K13; the next author must check
  the actual row ordering rather than blindly add a redundant exception. No
  undocumented starvation timing bound is supplied.

The reviewer now agrees with the mechanically verified cycle ledger. This pair
cost $0.954012 / 155,872 tokens (author 80,180 / $0.522021, review 75,692 /
$0.431991), with no model substitution. The six completed calls in this phase total
**$3.707501 / 517,855 tokens**. Both calls completed and the staged key was deleted.
These are checker-design costs, separate from all historical stimulus-model costs.

Three additional ERR-boundary controls have been prepared before any further call;
the new packet preserves all previous 88 traces and now has 91 cases. Its pre-edge
ledger distinguishes the held request's acceptance, ERR and the older request's
later ACK. The packet is 136,936 bytes and passes 14 offline integrity/transport
checks. The first attempt using `design-patch-packet-v2/` failed authentication
with provider HTTP 401 before any model design was returned. The independent review
was not attempted. CLI terminal accounting reports zero tokens and $0; the original
wrapper's earlier-exit metadata is preserved, with the terminal result recovered
separately in `design-patch-v2/author/recovered-error-result.json` and documented
in `design-patch-v2/failure-accounting.json`. The failed key was deleted.

The first replacement attempt, `design-patch-v2-retry1/`, also stopped before any
model response. Its cause was different: CLI rejected non-ASCII characters in the
staged header value locally. It did not produce an HTTP response; CLI terminal
usage and cost were again zero. Both failures and their recovered terminal
accounting are retained separately. Neither attempted its planned reviewer.

The hidden staging script now rejects non-ASCII values and inputs outside the
expected `sk-ant-` alphanumeric/underscore/hyphen form before writing anything.
It rejects quoted values, whole export commands and another provider's key;
messages never echo the entered value. Success still means local format checking,
not authenticated provider access. Three offline tests cover rejection/no echo,
0600 file and 0700 directory permissions, and refusal to overwrite a staged key.
An initial test erroneously treated the public `sk-ant-` prefix in a fixed error
message as a leaked secret; its assertion was corrected, then all three passed.
The 14 existing conformance transport tests also pass after this helper change.

The locally format-checked replacement successfully called exact
`claude-opus-5-5` in `design-patch-v2-retry2/author`: 80,763 tokens, $0.482771,
53.34 seconds. It returned three design patches and three new assessments.
The strict integration guard then stopped on a wrong list index in the third
patch, before calling the reviewer. The key was cleaned up by that failure path.

The model supplied index 8, but its complete `before` text uniquely equals item 9
of the same parent list. Item 8 is the distinct per-slave response-count invariant.
A separately recorded **location-only correction** changes 8 to 9; every Claude
`before`/`after` text and added assessment is byte-for-byte preserved. The original
rejected response stays immutable. `location-correction-audit.json` records the
unique match, derived hashes and retention of the per-slave rule. It creates only
a review candidate, not an accepted contract or checker. Fifteen offline tests
now pass, including reproduction of the original strict failure and exact
reconstruction of the corrected candidate. This avoids a paid generation retry
for an unambiguous transport error without concealing the failed guard.

The candidate branches over an ERR attributed to older live work versus an
unaccepted held request; it adds acceptance-edge alternatives and generic propagation
of unknown tags. These are still proposed semantics, not a validated checker.
The seven completed model responses in this phase total **$4.190272 / 598,618
tokens**, with two additional zero-reported-usage credential failures and one
separately recorded transport rejection. No usage is counted twice.

The user has staged a key for only the remaining planned independent review.
The hashed packet `err-boundary-review-packet-v1/` is 137,854 bytes and includes
all 91 controls, the full candidate and the location-correction evidence.
`err-boundary-review-v1/` completed and returned **`ready_for_implementation: true`**.
The reviewer checked the ERR/ACK distinction, acceptance and withdrawal edges,
older-live versus held-request alternatives, valid-prefix diagnostics and identity
masks against the full rows. It also confirmed that the exact before-text uniquely
selects index 9, retaining the separate per-slave invariant at index 8. This call
used 79,271 tokens, $0.445611 and 33.72 seconds. The staged key was deleted.

The remaining non-blocking limitation is explicit: repeated HR ERRs during one
held request are absorbed as unknown alternatives and **are not judged**. They
cannot be called normal behavior, successful recovery or confirmed DUT defects.
Candidate-history consistency is not a proof of actual hidden ownership. Formal
obligations and implementation-specific cancellation bounds remain unproved.

This design phase now records **eight completed model responses, two credential
failures, one separately accounted transport rejection, 677,889 tokens and
$4.635883**. The transport rejection's successful model usage is counted once.
The reviewer permits checker implementation within the declared scope; it does
not certify code, freeze a new experiment or authorize live B/C.

## Next phase: implement and validate the reference checker

An isolated implementation packet has been prepared in
`results/wbxbar_reference_checker_20261104/spec-packet-v1/` (83,498 bytes).
It copies the reviewed reference clauses exactly, includes the public interface
and prior Claude files for reuse, and withholds full private control trajectories
and their case-assessment table. No DUT RTL or B/C outcomes are supplied. Three
additional offline tests verify exact contract transfer, isolation, hashes,
bounded invocation and preservation of the original experiment limits.

The authorized one-call generation completed successfully in `claude-author-v1/`:
exact `claude-opus-5-5`, low effort, no tools, $4 CLI budget, 600-second timeout.
It took 544.524 seconds and cost $1.498306. API accounting is 4 uncached input +
34,242 cache-creation input + 66,354 output = **100,600 tokens**; 41,968 thinking
tokens are already included in output, not added again. The staged key was deleted.
This cost is separate from the preceding eight successful design calls and two
failed credential attempts. GPT did not edit the generated functional logic.

The candidate's checker SHA256 is
`aabd8f399a5fcc7ff53c42cfc381d4d4fd8e260ff73235c72aa7df1d366637f2`.
`evaluate_wbxbar_reference_checker.py` ran the immutable candidate in isolated,
CPU/time-bounded workers with no credential environment. Results in
`results/wbxbar_reference_checker_20261104/evaluation-v1/`:

| Evidence | Observed result | Interpretation |
| --- | --- | --- |
| Claude author selftests | 39/39 pass | Useful author checks, not independent validation |
| Reviewed synthetic cases | 91/91 expected classifications | Labels came from the reviewed design, before implementation |
| Heldback interface transformations | 36/36 expected classifications | Master-port renaming and three extra initial reset rows; labels still need fresh reviewer scrutiny |
| Resource-limit controls | 6/6 expected classifications | Exhaustion, direct-pin fault after exhaustion, and reset resumption without erasing earlier uncertainty |

The 127 normal controls contain **46 scoped passes, 46 synthetic DUT violations,
33 unresolved and 2 invalid-input cases**. Agreement does not turn unresolved
cases into passes; synthetic violations are not findings about the actual WBXBAR
DUT. No new DUT simulation, saved-action replay or stimulus-generation call ran.
The lowered limits are test-only; defaults remain 4,096 histories, 64 live entries
per master and 256 canceled entries. No original experiment budget changed.

A fresh read-only code-review packet is prepared in
`results/wbxbar_reference_checker_20261104/code-review-packet-v1/`.
It retains all four generated artifacts, the public specification, the reviewed
contract, **all 133 full control traces and all 133 full checker results**. Pin-vector
and dictionary-delta encodings were round-trip checked; no diagnostic or scope count
is sampled away. Nine offline tests pass for commissioning, control provenance,
packet losslessness, tamper rejection, single-call transport and key cleanup.

The first local packet-size check rejected 269,636 bytes before any API call.
For this larger full-code audit, the local transport cap is explicitly 300,000
bytes rather than the earlier 150,000-byte design-packet convention. The retained
author response reports a 1,000,000-token context window; actual reviewer acceptance
has not been tested. This packaging limit is separate from the unchanged B/C token
budget and the proposed one-call $4 review budget. Evidence was retained rather
than truncated to fit the former local cap.

The reviewer must inspect exact history branching, HR ERR alternatives, canceled
identity multiplicity, prefix faults, reset and resource-exhaustion behavior, and
whether per-clause status/scope reporting matches the executed code. In particular,
aggregate row exposure is not an activation count for every individual property.
K5/C1–C4 exclusions, inferred K6/K13 clauses, unjudged repeated HR ERRs and unproved
formal obligations must remain explicit. The original checker and all historical
results are unchanged. Fresh code review, a separate freeze and saved-action replay
are still required; no new B/C experiment has started.

Completed evaluation and offline reproduction commands (use a new output directory
for a new evaluation; never overwrite retained evidence):

```sh
.venv/bin/python scripts/evaluate_wbxbar_reference_checker.py --candidate results/wbxbar_reference_checker_20261104/claude-author-v1 --output results/wbxbar_reference_checker_20261104/evaluation-v1
.venv/bin/python -m unittest discover -s tests -p 'test_wbxbar_reference*.py' -v
```

The following fresh read-only review command has now completed; do not rerun it:

```sh
.venv/bin/python scripts/prepare_wbxbar_reference_review.py run --packet results/wbxbar_reference_checker_20261104/code-review-packet-v1 --output results/wbxbar_reference_checker_20261104/code-review-v1
```

## Independent code review and focused reproduction

The one authorized read-only review completed in 47.357 seconds, using exact
`claude-opus-5-5`, low effort and no tools. It returned
**`ready_for_replay_registration: false`**. Cost: $0.724751; 4 uncached input +
127,675 cache-creation input + 4,318 output = **131,997 tokens**. The 2,657 thinking
tokens are an output subset. Together with authorship, this implementation phase
has two completed responses, **232,597 tokens / $2.223057**. The key was deleted.
The larger review packet was accepted by the model; no transport retry occurred.

The reviewer disclosed that it performed static inspection and spot checks, not
independent execution or full decoding of every trace. Its conclusions are evidence
to investigate, not an infallible oracle. GPT therefore added nine public-pin
synthetic probes, evaluated against the immutable Claude candidate in isolated
workers. Full inputs, outputs and source snapshots are in `review-repro-v1/` and
`review-repro-v2/` under the implementation evidence directory.

| Review issue | Independent observation | Required action |
| --- | --- | --- |
| F1: discarded uncertainty/epoch evidence | A held-request ERR at row 8 is retained when later ordinary work completes. It disappears after branching exhaustion at row 15, or history-set death at row 19; the affected epoch is absent from `pending_alternatives`. Global verdicts remain unresolved/violation respectively. | Preserve provenance at loss of histories, explicitly distinguishing prior feasible uncertainty from histories later refuted. Never erase the fault or assert hidden ownership. |
| F2: activation versus exposure | A reset-plus-idle trace marks conditional ERR/cancellation/response properties `checked_not_refuted`; reports have no per-clause activation counts. | Claude must define/count actual activation units and checked/unknown/suspended scope, with `not_activated` where applicable. No activation is not itself a DUT violation. |
| F3: undisclosed truncation | A trace with ten equal accepted identities and two forwards leaves 90 histories but displays only 16 pending/tag entries. A corruption case also exercises the eight-witness display cap. | Report total, displayed and omitted counts; do not prune actual histories. |
| F4: same-edge projection classification | Duplicate ACK alone is rejected; adding an unrelated same-edge invalid held input moves the count/history diagnostics to `mixed_same_edge`. The review's statement that both projections count row-e accepts is inaccurate: current K6 uses `x < c`, whereas K4 includes current-row accepts. | Have Claude explicitly resolve each projection's input dependencies and invalid-boundary semantics, then independently review the decision. Do not impose a GPT golden label. |
| F5: unsettled implementation decisions | The author contract itself lists B2 on an already-forwarded entry, hypothesis-dependent undefined read data and undefined DUT controls as unresolved decisions. The corrected same-row HR accept/forward probe remains unresolved without a failure. | Resolve or explicitly bound each decision; the fixed integer driver does not excuse ambiguity in the checker's declared input scope. |

The first version of the last probe mistakenly forwarded SEL=15 when the accepted
request had SEL=5, producing an appropriate identity mismatch. This fixture error
is retained, with its original builder and outputs. Version 2 copies the accepted
identity into the forwarded request; all eight other probes are byte-for-byte
equivalent as decoded JSON. The invalid first probe is not evidence about B2 and
is not credited as detection of a real DUT defect. All nine v2 probes execute
without infrastructure errors; only the intentionally invalid-boundary probe has
an environment violation. No DUT simulator or experimental model was invoked.

`repair_wbxbar_reference_checker.py` prepares `repair-packet-v1/` (134,350 bytes):
public spec, exact reviewed contract, current Claude source, raw review and all nine
focused traces/results. Full heldback controls and real B/C results remain withheld
from the author. The next call is limited to one Claude exact-text repair request,
$4 CLI budget and 600 seconds. Ambiguous/nonmatching patches are rejected rather
than repaired by GPT. Proposed contract decisions require a fresh reviewer.

Thirteen focused offline tests passed at preparation, including full trace/result
roundtrips, the SEL correction's provenance, exact patch matching and cleanup on a
mocked failed call. The subsequently authorized repair and validation are recorded
below. A fresh code review remains required before any separate replay freeze.
Original DUT, driver,
17 target counters, 2,845 denominator, B/C budgets and historical results remain
unchanged. These are checker-reliability findings, not new evidence for C efficacy.

```sh
# Already completed; retained outputs must not be overwritten.
.venv/bin/python scripts/probe_wbxbar_reference_review.py --output results/wbxbar_reference_checker_20261104/review-repro-v2
.venv/bin/python -m unittest discover -s tests -p 'test_wbxbar_reference*.py' -v
# Subsequently completed; do not overwrite the retained candidate.
.venv/bin/python scripts/repair_wbxbar_reference_checker.py run --packet results/wbxbar_reference_checker_20261104/repair-packet-v1 --output results/wbxbar_reference_checker_20261104/repair-v1
```

## First exact code repair: partial improvement, offline gate still fails

One authorized Claude call completed in **101.270 seconds**, costing **$0.513766**:
4 uncached input + 57,194 cache-creation input + 11,389 output = **68,587 tokens**.
The 5,895 thinking tokens are already in output. Requested/returned model remains
`claude-opus-5-5`; no retry or tool use. The staged key was deleted. Implementation
phase totals are now **three completed calls, 301,184 tokens / $2.736823**. Earlier
design-phase and experimental model costs remain separate.

All **23 exact Claude-authored patches** applied without manual correction. The
candidate is in `repair-v1/candidate/`; original artifacts remain unchanged.
New checker SHA256:
`66759fe3a5c6d8544c2e2d199d7a95f5d851a785057e45dfbb42ad08f1c438c3`.
`properties.json` was not changed by the author. Exact reconstruction from the
prior files plus raw patches is checked before preparing the next review.

`evaluation-original/` repeats the frozen synthetic control set: **127/127 normal
and 6/6 resource-limit classifications still agree**. Author selftests are now
**45/46**, with `mixed_same_edge_explicit` failing. Thus the aggregate offline
gate is **false**, even though the evaluation command completed normally and no
worker infrastructure error occurred. No expected labels or selftest code were
changed by GPT to make this pass.

All nine focused probes were also re-evaluated in `evaluation-focused/`:

- The row-8 unknown ERR is retained before exhaustion at row 15. A suspended epoch
  record now exists. A valid-row later contradiction records the prior tag as
  discarded-history evidence while preserving the DUT-violation verdict.
- Idle conditional clauses now report `not_activated`. The checker provides raw
  `clause_activations`, but **not per-clause checked/unknown/suspended counts**.
  Activations can occur after association checking is suspended, so these counts
  cannot be presented as successfully checked-property coverage.
- Ninety histories are explicitly reported as 16 displayed and 74 omitted; witness
  displays include shown/total/omitted counts. This changes reporting, not the
  exact-history set.
- Proposed P4 changes the same-edge duplicate-ACK/invalid-input result from
  `input_or_scope_invalid` to `dut_violation`, retaining an unresolved membership
  diagnostic. The old author `_mixed()` test has the same conflict. The isolated
  `selftest-diagnostic.json` retains its full trace and old/new outputs; the rule
  versus test expectation needs independent adjudication.

An additional tagged mixed-edge diagnostic combines an earlier unknown ERR with
a row-19 data mismatch and an invalid held input on the other master. The result
still withholds a definite DUT verdict (`input_or_scope_invalid` plus
`mixed_same_edge`), yet `discarded_epoch_evidence` describes all carrying histories
as refuted by a concrete contradiction. The prior unknown is absent from the
open-unknown list. That wording/status combination needs independent review of
valid-prefix uncertainty; it must not be treated as a proven refutation.

The next packet, `repair-review-packet-v1/`, contains current source, original
public spec/approved design, the prior review, proposed P1–P5 decisions, **all 144
complete traces/results** (127+6 original, 9 focused, 2 diagnostic), the failed
selftest and old outputs for the diagnostics. It is **367,250 bytes**. The local
review-transport cap is 500,000 bytes to retain the full expanded reporting; this
does not change frozen B/C token limits or the one-call $4 reviewer budget. The
subsequently authorized review is recorded below. Sixteen offline transport/provenance tests passed, including complete
roundtrips and a mocked positive reviewer opinion that still cannot override the
failed offline gate.

Next action is a fresh **read-only review of the contract decisions and remaining
defects**, not automatic acceptance or another stimulus experiment. Only Claude
may change functional rules or author selftest expectations. Any eventual revised
candidate still requires complete control validation, code review and separate
freeze before saved-action replay. No DUT simulation or new GPT model call was
made during this repair phase.

```sh
# Completed offline evaluation; use new output names for any later candidate.
.venv/bin/python scripts/evaluate_wbxbar_reference_checker.py --candidate results/wbxbar_reference_checker_20261104/repair-v1/candidate --output results/wbxbar_reference_checker_20261104/repair-v1/evaluation-original
# Completed subsequently; retain its raw review and do not rerun.
.venv/bin/python scripts/review_wbxbar_reference_repair.py run --packet results/wbxbar_reference_checker_20261104/repair-review-packet-v1 --output results/wbxbar_reference_checker_20261104/repair-review-v1
```

## Fresh repair review: ACK/ERR distinction and remaining reporting work

The authorized one-call read-only review completed in **34.050 seconds** and
returned **`ready_for_replay_registration: false`**. Exact model remains
`claude-opus-5-5`; no tools or retries. Cost **$0.910961**; 4 uncached input +
170,729 cache-creation input + 2,865 output = **173,598 tokens** (reported thinking
subset: 0). Key deleted. Implementation-phase totals are now **four completed
calls, 474,782 tokens / $3.647784**. No checker source or selftest changed in this
read-only phase; the current author selftest result remains 45/46.

The review narrows the required repair rather than granting a freeze:

| Decision | Review outcome | Remaining implementation |
| --- | --- | --- |
| P1: historical uncertainty | Accept pre-suspension flushing and definite valid-row death disclosure. Reject concrete-refutation claims at an invalid boundary whose DUT judgment is withheld. | Preserve valid-prefix tags as open unknowns when death becomes mixed; state the snapshot point, actual/projected histories and any dying-row omissions per event. |
| P2: property scope | Raw activations alone are insufficient. | Count actually checked, suspended, post-death and unknown-tag exposure per clause/sub-obligation. Keep association-free projections separate from attribution checks. |
| P3: truncation | Accepted: displayed/total/omitted counts are present; actual histories are not pruned. | Preserve this implementation. |
| P4: same-edge count | ACK-specific handling is accepted under the current scoped contract; the old ACK selftest expectation is stale. ERR-driven counts depend on current HR conditions and must remain mixed at the invalid boundary under the proposed conservative rule. | Claude must update the ACK selftest and separate ERR handling, with a companion ERR control. No GPT edits to expected verdicts. |
| P5: scope decisions | B2-forwarded, undefined DUT-control termination and first-row K13 are accepted as scoped decisions, not normative claims. | The undefined slave-read-data rule remains a gap unless justified independently. Sync contract and property documentation. |

R7 calls a suggested undefined-read-data rule “association-free” while still
referring to a FIFO read in “any history.” That suggestion does not, by itself,
remove history dependence. The next author packet highlights this inconsistency
and permits the explicitly disclosed gap offered by the reviewer; it does not
silently install the suggestion as a golden rule. The reviewer also states that
its review was static and not every one of the 144 traces was fully decoded.

Two independently constructed ERR companions in `repair-followup-controls-v1/`
replace the author diagnostic's master-1 ACK with ERR at row 3. The clean baseline
also restores the other master's held identity. Both currently produce a K6
`dut_violation`; the invalid-boundary case additionally has an environment error
and mixed membership diagnostic. Under the review's conservative ERR rule the
invalid-boundary verdict must become `input_or_scope_invalid` with mixed evidence,
while the clean baseline must retain ordinary violation detection. Full rows,
outputs, command and source hashes are retained. No DUT or API call was needed
for these two evaluations.

`followup_wbxbar_reference_checker.py` prepares `followup-packet-v1/`:
**161,938 bytes**, the immutable current candidate, exact public spec/approved
reference design, raw fresh review and **13 complete focused/diagnostic/ERR
companion traces and outputs**. The complete 133 independent controls and all
actual B/C results remain withheld from the author. Exact-text patch matching,
pure-source validation, one-call $4/600-second transport and key cleanup are
retained. Nineteen transport/provenance tests pass; this is distinct from the
failing functional selftest. This packet was subsequently executed as recorded below.

The original DUT, driver, coverage denominator/targets, budgets and historical
results are still unchanged. No freeze, saved-action replay, new GPT stimulus or
B/C run occurred. The remaining work is Claude-owned checker repair and complete
offline validation, followed by independent review before any new freeze.

```sh
# Executed once; preserved here for reproduction into a new evidence directory.
.venv/bin/python scripts/followup_wbxbar_reference_checker.py run --packet results/wbxbar_reference_checker_20261104/followup-packet-v1 --output results/wbxbar_reference_checker_20261104/followup-v1
```

## ACK/ERR author follow-up: improved, offline gate still fails

The authorized author call completed in **202.954 seconds**, using exact
`claude-opus-5-5`, low effort, no tools and no retries. Claude supplied **35 exact
patches**; GPT changed no checker rules or author selftest expectations. Cost was
**$0.840561**; 4 uncached input + 69,437 cache-creation input + 24,668 output =
**94,109 tokens**. The 14,453 thinking tokens are already included in output.
The key was deleted. Implementation totals are now **five completed calls,
568,891 tokens / $4.488345**, separate from the earlier design phase.

Candidate `results/wbxbar_reference_checker_20261104/followup-v1/candidate/checker.py`
has SHA-256 `99d12449ef9c3ff11757ca6651b5d953ddc9e37c2920f469879a0ba68a6b6776`.
Its parent and all earlier candidates remain unchanged. Evidence is in
`followup-v1/evaluation-original/`, `evaluation-focused/`,
`author-test-diagnostic.json` and `offline-audit.json` beneath that result root.

| Offline check | Observed result |
| --- | --- |
| Original independent control classifications | 127/127 normal and 6/6 resource-limit classifications agree; no worker errors. |
| Claude author selftests | **53/54 pass**. `mixed_death_keeps_prefix_tag_open` fails. |
| Focused evidence | All 13 cases execute; four additional diagnostics preserve full rows and results. No DUT simulation or API call is involved. |
| ACK/ERR pair | ACK-specific count failure remains visible at the invalid boundary. The ERR companion becomes input-invalid with mixed evidence; its clean baseline still detects a violation. |
| Property accounting | New sub-obligation fields separate checking, suspension and post-death exposure. K11 environment checks are missing from this instrumentation. |
| Evidence transport | 21 tests pass, including exact reconstruction of all four authored files and lossless transmission of 17 traces, outputs and per-case limits. This does not certify the checker. |

The remaining selftest is a real evidence-retention defect, not another stale
expected verdict. In the author's `_tag_mixed()` trace, rows 0–7 retain an unknown
`possible_starvation_err` from cycle 3. At cycle 8 a stalled request changes
address, making the input invalid. Candidate histories are still active at that
boundary: no history-set death has occurred. The full result says
`prefix_unresolved` but its unresolved-record list is empty. The new `boundary()`
logic preserves old tags only when history death is reclassified as mixed; it
does not yet handle this ordinary invalid-input boundary. The failing fixture
and its shorter valid prefix are both retained. Changing its expected verdict or
moving the invalid edge merely to satisfy the current implementation is not an
acceptable repair.

Two reporting gaps remain. In `focused/tag_then_exhaustion`, K11 has 33 raw
activations but all measured sub-obligation scope counts are zero, despite actual
environment checks. Also, old proposed P1/P4 contract paragraphs contradict the
new mixed-boundary/ACK-only rules, and the status enumeration omits
`not_activated`. Claude also added a public per-slave FIFO rule for undefined
read-ACK data; its live/orphan selftests pass, but the new rule still requires
independent review and is not a formal conformance proof.

`scripts/prepare_wbxbar_boundary_completion.py` prepared
`results/wbxbar_reference_checker_20261104/completion-packet-v1/`: **212,753 bytes**,
the current candidate, approved design, latest independent review, and **17
complete focused/diagnostic traces and results** with exact resource limits.
The full 133 independent control inputs, DUT implementation and actual B/C
results remain withheld. The packet requests one targeted Claude correction of
valid-prefix retention, K11 accounting and documentation; it expressly preserves
the failing selftest. Its packet SHA-256 is
`321294c9eba19c12ae8d3e7b973e31193744bf941e3e31b0b41dcbbfd732cc09`.

```sh
# Executed once below; never overwrite the original evidence directory.
.venv/bin/python scripts/followup_wbxbar_reference_checker.py run --packet results/wbxbar_reference_checker_20261104/completion-packet-v1 --output results/wbxbar_reference_checker_20261104/completion-v1
```

The next call is bounded to one author response, a $4 CLI budget parameter and
600-second timeout. Complete offline controls must pass before a fresh independent
code review. No freeze, saved-action replay, new GPT stimulus or B/C run occurred;
original DUT, driver, source targets/denominator and experiment budgets stay fixed.

## Completion candidate: all original controls pass; fresh review pending

The one authorized completion call returned **ten exact Claude patches** in
**34.111 seconds**, with exact `claude-opus-5-5`, low effort, no tools and no retry.
It cost **$0.528926**: 4 uncached input + 90,786 cache-creation input + 3,749 output
= **94,539 tokens**. Thinking tokens (1,522) are an output subset. The staged key
was deleted. Implementation totals are **six calls, 663,430 tokens / $5.017271**;
earlier design costs remain separately recorded.

New checker SHA-256 is
`093baceb5d79d1bc87dd805c43584fef06428396c0f6b5e4be97a1d37891bdf3`, at
`results/wbxbar_reference_checker_20261104/completion-v1/candidate/checker.py`.
The selftest file is **byte-identical to its parent**: all **54/54** now pass,
including the previously failing valid-prefix case. All **127/127 normal and
6/6 resource-limit classifications agree**. No worker errors occurred. These
checks ran in isolated workers; no DUT simulations or GPT calls were added.

The checker now flushes the pre-row tag snapshot at an invalid-input boundary,
retaining `possible_starvation_err@3` when row 8 becomes invalid. K11 has an
association-free non-reset-row check counter: on the exhaustion control, raw,
eligible and checked counts are all 33. Schema checks and reset rule 3.20 are
explicitly excluded from this instrumentation. Historical P1/P4 proposals are
marked superseded, and the property-status list includes `not_activated`.

All **17 existing focused/diagnostic cases** were rerun with their original
resource limits. Five additional boundary probes preserve the same valid prefix
and alter only the next row. These are post-generation diagnostic probes, not
preregistered efficacy targets or new checker rules. Missing input/post fields,
non-contiguous cycle numbering and undefined input control all retain the old
unknown tag. The fifth probe, undefined DUT `o_mstall`, yields a pin-level
`dut_violation` and `unjudgeable_row`, but still omits the earlier unknown ERR
record. The integer JSON driver cannot emit this value; that limitation does not
automatically waive the checker's evidence-retention requirement. The reviewer
must assess whether repair or an explicit, justified scope restriction is needed.
The genuine undefined-output failure must not be suppressed. The public-pin
FIFO rule for undefined read-ACK data also remains an unreviewed scoped assumption.

Across all **155 results**, sub-obligation and clause activation totals equal
checked + suspended + post-death totals. This is arithmetic consistency, not
proof that every activation is instrumented correctly. The original control
gate passes; overall validation/replay readiness remains **false pending review**.

The complete fresh review packet is
`results/wbxbar_reference_checker_20261104/completion-review-packet-v1/`, prepared
by `scripts/prepare_wbxbar_completion_review.py`. It retains all **155 full traces,
results and per-case limits**, exact source/contract files, prior review and author
decisions, while withholding actual DUT/B/C evidence. Five malformed-input probes
are stored as literal rows because ordinary vector encoding assumes all fields
and contiguous cycles. An initial local packaging failure and a 524,664-byte size
rejection are retained; neither issued an API call. Interning repeated result
dictionary paths reduces the packet to **409,079 bytes**, within the unchanged
500,000-byte review transport cap. No values, diagnostics or traces are removed.
All **24 transport/provenance tests pass**, including exact patch reconstruction,
155 lossless trace/result round trips and rejection of tampered evidence.

```sh
# Executed once below; original review evidence must not be overwritten.
.venv/bin/python scripts/review_wbxbar_reference_repair.py run --packet results/wbxbar_reference_checker_20261104/completion-review-packet-v1 --output results/wbxbar_reference_checker_20261104/completion-review-v1
```

Evidence and costs are in `completion-v1/offline-audit.json`, the three
`evaluation-*` directories, `completion-v1/author-call/metadata.json`, and the
phase-level `claude-costs.json`. All old candidates/results are preserved.
No new freeze, saved-action replay or B/C run has occurred; original budgets,
source targets/denominator, DUT and fixed driver remain unchanged.

## Fresh completion review: termination reporting still blocks replay

The one authorized read-only review completed in **23.715 seconds**, returning
`ready_for_replay_registration: false`. Exact model: `claude-opus-5-5`, low effort,
no tools or retries. Cost **$1.027671**; 4 uncached input + 198,607 cache-creation
input + 1,731 output = **200,342 tokens**, with zero reported thinking tokens.
The key was deleted. Implementation-phase totals are now **seven calls,
863,772 tokens / $6.044942**. All four candidate artifact hashes remain unchanged.

| Review item | Outcome and independent evidence check |
| --- | --- |
| N1: unknown evidence on undefined DUT termination | Confirmed. The valid prefix contains `possible_starvation_err@3`; the `pd`-only termination at row 8 drops it and reports K6 as `checked_not_refuted`. The real K10 DUT violation remains correct. |
| N2: pending work and prefix scope | Confirmed. The prefix projection has two live entries in each of two feasible histories. The terminated result omits that active epoch, leaves `prefix_status` null and K12 `not_activated`. |
| N3: environment/schema/mixed-boundary handling | Accepted by the reviewer for the supplied scope. Existing original-failure and malformed-input controls retain their tags. |
| N4: K11 instrumentation | Accepted as non-reset processed-row exposure, with schema and reset-rule checks explicitly outside that instrumentation. This is not formal coverage. |
| N5 and contract decisions | Pin-FIFO read-data rule accepted as a scoped, non-normative assumption; ACK-only P4 accepted. Formal obligations and earlier exclusions remain open. |

N1/N2 are related reporting problems on one termination path, not two confirmed
DUT defect types. The reviewer requires preserving the genuine undefined-output
failure while reporting valid-prefix uncertainty, pending work and prefix scope.
Undefined DUT output is not an environment violation; a repair must not silently
relabel it as input invalid, normal batch end or reset.

The reviewer explicitly states that it used static reasoning and selectively
decoded boundary, focused and limit cases; it did **not** fully reconstruct all
155 cases. Local transport tests reconstruct the complete evidence, but that is
not equivalent to a complete semantic review or a correctness proof.

Three supplementary synthetic controls ran against the unchanged candidate:
termination after resource suspension retains its already-flushed tag; termination
after a valid membership failure preserves that earlier failure; a reset suffix
after undefined-output termination is not processed. They prevent the targeted
repair from hiding previous failures, double-counting old evidence or inspecting
later rows. Results are preserved in `termination-controls-v1/`; no simulator or
API calls were needed for these controls.

`scripts/prepare_wbxbar_termination_repair.py` prepared `termination-packet-v1/`
under the reference-checker result root: **205,642 bytes**, current source/spec,
the exact fresh review and **nine complete focused/prefix/termination cases** with
limits and outputs. The full 133 independent controls, DUT implementation and
actual B/C results remain withheld from the author. It requests only a targeted
Claude-owned termination reporting repair plus meaningful selftests, preserving
all current checks and budgets. **26 transport/provenance tests pass**. A future
candidate must rerun all 155 prior cases plus these three controls and undergo
fresh review; there is no waiver based on the integer driver's inability to emit
`None`.

```sh
# Executed once below; preserve the original evidence directory.
.venv/bin/python scripts/followup_wbxbar_reference_checker.py run --packet results/wbxbar_reference_checker_20261104/termination-packet-v1 --output results/wbxbar_reference_checker_20261104/termination-v1
```

Raw review and integration audit: `completion-review-v1/review.json` and
`completion-review-v1/integration-audit.json`. No checker edits, new freeze,
saved-action replay, GPT stimulus calls or B/C runs occurred in this review phase.

## Termination repair: observed controls pass, independent review pending

The authorized author call completed in **51.791 seconds**, exact
`claude-opus-5-5`, low effort, no tools/retries. Claude returned **12 exact patches**
applied only to a new candidate. Cost **$0.628751**; 4 uncached input + 102,991
cache-creation input + 5,689 output = **108,684 tokens**. The 2,187 thinking tokens
are included in output. Key deleted. Implementation-phase totals: **eight calls,
972,456 tokens / $6.673693**, excluding the separately recorded design phase.

Candidate checker SHA-256:
`682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d`, under
`results/wbxbar_reference_checker_20261104/termination-v1/candidate/`.
All **58 author selftests pass**; AST comparison confirms that all **54 prior test
expressions are unchanged** and four tests were added. All **127 normal and six
resource-limit control classifications agree**. The **25 supplemental cases**
were executed anew with their original limits, for **158 evaluated cases** total;
no infrastructure errors, DUT simulations or GPT stimulus calls occurred.

The targeted row-8 termination now retains `possible_starvation_err@3` exactly
once, reports two pending live entries per feasible history, and returns
`prefix_unresolved` with K6/K12 unresolved. The genuine K10 DUT violation and
`unjudgeable_row` remain. `termination_boundary=8` and its explicit reason are
separate from `input_validity_boundary=null`. The prefix closure has the distinct
reason `terminated_unjudgeable_dut_output`, not reset or ordinary batch end.

Supplementary controls confirm no duplicate unknown after resource suspension,
no loss of the prior valid membership failure, and no processing of a reset
suffix after termination. **154 non-termination results match the prior JSON
values after removing only the two new null
termination fields**; the four termination cases have the intended reporting
changes. All 158 activation partitions remain arithmetically consistent. These
observations support the targeted repair, but do not certify the whole checker.

One metric scope question is explicitly included for review: K12 pending work at
termination is unresolved but deliberately not a normal batch-end activation;
`unknown_tag_records` counts the named historical tags rather than every type of
unresolved diagnostic. The reviewer must assess whether the documentation and
reported scope make that distinction sufficiently clear.

The versioned `termination-v1/prepare-review.py` reuses the existing lossless
encoding and read-only review runner. It prepared `termination-review-packet-v1/`
with **158 complete newly evaluated traces/results**, exact per-case limits,
current code/contract, previous review and author decisions: **418,586 bytes**,
within the same 500,000-byte transport cap. Actual DUT/B/C evidence remains
withheld. **28 transport/provenance tests pass**, including all 158 round trips,
exact patch reconstruction and preservation of the 54 previous test expressions.

```sh
# Executed below with the newly authorized retained-key wrapper.
.venv/bin/python scripts/review_wbxbar_retained_key.py --packet results/wbxbar_reference_checker_20261104/termination-review-packet-v1 --output results/wbxbar_reference_checker_20261104/termination-review-v1
```

Raw evidence: `termination-v1/evaluation-original/`, `evaluation-focused/`,
`offline-audit.json`, and `author-call/metadata.json`. All old candidates and
results are retained. No new freeze, saved-action replay or B/C trial has run;
the original DUT, driver, targets, denominator and experiment budgets stay fixed.

## Scoped validation complete; replay registration is next

The user explicitly changed the credential policy: retain the staged key through
necessary checker review/repair calls and delete it after validation. A new
`review_wbxbar_retained_key.py` wrapper reused the existing verified packet and
bounded CLI call without changing historical runners or prompts. It retained the
key after the review. `clarify_wbxbar_contract.py` then allowed only Claude-owned
`contract.md` edits and a fresh documentation review; functional changes were
rejected locally. Each call retained the **$4 CLI parameter / 600-second timeout**.

| Completed call | API-reported total tokens | Cost | Wall time |
| --- | ---: | ---: | ---: |
| Fresh termination code review | 206,641 | $1.082866 | 36.317 s |
| Claude documentation author | 25,982 | $0.155661 | 18.740 s |
| Fresh documentation review | 32,117 | $0.193146 | 22.520 s |

All requested/returned models were exact `claude-opus-5-5`, low effort, with no
tools or retries. This cycle totals **264,740 tokens / $1.431673**. Input totals
include cache-creation input once; reported thinking tokens are already within
output. Implementation-phase totals are **11 calls, 1,237,196 tokens / $8.105366**;
the preceding design phase remains separate.

The code reviewer returned **`ready_for_replay_registration: true`**, accepting
the N1/N2 termination fix, distinct input/termination boundaries, unknown retention,
pending-work disclosure, prefix qualification and preservation of earlier faults.
It decoded boundary/supplementary/focused/limit evidence and spot-checked remaining
cases; it did not execute code or claim full semantic reconstruction. This is
scoped review, not proof or certification.

Three nonblocking reporting clarifications were authored by Claude and independently
accepted: closure records use the last processed cycle while termination_boundary
names the unjudged cycle; rows_beyond_input_boundary is total rows minus processed
rows; unknown_tag_records counts classified tag records, not every unresolved
diagnostic or DUT coverage. The final artifacts are under
`results/wbxbar_reference_checker_20261104/documentation-v1/candidate/`.
The checker, selftest and properties files are **hash-identical** to the tested
termination candidate. The contract alone changes, SHA-256
`5de9e47953e147600381c1028b21ebeea8427f7c24471302e8d350c39f351868`.

The documentation review accepted the addendum with two nonblocking edge notes,
retained here rather than silently omitted:

- With invalid resource limits, all rows can be unprocessed even though neither
  input_validity_boundary nor termination_boundary is set. The governing formula
  remains total rows minus processed rows.
- K13 `same_edge_response_after_abort` records are emitted directly, not through
  history flushing. They still contribute to unknown_tag_records because the
  governing TAG_CLAUSE filter includes them.

`scoped-validation.json` binds the final four artifact hashes, both accepted reviews,
the exact documentation patch, original evaluations and audit. **58/58 author
selftests, 127/127 normal and 6/6 limit classifications, all 158 evaluated cases,
and 31 transport/provenance tests** support the declared gate. The documentation
variant reuses evaluation evidence because its executable artifacts are unchanged;
it is not presented as a new simulation experiment. Original scope hashes were
rechecked. K5 remains excluded; C1-C4/F1-F8, timeout/cancellation bounds, sub-row
reset and other declared limitations remain unproved. Repeated HR ERR remains
unknown. These limits must accompany any use of the checker.

After all checks and accepted reviews, the staged key was deleted; cleanup is
recorded in `credential-cleanup-after-validation.json`. This satisfies the updated
retention request. No additional key is needed to complete this review stage.

Actual commands for this final cycle:

```sh
.venv/bin/python scripts/review_wbxbar_retained_key.py --packet results/wbxbar_reference_checker_20261104/termination-review-packet-v1 --output results/wbxbar_reference_checker_20261104/termination-review-v1
.venv/bin/python scripts/clarify_wbxbar_contract.py --output results/wbxbar_reference_checker_20261104/documentation-v1
```

**Next at the close of this stage (now completed in the linked replay report):**
separately register and freeze replay of the saved B/C actions using
these final hashes, then reassess functional attribution while preserving original
results. The scoped gate does not itself freeze files, execute replay, establish
whole-IP correctness or authorize new B/C stimulus. No new replay, DUT simulation,
GPT stimulus call or B/C run occurred in this final review cycle.

## Artifacts and commands

- `scripts/probe_wbxbar_cancel_boundary.py`: original-version proof observer and
  bounded task runner; not a specification checker.
- `scripts/prepare_wbxbar_conformance_role.py`: seven synthetic controls and
  verified spec-only design packet (135,723 bytes).
- `scripts/run_wbxbar_conformance_design.py`: one tool-free Claude design call,
  CLI budget $4, timeout 600 seconds, exact model and credential cleanup.
- `scripts/review_wbxbar_conformance_design.py`: separately bounded fresh review
  with a hashed packet and no automatic live permission.
- `scripts/prepare_wbxbar_design_revision.py`: complete synthetic evidence,
  lossless packing and bounded revision/review pair; no checker source edits.
- `scripts/patch_wbxbar_conformance_design.py`: exact Claude-authored design-value
  replacement and fresh review; changes must match the original value exactly.
- `tests/test_wbxbar_conformance.py`: fifteen offline role-transport regressions.
- `results/wbxbar_conformance_gate_20261104/prepare-patch-v2.py`: reproducible
  preparation of the three remaining ERR-boundary scenarios and versioned packet.
- `results/wbxbar_conformance_gate_20261104/validation.json`: offline proof/packet
  evidence, versions and current live gates.
- `results/wbxbar_conformance_gate_20261104/baseline-v4/`: all seven old-checker
  outputs; original checker remains unchanged.

Each new attempt requires a new output directory. The initial three proof tasks
already ran, so do not overwrite them or rerun merely to edit this report.

```sh
.venv/bin/python scripts/run_wbxbar_conformance_design.py --packet results/wbxbar_conformance_gate_20261104/claude-design-packet-v1 --output results/wbxbar_conformance_gate_20261104/claude-design-v1
```

The design call above has completed; do not rerun it. The separately authorized
review uses a different, fresh session and output directory:

```sh
.venv/bin/python scripts/review_wbxbar_conformance_design.py run --packet results/wbxbar_conformance_gate_20261104/design-review-packet-v1 --output results/wbxbar_conformance_gate_20261104/design-review-v1
.venv/bin/python -m unittest discover -s tests -p test_wbxbar_conformance.py -v
```

No new functional checker, live B or live C is authorized by either response alone.
