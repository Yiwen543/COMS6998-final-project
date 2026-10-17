Verification target: original 8-bit shifter interface, unsigned binary inputs.
left_right=1 means logical left shift, 0 means logical right shift; shift_bits=0..7.
The independent checker masks the left-shift result to 8 bits. The immutable
CVDP input RTL uses comparison operators instead of shifts and is expected to fail.
No DUT repair is allowed. Generate only stimulus vectors, never an RTL patch.
