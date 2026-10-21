# Experimental contract for the CVDP `sync_fifo` context module

This contract is authored for this verification pilot. The CVDP record
`cvdp_agentic_low_power_channel_0001` supplies the RTL as context for a
low-power channel task, but does not supply a standalone FIFO specification.
The contract below follows the public module interface and conventional
lossless FIFO behavior; it is **not** presented as a verbatim CVDP spec.

The experiment fixes `DEPTH=8` and `DATA_W=8`. A rising `reset` asynchronously
discards queued entries and sets `empty_o=1`, `full_o=0`. Stored memory data
need not be cleared. During reset, `push_i=pop_i=0`. With reset low, each rising
clock edge accepts a push and/or pop. `pop_data_o` is the oldest queued byte
before that edge when nonempty. A push appends `push_data_i`; a pop removes the
oldest byte. With both asserted, the old head is popped and the new byte is
appended, so occupancy is unchanged. Simultaneous push/pop is allowed while
full, but not while empty. `empty_o` means occupancy zero; `full_o` means
occupancy eight. The interface does not promise defined `pop_data_o` while
empty. The caller must not pop while empty or push while full unless an
existing item is popped on that same edge. Overflow and underflow are outside
the module contract; the channel controller is responsible for excluding them.

The fixed checker compares status and valid head data against an independent
queue model before each active edge, then checks status and the next head after
the edge. It also checks asynchronous reset assertion between clock edges.
The fixed driver applies validated cycle actions at falling edges. Functional
bins cover empty, data read, full, simultaneous operations, pointer wrap on
push/pop, reset during occupancy, full backpressure, and drain to empty.
