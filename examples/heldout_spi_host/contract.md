# Fixed SPI controller verification contract

Upstream is lowRISC OpenTitan at the revision in `provenance.json`. The RTL is
unmodified `spi_host_fsm`, parameter `NumCS=2`. This is the command/clock/control
component, not the peripheral's register bus, command FIFO, or serial payload
datapath. The contract below is a project-authored, scoped interpretation of the
pinned upstream specification; it is not an upstream specification file.

The source authority is `hw/ip/spi_host/doc/theory_of_operation.md`: “SPI Protocol
Basics”, “SPI Clock Generation”, “Chip Select Timing”, “Clock Phase”, “FSM” and
“Stall”, together with `registers.md` definitions of COMMAND and CONFIGOPTS.
The field widths come from the upstream command package. Upstream revision and
specification/RTL hashes are recorded separately.

Each JSON action drives exactly one rising core-clock edge. Drive changes occur
while the clock is low. Reset is active-low asynchronous: when `rst_n=0`, before
the next rising edge, CS pins are high, serial clock is low and the FSM is idle.
`sw_reset=1` aborts the current operation at a rising edge. It is distinct from
asynchronous reset. Two initial reset clocks and six idle clocks are the common
seed. They are replayed for every simulation and included in raw coverage/cycles.

`valid` and `ready` accept a command. An unaccepted command must remain valid
with all command fields unchanged until a handshake or reset. A continuously
asserted valid may accept multiple commands; use only when intended. `csid` is
0 or 1. `speed` is 0/1/2 for standard/dual/quad. Bidirectional transfer is legal
only at standard speed. `length` is the count minus one: a read/write command
transfers length+1 bytes, while a dummy command (read=write=0) transfers that
many serial-clock periods. `keep_cs` requests continued selection between
segments. CPOL/CPHA select the four SPI modes. `clkdiv+1` core clocks is the
minimum serial half-period. Lead/trail/idle and full-cycle fields have their
upstream meanings. The checker currently checks the minimum serial half-period,
but not exact lead/trail/idle delay or sample phase.

`tx_ready` / `rx_ready` are the external transmit-source / receive-sink readiness.
Unavailable data or space may stall the FSM. While stalled, serial clock and
CS must hold, and command handshake, read/write, shift and sample controls are
suppressed. `enable=0` pauses progress. `last_write` and `last_read` accompany
the last byte of their segment. The fixed checker counts accepted bytes and
serial edges using only public signals; it does not read DUT state or counters.

The JSON object contains only `actions`; every action must supply every field
in `stimulus.schema.json`. No user code, delays, repeats or checker edits are
accepted. The model can change reset/readiness/enable and command fields only.
No implicit drain is inserted. Incomplete transfers at the batch limit are
reported as incomplete, not as a complete correctness proof or a DUT failure.

For this initial scoreboard scope, retire/deselect a different CSID's burst
before offering a new CSID. For same-CS chained segments, keep configuration
fields unchanged until deselection. The full IP supports additional switching
behaviors, but overlapping CSID/configuration changes are not validated here.
Input/scope violations are reported separately from DUT defects and disqualify
a development repetition. Exact serial payload, all sample/shift timing,
long-term liveness and full formal correctness are outside this checker.

Calibration sequences and negative controls are independent validation evidence;
they must never appear in model prompts. Passing those finite tests does not
establish complete checker correctness. The full raw DUT coverage denominator
also includes counters outside this checker scope; none are removed as
unreachable without proof.
