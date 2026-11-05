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

**Limitations:**
- Exact arbitration, pipeline and timeout latencies are not checked. A master ERR on a mapped request with no matching slave ERR is recorded as unresolved (unexplained_mapped_err, with accept/ERR cycles); it is never scoped_pass and is not labeled timeout/starvation. It persists across later reset/restart in the same batch.
- Responses while master CYC is low are ignored (not attributable per WB B4 3.1.2); stale responses landing on new work are checked.
- Not checked: o_mack/o_merr inactive after reset, minimum reset duration, eventual o_scyc withdrawal after abort/timeout (liveness).
- Identical concurrent requests from both masters make ownership ambiguous. Functional checks are then suspended until reset and reported as unresolved.
- Pending work at trace end yields unresolved.
- Events are descriptive and are dropped if any failure falls in their window.
- The per-master forwarding order assumption is derived from the no-crossed-ACK claim.
- The selftests are minimal and are not certification.

