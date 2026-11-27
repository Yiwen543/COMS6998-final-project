"""Frozen source-only plans for dependency-driven proof reuse.

The two real archives are not new model calls. The live chronology is explicitly
deduplicated across the three identical arm histories. The ladder and portfolios
are controlled compositions of archived monitor sources, never labelled as LLM
answers. Their order/labels are fixed independently of this experiment's verdicts.
"""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import tarfile
import tempfile

from audit_egg_regression_live import audit
from egg_regression_workload import ARCHIVE, load_versions, workload
from egg_txn_terms import parse_term
from predicates import ROOT


LIVE_ARCHIVE = ROOT/'results/milestone3/frame-txn-regression-live/transcript.tar.gz'
LIVE_SHA256 = 'eee3de22f27f64c0d0511adf2b12d92eb1504ba3d7f7a9ffdf068134796972ef'
LIVE_PREFIX = 'live-20261125-173313'
PROTOCOL = ROOT/'docs/egg_dependency_reuse_protocol.md'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def _live_audit(archive, live_archive):
    require(digest(live_archive) == LIVE_SHA256, 'latest archived live transcript hash changed')
    # Extract only the fixed completed pilot, never the failed or fixture run.
    with tempfile.TemporaryDirectory(prefix='dependency-live-') as root:
        seen = set()
        with tarfile.open(live_archive, 'r:gz') as tar:
            for m in tar:
                path = PurePosixPath(m.name)
                require(not path.is_absolute() and '..' not in path.parts and path.parts, 'unsafe archive member')
                if path.parts[0] != LIVE_PREFIX or m.isdir():
                    continue
                require(m.isfile() and len(path.parts) > 1 and m.name not in seen, 'invalid live archive member')
                seen.add(m.name)
                output = Path(root).joinpath(*path.parts[1:])
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(tar.extractfile(m).read())
        require(len(seen) == 49, 'unexpected completed live inventory')
        return audit(Path(root), archive)


def _row(ident, round_no, prop, guard, left, right, relation, cohort, **extra):
    for source in (guard, left, right):
        parse_term(source)
    return {'id': ident, 'round': round_no, 'property': prop, 'guard': guard,
            'left': left, 'right': right, 'expected_relation': relation, 'cohort': cohort, **extra}


def plan(archive=ARCHIVE, live_archive=LIVE_ARCHIVE):
    versions = load_versions(archive)
    start = versions['trial-01/initial']
    reference = start['monitors']['data_last']
    sources = {'archive_member': start['source'], 'response_id': start['response_id'],
               'response_sha256': start['response_sha256']}
    suites = {'matrix': workload(archive)}

    live = _live_audit(archive, live_archive)
    require(live['audited_summary']['provider_api_calls'] == 9 and
            all(row['same_qualified_text'] and row['same_carried_text'] for row in live['stage_comparison']),
            'expected the same real scoped monitor history in all three arms')
    rows = []
    for stage in range(1, 4):
        stage_info = live['stage_comparison'][stage-1]
        guard = stage_info['guard']
        checked = live['checked_history']
        before = {a: checked[a]['preflights'][stage-1] for a in ('raw', 'ordinary', 'egg')}
        after = {a: [c for c in checked[a]['calls'] if c['stage'] == stage] for a in before}
        require(all(len(c) == 1 and c[0]['qualified'] for c in after.values()), 'expected one actual reply per arm/stage')
        require(len({x['relation'] for x in before.values()}) == 1 and
                len({x['candidate'] for x in before.values()}) == 1 and
                len({x[0]['candidate'] for x in after.values()}) == 1, 'real histories differ')
        receipts = {a: after[a][0]['response_id'] for a in after}
        rows.append(_row(f'L{2*stage-1:02}', 2*stage-2, 'data_last', guard, reference,
                         before['egg']['candidate'], before['egg']['relation'], 'real_live_preflight',
                         stage=stage, origins=receipts, source='archived carry checked before the real reply; three identical histories'))
        rows.append(_row(f'L{2*stage:02}', 2*stage-1, 'data_last', guard, reference,
                         after['egg'][0]['candidate'], 'equivalent', 'real_live_reply',
                         stage=stage, origins=receipts, source='same actual qualified reply in three arms'))
    suites['live'] = rows

    p = reference
    q = f'(and (ult data_n 8) {p})'
    r = f'(and (ult data_n 9) {p})'
    ladder = (
        (0, 4, p, q, 'equivalent', 'seed-P-Q'),
        (0, 4, q, r, 'equivalent', 'seed-Q-R'),
        (1, 5, p, r, 'equivalent', 'cross-P-R'),
        (2, 5, r, q, 'equivalent', 'reverse-R-Q'),
        (3, 8, p, r, 'equivalent', 'possible-old-path-invalid-but-goal-true'),
        (4, 8, p, q, 'weakened', 'invalid-N8-P-Q'),
        (5, 9, p, r, 'weakened', 'invalid-N9-P-R'),
        (6, 4, q, p, 'equivalent', 'return-reverse'),
        (7, 5, p, q, 'equivalent', 'cross-P-Q'),
    )
    suites['ladder'] = [_row(f'C{i:02}', step, 'data_last', f'(eq data_n {n})', a, b, rel,
                              'controlled_ladder', control=label, original=sources)
                        for i,(step,n,a,b,rel,label) in enumerate(ladder,1)]
    suites['ladder'].append(_row('C10',8,'data_last','(ult data_n 0)',p,q,'infeasible',
                                  'controlled_ladder',control='infeasible-guard',original=sources))

    names = ['data_last'] + sorted(n for n in start['monitors'] if n != 'data_last')
    for size in (1,3,5,9):
        selected = names[:size]
        alarm = start['monitors'][selected[0]]
        for name in selected[1:]:
            alarm = f'(or {alarm} {start["monitors"][name]})'
        gated = f'(and (ult data_n 8) {alarm})'
        key = f'portfolio-{size:02}'
        suites[key] = [_row(f'P{size:02}-{i+1:02}',i,'aggregate_alarm',f'(eq data_n {n})',alarm,gated,
                            'weakened' if n==8 else 'equivalent','controlled_portfolio',
                            selected_properties=selected,original=sources)
                       for i,n in enumerate((4,5,6,7,8,4))]
    require([len(v) for v in suites.values()] == [224,6,10,6,6,6,6], 'frozen workload size changed')
    return suites
