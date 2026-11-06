"""R01 metadata/AST/hash sealing. Never imports G1 runner or native tools."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PHASE = Path(__file__).resolve().parent
G1 = ROOT / 'test2/g1_v1'
RESULT = ROOT / 'test2/results/g1-qualification-v1'
REG = ROOT / 'test2/configs/g1_qualification_registration_v1.json'


def sha(path):
    assert not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


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
before = dict(head=git('rev-parse', 'HEAD'), branch=git('branch', '--show-current'),
              worktree=git('status', '--porcelain=v1', '--untracked-files=normal'))
write(PHASE / 'git-status-before.json', before)
protected = read(ROOT / 'docs/audits/producer_test2_g0_C01_2026-11-05/input-manifest.json')['files'].copy()
protected.update({
    'test2/results/g0-adapter-acceptance-p09-v1/independent-acceptance.json':
        '0a13e9a5b8b78efdc900d0e0ad7e7d215bf5700c14b7082b2237164b448fd51c',
    'docs/audits/producer_test2_g0_C01_2026-11-05/closure.json':
        '5a945310d6a35f3e91a403572fde383e57101b6f4576c9a35d8a5197c823495d',
    'docs/audits/producer_test2_g0_C01_2026-11-05/snapshot-manifest.json':
        '9bfc0cdb2763efc538ee637f5452ab00378efbf3a736dee9738b5eeafe46cc2c'})
for name in ['AGENTS.md', 'test2/AGENTS.md', 'docs/EXPERIMENT_PROTOCOL.md',
             'docs/DECISIONS.md']:
    protected[name] = sha(ROOT / name)
assert all(sha(ROOT / f) == digest for f, digest in protected.items())
freeze_checks = []
old = read(ROOT / 'docs/audits/producer_test2_g0_I01_2026-11-05/scope.json')
for freeze in old['freeze_membership']:
    assert sha(ROOT / freeze['path']) == freeze['sha256']
    data = read(ROOT / freeze['path'])
    members = data.get('files', data.get('artifact_sha256'))
    assert len(members) == freeze['member_names']
    conflicts = [p for p in members if p.startswith(('test2/g1_v1/',
        'test2/results/g1-qualification-v1/', rel(PHASE) + '/')) or p == rel(REG)]
    assert not conflicts
    freeze_checks.append(dict(freeze, new_namespace_conflicts=conflicts))
write(PHASE / 'scope-and-preservation.json', dict(
    protected_sha256=protected, protected_mismatches=[],
    freeze_manifest_identities_and_member_names=freeze_checks,
    full_old_4837_or_coordinator_7450_content_audit_rerun=False,
    write_allowlist=['test2/g1_v1/**', rel(REG), rel(RESULT) + '/**',
                     rel(PHASE) + '/**', 'docs/HANDOFF.md top only',
                     'docs/PROJECT_STATUS.md top only']))
reg = read(REG)
grant = ROOT / reg['user_authorization']
assert sha(grant) == reg['user_authorization_sha256']
labels = read(G1 / 'inputs/controls.json')['cases']
assert [c['id'] for c in labels] == [f'QC{i:02}' for i in range(16)]
assert all(c['actual_result'] is None and c['independent_label_status'] == 'PENDING_P10'
           and not c['completion128_credit'] for c in labels)
assert not (RESULT / 'execution-state.json').exists()
assert not (RESULT / 'build').exists()
assert not list(RESULT.rglob('*.vcd'))
for source in G1.glob('*.py'):
    ast.parse(source.read_text(), filename=rel(source))
mock_records = []
for number, count, receipt in [(1, 12, 'ebb225'), (2, 14, 'b38813')]:
    folder = RESULT / f'mock-attempt{number}'
    summary = read(folder / 'summary.json')
    assert summary['tests'] == count and summary['passed'] and summary['failures'] == summary['errors'] == 0
    revision = G1 if number == 2 else PHASE / 'mock-source-revisions/attempt1'
    assert all(sha(revision / name) == value for name, value in summary['source_sha256'].items())
    mock_records.append(dict(command=['PYTHONDONTWRITEBYTECODE=1', '.venv/bin/python',
        'test2/g1_v1/mock_tests.py', '--record', rel(folder)], exit_code=0,
        tool_receipt=receipt, summary_sha256=sha(folder / 'summary.json'),
        scope='MOCK_ONLY_NOT_G1_QUALIFICATION', tests=count,
        actual_setup_compile_native_physical_calls=0))
write(PHASE / 'commands-and-checks.json', dict(
    mock_runs=mock_records, Python_AST_sources_checked=6,
    real_tool_versions_probed=False, real_native_or_physical_run=False,
    preparation_incidents='preparation-incidents.json',
    all_incidents_are_saved_not_reclassified_as_product_or_qualification_failures=True))
inputs = {rel(path): sha(path) for path in G1.rglob('*')
          if path.is_file() and '__pycache__' not in path.parts}
for source in [REG, grant, PHASE / 'P10-review-checklist.md',
               ROOT / 'docs/designs/test2_g0_design_v1/public_controls.md',
               ROOT / 'docs/designs/test2_g0_design_v1/public_controls.index.json',
               ROOT / 'docs/test2_next_qualification_plan_v1.md']:
    inputs[rel(source)] = sha(source)
write(G1 / 'source-manifest.json', dict(
    kind='G1_EXACT_PRETOOL_PROFILE_INPUTS_V1', files=inputs,
    actual_tool_results_available=False, labels='PENDING_P10',
    waveform_SHA_policy='Actual waveform SHA unknown/null before tools; hand-derived observer/input contract hash is frozen, not passed off as a produced waveform'))
section = f'''

## Current G1 preparation — R01, new user grant (2026-11-05)

User separately authorized one public G1 profile under `docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/user-authorization.json`. R01 status **PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW**. New `test2/g1_v1/` contains18SV files,16 hand-derived QC00–QC15 labels/explicit inputs, a profile-specific contract/parser/runner and fixed job plan; new registration `{rel(REG)}`. G0 source/acceptance and every old draft/grant/freeze remain unchanged. Older G1-unapproved prose below is historical and does not cancel this new grant.

Planned shared pool:32 BMC/activation-cover total,depth8/10s;32 dual-simulator runs max32cycles each/1024cycles total/2s;32 compilation jobs/20s;1200s overall starting before actual setup/version/compile/native/physical work through parsing/output. Plan uses18 logical compilation batches(16Yosys+2shared physical builds),32native,32physical/128cycles,8setup queries. Child commands/time are included in root/global costs, PID sampling is best effort; batch-count interpretation is explicitly pending P10 resource review. Single persisted pool, reservations before dispatch, no restart/retry/repair-profile, group cleanup, all failures/NOT_RUN preserved.

R01 actuals: **0 version/setup/native/compile/physical/API/count/generation/key calls**. Final14 purePython budget/refusal mocks PASS; initial12 PASS and exact source revisions preserved. These26 mock case invocations are not G1 qualification or scientific/model samples. One source-history restoration helper failed on separator whitespace; corrected exact SHA identities and incident retained. Actual SV syntax, native raw parser/process lifecycle and simulator ABI remain unexercised. All real QC results and waveforms null/NOT_GENERATED; independent labels PENDING_P10. QC07/15 no vacuous/completion credit; QC12/13 no4state equivalence; QC08/09 delayed native-pre vs physical pre/post separate; QC14 finalpost marker outside DUT/no extra edge. No128/unbounded/realDUT/oracle/old74-witness cause claim.

Hallmark was read with actual SHA/use record at `{rel(PHASE / 'hallmark-usage.json')}` and used for factual material/fixed-input review organization only; no UI scripts or Hallmark correctness pass. Exact R01 `{rel(PHASE / 'phase.json')}` / `snapshot-manifest.json` freeze source, labels, inputs, runner, mocks and grant. Coordinator next sends this fixed package to existing P10 for read-only labels/resource review, then issues EXECUTE under the same G1 grant if accepted. This turn stops at that technical checkpoint; no additional user approval/key request. No G2–G5, API/paid/live, install/delete/commit/push or new chat/agent. All P04/P05/P06/P05-N1/F1/selected-sample/category/128/H1/H2/L1/billing limits and old C-negative results remain.
'''
for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
    path = ROOT / 'docs' / name
    original = path.read_bytes()
    prior = PHASE / 'before/docs' / name
    prior.parent.mkdir(parents=True, exist_ok=True)
    prior.write_bytes(original)
    first, rest = original.split(b'\n', 1)
    path.write_bytes(first + section.encode() + rest)
    assert path.read_bytes().endswith(rest)
assert all(sha(ROOT / f) == digest for f, digest in protected.items())
now = time.time()
created = (G1 / 'sources/common.sv').stat()
source_start = getattr(created, 'st_birthtime', created.st_mtime)
write(PHASE / 'phase.json', dict(
    phase='G1_R01_PREPARATION_AND_REGISTRATION',
    status='PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW',
    actual_HEAD=git('rev-parse', 'HEAD')['stdout'].strip(),
    new_user_authorization=rel(grant), new_user_authorization_sha256=sha(grant),
    registration=rel(REG), registration_sha256=sha(REG),
    source_manifest=rel(G1 / 'source-manifest.json'),
    source_manifest_sha256=sha(G1 / 'source-manifest.json'),
    label_source=rel(G1 / 'inputs/controls.json'), label_sha256=sha(G1 / 'inputs/controls.json'),
    input_sha256=sha(G1 / 'inputs/stimulus.json'),
    expected_waveform_contract_sha256=sha(G1 / 'inputs/expected-waveform-contract.json'),
    actual_waveforms='NOT_GENERATED', native_or_physical_labels='PENDING_P10',
    planned_caps=reg['caps'], planned_jobs=reg['planned_jobs'],
    executed_resources={key: 0 for key in ['tool_version_setup', 'native_BMC_cover',
        'compilation', 'physical_runs', 'physical_cycles', 'API', 'count',
        'generation', 'key_access', 'network', 'install', 'delete', 'commit', 'push']},
    shared_execution_pool_created=False,
    mock_only=dict(final_tests=14, initial_tests=12, failures=0,
                   independent_G1_qualification=False),
    preparation_elapsed=dict(full_read_thinking_authoring_wall_seconds=None,
        full_wall_knownness='NOT_INSTRUMENTED_FROM_TURN_ENTRY_NOT_ZERO',
        recorded_source_authoring_start_epoch=source_start,
        recorded_authoring_interval_through_phase_seconds=now-source_start,
        native1200_second_execution_clock_started=False,
        independent_readonly_review_elapsed='NOT_YET_RUN_BY_P10'),
    Hallmark='hallmark-usage.json;applicability-limited,notRTLqualification',
    open_P10_questions=['Independent correctness of16handmath labels/phase/reset mapping',
        'Acceptability of18logical shared/batch compilation-root accounting and nonexhaustivePID observations under32job cap',
        'Untested native/dualphysical syntax,ABI,VCDsubset and lifecycle;no tool launched to probe them'],
    preservation='scope-and-preservation.json;selected hashes/membernames only,no oldcontent audit or oldcohort rerun',
    API_or_G2_G3_G4_G5_authorized=False,
    snapshot_manifest=rel(PHASE / 'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase; phase names successor manifest without hashing itself',
    next_action='STOP_SAFE_CHECKPOINT_COORDINATOR_SENDS_EXISTING_P10_READONLY_REVIEW_THEN_EXACT_EXECUTE_HANDOFF_UNDER_SAME_GRANT'))
write(PHASE / 'git-status-after.json', dict(head=git('rev-parse', 'HEAD'),
      branch=git('branch', '--show-current'),
      worktree=git('status', '--porcelain=v1', '--untracked-files=normal')))
snapshot = PHASE / 'snapshot'
snapshot.mkdir()
for source in [G1, RESULT]:
    target = snapshot / rel(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
for source in [REG, grant, ROOT / 'docs/HANDOFF.md', ROOT / 'docs/PROJECT_STATUS.md']:
    target = snapshot / rel(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
files = {str(path.relative_to(PHASE)): sha(path) for path in PHASE.rglob('*')
         if path.is_file() and '__pycache__' not in path.parts}
write(PHASE / 'snapshot-manifest.json', dict(
    status='PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW', files=files,
    file_count=len(files), symlinks={}, excluded=['snapshot-manifest.json(self-hash)', '__pycache__']))
assert all(sha(PHASE / f) == value for f, value in files.items())
print(json.dumps(dict(phase=rel(PHASE / 'phase.json'), phase_sha256=sha(PHASE / 'phase.json'),
    manifest=rel(PHASE / 'snapshot-manifest.json'), manifest_sha256=sha(PHASE / 'snapshot-manifest.json'),
    registration_sha256=sha(REG), source_manifest_sha256=sha(G1 / 'source-manifest.json'),
    snapshot_files=len(files), protected_files_checked=len(protected),
    status='PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW', native_runs=0), indent=2))
