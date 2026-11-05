import collections
import math

CMD_F = ('csid', 'speed', 'write', 'read', 'length', 'keep_cs', 'clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol')
CFG_F = ('clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol')


def _ci(t):
    return int(math.ceil(t))


def check_rows(rows):
    F = []
    A = []
    U = []
    segs = []
    aborts = []
    cnt = {'rows': len(rows), 'tx_words_accepted': 0, 'rx_words_observed': 0}

    def fail(t, cat, d):
        F.append({'cycle': _ci(t), 'category': cat, 'detail': d})

    def av(t, cat, d):
        A.append({'cycle': _ci(t), 'category': cat, 'detail': d})

    def note(d):
        if d not in U:
            U.append(d)

    sdmap = {}
    for r in rows:
        sdmap[r['cycle']] = r['action'].get('sd', 0)
    st = {'hw': False, 'sw': False, 'swok': False, 'cmd_off': None, 'tx_off': None}

    def clear():
        st.update(q=collections.deque(), cur=None, prev=None, words=[], wi=0, bp=0,
                  rxexp=collections.deque(), blocked=False, fall={0: None, 1: None}, last_rise=None)
    clear()

    def start_reset(c, kind):
        cur = st['cur']
        if cur is not None and cur['edges'] > 0:
            aborts.append({'kind': kind, 'trig': c, 'rel': None, 'seg': cur})
            if kind == 'software':
                note('software reset hit in-flight segment %d: spec only requires ACTIVE/TXQD/RXQD to clear before release; TXQD/RXQD not visible at core pins; disposition of partially shifted or stalled data unspecified' % cur['id'])
        for s in segs:
            if not s['ab'] and (s['sdone'] is None or (not s['keep'] and s['rise'] is None) or any(w['obs'] is None for w in s['words'])):
                s['ab'] = True
        clear()

    def release(c):
        for ab in aborts:
            if ab['rel'] is None:
                ab['rel'] = c

    def mkseg(c, a):
        w = {0: 1, 1: 2, 2: 4}[a.get('speed', 0)]
        n = a.get('length', 0) + 1
        cfg = tuple(a.get(k, 0) for k in CFG_F)
        return {'id': len(segs), 'acc': c, 'csid': a.get('csid', 0), 'speed': a.get('speed', 0),
                'wr': a.get('write', 0), 'rd': a.get('read', 0), 'n': n, 'keep': a.get('keep_cs', 0),
                'cfg': cfg, 'half': cfg[0] + 1, 'w': w, 'edges': 0, 'total': 2 * n * 8 // w,
                'first': None, 'last': None, 'sdone': None, 'rise': None, 'txb': [], 'rxs': [],
                'words': [], 'bnd': None, 'starve': None, 'bpt': None, 'ab': False, 'unres': False}

    def fetch(t):
        W = st['words']
        while st['wi'] < len(W):
            wc, d, be = W[st['wi']]
            if wc >= t:
                return None, None
            # registered contract spi_host_core_public_contract_v2_lsb: lanes 0..3 ascending
            while st['bp'] < 4 and not (be >> st['bp']) & 1:
                st['bp'] += 1
            if st['bp'] < 4:
                b = (d >> (8 * st['bp'])) & 255
                st['bp'] += 1
                return b, wc
            st['wi'] += 1
            st['bp'] = 0
        return None, None

    def edge(t, s0, s1, mid):
        cur = st['cur']
        if cur is None:
            if not st['q']:
                fail(t, 'spurious_sck', 'SCK toggled with no accepted pending segment')
                return
            cur = st['q'].popleft()
            st['cur'] = cur
            prev = st['prev']
            f = st['fall'][cur['csid']]
            cont = f is None or (prev is not None and prev['last'] is not None and f < prev['last'])
            if cont:
                if not (prev is not None and prev['keep'] and prev['csid'] == cur['csid'] and prev['cfg'] == cur['cfg'] and prev['rise'] is None):
                    fail(t, 'cs_framing', 'segment %d started without a CSB assertion after the previous segment' % cur['id'])
                elif t - prev['last'] < cur['half']:
                    fail(t, 'sck_halfperiod', 'SCK half period shorter than CLKDIV+1 across CSAAT boundary')
            elif t - f < (cur['cfg'][2] + 1) * cur['half']:
                fail(t, 'csnlead', 'CSB fall to first SCK edge %.1f < (CSNLEAD+1)*(CLKDIV+1)' % (t - f))
            if s0['sck'] != cur['cfg'][6]:
                fail(t, 'cpol', 'SCK not at CPOL idle level before first edge of segment %d' % cur['id'])
        low = [i for i in (0, 1) if not (mid >> i) & 1]
        if low != [cur['csid']]:
            fail(t, 'cs_select', 'SCK edge while CSB selection %s != [%d]' % (low, cur['csid']))
        idx = cur['edges']
        lead = idx % 2 == 0
        exp_sck = (1 - cur['cfg'][6]) if lead else cur['cfg'][6]
        if s1['sck'] != exp_sck:
            fail(t, 'sck_phase', 'SCK edge direction inconsistent with CPOL')
        if cur['last'] is not None and t - cur['last'] < cur['half']:
            fail(t, 'sck_halfperiod', 'SCK half period %.1f < CLKDIV+1' % (t - cur['last']))
        beat = idx // 2
        w = cur['w']
        bpb = 8 // w
        bi = beat // bpb
        pos = beat % bpb
        mask = (1 << w) - 1
        if lead == (cur['cfg'][5] == 0):
            en = s0['sd_en']
            if cur['speed'] == 0 and (en >> 1) & 1:
                fail(t, 'sd_direction', 'SD[1] driven by host in Standard segment')
            if cur['wr']:
                if pos == 0:
                    b, wc = fetch(t)
                    if b is None:
                        fail(t, 'tx_underflow', 'SCK ticked for TX byte %d of segment %d with no accepted TX data' % (bi, cur['id']))
                    elif bi > 0 and cur['bnd'] is not None and wc >= cur['bnd'] and cur['starve'] is None:
                        cur['starve'] = (cur['bnd'], wc)
                    cur['txb'].append([b, 0])
                if en & mask != mask:
                    fail(t, 'sd_en_tx', 'TX data line not enabled at sampling edge')
                rec = cur['txb'][-1]
                rec[1] = (rec[1] << w) | (s0['sd'] & mask)
                if pos == bpb - 1 and rec[0] is not None and rec[0] != rec[1]:
                    fail(t, 'tx_payload', 'segment %d byte %d sent 0x%02x expected 0x%02x' % (cur['id'], bi, rec[1], rec[0]))
            if cur['rd']:
                if cur['speed'] > 0 and en & mask:
                    fail(t, 'sd_en_rx', 'host drives a data line during Dual/Quad RX sampling')
                row = _ci(t)
                fc = cur['cfg'][4]
                cur['rxs'].append((row, row + (cur['half'] if fc else 1)))
                if pos == bpb - 1 and (bi % 4 == 3 or bi == cur['n'] - 1):
                    wr_ = {'seg': cur, 'b0': bi - bi % 4, 'b1': bi, 'ready': row + (cur['half'] if fc else 0), 'obs': None}
                    cur['words'].append(wr_)
                    st['rxexp'].append(wr_)
        cur['edges'] += 1
        cur['last'] = t
        if cur['edges'] % (16 // w) == 0:
            cur['bnd'] = t
        if cur['first'] is None:
            cur['first'] = t
        if cur['edges'] == cur['total']:
            cur['sdone'] = t
            if cur['wr'] and st['bp'] > 0:
                st['wi'] += 1
                st['bp'] = 0
            st['prev'] = cur
            st['cur'] = None

    def fall(i, t, s1):
        st['fall'][i] = t
        nxt = st['cur'] or (st['q'][0] if st['q'] else None)
        if nxt is None:
            fail(t, 'cs_without_command', 'CSB[%d] asserted with no accepted segment' % i)
            return
        if nxt['csid'] != i:
            fail(t, 'cs_wrong_line', 'CSB[%d] asserted for segment targeting CSID %d' % (i, nxt['csid']))
        if st['last_rise'] is not None and t - st['last_rise'] < (nxt['cfg'][1] + 1) * nxt['half']:
            fail(t, 'csnidle', 'CSB idle %.1f < (CSNIDLE+1)*(CLKDIV+1)' % (t - st['last_rise']))
        if s1['sck'] != nxt['cfg'][6]:
            fail(t, 'cpol', 'SCK not at CPOL level at CSB assertion')

    def rise(i, t):
        st['last_rise'] = t
        cur = st['cur']
        if cur is not None and cur['csid'] == i:
            fail(t, 'cs_rise_midsegment', 'CSB[%d] deasserted inside segment %d' % (i, cur['id']))
            return
        p = st['prev']
        if p is not None and p['csid'] == i and p['rise'] is None:
            p['rise'] = t
            if t - p['last'] < (p['cfg'][3] + 1) * p['half']:
                fail(t, 'csntrail', 'last SCK edge to CSB rise %.1f < (CSNTRAIL+1)*(CLKDIV+1)' % (t - p['last']))
            if p['keep']:
                if st['q']:
                    n = (st['q'][0]['csid'], st['q'][0]['cfg'])
                elif st['cmd_off'] is not None:
                    n = (st['cmd_off'][0], tuple(st['cmd_off'][6:]))
                else:
                    n = None
                if n is None or (n[0] == p['csid'] and n[1] == p['cfg']):
                    fail(t, 'csaat', 'CSB deasserted after CSAAT segment without CSID/config change')
        else:
            fail(t, 'cs_rise_without_transfer', 'CSB[%d] deasserted without a completed segment' % i)

    def trans(s0, s1, t, quiet):
        c0 = s0['csb'] & 3
        c1 = s1['csb'] & 3
        if quiet or st['blocked']:
            if c1 & ~c0 & 3:
                st['last_rise'] = t
            return
        for i in (0, 1):
            if (c0 >> i) & 1 and not (c1 >> i) & 1:
                fall(i, t, s1)
        mid = c0 & c1
        if mid == 0:
            fail(t, 'multi_cs', 'both CSB lines asserted')
        if s0['sck'] != s1['sck']:
            edge(t, s0, s1, mid)
        for i in (0, 1):
            if not (c0 >> i) & 1 and (c1 >> i) & 1:
                rise(i, t)

    prev_post = None
    for r in rows:
        c = r['cycle']
        a = r['action']
        pre = r['pre']
        post = r['post']
        hwr = not a.get('rst_n', 1)
        swr = bool(a.get('sw_reset', 0)) and not hwr
        cf = tuple(a.get(k, 0) for k in CMD_F)
        tf = (a.get('tx_data', 0), a.get('tx_be', 0))
        if hwr or swr:
            st['cmd_off'] = None
            st['tx_off'] = None
        else:
            if st['cmd_off'] is not None and (not a.get('valid', 0) or cf != st['cmd_off']):
                av(c, 'cmd_transport', 'offered command withdrawn or changed before pre ready&valid handshake')
            if st['tx_off'] is not None and (not a.get('tx_valid', 0) or tf != st['tx_off']):
                av(c, 'tx_transport', 'offered TX word withdrawn or changed before pre ready&valid handshake')
        if hwr:
            if not st['hw']:
                start_reset(c, 'hardware')
                st['hw'] = True
            if (post['csb'] & 3) != 3:
                fail(c, 'reset_csb', 'CSB asserted while rst_n low')
            prev_post = post
            continue
        if st['hw']:
            st['hw'] = False
            release(c)
        if st['sw'] and not swr:
            if not st['swok']:
                av(c, 'sw_reset_protocol', 'SW_RST released before ACTIVE=0 and all CSB idle were observed')
            st['sw'] = False
            release(c)
        if prev_post is not None:
            trans(prev_post, pre, c - 0.5, st['sw'])
        if swr and not st['sw']:
            start_reset(c, 'software')
            st['sw'] = True
            st['swok'] = False
        if st['sw']:
            if a.get('valid', 0) and pre['ready']:
                av(c, 'sw_reset_protocol', 'command offered and ready during SW_RST')
            if a.get('tx_valid', 0) and pre['tx_ready']:
                av(c, 'sw_reset_protocol', 'TX word offered and ready during SW_RST')
            if pre['rx_valid'] and a.get('rx_ready', 0):
                note('RX word handshaked during software reset at cycle %d: content not judged' % c)
            if not post['active'] and (post['csb'] & 3) == 3:
                st['swok'] = True
            trans(pre, post, c, True)
            prev_post = post
            continue
        if a.get('valid', 0) and pre['ready']:
            sp = a.get('speed', 0)
            wr = a.get('write', 0)
            rd = a.get('read', 0)
            if sp == 3 or (wr and rd and sp != 0):
                av(c, 'unsupported_command', 'reserved speed or non-Standard bidirectional segment; checking blocked until reset')
                st['blocked'] = True
            elif not wr and not rd:
                note('dummy segment accepted at cycle %d: legal but outside checker scope (dummy cycle count not in supplied spec); serial checking suspended until reset' % c)
                st['blocked'] = True
            else:
                s = mkseg(c, a)
                segs.append(s)
                st['q'].append(s)
            st['cmd_off'] = None
        elif a.get('valid', 0):
            st['cmd_off'] = cf
        else:
            st['cmd_off'] = None
        if a.get('tx_valid', 0) and pre['tx_ready']:
            st['words'].append((c, a.get('tx_data', 0), a.get('tx_be', 0)))
            cnt['tx_words_accepted'] += 1
            st['tx_off'] = None
        elif a.get('tx_valid', 0):
            st['tx_off'] = tf
        else:
            st['tx_off'] = None
        if pre['rx_valid'] and a.get('rx_ready', 0):
            cnt['rx_words_observed'] += 1
            if st['rxexp']:
                rec = st['rxexp'].popleft()
                rec['obs'] = (c, pre['rx_data'])
                if c <= rec['ready']:
                    fail(c, 'rx_premature', 'RX word delivered before its last byte was sampled')
            else:
                fail(c, 'rx_unexpected_word', 'RX word 0x%08x with no corresponding received bytes' % pre['rx_data'])
        cur = st['cur']
        if pre['rx_valid'] and not a.get('rx_ready', 0) and cur is not None and cur['rd'] and cur['edges'] > 0 and cur['bpt'] is None:
            cur['bpt'] = c
        if cur is not None and cur['first'] is not None and c > cur['first'] and not pre['active']:
            fail(c, 'active_low_inflight', 'ACTIVE low while segment %d is mid-transfer' % cur['id'])
        trans(pre, post, c, False)
        prev_post = post

    cs = st['cur']
    if cs is not None and cs['wr'] and cs['starve'] is None and cs['edges'] > 0 and cs['edges'] % (16 // cs['w']) == 0 and st['wi'] >= len(st['words']):
        cs['starve'] = (cs['last'], None)
    if st['cur'] is not None:
        note('segment %d incomplete at end of trace' % st['cur']['id'])
    for s in st['q']:
        note('segment %d accepted but not started at end of trace' % s['id'])
    p = st['prev']
    if p is not None and not p['keep'] and p['rise'] is None and not p['ab']:
        note('segment %d: CSB deassertion not yet observed (no deadline specified)' % p['id'])
    if st['hw'] or st['sw']:
        note('trace ends with reset asserted')

    for s in segs:
        if not s['rd']:
            continue
        w = s['w']
        bpb = 8 // w
        vals = []
        for (row, due) in s['rxs']:
            seq = [sdmap.get(k) for k in range(row, due + 1)]
            if any(v is None for v in seq):
                vals.append(None)
                continue
            lane = [((v >> 1) & 1) if w == 1 else (v & ((1 << w) - 1)) for v in seq]
            vals.append(lane[0] if all(x == lane[0] for x in lane) else None)
        byts = []
        for bi in range(len(vals) // bpb):
            ch = vals[bi * bpb:(bi + 1) * bpb]
            if None in ch:
                byts.append(None)
                continue
            b = 0
            for v in ch:
                b = (b << w) | v
            byts.append(b)
        for rec in s['words']:
            if rec['obs'] is None:
                if not s['ab']:
                    note('segment %d: RX word for bytes %d..%d not yet delivered' % (s['id'], rec['b0'], rec['b1']))
                continue
            oc, data = rec['obs']
            for k in range(4):
                bi = rec['b0'] + k
                exp = byts[bi] if bi <= rec['b1'] and bi < len(byts) else 0
                got = (data >> (8 * k)) & 255
                if exp is None:
                    s['unres'] = True
                    note('segment %d RX byte %d unresolved: SD input not stable over sampling window' % (s['id'], bi))
                elif exp != got:
                    fail(oc, 'rx_payload' if bi <= rec['b1'] else 'rx_padding', 'segment %d word byte %d got 0x%02x expected 0x%02x' % (s['id'], k, got, exp))

    def done(s):
        if s is None or s['ab'] or s['sdone'] is None or s['unres']:
            return None
        if not s['keep'] and s['rise'] is None:
            return None
        if any(w['obs'] is None for w in s['words']):
            return None
        if s['wr'] and any(b[0] is None for b in s['txb']):
            return None
        xs = [_ci(s['sdone'])] + [w['obs'][0] for w in s['words']]
        if s['rise'] is not None:
            xs.append(_ci(s['rise']))
        return max(xs)

    EV = []

    def ev(fam, s, e, evid):
        bad_f = any(x['cycle'] >= s and (e is None or x['cycle'] <= e) for x in F)
        bad_a = any(x['cycle'] >= s and (e is None or x['cycle'] <= e) for x in A)
        kind = 'fail' if bad_f else ('blocked' if bad_a else ('pending' if e is None else 'pass'))
        EV.append({'family': fam, 'kind': kind, 'start_cycle': s, 'end_cycle': e, 'evidence': evid})

    for s in segs:
        if s['starve'] is not None:
            ev('tx_starvation_resume', s['acc'], done(s), 'segment %d starved at byte boundary %.1f; next TX word accepted cycle %s; completion %s' % (s['id'], s['starve'][0], s['starve'][1], done(s)))
        if s['bpt'] is not None:
            ev('rx_backpressure_resume', s['acc'], done(s), 'segment %d RX word held (rx_valid & !rx_ready) mid-segment at %d' % (s['id'], s['bpt']))
        if s['rd'] and s['n'] % 4 and s['id'] + 1 < len(segs):
            nx = segs[s['id'] + 1]
            if s['keep'] and nx['csid'] == s['csid'] and nx['cfg'] == s['cfg']:
                var = 'held_cs'
            elif nx['csid'] != s['csid']:
                var = 'csid_change'
            else:
                var = None
            if var:
                d1 = done(s)
                d2 = done(nx)
                ev('partial_word_then_next_transaction', s['acc'], max(d1, d2) if d1 is not None and d2 is not None else None, '%s: segment %d (%d bytes) then segment %d' % (var, s['id'], s['n'], nx['id']))
    for ab in aborts:
        nx = None
        if ab['rel'] is not None:
            for s in segs:
                if s['acc'] >= ab['rel']:
                    nx = s
                    break
        ev('reset_abort_restart', ab['trig'], done(nx), '%s reset at %d aborted segment %d; release %s; fresh segment %s' % (ab['kind'], ab['trig'], ab['seg']['id'], ab['rel'], nx['id'] if nx else None))
        if ab['kind'] == 'software' and EV[-1]['kind'] == 'pass':
            EV[-1]['kind'] = 'pass_unresolved'

    if F:
        verdict = 'fail'
    elif A:
        verdict = 'blocked'
    elif U or any(e['kind'] != 'pass' for e in EV):
        verdict = 'inconclusive'
    else:
        verdict = 'pass'
    cnt.update(commands_accepted=len(segs), segments_completed=sum(1 for s in segs if done(s) is not None),
               failures=len(F), assumption_violations=len(A), unresolved=len(U),
               events_pass=sum(1 for e in EV if e['kind'] == 'pass'),
               events_fail=sum(1 for e in EV if e['kind'] in ('fail', 'blocked')),
               events_pending=sum(1 for e in EV if e['kind'] == 'pending'))
    return {'failures': F, 'assumption_violations': A, 'events': EV, 'unresolved': U, 'verdict': verdict, 'counts': cnt}


