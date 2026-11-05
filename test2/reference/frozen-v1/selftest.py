from collections import deque
import copy


def run(check_rows):
    def gen(acts):
        q = deque()
        rows = []

        def ob():
            n = len(q)
            return {'fill': n, 'full': int(n == 16), 'empty': int(n == 0), 'data': q[0] if n else 0}
        for i, (rs, w, r, d) in enumerate(acts):
            pre = ob()
            if rs:
                q.clear()
            else:
                n = len(q)
                if r and n:
                    q.popleft()
                if w and n < 16:
                    q.append(d)
            rows.append({'cycle': i, 'action': {'reset': rs, 'wr': w, 'rd': r, 'data': d}, 'pre': pre, 'post': ob()})
        return rows

    acts = [(1, 0, 0, 0)] + [(0, 1, 0, i + 1) for i in range(18)] + [(0, 1, 1, 99)] + [(0, 0, 1, 0)] * 17 + [(0, 1, 1, 5)] + [(0, 1, 0, 7), (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]
    base = gen(acts)
    results = {}
    allok = [True]

    def t(name, rows, want):
        try:
            got = check_rows(rows)['verdict']
        except Exception as e:
            got = 'EXC:' + repr(e)
        results[name] = (got, want)
        if got != want:
            allok[0] = False

    def m(f):
        r = copy.deepcopy(base)
        f(r)
        return r

    t('legal', base, 'PASS')
    t('first_pre_garbage', m(lambda r: r[0]['pre'].update({'fill': 31, 'full': 1, 'empty': 1, 'data': -1})), 'PASS')
    t('empty_data_unspecified', m(lambda r: r[0]['post'].update({'data': 123})), 'PASS')
    t('wrong_fill', m(lambda r: r[5]['post'].update({'fill': 4})), 'FAIL')
    t('wrong_data_order', m(lambda r: r[22]['pre'].update({'data': 9})), 'FAIL')
    t('full_flag_missing', m(lambda r: r[16]['post'].update({'full': 0})), 'FAIL')
    t('write_on_full_accepted', m(lambda r: r[17]['post'].update({'fill': 17})), 'FAIL')
    t('empty_flag_wrong', m(lambda r: r[0]['post'].update({'empty': 0})), 'FAIL')
    t('reset_pre_timing', m(lambda r: r[40]['pre'].update({'fill': 0, 'empty': 1})), 'FAIL')
    t('reset_post_not_empty', m(lambda r: r[40]['post'].update({'fill': 1})), 'FAIL')
    t('unknown', m(lambda r: r[3]['post'].update({'data': -1})), 'UNRESOLVED')

    def both(r):
        r[3]['post']['data'] = -1
        r[8]['post']['fill'] = 0
    t('fail_dominates_unknown', m(both), 'FAIL')
    t('no_initial_reset', m(lambda r: r[0]['action'].update({'reset': 0})), 'INVALID_INPUT')
    t('reset_with_write', m(lambda r: r[40]['action'].update({'wr': 1})), 'INVALID_INPUT')
    t('missing_row', m(lambda r: r.pop(3)), 'INVALID_INPUT')

    def swap(r):
        r[3], r[4] = r[4], r[3]
    t('out_of_order', m(swap), 'INVALID_INPUT')
    t('data_width', m(lambda r: r[2]['action'].update({'data': 256})), 'INVALID_INPUT')
    t('extra_field', m(lambda r: r[2]['action'].update({'x': 0})), 'INVALID_INPUT')
    t('missing_field', m(lambda r: r[2]['post'].pop('empty')), 'INVALID_INPUT')
    t('unknown_input', m(lambda r: r[2]['action'].update({'wr': -1})), 'INVALID_INPUT')
    t('empty_rows', [], 'INVALID_INPUT')
    return {'passed': allok[0], 'results': results}

