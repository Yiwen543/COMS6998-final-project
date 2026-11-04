from collections import deque

ERR_KEYS = ('nak', 'nak_timeout', 'arbitration', 'scl_interference', 'stretch_timeout', 'sda_unstable', 'unhandled_nak', 'unhandled_timeout')
HEAD = (('fmt_byte', 'byte'), ('fmt_start', 'start'), ('fmt_stop', 'stop'), ('fmt_read', 'read'), ('fmt_rcont', 'rcont'), ('fmt_nak_ok', 'nak'))


def _g(d, k, dv=0):
    if not isinstance(d, dict) or k not in d or d[k] is None:
        return dv
    try:
        return int(d[k])
    except (TypeError, ValueError):
        return dv


def check_rows(rows):
    F = []
    A = []
    U = []
    events = []
    cnt = {'rows': 0, 'pushes': 0, 'pops': 0, 'starts': 0, 'stops': 0, 'wire_bytes': 0, 'rx': 0, 'resets': 0}
    cmds = []
    q = deque()
    exp = deque()
    txns = []
    S = {'cur': 0, 'act': False, 'nb': 0, 'bits': [], 'ss': False, 'es': False, 'dir': None, 't': None, 'unsup': False}

    def fail(c, cat, d):
        F.append({'cycle': c, 'category': cat, 'detail': d})
        if S['t'] is not None:
            S['t']['clean'] = False

    def assume(c, d):
        A.append({'cycle': c, 'detail': d})
        if S['t'] is not None:
            S['t']['clean'] = False

    def unsup(c, d):
        if not S['unsup']:
            U.append({'cycle': c, 'kind': 'unsupported', 'detail': d})
        S['unsup'] = True
        if S['t'] is not None:
            S['t']['clean'] = False

    def curcmd():
        return cmds[S['cur']] if S['cur'] < len(cmds) else None

    def end_txn(c, kind):
        t = S['t']
        if t is not None:
            t['end'] = c
            t['kind'] = kind
        S['t'] = None

    def discard(c):
        nb = S['nb']
        if nb == 8:
            fail(c, 'truncated_byte', 'eight data bits without ninth bit at START/STOP')
        elif nb >= 2:
            fail(c, 'partial_byte', '%d data bits pending at START/STOP' % nb)
        S['nb'] = 0
        S['bits'] = []

    def on_start(c):
        cnt['starts'] += 1
        prev = None
        if S['act']:
            discard(c)
            if S['es'] and not S['unsup']:
                fail(c, 'missing_stop', 'repeated START where STOP flag required')
            prev = len(txns) - 1 if S['t'] is not None else None
            end_txn(c, 'restart')
        S['es'] = False
        t = {'start': c, 'end': None, 'kind': None, 'cmds': [], 'clean': not S['unsup'], 'prev': prev}
        txns.append(t)
        S.update(t=t, act=True, nb=0, bits=[], ss=True, dir=None)
        cc = curcmd()
        if cc is not None and cc['read'] and not S['unsup']:
            fail(c, 'start_in_read', 'START while READB entry %d is current (START ignored for READB)' % cc['id'])

    def on_stop(c):
        if not S['act']:
            return
        cnt['stops'] += 1
        discard(c)
        if not S['es'] and not S['unsup']:
            fail(c, 'unexpected_stop', 'STOP without a completed STOP-flag entry')
        end_txn(c, 'stop')
        S['act'] = False
        S['es'] = False

    def complete(cc):
        cc['complete'] = True
        S['cur'] += 1
        if cc['stop']:
            S['es'] = True

    def on_byte(c):
        b = 0
        for v in S['bits']:
            b = (b << 1) | (1 if v else 0)
        cnt['wire_bytes'] += 1
        if S['unsup']:
            return
        cc = curcmd()
        if cc is None:
            fail(c, 'byte_without_command', 'wire byte 0x%02x with no queued entry' % b)
            return
        if S['es']:
            fail(c, 'missing_stop', 'wire byte after STOP-flag entry completed')
        if not cc['read']:
            if bool(cc['start']) != bool(S['ss']):
                fail(c, 'start_flag', 'entry %d START flag %d vs START seen %d' % (cc['id'], cc['start'], int(S['ss'])))
            if b != cc['byte']:
                fail(c, 'write_data', 'entry %d wire 0x%02x expected 0x%02x' % (cc['id'], b, cc['byte']))
            if S['ss']:
                S['dir'] = b & 1
            elif S['dir'] == 1:
                assume(c, 'write data entry inside read-addressed transaction')
            S['t']['cmds'].append(cc['id'])
        else:
            if S['dir'] != 1:
                assume(c, 'READB not preceded by read-address write')
            if cc['done'] == 0:
                S['t']['cmds'].append(cc['id'])
            cc['done'] += 1
            cc['wire'].append(b)
            exp.append((b, cc['id']))
        S['ss'] = False

    def on_ack(c, v):
        if S['unsup']:
            return
        cc = curcmd()
        if cc is None:
            return
        if not cc['read']:
            if v and not cc['nak']:
                unsup(c, 'target NACK of write entry %d (out of ACKing-target profile)' % cc['id'])
                return
            complete(cc)
        else:
            if cc['done'] == 0:
                return
            last = cc['done'] == cc['n']
            want = 0 if (not last or cc['rcont']) else 1
            if v != want:
                cc['acks_ok'] = False
                fail(c, 'read_ack', 'entry %d byte %d ninth bit %s expected %s' % (cc['id'], cc['done'] - 1, 'NACK' if v else 'ACK', 'NACK' if want else 'ACK'))
            if last:
                complete(cc)

    def on_rise(c, v):
        if not S['act']:
            return
        S['nb'] += 1
        if S['nb'] <= 8:
            S['bits'].append(v)
            if S['nb'] == 8:
                on_byte(c)
        else:
            on_ack(c, v)
            S['nb'] = 0
            S['bits'] = []

    def sample(s):
        if S['act'] and _g(s, 'scl', 1) == 0 and _g(s, 'scl_pin', 0) == 1:
            cc = curcmd()
            if cc is not None and cc['read']:
                cc['stretched'] = True

    def edge(c, a, b):
        if a is None:
            return
        sa = _g(a, 'scl', 1)
        sb = _g(b, 'scl', 1)
        da = _g(a, 'sda', 1)
        db = _g(b, 'sda', 1)
        if sa and sb:
            if da and not db:
                on_start(c)
            elif db and not da:
                on_stop(c)
        elif sb and not sa:
            on_rise(c, db)

    def reset(c):
        cnt['resets'] += 1
        if S['act']:
            end_txn(c, 'reset')
        for cm in cmds:
            if not cm['popped']:
                cm['aborted'] = True
        q.clear()
        exp.clear()
        S.update(cur=len(cmds), act=False, nb=0, bits=[], ss=False, es=False, dir=None, t=None, unsup=False)

    prev = None
    c = 0
    for i, r in enumerate(rows):
        cnt['rows'] += 1
        c = r.get('cycle', i)
        a = r.get('action') or {}
        pre = r.get('pre') or {}
        post = r.get('post') or {}
        if _g(a, 'rst_n', 1) == 0:
            reset(c)
            prev = None
            continue
        # Actions are applied while the core clock is low, before pre settles:
        # flush/push take effect before the pre FIFO head is observed.
        if _g(a, 'flush'):
            if S['act']:
                assume(c, 'flush during active transaction')
            for cm in q:
                cm['aborted'] = True
            q.clear()
            S['cur'] = len(cmds)
        if _g(a, 'push'):
            rd = _g(a, 'read')
            fb = _g(a, 'byte') & 255
            cm = {'id': len(cmds), 'byte': fb, 'start': _g(a, 'start'), 'stop': _g(a, 'stop'), 'nak': _g(a, 'nak_ok'), 'read': rd, 'rcont': _g(a, 'rcont') if rd else 0, 'n': (fb or 256) if rd else 1, 'done': 0, 'rx': 0, 'wire': [], 'acks_ok': True, 'complete': False, 'popped': False, 'aborted': False, 'stretched': False, 'cycle': c}
            if rd and cm['nak']:
                assume(c, 'READB with NAKOK')
            if rd and cm['rcont'] and cm['stop']:
                assume(c, 'READB with RCONT and STOP')
            cmds.append(cm)
            q.append(cm)
            cnt['pushes'] += 1
        if _g(a, 'target_ack', 1) == 0:
            unsup(c, 'target_ack=0 outside ACKing-target profile')
        sample(pre)
        edge(c, prev, pre)
        if _g(pre, 'rx_valid'):
            cnt['rx'] += 1
            d = _g(pre, 'rx_data')
            if not S['unsup']:
                if not exp:
                    fail(c, 'extra_rx', 'RX 0x%02x with no decoded unreported read byte' % d)
                else:
                    b, cid = exp.popleft()
                    if b != d:
                        fail(c, 'rx_data', 'RX 0x%02x but wire byte 0x%02x (entry %d)' % (d, b, cid))
                    cmds[cid]['rx'] += 1
        if _g(pre, 'valid'):
            if not q:
                fail(c, 'fifo_head', 'valid with empty queued-command model')
            else:
                h = q[0]
                for k, f in HEAD:
                    if k in pre and _g(pre, k) != int(h[f]):
                        fail(c, 'fifo_head', '%s=%d expected %d for entry %d' % (k, _g(pre, k), int(h[f]), h['id']))
                if _g(pre, 'ready'):
                    h = q.popleft()
                    h['popped'] = True
                    cnt['pops'] += 1
                    if S['unsup']:
                        pass
                    elif not h['read']:
                        if not h['complete']:
                            fail(c, 'premature_pop', 'write entry %d popped before ninth bit' % h['id'])
                    elif h['done'] < h['n']:
                        fail(c, 'premature_pop', 'READB entry %d popped after %d of %d bytes' % (h['id'], h['done'], h['n']))
                    elif h['rx'] < h['n']:
                        fail(c, 'missing_rx', 'READB entry %d popped with %d of %d RX' % (h['id'], h['rx'], h['n']))
        edge(c, pre, post)
        sample(post)
        prev = post
        for k in ERR_KEYS:
            if _g(post, k):
                unsup(c, 'controller event ' + k)

    if S['act']:
        U.append({'cycle': c, 'kind': 'incomplete', 'detail': 'transaction open at end of trace'})
    if q:
        U.append({'cycle': c, 'kind': 'incomplete', 'detail': '%d queued entries not popped' % len(q)})
    if exp:
        U.append({'cycle': c, 'kind': 'incomplete', 'detail': '%d decoded read bytes awaiting RX' % len(exp)})

    def rd_ok(x):
        return x['complete'] and x['acks_ok'] and x['done'] == x['n'] and x['rx'] == x['n'] and x['popped'] and not x['aborted']

    def all_ok(cl):
        return bool(cl) and all((rd_ok(x) if x['read'] else (x['complete'] and x['popped'])) for x in cl)

    def ev(fam, s, e, cl):
        events.append({'family': fam, 'kind': 'complete', 'start_cycle': s, 'end_cycle': e, 'evidence': {'entries': [x['id'] for x in cl], 'read_bytes': [x['wire'] for x in cl if x['read']]}})

    if not F and not A:
        for idx, t in enumerate(txns):
            if not t['clean'] or t['kind'] not in ('stop', 'restart'):
                continue
            cl = [cmds[j] for j in t['cmds']]
            rd = [x for x in cl if x['read']]
            if not rd or not all_ok(cl):
                continue
            if t['kind'] == 'stop':
                if any(x['n'] >= 2 for x in rd):
                    ev('multi_byte_read', t['start'], t['end'], cl)
                if len(rd) >= 2 and all(x['rcont'] for x in rd[:-1]) and not rd[-1]['rcont']:
                    ev('rcont_chain', t['start'], t['end'], cl)
                if any(x['stretched'] for x in rd):
                    ev('read_stretch_recovery', t['start'], t['end'], cl)
            elif cl[-1] is rd[-1] and not rd[-1]['rcont'] and idx + 1 < len(txns):
                t2 = txns[idx + 1]
                cl2 = [cmds[j] for j in t2['cmds']]
                if t2['prev'] == idx and t2['clean'] and t2['kind'] == 'stop' and cl2 and not cl2[0]['read'] and cl2[0]['start'] and all_ok(cl2):
                    ev('read_then_restart', t['start'], t2['end'], cl + cl2)

    if A:
        verdict = 'invalid'
    elif F:
        verdict = 'fail'
    elif U:
        verdict = 'pending'
    else:
        verdict = 'pass'
    cnt['failures'] = len(F)
    cnt['events'] = len(events)
    return {'failures': F, 'assumption_violations': A, 'events': events, 'unresolved': U, 'verdict': verdict, 'counts': cnt}


