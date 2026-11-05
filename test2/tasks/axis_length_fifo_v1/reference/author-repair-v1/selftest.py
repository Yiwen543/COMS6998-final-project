import copy


def _fr(lens, off):
    return [[(16 * j + i + 1 + off) & 255 for i in range(n)] for j, n in enumerate(lens)]


def _outs(st):
    o = {'s_ready': 1, 'm_valid': 0, 'm_data': 0, 'm_last': 0, 'h_valid': 0, 'h_pad': 0, 'h_truncate': 0, 'h_length': 0, 'h_original_length': 0}
    if st['oq']:
        o['m_valid'] = 1
        o['m_data'] = st['oq'][0][0]
        o['m_last'] = st['oq'][0][1]
    if st['hq']:
        s = st['hq'][0]
        o['h_valid'] = 1
        o['h_length'] = s[0]
        o['h_original_length'] = s[1]
        o['h_pad'] = s[2]
        o['h_truncate'] = s[3]
    return o


def _status(n):
    return (min(max(n, 4), 8), n, 1 if n < 4 else 0, 1 if n > 8 else 0)


def _accept(st, byte, last, n, opt):
    st['cur'].append(byte)
    p = len(st['cur']) - 1
    maxo = opt.get('maxo', 8)
    if opt.get('early_status') and p == 0:
        st['hq'].append(_status(n))
    if opt.get('cut', True):
        if p < maxo:
            lf = (p == maxo - 1) or (last == 1 and p >= 3)
            st['oq'].append((byte, 1 if lf else 0))
        if last == 1 and p < 3:
            for q in range(p + 1, 4):
                st['oq'].append((0, 1 if q == 3 else 0))
    elif last == 1:
        b = list(st['cur'][:maxo])
        while len(b) < 4:
            b.append(0)
        for q, v in enumerate(b):
            st['oq'].append((v, 1 if q == len(b) - 1 else 0))
    if last == 1:
        if not opt.get('early_status'):
            st['hq'].append(_status(len(st['cur'])))
        st['cur'] = []


def _step(rows, st, src, rst, mr, hr, opt):
    c = len(rows)
    x = {'rst': rst, 's_valid': 0, 's_data': 0, 's_last': 0, 'm_ready': mr, 'h_ready': hr}
    if rst == 0 and src:
        x['s_valid'] = 1
        x['s_data'] = src[0][0]
        x['s_last'] = src[0][1]
    pre = _outs(st)
    if rst == 1:
        st['cur'] = []
        if not opt.get('no_clear'):
            st['oq'] = []
            st['hq'] = []
    else:
        if x['s_valid'] == 1 and pre['s_ready'] == 1:
            b, l, n = src.pop(0)
            _accept(st, b, l, n, opt)
        if pre['m_valid'] == 1 and mr == 1:
            st['oq'].pop(0)
        if pre['h_valid'] == 1 and hr == 1:
            st['hq'].pop(0)
    rows.append({'cycle': c, 'inputs': x, 'pre': pre, 'post': _outs(st)})


def _gen(epochs, ep_cycles=(), tail=40, opt=None, block_early=False):
    opt = opt or {}
    rows = []
    st = {'oq': [], 'hq': [], 'cur': []}
    for k, lens in enumerate(epochs):
        src = []
        for f in _fr(lens, 100 * k):
            for i, v in enumerate(f):
                src.append((v, 1 if i == len(f) - 1 else 0, len(f)))
        _step(rows, st, src, 1, 1, 1, opt)
        if k < len(epochs) - 1:
            for _ in range(ep_cycles[k]):
                c = len(rows)
                mr = 0 if block_early else (0 if c % 4 == 2 else 1)
                hr = 0 if block_early else (0 if c % 5 in (1, 2) else 1)
                _step(rows, st, src, 0, mr, hr, opt)
        else:
            g = 0
            while src and g < 1000:
                c = len(rows)
                _step(rows, st, src, 0, 0 if c % 4 == 2 else 1, 0 if c % 5 in (1, 2) else 1, opt)
                g += 1
            for _ in range(tail):
                _step(rows, st, src, 0, 1, 1, opt)
    return rows


def _mut(rows, pred, fn, start=0):
    r = copy.deepcopy(rows)
    for i in range(start, len(r)):
        if pred(r[i]):
            fn(r[i])
            return r, i
    return None, None


def _mx(x):
    return x['cycle'] > 0 and x['inputs']['rst'] == 0 and x['pre']['m_valid'] == 1 and x['inputs']['m_ready'] == 1


def _hx(x):
    return x['cycle'] > 0 and x['inputs']['rst'] == 0 and x['pre']['h_valid'] == 1 and x['inputs']['h_ready'] == 1


def _mb(x):
    return x['cycle'] > 0 and x['inputs']['rst'] == 0 and x['pre']['m_valid'] == 1 and x['inputs']['m_ready'] == 0


def _hb(x):
    return x['cycle'] > 0 and x['inputs']['rst'] == 0 and x['pre']['h_valid'] == 1 and x['inputs']['h_ready'] == 0


def _rst_row(x):
    return x['cycle'] > 0 and x['inputs']['rst'] == 1


def _sv_row(x):
    return x['cycle'] > 0 and x['inputs']['s_valid'] == 1


def _set_pre_mdata_x85(x):
    x['pre']['m_data'] = x['pre']['m_data'] ^ 85


def _set_pre_hpad_flip(x):
    x['pre']['h_pad'] = 1 - x['pre']['h_pad']


def _set_pre_holen_inc(x):
    x['pre']['h_original_length'] = x['pre']['h_original_length'] + 1


def _set_post_mdata_x1(x):
    x['post']['m_data'] = x['post']['m_data'] ^ 1


def _set_post_mvalid_0(x):
    x['post']['m_valid'] = 0


def _set_post_hlen_x1(x):
    x['post']['h_length'] = x['post']['h_length'] ^ 1


def _set_post_mvalid_1(x):
    x['post']['m_valid'] = 1


def _set_pre_mdata_unk(x):
    x['pre']['m_data'] = -1


def _set_pre_sready_unk(x):
    x['pre']['s_ready'] = -1


def _set_pre_mlast_unk(x):
    x['pre']['m_last'] = -1


def _bad_missing_field(r):
    del r[3]['post']['h_pad']


def _bad_width(r):
    r[3]['pre']['m_data'] = 300


def _bad_bool(r):
    r[3]['inputs']['m_ready'] = True


def _bad_cycle_gap(r):
    r[4]['cycle'] = 7


def _bad_missing_row_key(r):
    del r[2]['post']


def _bad_valid_in_reset(r):
    r[0]['inputs']['s_valid'] = 1


def run(checker_module):
    res = {}

    def v(rows, rd=False):
        try:
            out = checker_module.check_rows(rows, rd)
            if not isinstance(out, dict):
                return {'verdict': 'BAD', 'failures': [], 'unknown': []}
            return out
        except Exception:
            return {'verdict': 'EXC', 'failures': [], 'unknown': []}

    def t(name, fn):
        try:
            res[name] = bool(fn())
        except Exception:
            res[name] = False

    def cats(out):
        return [f.get('category', '') for f in out.get('failures', [])]

    L1 = [2, 5, 11, 8, 4, 1, 12, 3]
    base = _gen([L1])
    saf = _gen([L1], opt={'cut': False})
    ep = _gen([[3, 10, 6], [7, 2]], ep_cycles=(9,))
    epb = _gen([[3, 10, 6], [7, 2]], ep_cycles=(9,), block_early=True)

    t('pos_cut_through_drained', lambda: v(base, True)['verdict'] == 'PASS')
    t('pos_store_forward_drained', lambda: v(saf, True)['verdict'] == 'PASS')
    t('pos_reset_epochs_drained', lambda: v(ep, True)['verdict'] == 'PASS')
    t('pos_reset_cancels_blocked_responses', lambda: v(epb, True)['verdict'] == 'PASS')
    t('pos_all_prefixes_partial', lambda: all(v(base[:k])['verdict'] == 'PASS' for k in range(1, len(base) + 1)))
    t('pos_saf_all_prefixes_partial', lambda: all(v(saf[:k])['verdict'] == 'PASS' for k in range(1, len(saf) + 1)))
    t('partial_prefix_drained_fails', lambda: v(base[:9], True)['verdict'] == 'FAIL')
    t('short_tail_not_pass', lambda: v(base[:len(base) - 30], True)['verdict'] != 'PASS')

    def wrong_payload():
        r, i = _mut(base, _mx, _set_pre_mdata_x85)
        return r is not None and v(r)['verdict'] == 'FAIL'
    t('neg_wrong_payload', wrong_payload)

    def wrong_pad():
        r, i = _mut(base, _hx, _set_pre_hpad_flip)
        return r is not None and v(r)['verdict'] == 'FAIL'
    t('neg_wrong_status_pad', wrong_pad)

    def wrong_len():
        r, i = _mut(base, _hx, _set_pre_holen_inc)
        return r is not None and v(r)['verdict'] == 'FAIL'
    t('neg_wrong_status_length', wrong_len)

    t('neg_truncate_to_9', lambda: v(_gen([L1], opt={'maxo': 9}), True)['verdict'] == 'FAIL')
    t('neg_truncate_to_9_saf', lambda: v(_gen([L1], opt={'maxo': 9, 'cut': False}), True)['verdict'] == 'FAIL')
    t('neg_status_before_completion', lambda: v(_gen([L1], opt={'early_status': True}), True)['verdict'] == 'FAIL')

    def stab_data():
        r, i = _mut(base, _mb, _set_post_mdata_x1)
        if r is None:
            return False
        out = v(r)
        return out['verdict'] == 'FAIL' and any('stability' in c for c in cats(out))
    t('neg_data_stability_payload', stab_data)

    def stab_drop():
        r, i = _mut(base, _mb, _set_post_mvalid_0)
        return r is not None and v(r)['verdict'] == 'FAIL'
    t('neg_data_valid_dropped', stab_drop)

    def stab_status():
        r, i = _mut(base, _hb, _set_post_hlen_x1)
        if r is None:
            return False
        out = v(r)
        return out['verdict'] == 'FAIL' and any('stability' in c for c in cats(out))
    t('neg_status_stability', stab_status)

    def reset_valid():
        r, i = _mut(ep, _rst_row, _set_post_mvalid_1)
        return r is not None and v(r)['verdict'] == 'FAIL'
    t('neg_reset_leaves_valid', reset_valid)
    t('neg_reset_carries_old_epoch', lambda: v(_gen([[3, 10, 6], [7, 2]], ep_cycles=(9,), block_early=True, opt={'no_clear': True}), True)['verdict'] == 'FAIL')

    def unknown_payload():
        r, i = _mut(base, _mx, _set_pre_mdata_unk)
        return r is not None and v(r)['verdict'] == 'UNRESOLVED'
    t('unknown_payload_unresolved', unknown_payload)

    def fail_then_unknown():
        r, i = _mut(base, _mx, _set_pre_mdata_x85)
        if r is None:
            return False
        r2, j = _mut(r, _mx, _set_pre_mdata_unk, start=i + 1)
        if r2 is None:
            return False
        out = v(r2)
        return out['verdict'] == 'FAIL' and len(out['unknown']) > 0
    t('failure_preserved_with_later_unknown', fail_then_unknown)

    def x_reset():
        r = copy.deepcopy(base)
        r[5]['inputs']['rst'] = -1
        return v(r)['verdict'] == 'UNRESOLVED' and v(r, True)['verdict'] != 'PASS'
    t('unknown_reset_unresolved', x_reset)

    def x_sready():
        r, i = _mut(base, _sv_row, _set_pre_sready_unk)
        return r is not None and v(r)['verdict'] == 'UNRESOLVED'
    t('unknown_s_ready_unresolved', x_sready)

    def x_last():
        r, i = _mut(base, _mx, _set_pre_mlast_unk)
        return r is not None and v(r, True)['verdict'] == 'UNRESOLVED'
    t('unknown_m_last_unresolved', x_last)

    def bad(fn):
        r = copy.deepcopy(base)
        fn(r)
        return v(r)['verdict'] == 'INVALID_INPUT'
    t('malformed_missing_field', lambda: bad(_bad_missing_field))
    t('malformed_width', lambda: bad(_bad_width))
    t('malformed_bool', lambda: bad(_bad_bool))
    t('malformed_cycle_gap', lambda: bad(_bad_cycle_gap))
    t('malformed_missing_row_key', lambda: bad(_bad_missing_row_key))
    t('malformed_not_list', lambda: v('rows')['verdict'] == 'INVALID_INPUT')
    t('malformed_empty', lambda: v([])['verdict'] == 'INVALID_INPUT')
    t('assumption_valid_in_reset', lambda: bad(_bad_valid_in_reset))

    def no_mutation():
        r = copy.deepcopy(base)
        v(r, True)
        return r == base
    t('input_not_mutated', no_mutation)

    def schema():
        out = v(base, True)
        ok = set(out.keys()) >= {'verdict', 'failures', 'unknown', 'checked_rows'}
        return ok and isinstance(out['failures'], list) and isinstance(out['unknown'], list) and out['checked_rows'] == len(base)
    t('result_schema', schema)
    return res

