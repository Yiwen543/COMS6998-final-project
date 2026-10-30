# Fixed FIFO verification contract

Source: ZipCPU `wb2axip/rtl/sfifo.v`, commit
`2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`, SHA-256
`76a653781f1ecca1c1da92c4e5105ecd5d0f832b13cbfd31300ec88d9947e0c1`.
The original file is copied without modification. It is marked public domain
in its header. This contract is a separately written abstract FIFO interface,
not an oracle derived from internal RTL pointers or assignments.

Fixed parameters: data width 8, depth 8 (`LGFLEN=3`), asynchronous front-data
read, `OPT_WRITE_ON_FULL=0`, `OPT_READ_ON_EMPTY=0`. `i_reset` is active-high
and synchronous. Each action sets `reset`, `wr`, `rd`, `data` before the next
rising edge. The first action resets; read/write are excluded while reset is
asserted. The expected queue is initially empty and reset empties it. Storage
contents while empty are unspecified.

`o_fill` is queue occupancy 0..8, `o_full` is true exactly at 8, and
`o_empty` is true exactly at 0. While nonempty, `o_data` is the front word
both before and after each edge. It is not checked while empty.

On an active edge without reset, a read consumes the front word if the queue
was nonempty before the edge. A write appends `i_data` if the queue was not
full before the edge. The two accepted operations may occur together and
preserve occupancy. At full, simultaneous read/write accepts the read only;
at empty it accepts the write only. Full/empty are recomputed from the new
occupancy after the edge. This pre-edge acceptance policy follows the fixed
interface configuration and is not a property of a particular implementation.

Coverage is Verilator's original DUT-only line, branch/expression, and toggle
counters; identical guard expressions at different source locations retain
separate counters. E-graph normalization is two-state combinational reasoning
only, under the original clock/reset/activation guards. It does not assert
four-state, sequential, or full-module equivalence.
