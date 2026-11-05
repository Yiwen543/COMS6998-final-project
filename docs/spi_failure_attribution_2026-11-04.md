# SPI failure attribution — 4 November 2026

The two final checker failures from the safe-offer B development run are
consistent with **one probable DUT/specification discrepancy**, followed by
cascaded checker diagnostics. They are not evidence that the transport driver
is still dropping commands. The historical run remains unchanged and still
fails the original discrimination gate; this investigation does not admit C.

## Independent Claude review

`results/spi_core_safe_20261104/failure-attribution-v1/review.json` is the
unmodified response from a fresh, read-only `claude-opus-5-5` session.
The 147,404-byte packet includes all 596 actual cycles, the frozen checker,
public specification, fixed driver and original DUT closure. Case x/y/z map
to repetition 3/1/2, respectively. The packet excludes coverage rankings,
targets, model prompts and B/C performance. The reviewer has no tools and
cannot modify files. Unlike the specification-only checker author, this
diagnostic role sees RTL solely to attribute observed discrepancies.

Claude identifies same-CSID configuration changes after a CSAAT/held-CS
segment as the likely common cause, with medium confidence. The public
configuration-change contract requires the old transaction to close before
applying the new configuration. The FSM's held-CS path tests CSID changes
but does not apply its `config_changed` test there. Configuration registers
can consequently change while CS remains asserted.

The original failures are six diagnostics in two categories (repetition 2)
and seventeen in five categories (repetition 3). Those 23 diagnostics are
**not 23 independent defects**. Claude also identifies a secondary checker
diagnostic weakness: it lacks a direct close-out obligation and can interpret
a CPOL change as a serial edge, then report repeated downstream errors.
Its `checker_fit_for_new_scope` answer is false. The frozen checker is not
silently revised or treated as whole-IP certification.

## Exact-cycle corrections and independent controls

The review manually decoded compressed traces and misstated two acceptance
cycles. The raw queue ledger establishes:

| Case | Offer cycle | Accepted cycle | Review approximation |
|---|---:|---:|---:|
| x / repetition 3 | 193 | **197** | 196 |
| z / repetition 2 | 185 | **189** | approximately 187 |

These are acceptance times, not claimed first-error or segment-completion
times. The original review remains available alongside this correction.

GPT/Codex implemented Claude's requested private diagnostic stimuli without
editing any expected-output logic. Six controls each run for 136 cycles on
both Verilator and Icarus, using the original DUT, safe driver and Claude v4
checker. Actual pins, queue ledgers and checker results agree exactly.

| Control | Original checker | Observed CS boundary |
|---|---|---|
| Same CSID, same configuration, held CS | pass | CS remains held as expected by the existing checker |
| Same CSID, only CLKDIV changes 1 → 2 | fail: one `cs_framing` diagnostic at cycle 25 | no intermediate deassertion; accepts second command at 22 |
| Change CSID and CPOL | pass | old CS deasserts at 26; new CS asserts at 34 |
| Release CS before changing CPOL | pass | CS deasserts at 26; asserts again at 34 |
| Same CSID, only CPOL changes, CPHA=0 | fail: 103 diagnostics | no intermediate deassertion |
| Same CSID, only CPOL changes, CPHA=1 | fail: 102 diagnostics | no intermediate deassertion |

The CLKDIV-only control is particularly discriminating: it reproduces the
missing boundary without changing CPOL or CPHA. Large CPOL diagnostic counts
are cascades, not additional discovered bug types. The formerly unreplayed
positive case y was also replayed on Icarus and agrees with Verilator.

Evidence: `results/spi_core_safe_20261104/failure-attribution-controls-v1/`.
This is finite simulation evidence, not a formal proof or a new validated
checker. Driver queue conservation is checked independently of the DUT
checker; cross-simulator agreement alone cannot establish specification
correctness.

## Public corroboration and limits

An [existing OpenTitan issue #31692](https://github.com/lowRISC/opentitan/issues/31692)
describes the same held-CS configuration-change behavior on other revisions.
It was found **after** Claude's review. At lookup it was open with zero
comments; it is not a maintainer-confirmed resolution. The external report's
formal checks and proposed patch were not run or adopted here. No issue or
comment was posted. The independently observed local discrepancy is retained
as a probable DUT violation, with checker attribution limitations explicit.

If this failing scope is reused, a separate specification-only Claude author
must implement the direct transaction-close/timing obligation and validate it
against clean controls and single faults. Preserve all raw diagnostics and
counterexamples; label downstream cascades separately rather than deleting
evidence. Any correction belongs to a new checker version and freeze. It must
not retroactively change the old verdicts or excuse the DUT behavior.

## Cost, provenance and reproduction

- Claude: one call; 44.690 seconds; reported cost **$0.437321**; requested and
  returned model `claude-opus-5-5`; CLI budget parameter $4; low effort.
- Input accounting: 4 ordinary input + 70,137 cache-creation input + 0
  cache-read input = 70,141 input tokens; 4,331 output tokens; **74,472 total**.
  The 1,166 thinking tokens are a subset of output and are not added again.
- Controls: **13 new simulations, 1,812 cycles, zero new compilations**, using
  pre-existing binaries. Simulation subprocess time: 0.378 seconds. The two
  earlier failure replays (416 cycles) are historical and not counted again.
- No OpenAI calls or new B/C runs. Staged Anthropic credentials were deleted.
- Repository base: `50d7ee83d61989017e28e981420cd58f4c5f0787` plus the recorded
  working-tree artifacts; no new commit or push is claimed.
- Checker SHA-256:
  `07765601452ca14f078e8a3889f6d2d21574181091eb404c717087ce2d20a540`.
  Original DUT revision `0ea5236fe749e70ba18f56ba19c4be982ef46da7` and complete
  source/trace hashes are preserved in the review packet manifest. The old
  experiment freeze verifies unchanged.

Run from the repository root, using new output directories:

```sh
.venv/bin/python scripts/review_spi_core_failures.py --mode prepare --output build/spi-failure-review
.venv/bin/python scripts/probe_spi_failure_attribution.py --output build/spi-failure-controls
.venv/bin/python -m unittest discover -s tests -p test_multistep_event_screen.py -v
```

The prepare command makes no API call. Repeating the historical live review
would require a newly staged credential and the script's `--mode live
--packet … --output …` arguments; it is unnecessary for replaying evidence.
The [new event screening](multistep_event_screen_2026-11-04.md) is separate
from this diagnostic experiment and retains the original B budget.
