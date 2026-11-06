# G1 R05 conditional parser preparation

Status: **BLOCKED pending P15, exact reuse acceptance and new budget authority**.
This directory has no real execution entrypoint, pool, lock or EXECUTE receipt.
The draft registration and job plan must not be used to start tools.

`native_evidence.py` reads one hash-bound public posedge wrapper with exactly
`assert(!active || ok)` and `cover(active)`. Its independent fields are:

| Field | Meaning |
| --- | --- |
| tool_status | Raw PASSED / FAILED / UNKNOWN; never rewritten from activation |
| process_exit_code | Actual receipt exit, including nonzero failures |
| activation | REACHED / UNREACHED / UNKNOWN, explicit source-bound tool lines |
| assertion_observation | FAILED / NO_FAILURE_REPORTED / UNKNOWN; never a proof |
| evidence_complete | Exact source/log/receipt/argv/trace support for this reading |
| qualification_credit | Always false; independent qualification is separate |

Reached requires a matching single-cover source ID, exact trace/log path and
registered sampled_active=1 at the reported SMT step. Missing/contradictory
records remain UNKNOWN. Explicit UNREACHED is the tool's finite-invocation report,
not unbounded unreachability or 128-cycle completion. Unsupported formats/wrappers
are UNKNOWN. This parser does not execute Yosys, a solver or simulator.

Saved E02 QC00: tool PASSED/exit0,activation REACHED,no assertion failure reported.
Saved E03 QC01: tool FAILED/exit1,activation REACHED,assertion FAILED. The old v4
NOT_REACHED label and all old evidence remain untouched. Thirteen new pure cases
cover those two real saved logs,ten synthetic unknown/refusal cases and one
synthetic explicit-unreached format control. Synthetic records are not real QC
outcomes, physical tests or RTL coverage. One initial missing-parent launch error
is retained in the R05 audit;the final suite uses preparation-attempt2.

All18 SV files,three input/label tables and the physical parser are identical to
v4. Job flags/order are unchanged apart from new source/output namespace and
explicit references to the old physical executables. No oracle or label edited.
`conditional-reuse.json` binds saved E02 prefix and E03 artifacts;this is a
proposal,not accepted qualification or a new independent trial.

If P15 accepts that exact reuse,remaining work is0setup/14compile/28native/
30physical/120cycles,projected cumulative8/20/32/33/132. Proposed prior charge15s
and current1185s need a new actual authority;they are not measured spend or a
budget reset. If reuse is invalid,stop and calculate extra costs. No silent
rebuild/retry. Old native cover PASS expectation remains in the original labels;
a new activation-only interpretation must be explicitly reviewed rather than
silently replacing tool FAILED with PASS.

Remaining before execution: P15 saved-evidence verdict,final interpretation/reuse
acceptance,new exact cumulative authority,then minimal runner/report integration
and independent preflight binding its final hashes. Raw/B/C,cross-IP,model APIs,
keys,paid calls,installation,commit and push remain outside this preparation.
