"""Record existing P08/P09 decisions. Metadata and hashes only, no test imports."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CLOSE = Path(__file__).resolve().parent
I01 = ROOT / 'docs/audits/producer_test2_g0_I01_2026-11-05'
BRIDGE = ROOT / 'docs/audits/agent_bridge_2026-11-06'
P08 = BRIDGE / 'P08_g0_design'
P08A = BRIDGE / 'P08a_context_checkpoint'
P09 = BRIDGE / 'P09_g0_implementation'


def sha(path):
    assert not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    with path.open('x') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def rel(path):
    return str(path.relative_to(ROOT))


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                            text=True, check=True)
    return {'argv': ['git', *args], 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


assert not (CLOSE / 'closure.json').exists()
before_git = {'HEAD': git('rev-parse', 'HEAD'),
              'branch': git('branch', '--show-current'),
              'worktree': git('status', '--porcelain=v1', '--untracked-files=normal')}
write(CLOSE / 'git-status-before.json', before_git)
inputs = read(I01 / 'scope.json')['protected_sha256'].copy()
inputs.update({
    rel(I01 / 'phase.json'): '0b6b49b4ca1ae4ea55d172d08e6d8d5f3b90eb26b5ff44ca24a023c4ff5a5bbe',
    rel(I01 / 'snapshot-manifest.json'): 'c49c8c409757322fe49c28142f77cad133fdf9407256e3dcb96ac3ffa2869eb6',
    rel(P08 / 'review.json'): 'f93d6fb191c851a6457318869521a10ac4a987946aeb95dffe098383625ea6ef',
    rel(P09 / 'review.json'): 'af863e7f8e5ca4d012a773a7d2a1f16736cf85cc08500f9ece45d0784b415850',
    rel(P09 / 'review.md'): 'f8dbd9ae11bb3590b8164641724528c4722e6974fcb6a32e2917723edd3e1a61',
    rel(P09 / 'evidence-manifest.json'): '01df254c3b1ea5bee0fe56251777a34e5d25583dfd2d698f27ee4e2055df1f4e',
    rel(P09 / 'snapshot-manifest.json'): 'fabdb3c34bda22c0862df0cdc37e9ba003b069849e15a27b1067b1d0a32e3232'})
review_metadata = []
for folder in [P08, P08A, P09]:
    manifest = folder / 'snapshot-manifest.json'
    inputs.setdefault(rel(manifest), sha(manifest))
    review_metadata.append(manifest)
    for name, expected in read(manifest)['files'].items():
        path = folder / name
        inputs.setdefault(rel(path), expected)
        assert inputs[rel(path)] == expected
        if name != 'thread-observation.json':
            review_metadata.append(path)
assert all(sha(ROOT / path) == expected for path, expected in inputs.items())
phase = read(I01 / 'phase.json')
review = read(P09 / 'review.json')
assert read(P08 / 'review.json')['status'] == review['status'] == 'PASS_WITH_LIMITS'
assert not review['findings'] and not review['blocking_findings']
assert not review['nonblocking_improvements']
assert review['input_identity']['producer_phase_sha256'] == sha(I01 / 'phase.json')
assert review['input_identity']['producer_manifest_sha256'] == sha(I01 / 'snapshot-manifest.json')
assert review['input_identity']['source_sha256'] == phase['source_sha256']
for path, expected in phase['source_sha256'].items():
    inputs[path] = expected
    assert sha(ROOT / path) == expected
for path in ['coverage_map', 'support_matrix']:
    source = ROOT / (phase['coverage_map'] if path == 'coverage_map'
                     else 'test2/g0_v1/support-matrix.json')
    assert sha(source) == phase[path + '_sha256']
    inputs[rel(source)] = sha(source)
for name in ['scope.json', 'evidence-checks.json', 'commands.json',
             'authorization.json', 'input-provenance.json']:
    inputs[rel(I01 / name)] = sha(I01 / name)
receipt_paths = {'saved_byte_replay_sha256': P09 / 'saved-byte-replay.json',
                 'CLI_receipt_sha256': P09 / 'cli-controls.json',
                 'fresh_suite_summary_sha256': P09 / 'fresh-suite/summary.json'}
for field, path in receipt_paths.items():
    assert sha(path) == review[field]
    inputs[rel(path)] = sha(path)
write(CLOSE / 'input-manifest.json', {
    'scope': 'Metadata identities and selected protected files freshly hashed; no tests/audits executed',
    'files': inputs,
    'old_protected_source_count': len(read(I01 / 'scope.json')['protected_sha256']),
    'P09_evidence_2279_files_2_link_texts': 'Coordinator verification reused; manifest identity checked here, content suite not re-audited',
    'I01_8695_files_6_link_texts': 'Exact prior seal/P09 verification reused; manifest identity checked here, not all contents rehashed',
    'all_4837_old_freeze_contents_rehashed': False})
out = ROOT / 'test2/results/g0-adapter-acceptance-p09-v1'
version = 1
while out.exists():
    version += 1
    out = ROOT / f'test2/results/g0-adapter-acceptance-p09-v{version}'
out.mkdir()
sidecar = out / 'independent-acceptance.json'
accounting = deepcopy(review['test_accounting'])
acceptance = {
    'record_kind': 'RECORD_OF_EXISTING_INDEPENDENT_ACCEPTANCE_NOT_NEW_SELF_ACCEPTANCE',
    'status': 'PASS_WITH_LIMITS', 'maintenance_stage_complete': True,
    'project_date': '2026-11-05 America/New_York',
    'D01_design_acceptance': {'review': rel(P08 / 'review.json'),
         'review_sha256': sha(P08 / 'review.json'),
         'review_md_sha256': sha(P08 / 'review.md'),
         'identity_manifest_sha256': sha(P08 / 'snapshot-manifest.json'),
         'decision': 'PASS_WITH_LIMITS', 'scope': 'Frozen D01 paper design only; not code or execution authorization'},
    'I01_implementation_acceptance': {'review': rel(P09 / 'review.json'),
         'review_sha256': sha(P09 / 'review.json'),
         'review_md_sha256': sha(P09 / 'review.md'),
         'evidence_manifest_sha256': sha(P09 / 'evidence-manifest.json'),
         'identity_manifest_sha256': sha(P09 / 'snapshot-manifest.json'),
         'decision': 'PASS_WITH_LIMITS',
         'scope': 'Exact I01 version only: origin=SYNTHETIC_FIXTURE, explicit identities, strict serial closed-shapes JSON/text metadata'},
    'P08a': {'scope': 'Context checkpoint only; not acceptance of implementation/science',
         'review_sha256': sha(P08A / 'review.json'),
         'identity_manifest_sha256': sha(P08A / 'snapshot-manifest.json')},
    'producer_phase': rel(I01 / 'phase.json'), 'producer_phase_sha256': sha(I01 / 'phase.json'),
    'producer_manifest': rel(I01 / 'snapshot-manifest.json'),
    'producer_manifest_sha256': sha(I01 / 'snapshot-manifest.json'),
    'source_sha256': phase['source_sha256'],
    'coverage_map': phase['coverage_map'], 'coverage_map_sha256': phase['coverage_map_sha256'],
    'support_matrix': 'test2/g0_v1/support-matrix.json',
    'support_matrix_sha256': phase['support_matrix_sha256'],
    'related_input_sha256': inputs,
    'independent_validation_accounting': accounting,
    'accounting_boundary': 'Separate categories, all executed earlier by P09; no new executions in C01. Producer six-suite history was not rerun as six suites and is not independent model/science sampling. Historical producer independent_acceptance=false is stage-time metadata, not current acceptance status.',
    'P08_N1': {'status': 'EXACT_I01_BEHAVIOR_ACCEPTED_USING_NEW_P09_PROBES',
         'evidence': '12 independent combinations: count/generation x retry/round/session x missing-terminal/matching-error;6 missing-terminal continuations REJECT,6 matching-error continuations retain UNRESOLVED/unknown costs',
         'producer_dedicated_combinations_at_I01_seal': 'NOT_SAVED; unchanged historical disclosure',
         'frozen_D01_or_I01_rewritten': False},
    'reviewer_harness_incidents': deepcopy(review['reviewer_harness_incidents']),
    'science': 'NOT_EVALUATED',
    'provider_invoice': {'knownness': 'UNKNOWN', 'value': None},
    'count_fees': {'knownness': 'UNKNOWN', 'value': None},
    'limitations': deepcopy(review['limitations']),
    'future_permissions': {k: False for k in ['G1', 'native', 'API', 'new_data',
         'count', 'generation', 'paid', 'live', 'key_access']},
    'future_paid_stage_requirement': 'Concrete service/purpose/model/request/token/fee/time caps and safe configuration, then specific user authorization; no key request now',
    'closure_path': rel(CLOSE / 'closure.json')}
write(sidecar, acceptance)
shared = {}
section = f'''

## Current acceptance closure — G0 P08/P09 / C01 (2026-11-05)

G0 implementation/review maintenance is **COMPLETE_WITH_LIMITS**. P08 accepted frozen D01 paper design only; P09 independently accepted the exact I01 synthetic-metadata adapter **PASS_WITH_LIMITS**, with no new finding/blocker. Identity/scope sidecar: `{rel(sidecar)}`; metadata closure: `{rel(CLOSE / 'closure.json')}`. Original D01/I01 PENDING records and all sealed files remain unchanged as stage-time history.

P09 evidence, not C01 executions: fresh final93 tests PASS;469 exact saved-byte case statuses reproduced with0 mismatch and original8 failures retained;28 independent probes and6 CLI controls matched expectations. Six FileNotFoundError absolute paths were explicitly normalized after snapshot relocation; excluding timing,0 unexplained result differences. P08-N1 combination evidence comes from P09's12 new probes, not producer tests retrospectively added. P09 mapping KeyError is a retained review-harness incident, not a product failure. Producer raw PTY receipt limitation remains. Counts are separate validation categories, not independent model trials/science samples.

Accepted scope remains origin=SYNTHETIC_FIXTURE, explicit identities, strict serial closed-shapes JSON/text metadata only. No real/legacy-run gate, authenticated authorization/provider provenance or concurrency support; no real VCD/literal/PREPOST/rows/HEX/MON parser, independent labels or scientific qualification. Science stays NOT_EVALUATED; invoice/count fees UNKNOWN. P04 exact-v1 REJECT/serialization-cause UNKNOWN, P05/P06 exact-format/cohort limits, P05-N1 backlog, F1/selected-sample/category/128completion/H1/H2/L1 remain open.

C01 performs metadata/hash checks only:0 tests/companion audits/API/count/native/DUT/formal/monitor/oracle/key/service calls; no code changes, install, deletion, commit or push. Current HEAD independently checked `{before_git['HEAD']['stdout'].strip()}`; dirty work preserved. G1/newdata/API/paid/live remain unauthorized. Stop after this closure; await a specifically authorized concrete future stage, without requesting keys now. Older entries below are preserved verbatim and superseded only within this exact acceptance scope.
'''
for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
    source = ROOT / 'docs' / name
    original = source.read_bytes()
    saved = CLOSE / 'before/docs' / name
    saved.parent.mkdir(parents=True, exist_ok=True)
    assert not saved.exists()
    saved.write_bytes(original)
    first, rest = original.split(b'\n', 1)
    source.write_bytes(first + section.encode() + rest)
    assert source.read_bytes().endswith(rest)
    shared[rel(source)] = {'before_sha256': hashlib.sha256(original).hexdigest(),
         'after_sha256': sha(source), 'old_body_preserved_verbatim': True,
         'before_copy': str(saved.relative_to(CLOSE))}
assert all(sha(ROOT / path) == expected for path, expected in inputs.items())
after_git = {'HEAD': git('rev-parse', 'HEAD'), 'branch': git('branch', '--show-current'),
             'worktree': git('status', '--porcelain=v1', '--untracked-files=normal')}
assert before_git['HEAD']['stdout'] == after_git['HEAD']['stdout']
write(CLOSE / 'git-status-after.json', after_git)
closure = {'phase': 'C01_G0_ACCEPTANCE_METADATA_CLOSURE',
    'status': 'MAINTENANCE_COMPLETE_WITH_LIMITS_NO_NEXT_STAGE_AUTHORIZATION',
    'actual_HEAD': after_git['HEAD']['stdout'].strip(),
    'worktree_records': ['git-status-before.json', 'git-status-after.json'],
    'sidecar': rel(sidecar), 'sidecar_sha256': sha(sidecar),
    'input_manifest': 'input-manifest.json', 'input_manifest_sha256': sha(CLOSE / 'input-manifest.json'),
    'shared_document_changes': shared, 'protected_input_hashes_checked': len(inputs),
    'protected_input_mismatches': [], 'source_test_score_checker_or_old_evidence_edits': 0,
    'execution_counts': {k: 0 for k in ['tests', 'companion_audits', 'experiments',
        'API', 'count', 'generation', 'native', 'DUT_simulation', 'formal',
        'monitor_replay', 'oracle', 'key_access', 'network_services',
        'installation', 'deletion', 'commit', 'push', 'new_agent', 'new_chat']},
    'metadata_writes_authorized_and_performed': True,
    'P09_executions_reused_not_rerun': True,
    'not_claimed': 'No fresh full I01/P09 evidence or4837 old-member content audit during C01; exact sealed identities and selected protected inputs freshly hashed.',
    'snapshot_manifest': 'snapshot-manifest.json',
    'hash_cycle_policy': 'Successor manifest hashes closure and snapshots; closure names it without self-cycle.',
    'next_action': 'Wait; no further implementation, qualification, key request or execution gate.'}
write(CLOSE / 'closure.json', closure)
snapshot = CLOSE / 'snapshot'
snapshot.mkdir()
for source in [sidecar, ROOT / 'docs/HANDOFF.md', ROOT / 'docs/PROJECT_STATUS.md', *review_metadata]:
    dest = snapshot / rel(source)
    if dest.exists():
        assert sha(dest) == sha(source)
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
files = {str(path.relative_to(CLOSE)): sha(path) for path in sorted(CLOSE.rglob('*')) if path.is_file()}
write(CLOSE / 'snapshot-manifest.json', {
    'scope': 'C01 metadata-only closure, pre-update shared bodies and accepted review metadata snapshots',
    'files': files, 'file_count': len(files), 'symlinks': {},
    'excluded': ['snapshot-manifest.json (self hash)']})
assert all(sha(CLOSE / path) == expected for path, expected in files.items())
print(json.dumps({'sidecar': rel(sidecar), 'sidecar_sha256': sha(sidecar),
    'closure': rel(CLOSE / 'closure.json'), 'closure_sha256': sha(CLOSE / 'closure.json'),
    'manifest_sha256': sha(CLOSE / 'snapshot-manifest.json'),
    'metadata_snapshot_files': len(files), 'protected_inputs_checked': len(inputs),
    'new_execution_counts': closure['execution_counts'], 'actual_HEAD': closure['actual_HEAD']}, indent=2))
