"""Seal R03 metadata/saved mocks only. Never dispatch a real G1 job."""
from pathlib import Path
from collections import Counter
import ast
import hashlib
import json
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
AUDIT = Path(__file__).resolve().parent
OLD = ROOT / 'test2/g1_v2'
NEW = ROOT / 'test2/g1_v3'
RESULT = ROOT / 'test2/results/g1-qualification-v3'
REG = ROOT / 'test2/configs/g1_qualification_registration_v3.json'
P11 = ROOT / 'docs/audits/agent_bridge_2026-11-06/P11_g1_execution'
STATUS = 'PREPARED_PENDING_P12_INCREMENTAL_REVIEW'


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


def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT)


def git_state():
    index = git('ls-files', '--stage', '-z')
    staged = git('diff', '--cached', '--name-only', '-z')
    status = git('status', '--porcelain=v1', '--untracked-files=normal').decode().splitlines()
    return dict(actual_HEAD=git('rev-parse', 'HEAD').decode().strip(),
        branch=git('branch', '--show-current').decode().strip(),
        index_entries_sha256=hashlib.sha256(index).hexdigest(),
        index_entries=len(index.split(b'\0')) - 1,
        staged_changed_paths_count=len(staged.split(b'\0')) - 1,
        worktree_status_counts=dict(Counter(line[:2] for line in status)),
        note='Read-only Git metadata;no index or branch mutation. Counts include user work.')


assert not (AUDIT / 'phase.json').exists()
assert not (AUDIT / 'snapshot-manifest.json').exists()
assert not (NEW / 'source-manifest.json').exists()
baseline = read(AUDIT / 'preservation-before.json')
protected = baseline['files']
assert all(sha(ROOT / name) == expected for name, expected in protected.items())
before_git = git_state()
assert before_git['index_entries_sha256'] == baseline['git_index_entries_sha256']
assert before_git['index_entries'] == baseline['git_index_entries']
assert before_git['staged_changed_paths_count'] == baseline['staged_changed_paths_count']
write(AUDIT / 'git-status-before-seal.json', before_git)
reg = read(REG)
for field in ['pool_state', 'attempt_lock']:
    assert not (ROOT / reg[field]).exists(), field
assert not (RESULT / 'build').exists()
prior_reg = read(ROOT / 'test2/configs/g1_qualification_registration_v2.json')
for key in ['caps', 'profile', 'native_depth', 'user_authorization', 'user_authorization_sha256']:
    assert reg[key] == prior_reg[key], key
for name, tool in reg['tools'].items():
    for key in ['configured', 'resolved', 'resolved_sha256', 'version_argv']:
        assert tool[key] == prior_reg['tools'][name][key], (name, key)
semantic = read(ROOT / 'docs/audits/producer_test2_g1_R02_2026-11-05/change-and-evidence-map.json')['unchanged_semantic_input_sha256']
assert len(semantic) == 24
assert all(sha(OLD / name) == sha(NEW / name) == expected for name, expected in semantic.items())
assert sha(OLD / 'observations.py') == sha(NEW / 'observations.py')
for path in (OLD / 'inputs/p10-regressions').iterdir():
    assert sha(path) == sha(NEW / 'inputs/p10-regressions' / path.name)
plan = read(NEW / 'job-plan.json')
old_plan = read(OLD / 'job-plan.json')
old_plan['jobs'] = [job for job in old_plan['jobs'] if job['id'] != 'setup-make']
assert json.dumps(plan).replace('/g1_v3/', '/g1_v2/') == json.dumps(old_plan)
assert Counter(job['kind'] for job in plan['jobs']) == dict(setup=7, compile=18, native=32, physical=32)
assert sum(job.get('cycles', 0) for job in plan['jobs']) == 128
for source in NEW.glob('*.py'):
    ast.parse(source.read_text(), filename=rel(source))

# Metadata-only final contract validation. These modules dispatch no tools.
sys.path.insert(0, str(NEW))
from allocation import load_allocation
from continuation_contracts import registration_contract
allocation = load_allocation(ROOT, reg)
registration_contract(ROOT, reg, read(ROOT / reg['user_authorization']), plan)

suites = []
for name, count, failures, receipt in [
    ('continuation-attempt1', 27, 0, '2deeba'),
    ('continuation-attempt2', 28, 1, None),
    ('continuation-attempt3', 28, 0, '30cf8e'),
    ('deadline-horizon-attempt1', 14, 0, '566dda'),
    ('deadline-horizon-attempt2', 14, 0, 'aa8839')]:
    folder = RESULT / name
    summary = read(folder / 'summary.json')
    assert (summary['tests'], summary['failures'], summary['errors']) == (count, failures, 0)
    assert summary['passed'] == (failures == 0)
    for file, expected in summary['source_sha256'].items():
        assert sha(folder / 'executed-source' / file) == expected
        if name in ['continuation-attempt3', 'deadline-horizon-attempt2']:
            assert sha(NEW / file) == expected
    cases = sorted(folder.glob('test_*'))
    assert len(cases) == count
    input_count = 0
    for case in cases:
        assert (case / 'result.json').is_file()
        bindings = read(case / 'input-bindings.json')
        for file, expected in bindings.items():
            assert sha(case / 'inputs' / file) == expected
            input_count += 1
    entrypoint = 'continuation_tests.py' if name.startswith('continuation') else 'regression_tests.py'
    suites.append(dict(path=rel(folder), command=['PYTHONDONTWRITEBYTECODE=1', '.venv/bin/python',
        rel(NEW / entrypoint), '--record', rel(folder)], summary_sha256=sha(folder / 'summary.json'),
        log_sha256=sha(folder / 'unittest.log'), tests=count, failures=failures, errors=0,
        seconds=summary['seconds'], final_source=name in ['continuation-attempt3', 'deadline-horizon-attempt2'],
        tool_receipt=receipt, recorded_exit_code=(0 if receipt else None),
        expected_exit_from_saved_entrypoint=(1 if failures else 0),
        exit_capture_note=('Original tool output truncated before context recovery;failure verified from saved summary/log;not rerun.'
                           if receipt is None else 'Observed exec_command completion.'),
        final_mutated_input_files_checked=input_count, source_files_checked=len(summary['source_sha256'])))
assert sum(suite['tests'] for suite in suites) == 111
red = read(RESULT / 'continuation-attempt2/test_28_final_persistence_crossing_cumulative_cap_cannot_pass/result.json')['ledger']
green_case = RESULT / 'continuation-attempt3/test_28_final_persistence_crossing_cumulative_cap_cannot_pass'
green = read(green_case / 'result.json')['ledger']
durable = read(green_case / 'synthetic-ledger.json')
assert red['halted'] is False and green['halted'] is True and durable['halted'] is True
assert durable['completed'] is True and durable['cumulative_charged_window_seconds'] == 1201.0
write(AUDIT / 'test-evidence-summary.json', dict(suites=suites,
    total_pure_case_invocations=111, total_retained_failures=1,
    final_source_tests=42, final_source_failures=0, final_source_errors=0,
    actual_G1_tool_process_signal_sleep_inventory_calls=0,
    final_persistence_red_green=dict(red_halted=False, green_durable_halted=True,
        green_current_elapsed_seconds=1199.0, green_charged_seconds=1201.0,
        reason=durable['halt_reason']),
    limits=['Pure tests,not independent scientific/model samples or native ABI qualification.',
        'Suite sources and final-mutated fixtures are saved;early/red results are never overwritten.',
        'Final registration explanatory prose/schema/README were updated after the final pure suites;executed Python unchanged and final registration/plan contract independently checked metadata-only here.']))

reasons = {
    'allocation.py': 'New exact predecessor/grant/decision loader;prior setup1,actualtime,charge2 and1198s enforced.',
    'continuation_contracts.py': 'New cumulative registration and exact P12 gate;legacy contracts.py retained unchanged/unexecuted.',
    'budget.py': 'Cumulative prior counters and bounded remaining window;exclusive ledger;post-final-persistence cap refusal.',
    'runtime.py': 'No real external inventory;owned PGID/deadline/poll/kill/wait mandatory;optional mocked errors isolated.',
    'runner.py': 'Exact P12 continuation gate/attempt claim;new lineage report and1198s window,not old full quota.',
    'continuation_tests.py': 'New pure inventory/mandatory-failure/cumulative-lineage/gate/final-persist regressions.',
    'regression_tests.py': 'Retained P10 pure tests adapted to prior2/current1198/work1193,exact old analytic fixtures.',
    'job-plan.json': 'Path namespace only plus omission ofsetup-make;allother argv/order unchanged.',
    'schema.json': 'New report/ledger schema2,cumulative knownness and owned-inventory limits.',
    'README.md': 'R03 preparation,retained red/green evidence,cumulative caps and realistic OS/science limits.'}
changes = []
for file, reason in reasons.items():
    old = OLD / file
    changes.append(dict(file='test2/g1_v3/' + file,
        before_sha256=sha(old) if old.is_file() else None,
        after_sha256=sha(NEW / file), reason=reason))
changes.append(dict(file=rel(REG), before_sha256=sha(ROOT / 'test2/configs/g1_qualification_registration_v2.json'),
    after_sha256=sha(REG), reason='New R03 namespace/allocation/P12/owned supervision metadata;original caps,pins andsemanticprofile unchanged.'))
write(AUDIT / 'change-and-evidence-map.json', dict(status=STATUS,
    findings=['P11-R1', 'R03_TEST28_FINAL_PERSISTENCE_BOUNDARY'], changes=changes,
    unchanged_semantic_input_sha256=semantic, unchanged_semantic_files=24,
    observations_unchanged_sha256=sha(NEW / 'observations.py'),
    all_native_physical_compile_argv_order_equal_after_path_normalization=True,
    only_removed_job='setup-make', original_caps_and_tool_pins_unchanged=True,
    legacy_contracts_and_mock_tests_unexecuted=True,
    prior_P11_CHANGES_REQUIRED_and_E01_failure_preserved=True,
    test_evidence_summary_sha256=sha(AUDIT / 'test-evidence-summary.json')))
write(AUDIT / 'commands-and-checks.json', dict(
    tests=suites, sealing_command=['PYTHONDONTWRITEBYTECODE=1', '.venv/bin/python', rel(Path(__file__))],
    sealing_scope='Onlymetadata/source/hash/snapshot/Gitreads;noG1 tool execution.',
    final_metadata_registration_contract_checked=True,
    helper_incidents=[
        'README apply_patch delete+add of same target was rejected before mutation;single-file write corrected it.',
        'One optional read helper used a nonexistent regression-case directory name;all actualcase paths enumerated and bindings checked during sealing.'],
    old_tests_or_experiments_rerun=False, actual_G1_jobs=0, paid_API_calls=0,
    git_index_mutations=0, key_access=0, network=0, installs=0,
    runtime_deadline_limits='Mocked observed refusals;no OS hard realtime or complete child-census guarantee.'))

source_inputs = {rel(path): sha(path) for path in sorted(NEW.rglob('*'))
                 if path.is_file() and '__pycache__' not in path.parts}
bound_old = [ROOT / reg[key] for key in ['user_authorization', 'continuation_decision',
             'predecessor_pool', 'predecessor_phase', 'predecessor_review']]
bound_old += [P11 / 'review.md', P11 / 'evidence-manifest.json']
for path in [REG, AUDIT / 'P12-review-checklist.md', *bound_old]:
    source_inputs[rel(path)] = sha(path)
write(NEW / 'source-manifest.json', dict(kind='G1_R03_CUMULATIVE_CONTINUATION_PREPARATION_INPUTS',
    files=source_inputs, semantic_profile=reg['profile'], new_executed_profile=False,
    predecessor_E01='HALTED_ERROR_89NOT_RUN_16QC_NOT_RUN_UNCHANGED',
    prior_review='P11_CHANGES_REQUIRED_RETAINED', independent_review='PENDING_P12',
    waveform_policy='Copied P10 analytic fixtures only;no actual R03 native/physical waveform generated.',
    mutable_shared_docs_excluded=True))

section = '''

## Current G1 continuation preparation — R03 / pending P12 (2026-11-06)

R03 **PREPARED_PENDING_P12_INCREMENTAL_REVIEW**. The new hash-bound continuation decision routes one reasonable retry within the original grant; it adds no budget/permissions and supersedes old one-attempt stop wording only for this accounted continuation. E01/P11 remain unchanged: ERROR/89NOT_RUN/16QC NOT_RUN, version/root exit UNKNOWN, old pool halted/completed. No R03 real job/pool/attempt-lock has started.

New `test2/g1_v3/` separates optional inventory from mandatory owned PID/PGID/poll/wait/killpg/deadline protection; registered path never calls ps. External inventory remains known-unavailable/complete=false, not a child census. Cumulative ledger inherits E01 setup1 and actual0.045724458s separately from conservative charge2s; current max1198s/work1193s, setup7. Original32compile/32native/32physical/1024cycles/1200s and stricter setup8 caps stay. Only setup-make is skipped, version explicitly NOT_REPROBED;18SV/all24 semantic-reference materials and normalized native/physical/compile flags/order unchanged.

Saved pure tests: initial27PASS; added final-persist control28tests/1FAIL preserved; repaired final28/28PASS(0.039479s), retained deadline/horizon final14/14PASS(0.023108s). Final save crossing now durably halts; known overruns fail, no OS absolute realtime guarantee. Exact executed sources/final-mutated fixtures retained. These111 case invocations/one retained failure are not scientific samples or real G1 qualification. Prior G1/tests/experiments/companion audits were not rerun.

Exact package `docs/audits/producer_test2_g1_R03_2026-11-06/phase.json` / `snapshot-manifest.json`; source `test2/g1_v3/source-manifest.json`; registration `test2/configs/g1_qualification_registration_v3.json`. Coordinator next sends existing P12 for incremental review; gate requires exact new manifest/registration/decision and later coordinator EXECUTE, not old P10/P11 receipts. Stop at P12 checkpoint; same-grant routing needs no repeated user/key request.0 real R03 setup/compile/native/physical/ps/API/key/network/install/delete/index/commit/push/newagent/chat. Hallmark applicability is recorded,not RTL proof. All old scores/unknowns/timeouts,QC exclusions,128completion/74witness/C-benefit/billing/P04/P05/P06/P05-N1/F1/H1/H2/L1 limits remain. Full old document bodies preserved below.
'''
shared = {}
for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
    path = ROOT / 'docs' / name
    original = path.read_bytes()
    saved = AUDIT / 'before/docs' / name
    saved.parent.mkdir(parents=True, exist_ok=True)
    with saved.open('xb') as stream:
        stream.write(original)
    header, body = original.split(b'\n', 1)
    path.write_bytes(header + section.encode() + body)
    assert path.read_bytes() == header + section.encode() + body
    shared[name] = dict(before_sha256=sha(saved), after_sha256=sha(path),
        old_header_preserved=True, entire_old_body_sha256=hashlib.sha256(body).hexdigest(),
        entire_old_body_retained_exactly=True)

after_git = git_state()
assert after_git['index_entries_sha256'] == baseline['git_index_entries_sha256']
assert after_git['staged_changed_paths_count'] == baseline['staged_changed_paths_count']
assert all(sha(ROOT / name) == expected for name, expected in protected.items())
for field in ['pool_state', 'attempt_lock']:
    assert not (ROOT / reg[field]).exists()
write(AUDIT / 'git-status-after-seal.json', after_git)
write(AUDIT / 'preservation-checks.json', dict(protected_files_checked=len(protected),
    protected_hash_mismatches=[], baseline_sha256=sha(AUDIT / 'preservation-before.json'),
    original_E01_pool_sha256=sha(ROOT / reg['predecessor_pool']),
    old_pool_immutable=True, semantic_files_checked=24, semantic_hash_mismatches=[],
    index_entries_sha256=after_git['index_entries_sha256'], index_unchanged=True,
    index_entries=after_git['index_entries'], staged_changed_paths_count=after_git['staged_changed_paths_count'],
    initial_user_9996_vs_observed_10000='Observed10000 stagedchangedpaths;noindex reconciliation/mutation.',
    shared_document_additions=shared, real_R03_pool_created=False, real_attempt_lock_created=False,
    final_tested_python_sources_match=True))
elapsed = dict(full_turn_wall_seconds=None, full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',
    partial_namespace_authoring_span_seconds=time.time() - baseline['prepared_namespace_epoch'],
    partial_span_scope='From recorded R03 namespace baseline through sealing;includes idle/context recovery;not controlled execution spend.',
    current_controlled_G1_execution_window_seconds=0,
    independent_review_elapsed_seconds=None, independent_review='PENDING_P12_NOT_MEASURED')
write(AUDIT / 'phase.json', dict(phase='G1_R03_CUMULATIVE_CONTINUATION_REPAIR_PREPARATION',
    status=STATUS, actual_HEAD=after_git['actual_HEAD'], branch=after_git['branch'],
    registration=rel(REG), registration_sha256=sha(REG),
    source_manifest=rel(NEW / 'source-manifest.json'), source_manifest_sha256=sha(NEW / 'source-manifest.json'),
    original_user_grant=reg['user_authorization'], original_user_grant_sha256=reg['user_authorization_sha256'],
    continuation_decision=reg['continuation_decision'], continuation_decision_sha256=reg['continuation_decision_sha256'],
    predecessor_pool=reg['predecessor_pool'], predecessor_pool_sha256=reg['predecessor_pool_sha256'],
    predecessor_phase=reg['predecessor_phase'], predecessor_phase_sha256=reg['predecessor_phase_sha256'],
    predecessor_review=reg['predecessor_review'], predecessor_review_sha256=reg['predecessor_review_sha256'],
    predecessor_review_evidence_manifest_sha256=sha(P11 / 'evidence-manifest.json'),
    addressed_findings=['P11-R1', 'R03_TEST28_FINAL_PERSISTENCE_BOUNDARY'],
    independent_acceptance='PENDING_P12_NOT_SELF_ACCEPTED',
    original_cumulative_caps=reg['caps'], native_depth=8, prior_reserved=reg['prior_reserved'],
    prior_actual_window_seconds=allocation.prior_actual_seconds,
    prior_wall_charge_seconds=allocation.prior_charge_seconds, prior_charge_is_not_actual_spend=True,
    attempt_maximum_window_seconds=1198, work_cutoff_seconds=1193,
    remaining_allocation=reg['remaining_allocation'], planned_jobs=reg['planned_jobs'],
    process_supervision='owned_process_group_only', external_inventory='KNOWN_UNAVAILABLE_NOT_ATTEMPTED_NO_PS',
    real_pool_created=False, real_attempt_lock_created=False,
    unchanged_semantic_files=24, normalized_job_changes='Onlyremove setup-make;remaining argv/order/pathnormalization verified.',
    change_map_sha256=sha(AUDIT / 'change-and-evidence-map.json'),
    test_evidence_summary_sha256=sha(AUDIT / 'test-evidence-summary.json'),
    final_pure_tests=42, final_pure_failures=0, all_saved_pure_case_invocations=111, retained_test_failures=1,
    actual_R03_resources={name: 0 for name in ['setup_version', 'compile', 'native_BMC_cover',
        'physical_simulation', 'physical_cycles', 'real_G1_tool_child', 'real_runtime_signal_sleep_inventory',
        'API', 'count', 'generation', 'Claude', 'key_access', 'network', 'installation',
        'deletion', 'git_index_mutation', 'commit', 'push', 'new_agent', 'new_chat']},
    actual_native_waveforms='NOT_GENERATED;analytic P10 fixtures only',
    protected_files_checked=len(protected), protected_hash_mismatches=[],
    index_entries_sha256=after_git['index_entries_sha256'], staged_changed_paths_count=after_git['staged_changed_paths_count'],
    shared_old_document_bodies_retained=True, elapsed=elapsed,
    hallmark_usage_sha256=sha(AUDIT / 'hallmark-usage.json'),
    limits=['Producer pure mocks only;P12/native ABI/real protected process lifecycle unqualified.',
        'No complete child census or OS hard realtime guarantee;observed overrun fails.',
        'All historical scientific/unknown/timeouts/scores/billing and128-cycle/four-state exclusions retained.'],
    snapshot_manifest=rel(AUDIT / 'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase;phase names successor manifest without its hash.',
    next_action='STOP_FOR_EXISTING_P12_INCREMENTAL_REVIEW;COORDINATOR_EXACT_EXECUTE_AFTER_ACCEPTANCE_UNDER_SAME_CUMULATIVE_GRANT'))

# Snapshot exact new sources/results and the bounded immutable lineage, not long logs.
snapshot = AUDIT / 'snapshot'
snapshot.mkdir()
copies = [*NEW.rglob('*'), REG, *RESULT.rglob('*'), *bound_old,
          ROOT / 'docs/HANDOFF.md', ROOT / 'docs/PROJECT_STATUS.md',
          ROOT / 'AGENTS.md', ROOT / 'test2/AGENTS.md',
          ROOT / 'docs/EXPERIMENT_PROTOCOL.md', ROOT / 'docs/DECISIONS.md']
for source in copies:
    if not source.is_file() or '__pycache__' in source.parts:
        continue
    assert not source.is_symlink(), source
    target = snapshot / rel(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert sha(target) == sha(source)
    else:
        shutil.copy2(source, target)
files = {}
symlinks = {}
for path in sorted(AUDIT.rglob('*')):
    if path.is_symlink():
        symlinks[path.relative_to(AUDIT).as_posix()] = str(path.readlink())
    elif path.is_file() and '__pycache__' not in path.parts:
        files[path.relative_to(AUDIT).as_posix()] = sha(path)
write(AUDIT / 'snapshot-manifest.json', dict(status=STATUS, files=files,
    file_count=len(files), symlinks=symlinks,
    excluded=['snapshot-manifest.json(self-hash)', '__pycache__'],
    scope='Exact R03 source/registration/all saved pure evidence plus bounded lineage/sharedbefore-current snapshots.'))
print(json.dumps(dict(status=STATUS, phase_sha256=sha(AUDIT / 'phase.json'),
    snapshot_manifest_sha256=sha(AUDIT / 'snapshot-manifest.json'), registration_sha256=sha(REG),
    source_manifest_sha256=sha(NEW / 'source-manifest.json'), files=len(files),
    final_tests=42, failures=0, retained_red_failures=1, protected_files=len(protected),
    old_pool_unchanged=True, index_unchanged=True, real_G1_jobs=0), indent=2))
