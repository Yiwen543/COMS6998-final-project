# OpenTitan I2C controller offline fixture

This folder freezes a **scoped write-mode checker/driver**, not an A/B/C experiment.
Original source and public specification remain in the pinned OpenTitan checkout;
`provenance.json` records their hashes. `freeze.json` checks them before replay.

The JSON schema allows only cycle actions. `push` enqueues byte/start/stop/nak_ok
in a fixed 64-entry FMT FIFO, which holds its head until the DUT pops it. `flush`
requires halted/idle environment conditions. `clear_events` clears sticky public
event state. `target_ack` controls a passive write target, `stretch` pulls SCL low,
and enable/reset/timeout fields drive their corresponding controller inputs.
Reset is active-low asynchronous. READB/RCONT are fixed zero in this scope.

The bus uses open-drain wired-AND with a launch register and two input synchronizer
flops. The target reads physical bus edges only. Initial batches include two reset
cycles. A whole batch runs before the Claude checker; environment errors, failures,
assumption violations or pending obligations prevent event credit. Coverage keeps
all original controller counters, including unsupported read/arbitration paths.

`checker.py`, `selftest.py`, `properties.json` and `contract.md` are exact Claude
artifacts. The SV driver, schema and private calibration are GPT/Codex integration
work. See [the report](../../docs/i2c_role_separated_preflight_2026-11-04.md) for
controls, failures, limits and reproduction commands. Do not expose the private
calibration or checker controls to future experimental stimulus sessions.
