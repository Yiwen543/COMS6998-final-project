# Scoped I2C controller read/write checker contract

Scope: OpenTitan I2C controller (FifoDepth64) issuing address/data WRITE entries and READB entries to a single ACKing external target. Derived only from theory_of_operation.md L9-87 and registers.md FDATA/TIMING excerpts.

Observed: action push/flush/rst_n/target_ack, pre/post scl, sda, scl_pin, valid, ready, fmt_* head fields, rx_valid, rx_data, controller event outputs. Wire decoding uses consecutive samples (prev post, pre, post): START/STOP = SDA edge with SCL high; data bit = SDA at SCL rise; 8 data bits then ninth ACK bit. One pending setup bit at START/STOP is discarded; 2-7 pending bits or a full 8-bit byte without ninth bit is a failure. No internal RTL state, no hardcoded cycle counts.

Checked: write data and START flag, READB count (0=256), intermediate ACK / final NACK / RCONT ACK, START not issued for READB, STOP placement, one RX per read wire byte with matching data and order (RX may precede the ninth bit), FIFO head order, pop only after processing, reset separation.

Verdict: invalid if environment assumptions violated (READB+NAKOK, READB+RCONT+STOP, READB without read address, flush while active); fail on any property failure; pending if trace incomplete (open transaction, unpopped entries, undelivered RX) or an out-of-profile event (target NACK, timeout, arbitration, sda_unstable, interference) occurred; else pass. No liveness deadline is enforced.

Events (multi_byte_read, rcont_chain, read_then_restart, read_stretch_recovery) are credited only when the whole trace has no failures/assumption violations, the transaction window is clean (no unsupported event), every involved entry fully completed, popped and RX delivered. Partial or reset-terminated transactions never get credit.

Limits: no arbitration, multi-controller, NACK error recovery, timeout, analog or exact-cycle timing proof; target_data is not used as a DUT expectation; this is not a claim of full IP correctness.
