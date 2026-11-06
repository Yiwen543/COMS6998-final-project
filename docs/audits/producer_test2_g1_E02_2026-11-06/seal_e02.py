"""Read/seal the single completed E02 entry. No tests, tools or retries."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
AUDIT = Path(__file__).resolve().parent
OUT = ROOT / 'test2/results/g1-qualification-v3'
R03 = ROOT / 'docs/audits/producer_test2_g1_R03_2026-11-06'
P12 = ROOT / 'docs/audits/agent_bridge_2026-11-06/P12_g1_retry_preflight'
STATUS = 'EXECUTED_PENDING_P13_SAVED_EVIDENCE_REVIEW'


def sha(path):
    assert path.is_file() and not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def rel(path):
    return path.relative_to(ROOT).as_posix()


def write(path, data):
    with path.open('x') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


assert not (AUDIT / 'phase.json').exists()
baseline = read(AUDIT / 'pre-entry.json')
reg_path = ROOT / 'test2/configs/g1_qualification_registration_v3.json'
reg = read(reg_path)
receipt_path = ROOT / 'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r03.json'
assert sha(receipt_path) == 'ac8d5ef19740cf1cda86b457f3f4e2f4f30b46b53f93439e5519216b59057be0'
assert sha(P12 / 'review.json') == '41c7ed9ee4af55dd6454b92e9356ddee22222c7ec4ea9de2c704de9fdebf70b2'
assert all(sha(ROOT / name) == expected for name, expected in baseline['protected_files'].items())
pool_path = ROOT / reg['pool_state']
pool, report = read(pool_path), read(OUT / 'report.json')
command = read(AUDIT / 'runner-command.json')
assert command['runner_exit_code'] == 1
assert pool['halted'] is True and pool['completed'] is True
assert pool['halt_reason'] == report['execution_error'] == 'Unqualified:PHYSICAL_EXPECTED_MISMATCH:a'
assert report['status'] == 'HALTED_WITH_REMAINDER_NOT_RUN' and report['controls'] == {}
events = pool['events']
assert len(events) == 13 and all(e['status'] == 'RETURNED' and e['exit_code'] == 0 for e in events)
assert all(not e['timed_out'] and not e['mandatory_errors'] and not e['cleanup_group_kill'] for e in events)
assert all(e['inventory']['attempts'] == 0 and e['inventory']['complete'] is False for e in events)
assert pool['attempt_reserved'] == dict(compile=3, native=2, physical=1, physical_cycles=4, setup=7)
assert pool['reserved'] == dict(compile=3, native=2, physical=1, physical_cycles=4, setup=8)
assert Counter(x['status'] for x in report['jobs'].values()) == {'RETURNED': 13, 'NOT_RUN': 76}
assert len(report['jobs']) == 89
for event in events:
    folder = OUT / 'jobs' / event['job_id']
    receipt = read(folder / 'receipt.json')
    assert receipt['job_id'] == event['job_id'] and receipt['exit_code'] == event['exit_code']
    for name in ['stdout', 'stderr']:
        assert sha(folder / (name + '.log')) == event[name + '_sha256'] == receipt[name + '_sha256']
raw_manifest = read(OUT / 'result-manifest.json')
assert all(sha(OUT / name) == expected for name, expected in raw_manifest['files'].items())
assert sha(ROOT / reg['predecessor_pool']) == reg['predecessor_pool_sha256']

labels = read(ROOT / reg['controls'])['cases']
physical_folder = OUT / 'jobs/QC00-icarus'
raw_text = (physical_folder / 'stdout.log').read_text()
rows = []
for line in raw_text.splitlines():
    if line.startswith('OBS '):
        row = dict(pair.split('=', 1) for pair in line.split()[1:])
        for name in ['qc', 'cycle', 'tick']:
            row[name] = int(row[name])
        rows.append(row)
assert len(rows) == 8 and 'END qc=0 cycles=4 posedges=4' in raw_text
mismatches = []
for index, (row, expected) in enumerate(zip(rows, labels[0]['physical_rows_expected_icarus'])):
    for field, value in expected.items():
        if row[field] != value:
            mismatches.append(dict(row_index=index, cycle=row['cycle'], phase=row['phase'],
                tick=row['tick'], field=field, expected=value, observed=row[field]))
assert mismatches[0] == dict(row_index=0, cycle=0, phase='pre', tick=1000,
    field='a', expected='0000', observed='xxxx')

# Saved VCD inspection only: no simulator/solver/parser qualification rerun.
vcd_path = physical_folder / 'trace.vcd'
lines = vcd_path.read_text().splitlines()
stack, clock_token = [], None
for line in lines:
    parts = line.split()
    if parts[:1] == ['$scope']:
        stack.append(parts[2])
    elif parts[:1] == ['$upscope']:
        stack.pop()
    elif parts[:1] == ['$var'] and parts[4] == 'clk' and stack == ['physical_tb']:
        clock_token = parts[3]
    elif parts[:1] == ['$enddefinitions']:
        break
assert clock_token is not None
tick, previous, posedges = 0, None, []
for line in lines:
    if line.startswith('#'):
        tick = int(line[1:])
    elif line and line[0] in '01xz' and line[1:] == clock_token:
        if previous == '0' and line[0] == '1':
            posedges.append(tick)
        previous = line[0]
assert posedges == [2000, 6000, 10000, 14000]
write(AUDIT / 'raw-observation-disclosure.json', dict(
    status='RAW_SAVED_OBSERVATIONS_NOT_ACCEPTED_CONTROL_ROWS', source_stdout=rel(physical_folder / 'stdout.log'),
    source_stdout_sha256=sha(physical_folder / 'stdout.log'), rows=rows,
    accepted_by_registered_parser=False, registered_refusal='PHYSICAL_EXPECTED_MISMATCH:a',
    independent_saved_text_mismatches=mismatches, raw_rows=8, accepted_rows=0,
    physical_cycles_from_END=4, posedges_from_saved_VCD=posedges,
    saved_VCD=rel(vcd_path), saved_VCD_sha256=sha(vcd_path),
    VCD_recorded_tick_span=[min(int(x[1:]) for x in lines if x.startswith('#')),
                            max(int(x[1:]) for x in lines if x.startswith('#'))],
    cause_knownness='NOT_EXPERIMENTALLY_QUALIFIED',
    source_based_hypothesis='Initial step is declared0 and assigned0 again before first observation;stimulus uses always@*. Time-zero combinational scheduling is a candidate explanation for cycle0 X inputs,not a demonstrated simulator bug. No fix or rerun.',
    limits='Raw text/clock count only;no dual-simulator agreement,accepted-row binding,oracle or128completion claim.'))

per_qc = []
for case in labels:
    cid = case['id']
    row = dict(qc=cid, declared_eligibility=case['eligibility'],
        declaration_is_not_observation=True,
        formal_compile=report['jobs']['compile-' + cid]['status'],
        native_BMC=report['jobs'][cid + '-bmc'].get('native_status', 'NOT_RUN'),
        activation_cover=report['jobs'][cid + '-cover'].get('native_status', 'NOT_RUN'),
        icarus_process=report['jobs'][cid + '-icarus']['status'],
        verilator_process=report['jobs'][cid + '-verilator']['status'],
        complete_control_qualified=False, completion128_credit=False,
        full_status='PARTIAL_REJECTED_PHYSICAL_EXPECTATION' if cid == 'QC00' else 'NOT_RUN',
        physical_row_validation='REJECTED:PHYSICAL_EXPECTED_MISMATCH:a' if cid == 'QC00' else 'NOT_RUN',
        observed_physical_cycles=4 if cid == 'QC00' else 0,
        limits=('BMC depth8 PASS and activation cover reached;Icarus root0 but row contract rejects;Verilator not run.'
                if cid == 'QC00' else 'Not dispatched after global halt;declared exclusions are not observed outcomes.'))
    per_qc.append(row)
write(AUDIT / 'per-qc-results.json', dict(controls=per_qc,
    fully_qualified_controls=0, partial_rejected_controls=1, not_run_controls=15,
    eligible_means='Declared limited public-control scope only,not qualification.',
    exclusions='QC07/15 vacuous;QC12/13 four-state equivalence unsupported;QC14 transport-only;all remain NOT_RUN.'))

versions = {}
for tool, pin in reg['tools'].items():
    job_id = 'setup-clangpp' if tool == 'clang++' else 'setup-' + tool
    folder = OUT / 'jobs' / job_id
    entry = dict(configured=pin['configured'], resolved=pin['resolved'],
        configured_binary_sha256=pin['resolved_sha256'], binary_pin_verified_by_runner=True,
        configured_version_argv=pin['version_argv'])
    if not folder.exists():
        entry.update(status='NOT_REPROBED_TO_PRESERVE_CUMULATIVE_SETUP_CAP', actual_version=None,
                     knownness='UNKNOWN_NO_VERSION_QUERY')
    else:
        stdout, stderr = (folder / 'stdout.log').read_text(), (folder / 'stderr.log').read_text()
        first = next((line for line in (stdout + '\n' + stderr).splitlines() if line.strip()), None)
        entry.update(status='RETURNED', exit_code=0, first_nonempty_output=first,
            stdout_sha256=sha(folder / 'stdout.log'), stderr_sha256=sha(folder / 'stderr.log'),
            actual_version=None if tool == 'smtbmc' else first,
            knownness='UNKNOWN_HELP_ONLY' if tool == 'smtbmc' else 'OBSERVED_VERSION_TEXT',
            raw_stdout=rel(folder / 'stdout.log'), raw_stderr=rel(folder / 'stderr.log'))
    versions[tool] = entry
write(AUDIT / 'tool-versions.json', versions)

resources = dict(current_attempt_reserved=pool['attempt_reserved'],
    current_dispatched_roots=dict(Counter(e['kind'] for e in events)),
    current_returned_roots=13, current_native_BMC_jobs=1, current_activation_cover_jobs=1,
    current_native_statuses={'PASS': 2}, current_physical_runs=1,
    current_observed_physical_cycles=4, current_raw_physical_rows=8, current_accepted_physical_rows=0,
    current_logical_compile_batches=3, actual_internal_OS_child_count=None,
    internal_child_count_knownness='UNKNOWN_NO_COMPLETE_INVENTORY;raw compiler commands retained',
    cumulative_reserved=pool['reserved'], prior_reserved=pool['prior_reserved'],
    cumulative_remaining_counters=pool['remaining'], remaining_is_not_restart_authorization=True,
    current_window_total_elapsed_recorded_seconds=pool['total_elapsed_seconds'],
    current_window_elapsed_checkpoint_seconds=pool['attempt_elapsed_checkpoint_seconds'],
    prior_actual_window_seconds=pool['prior_actual_window_seconds'],
    prior_conservative_charge_seconds=pool['prior_conservative_charge_seconds'],
    cumulative_actual_window_checkpoint_seconds=pool['cumulative_actual_window_seconds'],
    cumulative_charged_window_checkpoint_seconds=pool['cumulative_charged_window_seconds'],
    prior_charge_is_not_actual_spend=True,
    clock_note='Monotonic fields are sampled separately;preserve original checkpoint values rather than force arithmetic equality.',
    original_caps=pool['caps'], current_window_cap_seconds=1198,
    sum_root_elapsed_including_cleanup_seconds=sum(e['elapsed_seconds_including_cleanup'] for e in events),
    optional_inventory_attempts=0, full_inventory_complete=False,
    required_group_probe_receipts=13, required_protection_errors=0,
    timeout_roots=0, recorded_SIGKILL_attempts=0,
    memory_peak_bytes=None, memory_knownness='NOT_MEASURED',
    API=0, count=0, generation=0, Claude=0, key_access=0,
    extra_real_tool_or_process_probes=0, execution_entry_attempts=1,
    preparation_and_review=dict(prior_R03_partial_span_seconds=baseline['prior_partial_preparation_seconds'],
        P12_full_turn_approx_seconds=baseline['P12_full_turn_approx_seconds'],
        E02_full_turn_seconds=None, E02_full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',
        E02_observed_namespace_span_through_sealing_seconds=time.time()-baseline['observed_at_epoch'],
        namespace_span_includes_execution_and_audit_not_the_controlled_execution_cap=True))
write(AUDIT / 'resource-summary.json', resources)
write(AUDIT / 'process-and-job-summary.json', dict(
    jobs_status_counts=dict(Counter(x['status'] for x in report['jobs'].values())),
    events=[{key: e.get(key) for key in ['job_id','kind','status','exit_code','timed_out',
        'absolute_job_deadline','elapsed_seconds_including_cleanup','mandatory_errors',
        'owned_group_probe','cleanup_group_kill','root_exit_knownness']} for e in events],
    every_optional_inventory_attempts_zero=True, child_inventory_complete=False,
    note='13 root processes returned0. Adapter row rejection causes runner exit1;not a process timeout/nativeFAIL.'))

hallmark = Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')
assert sha(hallmark) == '25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3'
write(AUDIT / 'hallmark-usage.json', dict(hallmark=dict(considered=True,
    read_this_round=False, source=str(hallmark), source_sha256=sha(hallmark), version='2.0.0',
    read_evidence='Current bytes hash checked only;no new full read claimed for E02.',
    prior_read_reference='docs/audits/producer_test2_g1_R03_2026-11-06/hallmark-usage.json',
    applied_for=['Fixed reviewed input identities before one execution.',
        'Separate actual raw X evidence,unqualified cause hypothesis,process return and adapter rejection.',
        'Keep prior actual/charge/current costs,all NOT_RUN and no fabricated successful control.'],
    workflow_executed=False, scripts_executed=False,
    not_applicable_reason='No UI;Hallmark cannot prove RTL/native/runtime correctness.',
    technical_review_methods=['Saved raw log/VCD clock inspection','Exact source/result/ledger/Git preservation checks'],
    limits=['Producer evidence sealing only;P13 pending,no general or scientific qualification.'])))
p12a = ROOT / 'docs/audits/agent_bridge_2026-11-06/P12a_coordination_check.json'
write(AUDIT / 'scope-disclosure-p12-n1.json', dict(finding='P12-N1', severity='P3_NONBLOCKING',
    source=rel(p12a), source_sha256=sha(p12a), sealed_R03_not_modified=True,
    earlier_combined_turn='Included historical PPT/web reads and auxiliary records,as preserved in P12a;not G1-only/no-web.',
    zero_network_scope='Current controlled G1 runner and E02 evidence sealing only;not a claim about all historical turn activity.',
    elapsed_scope='Prior R03 partial1466.678544998169s and P12 approx575.6s are preparation/review,not the current1198s execution window. Full earlier turn unmeasured,not0.'))

lines_md = ['| QC | Declared scope | Formal compile | BMC | Cover | Icarus | Verilator | Full result |',
            '|---|---|---|---|---|---|---|---|']
for row in per_qc:
    lines_md.append('| ' + ' | '.join(str(row[k]) for k in ['qc','declared_eligibility',
        'formal_compile','native_BMC','activation_cover','icarus_process','verilator_process','full_status']) + ' |')
text = f'''# G1 E02 — exact R03 execution halted on physical-row mismatch

Status: **{STATUS}**. Outcome: **HALTED_ON_QC00_PHYSICAL_EXPECTATION_MISMATCH**.
Exact P12 acceptance and coordinator receipt were checked before the single registered
entry. Runner exit1; stdout/stderr for the entry are empty, while every job has
original raw logs/receipts. No code, label, pin, flag or limit was changed, and no
retry, extra version/smoke/compiler/process probe or permission escalation occurred.

## Observed execution

13 roots returned0:7setup,3logical compile batches,1BMC,1activation cover,1Icarus
physical run. QC00 BMC depth8 PASS; activation cover reached step2. These do not
complete QC00: Icarus cycle0 pre/post shows a/b=xxxx,rst/en/valid=x,active/ok=x
where the fixed table expects known reset inputs. The first parser refusal is
PHYSICAL_EXPECTED_MISMATCH:a at cycle0 pre/tick1000, expected0000/observedxxxx.
All raw X values remain.8OBS rows and END4cycles agree with saved VCD's4posedge
ticks2000/6000/10000/14000; no physical rows were accepted. QC00 Verilator and all
later QC jobs were NOT_RUN. Root return0 is distinct from adapter rejection.

Time-zero scheduling of the declaration-initialized step and always@* stimulus
is a source-based candidate explanation only. It was not experimentally isolated;
no simulator-bug conclusion, code repair, oracle change or rerun is made here.

{chr(10).join(lines_md)}

Complete qualified QC0; partial/rejected QC1; wholly NOT_RUN QC15. The16 declared
eligibilities above are not16 observations. QC07/15 vacuity,QC12/13 unsupported
four-state equivalence,QC14 finalpost transport remain exclusions and NOT_RUN.
No dual-simulator binding,128-cycle/unbounded completion,realDUT/oracle/monitor
soundness or C-benefit conclusion follows.

## Resource accounting

Current reservations/dispatches: setup7,compile3,native2,physical1/4cycles.
Cumulative including E01: setup8,compile3,native2,physical1/4cycles. Remaining
counters setup0,compile29,native30,physical31/1020cycles do not authorize restart.
Original32/32/32 roots,1024cycles and1200seconds caps remain;make version was not
reprobed. Actual internal compiler child count is UNKNOWN; raw commands are retained.

Current recorded window {pool['total_elapsed_seconds']:.12f}s; latest checkpoint
{pool['attempt_elapsed_checkpoint_seconds']:.12f}s. Historical measured window
{pool['prior_actual_window_seconds']:.12f}s differs from conservative prior charge2s.
Saved cumulative actual checkpoint {pool['cumulative_actual_window_seconds']:.12f}s;
charged checkpoint {pool['cumulative_charged_window_seconds']:.12f}s. Original fields
are separately sampled,not forced equal. Memory unmeasured. Full preparation/closure
turn elapsed is unmeasured,not0; prior R03 partial1466.678545s and P12 approx575.6s
are separate preparation/review. Resource-summary retains exact values.

All13 receipts show owned-group probe absent at its sampling point,0mandatory
errors,0timeouts/cleanup kills and0external inventory attempts. This is limited
observed process evidence,not an exhaustive child census or OS hard realtime
guarantee. API/count/generation/Claude/key/network/install/delete/index changes0
for this controlled G1 execution/E02 sealing path.

## Versions, provenance and next checkpoint

Tool-versions.json records actual version text from saved outputs:Yosys0.70+post,
Z3 5.1.0,Icarus/vvp12.0,Verilator5.050,Appleclang21.0.0. smtbmc help returned0 but
did not report a version:actual version UNKNOWN. Make remains NOT_REPROBED.
No standalone diagnostic was run to fill either unknown.

P12-N1 scope sidecar preserves P12a:the earlier combined preparation turn diverted
into historical PPT/web reads. Earlier network=0 is scoped to controlled G1
preparation,not the entire old turn. No frozen R03 original was edited.

Actual entry/exit and tool receipts:runner-command.json. Per-QC table,raw
observation refusal,VCDs,all76NOT_RUN,ledger,raw result manifest,source bindings
and exact original logs/build files are saved in this snapshot. Prior pure
fixtures in the shared result root are explicitly distinguished from2 new
actual job VCDs. No old tests/experiments/companion audits were rerun.

Next: existing P13 independently reviews this saved evidence with0additional real
jobs. Stop here; no pool reset/refund/retry/newprofile. Further routing requires
coordinator accounting of cumulative remaining resources under the original grant.
All old scores/timeouts/unknowns,P04/P05/P06/P05-N1/F1/selected-sample/category/
128completion/H1/H2/L1/74witness/billing/R0-R1-R2 limitations remain.
'''
with (AUDIT / 'report.md').open('x') as stream:
    stream.write(text)

section = f'''

## Current G1 execution — E02 / halted, pending P13 (2026-11-06)

Exact R03 executed once after P12 PASS_WITH_LIMITS, receipt SHAac8d5ef19740cf1cda86b457f3f4e2f4f30b46b53f93439e5519216b59057be0. Status **EXECUTED_PENDING_P13_SAVED_EVIDENCE_REVIEW**, outcome **HALTED_ON_QC00_PHYSICAL_EXPECTATION_MISMATCH**, runner exit1.13roots returned0(7setup/3logical compile/2native/1Icarus). QC00 depth8 BMC PASS and activation cover reached step2; Icarus cycle0 a/b=xxxx and reset/controlX contradict expected known reset table; first rejection PHYSICAL_EXPECTED_MISMATCH:a.8raw OBS/4VCDposedge cycles retained,0accepted rows; QC00 partial/rejected,other15QC NOT_RUN,0full QC qualified. Remaining76jobs NOT_RUN. No repair or retry.

Current reservations setup7/compile3/native2/physical1/4cycles; cumulative setup8/compile3/native2/physical1/4cycles. Current recorded window {pool['total_elapsed_seconds']:.9f}s; historical actual0.045724458s versus conservative prior charge2s separately retained; cumulative actual checkpoint {pool['cumulative_actual_window_seconds']:.9f}s,charged {pool['cumulative_charged_window_seconds']:.9f}s. Remaining setup0/compile29/native30/physical31/1020cycles is not restart authorization. New R03 pool halted/completed and attempt lock retained; old E01 pool unchanged.7actual setup outputs saved,smtbmc version UNKNOWN(help only),make NOT_REPROBED.0ps/optional inventory/mandatory protection errors;no full child census/hard realtime guarantee. Memory unmeasured.

Exact saved package `docs/audits/producer_test2_g1_E02_2026-11-06/phase.json` / `snapshot-manifest.json`, report/perQC/resources/raw-observation/tool-version files. FrozenR03/old scores/checker/unknowns/index unchanged;oldbody retained. P12-N1 sidecar limits prior network0 to controlled G1 preparation:old combined turn included PPT/web reads,not G1-only. R03 partial1466.678545s/P12approx575.6s are prep/review,not current1198s execution budget;full turn unmeasured,not0. Existing P13 next reviews saved evidence only;stop,0additional realjobs/API/key/network/install/delete/index/commit/push/newagent/chat/G2–G5. No128completion/realDUT/oracle/C-benefit or explanation ofall74witnesses;all historical scientific/billing limits retained.
'''
shared = {}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
    path = ROOT / 'docs' / name
    before = (AUDIT / 'before/docs' / name).read_bytes()
    assert path.read_bytes() == before
    header, body = before.split(b'\n',1)
    path.write_bytes(header + section.encode() + body)
    assert path.read_bytes().endswith(body)
    shared[name] = dict(before_sha256=sha(AUDIT / 'before/docs' / name),
        after_sha256=sha(path), entire_old_body_retained=True)

index = subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)
index_sha = hashlib.sha256(index).hexdigest()
assert index_sha == baseline['index_entries_sha256']
assert all(sha(ROOT / name) == expected for name, expected in baseline['protected_files'].items())
all_files = [p for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
actual_files = [p for p in all_files if p.relative_to(OUT).parts[0] in ['jobs','build','tmp'] or p.parent == OUT]
write(AUDIT / 'preservation-and-inventory.json', dict(
    protected_files_checked=len(baseline['protected_files']), protected_mismatches=[],
    index_entries_sha256=index_sha,index_unchanged=True,staged_changed_paths_count=baseline['staged_changed_paths_count'],
    shared_document_additions=shared, old_E01_pool_sha256=sha(ROOT / reg['predecessor_pool']),
    frozen_R03_manifest_sha256=sha(R03/'snapshot-manifest.json'),frozen_R03_unchanged=True,
    result_root_files=len(all_files),current_production_files=len(actual_files),
    prior_mock_fixture_files=len(all_files)-len(actual_files),
    new_actual_job_VCDs=[rel(p) for p in sorted((OUT/'jobs').rglob('*.vcd'))],
    all_result_files_sha256={str(p.relative_to(OUT)):sha(p) for p in all_files},
    raw_result_manifest_members_checked=len(raw_manifest['files']),
    raw_result_manifest_note='Producer result manifest includes pre-existing pure fixtures in this root and excludes final ledger. All retained;no mock VCD is labeled actual.'))
phase = dict(phase='G1_E02_EXACT_R03_EXECUTION',status=STATUS,
    outcome='HALTED_ON_QC00_PHYSICAL_EXPECTATION_MISMATCH',
    actual_HEAD=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    runner_exit_code=1,execution_receipt=rel(receipt_path),execution_receipt_sha256=sha(receipt_path),
    P12_review_sha256=sha(P12/'review.json'),R03_manifest_sha256=sha(R03/'snapshot-manifest.json'),
    registration_sha256=sha(reg_path),source_manifest_sha256=sha(ROOT/reg['source_manifest']),
    continuation_decision_sha256=reg['continuation_decision_sha256'],original_grant_sha256=reg['user_authorization_sha256'],
    predecessor_pool_sha256=sha(ROOT/reg['predecessor_pool']),
    current_final_pool=reg['pool_state'],current_final_pool_sha256=sha(pool_path),
    attempt_lock=reg['attempt_lock'],attempt_lock_sha256=sha(ROOT/reg['attempt_lock']),
    raw_report_sha256=sha(OUT/'report.json'),raw_result_manifest_sha256=sha(OUT/'result-manifest.json'),
    runner_command_sha256=sha(AUDIT/'runner-command.json'),
    original_caps=pool['caps'],native_depth=8,
    current_attempt_reserved=pool['attempt_reserved'],cumulative_reserved=pool['reserved'],
    cumulative_remaining=pool['remaining'],current_recorded_window_seconds=pool['total_elapsed_seconds'],
    prior_actual_window_seconds=pool['prior_actual_window_seconds'],prior_conservative_charge_seconds=2,
    cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],
    cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],
    root_statuses={'RETURNED':13,'NOT_RUN':76},adapter_refusal=pool['halt_reason'],
    fully_qualified_QC=0,partial_rejected_QC=1,not_run_QC=15,
    actual_physical_cycles=4,actual_raw_physical_rows=8,accepted_physical_rows=0,
    actual_job_VCDs=2,extra_real_jobs_or_probes=0,retries=0,tests_rerun=0,
    memory_bytes=None,memory_knownness='NOT_MEASURED',
    API=0,count=0,generation=0,Claude=0,key_access=0,
    network_scope='0 for this controlled G1/E02 path;earlier combined turn web/PPT explicitly disclosed in sidecar.',
    G2_G3_G4_G5=False,permissions_expanded=False,index_unchanged=True,
    old_protected_files_checked=len(baseline['protected_files']),old_hash_mismatches=[],
    preparation_review_elapsed=resources['preparation_and_review'],
    independent_acceptance='PENDING_P13_NOT_SELF_ACCEPTED',
    scientific_qualification='NOT_QUALIFIED',completion128_credit=False,
    snapshot_manifest=rel(AUDIT/'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase;phase names successor manifest without self-hash.',
    next_action='STOP_FOR_EXISTING_P13_READONLY_SAVED_EVIDENCE_REVIEW;NO_RETRY_OR_NEW_REAL_PROBES')
write(AUDIT/'phase.json',phase)

snap = AUDIT/'snapshot';snap.mkdir()
sources = [*all_files,* (ROOT/'test2/g1_v3').rglob('*'),reg_path,receipt_path,
    ROOT/reg['predecessor_pool'],ROOT/reg['predecessor_phase'],ROOT/reg['predecessor_review'],
    ROOT/reg['continuation_decision'],ROOT/reg['user_authorization'],
    R03/'phase.json',R03/'snapshot-manifest.json',
    P12/'review.json',P12/'review.md',P12/'evidence-manifest.json',p12a,
    ROOT/'docs/HANDOFF.md',ROOT/'docs/PROJECT_STATUS.md']
for source in sources:
    if not source.is_file() or '__pycache__' in source.parts:
        continue
    assert not source.is_symlink()
    target = snap/rel(source);target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        assert sha(target)==sha(source)
    else:
        shutil.copy2(source,target)
files = {p.relative_to(AUDIT).as_posix():sha(p) for p in sorted(AUDIT.rglob('*'))
         if p.is_file() and '__pycache__' not in p.parts}
write(AUDIT/'snapshot-manifest.json',dict(status=STATUS,files=files,file_count=len(files),
    excluded=['snapshot-manifest.json(self-hash)','__pycache__'],symlinks={},
    scope='Exact single E02 execution originals/costs/rejections/NOT_RUN plus immutable input identity snapshots.'))
print(json.dumps(dict(status=STATUS,outcome=phase['outcome'],runner_exit_code=1,
    phase_sha256=sha(AUDIT/'phase.json'),snapshot_manifest_sha256=sha(AUDIT/'snapshot-manifest.json'),
    current_pool_sha256=sha(pool_path),files=len(files),protected_files=len(baseline['protected_files']),
    current_reserved=pool['attempt_reserved'],cumulative_reserved=pool['reserved'],
    qualified_QC=0,NOT_RUN_jobs=76,index_unchanged=True),indent=2))
