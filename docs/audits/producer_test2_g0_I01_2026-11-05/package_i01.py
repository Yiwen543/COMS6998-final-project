"""I01 evidence packaging only. Never imports/runs the adapter or tests."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PHASE = Path(__file__).resolve().parent
RESULT = ROOT / 'test2/results/g0-adapter-i01-v1'
SOURCE = ['test2/g0_v1/adapter.py', 'test2/g0_v1/schema.json',
          'test2/tests/test_g0_adapter_v1.py']


def digest(path):
    assert not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    with path.open('x') as out:
        out.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def rel(path):
    return str(path.relative_to(ROOT))


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                            text=True, check=True)
    return {'argv': ['git', *args], 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def inventory(base):
    files, links = {}, {}
    for folder, dirs, names in os.walk(base, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d != '__pycache__')
        for name in sorted(dirs + names):
            path = Path(folder) / name
            key = str(path.relative_to(base))
            if path.is_symlink():
                target = os.readlink(path)
                links[key] = {'target': target, 'target_text_sha256':
                              hashlib.sha256(target.encode()).hexdigest()}
            elif path.is_file():
                files[key] = digest(path)
    return files, links


def prepare():
    assert not (PHASE / 'evidence-checks.json').exists()
    scope = read(PHASE / 'scope.json')
    protected = scope['protected_sha256']
    assert all(digest(ROOT / p) == sha for p, sha in protected.items())
    freeze_records = []
    for item in scope['freeze_membership']:
        path = ROOT / item['path']
        assert digest(path) == item['sha256']
        data = read(path)
        members = data.get('files', data.get('artifact_sha256'))
        assert len(members) == item['member_names']
        conflicts = [p for p in members if p.startswith(('test2/g0_v1/',
            'test2/results/g0-adapter-i01-v1/', rel(PHASE) + '/'))
            or p in ['test2/tests/test_g0_adapter_v1.py',
                     'docs/HANDOFF.md', 'docs/PROJECT_STATUS.md']]
        assert not conflicts, conflicts
        freeze_records.append(dict(item, write_conflicts=conflicts))
    d01 = ROOT / 'docs/audits/producer_test2_g0_D01_2026-11-05'
    d01_manifest = read(d01 / 'snapshot-manifest.json')
    assert all(digest(d01 / p) == (v if isinstance(v, str) else v['sha256'])
               for p, v in d01_manifest['files'].items())
    p08 = ROOT / 'docs/audits/agent_bridge_2026-11-06/P08_g0_design'
    p08_hashes = {'review.json':
        'f93d6fb191c851a6457318869521a10ac4a987946aeb95dffe098383625ea6ef',
        'review.md':
        '3a8274d713c14e30df61141428bb50118e52d9fce85c92175fbd74caa30b88e1'}
    assert all(digest(p08 / p) == sha for p, sha in p08_hashes.items())
    assert read(p08 / 'review.json')['status'] == 'PASS_WITH_LIMITS'
    suite_history = []
    input_checks = 0
    retained_mismatches = []
    for index in range(1, 7):
        base = RESULT / f'attempt{index}'
        summary = read(base / 'summary.json')
        revision = ROOT if index == 6 else PHASE / 'drafts' / f'attempt{index}'
        for path, field in zip(SOURCE, ['adapter_source_sha256',
                                       'schema_sha256', 'tests_source_sha256']):
            assert digest(revision / path) == summary[field]
        cases = sorted(base.glob('test_*'))
        assert len(cases) == summary['tests'] == summary['fixture_case_directories']
        log = (base / 'unittest.log').read_text()
        assert f"Ran {summary['tests']} tests" in log
        assert ('FAILED (failures=8)' in log if index == 1 else log.rstrip().endswith('OK'))
        assert len(re.findall(r'^FAIL: ', log, re.M)) == summary['failures']
        for case in cases:
            binding = read(case / 'fixture-binding.json')
            result = read(case / 'result.json')
            files, links = inventory(case / 'bundle')
            assert files == binding['input_sha256'], str(case)
            if 'symlinks' in binding:
                assert {p: v['target'] for p, v in links.items()} == binding['symlinks']
            input_checks += len(files)
            assert binding['actual'] == result['integrity']['status']
            assert result['adapter_source_sha256'] == summary['adapter_source_sha256']
            assert result['schema_sha256'] == summary['schema_sha256']
            assert result['scientific_attribution']['status'] == 'NOT_EVALUATED'
            assert not any(result['execution_capabilities'].values())
            if binding['expected'] != binding['actual']:
                retained_mismatches.append({'case': rel(case),
                    'expected': binding['expected'], 'actual': binding['actual']})
        suite_history.append(dict(summary, record_directory=rel(base),
            summary_sha256=digest(base / 'summary.json'),
            unittest_log_sha256=digest(base / 'unittest.log'),
            revision_directory=rel(revision),
            reported_command_argv=['.venv/bin/python',
                'test2/tests/test_g0_adapter_v1.py', '--record', rel(base)],
            reported_exit_code=int(not summary['passed']),
            exit_evidence='Prior producer-turn report plus preserved summary and runner return int(not wasSuccessful()). No separate raw PTY receipt is archived; not rerun here.'))
    assert [x['tests'] for x in suite_history] == [60, 66, 78, 83, 89, 93]
    assert len(retained_mismatches) == 8
    coverage = read(RESULT / 'coverage-map.json')
    assert [c['case_id'] for c in coverage['cases']] == [f'FM{i:02}' for i in range(1, 45)]
    coverage_evidence = 0
    for case in coverage['cases']:
        assert case['scientific_validation'] == 'NOT_EVALUATED'
        for evidence in case['evidence']:
            for field in ['result', 'fixture_binding']:
                assert digest(ROOT / evidence[field]) == evidence[field + '_sha256']
            assert read(ROOT / evidence['result'])['integrity']['status'] == evidence['observed_integrity']
            coverage_evidence += 1
    cli = read(RESULT / 'cli-records.json')
    assert [r['exit_code'] for r in cli['records']] == [0, 2, 1, 1]
    for name, expected in [('pass', 'PASS_WITH_SCOPE'), ('unknown', 'UNRESOLVED'),
                           ('reject', 'REJECT')]:
        assert read(RESULT / f'g0-cli-{name}/result.json')['integrity']['status'] == expected
    last = cli['records'][-1]
    assert last['existing_result_sha256_before'] == last['existing_result_sha256_after'] == digest(RESULT / 'g0-cli-pass/result.json')
    source_hashes = {p: digest(ROOT / p) for p in SOURCE}
    resource = {'scope': 'I01 only; prior local synthetic tests, no science samples',
        'suite_count': 6, 'synthetic_case_invocations': sum(s['tests'] for s in suite_history),
        'suite_wall_seconds_sum': sum(s['seconds'] for s in suite_history),
        'final_suite_seconds': suite_history[-1]['seconds'],
        'memory_peak': None, 'memory_peak_knownness': 'NOT_MEASURED',
        'actual_API_calls': 0, 'actual_count_calls': 0, 'paid_generation_calls': 0,
        'native_jobs': 0, 'DUT_simulations': 0, 'monitor_replays': 0,
        'formal_jobs': 0, 'oracle_executions': 0, 'new_scientific_samples': 0,
        'key_access': 0, 'network_calls': 0, 'installations': 0,
        'note': 'Synthetic count/generation/token fields describe test input records, never provider usage. Fixture result parse_seconds are local validation measurements; invoice/count fees stay UNKNOWN/null.'}
    checks = {'status': 'EVIDENCE_BINDINGS_VERIFIED_NOT_A_TEST_RERUN',
        'source_sha256': source_hashes, 'protected_files_checked': len(protected),
        'protected_mismatches': [], 'freeze_membership': freeze_records,
        'freeze_member_names_total': sum(i['member_names'] for i in freeze_records),
        'all_4837_member_contents_freshly_hashed': False,
        'D01_snapshot_members_checked': len(d01_manifest['files']),
        'coverage_cases': 44, 'coverage_evidence_bindings_checked': coverage_evidence,
        'coverage_status_counts': dict(Counter(c['coverage_status'] for c in coverage['cases'])),
        'synthetic_input_regular_file_hashes_checked': input_checks,
        'preserved_expected_actual_mismatches': retained_mismatches,
        'suite_history': suite_history, 'CLI_records_sha256': digest(RESULT / 'cli-records.json'),
        'P08_review_sha256': {rel(p08 / p): sha for p, sha in p08_hashes.items()},
        'P08_scope': 'D01 paper design only; not I01 implementation acceptance',
        'resources': resource, 'new_test_or_experiment_execution_during_packaging': False}
    write(PHASE / 'evidence-checks.json', checks)
    write(PHASE / 'commands.json', {
        'scope': 'Retained prior implementation invocations; no rerun during packaging',
        'test_commands': [{k: s[k] for k in ['reported_command_argv',
             'reported_exit_code', 'exit_evidence', 'summary_sha256',
             'unittest_log_sha256']} for s in suite_history],
        'CLI_commands': cli['records'],
        'packaging_entrypoint': [sys.executable, rel(Path(__file__)), 'prepare'],
        'packaging_does_not_import_or_execute_adapter_or_tests': True})
    write(PHASE / 'input-provenance.json', {
        'historical_authorization_record_preserved': rel(PHASE / 'authorization.json'),
        'P08_pending_in_that_earlier_record_is_historical': True,
        'current_P08': {'status': 'PASS_WITH_LIMITS_DESIGN_ONLY',
             'sha256': checks['P08_review_sha256']},
        'I01_code_acceptance': 'PENDING_P09',
        'only_fixture_origin': 'PURE_SYNTHETIC_JSON_TEXT_NO_SCIENTIFIC_DATA',
        'no_old_experiment_inputs_used_for_fixture_generation': True,
        'all_intermediate_revisions_and_negative_results_retained': True,
        'symlink_policy': 'Copy link text without dereferencing. Negative-test absolute link targets stay original; snapshot is evidence, not a portable execution bundle.',
        'cache_policy': 'Do not copy __pycache__; do not delete it.',
        'P08_N1': {'assessment': 'READ_ONLY_CODE_TRACE_NOT_DEDICATED_COMBINATION_TEST',
             'source': 'test2/g0_v1/adapter.py:ledger.terminal / ledger.take / gap check',
             'existing_test_numbers': [6, 7, 8, 16, 83],
             'missing_terminal_then_dispatch_dedicated_fixture': 'NOT_SAVED',
             'matched_error_then_legal_retry_dedicated_fixture': 'NOT_SAVED',
             'test69_is_input_cap_retry_not_error_retry': True,
             'gap_barrier_static_behavior': 'Missing terminal persists gap; subsequent request flags/dispatch rejected. Matching error consumes terminal and retains unknown cost without setting gap.'}})
    for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
        src = ROOT / 'docs' / name
        before = PHASE / 'shared-before/docs' / name
        before.parent.mkdir(parents=True, exist_ok=True)
        assert not before.exists()
        shutil.copy2(src, before)
        original = src.read_text()
        first, rest = original.split('\n', 1)
        section = '''

## Current implementation handoff — G0 I01 (2026-11-05)

I01 **IMPLEMENTATION_AND_SELF_TEST_COMPLETE_PENDING_P09**: new `test2/g0_v1/adapter.py`, finite closed-shapes schema, support matrix and D01 44-case mapping. This separately authorized stage permits only offline infrastructure and lightweight synthetic JSON/text fixtures; historical D01/E05/draft false permissions remain unchanged. P08 accepted the sealed D01 paper design **PASS_WITH_LIMITS**, not I01 code or execution rights. Current code acceptance awaits P09; no self-acceptance or next gate.

Saved new-G0 suite history: 60/8 failures, then 66/78/83/89/93 tests with zero failures; all six revisions/results and 469 synthetic case invocations retained. Final attempt6: **93 PASS**, 0.825039s. New CLI recorded PASS/UNRESOLVED/REJECT exits 0/2/1 and existing-output refusal exit1 with unchanged result SHA. These are prior I01 runs verified from saved bindings during sealing, not fresh reruns. No old tests, companion audits or experiments rerun. Source/schema/tests exact SHA and command/exit provenance are in `docs/audits/producer_test2_g0_I01_2026-11-05/evidence-checks.json` and `commands.json`.

44 cases mapped: 26 metadata-tested,12 partial metadata-only,4 raw-parser out of scope,2 G1 out of scope. Only explicit synthetic identities, serial ledger/global halt, unknown costs, path/release and declared observation metadata are implemented. No real VCD/PRE-POST/HEX/MON parser, real grant/provider authentication, oracle execution, independent labels, actual prompt-content secrecy proof, physical reachability, monitor soundness or128-cycle completion. Scientific attribution is NOT_EVALUATED. P08-N1 gap barrier is traceable in code; dedicated missing-terminal→dispatch and matched-error→retry combination fixtures are not saved, so no new passing claim. P05-N1 and all original P04/P05/P06/scientific/billing limits remain.

Exact handoff: `docs/audits/producer_test2_g0_I01_2026-11-05/phase.json` plus `snapshot-manifest.json`; snapshots preserve source/tests, all fixtures/results, initial failures, drafts and these compact entries. Actual HEAD rechecked c25180848ebfe9a1f49da0aa5f579cac913e6428; dirty work preserved. Protected41 file hashes and four freeze identities/member-name inventories checked; **not** a fresh content audit of all4837 members. I01:0 API/count/native/DUT/formal/monitor/oracle/key/network/install/commit/push; no new science data. Next action is coordinator routing this exact sealed I01 to the existing independent reviewer for P09. Do not start G1/services/scientific qualification or create another chat/agent. Older entries below retain stage-time history and are superseded only within this bounded scope.
'''
        src.write_text(first + section + rest)
        assert src.read_text().endswith(rest)
    write(PHASE / 'git-status-after.json', {
        'head': git('rev-parse', 'HEAD'), 'branch': git('branch', '--show-current'),
        'status': git('status', '--porcelain=v1', '--untracked-files=normal')})
    assert git('rev-parse', 'HEAD')['stdout'].strip() == scope['head']
    print(json.dumps({'prepared': True, 'final_tests_saved': 93,
        'all_suite_cases': resource['synthetic_case_invocations'],
        'retained_initial_failures': len(retained_mismatches),
        'protected_matches': len(protected), 'coverage_cases': 44,
        'new_test_runs': 0}, indent=2))


def seal():
    assert not (PHASE / 'phase.json').exists()
    assert not (PHASE / 'snapshot-manifest.json').exists()
    checks = read(PHASE / 'evidence-checks.json')
    scope = read(PHASE / 'scope.json')
    assert all(digest(ROOT / p) == sha for p, sha in scope['protected_sha256'].items())
    assert all(digest(ROOT / p) == sha for p, sha in checks['source_sha256'].items())
    phase = {'phase_id': 'I01_G0_ADAPTER_SYNTHETIC_SELFTEST',
        'project_date': '2026-11-05 America/New_York',
        'status': 'IMPLEMENTATION_AND_SELF_TEST_COMPLETE_PENDING_INDEPENDENT_REVIEW',
        'independent_code_review': 'PENDING_P09_NOT_SELF_ACCEPTED',
        'actual_HEAD': git('rev-parse', 'HEAD')['stdout'].strip(),
        'authorization': rel(PHASE / 'authorization.json'),
        'authorization_sha256': digest(PHASE / 'authorization.json'),
        'scope_sha256': digest(PHASE / 'scope.json'),
        'source_sha256': checks['source_sha256'],
        'evidence_checks_sha256': digest(PHASE / 'evidence-checks.json'),
        'command_provenance_sha256': digest(PHASE / 'commands.json'),
        'coverage_map': rel(RESULT / 'coverage-map.json'),
        'coverage_map_sha256': digest(RESULT / 'coverage-map.json'),
        'support_matrix_sha256': digest(ROOT / 'test2/g0_v1/support-matrix.json'),
        'final_saved_suite': checks['suite_history'][-1],
        'resources': checks['resources'],
        'checks_scope': 'Saved new-I01 artifact/hash checks only; no adapter/test/native/science rerun during sealing',
        'P08': {'status': 'PASS_WITH_LIMITS_DESIGN_ONLY',
             'review_sha256': checks['P08_review_sha256'],
             'N1_scope': 'Existing static branch/barrier tracing only; dedicated combination tests not saved'},
        'scientific_attribution': 'NOT_EVALUATED',
        'raw_scientific_parsers': 'NOT_IMPLEMENTED_OUT_OF_SCOPE',
        'known_limits': ['Synthetic metadata only; not a real/legacy-run acceptance gate',
            'No authenticated grant/provider provenance or general opaque-prompt privacy proof',
            'No G1/independent-label/oracle/physical-reachability qualification',
            'Stable local filesystem assumed; no hostile concurrent-race guarantee',
            'P08-N1 dedicated cross-attempt missing-terminal/error-retry tests not saved',
            'P04 discrepancy, P05-N1 backlog and F1/selected-sample/128completion/H1/H2/L1/billing limits unchanged'],
        'snapshot_manifest': rel(PHASE / 'snapshot-manifest.json'),
        'manifest_hash_cycle_policy': 'Manifest hashes this phase and exact snapshots. Phase names successor manifest but does not hash it.',
        'next_action': 'Coordinator sends this exact I01 to existing independent P09 reviewer. No next gate execution authorized.'}
    write(PHASE / 'phase.json', phase)
    snapshot = PHASE / 'snapshot'
    snapshot.mkdir(exist_ok=False)
    for path in ['test2/g0_v1', 'test2/results/g0-adapter-i01-v1']:
        dst = snapshot / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(ROOT / path, dst, symlinks=True,
                        ignore=shutil.ignore_patterns('__pycache__'))
    for path in ['test2/tests/test_g0_adapter_v1.py', 'docs/HANDOFF.md',
                 'docs/PROJECT_STATUS.md']:
        dst = snapshot / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / path, dst)
    files, links = inventory(PHASE)
    assert 'snapshot-manifest.json' not in files
    write(PHASE / 'snapshot-manifest.json', {
        'phase': 'I01', 'status': 'SEALED_FOR_P09_REVIEW_NOT_ACCEPTED',
        'files': files, 'symlinks': links,
        'symlinks_are_link_text_not_dereferenced_content': True,
        'excluded': ['__pycache__', 'snapshot-manifest.json (self hash)'],
        'regular_file_count': len(files), 'symlink_count': len(links),
        'regular_bytes': sum((PHASE / p).stat().st_size for p in files)})
    for p, sha in files.items():
        assert digest(PHASE / p) == sha
    for p, item in links.items():
        assert os.readlink(PHASE / p) == item['target']
    print(json.dumps({'sealed': True, 'phase_path': rel(PHASE / 'phase.json'),
        'phase_sha256': digest(PHASE / 'phase.json'),
        'manifest_path': rel(PHASE / 'snapshot-manifest.json'),
        'manifest_sha256': digest(PHASE / 'snapshot-manifest.json'),
        'files': len(files), 'links': len(links),
        'new_test_runs': 0, 'independent_review': 'PENDING_P09'}, indent=2))


if __name__ == '__main__':
    {'prepare': prepare, 'seal': seal}[sys.argv[1]]()
