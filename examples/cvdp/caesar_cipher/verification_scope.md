Verification target: original Caesar cipher interface, 8-bit character and 4-bit key.
ASCII A..Z and a..z rotate modulo 26 within the same case; other bytes are unchanged.
The independent checker enforces these ranges. Predicate atoms describe the
actual buggy RTL guards, not the intended ranges. le_a && ge_z has no concrete
8-bit character witness. Keep its raw coverage counter in the denominator.
No DUT repair is allowed. Generate only stimulus vectors, never an RTL patch.
Coverage objective is source line coverage: this build has no branch counters.
