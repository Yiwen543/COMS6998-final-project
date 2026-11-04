# Bounded OpenTitan I2C READB profile

Fixed JSON driver plus independently Claude-authored wire checker. Original
OpenTitan RTL/specification remain in the pinned third-party checkout. This
profile is a separately versioned extension; the old write-only profile is
unchanged.

The checker covers read byte/count/order, ACK/NACK and command ordering under
the documented interface contract. See `contract.md`, `properties.json` and
`authorship.json`. The integration gate also checks driver errors and unsupported
event pulses. It does not promote stretch observations to recovery proofs.

`freeze.json` certifies only a scoped offline artifact snapshot. This profile
**is not eligible for B or A/B/C/P trials**: no multistep-specific equivalent
source groups pass selection. Fault attribution is also incomplete for the
extra-STOP control. No general formal correctness is claimed.

For exact reproduction commands, evidence and limitations see
[the read preflight report](../../docs/i2c_read_preflight_2026-11-04.md).
