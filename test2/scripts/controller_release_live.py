"""All-round immutable snapshots and final release; no model or hidden inputs."""
import json
from pathlib import Path
from common import dump, sha

ARMS = ('B2_raw', 'C2_semantic')


def freeze_round(root, directory, context, status):
    files = {str(p.relative_to(root)): sha(p) for p in directory.rglob('*') if p.is_file() and p.name != 'snapshot.json'}
    row = dict(context, status=status, directory=str(directory.relative_to(root)), files=files)
    path = directory / 'snapshot.json'
    if path.exists():
        raise FileExistsError('Round snapshot already frozen')
    dump(path, row)
    return {'snapshot': str(path.relative_to(root)), 'sha256': sha(path)}


def checked_snapshot(root, row):
    path = (root / row['snapshot']).resolve()
    if not path.is_relative_to(root.resolve()) or sha(path) != row['sha256']:
        raise ValueError('Snapshot changed or outside run')
    data = json.loads(path.read_text())
    for name, expected in data['files'].items():
        artifact = (root / name).resolve()
        if not artifact.is_relative_to(root.resolve()) or sha(artifact) != expected:
            raise ValueError('Frozen round artifact changed: '+name)
    if data['status'] == 'compiled':
        required = ['candidate.sv', 'candidate.json', 'replay.vvp']
        if any(data['directory']+'/compiled/'+n not in data['files'] for n in required):
            raise ValueError('Compiled snapshot lacks source/replay binding')
    return data


def release(root, snapshots, mode):
    data = [checked_snapshot(root, r) for r in snapshots]
    expected = {(a, r, n) for a in ARMS for r in (1, 2, 3) for n in range(1, 7)}
    if len(data) != 36 or {(d['arm'], d['repetition'], d['round']) for d in data} != expected:
        raise ValueError('All36 valid/invalid round snapshots required before release')
    ids = [{d['session_id'] for d in data if (d['arm'], d['repetition']) == (a, r)} for a in ARMS for r in (1, 2, 3)]
    if any(len(v) != 1 for v in ids) or len(set.union(*ids)) != 6:
        raise ValueError('Six independent own-history session IDs required')
    manifest = {'mode': mode, 'rounds': snapshots, 'all36_rounds_present': True,
                'hidden_scoring_started': False, 'not_new_model_evidence': mode != 'live'}
    dump(root / 'all-round-candidates.json', manifest)
    finals = []
    for arm in ARMS:
        for rep in (1, 2, 3):
            valid = sorted((d for d in data if d['arm'] == arm and d['repetition'] == rep and d['status'] == 'compiled'), key=lambda d: d['round'])
            selected = valid[-1] if valid else None
            finals.append({'arm': arm, 'repetition': rep, 'status': 'compiled' if selected else 'invalid',
                           'selected_round': selected['round'] if selected else None,
                           'directory': selected['directory']+'/compiled' if selected else None})
    dump(root / 'final-candidates.json', {'mode': mode, 'candidates': finals})
    files = ['all-round-candidates.json', 'final-candidates.json', 'calls.jsonl', 'run.json']
    dump(root / 'release.json', {'mode': mode, 'files': {n: sha(root / n) for n in files},
                               'candidate_revision_allowed': False, 'all_rounds_frozen': True})
    return finals


def verify_release(root):
    record = json.loads((root / 'release.json').read_text())
    if record['candidate_revision_allowed'] or not record['all_rounds_frozen']:
        raise ValueError('Invalid final release')
    for name, h in record['files'].items():
        if sha(root / name) != h:
            raise ValueError('Release artifact changed: '+name)
    rounds = json.loads((root / 'all-round-candidates.json').read_text())['rounds']
    data = [checked_snapshot(root, row) for row in rounds]
    expected = {(a, r, n) for a in ARMS for r in (1, 2, 3) for n in range(1, 7)}
    if len(data) != 36 or {(d['arm'], d['repetition'], d['round']) for d in data} != expected:
        raise ValueError('Missing frozen round')
    ids = [{d['session_id'] for d in data if (d['arm'], d['repetition']) == (a, r)} for a in ARMS for r in (1, 2, 3)]
    if any(len(v) != 1 for v in ids) or len(set.union(*ids)) != 6:
        raise ValueError('Session independence changed')
    finals = json.loads((root / 'final-candidates.json').read_text())['candidates']
    if len(finals) != 6 or {(d['arm'],d['repetition']) for d in finals} != {(a,r) for a in ARMS for r in (1,2,3)}:
        raise ValueError('Invalid final candidate set')
    for f in finals:
        valid = [d for d in data if (d['arm'],d['repetition']) == (f['arm'],f['repetition']) and d['status']=='compiled']
        last = max(valid, key=lambda d:d['round']) if valid else None
        if f['selected_round'] != (last['round'] if last else None) or f['directory'] != (last['directory']+'/compiled' if last else None):
            raise ValueError('Final selection changed')
    return data
