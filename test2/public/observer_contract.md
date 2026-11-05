# Passive FIFO observer contract v1

One JSON action per clock: reset/wr/rd unsigned 1 bit, data unsigned 8 bits.
All fields are required; reset=1 requires wr=rd=0. First action resets.
Inputs settle before pre observation; rising edge then post observation.
The initial pre observation is unspecified and excluded. Every subsequent pre
and post observation is eligible, including reset cycles. Empty data is unspecified.
Each fixed sequence includes two counted idle tail cycles. No candidate adds cycles.

Reference rows have cycle, action, pre and post fields. pre/post each contains
fill (5 bits), full/empty (1 bit), data (8 bits). A value of -1 denotes X/Z.
The reference observes only public I/O. It is not allowed to read implementation
pointers, memory or a candidate monitor's output as expected behavior.

Candidate code is a SystemVerilog passive module body wrapped in a fixed module:
inputs i_clk, i_reset, i_wr, i_rd, i_data[7:0], o_fill[4:0], o_full,
o_empty, o_data[7:0]; outputs active[5:0] and ok[5:0]. It may have private,
bounded state, initial assignments and posedge i_clk processes. At each sample,
active[j]=1 means property j actually checks, and ok[j]=0 is an alarm.
The trusted wrapper records outputs without stopping simulation; it instantiates
formal immediate assertions active[j] implies ok[j] separately. Six metadata
descriptions are mandatory. No system calls, hierarchy, additional modules,
assumptions, force/release, delays, event controls besides posedge i_clk or
combinational processes, or access to files are permitted.

Candidate simulation replays immutable public-I/O observations in a separate
process, with the same input/edge timing as the DUT. It never drives the DUT.
Candidates may maintain their own expected state, but that state is a tested
hypothesis, not the independent scoring oracle. In formal evaluation the same
body observes the DUT pins under a fixed harness and fixed input assumptions.
Unknown candidate outputs, missing samples, compile failure or timeout are
unresolved/invalid, never a pass. Never activated properties are vacuous.

No upstream assertions, reference source, mutant locations or held-out data
are supplied to the experimental model. Implementation equivalences are not
specification assertions. Restating an RTL expression as its equal rewrite
does not earn detection credit without identifying an independently confirmed
specification violation.
