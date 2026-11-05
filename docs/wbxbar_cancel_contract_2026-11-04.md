# WBXBAR cancellation contract revision and retrospective replay — 4 November 2026

**Completed:** Claude independently revised the cancellation contract and checker;
a fresh Claude session accepted the limited scope; the new checker was separately
frozen; all 42 saved seed/round batches were re-executed through the original
Verilator driver. Every public pin, transport ledger and original DUT coverage
counter matched the saved evidence. Original results were not rewritten.

The five final `dut_violation` verdicts become **unresolved**, while the sixth
remains unresolved. None becomes a functional pass. Every one of the 59 repeated
round diagnostics, including 18 instances in final cumulative traces, maps to an
explicit same-cycle, same-slave `post_abort_forward` unresolved record. They did
not merely disappear behind an ownership-ambiguity suspension.

## Contract and role separation

Claude alone produced exact patches to checker.py, selftest.py, properties.json
and contract.md. Its author packet contained the pinned public specification,
its own prior artifacts and six independent synthetic examples. It contained no
executable DUT, real DUT traces, B/C stimuli/results, coverage targets, semantic
groups or rankings. A new stateless Claude session reviewed all 69 controls,
source and contract. GPT/Codex supplied independent transport controls, integration,
measurement and saved-action replay; it made no checker logic edits.

The revised [Claude-authored contract](../results/wbxbar_abort_contract_20261104/claude-v4/candidate/contract.md)
distinguishes authoritative Wishbone rules, declared environmental assumptions,
inferred rules and unknown timing. Its cancellation treatment is:

1. On master CYC withdrawal, retain identities of accepted, unforwarded mapped
   requests as possible residual work. Public prose does not establish that older
   requests must survive cancellation before a later one can be observed.
2. A matching unconsumed old request can explain a downstream forward only as
   **unresolved post-abort behavior**, not as correct cancellation or completion.
   Record acceptance, abort and forward cycles; consume one identity per forward.
3. Unmatched/corrupted work, duplicate identity consumption and pre-reset identity
   reuse still fail. Enabled data bytes, address, direction and SEL remain checked.
4. Live/aborted or cross-master ownership ties remain unresolved. Ordinary live
   ordering and response/read-data checks are retained. Reset clears identities
   without erasing uncertainty already emitted for the cumulative batch.
5. No grace period, cancellation latency, timeout deadline or additional input
   restriction was invented. Unknown survivor sets and cancellation timing remain
   unresolved; matching a request never proves whole-IP conformance.

Authority: pinned Wishbone B4 PDF SHA-256
`d712d61fe7f363b671e6b821b7b0259f43ec0b4ce8f3b2072172b2878f347a5a`,
full relevant pages 31–37 extracted with Poppler, pinned WBXBAR introductory
comments/README, and the [author's crossbar explanation](https://zipcpu.com/blog/2019/07/17/crossbar.html).
The older article is supplementary prose, not version-specific timing authority;
its implementation examples were excluded from the author packet.

## Independent controls and review

The 46 prior controls were preserved. Twenty-three new synthetic scenarios cover
multi-request/partial cancellation, non-head and late residual forwarding, all
master/slave combinations, acceptance simultaneous with ERR, duplicate reuse,
identical live/aborted identities, reset separation, SEL masking, normal live
FIFO order, deliberate reordering and stale completion into a new epoch.

| Check | Old v3 checker | Revised v4 checker |
|---|---:|---:|
| Historical control classifications retained | 46/46 | 46/46 |
| New proposed classifications matched | 12/23 | 23/23 |
| Unresolved scenarios incorrectly labelled DUT violations | 10 | 0 |
| Ambiguous scenario incorrectly labelled scoped pass | 1 | 0 |

V4 passes **69/69 independent controls and 22/22 author selftests**. The independent
control accounting contains 16 detected mutations with clean positive baselines;
11 additional fault detections have unresolved baselines and are reported
separately. These are bounded controls, not an exhaustive proof. Claude's
selftests are not independent certification.

The original false-pass control is `multi_abort/live_aborted_same_identity`: a
live request and a non-head aborted request share an identity. The old checker
missed the old candidate and credited the live one; the revision records ambiguity.
This guards against fixing false alarms by simply accepting all residual work.

[Fresh read-only review](../results/wbxbar_abort_contract_20261104/claude-v4/review.json)
returned `ready_for_offline_gate=true`. It explicitly retained these limits:

- Cross-slave per-master forwarding order is an inherited inference, not clearly
  a public normative requirement. The replay-only freeze accepts this limited
  cancellation revision; any future alarm based on that inference requires
  separate source-based attribution. It is not a confirmed-DUT-defect oracle.
- Ownership ambiguity suspends ownership-dependent matching/data checks until
  reset; the overall result remains unresolved. Basic protocol checks still run.
  The review's phrase “all checks” is broader than the implementation.
- Exact timing, minimum reset duration, post-reset master ACK/ERR, eventual slave
  CYC withdrawal and general liveness remain outside the checked scope.
- Historical `negative/stale_after_reset` is an exclusion witness because master
  CYC is low. Its name is retained for provenance; it is not credited as detection.

The review neither executed the checker nor proved it formally. Independent
worker executions, counter/pin comparisons and the audit provide the execution
part of the evidence. The reviewers' prose is not treated as an oracle.

## Separate freeze and unchanged replay

Registration: [wbxbar_cancel_contract_v1.json](../configs/wbxbar_cancel_contract_v1.json),
SHA-256 `ed3e6213e2f4c4155895f780b7f926cd7adc85ac1f92d1c3d78f38546083b5f8`.
A manifest binds 258 original evidence files. Original RTL, specification,
driver, source targets, 2,845-point denominator, model settings and 3 × 6 × 64
cycle budget remain unchanged. There are **zero new stimulus-generation calls**.

Replay-only freeze: [wbxbar_cancel_replay_freeze_v1.json](../configs/wbxbar_cancel_replay_freeze_v1.json),
SHA-256 `c099939dabc20bb61a077efcdc89dbe044830d5600e534f8092a93299937f692`.
New checker SHA-256:
`64a5b7ab5da5fb46fa610e040589f8063b20ddbe806349ccc1a29e026f6a3468`.
Original checker SHA-256:
`163fd64a9fe3925b3cd64130c2b9a22e4489c1acfea36b985026c228aa6f3545`.
Original experiment freeze SHA-256:
`216ef3ea4cf3748c6a65be215bbdca7fb2c2ce832ff4dc745c1386641b5715aa`.
The freeze preserves the independent review limitations and disallows new live
experiments. It was written before examining the revised checker on live-pilot
traces. No change to any old checker verdict was made in place.

The exact saved JSON actions, seed, resets, fresh-counter cumulative replay and
absence of a hidden drain are preserved. The original verified Verilator binary
was reused (SHA-256
`5720db4797f9f372ac76f2478ed963ffeb3bf947d9385ed70f11b43a710d35c6`).
No recompilation or new Icarus run was needed; the earlier two representative
Icarus replays remain historical evidence, not new costs.

| Final session | Original verdict | Original diagnostics | Revised verdict | Revised diagnostics | Remaining unresolved records |
|---|---|---:|---|---:|---:|
| B1 | dut_violation | 1 | unresolved | 0 | 4 |
| B2 | dut_violation | 3 | unresolved | 0 | 3 |
| B3 | dut_violation | 2 | unresolved | 0 | 3 |
| C1 | dut_violation | 7 | unresolved | 0 | 11 |
| C2 | dut_violation | 5 | unresolved | 0 | 10 |
| C3 | unresolved | 0 | unresolved | 0 | 1 |

All 36 model-generated round batches are unresolved; the six common seed batches
remain scoped_pass. There are no new input-assumption violations. Final uncertainty
includes 19 post-abort forwards, 11 ownership ambiguities and two pending-prefix
records. These record counts are not independent defect counts. Every old final
alarm has an explicit post-abort counterpart, including two distinct slave alarms
on the same cycle; the correspondence audit consumes each match only once.

[Per-batch comparison CSV](../results/wbxbar_abort_contract_20261104/replay-v1/comparison.csv)
and [diagnostic correspondence](../results/wbxbar_abort_contract_20261104/replay-audit-v1/diagnostic-correspondence.json)
retain old and new evidence side by side. The original 59 repeated round reports
and 18 final instances are preserved; there are **zero confirmed new DUT defect
types** from this correction. Absence of new violations does not establish a pass.

Raw coverage and the earlier B/C conclusion remain unchanged: both arms hit all
17 targets in round 1, final line 82/86 and branch 79/88, with C using 43.30% more
mean API tokens to the raw target. Initial C toggle improvement remains an
observation with extra cost and no placebo isolation. Reclassification cannot
undo the old feedback seen by the model; these are not the trajectories a new
run under v4 would necessarily produce. This is a reliability correction, not a
new causal experiment or new evidence of E-graph superiority.

## Costs and verification

Two actual calls used exact `claude-opus-5-5`, low effort, tool-free fresh sessions,
600-second timeouts and CLI budget parameter $4 each. Both succeeded without a
retry: author **$0.520906 / 84,859 tokens**, reviewer **$0.439976 / 71,958 tokens**;
total **$0.960882 / 156,817 tokens**. Cache creation/read are separate input
categories; thinking and cache-duration breakdowns are not counted again.
These validation costs are separate from the original OpenAI pilot's 770,531 tokens.
The staged Anthropic key was deleted; no OpenAI credential was requested.

Additional replay: **42 executions / 8,360 physical cycles**, zero compilations,
1.6262 seconds simulator process time and 2.5587 seconds replay wall time.
A separate evidence audit executes the new checker again on all saved replay
traces, with zero additional DUT simulations or model calls. It recomputes every
raw counter and pin/transport trace and verifies all original hashes.

[Replay audit](../results/wbxbar_abort_contract_20261104/replay-audit-v1/audit.json)
passes all 42 batches and 2,845 source points per batch. Eight integration tests
cover unchanged evidence/budget, holdback, lossless review packing, tampered-packet
rejection, strict review gates and prevention of blanket uncertainty. Full traces
round-trip in the actual 147,770-byte review packet. Original DUT and pilot
artifacts remain unchanged. No commit or push is claimed.

Preparation failures are retained in this account: an initial glob matched
report.md and failed before registration; an oversized 209,948-byte review was
rejected offline, then packed losslessly; a missing pypdf import used installed
pdftotext instead; a test's assumption that all 11 mismatches were alarms was
corrected after identifying the false pass. These involved no model calls or new
DUT simulation. Complete raw evaluations remain on disk even though reviewer
summaries omit descriptive event/count fields.

## Reproduction and next boundary

Run from the repository, using new output directories; scripts refuse overwrites.
These commands require no API key:

```sh
.venv/bin/python -m unittest discover -s tests -p test_wbxbar_cancel.py -v
.venv/bin/python scripts/audit_wbxbar_cancel_replay.py --run results/wbxbar_abort_contract_20261104/replay-v1 --output build/wbxbar-cancel-audit-new
.venv/bin/python scripts/replay_wbxbar_cancel.py replay --freeze configs/wbxbar_cancel_replay_freeze_v1.json --output build/wbxbar-cancel-replay-new
```

The last command adds another separately counted 42 executions / 8,360 cycles;
it is unnecessary merely to read the report. The role runner, exact Claude
patches, prompts, responses, usage, independent control evaluations, freeze and
raw replay evidence are retained under `results/wbxbar_abort_contract_20261104/`.

Further conformance work should resolve the forwarding-order inference and use
explicitly scoped formal/public-contract checks for cancellation properties that
can actually be established. Ambiguous public behavior must remain unresolved.
A new effectiveness experiment would need its own freeze and authorization;
this completed replay does not authorize new stimuli or altered resource limits.
