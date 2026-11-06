# Independent reference contract v2 (frame_task, MIN=4, MAX=8)

## Signature
`check_rows(rows, require_drained=False, min_tail=32)` is a pure function. It returns `{verdict, failures, unknown, checked_rows}`.

- Final evaluation calls it with `min_tail=128`.
- Development and independent finite controls use 32.

## Edge model (registered, no bypass)
For each row with rst=0, the steps run in this order:

1. Check stability obligations at `pre`.
2. Sample `pre` against the scoreboard built from **earlier edges only**.
3. Check data and status transfers, using `pre` with the row's ready inputs, against the same prior-edge scoreboard.
4. Apply the current input acceptance (`s_valid && pre.s_ready`).
5. Check stability at `post` and sample `post` against the scoreboard **including** the input accepted at this edge.

A current input offer never justifies a `pre` output. Same-edge cut-through is a FAIL (v2 clarification).

## Presentation checks (v2)
Every `pre` and `post` sample is checked, except `pre` of cycle 0 and `pre` while rst=1.

- **Data:** a sample with m_valid=1 must have a justified beat at the data cursor. The checks are:
  - `data_spurious`: there is no frame at the cursor.
  - `data_premature`: the beat is beyond the known prefix, or is padding before s_last.
  - `data_payload` and `data_last`: the byte or last flag is wrong. Expected m_last is always definite for a known byte. A byte accepted with s_last=0 implies at least one more byte, so last=1 is expected only at the 8th byte.
- **Status:** a sample with h_valid=1 needs a completed accepted frame at the status cursor (`status_premature_or_spurious`).
- These checks apply with ready=0. A later reset or X does not erase the failure.

## Scoreboard
- The reset epoch holds a list of accepted frames, each with a known prefix and a done flag.
- There are independent data (frame, byte) and status cursors.
- Partial prefixes are supported.
- Padding is expected only after s_last. Truncation `last` falls on byte 8, and later input bytes are drained.
- Expected values come only from accepted inputs.

## Reset and unknowns
- On a reset edge, post must show m_valid=h_valid=0. Obligations are dropped and earlier failures are kept.
- rst=X loses the scoreboard until a known reset.
- Any X/Z that is meaningful is recorded as unknown.
- Verdict precedence: INVALID_INPUT (malformed, bad parameter, or source assumption violation) > FAIL > UNRESOLVED > PASS.

## Completion
With `require_drained=True`:

- Residual s_valid, m_valid or h_valid, an incomplete accepted frame, or unconsumed data or status responses are FAIL.
- A quiet tail (rst=0, s_valid=0, m_ready=h_ready=1) shorter than `min_tail` cycles is an unknown, so the result is UNRESOLVED and never PASS.

## Residual limitations (not resolved by invention)
1. After a definite transfer failure (`data_last`, spurious or premature transfer) or an X on a transfer, that channel's scoreboard is abandoned. Later errors on that channel are not reported. The verdict stays FAIL or UNRESOLVED.
2. Presentation failures do not latch, so a stalled bad beat is reported at every sample. This produces duplicate entries but does not change the verdict.
3. These cases are unknown or out of scope rather than checked:
   - input frames longer than 12 bytes;
   - traces that do not start with reset;
   - `pre` while rst=1.
4. Output changes between `post(n)` and `pre(n+1)` are checked only through the stated valid&&!ready stability rule and the per-sample justification checks.
5. s_ready is not checked except to determine input transfers. No liveness beyond the finite completion check is claimed.
6. The mapping of R0..R8 to candidate slots P0..P5 is not given. These are reference properties only.
7. The evidence is finite: selftests and controls. Neither the selftests nor any agreement with simulation proves the checker sound or complete. A PASS is evidence for that trace only.

