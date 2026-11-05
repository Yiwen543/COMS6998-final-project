# Depth-16 synchronous FIFO functional specification

Parameters: `BW=8`, `LGFLEN=4`, depth 16, asynchronous front read,
`OPT_WRITE_ON_FULL=0`, `OPT_READ_ON_EMPTY=0`. Reset is active-high and
synchronous. Each JSON action has exactly `reset`, `wr`, `rd` and 8-bit `data`;
it is applied before the next rising edge. The first action resets. Reads and
writes during reset are outside the fixed contract.

The independently expected queue is empty after reset. Before and after
every edge, `o_fill` equals the number of queued words, `o_full` means 16
words, and `o_empty` means zero words. If nonempty, `o_data` equals the oldest
queued word. Empty `o_data` is unspecified. A read is accepted when the
pre-edge queue is nonempty; a write is accepted when it is not full. During
simultaneous read/write, both may be accepted. At full, only the read is
accepted; at empty, only the write is accepted. Accepted operations update
the queue at the rising edge. This contract uses only public I/O, never DUT
pointer or memory implementation state.

The expected queue behavior includes reset during operation, data order,
full and empty, simultaneous read/write, and continued operation after any
number of accepted transfers.
