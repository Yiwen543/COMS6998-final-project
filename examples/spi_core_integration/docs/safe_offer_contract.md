# Protocol-safe offer interface v1

Each actions item consumes exactly one physical clock cycle. `cmd_offer` and
`tx_offer` are enqueue pulses, NOT DUT valid signals. A 1 in two successive
actions means two separate requests, even when their payloads are identical.
All fields remain required unsigned integers. All hardware meanings and widths
come from the same pinned SPI core contract; only delivery is adapted.

Command payload: csid, speed, write, read, length, keep_cs, clkdiv, idle, lead,
trail, full_cycle, cpha, cpol. TX payload: tx_data, tx_be. A payload is captured
only when its offer is 1. Changing unused fields never changes a waiting or
idle DUT payload. Do not repeat an offer merely to keep it valid.

The driver has two separate first-in-first-out queues, capacity 392 each.
At clock low it enqueues at most one new command and one new TX word. It drives
each nonempty queue's head and valid=1 throughout the cycle. That head is
removed exactly once if valid AND ready was true before the rising edge.
There is no lookahead, transfer on post-edge ready, reordering, duplication or
coverage-directed choice. The next head is driven on the next cycle. Empty
queues drive valid=0 and hold the last presented payload.

`rx_ready` and `sd` still directly control pins each cycle, even while command
or TX delivery is pending. The driver does not invent device receive data,
fill the TX FIFO, drain RX, choose modes, or generate missing commands.

`rst_n=0` asynchronously resets the original DUT and cancels all offers still
in the driver queues. It zeros the visible payloads, records cancellations,
and forbids simultaneous offers. Accepted transactions are not reclassified
as cancelled by the driver. Their reset disposition remains the independent
specification checker's responsibility. The seed remains two asserted-reset
and six inactive, disabled cycles. After the seed, enable=1 and sw_reset=0.
Dummy commands, reserved speed 3 and Dual/Quad bidirectional are excluded.

No hidden cycles: waiting for ready consumes actions just like any other cycle.
If you need time to finish a transfer, include no-offer actions with suitable
rx_ready/sd. EOF stops immediately after the last requested cycle; there is
no automatic drain. Outstanding offers remain pending, not successful. Next
round the entire seed and cumulative request list is replayed from reset, so
pending work is reconstructed at the same point before new cycles begin.
Return between 1 and 64 actions per round; the six-round budget is unchanged.

Each offer ID is its absolute cycle index including the seed. Feedback records
pending counts and accepted/cancelled totals separately per channel, alongside
actual pin traces. Conservation is: offered = accepted + reset_cancelled + pending.
All experimental arms receive the same transport information and driver.

The unchanged Claude checker sees only ACTUAL pins, not the requested offers.
Its raw verdict is retained. If delivery is pending, overall completion is
false even if checks on the observed part pass. No driver outcome overrides a
checker failure or unresolved result. Coverage remains original DUT counters,
including initialization/reset/settling, never producer-queue coverage.
