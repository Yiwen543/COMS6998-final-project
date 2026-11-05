# SPI host core specification checker contract

**Scope:** OpenTitan spi_host_core, NumCS=2, observed only through public core pins in the supplied rows. Each row is one clock. Pin changes are processed chronologically and each is counted once: previous post -> current pre (time c-0.5), then current pre -> post (time c, the rising edge). Within one transition the order is CSB falls, then SCK edge, then CSB rises.

**Transport.** These are driver assumptions, not DUT defects.
- Command, TX and RX handshakes use pre values only at the rising edge: `pre.ready&valid`, `pre.tx_ready&tx_valid`, `pre.rx_valid&rx_ready`.
- If an offered command or TX word is withdrawn or changed before it is accepted, that is an assumption violation.

**Supported segments.**
- Standard TX, RX and bidirectional segments.
- Dual and Quad TX-only or RX-only segments.
- Any CPOL, CPHA, FULLCYC, CLKDIV, CSNLEAD, CSNTRAIL or CSNIDLE value, and CSID 0 or 1.

**Blocking unsupported.** The following are recorded as assumption violations, and serial checking stops until the next reset:
- dummy segments, because the dummy-cycle semantics are absent from the supplied excerpts;
- speed 3;
- Dual or Quad bidirectional segments.

**Payload.**
- **TX:** expected bytes are the enabled bytes of accepted words, most-significant first. A partial word is flushed at segment end. The DUT value is sampled on the device sampling edge from the pre-edge pin value.
- **RX:** expected bits come from `action.sd` (SD[1] in Standard mode) at the host sampling edge. With FULLCYC=1 the sample is taken CLKDIV+1 clocks later. A bit is judged only if `action.sd` is stable across the sample window; otherwise it is reported as unresolved.
- **RX words:** bytes are packed most-significant first, with zero padding in the low bytes. Words must be delivered in order and never before their last byte has been sampled.
- **Lane order assumption:** in Dual and Quad modes, the higher-numbered SD line is assumed to carry the more significant bit.

**Timing.** Only minimum bounds are checked:
- lead, trail and idle: (N+1)*(CLKDIV+1) clocks;
- SCK half period: at least CLKDIV+1 clocks.

No exact-cycle deadlines are imposed. The trace may end while waiting for a CSB rise or an RX word, which leaves the result inconclusive.

**Chip select.**
- Exactly the commanded line must be low during SCK edges, and both lines must never be low.
- No deassertion is allowed mid-segment.
- After CSAAT=1, CSB stays low unless the next accepted segment changes CSID or configuration.

**Resets.**
- **Hardware reset:** CSB must be idle and all state is cleared.
- **Software reset:** the driver must observe ACTIVE=0 and idle CSB before releasing it. All state is cleared. Behaviour during a stall beyond the documented procedure is listed in `unresolved`, not asserted. Stale data after release counts as a failure.

**Verdicts.**
- `fail`: any failure.
- `blocked`: any assumption violation (and no failures).
- `inconclusive`: unresolved items, or a non-passing event.
- `pass`: none of the above.

Incomplete segments or batches are never reported as pass. Events report trigger, resolution and completion windows. A window passes only if it contains no failures or assumption violations and the full segment completes. A stall flag, ready, ACTIVE=0 or an accepted command alone is never treated as completion.

Event results are not coverage or equivalence evidence. The self-tests are minimal single-fault controls, not validation of this checker.
