import collections
import copy

DEFAULT_LIMITS = {'MAX_HYP': 4096, 'MAX_LIVE_PER_MASTER': 64, 'MAX_CANCELED_POOL': 256}
LW = {'i_mcyc': 1, 'i_mstb': 1, 'i_mwe': 1, 'i_maddr': 8, 'i_mdata': 32, 'i_msel': 4, 'i_sstall': 1, 'i_sack': 1, 'i_sdata': 32, 'i_serr': 1, 'o_mstall': 1, 'o_mack': 1, 'o_mdata': 32, 'o_merr': 1, 'o_scyc': 1, 'o_sstb': 1, 'o_swe': 1, 'o_saddr': 8, 'o_sdata': 32, 'o_ssel': 4}
IN_KEYS = ['i_reset', 'i_mcyc', 'i_mstb', 'i_mwe', 'i_maddr', 'i_mdata', 'i_msel', 'i_sstall', 'i_sack', 'i_sdata', 'i_serr']
OUT_KEYS = ['o_mstall', 'o_mack', 'o_mdata', 'o_merr', 'o_scyc', 'o_sstb', 'o_swe', 'o_saddr', 'o_sdata', 'o_ssel']
CTRL_IN = ['i_reset', 'i_mcyc', 'i_mstb', 'i_sstall', 'i_sack', 'i_serr']
CTRL_OUT = ['o_mstall', 'o_mack', 'o_merr', 'o_scyc', 'o_sstb']
CLAUSES = ['K1_reset', 'K2_accept_identity', 'K3_routing', 'K4_no_invention_multiplicity', 'K5_forward_order', 'K6_response_order', 'K7_ack_basis_read_data', 'K8_errors', 'K9_cancellation_orphans', 'K10_dut_master_handshake', 'K11_env', 'K12_batch_end', 'K13_response_without_cyc']
ASSOC = ['K4_no_invention_multiplicity', 'K6_response_order', 'K7_ack_basis_read_data', 'K8_errors', 'K9_cancellation_orphans', 'K12_batch_end']
TAG_CLAUSE = {'post_abort_forward': 'K9_cancellation_orphans', 'unexplained_mapped_err': 'K8_errors', 'possible_starvation_err': 'K6_response_order', 'starvation_attributed': 'K6_response_order', 'same_edge_response_after_abort': 'K13_response_without_cyc'}
HR_NOTE = 'Repeated HR ERRs during one held request are absorbed by branch B and are not judged; they stay unknown.'
EXCLUSIONS = [
    'K5 forward and side-effect order (within one slave and across slaves) is not judged; no pass asserts order preservation',
    'C1-C4 characterization (restart-safe noninterference, survivor set, forward order, timeout/starvation conditions and precedence) is unproved and excluded from every scoped_pass',
    HR_NOTE,
    'No liveness, latency, timeout deadline or eventual-ERR claim',
    'DUT o_mack/o_merr inside reset rows are judged only by K13 and rule 3.45',
    'Payload while STB is low, read data lanes on requests and SEL-disabled write lanes',
    'Write ACK data',
    'Rule 3.05 minimum reset length: one sampled reset row is taken as one complete cycle; shorter pulses are not observable in row traces',
    'Formal obligations F1-F8 are unproved targets',
]


SUBS = collections.OrderedDict([
    ('K1_reset_outputs', ('K1_reset', False)),
    ('K2_master_identity_env', ('K2_accept_identity', False)),
    ('K2_slave_identity', ('K2_accept_identity', False)),
    ('K3_routing', ('K3_routing', False)),
    ('K4_count_projection', ('K4_no_invention_multiplicity', False)),
    ('K4_candidate_consumption', ('K4_no_invention_multiplicity', True)),
    ('K6_count_bound', ('K6_response_order', False)),
    ('K6_attribution', ('K6_response_order', True)),
    ('K7_ack_basis', ('K7_ack_basis_read_data', True)),
    ('K8_attribution', ('K8_errors', True)),
    ('K9_cancellation', ('K9_cancellation_orphans', True)),
    ('K10_handshake', ('K10_dut_master_handshake', False)),
    ('K11_env_checks', ('K11_env', False)),
    ('K10_rule_3_45', ('K10_dut_master_handshake', False)),
    ('K12_batch_end', ('K12_batch_end', True)),
    ('K13_response_without_cyc', ('K13_response_without_cyc', False)),
])


def _width(k):
    if k == 'i_reset':
        return 1
    return LW[k] * 2


def _lane(v, k, i):
    if v is None:
        return None
    w = LW[k]
    return (v >> (i * w)) & ((1 << w) - 1)


def _mask(sel):
    m = 0
    for i in range(4):
        if (sel >> i) & 1:
            m |= 0xff << (8 * i)
    return m


def _proj(we, a, sel, d):
    if we is None or a is None or sel is None:
        return None
    if we:
        if sel == 0:
            return (1, a, 0, 0)
        if d is None:
            return None
        return (1, a, sel, d & _mask(sel))
    return (0, a, sel, -1)


def _dec(a):
    if (a & 0xf0) == 0x00:
        return 0
    if (a & 0xf0) == 0x10:
        return 1
    return None


def _pstr(p):
    if p is None:
        return 'undefined/withdrawn'
    if p[0] == 0:
        return 'read addr=0x%02x sel=0x%x' % (p[1], p[2])
    return 'write addr=0x%02x sel=0x%x data(enabled lanes)=0x%08x' % (p[1], p[2], p[3])


def _validate(r, lastc):
    pe = []
    pd = []
    if not isinstance(r, dict):
        return None, ['row is not an object'], pd
    c = r.get('cycle')
    pre = r.get('pre')
    post = r.get('post')
    if isinstance(c, bool) or not isinstance(c, int):
        pe.append('cycle is not an integer')
        c = None
    elif lastc is not None and c != lastc + 1:
        pe.append('non-contiguous cycle numbering')
    if not isinstance(pre, dict) or not isinstance(post, dict):
        pe.append('pre or post is not an object')
        return c, pe, pd
    for name, src, keys in (('pre', pre, IN_KEYS + OUT_KEYS), ('post', post, OUT_KEYS)):
        for k in keys:
            if k not in src:
                pe.append('missing %s.%s' % (name, k))
                continue
            v = src[k]
            if v is None:
                if name == 'pre' and k in CTRL_IN:
                    pe.append('undefined control input pre.%s' % k)
                elif name == 'pre' and k in CTRL_OUT:
                    pd.append('pre.%s' % k)
                continue
            if isinstance(v, bool) or not isinstance(v, int) or v < 0 or v >= (1 << _width(k)):
                pe.append('out-of-range or non-integer %s.%s' % (name, k))
    return c, pe, pd


def _newh():
    return {'E': {}, 'mq': [[], []], 'pool': [], 'sq': [[], []], 'tags': []}


DISP = 16
WIT = 8


def _agg(H):
    agg = collections.OrderedDict()
    for h in H:
        seen = set()
        for t in h['tags']:
            key = (t[0], t[1], t[2])
            if key in seen:
                continue
            seen.add(key)
            agg[key] = agg.get(key, 0) + 1
    return agg


def _ack(h, eid, m, c, md):
    if eid is None:
        return ('K6: master %d ACK with no live entry accepted before cycle %s (invented)' % (m, c), 'K6_response_order')
    e = h['E'][eid]
    if e['map'] is None:
        return ('K8: master %d ACK retires unmapped entry accepted@%s' % (m, e['row']), 'K8_errors')
    st = e['st']
    if st == 'serr':
        return ('K8: master %d ACK retires slave-ERRed entry accepted@%s' % (m, e['row']), 'K8_errors')
    if st == 'scan':
        return ('K12: master %d ACK retires slave_canceled entry accepted@%s' % (m, e['row']), 'K12_batch_end')
    if st in ('unf', 'fwd'):
        return ('K7: master %d ACK retires entry accepted@%s without a bound slave ACK (state %s)' % (m, e['row'], st), 'K7_ack_basis_read_data')
    if e['idt'][0] == 0 and (md is None or md != e['sd']):
        return ('K7: master %d read data %r differs from bound slave ACK data %r (entry accepted@%s)' % (m, md, e['sd'], e['row']), 'K7_ack_basis_read_data')
    h['mq'][m].pop(0)
    e['loc'] = 'ret'
    return None


def _err(h, eid, m, c):
    e = h['E'][eid]
    h['mq'][m].pop(0)
    e['loc'] = 'ret'
    if e['map'] is None or e['st'] == 'serr':
        return
    h['tags'].append(['unexplained_mapped_err', c, 'master %d ERR retired mapped entry accepted@%s in state %s with no slave ERR; timeout/starvation conditions and precedence unknown' % (m, e['row'], e['st'])])


def check_rows(rows, limits=None):
    failures = []
    av = []
    unresolved = []
    events = []
    cnt = collections.Counter()
    lim = dict(DEFAULT_LIMITS)
    bad_lim = None
    if limits is not None:
        if not isinstance(limits, dict):
            bad_lim = 'limits must be a dictionary'
        else:
            for k in limits:
                v = limits[k]
                if k not in DEFAULT_LIMITS:
                    bad_lim = 'unknown limit name %r' % (k,)
                elif isinstance(v, bool) or not isinstance(v, int) or v < 1:
                    bad_lim = 'limit %s must be a positive integer' % k
                else:
                    lim[k] = v
    S = {'H': None, 'mode': 'pre_reset', 'rep': 0, 'mep': [0, 0], 'nid': 0,
         'idm': collections.Counter(), 'ids': collections.Counter(), 'sfq': [[], []],
         'cacc': [[], []], 'cack': [0, 0], 'cnon': [0, 0], 'chr': [0, 0],
         'susp': 0, 'dead': 0, 'exh': [], 'cl_unk': set(), 'cl_susp': set(),
         'e': None, 'prefix': None, 'rowtags': None, 'disc': [], 'sub': {}}
    alts = []

    def fail(c, cat, detail, pin, clauses):
        failures.append({'cycle': c, 'category': cat, 'detail': detail, 'pin': pin, 'clauses': list(clauses)})

    def env(c, cat, detail):
        av.append({'cycle': c, 'category': cat, 'detail': detail})

    def unr(c, item, detail, clause):
        unresolved.append({'cycle': c, 'item': item, 'detail': detail})
        if clause:
            S['cl_unk'].add(clause)

    def sub(name):
        d = S['sub'].setdefault(name, [0, 0, 0, 0])
        d[0] += 1
        if not SUBS[name][1] or S['mode'] == 'active':
            d[1] += 1
        elif S['mode'] == 'suspended':
            d[2] += 1
        else:
            d[3] += 1

    def sizes_of(H):
        live = 0
        pool = 0
        for h in H:
            for q in h['mq']:
                if len(q) > live:
                    live = len(q)
            if len(h['pool']) > pool:
                pool = len(h['pool'])
        return {'hypotheses': len(H), 'max_live_per_master': live, 'max_canceled_pool': pool}

    def exhaust(c, sz, point, projected=None):
        H0 = S['H'] or []
        agg0 = _agg(H0)
        n0 = len(H0)
        sz = dict(sz)
        pj = projected if projected is not None else n0
        sz['actual_hypotheses'] = n0
        sz['projected_hypotheses'] = pj
        for key in agg0:
            unr(key[1], key[0], '%s [class unknown; carried by %d of %d actual histories in the %s snapshot at cycle %s (projected hypothesis count %d); reset_epoch %d; retained pre-suspension evidence]' % (key[2], agg0[key], n0, point, c, pj, S['rep']), TAG_CLAUSE.get(key[0], 'unknown_tag'))
        alts.append({'reset_epoch': S['rep'], 'closed_at': c, 'reason': 'suspended_on_limit', 'snapshot': point, 'actual_hypotheses': n0, 'projected_hypotheses': pj, 'surviving_histories': n0, 'ownership': 'not_reported_suspended', 'histories_total': n0, 'histories_displayed': 0, 'histories_omitted': n0, 'tag_kinds_before_suspension': sorted(set(k[0] for k in agg0))})
        S['mode'] = 'suspended'
        S['H'] = None
        S['rowtags'] = None
        S['exh'].append({'cycle': c, 'reset_epoch': S['rep'], 'sizes': sz, 'snapshot': point, 'actual_hypotheses': n0, 'projected_hypotheses': pj})
        S['cl_susp'].update(ASSOC)
        unresolved.append({'cycle': c, 'item': 'unresolved_on_limit', 'detail': 'resource limit exceeded at cycle %s (%s snapshot; actual hypotheses %d, projected %d), sizes=%r, limits=%r; no pruning or branch selection; K4 per-candidate consumption, K6, K7, K8 attribution, K9 tags and K12 suspended for all masters until reset; earlier violations stay final' % (c, point, n0, pj, sz, lim)})

    def exhaust_check(c):
        if S['mode'] != 'active':
            return
        sz = sizes_of(S['H'])
        if sz['hypotheses'] > lim['MAX_HYP'] or sz['max_live_per_master'] > lim['MAX_LIVE_PER_MASTER'] or sz['max_canceled_pool'] > lim['MAX_CANCELED_POOL']:
            exhaust(c, sz, 'post_expansion_step_check')

    def death_check(c, wits):
        if S['mode'] == 'active' and not S['H']:
            S['mode'] = 'dead'
            cls = sorted(set(w[1] for w in wits))
            txt = '; '.join(w[0] for w in wits[:WIT]) + ' [witnesses shown %d of %d, omitted %d]' % (min(len(wits), WIT), len(wits), max(0, len(wits) - WIT))
            rt = S['rowtags']
            rn = 0
            if rt:
                ragg, rn = rt
                for key in ragg:
                    S['disc'].append({'reset_epoch': S['rep'], 'tag': key[0], 'tag_row': key[1], 'detail': key[2], 'carried_by': ragg[key], 'of_histories': rn, 'status': 'all carrying histories refuted at cycle %s by concrete pin contradiction; disclosure only, not an open unknown and not a hidden-owner fact' % c, 'death_cycle': c})
            alts.append({'reset_epoch': S['rep'], 'closed_at': c, 'reason': 'membership_dead', 'surviving_histories': 0, 'histories_alive_at_row_start': rn, 'dying_row_tags': 'not_captured: tags created in row %s by branches that all died in row %s are omitted' % (c, c), 'ownership': 'none_surviving', 'histories_total': 0, 'histories_displayed': 0, 'histories_omitted': 0})
            fail(c, 'membership_empty_H', 'no surviving explicit history at cycle %s; per-branch witnesses: %s; clauses used: %s (K4 per-candidate, K6, K7, K8 and K12 are inferred)' % (c, txt, ', '.join(cls)), False, cls)

    def close_epoch(c, end):
        if S['mode'] != 'active' or not S['H']:
            return
        H = S['H']
        n = len(H)
        S['rowtags'] = None
        agg = collections.OrderedDict()
        for h in H:
            seen = set()
            for t in h['tags']:
                key = (t[0], t[1], t[2])
                if key in seen:
                    continue
                seen.add(key)
                agg[key] = agg.get(key, 0) + 1
        for key in agg:
            unr(key[1], key[0], '%s [class unknown; carried by %d of %d surviving histories; reset_epoch %d]' % (key[2], agg[key], n, S['rep']), TAG_CLAUSE.get(key[0], 'unknown_tag'))
        pend = []
        scan = 0
        for h in H:
            p = 0
            for q in h['mq']:
                for eid in q:
                    if h['E'][eid]['st'] == 'scan':
                        scan += 1
                    else:
                        p += 1
            pend.append(p)
        alts.append({'reset_epoch': S['rep'], 'closed_at': c, 'reason': 'batch_end' if end else 'reset', 'surviving_histories': n, 'ownership': 'unique_by_elimination' if n == 1 else 'indistinguishable(%d)' % n, 'pending_live_per_history': pend[:DISP], 'tag_sets': [sorted(set(t[0] for t in h['tags'])) for h in H[:DISP]], 'histories_total': n, 'histories_displayed': min(n, DISP), 'histories_omitted': max(0, n - DISP)})
        if end:
            cnt['act_K12_batch_end'] += 1
            sub('K12_batch_end')
            if max(pend) > 0:
                unr(c, 'pending_at_batch_end', 'live entries not retired at trace end in surviving histories (min %d, max %d); inconclusive, never a liveness failure' % (min(pend), max(pend)), 'K12_batch_end')
            cnt['slave_canceled_live_at_end'] += scan
        else:
            cnt['live_discarded_by_reset'] += sum(pend) + scan

    def clean():
        if failures or unresolved or S['mode'] != 'active':
            return False
        for h in S['H']:
            if h['tags']:
                return False
            for q in h['mq']:
                for eid in q:
                    if h['E'][eid]['st'] != 'scan':
                        return False
        return True

    def new_epoch():
        S['H'] = [_newh()]
        S['mode'] = 'active'
        S['idm'] = collections.Counter()
        S['ids'] = collections.Counter()
        S['sfq'] = [[], []]
        S['cacc'] = [[], []]
        S['cack'] = [0, 0]
        S['cnon'] = [0, 0]
        S['chr'] = [0, 0]

    def boundary(c, nf, snap):
        S['e'] = c
        keep = failures[:nf]
        mixed = []
        for f in failures[nf:]:
            if f['pin']:
                keep.append(f)
            else:
                mixed.append(f)
        failures[:] = keep
        for f in mixed:
            unresolved.append({'cycle': c, 'item': 'mixed_same_edge', 'detail': 'mixed_same_edge(dut_candidate, env): %s: %s; no public ordering exists between this DUT candidate and the same-row input violation; unresolved for the DUT' % (f['category'], f['detail'])})
        mdeath = any(f['category'] == 'membership_empty_H' for f in mixed)
        if mdeath:
            S['disc'] = [d for d in S['disc'] if d.get('death_cycle') != c]
        rt = S['rowtags']
        S['rowtags'] = None
        if rt:
            ragg, rn = rt
            for key in ragg:
                unr(key[1], key[0], '%s [class unknown; valid-prefix tag carried by %d of %d histories feasible at the start of boundary row %s (snapshot before processing that row; tags created in row %s are not promoted); %s; reset_epoch %d]' % (key[2], ragg[key], rn, c, c, 'the membership death at that row is mixed_same_edge and is NOT a refutation' if mdeath else 'judgment stops at the first invalid input row', S['rep']), TAG_CLAUSE.get(key[0], 'unknown_tag'))
        if mdeath:
            for a in alts:
                if a.get('reason') == 'membership_dead' and a.get('closed_at') == c:
                    a['reason'] = 'membership_dead_mixed_same_edge'
                    a['ownership'] = 'withheld_mixed_same_edge'
        if nf > 0:
            S['prefix'] = 'prefix_dut_violation'
        elif snap:
            S['prefix'] = 'prefix_scoped_pass'
        else:
            S['prefix'] = 'prefix_unresolved'

    truncated = False
    lastc = None
    pp = None
    pp_reset = False
    seen_reset = False
    nrows = len(rows) if isinstance(rows, list) else 0
    if bad_lim:
        env(None, 'invalid_limits', bad_lim)
    elif not isinstance(rows, list) or not rows:
        env(None, 'K11_env_input_validity', 'empty or non-list trace')
    else:
        for idx in range(len(rows)):
            r = rows[idx]
            snap = clean()
            S['rowtags'] = (_agg(S['H']), len(S['H'])) if S['mode'] == 'active' and S['H'] else None
            nf = len(failures)
            na = len(av)
            c, pe, pd = _validate(r, lastc)
            if pe or pd:
                for d in pd:
                    fail(c, 'K10_dut_master_handshake', 'undefined DUT control output ' + d, True, ['K10_dut_master_handshake'])
                for d in pe:
                    env(c, 'K11_env_input_validity', d)
                if not pe:
                    truncated = True
                    unresolved.append({'cycle': c, 'item': 'unjudgeable_row', 'detail': 'undefined DUT control output; this and later rows are not judged'})
                    break
                boundary(c, nf, snap)
                break
            lastc = c
            cnt['total_rows'] += 1
            pre = r['pre']
            post = r['post']

            def g(k, i):
                return _lane(pre[k], k, i)

            def gp(k, i):
                return _lane(pp[k], k, i)

            reset = pre['i_reset'] == 1
            resp_done = [False, False]
            for m in (0, 1):
                ra = g('o_mack', m)
                re_ = g('o_merr', m)
                if ra and re_:
                    resp_done[m] = True
                    cnt['act_K10_dut_master_handshake'] += 1
                    sub('K10_rule_3_45')
                    fail(c, 'K10_dut_master_handshake', 'rule 3.45: o_mack and o_merr both high on master %d; response not attributed' % m, True, ['K10_dut_master_handshake'])
                elif (ra or re_) and not g('i_mcyc', m):
                    resp_done[m] = True
                    cnt['act_K13_response_without_cyc'] += 1
                    sub('K13_response_without_cyc')
                    if pp is None:
                        cnt['k13_unjudged_first_row'] += 1
                    elif not gp('i_mcyc', m):
                        fail(c, 'K13_response_without_cyc', 'master %d %s while pre i_mcyc is low in this row and the previous row (inferred K13)' % (m, 'ACK' if ra else 'ERR'), True, ['K13_response_without_cyc'])
                    else:
                        unr(c, 'same_edge_response_after_abort', 'master %d %s in the row where i_mcyc fell; never retired into work' % (m, 'ACK' if ra else 'ERR'), 'K13_response_without_cyc')
            if reset:
                cnt['reset_rows'] += 1
                cnt['act_K1_reset'] += 1
                sub('K1_reset_outputs')
                for k in ('o_scyc', 'o_sstb'):
                    v = post[k]
                    if v is None or v != 0:
                        fail(c, 'K1_reset', 'post %s=%r in a reset row' % (k, v), True, ['K1_reset'])
                if pp is not None and pp_reset and (pre['i_mcyc'] or pre['i_mstb']):
                    env(c, 'K1_reset', 'master CYC/STB high in a reset row that follows a reset row (rule 3.20)')
                if seen_reset:
                    close_epoch(c, False)
                seen_reset = True
                S['rep'] += 1
                new_epoch()
            elif not seen_reset:
                env(c, 'K11_env_input_validity', 'trace does not begin with reset')
            else:
                cnt['nonreset_rows'] += 1
                cnt['act_K11_env'] += 1
                sub('K11_env_checks')
                act = S['mode'] == 'active'
                mcyc = [g('i_mcyc', m) for m in (0, 1)]
                mstb = [g('i_mstb', m) for m in (0, 1)]
                mst = [g('o_mstall', m) for m in (0, 1)]
                mproj = [_proj(g('i_mwe', m), g('i_maddr', m), g('i_msel', m), g('i_mdata', m)) for m in (0, 1)]
                held = [bool(mcyc[m] and mstb[m] and mst[m]) for m in (0, 1)]
                acc = [bool(mcyc[m] and mstb[m] and not mst[m]) for m in (0, 1)]
                pheld = [False, False]
                pproj = [None, None]
                if pp is not None and not pp_reset:
                    for m in (0, 1):
                        pheld[m] = bool(gp('i_mcyc', m) and gp('i_mstb', m) and gp('o_mstall', m))
                        pproj[m] = _proj(gp('i_mwe', m), gp('i_maddr', m), gp('i_msel', m), gp('i_mdata', m))
                hr = [False, False]
                hr2 = [False, False]
                for m in (0, 1):
                    if held[m] or acc[m]:
                        cnt['act_K2_accept_identity'] += 1
                        sub('K2_master_identity_env')
                    if (held[m] or acc[m]) and mproj[m] is None:
                        env(c, 'K2_accept_identity', 'master %d strobed request with undefined identity projection' % m)
                    if pheld[m] and mcyc[m]:
                        if not mstb[m] or mproj[m] != pproj[m]:
                            env(c, 'K11_env', 'master %d changed or withdrew a stalled request while CYC stayed high (%s -> %s)' % (m, _pstr(pproj[m]), _pstr(mproj[m] if mstb[m] else None)))
                    hr2[m] = bool(acc[m] and pheld[m] and mproj[m] is not None and mproj[m] == pproj[m])
                    hr[m] = held[m] or hr2[m]
                # step 1: CYC drop
                for m in (0, 1):
                    if not mcyc[m]:
                        if pp is not None and gp('i_mcyc', m):
                            S['mep'][m] += 1
                            cnt['act_K9_cancellation_orphans'] += 1
                            sub('K9_cancellation')
                        S['cacc'][m] = []
                        S['cack'][m] = 0
                        S['cnon'][m] = 0
                        S['chr'][m] = 0
                        if act:
                            for h in S['H']:
                                for eid in h['mq'][m]:
                                    e = h['E'][eid]
                                    if e['st'] == 'unf':
                                        e['loc'] = 'pool'
                                        e['crow'] = c
                                        h['pool'].append(eid)
                                    elif e['st'] == 'fwd':
                                        e['loc'] = 'orph'
                                    else:
                                        e['loc'] = 'gone'
                                h['mq'][m] = []
                exhaust_check(c)
                act = S['mode'] == 'active'
                # step 2: master acceptances
                new_eid = [None, None]
                for m in (0, 1):
                    if acc[m] and mproj[m] is not None:
                        S['idm'][mproj[m]] += 1
                        S['cacc'][m].append(c)
                        cnt['master_accepted'] += 1
                        eid = S['nid']
                        S['nid'] += 1
                        new_eid[m] = eid
                        if act:
                            for h in S['H']:
                                h['E'][eid] = {'id': eid, 'm': m, 'idt': mproj[m], 'row': c, 'mep': S['mep'][m], 'rep': S['rep'], 'map': _dec(mproj[m][1]), 'st': 'unf', 'loc': 'live', 'starv': False, 'sd': None}
                                h['mq'][m].append(eid)
                exhaust_check(c)
                act = S['mode'] == 'active'
                # step 3: slave CYC withdrawal
                scyc = [g('o_scyc', s) for s in (0, 1)]
                for s in (0, 1):
                    if not scyc[s]:
                        if g('i_sack', s) or g('i_serr', s):
                            env(c, 'K11_env', 'slave %d response while pre o_scyc is low' % s)
                        S['sfq'][s] = []
                        if act:
                            for h in S['H']:
                                for eid in h['sq'][s]:
                                    if eid is None:
                                        continue
                                    e = h['E'][eid]
                                    if e['loc'] == 'live' and e['st'] == 'fwd':
                                        e['st'] = 'scan'
                                h['sq'][s] = []
                # step 4: slave responses
                for s in (0, 1):
                    sa = g('i_sack', s)
                    se = g('i_serr', s)
                    if not scyc[s] or not (sa or se):
                        continue
                    if sa and se:
                        env(c, 'K11_env', 'slave %d asserted ACK and ERR together' % s)
                        continue
                    if not S['sfq'][s]:
                        env(c, 'K11_env', 'slave %d response with an empty FIFO' % s)
                        continue
                    head = S['sfq'][s].pop(0)
                    cnt['slave_responses'] += 1
                    if sa and head[1] == 0 and g('i_sdata', s) is None:
                        env(c, 'K2_accept_identity', 'slave %d read ACK with undefined data; public per-slave FIFO head is the read forward accepted@%s (association-free)' % (s, head[0]))
                    if act:
                        for h in S['H']:
                            eid = h['sq'][s].pop(0)
                            if eid is None:
                                continue
                            e = h['E'][eid]
                            if e['loc'] == 'live' and e['st'] == 'fwd':
                                e['sr'] = c
                                if sa:
                                    e['st'] = 'sack'
                                    e['sd'] = g('i_sdata', s)
                                else:
                                    e['st'] = 'serr'
                # step 5: slave acceptances
                for s in (0, 1):
                    if not (scyc[s] and g('o_sstb', s) and not g('i_sstall', s)):
                        continue
                    sp = _proj(g('o_swe', s), g('o_saddr', s), g('o_ssel', s), g('o_sdata', s))
                    cnt['slave_accepted'] += 1
                    cnt['act_K2_accept_identity'] += 1
                    cnt['act_K3_routing'] += 1
                    cnt['act_K4_no_invention_multiplicity'] += 1
                    sub('K2_slave_identity')
                    sub('K3_routing')
                    S['sfq'][s].append((c, g('o_swe', s)))
                    if sp is None:
                        fail(c, 'K2_accept_identity', 'slave %d accepted request with undefined identity projection' % s, True, ['K2_accept_identity'])
                        if act:
                            for h in S['H']:
                                h['sq'][s].append(None)
                        continue
                    if _dec(sp[1]) != s:
                        fail(c, 'K3_routing', 'slave %d accepted %s whose decode is %r' % (s, _pstr(sp), _dec(sp[1])), True, ['K3_routing'])
                    S['ids'][sp] += 1
                    sub('K4_count_projection')
                    sub('K4_candidate_consumption')
                    if S['ids'][sp] > S['idm'][sp]:
                        fail(c, 'K4_count_projection', 'identity %s forwarded %d times but accepted %d times by masters in this reset epoch' % (_pstr(sp), S['ids'][sp], S['idm'][sp]), False, ['K4_no_invention_multiplicity'])
                    if not act:
                        continue
                    plans = []
                    total = 0
                    for h in S['H']:
                        cl = []
                        for m in (0, 1):
                            for eid in h['mq'][m]:
                                e = h['E'][eid]
                                if e['st'] == 'unf' and e['idt'] == sp:
                                    cl.append(eid)
                        for eid in h['pool']:
                            if h['E'][eid]['idt'] == sp:
                                cl.append(eid)
                        plans.append(cl)
                        total += len(cl)
                    if total > lim['MAX_HYP']:
                        sz = sizes_of(S['H'])
                        exhaust(c, sz, 'pre_expansion_branching_precheck', total)
                        act = False
                        continue
                    newH = []
                    wits = []
                    for j in range(len(S['H'])):
                        h = S['H'][j]
                        cl = plans[j]
                        if not cl:
                            wits.append(('K4: slave %d acceptance %s has no identity-equal live unforwarded or canceled-pool candidate' % (s, _pstr(sp)), 'K4_no_invention_multiplicity'))
                            continue
                        for k in range(len(cl)):
                            h2 = h if k == len(cl) - 1 else copy.deepcopy(h)
                            eid = cl[k]
                            e = h2['E'][eid]
                            if e['loc'] == 'pool':
                                h2['pool'].remove(eid)
                                e['loc'] = 'pfwd'
                                h2['tags'].append(['post_abort_forward', c, 'slave %d consumed canceled member of master %d accepted@%s master_epoch %d reset_epoch %d canceled@%s' % (s, e['m'], e['row'], e['mep'], e['rep'], e.get('crow'))])
                                if e['starv']:
                                    h2['tags'].append(['starvation_attributed', c, 'forward of a starvation-attributed member accepted@%s' % e['row']])
                            else:
                                e['st'] = 'fwd'
                                e['s'] = s
                                e['fr'] = c
                            h2['sq'][s].append(eid)
                            newH.append(h2)
                    S['H'] = newH
                    death_check(c, wits)
                    exhaust_check(c)
                    act = S['mode'] == 'active'
                # step 6: master responses
                for m in (0, 1):
                    if resp_done[m]:
                        continue
                    ra = g('o_mack', m)
                    re_ = g('o_merr', m)
                    if not (ra or re_):
                        continue
                    cnt['act_K6_response_order'] += 1
                    cnt['act_K8_errors'] += 1
                    sub('K6_count_bound')
                    sub('K6_attribution')
                    sub('K8_attribution')
                    if ra:
                        cnt['act_K7_ack_basis_read_data'] += 1
                        sub('K7_ack_basis')
                    nacc = len([x for x in S['cacc'][m] if x < c])
                    if ra:
                        S['cack'][m] += 1
                    elif hr[m]:
                        S['chr'][m] += 1
                        cnt['hr_err_unjudged'] += 1
                    else:
                        S['cnon'][m] += 1
                    if S['cack'][m] + S['cnon'][m] > nacc:
                        fail(c, 'K6_count_projection', 'master %d: ACKs (%d) + non-HR ERRs (%d) in current CYC exceed acceptances from earlier rows (%d); HR ERRs (%d) counted separately; driven by %s' % (m, S['cack'][m], S['cnon'][m], nacc, S['chr'][m], 'ACK (pins and rows < c only)' if ra else 'ERR (non-HR classification uses row-c inputs)'), bool(ra), ['K6_response_order'])
                    if not act:
                        continue
                    md = g('o_mdata', m)
                    newH = []
                    wits = []
                    for h in S['H']:
                        q = h['mq'][m]
                        old = q[0] if (q and h['E'][q[0]]['row'] < c) else None
                        if ra:
                            w = _ack(h, old, m, c, md)
                            if w is None:
                                newH.append(h)
                            else:
                                wits.append(w)
                        elif hr[m]:
                            if old is None:
                                wits.append(('K6 branch A: master %d ERR under HR has no live entry before cycle %s' % (m, c), 'K6_response_order'))
                            else:
                                ha = copy.deepcopy(h)
                                _err(ha, old, m, c)
                                newH.append(ha)
                            if hr2[m] and new_eid[m] is not None and new_eid[m] in h['mq'][m]:
                                hb2 = copy.deepcopy(h)
                                eid = new_eid[m]
                                hb2['mq'][m].remove(eid)
                                e = hb2['E'][eid]
                                e['crow'] = c
                                e['starv'] = True
                                if e['st'] == 'unf':
                                    e['loc'] = 'pool'
                                    hb2['pool'].append(eid)
                                else:
                                    e['loc'] = 'orph'
                                    hb2['tags'].append(['post_abort_forward', c, 'starvation-attributed row-%s entry of master %d was already forwarded in the same row' % (c, m)])
                                hb2['tags'].append(['starvation_attributed', c, 'branch B2: master %d row-%s entry treated as starvation-attributed canceled member; no claim that starvation occurred' % (m, c)])
                                hb2['tags'].append(['possible_starvation_err', c, 'master %d ERR at acceptance edge (HR case ii), branch B2' % m])
                                newH.append(hb2)
                            h['tags'].append(['possible_starvation_err', c, 'master %d ERR during held request (HR case %s), branch B retires nothing' % (m, 'ii' if hr2[m] else 'i')])
                            newH.append(h)
                        else:
                            if old is None:
                                wits.append(('K6: master %d ERR with no live entry before cycle %s and no HR' % (m, c), 'K6_response_order'))
                            else:
                                _err(h, old, m, c)
                                newH.append(h)
                    S['H'] = newH
                    death_check(c, wits)
                    exhaust_check(c)
                    act = S['mode'] == 'active'
                # step 7: association-free DUT handshake checks
                for s in (0, 1):
                    if g('o_sstb', s):
                        cnt['act_K10_dut_master_handshake'] += 1
                        sub('K10_handshake')
                    if g('o_sstb', s) and not scyc[s]:
                        fail(c, 'K10_dut_master_handshake', 'slave %d o_sstb without o_scyc' % s, True, ['K10_dut_master_handshake'])
                    sp = _proj(g('o_swe', s), g('o_saddr', s), g('o_ssel', s), g('o_sdata', s))
                    if scyc[s] and g('o_sstb', s) and g('i_sstall', s) and sp is None:
                        fail(c, 'K2_accept_identity', 'slave %d held strobed request with undefined identity projection' % s, True, ['K2_accept_identity'])
                    if pp is not None and not pp_reset and gp('o_scyc', s) and gp('o_sstb', s) and gp('i_sstall', s) and scyc[s]:
                        ps_ = _proj(gp('o_swe', s), gp('o_saddr', s), gp('o_ssel', s), gp('o_sdata', s))
                        if not g('o_sstb', s) or sp != ps_:
                            fail(c, 'K10_dut_master_handshake', 'slave %d stalled request changed or withdrawn while o_scyc stayed high (%s -> %s)' % (s, _pstr(ps_), _pstr(sp if g('o_sstb', s) else None)), True, ['K10_dut_master_handshake'])
                if S['mode'] == 'suspended':
                    S['susp'] += 1
                elif S['mode'] == 'dead':
                    S['dead'] += 1
            if len(av) > na:
                boundary(c, nf, snap)
                break
            pp = pre
            pp_reset = reset
    if S['e'] is None and not truncated and seen_reset and not av:
        if S['mode'] == 'active':
            close_epoch(lastc, True)
        else:
            sub('K12_batch_end')
    out_f = [{'cycle': f['cycle'], 'category': f['category'], 'detail': f['detail']} for f in failures]
    cl_fail = set()
    for f in failures:
        cl_fail.update(f['clauses'])
    for a in av:
        if a['category'] in ('K11_env', 'K11_env_input_validity'):
            cl_fail.add('K11_env')
    ps = {}
    for k in CLAUSES:
        if k == 'K5_forward_order':
            ps[k] = 'excluded_not_judged'
        elif k in cl_fail:
            ps[k] = 'violated' if k != 'K11_env' else 'env_violation_recorded'
        elif k in S['cl_susp']:
            ps[k] = 'suspended'
        elif k in S['cl_unk']:
            ps[k] = 'unresolved'
        elif cnt['act_' + k] == 0:
            ps[k] = 'not_activated'
        elif S['e'] is not None:
            ps[k] = 'prefix_checked_not_refuted'
        else:
            ps[k] = 'checked_not_refuted'
    ps['C1_C4_characterization'] = 'excluded_unproved'
    if out_f:
        verdict = 'dut_violation'
    elif av:
        verdict = 'input_or_scope_invalid'
    elif unresolved or truncated:
        verdict = 'unresolved'
    else:
        verdict = 'scoped_pass'
    nr = cnt['nonreset_rows']
    counts = dict(cnt)
    counts['property_status'] = ps
    counts['checked_scope'] = {'total_rows_in_trace': nrows, 'processed_rows': cnt['total_rows'], 'nonreset_rows': nr, 'suspended_rows': S['susp'], 'suspended_fraction': (float(S['susp']) / nr) if nr else 0.0, 'rows_after_membership_death': S['dead'], 'effective_association_checked_rows': nr - S['susp'] - S['dead'], 'exhaustions': S['exh'], 'rows_beyond_input_boundary': nrows - cnt['total_rows']}
    counts['input_validity_boundary'] = S['e']
    counts['prefix_status'] = S['prefix']
    counts['pending_alternatives'] = alts
    counts['declared_exclusions'] = list(EXCLUSIONS)
    counts['scoped_pass_excludes'] = ['K5_forward_order', 'C1', 'C2', 'C3', 'C4']
    counts['hr_err_note'] = HR_NOTE
    counts['limits'] = dict(lim)
    counts['reset_epochs'] = S['rep']
    counts['clause_activations'] = dict((k, cnt['act_' + k]) for k in CLAUSES if k != 'K5_forward_order')
    counts['discarded_epoch_evidence'] = list(S['disc'])
    counts['display_limits'] = {'histories': DISP, 'witnesses': WIT, 'note': 'displays only; histories are never pruned for reporting'}
    subo = collections.OrderedDict()
    for nm in SUBS:
        d = S['sub'].get(nm, [0, 0, 0, 0])
        subo[nm] = {'clause': SUBS[nm][0], 'association_dependent': SUBS[nm][1], 'activations': d[0], 'checked_activations': d[1], 'suspended_activations': d[2], 'post_death_activations': d[3]}
    counts['subobligation_activations'] = subo
    csc = collections.OrderedDict()
    for k in CLAUSES:
        if k == 'K5_forward_order':
            continue
        rec = {'raw_activations': cnt['act_' + k], 'activations': 0, 'checked_activations': 0, 'suspended_activations': 0, 'post_death_activations': 0, 'unknown_tag_records': len([u for u in unresolved if TAG_CLAUSE.get(u['item']) == k])}
        for nm in SUBS:
            if SUBS[nm][0] == k:
                for f in ('activations', 'checked_activations', 'suspended_activations', 'post_death_activations'):
                    rec[f] += subo[nm][f]
        csc[k] = rec
    counts['clause_scope'] = csc
    counts['scope_note'] = 'activations are exposure, not coverage; association-free sub-obligations are checked in every mode (suspended/post_death counts are 0 by definition); association-dependent ones count as checked only while the explicit history set is active; zero activation is never a pass, cover or proof claim'
    return {'failures': out_f, 'assumption_violations': av, 'unresolved': unresolved, 'events': events, 'verdict': verdict, 'counts': counts}

