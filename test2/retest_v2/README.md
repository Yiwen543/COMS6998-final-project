# R02: zero remote count, same benchmark B/C retest

This version adapts sealed R01 to the explicitly confirmed zero remote count
method. It is **prepared, pending exact independent code precheck and EXECUTE**.
It does not start automatically. The current staged credential is retained; this
preparation has neither read nor hashed its contents or made an API request.

B receives the unchanged public packet and raw source coverage feedback. C adds
the old verified E-graph feedback. Each has one independent session and three
rounds, interleaved B1,C1,C2,B2,B3,C3. This reuses a published benchmark, not a new
hidden set. A session sees only its own preceding candidate and development
feedback. All six snapshots freeze before the shared v4 grader sees them; each
arm's final is its last compile-valid round. The independent Claude checker,
fixed DUT stimuli, monitor ABI, old labels and raw12/N10/38unknown remain unchanged.

`api.py` builds the whole JSON request, including system text and output schema.
Admission uses `ceil(UTF8bytes/2.5)+4096 <= 64000`, explicitly an ESTIMATE rather
than an exact tokenizer count or server input cap. Actual reported input above
64000 is retained with its costs and halts the stage as not qualified. No packet
is trimmed to make C fit. Remote counting calls are zero; counting is not assumed
free. The stdlib HTTPS transport uses the fixed official Responses endpoint,
existing `/etc/ssl/cert.pem`, certificate/hostname verification, one POST and no
redirects, SDK or automatic retry. Failed HTTP bodies are not logged.

Before every generation, the persistent ledger reserves 5,910,168 microUSD using
the reviewed full-context financial bound. A complete trusted qualified response
may settle to `ceil(5.5*input_tokens + 16.5*output_tokens)` microUSD, releasing only
the unused reservation. This is neither a refund nor a provider invoice. Missing,
invalid, incomplete, failed or over-target responses retain the entire reserve
and halt; another probe is not sent. Cached/reasoning tokens are optional subsets,
not additional token totals. A new dispatch requires commitments plus its full
reserve to fit within 20,000,000 microUSD. Twelve generation attempts is an upper
cap, not a promise to continue after a fatal failure.

The inherited owned-process-group supervisor, deadline and release code retain
R01 behavior. One future live pass has at most 12 compile roots, 990 monitor
replays, 204444 replay cycles, zero new DUT/native/setup jobs and a total 3600s
window including cleanup. This is not a hard realtime or detached-child census
proof. Real transport, process lifecycle and SV compilation were not exercised
in R02 preparation.

Targeted R02 checks: `python3 -B test2/retest_v2/targeted_tests.py --record <new path>`.
The initial saved attempt has 18 PASS; it uses fake HTTPS and a narrow six-round
stub, not a fresh complete mock/independent scientific score. A later one-check
delta verifies provider JSON retention on a malformed nested response (1 PASS).
That extraction changes only api.py and the test harness after the 18-check run;
the completed 18 were not rerun and this is not one final-source 19-test suite.
R01's historical full
mock/replay evidence is referenced separately and was not rerun. A later evidence
inspection should read the saved checks rather than repeat them for context.

Live, only after the exact independent review and root EXECUTE:
`python3 -B test2/retest_v2/cli.py --mode live --output test2/results/controller-done-bc-retest-v2 --execute <exact receipt>`.
Do not use that command as permission to run. The receipt must bind the new
registration, source/preparation manifests, reviewed financial records, explicit
user method confirmation and exact precheck. R01 remains sealed and unexecuted.
