import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
OWN = Path(__file__).resolve().parent
PACKET = OWN / 'phase-packet.json'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def run():
    started = time.monotonic()
    packet = read(PACKET)
    audit = (ROOT / packet['producer_phase']).parent
    snap = audit / 'snapshot'
    mismatches = []
    checked = []
    def check_file(path, expected, category):
        path = Path(path)
        actual = sha(path) if path.is_file() else None
        row = dict(path=str(path), expected=expected, actual=actual, category=category)
        checked.append(row)
        if actual != expected:
            mismatches.append(row)
    for key in ['producer_phase', 'producer_manifest', 'registration', 'source_manifest', 'continuation_decision']:
        check_file(ROOT / packet[key], packet[key + '_sha256'], 'packet')
    manifest = read(ROOT / packet['producer_manifest'])
    for rel, expected in manifest['files'].items():
        check_file(audit / rel, expected, 'sealed_member')
        if rel.startswith('snapshot/'):
            check_file(ROOT / rel[len('snapshot/'):], expected, 'current_vs_snapshot')
    sources = read(snap / packet['source_manifest'])['files']
    for rel, expected in sources.items():
        sealed = snap / rel
        # The producer-owned checklist is sealed at the package root, not recursively.
        if not sealed.exists() and (ROOT / rel).parent == audit:
            sealed = audit / Path(rel).name
        check_file(sealed, expected, 'sealed_source')
        check_file(ROOT / rel, expected, 'current_source')
    preservation = read(audit / 'preservation-before.json')
    for rel, expected in preservation['files'].items():
        check_file(ROOT / rel, expected, 'protected')
    change = read(audit / 'change-and-evidence-map.json')
    for rel, expected in change['unchanged_semantic_input_sha256'].items():
        check_file(snap / 'test2/g1_v3' / rel, expected, 'semantic_new')
        check_file(ROOT / 'test2/g1_v2' / rel, expected, 'semantic_accepted_old')
    check_file(snap / 'test2/g1_v3/observations.py', change['observations_unchanged_sha256'], 'observer_new')
    check_file(ROOT / 'test2/g1_v2/observations.py', change['observations_unchanged_sha256'], 'observer_old')
    oldplan = read(ROOT / 'test2/g1_v2/job-plan.json')
    newplan = read(snap / 'test2/g1_v3/job-plan.json')
    normalize = lambda value: json.dumps(value, sort_keys=True).replace('g1_v3', 'g1_v2').replace('g1-qualification-v3', 'g1-qualification-v2')
    planned_old = [j for j in oldplan['jobs'] if j['id'] != 'setup-make']
    assert normalize(planned_old) == normalize(newplan['jobs']), 'JOB_PLAN_SEMANTIC_DRIFT'
    reg = read(snap / packet['registration'])
    oldreg = read(ROOT / 'test2/configs/g1_qualification_registration_v2.json')
    assert reg['caps'] == oldreg['caps']
    assert {k:{a:b for a,b in v.items() if a not in ['actual_version','version_policy']} for k,v in reg['tools'].items()} == {k:{a:b for a,b in v.items() if a not in ['actual_version','version_policy']} for k,v in oldreg['tools'].items()}
    assert reg['tools']['make']['actual_version'] == 'NOT_REPROBED_TO_PRESERVE_CUMULATIVE_SETUP_CAP'
    for name in ['HANDOFF.md', 'PROJECT_STATUS.md']:
        before = (audit / 'before/docs' / name).read_bytes()
        after = (snap / 'docs' / name).read_bytes()
        assert after.endswith(before[before.index(b'\n')+1:]), 'OLD_DOC_BODY_CHANGED'
    test_summary = read(audit / 'test-evidence-summary.json')
    suites = []
    for row in test_summary['suites']:
        base = snap / row['path']
        check_file(base / 'summary.json', row['summary_sha256'], 'saved_test_summary')
        check_file(base / 'unittest.log', row['log_sha256'], 'saved_test_log')
        summary = read(base / 'summary.json')
        assert (summary['tests'], summary['failures'], summary['errors']) == (row['tests'], row['failures'], row['errors'])
        for name, expected in summary['source_sha256'].items():
            check_file(base / 'executed-source' / name, expected, 'saved_executed_source')
            if row['final_source']:
                check_file(snap / 'test2/g1_v3' / name, expected, 'final_source_identity')
        for binding in base.glob('*/input-bindings.json'):
            inputs = binding.parent / 'inputs'
            for rel, expected in read(binding).items():
                check_file(inputs / rel, expected, 'saved_fixture_binding')
        suites.append({k:row[k] for k in ['path','tests','failures','final_source','recorded_exit_code','exit_capture_note']})
    assert sum(s['tests'] for s in suites) == 111
    assert sum(s['failures'] for s in suites) == 1
    index = subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'], cwd=ROOT)
    index_sha = hashlib.sha256(index).hexdigest()
    assert index_sha == preservation['git_index_entries_sha256'], 'INDEX_DRIFT'
    head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    uncreated = {key: not (ROOT / reg[key]).exists() for key in ['pool_state','attempt_lock']}
    assert all(uncreated.values()), 'REAL_R03_POOL_OR_LOCK_EXISTS'
    result = dict(actual_HEAD=head, packet_sha256=sha(PACKET), producer_manifest_sha256=sha(ROOT/packet['producer_manifest']), sealed_members=len(manifest['files']),source_bindings=len(sources),protected_files=len(preservation['files']),semantic_materials=24,observer_unchanged=True,job_order_normalized_equal=True,only_removed_job='setup-make',index_sha256=index_sha,real_paths_uncreated=uncreated,saved_suites=suites,checked=checked,mismatches=mismatches,elapsed_seconds=time.monotonic()-started)
    label = sys.argv[1] if len(sys.argv)>1 else 'before'
    target = OWN / ('input-verification-' + label + '.json')
    with target.open('x') as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['checked','saved_suites']}))
    assert not mismatches, 'INPUT_HASH_MISMATCH'

if __name__ == '__main__':
    run()
