# Next test2 pilot: bounded I2C READB

**Offline task draft, not a live registration or execution approval.** This is
the next protocol IP after the existing FIFO/controller studies. No new I2C
monitor, hidden set, DUT mutant or model result exists in this task yet.

**DUT and available assets.** Original OpenTitan i2c_controller_fsm at revision
0ea5236fe749e70ba18f56ba19c4be982ef46da7, FifoDepth64. Existing public specification,
READB fixed driver, two-simulator calibration observations, Claude-authored finite
checker and verified guard assets are indexed in asset-index.json. Historical
stimulus-screen rejection stays unchanged; it does not automatically prohibit
this separately registered fixed-stimulus monitor task.

**Limited reference scope.** One ACKing target, READB byte/count/order, command
ordering and wire ACK/NACK under the existing contract. Push/flush occurs before
same-row pre. Deferred pop/RX ordering and the fixture-specific RX-before-pop
condition must remain explicit. Invalid assumptions and incomplete transactions
remain invalid/pending. No new liveness deadline, stretch/recovery, extra-STOP
fault attribution, multi-controller or256-byte completion credit. GPT does not
edit the Claude oracle. First online step is an independent scope review; an
oracle change requires a separate Claude author and fresh reviewer.

**Public ABI draft.** public-abi-mapping.json maps all32 legacy observation fields
to existing DUT outputs/environment signals, with widths and pre/post phases.
Inputs include16 action fields. Per old TB loop, action/push/flush precedes
pre at+2ns, DUT posedge+3ns and post+4ns, next row+5ns. A passive replay sample
clock/phase may transport these observations without changing DUT clocks.
The new SV adapter is **not implemented or compiled**. Before use, check actual
first-row/reset/phase consistency and positive/negative/unknown controls. Preserve
unknown bits or explicit known masks; never map unknown or missing data to0.

**Minimal fair comparison proposal.** B receives public spec/clean RTL, fixed
development observations/raw counters and own-session feedback. C adds only
relevant already-validated typed complete guard relations. Same DUT, reference,
stimuli, model/settings, caps, round schedule and selection rule. Proposed small
pilot:2 independent sessions per arm ×3 rounds =12 normal generation calls,
at most24 attempts/counts with one failed-call retry. This is an unapproved
draft; model access, rates, counts and worst-case dollar reserve must be reviewed
tomorrow before dispatch. No token-matched placebo: claim scope is the whole
feedback package. Freeze every round before hidden scoring.

**Still needed before candidate calls.** New disjoint development/hidden input
sets and raw observations; relevant C appendix; independent physically observable
single-point DUT mutants; reference labels; exact prompt allowlists and budgets.
Old calibration traces are not a new hidden set. Old trace-corruption controls
are not RTL defects. Retain all raw types/pairs, false alarms, invalid, unknown
and not-reached outcomes. Count actual tokens, compile, physical runs/cycles,
monitor replay and wall cost separately. DUT coverage is fixed-input background.

**Tonight:** task card, mapping, role lists and scope-review checklist only.
No API/count/Claude/key/network or real SV tools. Full generic G1 qualification
is not a prerequisite for this finite simulation study; its actual adopted
driver/reference path still needs the small checks listed above.
