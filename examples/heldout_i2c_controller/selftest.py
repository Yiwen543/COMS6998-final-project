def run(check_rows):
    def fr(b, ack, start=True, stop=True):
        s = [(1, 1), (1, 0)] if start else []
        for i in range(7, -1, -1):
            x = (b >> i) & 1
            s += [(0, x), (1, x), (0, x)]
        s += [(0, ack), (1, ack), (0, ack)]
        if stop:
            s += [(0, 0), (1, 0), (1, 1)]
        return [(p, q, {}, 0, {}) for p, q in s]

    def P(b, s, p):
        return {'push': 1, 'byte': b, 'start': s, 'stop': p, 'nak_ok': 0}

    def build(seq):
        rows = []
        q = []
        for i, item in enumerate(seq):
            scl, sda, act, rdy, ex = item
            if act.get('flush'):
                q = []
            if act.get('push'):
                q.append(act)
            d = {'scl': scl, 'sda': sda, 'scl_pin': scl, 'sda_pin': sda, 'target_low': 0, 'scl_o': scl,
                 'sda_o': sda, 'idle': 1, 'ready': rdy, 'valid': 1 if q else 0, 'depth': len(q)}
            if q:
                d.update(fmt_byte=q[0]['byte'], fmt_start=q[0]['start'], fmt_stop=q[0]['stop'], fmt_nak_ok=q[0]['nak_ok'])
            d.update(ex)
            a = dict(act)
            a.setdefault('rst_n', 1)
            a.setdefault('enable', 1)
            rows.append({'cycle': i, 'action': a, 'pre': dict(d), 'post': dict(d)})
            if rdy and q:
                q.pop(0)
        return rows

    R = [(1, 1, {'rst_n': 0}, 0, {}), (1, 1, {'rst_n': 0}, 0, {})]
    res = []

    def t(n, c):
        res.append({'name': n, 'pass': bool(c)})

    clean = R + [(1, 1, P(0x50, 1, 1), 0, {})] + fr(0x50, 0) + [(1, 1, {}, 1, {})]
    r = check_rows(build(clean))
    t('clean_write_0x50_pass', r['verdict'] == 'pass' and r['counts'].get('wire_bytes') == 1)
    wrong = R + [(1, 1, P(0x50, 1, 1), 0, {})] + fr(0x51, 0) + [(1, 1, {}, 1, {})]
    r = check_rows(build(wrong))
    t('wrong_byte_0x51_fails_mismatch', r['verdict'] == 'fail' and any('BYTE MISMATCH' in f['detail'] for f in r['failures']))
    rf = list(clean)
    rf[0] = (1, 1, {'rst_n': 0}, 0, {'scl_o': 0})
    r = check_rows(build(rf))
    t('reset_drive_fault', any(f['category'] == 'reset' for f in r['failures']))
    bf = list(clean)
    bf[4] = (1, 0, {}, 0, {'sda_pin': 1})
    r = check_rows(build(bf))
    t('bus_composition_fault', any(f['category'] == 'bus' for f in r['failures']))
    tr = R + [(1, 1, P(0x50, 1, 1), 0, {})] + fr(0x50, 0, stop=False)
    r = check_rows(build(tr))
    t('truncated_pending_no_events', r['verdict'] == 'pending' and not r['events'])
    ms = tr + [(0, 1, {}, 0, {}), (1, 1, {}, 0, {}), (1, 0, {}, 0, {})]
    r = check_rows(build(ms))
    t('missing_stop_fails', any('missing STOP' in f['detail'] for f in r['failures']))

    def nack(status, b0=0x50):
        return (R + [(1, 1, P(0x50, 1, 0), 0, {})] + fr(b0, 1, stop=False) +
                [(0, 1, {}, 0, {'nak': 1} if status else {}), (0, 1, {'clear_events': 1, 'flush': 1}, 0, {}),
                 (0, 1, P(0x52, 1, 1), 0, {}), (1, 1, {}, 0, {}), (1, 0, {}, 0, {})] +
                fr(0x52, 0, start=False) + [(1, 1, {}, 1, {})])
    r = check_rows(build(nack(True)))
    t('nak_restart_event', r['verdict'] == 'pass' and any(e['family'] == 'nak_restart' for e in r['events']))
    r = check_rows(build(nack(False)))
    t('nak_restart_needs_status', not any(e['family'] == 'nak_restart' for e in r['events']))
    t('missing_nak_status_not_pass', r['verdict'] != 'pass')
    r = check_rows(build(nack(True, 0x51)))
    t('first_nack_byte_mismatch_no_event', r['verdict'] == 'fail' and not r['events'])
    TE = {'nak_timeout_enable': 1}
    pt = (R + [(1, 1, P(0x50, 1, 0), 0, {})] + fr(0x50, 1, stop=False) +
          [(0, 1, dict(TE), 0, {'nak': 1}), (0, 0, dict(TE), 0, {}), (1, 0, dict(TE), 0, {}), (1, 1, dict(TE), 0, {})])
    r = check_rows(build(pt))
    t('premature_timeout_stop_fails', r['verdict'] == 'fail' and any(f['category'] == 'halt' for f in r['failures']) and not r['events'])
    hc = R + [(1, 1, P(0x50, 1, 0), 0, {})] + fr(0x50, 1, stop=False) + [(1, 1, {}, 0, {}), (0, 1, {}, 0, {})]
    r = check_rows(build(hc))
    t('scl_release_during_halt_fails', any(f['category'] == 'halt' for f in r['failures']))
    return res


