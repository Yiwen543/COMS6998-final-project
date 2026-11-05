import collections
import copy
import math

_INW = {'rst': 1, 's_valid': 1, 's_data': 8, 's_last': 1, 'm_ready': 1, 'h_ready': 1}
_OUTW = {'s_ready': 1, 'm_valid': 1, 'm_last': 1, 'h_valid': 1, 'h_pad': 1, 'h_truncate': 1, 'm_data': 8, 'h_length': 16, 'h_original_length': 16}
_SF = ('h_length', 'h_original_length', 'h_pad', 'h_truncate')
MIN_LEN = 4
MAX_LEN = 8
MAX_IN = 12
TAIL_MIN = 32


def _okv(x, w):
    return isinstance(x, int) and not isinstance(x, bool) and (x == -1 or 0 <= x < (1 << w))


def _validate(rows):
    if not isinstance(rows, list) or len(rows) == 0:
        return 'rows must be a non-empty list'
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            return 'row %d is not a dict' % i
        for k in ('cycle', 'inputs', 'pre', 'post'):
            if k not in r:
                return 'row %d missing %s' % (i, k)
        c = r['cycle']
        if not isinstance(c, int) or isinstance(c, bool) or c != i:
            return 'row %d: cycles must be consecutive from 0' % i
        for k, spec in (('inputs', _INW), ('pre', _OUTW), ('post', _OUTW)):
            d = r[k]
            if not isinstance(d, dict) or set(d.keys()) != set(spec.keys()):
                return 'row %d: %s must contain exactly the documented fields' % (i, k)
            for f in spec:
                if not _okv(d[f], spec[f]):
                    return 'row %d: %s.%s out of range or not an int' % (i, k, f)
    return None


def _assume(rows):
    for i, r in enumerate(rows):
        x = r['inputs']
        if x['rst'] == 1 and x['s_valid'] == 1:
            return (i, 'source valid during reset')
        if i > 0:
            p = rows[i - 1]
            px = p['inputs']
            if px['rst'] == 0 and px['s_valid'] == 1 and p['pre']['s_ready'] == 0 and x['rst'] == 0:
                for f in ('s_valid', 's_data', 's_last'):
                    a = px[f]
                    b = x[f]
                    if a != -1 and b != -1 and a != b:
                        return (i, 'source changed %s while blocked' % f)
    return None


def _xfer(v, r):
    if v == 0 or r == 0:
        return 0
    if v == 1 and r == 1:
        return 1
    return -1


def _exp_beat(frames, fo, pos):
    # returns (kind, byte_or_None, last_bool, last_definite_at_sample)
    if fo >= len(frames):
        return ('noframe', None, None, False)
    fr = frames[fo]
    b = fr['b']
    n = len(b)
    if pos < n and pos < MAX_LEN:
        if fr['done']:
            return ('ok', b[pos], pos == min(max(n, MIN_LEN), MAX_LEN) - 1, True)
        return ('ok', b[pos], pos == MAX_LEN - 1, pos == MAX_LEN - 1)
    if fr['done'] and pos < MIN_LEN:
        return ('ok', 0, pos == MIN_LEN - 1, True)
    return ('premature', None, None, False)


def _exp_status(frames, ho):
    if ho >= len(frames) or not frames[ho]['done']:
        return None
    n = len(frames[ho]['b'])
    return {'h_original_length': n, 'h_length': min(max(n, MIN_LEN), MAX_LEN), 'h_pad': 1 if n < MIN_LEN else 0, 'h_truncate': 1 if n > MAX_LEN else 0}


def _res(v, f, u, n):
    return {'verdict': v, 'failures': f, 'unknown': u, 'checked_rows': n}


def check_rows(rows, require_drained=False):
    try:
        msg = _validate(rows)
    except Exception:
        msg = 'unreadable rows'
    if msg is None and not isinstance(require_drained, bool):
        msg = 'require_drained must be a bool'
    if msg is not None:
        return _res('INVALID_INPUT', [{'cycle': -1, 'phase': 'end', 'category': 'malformed', 'detail': msg}], [], 0)
    a = _assume(rows)
    if a is not None:
        return _res('INVALID_INPUT', [{'cycle': a[0], 'phase': 'pre', 'category': 'assumption_violation', 'detail': a[1]}], [], 0)
    fails = []
    unk = []

    def F(c, ph, cat, d):
        fails.append({'cycle': c, 'phase': ph, 'category': cat, 'detail': d})

    def U(c, ph, cat, d):
        unk.append({'cycle': c, 'phase': ph, 'category': cat, 'detail': d})

    S = {'frames': [], 'fo': 0, 'pos': 0, 'ho': 0, 'ld': True, 'lh': True, 'li': True}

    def lose_all():
        S['ld'] = True
        S['lh'] = True
        S['li'] = True

    if rows[0]['inputs']['rst'] != 1:
        U(0, 'pre', 'no_initial_reset', 'scoreboard unknown until a known reset edge')

    def ob_check(c, ph, o, ob, vf, fields, cat):
        if ob is None:
            return
        if o[vf] != 1:
            if o[vf] == -1:
                U(c, ph, cat, vf + ' X/Z while held')
            else:
                F(c, ph, cat, vf + ' dropped without transfer or reset')
            return
        for f, val in zip(fields, ob):
            if o[f] == -1 or val == -1:
                U(c, ph, cat, f + ' X/Z in held beat')
            elif o[f] != val:
                F(c, ph, cat, f + ' changed while held')

    def sample(c, ph, o):
        for f in ('m_valid', 'h_valid'):
            if o[f] == -1:
                U(c, ph, 'x_valid', f + ' is X/Z')
        if o['m_valid'] == 1:
            for f in ('m_data', 'm_last'):
                if o[f] == -1:
                    U(c, ph, 'x_payload', f + ' X/Z while m_valid')
            if not S['ld']:
                k, eb, el, ldef = _exp_beat(S['frames'], S['fo'], S['pos'])
                if k == 'ok':
                    if eb is not None and o['m_data'] != -1 and o['m_data'] != eb:
                        F(c, ph, 'data_payload', 'presented m_data %d expected %d' % (o['m_data'], eb))
                    if ldef and o['m_last'] != -1 and o['m_last'] != (1 if el else 0):
                        F(c, ph, 'data_last', 'presented m_last %d expected %d' % (o['m_last'], 1 if el else 0))
        if o['h_valid'] == 1:
            for f in _SF:
                if o[f] == -1:
                    U(c, ph, 'x_payload', f + ' X/Z while h_valid')
            if not S['lh']:
                e = _exp_status(S['frames'], S['ho'])
                if e is not None:
                    for f in _SF:
                        if o[f] != -1 and o[f] != e[f]:
                            F(c, ph, 'status_payload', 'presented %s %d expected %d' % (f, o[f], e[f]))

    obm = None
    obh = None
    n = len(rows)
    for i in range(n):
        r = rows[i]
        x = r['inputs']
        pre = r['pre']
        post = r['post']
        rst = x['rst']
        if rst == -1:
            U(i, 'pre', 'x_reset', 'rst is X/Z; epoch unknown')
            lose_all()
            obm = None
            obh = None
            continue
        if rst == 1:
            S['frames'] = []
            S['fo'] = 0
            S['pos'] = 0
            S['ho'] = 0
            S['ld'] = False
            S['lh'] = False
            S['li'] = False
            obm = None
            obh = None
            for f in ('m_valid', 'h_valid'):
                if post[f] == 1:
                    F(i, 'post', 'reset_clear', f + ' high after reset edge')
                elif post[f] == -1:
                    U(i, 'post', 'reset_clear', f + ' X/Z after reset edge')
            continue
        if i > 0:
            ob_check(i, 'pre', pre, obm, 'm_valid', ('m_data', 'm_last'), 'data_stability')
            ob_check(i, 'pre', pre, obh, 'h_valid', _SF, 'status_stability')
            sample(i, 'pre', pre)
            obm = (pre['m_data'], pre['m_last']) if (pre['m_valid'] == 1 and x['m_ready'] == 0) else None
            obh = tuple(pre[f] for f in _SF) if (pre['h_valid'] == 1 and x['h_ready'] == 0) else None
        else:
            obm = None
            obh = None
        t = _xfer(x['s_valid'], pre['s_ready'])
        if t == -1:
            U(i, 'pre', 'x_transfer', 'input transfer undeterminable')
            lose_all()
        elif t == 1 and not S['li']:
            frames = S['frames']
            if not frames or frames[-1]['done']:
                frames.append({'b': [], 'done': False})
            fr = frames[-1]
            if x['s_data'] == -1:
                U(i, 'pre', 'x_input', 'accepted s_data X/Z')
                fr['b'].append(None)
            else:
                fr['b'].append(x['s_data'])
            if x['s_last'] == -1:
                U(i, 'pre', 'x_input', 'accepted s_last X/Z; frame boundary unknown')
                lose_all()
            elif x['s_last'] == 1:
                fr['done'] = True
            if len(fr['b']) == MAX_IN + 1:
                U(i, 'pre', 'out_of_scope', 'input frame longer than 12 bytes')
        t = _xfer(pre['m_valid'], x['m_ready'])
        if t == -1:
            U(i, 'pre', 'x_transfer', 'data transfer undeterminable')
            S['ld'] = True
        elif t == 1 and not S['ld']:
            k, eb, el, ldef = _exp_beat(S['frames'], S['fo'], S['pos'])
            if k != 'ok':
                F(i, 'pre', 'data_spurious' if k == 'noframe' else 'data_premature', 'data beat transferred without accepted input to justify it')
                S['ld'] = True
            else:
                md = pre['m_data']
                ml = pre['m_last']
                if md == -1 or eb is None:
                    U(i, 'pre', 'data_unresolved', 'transferred byte not determinable')
                elif md != eb:
                    F(i, 'pre', 'data_payload', 'transferred m_data %d expected %d (frame %d byte %d)' % (md, eb, S['fo'], S['pos']))
                if ml == -1:
                    U(i, 'pre', 'data_unresolved', 'transferred m_last X/Z; frame boundary unknown')
                    S['ld'] = True
                elif ml != (1 if el else 0):
                    F(i, 'pre', 'data_last', 'transferred m_last %d expected %d (frame %d byte %d)' % (ml, 1 if el else 0, S['fo'], S['pos']))
                    S['ld'] = True
                elif el:
                    S['fo'] += 1
                    S['pos'] = 0
                else:
                    S['pos'] += 1
        t = _xfer(pre['h_valid'], x['h_ready'])
        if t == -1:
            U(i, 'pre', 'x_transfer', 'status transfer undeterminable')
            S['lh'] = True
        elif t == 1 and not S['lh']:
            e = _exp_status(S['frames'], S['ho'])
            if e is None:
                F(i, 'pre', 'status_premature_or_spurious', 'status transferred before its input frame completed or without a frame')
                S['lh'] = True
            else:
                for f in _SF:
                    if pre[f] == -1:
                        U(i, 'pre', 'status_unresolved', f + ' X/Z on transfer')
                    elif pre[f] != e[f]:
                        F(i, 'pre', 'status_payload', 'transferred %s %d expected %d (status %d)' % (f, pre[f], e[f], S['ho']))
                S['ho'] += 1
        ob_check(i, 'post', post, obm, 'm_valid', ('m_data', 'm_last'), 'data_stability')
        ob_check(i, 'post', post, obh, 'h_valid', _SF, 'status_stability')
        sample(i, 'post', post)
        obm = (post['m_data'], post['m_last']) if (post['m_valid'] == 1 and x['m_ready'] == 0) else None
        obh = tuple(post[f] for f in _SF) if (post['h_valid'] == 1 and x['h_ready'] == 0) else None

    if require_drained:
        c = n - 1
        last = rows[-1]
        sv = last['inputs']['s_valid']
        if sv == 1:
            F(c, 'end', 'completion', 's_valid still offered at end')
        elif sv == -1:
            U(c, 'end', 'completion', 's_valid X/Z at end')
        for f in ('m_valid', 'h_valid'):
            if last['post'][f] == 1:
                F(c, 'end', 'completion', f + ' still high at end')
            elif last['post'][f] == -1:
                U(c, 'end', 'completion', f + ' X/Z at end')
        frames = S['frames']
        if S['li'] or S['ld'] or S['lh']:
            U(c, 'end', 'completion_unresolved', 'scoreboard not fully known; completion cannot be proven')
        if not S['li'] and frames and not frames[-1]['done']:
            F(c, 'end', 'completion', 'incomplete accepted input frame at end')
        if not S['li'] and not S['ld'] and (S['fo'] < len(frames)):
            F(c, 'end', 'completion', '%d data response frame(s) not fully consumed' % (len(frames) - S['fo']))
        if not S['li'] and not S['lh'] and S['ho'] < len(frames):
            F(c, 'end', 'completion', '%d status response(s) not consumed' % (len(frames) - S['ho']))
        k = 0
        for rr in reversed(rows):
            xx = rr['inputs']
            if xx['rst'] == 0 and xx['s_valid'] == 0 and xx['m_ready'] == 1 and xx['h_ready'] == 1:
                k += 1
            else:
                break
        if k < TAIL_MIN:
            U(c, 'end', 'drain_tail_short', 'quiet ready-high tail is %d cycles (< %d)' % (k, TAIL_MIN))

    if fails:
        v = 'FAIL'
    elif unk:
        v = 'UNRESOLVED'
    else:
        v = 'PASS'
    return _res(v, fails, unk, n)

