# spi_host_fsm command/clock/select boundary contract (scoped, NumCS=2)

## Observation model
- One row per core clock. `pre` is settled before the rising edge; `post` after it with the same inputs. Only `pre` handshakes (wr, rd, ready, stall flags) count operations at that edge.
- Acceptance: `valid=1` and `pre.ready=1` on a row with `rst_n=1`, `sw_reset=0`.
- SCK edge at a row: `pre.sck != post.sck`. Select rise/fall: per-bit change of csb from pre to post.

## Input assumptions (violations reported separately)
Two initial reset cycles; listed field widths; no valid while rst_n=0; pending valid and command fields held until acceptance or reset; speed 3 reserved; bidirectional only at standard speed.

## Enforced properties
- Byte accounting: LEN+1 wr pulses for write/bidir, LEN+1 rd pulses for read/bidir, in acceptance order; no unexpected pulses (registers.md COMMAND.LEN/DIRECTION).
- last_write/last_read asserted exactly on the final byte handshake of a segment.
- Asynchronous reset: all selects inactive and no handshakes in reset rows. Software reset: all inactive / no handshakes from second held cycle. Any handshake after reset and before a new acceptance is a stale byte.
- Stall safety: during tx_stall/rx_stall no handshakes, no SCK edges, csb unchanged (theory_of_operation 579-585, 1208-1223).
- Exclusive select; active select must target an open accepted command's CSID.
- CSAAT hold: completed CSAAT segment keeps its select until a later command or reset.
- Constrained switch: after a CSAAT segment, a changed CSID/CONFIGOPTS command (may be queued while the old segment is active) must cause old-select release, an all-inactive gap, then the new select; timing lower bounds use old CSNTRAIL, new CSNIDLE (max(old,new) if configuration changed) and new CSNLEAD in units of CLKDIV+1 core cycles with no tolerance; trail/lead edges attributed by CSID bit; a config-change gap in [max, old+new) is blocking unresolved.
- No idle SCK edge away from the accepted CPOL level.
- Accept and first wr/rd on the same edge are legal (command enqueued first). Switch tracking starts at the pending changed offer; old select may release before acceptance. Timing bounds have no tolerance; config-change gap below old+new idle is blocking unresolved.
- Release of a selected segment with bytes outstanding fails; wr/rd while tx_ready/rx_ready=0 fails. Completion requires (LEN+1)*16/lanes SCK edges.

## Events (counted only when fully witnessed, with no failures in their window)
- backpressure_then_recovery (tx/rx), abort_then_restart (sw_reset / async_reset kinds separate), constrained_transaction_switch (csid/config kinds).
- Completion requires all bytes accounted plus later select release or later-segment handshake plus at least (LEN+1)*8/lanes SCK edges; ready/active are never used.

## Limitations
- No payload, SD line, FIFO, register bus or STATUS checks; STATUS may differ from this boundary.
- Exact SCK edges per byte, CPHA/FULLCYC phase, sample/shift/sd_en/speed outputs unchecked.
- Dummy segments are not completion-tracked.
- CSN timing outside switches not checked; additive idle reading not enforced.
- Software reset coincident with a stall suspends the scoreboard (verdict unresolved).
- Unfinished operations at trace end are pending, never liveness failures; no latency bounds.
- enable semantics unspecified here.
- LEN documentation mismatch (8 vs 20 bits); 20 bits used.
- A scoped_pass is not a proof of full correctness.
- Events require a violation-free inclusive [start,end] window.
- active output, last flags without handshake and single-cycle sw_reset pulses are out of scope; edges-per-byte (16/lanes) is an uncited modelling assumption.
