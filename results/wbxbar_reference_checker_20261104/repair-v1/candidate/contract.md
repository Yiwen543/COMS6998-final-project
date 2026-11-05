# WBXBAR exact-history reference checker (candidate)

Scope: public pins of WBXBAR rev 2e8d3bc2, NM=2, NS=2, AW=8, DW=32, slave0 = (addr&0xf0)==0x00, slave1 = (addr&0xf0)==0x10. Rows are pre/post samples; only pre defines transfers, post is used for K1 reset outputs. Candidate only: independent controls, code review, freeze and replay are required before any B/C.

## Model
Exact explicit hypothesis set H per reset epoch; no quotient, partition, deduplication or pruning. Each hypothesis holds per-master FIFOs of live entries (identity, accept_row, master_epoch, reset_epoch, state unforwarded/forwarded/slave_acked/slave_erred/slave_canceled), a canceled pool of distinct members, orphans, per-slave forward FIFOs and a tag list. Row order: reset; CYC drop; master acceptances; slave CYC withdrawal; slave responses (bind to forwards from rows < c); slave acceptances (branch over every identity-equal candidate); master responses (K13, then K6/K7/K8 against entries from rows < c); association-free checks.

## Verdicts
scoped_pass, dut_violation, input_or_scope_invalid, unresolved only. Per-clause statuses are in counts.property_status (violated, suspended, unresolved, checked_not_refuted, prefix_checked_not_refuted, excluded_not_judged). scoped_pass means not refuted by the reference on this trace; it excludes K5 forward order and unproved characterization C1-C4, and is not proof of hidden ownership. Ownership per epoch is unique_by_elimination or indistinguishable(k) in counts.pending_alternatives.

Time-bounded precedence: e = first row with an environment violation; processing stops there. DUT violations before e stay final. At row e, pin-only DUT checks (K1, K2 slave payload, K3, K10, K13, rule 3.45) stay dut_violation; the K6 per-CYC count bound (proposed decision P4, see below) also stays dut_violation; association-dependent or row-e-input-dependent candidates (empty H, K4 per-identity count projection) become mixed_same_edge(dut_candidate, env), unresolved, with a note that no public ordering exists. counts.prefix_status gives prefix_scoped_pass / prefix_unresolved / prefix_dut_violation for rows < e.

## Unknown tags
post_abort_forward, unexplained_mapped_err, same_edge_response_after_abort, possible_starvation_err, starvation_attributed; any unclassified tag defaults to unknown. Tags carried by any surviving history are flushed to cumulative unresolved records at reset and batch end; reset never erases cumulative uncertainty.

Repeated HR ERRs during one held request are absorbed by branch B and are not judged; they stay unknown.

## Resource limits
Defaults MAX_HYP=4096, MAX_LIVE_PER_MASTER=64, MAX_CANCELED_POOL=256. The limits argument is for development selftests only and is validated; frozen callers pass rows only. On exhaustion: unresolved_on_limit(row, sizes), association clauses (K4 per-candidate, K6, K7, K8 attribution, K9 tags, K12) suspended for all masters until reset; still checked: K1, K2, K3, K10, K11, K13, rule 3.45, K4 per-identity count projection, per-slave response count, per-CYC ACK+non-HR-ERR bound. Counters are arbitrary-precision Python ints. counts.checked_scope reports suspended rows, fraction, exhaustion rows/sizes and effective checked rows.

## Declared exclusions
K5 order; C1-C4; liveness/latency/deadlines; payload while STB low, read-data lanes on requests, SEL-disabled lanes; write ACK data; reset-row master responses beyond K13/3.45; rule 3.05 sub-row reset length; formal F1-F8 unproved.

## Implementation decisions and blockers (not settled by the reviewed contract)
- B2 when the row-c entry was already forwarded in the same row: treated as orphan with post_abort_forward + starvation_attributed tags (blocker: contract silent).
- Undefined i_sdata on a slave ACK is an env violation only if at least one history binds it to a live read (blocker: hypothesis-dependent env classification).
- Simultaneous o_mack&o_merr: rule 3.45 violation, response not attributed.
- K13 is not judged on the first trace row (no c-1).
- The K6 count bound uses acceptances from earlier rows of the current CYC (consistent with K6 retiring only rows < c).
- Master STB without CYC is not an acceptance and is not separately flagged.
- slave_canceled live entries at batch end are counted (non-obligation), not pending.
- A row with undefined DUT control output is a DUT violation and stops judgment (unjudgeable_row).
- Mixed same-edge pin-only vs association-dependent split as described above.

## Proposed decisions for fresh independent review (not normative authority)
- P1 (F1): On exhaustion, tags of the histories feasible immediately before suspension are flushed to unresolved (class unknown, marked pre-suspension) and a pending_alternatives record with reason suspended_on_limit is emitted. On membership death, tags carried by histories alive at the start of the dying row are recorded in counts.discarded_epoch_evidence, explicitly as refuted-history disclosure: not open uncertainty, not a hidden-owner fact, never masking the fault; a membership_dead record is emitted. Tags created within the dying row itself are not captured (disclosed limitation).
- P2 (F2): Per-clause activation units in counts.clause_activations: K1 reset rows; K2 master held/accepted strobes plus slave acceptances; K3/K4 slave acceptances; K6/K8 master responses with CYC high; K7 master ACKs; K9 master CYC 1->0 transitions; K10 slave strobe rows plus ACK&ERR rows; K11 nonreset rows; K12 batch-end closure; K13 responses with CYC low. A non-violated, non-suspended, non-unresolved clause with zero activations reports not_activated. Zero activation is never a DUT violation and never a formal or cover claim.
- P3 (F3): Displays capped at 16 histories and 8 witnesses with explicit histories_total/displayed/omitted and witness shown/total/omitted; no history is pruned for reporting.
- P4 (F4): The K6 per-CYC count bound uses only DUT response pins and acceptances from rows < c within the current CYC (a CYC drop at row c routes the response to K13), so at row e it depends only on pins and inputs from rows < e and is kept as dut_violation under precedence rule (2). The K4 per-identity projection counts row-c master acceptances (permitted same-row forward), so at row e it remains mixed_same_edge. Membership death at row e remains mixed_same_edge.
- P5 (F5): B2 on an entry already forwarded in its acceptance row: kept as orphan with post_abort_forward + starvation_attributed tags; branch B1 is always also kept, so no verdict depends on B2 alone. Undefined i_sdata on a slave ACK: env violation only if some history binds it to a live read (hypothesis-dependent; integer drivers cannot emit None). Undefined pre DUT control output: DUT violation, judgment stops (unjudgeable_row). First-row K13 not judged (no c-1). All remain scoped decisions pending review.
- Events list is always empty; no recovery event or ownership proof is invented.
- Identical histories are not merged, so exhaustion may occur earlier than with a quotient; this is reported, never pruned.

