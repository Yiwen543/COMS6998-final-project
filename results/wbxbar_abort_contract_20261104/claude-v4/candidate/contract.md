# WBXBAR spec checker contract

**Scope:** public pins of wbxbar rev 2e8d3bc2, NM=2, NS=2, AW=8, DW=32, with the packet's decode. Only pre-edge values define transfers; post values are used only for post-reset output checks. Reset is synchronous. The trace must start with reset and have contiguous cycles.

**Checked:**
- routing
- payload and SEL preservation (write data compared only on SEL-enabled byte lanes; address, WE, SEL compared fully)
- per-master in-order retirement
- ACK only after the matching slave ACK
- read-data equality with slave-returned data
- decode ERR for unmapped addresses
- slave ERR propagation
- abort/reset/CYC-drop epoch separation
- stalled-request hold and basic handshake legality

**Environment violations:** these are reported separately and yield input_or_scope_invalid. They include:
- master hold or STB-without-CYC
- unsolicited slave responses
- undefined active payload
- CYC/STB high during reset

**Normative scope (resolved):**
- Authoritative (WB B4): synchronous reset and CYC/STB negation (3.1.1, rules 3.00/3.20); CYC qualifies activity, slaves ignore signals without CYC (3.1.2, rules 3.25/3.30); pipelined acceptance = CYC&STB&!STALL, WE selects direction (rules 3.57/3.58); ACK any time after initiation, read data valid with ACK (rule 3.59, 3.1.3.2, obs 3.10); ACK/ERR exclusive (rule 3.45); payload qualified by STB (rule 3.60); master reaction to ERR unspecified (perm 3.20).
- Declared environment assumptions (packet environment_contract): master hold through stall, in-order non-unsolicited slaves, slave work canceled by CYC withdrawal/reset.
- Inferred: decode ERR and per-master non-crossed ordering of live work (README 188-196, crossbar article); no attribution of completions across abort/reset epochs (article, supplementary).
- Unknown: pipeline/cancellation latency, which buffered requests survive a partial cancellation, order of residual forwards, timeout/starvation edge counts.

**Cancellation attribution:** after CYC withdrawal, a downstream request matching any unconsumed aborted request of that master (full identity, enabled-lane data) is unresolved post_abort_forward with accept/abort/forward cycles. The old 'oldest aborted entry only' rule had no normative basis and is withdrawn. Each aborted entry may explain one forward (multiplicity checked). Unmatched forwards remain violations; aborted work never forwarded is legal; canceled work is never counted as completion. Reset clears identities but not cumulative unresolved records. Live traffic ordering, payload, response and read-data checks are unchanged.

**Limitations:**
- Exact arbitration, pipeline and timeout latencies are not checked. A master ERR on a mapped request with no matching slave ERR is recorded as unresolved (unexplained_mapped_err, with accept/ERR cycles); it is never scoped_pass and is not labeled timeout/starvation. It persists across later reset/restart in the same batch.
- Responses while master CYC is low are ignored (not attributable per WB B4 3.1.2); stale responses landing on new work are checked.
- Not checked: o_mack/o_merr inactive after reset, minimum reset duration, eventual o_scyc withdrawal after abort/timeout (liveness).
- Identical concurrent requests from both masters make ownership ambiguous. Functional checks are then suspended until reset and reported as unresolved.
- Pending work at trace end yields unresolved.
- Events are descriptive and are dropped if any failure falls in their window.
- The per-master forwarding order assumption is derived from the no-crossed-ACK claim.
- The selftests are minimal and are not certification.



