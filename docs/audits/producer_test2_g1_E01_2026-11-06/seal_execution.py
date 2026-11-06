"""Saved-evidence E01 summary/seal only. No runner, tests or tool jobs launched."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PHASE = Path(__file__).resolve().parent
REG = ROOT / 'test2/configs/g1_qualification_registration_v2.json'
R02 = ROOT / 'docs/audits/producer_test2_g1_R02_2026-11-05'
P10B = ROOT / 'docs/audits/agent_bridge_2026-11-06/P10B_g1_fix'
RECEIPT = ROOT / 'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-v2.json'
metadata_started = time.monotonic()


def read(path):
    return json.loads(path.read_text())


def sha(path):
    assert not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def write(path, data):
    with path.open('x') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def git(*args):
    proc = subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                          text=True, check=True)
    return dict(argv=['git', *args], exit_code=proc.returncode,
                stdout=proc.stdout, stderr=proc.stderr)


assert not (PHASE / 'phase.json').exists()
reg = read(REG)
OUT = ROOT / reg['result_root']
POOL = ROOT / reg['pool_state']
report, pool = read(OUT / 'report.json'), read(POOL)
jobs = read(ROOT / reg['job_plan'])['jobs']
raw_manifest = read(OUT / 'result-manifest.json')
assert all(sha(OUT / path) == expected for path, expected in raw_manifest['files'].items())
assert report['status'] == 'HALTED_WITH_REMAINDER_NOT_RUN'
assert pool['halted'] and pool['completed']
assert pool['reserved'] == dict(compile=0, native=0, physical=0, physical_cycles=0, setup=1)
assert len(pool['events']) == 1
event = pool['events'][0]
assert event['job_id'] == 'setup-yosys' and event['status'] == 'ERROR'
assert event['dispatch_attempted'] and 'PermissionError' in event['error'] and '/bin/ps' in event['error']
assert event['exit_code'] is None
statuses = Counter(value['status'] for value in report['jobs'].values())
assert statuses == {'NOT_RUN': 89, 'ERROR': 1}
assert not report['controls']
by_kind = {}
for kind in ['setup', 'compile', 'native', 'physical']:
    by_kind[kind] = dict(Counter(report['jobs'][job['id']]['status'] for job in jobs if job['kind'] == kind))
write(PHASE / 'runner-exit.json', dict(
    command=read(PHASE / 'execution-command.json')['command_argv'],
    environment_override={'PYTHONDONTWRITEBYTECODE': '1'}, exit_code=1,
    tool_receipt='dc4f6b', outer_tool_reported_wait_seconds=0.022352959,
    stdout_sha256=sha(PHASE / 'runner.stdout.log'), stderr_sha256=sha(PHASE / 'runner.stderr.log'),
    scope='One exact authorized attempt; not rerun. Outer tool wait receipt is not substituted for runner monotonic resource duration.',
    exit_recorded_epoch=time.time()))
source = read(ROOT / reg['source_manifest'])
assert all(sha(ROOT / path) == expected for path, expected in source['files'].items())
protected = read(R02 / 'protected-before.json')['files']
assert all(sha(ROOT / path) == expected for path, expected in protected.items())
assert sha(R02 / 'phase.json') == 'ae927e87cf7ee8b22ea76c1e29914ebfc27b5691f53e2838b7af73e40a05d7c7'
assert sha(R02 / 'snapshot-manifest.json') == '7c16e5020ab6212fbd66bdd57ecb272bef56e1bfc6ce4362a661960d331fb201'
r02_snapshot = read(R02 / 'snapshot-manifest.json')
assert all(sha(R02 / path) == expected for path, expected in r02_snapshot['files'].items())
r02_current_copies = 0
for path, expected in r02_snapshot['files'].items():
    if path.startswith('snapshot/'):
        original = path[len('snapshot/'):]
        if original.startswith(('test2/g1_v2/', 'test2/results/g1-qualification-v2/regression-attempt1/')):
            assert sha(ROOT / original) == expected
            r02_current_copies += 1
assert sha(RECEIPT) == '9a6dfd949c54e1a159ff4b3e8e97999edc306c8dcac3cf3b233785a29de0dd95'
assert sha(P10B / 'review.json') == '864e76e168db17878e29bbf1d580b546620497acf269b3dcb34a144775c460dc'
labels = read(ROOT / reg['controls'])['cases']
per_qc = []
for case in labels:
    subset = [job for job in jobs if job.get('qc') == case['id']]
    assert all(report['jobs'][job['id']]['status'] == 'NOT_RUN' for job in subset)
    per_qc.append(dict(id=case['id'], execution_status='NOT_RUN',
        reason=pool['halt_reason'], declared_eligibility=case['eligibility'],
        expected_BMC=case['native_BMC_expected'], expected_cover=case['activation_cover_expected'],
        actual_BMC='NOT_RUN', actual_cover='NOT_RUN',
        actual_icarus='NOT_RUN', actual_verilator='NOT_RUN',
        actual_physical_rows=None, actual_waveforms=None,
        qualified=False, science='NOT_EVALUATED', completion128_credit=False,
        note='Declared vacuity/four-state exclusions are plan scope, not observed native results.'))
write(PHASE / 'per-qc.json', per_qc)
versions = {}
for name, tool in reg['tools'].items():
    job_id = 'setup-' + name.replace('+', 'p')
    status = report['jobs'][job_id]
    versions[name] = dict(configured=tool['configured'], resolved=tool['resolved'],
        registered_binary_sha256=tool['resolved_sha256'],
        version_argv=tool['version_argv'], actual_version=None,
        actual_version_knownness='UNKNOWN' if job_id == 'setup-yosys' else 'NOT_RUN',
        setup_status=status['status'], setup_exit_code=status.get('exit_code'),
        root_pin_verification_scope='Runner reaches first setup only after all registered binary hash comparisons. No version is inferred from a path or historical record.')
write(PHASE / 'tool-observations.json', versions)
window = dict(start_monotonic=pool['start_monotonic'], start_epoch=pool['start_epoch'],
    start_UTC=datetime.fromtimestamp(pool['start_epoch'], timezone.utc).isoformat(),
    start_America_New_York=datetime.fromtimestamp(pool['start_epoch'], ZoneInfo('America/New_York')).isoformat(),
    setup_first_reserved_elapsed=event['reserved_at_elapsed'],
    setup_root_elapsed_including_cleanup=event['elapsed_seconds_including_cleanup'],
    global_elapsed_after_other_output=pool['elapsed_after_all_other_output_writes'],
    global_total_elapsed_seconds=pool['total_elapsed_seconds'],
    pool_file_mtime_epoch=POOL.stat().st_mtime,
    cap_seconds=reg['caps']['wall_seconds'],
    scope='Recorded runner monotonic window including its setup/hash/parse/report serialization. E01 saved-evidence documentation/sealing is separately measured; full-turn thinking time not instrumented.')
remaining = dict(pool['remaining'], setup_queries=reg['caps']['setup_jobs']-pool['reserved']['setup'])
summary = dict(status='EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW',
    execution_outcome='HALTED_DURING_FIRST_SETUP_NO_QC_EXECUTED',
    raw_runner_status=report['status'], runner_exit_code=1,
    stop_reason=pool['halt_reason'], job_status_counts=dict(statuses), job_counts_by_kind=by_kind,
    actual_reserved=pool['reserved'], native_depth=reg['native_depth'],
    actual_native_BMC_cover_jobs=0, actual_compilation_jobs=0,
    actual_physical_simulator_runs=0, actual_physical_cycles=0,
    actual_native_waveform_files=len(list((OUT / 'jobs').rglob('trace.vcd'))),
    actual_physical_observation_rows=0,
    successful_version_queries=0, dispatched_version_queries=1,
    failed_monitor_command=['/bin/ps', '-ax', '-o', 'pid=,ppid=,pgid=,comm='],
    failed_monitor_attempts_inferred_from_saved_error=1,
    successful_monitor_calls_recorded=event['monitor_calls'],
    root_process_group=event['process_group'], root_exit_code=None,
    root_exit_code_knownness='UNKNOWN_NOT_CAPTURED_AFTER_SUPERVISOR_ERROR',
    cleanup_group_kill_recorded=event['cleanup_group_kill'],
    child_lifecycle='Cleanup attempt/wait path recorded;no complete child PID census or independently observed lifecycle proof. Empty observed list is not absence proof.',
    timing=window, unused_counters_at_halt=remaining,
    unused_counters_are_not_authorization_to_restart=True,
    local_memory_peak=None, local_memory_peak_knownness='NOT_MEASURED',
    timeout_jobs=0, invalid_candidate_results='NOT_APPLICABLE_NO_CANDIDATES',
    science='NOT_EVALUATED', G1_qualification='NOT_QUALIFIED_SETUP_SUPERVISION_ERROR',
    limitations=['No real native/physical/compile control outcome or actual tool version collected',
        'No claim about SV support, DUT/oracle/monitor correctness,128completion,old74 witnesses or C benefit',
        'Prior analytic/mock fixtures in result root are preserved historical preparation evidence,not newly generated traces',
        'Outer tool wait receipt and runner monotonic duration have different reporting scopes; no wall-duration inference from poll latency',
        'Old P04/P05/P06/P05-N1/F1/selected-sample/category/H1/H2/L1/billing/recovery limits unchanged'],
    API_count_generation_Claude_key_network_install_commit_push_delete=0,
    source_or_profile_changed_after_outcome=False, reruns=0)
write(PHASE / 'execution-summary.json', summary)
input_hashes = dict(source['files'])
for path in [REG, ROOT / reg['source_manifest'], ROOT / reg['user_authorization'],
             R02 / 'phase.json', R02 / 'snapshot-manifest.json', RECEIPT,
             P10B / 'review.json', P10B / 'review.md', POOL,
             OUT / 'report.json', OUT / 'result-manifest.json']:
    input_hashes[rel(path)] = sha(path)
for name in ['evidence-manifest.json', 'snapshot-manifest.json', 'phase-packet.json']:
    if (P10B / name).exists():
        input_hashes[rel(P10B / name)] = sha(P10B / name)
for path in (OUT / 'jobs').rglob('*'):
    if path.is_file():
        input_hashes[rel(path)] = sha(path)
write(PHASE / 'input-and-output-bindings.json', dict(files=input_hashes,
    source_files_verified=len(source['files']), old_protected_files_verified=len(protected),
    R02_snapshot_members_verified=len(r02_snapshot['files']),
    R02_current_source_and_prior_regression_copies_verified=r02_current_copies,
    protected_mismatches=[], actual_result_manifest_members_verified=len(raw_manifest['files']),
    full_old_cohort_audit_rerun=False))
text = f'''# G1 E01 execution outcome — 2026-11-06 America/New_York

Status: **EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW**.
Outcome: **HALTED_DURING_FIRST_SETUP_NO_QC_EXECUTED**. This is not G1 qualification success.

The exact R02 command was invoked once under the accepted receipt. Runner exited1
and its raw stdout/stderr are empty. The first `yosys -V` job was dispatched,
then `/bin/ps` supervision raised the saved PermissionError. The supervisor
recorded ERROR, a process-group kill attempt and persistent halt. The root exit
code is null/UNKNOWN; do not invent a successful/failed Yosys version result or
say that a language control failed. No version output was collected.

| Actual root-job category | Dispatched/reserved | NOT_RUN |
|---|---:|---:|
| Setup/version | 1 ERROR | 7 |
| Compilation | 0 | 18 |
| Native BMC/activation cover | 0 | 32 |
| Physical Icarus/Verilator | 0 | 32 |

All16 QC execution outcomes are NOT_RUN, with0 physical cycles/rows and no actual
native or simulator VCD. Pre-existing analytic VCD regression fixtures remain
preparation evidence; they are not execution traces. QC07/15 ineligibility and
QC12/13 four-state exclusions remain declared scope, not observed cover results.
QC14 transport and128-cycle completion were not exercised.

The registered single pool is now halted/completed; one setup reservation remains
charged. Its recorded global monotonic window is {pool['total_elapsed_seconds']:.9f}s,
including runner setup/hash/parse/output work. The setup process receipt records
{event['elapsed_seconds_including_cleanup']:.9f}s including cleanup. Empty PID
observations do not prove no children; monitoring was denied, so full child
lifecycle and root exit remain unverified. Local peak memory is unmeasured.
Unused counts32compile/32native/32physical/1024cycles/7setup are not a new grant,
permission to repair this profile, or permission to reset/restart its pool.

No source, labels, flags, cap or profile was changed after outcome. No retry,
smoke test, simulator, solver, native job, API/count/generation/Claude/key access,
network/install/delete/commit/push occurred in postprocessing. Only saved JSON,
logs/hashes and metadata are inspected; no process/signal diagnostic is retried.
The saved PermissionError identifies the execution-environment refusal.

P10B PASS_WITH_LIMITS remains execution-precheck acceptance only; frozen R02,
R01/P10 CHANGES_REQUIRED and all old evidence remain unchanged. P11 should read
the exact saved report/pool/job receipts, source and public arithmetic only,
with0 extra compiler/native/physical jobs and no refreshed budget. Hallmark use
is applicability-limited organization/critique, not an RTL or UI workflow pass.
No conclusion about E-graph or B/C efficacy, real DUT/oracle/monitor correctness,
old74 witnesses or128/unbounded completion follows from this halted setup.
'''
with (PHASE / 'report.md').open('x') as stream:
    stream.write(text)
section = f'''

## Current G1 execution — E01, halted / pending P11 (2026-11-06)

Exact R02 was executed once after P10B **PASS_WITH_LIMITS** using receipt SHA9a6dfd949c54e1a159ff4b3e8e97999edc306c8dcac3cf3b233785a29de0dd95. E01 status **EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW**; outcome **HALTED_DURING_FIRST_SETUP_NO_QC_EXECUTED**. First `yosys -V` dispatched, then `/bin/ps` supervision raised PermissionError; runner exited1, recorded ERROR/cleanup-group-kill attempt and persistent halt. Version/root exit remain UNKNOWN, rawstdout/stderr empty; not a Yosys semantic/control failure or G1 qualification success.

Actual reserved setup1; remaining7setup+18compile+32native+32physical jobs are NOT_RUN(89total). Actual compile/native/physical runs/cycles/observation rows0, all16QC NOT_RUN, actual generated waveforms none. Declared vacuity/four-state exclusions are not observed outcomes. Recorded runner window {pool['total_elapsed_seconds']:.9f}s, firstroot {event['elapsed_seconds_including_cleanup']:.9f}s including cleanup; empty observed PID list is not full child-lifecycle proof. Memory unmeasured. Same canonical `{reg['pool_state']}` is now halted/completed; reservation not refunded. Unused32compile/32native/32physical/1024cycle/7setup counters do not authorize restart/reset/newprofile. No code/labels/flags/caps changed, no rerun or outside smoke/version diagnostic.

E01 exact handoff `{rel(PHASE / 'phase.json')}` / `snapshot-manifest.json`; report `{rel(PHASE / 'report.md')}`; per-QC, tool/version unknowns, original logs/receipts/pool/commands/costs and hashes retained. OldR01/R02/P10/P10B/G0/frozen checker/scores/unknowns and original document bodies preserved. P10B accepted pre-execution repairs, not this failed execution. Hallmark reuse/read hash and applicable critique organization recorded; no UI scripts or correctness claim.

Next: coordinator sends exact saved E01 to existing P11 for read-only evidence/RTL/math review,0 extra compile/native/physical jobs. Stop here; no pool reset, repair-profile, G2–G5, API/count/generation/Claude/key/network/install/delete/commit/push or newagent/chat. No new conclusion about C, realDUT/oracle/monitor soundness,128completion or old74 witnesses; prior scientific/billing/P04/P05/P06/P05-N1/F1/H1/H2/L1 limits remain. Older pending/permission entries below retain their historical stage scope.
'''
shared = {}
for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
    path = ROOT / 'docs' / name
    original = path.read_bytes()
    saved = PHASE / 'before/docs' / name
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_bytes(original)
    header, body = original.split(b'\n', 1)
    path.write_bytes(header + section.encode() + body)
    assert path.read_bytes().endswith(body)
    shared[rel(path)] = dict(before_sha256=hashlib.sha256(original).hexdigest(),
                            after_sha256=sha(path), old_body_preserved_verbatim=True)
assert all(sha(ROOT / path) == expected for path, expected in protected.items())
write(PHASE / 'git-status-after.json', dict(head=git('rev-parse', 'HEAD'),
    branch=git('branch', '--show-current'), worktree=git('status', '--porcelain=v1', '--untracked-files=normal')))
write(PHASE / 'phase.json', dict(phase='G1_E01_SINGLE_AUTHORIZED_EXECUTION',
    project_date='2026-11-06 America/New_York', status='EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW',
    outcome=summary['execution_outcome'], actual_HEAD=git('rev-parse', 'HEAD')['stdout'].strip(),
    execute_receipt=rel(RECEIPT), execute_receipt_sha256=sha(RECEIPT),
    P10B_review_sha256=sha(P10B / 'review.json'),
    R02_phase_sha256=sha(R02 / 'phase.json'), R02_manifest_sha256=sha(R02 / 'snapshot-manifest.json'),
    registration_sha256=sha(REG), source_manifest_sha256=sha(ROOT / reg['source_manifest']),
    user_grant_sha256=reg['user_authorization_sha256'], runner_exit_code=1,
    pool_path=rel(POOL), pool_sha256=sha(POOL), pool_halted=True, pool_completed=True,
    summary_sha256=sha(PHASE / 'execution-summary.json'), per_QC_sha256=sha(PHASE / 'per-qc.json'),
    actual_reserved=pool['reserved'], job_status_counts=dict(statuses), timing=window,
    source_profile_changed=False, retries=0, API_count_generation_Claude_key_network_install_delete_commit_push=0,
    new_agent_or_chat=0, old_protected_files_verified=len(protected), protected_mismatches=[],
    shared_document_changes=shared,
    postexecution_metadata_elapsed=dict(full_analysis_turn_seconds=None,
        knownness='NOT_INSTRUMENTED_FROM_TURN_ENTRY_NOT_ZERO',
        sealing_script_seconds_through_phase=time.monotonic()-metadata_started,
        scope='Saved-evidence metadata stage after runner results finalized; not extra qualification jobs'),
    independent_result_acceptance='PENDING_P11_NOT_SELF_ACCEPTED',
    snapshot_manifest=rel(PHASE / 'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase;phase names successor manifest without its hash',
    next_action='STOP_EXISTING_P11_SAVED_EVIDENCE_REVIEW_ONLY_NO_NEW_TOOL_BUDGET'))
snapshot = PHASE / 'snapshot'
snapshot.mkdir()
for source_dir in [ROOT / 'test2/g1_v2', OUT]:
    dest = snapshot / rel(source_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, dest, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
for path in [REG, RECEIPT, ROOT / reg['user_authorization'], POOL,
             R02 / 'phase.json', R02 / 'snapshot-manifest.json',
             P10B / 'review.json', P10B / 'review.md', ROOT / 'docs/HANDOFF.md', ROOT / 'docs/PROJECT_STATUS.md']:
    dest = snapshot / rel(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)
for name in ['evidence-manifest.json', 'snapshot-manifest.json', 'phase-packet.json']:
    path = P10B / name
    if path.exists():
        dest = snapshot / rel(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
files = {str(path.relative_to(PHASE)): sha(path) for path in PHASE.rglob('*')
         if path.is_file() and '__pycache__' not in path.parts}
write(PHASE / 'snapshot-manifest.json', dict(status='EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW',
    files=files, file_count=len(files), symlinks={},
    excluded=['snapshot-manifest.json(self-hash)', '__pycache__']))
assert all(sha(PHASE / path) == expected for path, expected in files.items())
print(json.dumps(dict(phase=rel(PHASE / 'phase.json'), phase_sha256=sha(PHASE / 'phase.json'),
    manifest=rel(PHASE / 'snapshot-manifest.json'), manifest_sha256=sha(PHASE / 'snapshot-manifest.json'),
    snapshot_files=len(files), old_protected_files_verified=len(protected),
    outcome=summary['execution_outcome'], setup_reserved=1,
    compile_native_physical_jobs=0, pending_review='P11'), indent=2))
