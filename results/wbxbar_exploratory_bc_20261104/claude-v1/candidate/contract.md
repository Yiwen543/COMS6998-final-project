# WBXBAR spec checker contract

**Scope:** public pins of wbxbar rev 2e8d3bc2, NM=2, NS=2, AW=8, DW=32, with the packet's decode. Only pre-edge values define transfers; post values are used only for post-reset output checks. Reset is synchronous. The trace must start with reset and have contiguous cycles.

**Checked:**
- routing
- payload and SEL preservation (write data only)
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
- Exact arbitration, pipeline and timeout latencies are not checked. Timeout/starvation ERR is accepted for any request that has no slave ACK.
- Responses while master CYC is low are ignored.
- Identical concurrent requests from both masters make ownership ambiguous. Functional checks are then suspended until reset and reported as unresolved.
- Pending work at trace end yields unresolved.
- Events are descriptive and are dropped if any failure falls in their window.
- The per-master forwarding order assumption is derived from the no-crossed-ACK claim.
- The selftests are minimal and are not certification.
