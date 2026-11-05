# Independent reference contract (frame_task, MIN=4, MAX=8)

## Model
- Per row: inputs applied, `pre` sampled, rising edge, `post` sampled. Transfers at the edge use row inputs and `pre` outputs with rst=0.
- Within one edge, the input transfer is applied to the scoreboard before the data/status transfers (same-edge cut-through allowed).
- Scoreboard per reset epoch: ordered list of accepted input frames (known prefix + completion flag), a data cursor (frame, byte) and a status cursor. Expected values come only from accepted inputs, never from DUT flags/state.
- Data and status cursors are independent; no inter-channel order is imposed.
- Initial `pre` (cycle 0) is not checked; `pre` while rst=1 is not checked; `post` of a reset edge must show m_valid=h_valid=0.
- Stability obligations are created at a sample when valid=1 and the corresponding ready=0 and checked at the next sample; they are dropped at reset.
- Payload when valid=0 is ignored. s_ready is only used to determine input transfers.
- Presented (non-transferred) m_last is checked only when already determined (input complete or 8 bytes reached); the transfer check is stricter.

## Verdicts
INVALID_INPUT (malformed or assumption-violating trace) > FAIL > UNRESOLVED > PASS. Unknowns never erase failures. PASS on a finite trace is evidence for that trace only.

## Completion (require_drained=True)
Residual s_valid/m_valid/h_valid, an incomplete accepted input frame, or unconsumed data/status responses are FAIL. A quiet tail shorter than 32 cycles is reported as unknown (`drain_tail_short`), since the 128-cycle final threshold is not signalled to the function.

## Blocking scope findings (not resolved by invention)
1. Same-edge causality: whether an output/status may be transferred at the same edge the justifying input byte/s_last is accepted (combinational cut-through) is not stated. This reference permits it; a stricter reading would change verdicts.
2. Source-assumption violations (s_valid during reset, blocked source changing) are treated as INVALID_INPUT; the packet only defines INVALID_INPUT for malformed rows.
3. Traces not starting with reset: the scoreboard is UNRESOLVED until a known reset edge; reset-free semantics are unspecified.
4. Extra keys in a row dict are ignored; inner inputs/pre/post dicts must contain exactly the documented fields.
5. Input frames longer than 12 bytes are out of scope and reported as unknown, not checked as a contract.
6. Mapping of candidate slots P0..P5 to properties is not given in the packet; R0..R5 are reference properties only, not a slot assignment.
7. Whether the drain tail length (32 vs 128) should change the verdict is not specified for this function; it is reported as unknown only.
8. Whether a registered DUT may change outputs between `post` of cycle n and `pre` of cycle n+1 when no stability condition holds is unspecified; only the stated valid&&!ready stability is enforced.

