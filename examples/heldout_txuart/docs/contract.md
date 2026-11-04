# Candidate TX UART contract (fixed 8N1 configuration)

Source: ZipCPU `wbuart32` `doc/spec.pdf`, chapter 2 and setup-register section,
plus the upstream `txuart.v` interface comment. The pinned source and document
hashes are in `../provenance.json`. The original RTL is external and unchanged.

The independent pilot fixes `INITIAL_SETUP = i_setup = 31'h40000002`: 8 data
bits, no parity, one stop bit, hardware flow control disabled, two system clocks
per baud. This is a deliberately small timing parameter, not a new protocol.
The source's active-high `i_reset` is synchronous. While `i_break` is asserted,
the serial line is low; reset takes precedence. After the transmitter becomes
ready (`o_busy = 0`), a rising-edge request with `i_wr = 1` is accepted and
emits one UART frame: low start, eight data bits least significant bit first,
then high stop. Each bit lasts two system clocks. A request while busy may be
ignored and is not scored as an accepted byte. Reset or break can abort an
incomplete frame; subsequent completed frames remain checked.

The checker uses only public inputs, `o_busy`, and `o_uart_tx`. It decodes the
serial line at bit centers and compares complete frames against accepted input
bytes. It checks reset output and sustained break low. It does not infer
expected state, counters, or bit values from DUT internal registers. The
upstream testbench and formal assertions are not used as model feedback or as
the checker implementation. The contract does not score parity, variable baud,
CTS, or the exact startup busy latency; those features remain outside this
fixed pilot. A passing checker is evidence for these declared properties only.
