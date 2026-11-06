# P10 exact R01 pre-execution review

Read-only independent math/RTL/registration review; zero compiler, simulator,
solver or version calls. Existing independent reviewer, no new agent/chat.
No producer independent acceptance is implied by this checklist.

1. Confirm source manifest and R01 seal identities, grant/caps and absence of
   real execution-state, waveform, build or EXECUTE receipt. Old freezes/grants
   and G0 scopes remain unchanged; this new grant supersedes old G1-unapproved
   prose only within its own scope.
2. Check all16 hand labels from language arithmetic and4-step state progression,
   including explicit widths, truncation at4, signed casts, complete guard,
   initial0/synchronous reset, the one deliberate reset-polarity change, and the
   exact sampled-pre vs physical-post distinction. Do not derive labels from
   future tool outcomes. Real-DUT/oracle truth stays UNQUALIFIED.
3. Check18 logical compilation batches and every internal compiler/tool process
   included in root/global timing, versus the user32-job cap. The batch counting
   interpretation and non-exhaustive PID sampling are explicit review questions.
   Reject before execution if that accounting does not meet the grant; do not
   silently treat all child compiler invocations as independently free jobs.
4. Check32depth8 BMC/cover only, dual32physical runs/128 planned cycles, fixed90
   root order, single exclusive persistent pool/global halt, reservation before
   dispatch, no retries/reset/resume, process-group kill, version/setup/parse/
   cleanup/output within one1200s clock. No unused quota is a new-profile grant.
5. Check QC07/QC15 no activation/completion credit, QC12/QC13 no four-state
   equivalence, QC14 no extra edge/DUT input, and QC08/09 native delayed sample
   binding. Tool failure, unsupported or UNKNOWN cannot be converted to PASS.
6. Check the profile-specific text/VCD parser's declared names/width/time subset
   and refusal semantics; no general raw-chain capability inherited from G0.
   No source has been compiled/simulated yet; syntax/tool ABI remains untested.
7. Read/use Hallmark according to future-review-policy.md; record actual path,
   SHA/read evidence, applicability and methods separately. UI workflow is not
   an RTL or budget proof. Review fixed inputs in fresh independent context and
   rank concrete findings by material risk with exact paths/minimal corrections.
8. Return exact status/findings/limits, source/grant/registration and R01 manifest
   identities. Required for the future non-secret gate: phase begins P10;
   input_identity.producer_manifest_sha256 and registration_sha256. Accepting
   R01 source/labels/resource plan does not itself launch a tool; coordinator
   sends EXECUTE under the existing G1 grant after the safe checkpoint.

No current paid/key stage is proposed. Any later model/oracle API needs its own
service/purpose/model/request/token/USD/time caps and specific user permission.
