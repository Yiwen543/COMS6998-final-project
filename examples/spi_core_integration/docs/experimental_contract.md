# Fixed SPI core stimulus interface

Scope: original OpenTitan `spi_host_core`, revision
`0ea5236fe749e70ba18f56ba19c4be982ef46da7`, NumCS=2, including its
byte select/merge, shift register, FSM and two packer FIFO instances.
The external register interface and external data FIFOs are outside this scope.
The public theory of operation and programmer guide at this revision supply
the specification. This document maps their commands to the fixed public pins.

Every JSON action lasts one 10 ns clock cycle. Inputs change with clock low;
outputs are recorded before the rising edge and after settling. Each full
cumulative batch is replayed from the same eight-cycle reset/idle seed. There
are no implicit idle/drain cycles. Return 1 to 64 new actions. All fields are
unsigned integers with the exact widths in the provided schema.

* `rst_n`: asynchronous active-low hardware reset. During reset, `valid` and
  `tx_valid` must be zero. Reset clears the transaction and pending data.
* `enable`: this limited experiment keeps it 1 after the common seed.
  `sw_reset` remains 0: software-reset completion is not qualified here.
* `valid`, `csid`, `speed`, `write`, `read`, `length`, `keep_cs`, `clkdiv`,
  `idle`, `lead`, `trail`, `full_cycle`, `cpha`, `cpol`: command channel.
  A command is accepted on `valid && pre.ready`. Hold all command fields
  and valid stable until acceptance. Do not withdraw a pending command.
* `speed` 0/1/2 selects Standard/Dual/Quad. Standard allows TX, RX or both;
  Dual/Quad permit one direction. This experiment excludes dummy commands
  (`read=write=0` when valid). `length+1` is the number of bytes.
* `keep_cs` is CSAAT: retain the chip select after the segment. A following
  segment with changed CSID or configuration closes the old selection,
  observes idle time and starts with the new configuration. With CSAAT=0,
  finish with chip select deasserted. CSID is 0 or 1.
* `clkdiv+1` is a half SCK period in core clocks; idle, lead and trail
  minima are `(field+1)*(clkdiv+1)`. CPOL is idle SCK level; CPHA selects
  capture on leading (0) or trailing (1) edges. FULLCYC delays host capture
  by one half SCK period. All chip selects high permits CPOL idle setup.
* `tx_data[31:0]`, `tx_be[3:0]`, `tx_valid`: data accepted when
  `tx_valid && pre.tx_ready`. Hold word and byte enables stable while
  waiting for acceptance. The enabled bytes are consumed in increasing
  lane order 0,1,2,3. Unused bytes of a partial final word are discarded
  at segment end. A word with no enabled bytes contributes no payload.
* `rx_ready`: consume a word on `pre.rx_valid && rx_ready`.
  RX words pack successive bytes into lanes 0,1,2,3. A short last word
  pads unused high lanes with zero. RX and TX word order is preserved.
* `sd[3:0]`: external device inputs. Standard TX uses SD[0] and Standard
  RX uses SD[1]. Dual/Quad use SD[1:0]/SD[3:0]; higher-numbered lanes
  carry the more significant bits. Each byte is sent most-significant
  bit/group first. Keep RX data stable across the host sample window;
  ambiguous samples are unresolved, never assumed correct.

The low-byte-first word contract is a registered project interpretation of
public theory lines 412–419 and 483, the register/programmer descriptions and
the original parent's boundary wiring at lines 427–460. Older internal theory
paragraphs 698–702 and 735–740 conflict with these clauses. They are retained
as historical disagreement, not treated as a maintainer-confirmed erratum.
Bit order within bytes is unchanged.

The checker checks payload, selected chip, minimum timing and transport
assumptions. It does not impose an undocumented completion deadline. A batch
ending with work pending or an ambiguous RX sample is inconclusive, not pass.
Checker failures are evidence about the DUT under this contract; do not change
the checker, DUT, reset semantics, or measurement. The model only supplies
stimulus. It receives no checker source, private calibration or solver witness.

Public sources (pinned revision):
- `hw/ip/spi_host/doc/theory_of_operation.md`
- `hw/ip/spi_host/doc/programmers_guide.md`
- `hw/ip/spi_host/rtl/spi_host.sv` (external boundary wiring only)

