Verify only the existing 8-bit register interface and operations: mode 0 hold,
1 shift, 2 rotate, 3 parallel load; direction 0 right, 1 left. Serial shifts
insert serial_in, rotations wrap the outgoing bit. rst clears q. serial_out
selects q[0] for right direction and q[7] for left direction.
The CVDP task asks for new features; those are outside this fixed-DUT experiment.
Sample q and serial_out after the active clock edge settles. This experiment
does not decide the synchronous/asynchronous reset documentation discrepancy.
Binary mode_sel exhausts all four case values; the default counter stays in
the denominator. No DUT repair or new port is allowed; return stimulus only.
