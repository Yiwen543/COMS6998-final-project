import collections


def _g(d, k, dv=0):
    if not isinstance(d, dict):
        return dv
    v = d.get(k, dv)
    return v if isinstance(v, int) else dv


HEAD = (('fmt_byte', 'byte'), ('fmt_start', 'start'), ('fmt_stop', 'stop'), ('fmt_nak_ok', 'nak_ok'))


def check_rows(rows):
    F = []
    A = []
    E = []
    U = []
    C = collections.Counter()
    S = {'fifo': collections.deque(), 'cons': 0, 'prev': None, 'txn': False, 'bits': [], 'pend': None,
         'sst': False, 'need': False, 'last': None, 'halt': None, 'st': None, 'pstr': 0, 'c': 0,
         'en': 1, 'toen': 0}

    def fail(cat, d):
        F.append({'cycle': S['c'], 'category': cat, 'detail': d})

    def ev(fam, kind, s, d):
        E.append({'family': fam, 'kind': kind, 'start_cycle': s, 'end_cycle': S['c'], 'evidence': d})

    def finalize(ack):
        val = 0
        for b in S['bits']:
            val = (val << 1) | (1 if b else 0)
        S['bits'] = []
        S['pend'] = None
        C['wire_bytes'] += 1
        h = S['halt']
        if h is not None and not h.get('clr'):
            fail('halt', 'byte 0x%02x transmitted while NACK-halted' % val)
        cmd = None
        if S['cons'] >= len(S['fifo']):
            fail('scoreboard', 'wire byte 0x%02x with no enqueued command' % val)
        else:
            cmd = S['fifo'][S['cons']]
            S['cons'] += 1
            if cmd['byte'] != val:
                fail('scoreboard', 'BYTE MISMATCH wire 0x%02x expected 0x%02x' % (val, cmd['byte']))
            if bool(cmd['start']) != S['sst']:
                fail('scoreboard', 'START flag %d but wire START %d before 0x%02x' % (cmd['start'], int(S['sst']), val))
        S['sst'] = False
        S['last'] = cmd
        S['need'] = bool(cmd and cmd['stop'])
        if ack:
            if cmd and cmd['nak_ok']:
                C['expected_nack'] += 1
                ev('expected_nack', 'event', S['c'], 'NAKOK byte 0x%02x NACKed (environment intent)' % val)
            else:
                C['unexpected_nack'] += 1
                S['need'] = False
                S['halt'] = {'c': S['c'], 'f': len(F), 'ph': 'ack'}
        else:
            if h is not None and S['halt'] is h and h.get('clr') and h.get('rs'):
                h['ok'] = 1
            st = S['st']
            if st and st['rel']:
                st['byte'] = 1

    def on_start():
        if S['bits']:
            fail('protocol', 'START inside byte after %d bits' % len(S['bits']))
        S['bits'] = []
        S['pend'] = None
        if S['need']:
            fail('scoreboard', 'missing STOP after STOP-flagged byte')
            S['need'] = False
        h = S['halt']
        if h is not None:
            if h.get('clr'):
                h['rs'] = 1
            else:
                fail('halt', 'START issued while halted before software clear')
        S['txn'] = True
        S['sst'] = True
        C['start'] += 1

    def on_stop():
        if S['bits']:
            fail('protocol', 'STOP inside byte after %d bits' % len(S['bits']))
        S['bits'] = []
        S['pend'] = None
        C['stop'] += 1
        h = S['halt']
        if h is not None and not h.get('clr'):
            if S['en'] == 0 or h.get('to') or S['toen']:
                h['stop'] = S['c']
            else:
                fail('halt', 'STOP during NACK halt without timeout or disable')
        elif h is not None and h.get('ok'):
            if len(F) == h['f'] and h.get('seen'):
                if h.get('stop'):
                    if h.get('to'):
                        ev('nak_timeout_recovery', 'success', h['c'], 'unexpected NACK, halt, timeout STOP+release, clear, START, clean byte, STOP')
                else:
                    ev('nak_restart', 'success', h['c'], 'unexpected NACK, SCL held, clear, repeated START, clean byte, STOP')
            S['halt'] = None
        elif h is None and S['txn']:
            if S['last'] is None or not S['last']['stop']:
                fail('scoreboard', 'STOP without STOP-flagged byte')
        S['need'] = False
        S['txn'] = False
        S['sst'] = False
        st = S['st']
        if st and st['byte']:
            if len(F) == st['f']:
                ev('stretch_recovery', 'success', st['c'], 'SCL extended by target while scl_pin=1, released, clean byte, STOP')
            S['st'] = None

    def on_rise(sda):
        if not S['txn']:
            fail('protocol', 'SCL pulse outside START/STOP transaction')
            return
        h = S['halt']
        if h is not None and h['ph'] == 'halted' and not h.get('clr') and not (h.get('to') or S['toen'] or S['en'] == 0):
            fail('halt', 'SCL released during NACK halt before clear/timeout')
        if len(S['bits']) == 8:
            finalize(sda)
        else:
            S['pend'] = sda

    def on_fall():
        h = S['halt']
        if h is not None and h['ph'] == 'ack':
            h['ph'] = 'halted'
        if S['pend'] is not None:
            if h is not None and not h.get('clr'):
                fail('halt', 'data bit clocked while halted')
            if S['need']:
                fail('scoreboard', 'missing STOP after STOP-flagged byte')
                S['need'] = False
            S['bits'].append(S['pend'])
            S['pend'] = None

    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            A.append({'cycle': idx, 'detail': 'row not a dict'})
            continue
        a = row.get('action', row.get('actions', {})) or {}
        pre = row.get('pre') or {}
        post = row.get('post') or {}
        cy = row.get('cycle', idx)
        S['c'] = cy if isinstance(cy, int) else idx
        for k in a:
            v = a[k]
            if not isinstance(v, int) or v < 0:
                A.append({'cycle': S['c'], 'detail': 'action %s not nonnegative int' % k})
        if _g(a, 'rst_n', 1) == 0:
            for ph in (pre, post):
                if _g(ph, 'scl_o', 1) == 0 or _g(ph, 'sda_o', 1) == 0:
                    fail('reset', 'controller drives bus low during reset')
            S.update(fifo=collections.deque(), cons=0, prev=None, txn=False, bits=[], pend=None,
                     sst=False, need=False, last=None, halt=None, st=None)
            continue
        S['en'] = _g(a, 'enable', 1)
        S['toen'] = _g(a, 'nak_timeout_enable', 0)
        stretch = 1 if _g(a, 'stretch', 0) else 0
        h = S['halt']
        fifo = S['fifo']
        if _g(a, 'flush'):
            if h is None and S['txn'] and _g(pre, 'idle', 1) == 0:
                A.append({'cycle': S['c'], 'detail': 'flush outside halted/idle context'})
            fifo.clear()
            S['cons'] = 0
        if _g(a, 'push'):
            if len(fifo) >= 64:
                A.append({'cycle': S['c'], 'detail': 'push into full FIFO'})
            else:
                fifo.append({'byte': _g(a, 'byte') & 255, 'start': 1 if _g(a, 'start') else 0,
                             'stop': 1 if _g(a, 'stop') else 0, 'nak_ok': 1 if _g(a, 'nak_ok') else 0})
        if _g(a, 'clear_events') and h is not None and not h.get('clr'):
            h['clr'] = S['c']
        if stretch and not S['pstr'] and S['prev'] is not None and S['prev'][0] == 1:
            A.append({'cycle': S['c'], 'detail': 'stretch asserted while SCL high'})
        S['pstr'] = stretch
        if S['st'] is not None and not stretch:
            S['st']['rel'] = 1
        if 'valid' in pre:
            if _g(pre, 'valid'):
                if not fifo:
                    fail('fifo', 'valid with empty model FIFO')
                else:
                    hd = fifo[0]
                    for ok_, mk in HEAD:
                        if ok_ in pre and _g(pre, ok_) != hd[mk]:
                            fail('fifo', 'head %s=%d model %d' % (ok_, _g(pre, ok_), hd[mk]))
                    if 'depth' in pre and _g(pre, 'depth') != len(fifo):
                        fail('fifo', 'depth %d model %d' % (_g(pre, 'depth'), len(fifo)))
            elif fifo:
                fail('fifo', 'valid low with nonempty FIFO')
            if _g(pre, 'ready') and _g(pre, 'valid') and fifo:
                if S['cons'] == 0:
                    fail('scoreboard', 'FMT pop before its byte appeared on wire')
                else:
                    S['cons'] -= 1
                fifo.popleft()
        h = S['halt']
        if h is not None:
            if _g(pre, 'nak') or _g(pre, 'unhandled_nak'):
                h['seen'] = 1
            if _g(pre, 'nak_timeout') or _g(pre, 'unhandled_timeout'):
                h['to'] = 1
        for ph in (pre, post):
            if 'scl' not in ph or 'sda' not in ph:
                continue
            scl = 1 if _g(ph, 'scl') else 0
            sda = 1 if _g(ph, 'sda') else 0
            if 'scl_pin' in ph and scl != ((1 if _g(ph, 'scl_pin') else 0) & (1 - stretch)):
                fail('bus', 'SCL != scl_pin & !stretch')
            if 'sda_pin' in ph and sda != ((1 if _g(ph, 'sda_pin') else 0) & (0 if _g(ph, 'target_low') else 1)):
                fail('bus', 'SDA != sda_pin & !target_low')
            if stretch and S['txn'] and _g(ph, 'scl_pin') == 1 and scl == 0 and S['st'] is None:
                S['st'] = {'c': S['c'], 'f': len(F), 'rel': 0, 'byte': 0}
            h = S['halt']
            if h is not None and h.get('stop') and not h.get('clr') and (scl == 0 or sda == 0):
                fail('timeout', 'bus not released after NACK-timeout STOP')
            pv = S['prev']
            S['prev'] = (scl, sda)
            if pv is None:
                continue
            if pv[0] == 1 and scl == 1 and pv[1] != sda:
                if sda == 0:
                    on_start()
                else:
                    on_stop()
            elif pv[0] == 0 and scl == 1:
                on_rise(sda)
            elif pv[0] == 1 and scl == 0:
                on_fall()
    if S['bits'] or S['pend'] is not None:
        U.append('partial wire byte pending')
    if S['txn']:
        U.append('transaction open (no STOP)')
    if S['halt'] is not None:
        U.append('NACK recovery incomplete from cycle %d' % S['halt']['c'])
    if S['st'] is not None:
        U.append('stretch recovery incomplete from cycle %d' % S['st']['c'])
    if S['fifo']:
        U.append('%d FMT entries pending' % len(S['fifo']))
    for e in E:
        C['event_' + e['family']] += 1
    verdict = 'fail' if F else ('invalid' if A else ('pending' if U else 'pass'))
    return {'failures': F, 'assumption_violations': A, 'events': E, 'unresolved': U,
            'verdict': verdict, 'counts': dict(C)}

