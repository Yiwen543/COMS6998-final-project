# Fixed 8-bit iterative divider verification contract

Subject: CVDP `cvdp_copilot_radix2_div_0001`, original context RTL
`rtl/radix2_div.sv`, SHA-256
`64f9f4f2f8adece3b8630e8e14c1a8774c307def39ffc79655f978ef6ca77e30`.
The original source is preserved. The CVDP prompt also contains failing
examples and proposed repair text; **neither is included in model prompts**.

Inputs are `clk`, active-low asynchronous `rst_n`, one-cycle `start`, and
8-bit unsigned `dividend` and `divisor`. A start is accepted only while idle.
The input operands remain stable until completion. A new operation may begin
after `done`. Reset aborts an operation and clears `quotient`, `remainder`,
and `done` immediately, before a clock edge.

For a nonzero divisor, completion must produce unsigned integer quotient
`dividend // divisor` and remainder `dividend % divisor`. This is derived
from arithmetic, not the RTL algorithm. `done` is a one-cycle pulse after
eight processing edges following the accepted start edge. Division by zero
is defined for this fixed interface contract to produce `quotient=0xFF`,
`remainder=0xFF`, and `done=1` on the start edge. The zero-divisor response
is a declared study assumption because the benchmark prose does not define
it unambiguously; it must not be presented as a general divider standard.

The checker observes only public outputs before and after each active edge.
No internal bit counter, busy register, or RTL computation is an oracle.
Coverage uses original DUT source counters and retains uncovered targets in
the denominator, including unsupported extractor cases.
