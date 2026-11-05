from collections import deque

PROPS = ['P1_RESET_EMPTY', 'P2_FILL', 'P3_FULL', 'P4_EMPTY', 'P5_DATA_ORDER', 'P6_ACCEPTANCE']


def _int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _chk(res, c, ph, o, q):
    n = len(q)
    exp = [('fill', n, 'P2_FILL'), ('full', 1 if n == 16 else 0, 'P3_FULL'), ('empty', 1 if n == 0 else 0, 'P4_EMPTY')]
    if n:
        exp.append(('data', q[0], 'P5_DATA_ORDER'))
    for k, e, p in exp:
        res['checks'] += 1
        v = o[k]
        if v == -1:
            res['unresolved'].append({'cycle': c, 'phase': ph, 'category': p, 'field': k, 'actual': -1, 'expected': e})
        elif v != e:
            res['failures'].append({'cycle': c, 'phase': ph, 'category': p, 'field': k, 'actual': v, 'expected': e})


def check_rows(rows):
    res = {'verdict': 'PASS', 'failures': [], 'assumption_violations': [], 'unresolved': [],
           'checks': 0, 'rows_processed': 0, 'properties': list(PROPS)}

    def inv(msg):
        res['assumption_violations'].append(msg)
        res['verdict'] = 'INVALID_INPUT'
        return res

    if not isinstance(rows, list) or not rows:
        return inv('rows must be a nonempty list')
    q = deque()
    start = None
    for i, r in enumerate(rows):
        if not isinstance(r, dict) or set(r) != {'cycle', 'action', 'pre', 'post'}:
            return inv('row %d: illegal or missing fields' % i)
        c = r['cycle']
        if not _int(c):
            return inv('row %d: cycle not integer' % i)
        if i == 0:
            start = c
        elif c != start + i:
            return inv('row %d: cycle %r missing or out of order' % (i, c))
        a = r['action']
        if not isinstance(a, dict) or set(a) != {'reset', 'wr', 'rd', 'data'}:
            return inv('cycle %d: illegal action fields' % c)
        for k, w in (('reset', 1), ('wr', 1), ('rd', 1), ('data', 8)):
            v = a[k]
            if not _int(v) or v < 0 or v >= (1 << w):
                return inv('cycle %d: action %s illegal value %r' % (c, k, v))
        if a['reset'] and (a['wr'] or a['rd']):
            return inv('cycle %d: read/write during reset' % c)
        if i == 0 and a['reset'] != 1:
            return inv('first action must reset')
        for ph in ('pre', 'post'):
            o = r[ph]
            if not isinstance(o, dict) or set(o) != {'fill', 'full', 'empty', 'data'}:
                return inv('cycle %d: illegal %s fields' % (c, ph))
            for k, w in (('fill', 5), ('full', 1), ('empty', 1), ('data', 8)):
                v = o[k]
                if not _int(v) or v < -1 or v >= (1 << w):
                    return inv('cycle %d: %s.%s illegal value %r' % (c, ph, k, v))
        if i > 0:
            _chk(res, c, 'pre', r['pre'], q)
        if a['reset']:
            q.clear()
        else:
            n = len(q)
            do_rd = bool(a['rd']) and n > 0
            do_wr = bool(a['wr']) and n < 16
            if do_rd:
                q.popleft()
            if do_wr:
                q.append(a['data'])
        _chk(res, c, 'post', r['post'], q)
        res['rows_processed'] += 1
    if res['failures']:
        res['verdict'] = 'FAIL'
    elif res['unresolved']:
        res['verdict'] = 'UNRESOLVED'
    else:
        res['verdict'] = 'PASS'
    return res

