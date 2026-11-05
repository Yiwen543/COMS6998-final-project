# Byte-stream length adjustment controller: fixed project contract v1

This task uses the unmodified MIT-licensed verilog-axis length-adjustment core
at revision 48ff7a7e2ef782cf778d47910cf85835c64b1bce. It is a newly scoped
monitor task on a previously inspected IP family, not an unseen repository or
an official benchmark. The upstream README describes padding/truncation and
original/current length reports; the timing and finite-trace rules below are
the explicit project contract, not a claim of verbatim upstream prose.

The selected wrapper is task_top_v3.sv. Data width is 8 bits, KEEP is disabled
(each accepted input is exactly one byte), ID/DEST/USER are disabled. Length
limits are constant MIN=4 and MAX=8 bytes. Input frames contain 1..12 bytes.
There is one positive-edge clock and synchronous active-high reset. Reset is
the only cancellation mechanism in this scope; there is no independent cancel pin.

A transfer occurs at a rising edge iff valid and ready are both 1 before that
edge and rst=0. Input s_last marks the final byte of an input frame. The source
holds s_valid, s_data and s_last while blocked, except that reset cancels it.
Input gaps, back-to-back frames and independent data/status backpressure are
legal. Source validity during reset is 0. The sink need not keep ready asserted.

For each accepted input frame X of length L, the expected output frame is:

- L<4: all input bytes, then zero bytes until length 4;
- 4<=L<=8: the input bytes unchanged;
- L>8: the first 8 bytes; the remaining input bytes are still accepted/drained.

Exactly one accepted output beat has m_last=1 per completed output frame, on
its final byte. Frames and bytes retain input order. No output may depend on
an unaccepted input byte. Output may stream before input s_last is accepted;
the checker must support partial known prefixes rather than requiring the
whole input frame to arrive first. Padding is known only after input completion.
For truncation the output end may wait for the rest of the input frame.

Each completed, uncancelled input frame has exactly one status response:
h_original_length=L, h_length=min(max(L,4),8), h_pad=(L<4), h_truncate=(L>8).
Statuses preserve input-frame order. Data and status responses are independent
channels; no required order is imposed between the two channels' completion.
A status cannot describe an input frame before that input frame completes.

If m_valid=1 and m_ready=0, m_valid/data/last remain stable until transfer or
reset. If h_valid=1 and h_ready=0, h_valid and all status fields remain stable
until transfer or reset. Payload fields when their valid is 0 are unspecified.
s_ready is flow control, not an independently prescribed cycle-by-cycle value.

Reset cancels in-progress input and all not-yet-consumed data/status responses.
After the reset edge m_valid=h_valid=0. Already consumed output prefixes are
not retroactively failures: reset discards the remaining epoch. No pre-reset
obligation may be carried into the next epoch. A reset edge performs no transfer.
Pre-edge observations while rst=1 may still show pre-reset values.

This is a two-state task. Saved -1 observations denote X/Z and are unresolved
when meaningful, never successful checks. The initial pre sample is excluded.
At every subsequent pre/post sample, valid fields and enabled payloads are checked.
Unknowns must not erase an earlier definite violation.

Finite evaluation traces declare require_drained=true and end in an uninterrupted
ready-high, reset-low, no-new-offer tail of at least 32 cycles (development) or
128 cycles (final). For the fixed bounded offered workload, all offered bytes
must be accepted and all uncancelled responses consumed by the end. Remaining
s_valid/m_valid/h_valid, an incomplete accepted input frame or remaining expected
responses is a finite completion failure, not permission to infer an unbounded
liveness guarantee. Partial unit controls may use require_drained=false.
