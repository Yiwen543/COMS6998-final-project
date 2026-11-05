# WBXBAR exploratory B/C — separately registered 4 November 2026

The user requested relaxing difficulty admission so that this IP can be tested
with an independent Claude checker and a matched B/C comparison. This is a new
exploratory scope, **not a retroactive pass of the previous screen**. The prior
ordinary-screen rejection and all its raw evidence remain unchanged.

**Completed live result:** see [the result and attribution report](wbxbar_exploratory_bc_result_2026-11-04.md).
All 36 rounds ran and were audited; all six sessions hit the raw target in round 1.
C used 43.30% more mean tokens to target. Later independent attribution found a
checker abort-queue limitation, so functional conformance remains unresolved.
This document preserves the preparation history below; its pre-live statements
are historical, not the current run status. Final freeze SHA-256:
`216ef3ea4cf3748c6a65be215bbdca7fb2c2ce832ff4dc745c1386641b5715aa`.

Scope: [`wbxbar_exploratory_bc_v1.json`](../configs/wbxbar_exploratory_bc_v1.json),
SHA-256 `1a87bc051af7cff7e0819f463fe93a7cb029efd91171c5aa198afe895798bb31`.
It was registered before WBXBAR checker/model calls, but after observing that
handcrafted ordinary traffic hits all eight groups. Selection is therefore not
blind to offline difficulty. At that registration checkpoint there were no WBXBAR live stimulus outcomes.

## What changes, and what does not

| Requirement | New exploratory scope |
|---|---|
| Ordinary operations leave targets unhit | Waived; previous hits disclosed |
| Three disjoint late-event target families | Waived as an admission condition |
| B must pass the original difficulty gate before C | Waived; report B difficulty descriptively and run C regardless of rapid saturation |
| Conditional semantic proof and exact source mapping | Retained |
| Independent specification checker and validation | Retained |
| Original DUT, all raw counters, role separation | Retained |
| Equal model/cycle/token limits across arms | Retained |
| Freeze checker/driver/prompts/targets before live comparison | Retained |

The original tests used manually constructed ordinary stimuli. Easy attainment by
those controls is not direct evidence that an independent LLM will generate the
same inputs or achieve identical cost. The exploratory experiment can measure
that distinction. It may also confirm a ceiling effect and provide a useful
negative/easy-task control; a positive C result is not required.

## Fixed comparison

Use **all eight groups / 17 original source counters** from the certified screen;
do not pick a subset after model outcomes. These counters mix line and branch
instrumentation; they are not 17 branch points. Primary endpoint: first complete
round with every target counter hit. Keep unsuccessful trials as not reached.
Report raw hits separately from checker/transport validity and pending obligations.

B and C each receive 3 independent sessions × 6 rounds × at most 64 new physical
cycles per round, with the same eight-cycle seed. Model remains `gpt-6.1-sol`, low
reasoning, 32,000 input / 16,384 output token caps, 120-second timeout, one retry.
Normal generation calls: 36 total; at most 72 attempts including one retry per
call, plus bounded input-token accounting requests. No early termination for
target saturation, no selectively replaced trials and no uncounted drain cycles.

Both arms receive seed feedback before round 1 and whole-batch feedback thereafter.
B receives raw coverage; C receives the same raw evidence plus certified semantic
relations. Sessions are independent; arm order alternates by repetition. Every
simulation replays cumulative seed+actions in a fresh process with fresh counters;
all replayed cycles/executions count toward cost. Initial seed runs, failed calls,
compilation, preprocessing and checker failures remain separately recorded.

Secondary metrics: per-round target hits, raw line/branch/expr/toggle coverage,
API input-plus-output tokens, cycles, executions, timings, time/token cost to target,
functional failures and distinct attributed categories. Token ROI uses newly
covered raw branch points per 1,000 API input-plus-output tokens. Cached/reasoning
details are recorded without adding them twice to totals.

This first comparison has **no length-matched placebo**. It evaluates the complete
C feedback package, including its token overhead; it cannot isolate semantic
relations from prompt-length effects. A length-controlled ablation requires its
own preregistration rather than an interpretation added after results.

## Independent checker preparation and execution

The author receives only public specification summaries, pinned introductory
documentation and public pin widths/sampling/configuration. It receives no
executable RTL, old checker, target/equivalence data, private traces or model
outcomes. Authority includes the pinned WBXBAR README/introduction, the official
[Wishbone B4 specification](https://cdn.opencores.org/downloads/wbspec_b4.pdf),
and prose intent from the [author's crossbar article](https://zipcpu.com/blog/2019/07/17/crossbar.html).
Older article prose is not treated as exact-cycle implementation authority.

Downloaded PDF SHA-256:
`d712d61fe7f363b671e6b821b7b0259f43ec0b4ce8f3b2072172b2878f347a5a`.
It is cached in ignored `third_party/wishbone_b4/`; bounded paraphrases cite exact
rules/pages in the author packet. Page 37's pipeline timing/rules were also
visually checked. The first sandbox download failed DNS; the authorized download
outside that sandbox succeeded. No credential was involved in fetching the spec.

Prepared author packet:
[`spec-packet-v1`](../results/wbxbar_exploratory_bc_20261104/spec-packet-v1),
10,558 bytes; prompt SHA-256
`ba8e32e1f60f11c93ece309b1003aa4fd4ab93c3987c90b1863fc856177a176e`.
Seventeen focused tests pass, covering current proof/transport regressions and
six new isolation/admission checks. Packet edits, even rehashed extra author fields,
fail before credential access. The wrapper reuses the existing isolated transport:
no tools, no session persistence, exact Claude model, $4 CLI budget per call.

The initial Claude `claude-opus-5-5` authorship completed in 182.75 seconds and
reported $0.439711. API usage: 4 uncached input + 4,219 cache-creation input +
20,930 output = **25,153 total tokens**; 12,917 thinking tokens are a subset of
output, not extra tokens. The returned model matches the requested model.

Its ten selftests pass. Independent controls initially found ten clean positives,
44 clean observed ordinary DUT traces, and nine detections out of ten proposed
fault controls. Subsequent development controls distinguish an inactive-CYC ACK
from a stale response mixed into a new transaction. The former is ignored by the
declared checker contract; the latter is detected. A further early unexplained
mapped-address ERR exposes a possible permissive-error gap. All control versions
and raw classifications are retained; final validity/credit requires independent
review, not merely relabeling a missed control as unsupported.

## Repair, independent review and current boundary

Three versioned Claude author/reviewer pairs have completed. Original versions,
exact patches, prompts, streaming logs and failed controls are retained.

| Version | Independent finding | Outcome |
|---|---|---|
| v1 | Unexplained mapped ERR could pass; disabled SEL write bytes compared | Blocked |
| v2 | ERR and SEL fixes accepted; accepted buffered work misattributed after upstream abort | Blocked |
| v3 | Retain aborted-but-unforwarded identities, consume a unique match once, keep attribution unresolved | Limited offline readiness accepted |

The third author's packet contained only the public specification, its own prior
checker and independent synthetic controls. It contained no executable DUT,
actual DUT traces, target guards or B/C results. GPT did not edit any checker.
The fresh v3 reviewer received 46 hand traces and six selected driver traces,
losslessly packed into a 143,294-byte request with 52 verified round trips.
Its verdict is `ready_for_offline_gate=true`, **not whole-IP certification**.

The repaired checker distinguishes these cases:

- Matching accepted work forwarded after master abort: `unresolved`, never a
  successful completion and never automatically an invented DUT transaction.
- A duplicate old forward, enabled-byte corruption, unaccepted address or
  pre-reset identity reused after reset: rejected.
- Live and aborted requests with indistinguishable ownership: unresolved.
- A later reset clears old identities but does not erase earlier unresolved evidence.
- Unexplained mapped ERR stays unresolved; a slave-attributed ERR and a decode
  ERR remain distinct. Only SEL-enabled write bytes are compared.

`evaluation-v8` contains 46 independent hand controls. All 16 positives pass.
The historical ledger retains 20 proposed faults: 14 clean-baseline in-scope
faults are detected; four abort-identity mutations are rejected on unresolved
baselines and receive **no ordinary mutation-score credit**; one inactive-CYC ACK
is an exclusion demonstration; one unexplained ERR exercises an unresolved spec
boundary. There are also six unresolved, three incomplete and one invalid-input
control. See `offline-gate-v4/control-accounting.json` for the explicit categories.
This is a small hand-control set, not a general 100% defect-detection claim.

The reviewer prose contains two minor counting errors. V3 says five rather than
four unresolved-baseline negatives; its cycle narrative omits the fourth master
acceptance at cycle 12 in the actual error-burst trace. The raw evaluator/transport
ledgers remain authoritative: five total accepts in that complete case, including
the later restart, and three accepted requests aborted. The review conclusion is
supported by the exact identity controls, not by adopting those prose counts.

## Fixed driver and independently checked reachability

The separate JSON offer driver holds STB/payload until sampled acceptance. It
keeps CYC high while work is queued or pending. A sampled ERR discards accepted
outstanding work, retains unaccepted queued offers and inserts one counted
low-CYC cycle. Reset clears both kinds of work. No hidden drain is added.
Incomplete prefixes remain pending instead of becoming simulation failures.
The Python transport parser independently reconstructs driven pins and queue
accounting; it is not an expected-output checker.

Seven fixed fields: `rst:1`, `offer:2`, `addr:16`, `data:64`, `we:2`, `sel:8`,
`slave_error:2`. Widths, integer types, unknown fields, reset-with-offer and sequence
length are validated. One JSON action is exactly one physical cycle.

`driver-v1`: 48 cases, 96 dual-simulator executions, 7,212 physical cycles, matching
meaningful Verilator/Icarus traces and transport ledgers. All 2,845 original DUT
counter identities remain. Under the accepted v3 checker, 46 driver cases pass;
`pending_prefix` is unresolved due to pending work, and `error_burst_restart` is
unresolved due to the documented abort boundary. Forty-four old ordinary
observations also remain clean; these overlap the new driver case families and
must not be described as 92 independent behavioral tests.

All eight preregistered groups / 17 counters have witnesses in checker-clean,
completed cases. Witnesses are private gate evidence only and are never rendered
in model prompts. Ordinary traffic reaches these targets, so this is still the
known-easy exploratory control permitted by the user, not a newly difficult IP.

## Prompt representation and resource checks

The original uncompressed common RTL plus repeated semantic metadata exceeded
the fixed input budget in local token sizing (B 36,329 / C 47,133 content tokens
at the seed). This was caught offline, before any OpenAI call.
`configs/wbxbar_prompt_representation_v1.json` records the common representation
chosen before live outcomes:

- Verilator `-E` under the simulation macros supplies **all active compiled RTL**,
  with original source line numbers. Comments and inactive formal/alternative
  preprocessor branches are omitted equally. Original files and hashes are unchanged.
- Both arms see the last 64 generated cycles, encoded as repeat-count/vector pairs,
  with explicit total/omitted counts, and the last 16 pin-trace cycles as vectors.
  The entire cumulative history is stored and simulated; all coverage and checker
  feedback are computed on the full batch.
- Both see all 17 registered raw counters plus the same rotating page of 48
  uncovered line/branch/expression points. C adds the certified complete guards,
  equivalent groups, representatives and rewrite explanations for unhit groups.
- Repeated typed atoms are shared and given reversible short aliases. No type,
  source provenance, guard or clock/reset context is dropped. Round-trip tests
  verify this; the source mapping still counts every original location separately.

Local stress estimates with all semantic groups still uncovered are approximately
19,825 tokens for B and 28,007 for C before provider framing/schema. These are
estimates, not API usage. Every live attempt will use the provider's exact input
count and reject over-cap input without raising the budget or silently changing
feedback. The policy bounds common history identically; it does not isolate
semantic value from C's remaining extra prompt length.

An intermediate compaction attempt incorrectly treated a substring of the source
path as an atom ID. Two tests and `mock-v2` failed before any API call; the exact
20-hex atom boundary fixed it. Those artifacts are retained. Early raw replay
hash comparison also caught harmless JSON object key-order differences; the audit
now compares decoded values while retaining list order, every count and source
identity. It does not ignore numeric or trace differences.

## Costs and limitations

| Version | Author cost | Reviewer cost | Total API tokens |
|---|---:|---:|---:|
| v1 | $0.439711 | $0.441046 | 95,591 |
| v2 | $0.357916 | $0.450601 | 128,156 |
| v3 | $0.337611 | $0.433056 | 130,489 |

Six actual Claude calls total **$2.459941 / 354,236 tokens**. Anthropic totals add
uncached input, cache-creation input, cache-read input and output once. Thinking
and cache-duration subfields are not added again. All calls returned
`claude-opus-5-5`. The staged Anthropic key was deleted after each completed pair.
OpenAI stimulus calls remain zero at this preparation checkpoint.

Important exclusions: timeout/starvation timing, abort-propagation latency and
post-reset/inactive-CYC responses are not fully checked. Identical ownership can
suspend functional attribution until reset and remains unresolved. The driver
has prompt slaves and no slave backpressure. Hand controls exercise some stall
checks, but that does not make the live driver a backpressure environment.

## Reproduction and next action

Latest offline runner artifacts: `mock-v4`, `replay-v4`, and
`runner-validation-v1.json`. The final run uses the frozen config named below.
All model logs, simulator output, raw counters and failed versions are retained.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_wbxbar*.py' -v
.venv/bin/python scripts/audit_wbxbar_experiment.py --config results/wbxbar_exploratory_bc_20261104/offline-gate-v4/offline-config.json --mock results/wbxbar_exploratory_bc_20261104/mock-v4 --replay results/wbxbar_exploratory_bc_20261104/replay-v4 --output build/wbxbar-runner-audit.json
.venv/bin/python scripts/stage_midterm_openai_key.py
.venv/bin/python scripts/run_wbxbar_bc.py --mode live --config configs/wbxbar_exploratory_bc_freeze_v1.json --output results/wbxbar_exploratory_bc_20261104/live-v1
.venv/bin/python scripts/report_wbxbar_bc.py --run results/wbxbar_exploratory_bc_20261104/live-v1
```

Use fresh output directories; do not overwrite completed evidence. The live runner
removes its staged OpenAI key on exit. A network-enabled execution context is
needed for the API. Its model setting is exact; no silent substitution is allowed.
No live B/C result or C advantage is claimed at this checkpoint.
