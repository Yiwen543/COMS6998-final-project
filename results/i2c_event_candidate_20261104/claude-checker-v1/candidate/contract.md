# Scope
Write-mode wire scoreboard for pinned OpenTitan i2c_controller_fsm (FifoDepth=64). Decodes physical scl/sda edges (previous post, pre, post order), reconstructs START/STOP, 8-bit MSB-first bytes and ACK slot, compares to pushed commands. Reset safety, halt-on-unexpected-NACK, NACK-timeout STOP/release, and stretch/NACK recovery events.

# Limitations
Not a full I2C correctness claim. Excludes read mode, arbitration/multi-controller, analog timing, register bus, exact cycle liveness. Incomplete transfers are reported unresolved/pending, never success. Expected NACKs (NAKOK) are events, not defects. Halt SCL-hold check is heuristic; timeout attribution uses public nak_timeout output plus observed STOP.
