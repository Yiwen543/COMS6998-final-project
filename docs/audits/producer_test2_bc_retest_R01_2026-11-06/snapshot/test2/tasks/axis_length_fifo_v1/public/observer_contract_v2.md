# Public observation and passive monitor interface v1

The public wrapper frame_task has the following pins:

| Direction | Pins | Width |
|---|---|---|
| input | clk,rst,s_valid,s_last,m_ready,h_ready | 1 each |
| input | s_data | 8 |
| output | s_ready,m_valid,m_last,h_valid,h_pad,h_truncate | 1 each |
| output | m_data | 8 |
| output | h_length,h_original_length | 16 each |

Rows are consecutive from cycle0. Each row has cycle, inputs, pre and post.
inputs contains rst,s_valid,s_data,s_last,m_ready,h_ready, applied before pre.
pre/post contain exactly the nine output fields above (excluding clk).
The rising edge follows pre; post is sampled after nonblocking assignments.
Input values remain fixed until the next cycle. A -1 value denotes X/Z.

An experimental candidate is a passive SV body with these same input pins
(including observed DUT output pins), plus outputs active[5:0],ok[5:0]. It has
six descriptions P0..P5. active[j] means a check is enabled and ok[j]=0 an alarm.
It can keep bounded private state but cannot drive DUT pins, add assumptions,
read hierarchy/files, instantiate modules, call system functions or see hidden
cases. Its internal expected state is not the scoring reference.

Replay records pre/post values independently without driving the DUT. A formal
harness checks each slot separately; assumptions are common and frozen, never
candidate-authored. Initial pre is excluded. Reset pre and post have distinct
synchronous meanings. Never-active slots are vacuous; active-cover PASS only
shows that activation can occur.

The independent reference exports check_rows(rows, require_drained=False, min_tail=32), a pure
function returning a dict with verdict, failures, unknown and checked_rows.
verdict is PASS, FAIL, UNRESOLVED or INVALID_INPUT. failures/unknown are lists
of dicts with cycle, phase (pre/post/end), category and detail. A definite FAIL
has priority over unknown; malformed rows or source-protocol assumption violations yield INVALID_INPUT. Partial valid
controls may omit final completion checks; evaluation explicitly requests them.
The reference never reads RTL, mutant implementation state or candidate outputs.

V2 reference contract: inspect all meaningful pre/post presentations, including blocked unjustified valids. Use prior-edge accepted state at pre, and state including the current accepted input at post. Call final observations with min_tail=128; development and independent finite controls use32 unless explicitly overridden.
