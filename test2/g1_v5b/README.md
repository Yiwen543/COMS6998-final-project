# G1 R05B integration — prepared, pending P16

This new namespace integrates the separately sealed R05 cover reader without
editing R05,v4,E03 or older evidence. Actual R05 allocation is bound;it is not an
EXECUTE receipt. No real pool or lock exists yet.

New code is limited to cumulative allocation/gates,strict prior-artifact reuse,
native result/target separation and the registered runner. Runtime is byte-for-
byte v4;budget changes only the attempt-id text. All18SV and original inputs,
labels,flags,tools,guards,timing and physical parser remain unchanged in v5.
No specification oracle is modified.

Conditional reuse is now grounded in P15's saved-evidence/feasibility findings;
P16 must still accept these exact final implementation hashes. Reuse includes
E02QC00frontend/native pair and E03shared builds,QC00dualphysics,QC01frontend/native
pair. Every reused job is marked new_execution=false;all original costs/failures
remain. New traces/results go only to v5b;old compiled executables are read only.

New plan0setup/14compile/28native/30physical120cycles projects cumulative8/20/32/33,
132cycles. Actual prior counts8/6/4/3,12cycles and actual11.770645541s/charged
14.572948167s retained;allocation charge15/current1185/work1180 is not measured
spend or a reset. No native/physical retry reserve. Any unsafe reuse or new
failure remains charged;do not silently rebuild/rerun beyond the exact plan.

Eleven focused pure checks cover actual allocation,reuse,negative cover results,
missing/old gates,count reset,binary drift,synthetic ledger inheritance,truncated
coverVCD and missing BMC witness. They execute no tool/process/signal/sleep and
are not a complete mock of all72future jobs. Full positive entry/real G1 and all
remaining15physical pairs await exact P16+EXECUTE. Inspect saved evidence to
resume;never restart an existing pool/lock or modify a sealed input.

Entry once authorized:
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/g1_v5b/runner.py --execute-authorization <exact-coordinator-receipt>`
No authorization file is synthesized here. No modelAPI/key/raw/B/C/cross-IP,
installation,commit or push belongs to this phase.
