"""R02 metadata/hash sealing only; no G1 code/test/tool execution."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PHASE = Path(__file__).resolve().parent
V1, V2 = ROOT / 'test2/g1_v1', ROOT / 'test2/g1_v2'
RESULT = ROOT / 'test2/results/g1-qualification-v2'
REG = ROOT / 'test2/configs/g1_qualification_registration_v2.json'
P10 = ROOT / 'docs/audits/agent_bridge_2026-11-06/P10_g1_registration'


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
protected = read(PHASE / 'protected-before.json')['files']
assert all(sha(ROOT / path) == digest for path, digest in protected.items())
assert sha(P10 / 'review.json') == 'cca7589786545675331ba1daa163d4e5cc757795aa8ac57972404e7463ee73e1'
assert sha(P10 / 'review.md') == '9edcb094e704007eb0db1836fbb1214d5d9f1d7cedf222761781a79434a8d62b'
assert read(P10 / 'review.json')['status'] == 'CHANGES_REQUIRED'
reg, prior_reg = read(REG), read(ROOT / 'test2/configs/g1_qualification_registration_v1.json')
for key in ['caps', 'tools', 'profile', 'pool_state', 'native_depth', 'user_authorization_sha256']:
    assert reg[key] == prior_reg[key]
assert reg['user_authorization_sha256'] == 'bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab'
assert sha(ROOT / reg['user_authorization']) == reg['user_authorization_sha256']
assert not (ROOT / reg['pool_state']).exists()
assert not (RESULT / 'execution-state.json').exists()
assert not (RESULT / 'build').exists()
semantic = read(PHASE / 'change-and-evidence-map.json')['unchanged_semantic_input_sha256']
assert all(sha(V1 / path) == sha(V2 / path) == digest for path, digest in semantic.items())
plan1, plan2 = read(V1 / 'job-plan.json'), read(V2 / 'job-plan.json')
assert json.dumps(plan2).replace('/g1_v2/', '/g1_v1/') == json.dumps(plan1)
for source in V2.glob('*.py'):
    ast.parse(source.read_text(), filename=rel(source))
run = RESULT / 'regression-attempt1'
summary = read(run / 'summary.json')
assert summary['tests'] == 14 and summary['passed'] and summary['failures'] == summary['errors'] == 0
assert all(sha(V2 / name) == sha(run / 'executed-source' / name) == digest
           for name, digest in summary['source_sha256'].items())
for case in run.glob('test_*'):
    bindings = read(case / 'input-bindings.json')
    assert all(sha(case / 'inputs' / name) == digest for name, digest in bindings.items())
write(PHASE / 'commands-and-checks.json', dict(
    executed_command=['PYTHONDONTWRITEBYTECODE=1', '.venv/bin/python',
        'test2/g1_v2/regression_tests.py', '--record', rel(run)],
    exit_code=0, tool_receipt='8f803b', summary_sha256=sha(run / 'summary.json'),
    unittest_log_sha256=sha(run / 'unittest.log'), tests=14, failures=0, errors=0,
    seconds=summary['seconds'], old_R01_P10_G0_tests_rerun=False,
    real_tool_or_OS_process_sleep_calls=0,
    source_and_final_mutated_fixture_bindings_checked=True,
    Python_AST_source_files_checked=len(list(V2.glob('*.py')))))
facts = {}
for case in sorted(run.glob('test_*')):
    data = read(case / 'result.json')
    facts[case.name] = {key: data.get(key) for key in
        ['mocked_Popen_calls', 'parse_outcome', 'outcome', 'reason']}
    if 'runtime_receipt' in data:
        facts[case.name]['status'] = data['runtime_receipt']['status']
        facts[case.name]['deadline'] = data['runtime_receipt']['absolute_job_deadline']
write(PHASE / 'final-selfcheck-facts.json', facts)
inputs = {rel(path): sha(path) for path in V2.rglob('*')
          if path.is_file() and '__pycache__' not in path.parts}
for source in [REG, ROOT / reg['user_authorization'], PHASE / 'P10B-review-checklist.md',
               P10 / 'review.json', P10 / 'review.md', P10 / 'evidence-manifest.json',
               P10 / 'independent-probes/deadline-crossed-during-reservation/result.json']:
    inputs[rel(source)] = sha(source)
write(V2 / 'source-manifest.json', dict(kind='G1_R02_PRETOOL_INFRASTRUCTURE_REPAIR_INPUTS',
    files=inputs, semantic_profile=reg['profile'], new_executed_profile=False,
    P10_parent_decision='CHANGES_REQUIRED_RETAINED', independent_review='PENDING_P10B',
    waveform_policy='Copied P10 analytic VCD regressions only; no actual G1 simulator/native waveform generated'))
section = f'''

## Current G1 repair preparation — R02 / pending P10B (2026-11-05)

P10 returned **CHANGES_REQUIRED** for frozen R01: P10-R1 late dispatch after slow reservation persistence; P10-R2 VCD EOF extrapolation past requiredpost15ns. R01/P10/source/fixtures/results remain byte-identical. New `test2/g1_v2/` and `{rel(REG)}` implement only these pre-execution repairs plus necessary namespace/bindings. R02 status **PREPARED_PENDING_P10B_INCREMENTAL_REVIEW**, not independent acceptance and not a second executed profile.

R1 now rechecks original absolute root/work deadline after persistence and after mkdir/log immediately before Popen; consumed reservations remain charged NOT_RUN and persistent halt, no refunds/rebase/restart. R2 bounds each required row/native selected candidate to the recorded VCD span; missing tail retains explicit VCD_TIME_COVERAGE_MISSING. New14 targeted purePython regressions PASS(0.025039s): save/mkdir/log1194+7 cases invoke mockedPopen0, normal100 baseline1, timeout stays original20deadline; exact P10 full16ns fixture accepts and exact14ns prefix rejects post15ns for coverage, unknown/missing-signal refusals preserved. Source is copied before each execution and final-mutated inputs/results/SHA saved. No R01/P10/G0 suite/experiment/companion rerun.

All18SV files, original3 inputs/math-label JSONs, support matrix, caps/toolpins/profile and path-normalized flags/job order unchanged. P10 independently found no16-label mismatch; that limited analysis is reused, not native qualification. P10-N1 accepts logical compile batches only with all children in root/global time/raw logs; not18OSprocesses. Same original usergrant SHA bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab and same uncreated canonical pool `{reg['pool_state']}`:32native(depth8/10s),32physical(1024cycles/2s),32compile(20s),1200s. R02 outputs use a new result root; no per-version allowance. Actual G1 version/compile/native/physical/API/key/pool starts remain0.

Exact handoff `{rel(PHASE / 'phase.json')}` / `snapshot-manifest.json`; source `{rel(V2 / 'source-manifest.json')}`. Hallmark applicability/fixed-input/ranked-minimal-repair use is recorded in R02 hallmark-usage.json, with no UI workflow or RTL correctness certification. Coordinator next sends exact R02 to existing P10B for incremental review; accepted review.phase must startP10 and bind new producer manifest/registration. Later EXECUTE under the same grant uses preparation_manifest_sha256 for R02; no key/newuserapproval now. Stop at this safety checkpoint. All old scientific/unknown/negative/P04/P05/P06/P05-N1/F1/selected-sample/category/128/H1/H2/L1/billing limits and all old bodies below remain preserved; no G2–G5/API/paid/install/delete/commit/push or new chat/agent.
'''
for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
    source = ROOT / 'docs' / name
    original = source.read_bytes()
    saved = PHASE / 'before/docs' / name
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_bytes(original)
    header, body = original.split(b'\n', 1)
    source.write_bytes(header + section.encode() + body)
    assert source.read_bytes().endswith(body)
assert all(sha(ROOT / path) == digest for path, digest in protected.items())
created = PHASE.stat()
write(PHASE / 'phase.json', dict(
    phase='G1_R02_PREEXECUTION_INFRASTRUCTURE_REPAIR',
    status='PREPARED_PENDING_P10B_INCREMENTAL_REVIEW', actual_HEAD=git('rev-parse', 'HEAD')['stdout'].strip(),
    parent_phase='docs/audits/producer_test2_g1_R01_2026-11-05/phase.json',
    parent_phase_sha256=sha(ROOT / 'docs/audits/producer_test2_g1_R01_2026-11-05/phase.json'),
    parent_manifest_sha256=sha(ROOT / 'docs/audits/producer_test2_g1_R01_2026-11-05/snapshot-manifest.json'),
    P10_review_sha256=sha(P10 / 'review.json'), P10_md_sha256=sha(P10 / 'review.md'),
    P10_evidence_manifest_sha256=sha(P10 / 'evidence-manifest.json'),
    P10_parent_decision='CHANGES_REQUIRED_NOT_RELABELED',
    addressed_findings=['P10-R1', 'P10-R2'], producer_disposition='SELFTESTED_REPAIRS_PENDING_P10B',
    registration=rel(REG), registration_sha256=sha(REG),
    source_manifest=rel(V2 / 'source-manifest.json'), source_manifest_sha256=sha(V2 / 'source-manifest.json'),
    user_grant_sha256=reg['user_authorization_sha256'], semantic_profile=reg['profile'],
    shared_pool_path=reg['pool_state'], pool_created=False,
    unchanged_semantic_files=len(semantic), flags_and_order_identical_except_paths=True,
    change_map_sha256=sha(PHASE / 'change-and-evidence-map.json'),
    regression_summary_sha256=sha(run / 'summary.json'), new_regression_tests=14,
    new_regression_failures=0, actual_resources={key: 0 for key in ['setup_version',
        'compiler', 'native_BMC_cover', 'simulator', 'physical_cycles', 'real_G1_tool_child_process',
        'real_sleep', 'API', 'count', 'generation', 'Claude', 'key', 'network', 'install',
        'delete', 'commit', 'push', 'new_agent', 'new_chat']},
    caps=reg['caps'], old_protected_files_checked=len(protected), old_hash_mismatches=[],
    actual_native_waveforms='NOT_GENERATED;only copied analytic P10 fixtures in regression namespace',
    independent_acceptance='PENDING_P10B_NOT_SELF_ACCEPTED',
    elapsed=dict(full_turn_wall_seconds=None, full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',
        observed_namespace_authoring_span_seconds=time.time()-getattr(created, 'st_birthtime', created.st_mtime),
        execution1200s_clock_started=False, independent_P10B_readonly_elapsed='NOT_YET_REVIEWED'),
    snapshot_manifest=rel(PHASE / 'snapshot-manifest.json'),
    hash_cycle_policy='Successor manifest hashes phase; phase names manifest without its hash',
    next_action='STOP_COORDINATOR_SENDS_EXISTING_P10B_INCREMENTAL_REVIEW;EXECUTE_ONLY_AFTER_EXACT_ACCEPTANCE_UNDER_SAME_GRANT'))
write(PHASE / 'git-status-after.json', dict(head=git('rev-parse', 'HEAD'),
      branch=git('branch', '--show-current'),
      worktree=git('status', '--porcelain=v1', '--untracked-files=normal')))
snapshot = PHASE / 'snapshot'
snapshot.mkdir()
for source in [V2, RESULT]:
    target = snapshot / rel(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
for source in [REG, ROOT / reg['user_authorization'], P10 / 'review.json', P10 / 'review.md',
               P10 / 'evidence-manifest.json', ROOT / 'docs/HANDOFF.md', ROOT / 'docs/PROJECT_STATUS.md']:
    target = snapshot / rel(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
files = {str(path.relative_to(PHASE)): sha(path) for path in PHASE.rglob('*')
         if path.is_file() and '__pycache__' not in path.parts}
write(PHASE / 'snapshot-manifest.json', dict(status='PREPARED_PENDING_P10B_INCREMENTAL_REVIEW',
    files=files, file_count=len(files), symlinks={}, excluded=['snapshot-manifest.json(self-hash)', '__pycache__']))
assert all(sha(PHASE / path) == digest for path, digest in files.items())
print(json.dumps(dict(phase=rel(PHASE / 'phase.json'), phase_sha256=sha(PHASE / 'phase.json'),
    manifest=rel(PHASE / 'snapshot-manifest.json'), manifest_sha256=sha(PHASE / 'snapshot-manifest.json'),
    registration_sha256=sha(REG), source_manifest_sha256=sha(V2 / 'source-manifest.json'),
    snapshot_files=len(files), protected_files=len(protected), tests=14, real_tool_calls=0,
    status='PREPARED_PENDING_P10B_INCREMENTAL_REVIEW'), indent=2))
