import copy

# Scoped public-pin scoreboard for the spi_host_fsm command/clock/select boundary (NumCS=2).
# Authored only from the supplied specification excerpts and interface description.

IN_W = {'rst_n': 1, 'enable': 1, 'sw_reset': 1, 'valid': 1, 'csid': 1, 'speed': 2, 'write': 1, 'read': 1, 'length': 20, 'keep_cs': 1, 'clkdiv': 16, 'idle': 4, 'lead': 4, 'trail': 4, 'full_cycle': 1, 'cpha': 1, 'cpol': 1, 'tx_ready': 1, 'rx_ready': 1}
BIT_OUT = ['ready', 'sck', 'wr', 'rd', 'last_read', 'last_write', 'rx_stall', 'tx_stall', 'active']
CMD = ['csid', 'speed', 'write', 'read', 'length', 'keep_cs', 'clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol']
CFG = ['clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol']
LANES = {0: 1, 1: 2, 2: 4}

SCOPE = [
    'Only the spi_host_fsm command/clock/select boundary with NumCS=2 is checked; no register bus, FIFO, STATUS or payload/SD data checks.',
    'Byte accounting uses wr/rd pulses sampled in pre (before the rising edge) and last_write/last_read flags; serial bit content is not checked.',
    'Exact SCK edges per byte, CPHA/FULLCYC sampling phase and the sample/shift/sd_en/speed/full_cycle outputs are not checked; the cited text does not fix them cycle-exactly at this boundary.',
    'Dummy segments (write=read=0) have no externally countable handshakes; their completion is not tracked and switches involving them are not evaluated.',
    'CSNLEAD/CSNTRAIL/CSNIDLE are enforced only inside a witnessed constrained switch, as lower bounds in core cycles (half-SCK = CLKDIV+1 core cycles) with no tolerance.',
    'For a configuration change max(old,new) idle is enforced; a gap below old+new (theory_of_operation 326-329) is blocking unresolved for that switch.',
    'A switch is tracked from the first pending offer of a changed CSID/config after a CSAAT segment; old select may release before acceptance. Accept and first wr/rd may share an edge (command processed first).',
    'last flags are constrained only on handshake edges; their level elsewhere is unspecified and not checked.',
    'A software reset coincident with a stall indication suspends the scoreboard (reset-over-stall precedence is not established at this boundary) and makes the verdict unresolved.',
    'Asynchronous reset is checked for all-inactive selects and no handshakes in pre and post of reset rows; software reset is checked from its second consecutive held cycle.',
    'An operation counts as complete only with all bytes accounted, a later select release or later-segment handshake, and at least (LEN+1)*8/lanes SCK edges while it was the oldest open segment; unfinished operations at trace end are pending, never liveness failures.',
    'Documentation mismatch: theory_of_operation segment table lists LEN as 8 bits ([0:255]); registers.md and the public interface give 20 bits; 20 bits is used.',
    'enable (en_i) semantics are not given in the packet; it is not used to gate acceptance or progress.',
    'ready/active are never used as evidence of completion; register-bus STATUS semantics are not assumed to match this boundary.',
    'The active output and last flags without a handshake are out of scope; controls mutating only them are scope-confirming, not detection evidence.',
    'A single-cycle software reset pulse is not checked for select/handshake separation (only from the second held cycle).',
    'MODELLING ASSUMPTION (uncited): completion needs (LEN+1)*16/lanes SCK edges (8 bits, 2 edges/bit, 1/2/4 lanes) attributed to the oldest open segment.',
    'Events are emitted only if no failure or assumption violation lies in the inclusive [start_cycle,end_cycle] window.',
    'Switch trail uses the last SCK edge while the old CSID bit was low; lead uses the first SCK edge while the new CSID bit is low; edges of a queued segment under the old select are pin-indistinguishable.'
]


def _bit(v, i):
    return (v >> i) & 1


def check_rows(rows):
    F = []
    AV = []
    E = []
    U = []
    cnt = {'rows': 0, 'accepted': 0, 'wr': 0, 'rd': 0, 'sck_edges': 0, 'async_reset_rows': 0, 'sw_reset_rows': 0, 'stall_rows': 0, 'switches_offered': 0}

    def fail(c, cat, d):
        F.append({'cycle': c, 'category': cat, 'detail': d})

    def av(c, cat, d):
        AV.append({'cycle': c, 'category': cat, 'detail': d})

    def un(c, cat, d, blocking=False):
        U.append({'cycle': c, 'category': cat, 'detail': d, 'blocking': blocking})

    def wclean(s, e):
        return not any(isinstance(x.get('cycle'), int) and s <= x['cycle'] <= e for x in F + AV)

    def result():
        if AV:
            v = 'input_or_scope_invalid'
        elif F:
            v = 'dut_violation'
        elif any(u['blocking'] for u in U):
            v = 'unresolved'
        else:
            v = 'scoped_pass'
        cnt['failures'] = len(F)
        cnt['assumption_violations'] = len(AV)
        cnt['events'] = len(E)
        cnt['unresolved'] = len(U)
        fam = {}
        for e in E:
            key = e['family'] + ':' + e['kind']
            fam[key] = fam.get(key, 0) + 1
        cnt['event_kinds'] = fam
        return {'failures': F, 'assumption_violations': AV, 'events': E, 'unresolved': U, 'verdict': v, 'counts': cnt, 'scope_limitations': list(SCOPE)}

    if not isinstance(rows, list) or not rows:
        un(None, 'empty_trace', 'no rows supplied', True)
        return result()
    cnt['rows'] = len(rows)
    for i, r in enumerate(rows):
        if not isinstance(r, dict) or not isinstance(r.get('action'), dict) or not isinstance(r.get('pre'), dict) or not isinstance(r.get('post'), dict):
            av(i, 'malformed_row', 'row lacks action/pre/post dicts')
            continue
        c = r.get('cycle', i)
        for k, w in IN_W.items():
            v = r['action'].get(k)
            if not isinstance(v, int) or v < 0 or v >= (1 << w):
                av(c, 'input_encoding', 'action.%s=%r' % (k, v))
        for side in ('pre', 'post'):
            for k in BIT_OUT:
                v = r[side].get(k)
                if not isinstance(v, int) or v not in (0, 1):
                    av(c, 'output_encoding', '%s.%s=%r' % (side, k, v))
            v = r[side].get('csb')
            if not isinstance(v, int) or v < 0 or v > 3:
                av(c, 'output_encoding', '%s.csb=%r' % (side, v))
    if AV:
        return result()
    if len(rows) < 2 or rows[0]['action']['rst_n'] != 0 or rows[1]['action']['rst_n'] != 0:
        av(rows[0].get('cycle', 0), 'initial_reset', 'trace must begin with two rst_n=0 cycles (interface transport assumption)')

    segs = []
    switches = []
    st = {'nid': 0, 'cpol': None, 'susp': False, 'abort': None, 'restart': None, 'window': False, 'stall': None, 'prev_sw': False, 'last_edge': None, 'le': {0: None, 1: None}}

    def cur():
        for s in segs:
            if not s['dummy'] and s['done'] is None:
                return s
        return None

    def enough(s):
        return s['edges'] >= s['total'] * (16 // LANES.get(s['speed'], 1))

    def do_reset(c, kind):
        k = [s for s in segs if s['done'] is None and s['progress']]
        if k:
            st['abort'] = {'kind': kind, 'cycle': c, 'stale': False, 'nf': len(F), 'seg': k[0]['id']}
        st['restart'] = None
        for sw in switches:
            if sw['state'] == 'open':
                un(c, 'switch_interrupted', 'constrained switch from segment %d interrupted by %s; not counted' % (sw['A']['id'], kind))
        if st['stall'] is not None:
            un(c, 'stall_interrupted', 'stall on segment %d ended by %s; recovery not witnessed' % (st['stall']['seg']['id'], kind))
        del segs[:]
        del switches[:]
        st['stall'] = None
        st['window'] = True
        st['cpol'] = None

    def finalize(sw, c):
        A = sw['A']
        B = sw['B']
        O = sw['off']
        if sw['rise'] is None or sw['fall'] is None:
            fail(c, 'switch_fresh_idle', 'segment %d completed without release of old select and an all-high gap after CSAAT segment %d (theory_of_operation 204-208, 246-249)' % (B['id'], A['id']))
            sw['state'] = 'failed'
            return
        ho = A['clkdiv'] + 1
        hn = O['clkdiv'] + 1
        idle_old = (A['idle'] + 1) * ho
        idle_new = (O['idle'] + 1) * hn
        cfg = any(A[k] != O[k] for k in CFG)
        req = {'trail': (A['trail'] + 1) * ho, 'gap': max(idle_old, idle_new) if cfg else idle_new, 'lead': (O['lead'] + 1) * hn}
        bad = False
        for name in ('trail', 'gap', 'lead'):
            m = sw[name]
            b = req[name]
            if m is None:
                un(c, 'switch_timing_unobserved', '%s not observed for switch %d->%d' % (name, A['id'], B['id']))
                bad = True
            elif m < b:
                fail(c, 'switch_timing', '%s=%d core cycles < required %d (old trail, new idle/lead; theory_of_operation 206-208, 254-259, 321-332; registers.md CONFIGOPTS 224-245)' % (name, m, b))
                bad = True
        if cfg and sw['gap'] is not None and req['gap'] <= sw['gap'] < idle_old + idle_new:
            un(c, 'switch_idle_additive', 'gap=%d meets max(old,new)=%d but not old+new=%d; additive before/after idle reading (theory_of_operation 326-329) unresolved' % (sw['gap'], req['gap'], idle_old + idle_new), True)
            bad = True
        ws = sw['offer'] if A['done'] is None else min(A['done'], sw['offer'])
        if len(F) > sw['nf'] or not wclean(ws, c):
            bad = True
        if not enough(B):
            un(c, 'insufficient_serial_evidence', 'segment %d closed with only %d SCK edges observed' % (B['id'], B['edges']))
            bad = True
        sw['state'] = 'done'
        if not bad:
            if cfg and A['csid'] != B['csid']:
                kind = 'csid_and_config_change'
            elif A['csid'] != B['csid']:
                kind = 'csid_change'
            else:
                kind = 'config_change'
            E.append({'family': 'constrained_transaction_switch', 'kind': kind, 'start_cycle': ws, 'end_cycle': c,
                      'evidence': {'old_segment': A['id'], 'new_segment': B['id'], 'new_accept_cycle': sw['accept'], 'old_release_cycle': sw['rise'], 'new_select_cycle': sw['fall'],
                                   'trail': sw['trail'], 'gap': sw['gap'], 'lead': sw['lead'], 'required': req, 'additive_idle_reading': idle_old + idle_new, 'new_edges': B['edges']}})

    for i, r in enumerate(rows):
        c = r.get('cycle', i)
        a = r['action']
        p = r['pre']
        q = r['post']
        if a['rst_n'] == 0:
            cnt['async_reset_rows'] += 1
            if a['valid']:
                av(c, 'valid_during_reset', 'command valid asserted while rst_n=0')
            for side, o in (('pre', p), ('post', q)):
                if o['csb'] != 3:
                    fail(c, 'reset_separation', '%s.csb=%d during asynchronous reset (expected all inactive)' % (side, o['csb']))
                if o['wr'] or o['rd']:
                    fail(c, 'reset_separation', '%s wr/rd handshake during asynchronous reset' % side)
            do_reset(c, 'async_reset')
            st['susp'] = False
            st['prev_sw'] = False
            continue
        if a['sw_reset']:
            cnt['sw_reset_rows'] += 1
            if p['tx_stall'] or p['rx_stall']:
                if not st['susp']:
                    un(c, 'sw_reset_during_stall', 'software reset with stall indication; reset precedence over stall not established by cited spec at this boundary; scoreboard suspended until async reset or an unstalled software reset', True)
                st['susp'] = True
                del segs[:]
                del switches[:]
                st['stall'] = None
                st['abort'] = None
                st['restart'] = None
                st['window'] = True
                st['prev_sw'] = False
                continue
            if st['prev_sw']:
                if p['csb'] != 3:
                    fail(c, 'reset_separation', 'pre.csb=%d while software reset held for a further cycle' % p['csb'])
                if p['wr'] or p['rd']:
                    fail(c, 'reset_separation', 'wr/rd handshake while software reset held')
            do_reset(c, 'sw_reset')
            st['susp'] = False
            st['prev_sw'] = True
            continue
        st['prev_sw'] = False
        if st['susp']:
            continue

        accept = bool(a['valid'] and p['ready'])
        if a['valid']:
            if a['speed'] == 3:
                av(c, 'reserved_speed', 'speed=3 (RESERVED) offered')
            if a['write'] and a['read'] and a['speed'] != 0:
                av(c, 'illegal_bidir', 'bidirectional command offered at speed %d' % a['speed'])

        active_ids = set(s['csid'] for s in segs if s['closed'] is None)
        for side, o in (('pre', p), ('post', q)):
            v = o['csb']
            if v == 0:
                fail(c, 'select_exclusive', '%s.csb=0: both chip selects active' % side)
            elif v != 3:
                idx = 0 if v == 2 else 1
                if idx not in active_ids and not (side == 'post' and accept and a['csid'] == idx):
                    fail(c, 'select_target', '%s selects csb[%d] with no open accepted command targeting it' % (side, idx))

        edge = p['sck'] != q['sck']
        if edge:
            cnt['sck_edges'] += 1
        if edge and p['csb'] == 3 and q['csb'] == 3 and st['cpol'] is not None and q['sck'] != st['cpol']:
            fail(c, 'spurious_sck', 'SCK edge while all selects inactive, not toward accepted CPOL idle level')
        stalled = bool(p['tx_stall'] or p['rx_stall'])
        if stalled:
            cnt['stall_rows'] += 1
            if p['wr'] or p['rd']:
                fail(c, 'stall_safety', 'wr/rd handshake asserted during stall')
            if edge:
                fail(c, 'stall_safety', 'SCK edge during stall')
            if q['csb'] != p['csb']:
                fail(c, 'stall_safety', 'csb changed during stall')
        cs = cur()
        stl = st['stall']
        if stl is None:
            txs = bool(p['tx_stall'] and not a['tx_ready'])
            rxs = bool(p['rx_stall'] and not a['rx_ready'])
            if cs is not None and p['csb'] != 3 and (txs or rxs):
                st['stall'] = {'seg': cs, 'start': c, 'release': None, 'kind': 'tx' if txs else 'rx', 'nf': len(F), 'rows': 1}
        elif stl['release'] is None:
            if stalled:
                stl['rows'] += 1
            else:
                stl['release'] = c

        prev = segs[-1] if segs else None
        if a['valid'] and prev is not None and prev['keep_cs'] and (prev['csid'] != a['csid'] or any(prev[k] != a[k] for k in CFG)) and not any(sw['state'] == 'open' and sw['B'] is None for sw in switches):
            cnt['switches_offered'] += 1
            if prev['dummy'] or not (a['write'] or a['read']):
                un(c, 'switch_scope', 'switch involving a dummy segment; completion not externally countable; not checked')
            else:
                switches.append({'A': prev, 'B': None, 'off': dict((k, a[k]) for k in CMD), 'state': 'open', 'rise': None, 'fall': None, 'lead': None, 'trail': None, 'gap': None, 'nf': len(F), 'accept': None, 'offer': c})
        if accept:
            cnt['accepted'] += 1
            nb = a['length'] + 1
            s = {'id': st['nid'], 'cycle': c, 'dummy': not (a['write'] or a['read']), 'total': nb,
                 'wr_rem': nb if a['write'] else 0, 'rd_rem': nb if a['read'] else 0,
                 'edges': 0, 'progress': False, 'done': None, 'closed': None}
            for k in CMD:
                s[k] = a[k]
            st['nid'] += 1
            for sw in switches:
                if sw['state'] == 'open' and sw['B'] is None:
                    sw['B'] = s
                    sw['accept'] = c
            if s['dummy']:
                un(c, 'dummy_segment', 'dummy segment %d accepted; completion not tracked' % s['id'])
            segs.append(s)
            st['cpol'] = a['cpol']
            if st['window']:
                st['window'] = False
                if st['abort'] is not None and st['restart'] is None:
                    st['restart'] = s

        hs = set()
        for kind, rem, last, word in (('wr', 'wr_rem', 'last_write', 'transmit'), ('rd', 'rd_rem', 'last_read', 'receive')):
            if not p[kind]:
                continue
            cnt[kind] += 1
            if not a['tx_ready' if kind == 'wr' else 'rx_ready']:
                fail(c, 'handshake_without_ready', '%s pulse while external %s not ready' % (kind, 'source' if kind == 'wr' else 'sink'))
            s = None
            for x in segs:
                if x[rem] > 0:
                    s = x
                    break
            if s is None:
                if st['abort'] is not None:
                    st['abort']['stale'] = True
                if st['window']:
                    fail(c, 'stale_byte', '%s pulse after reset before any newly accepted command' % kind)
                else:
                    fail(c, 'byte_accounting', '%s pulse with no accepted command expecting a %s byte' % (kind, word))
                continue
            exp = 1 if s[rem] == 1 else 0
            if p[last] != exp:
                fail(c, 'last_flag', '%s=%d on %s byte %d of %d (segment %d)' % (last, p[last], kind, s['total'] - s[rem] + 1, s['total'], s['id']))
            s[rem] -= 1
            s['progress'] = True
            hs.add(s['id'])

        if edge:
            for s in segs:
                if not s['dummy'] and s['closed'] is None:
                    if _bit(p['csb'], s['csid']) == 0:
                        s['edges'] += 1
                        s['progress'] = True
                    break
            if p['csb'] != 3 or q['csb'] != 3:
                st['last_edge'] = c
            for b in (0, 1):
                if _bit(p['csb'], b) == 0 or _bit(q['csb'], b) == 0:
                    st['le'][b] = c

        for s in segs:
            if s['done'] is None and not s['dummy'] and s['wr_rem'] == 0 and s['rd_rem'] == 0:
                s['done'] = c

        if prev is not None and not a['valid']:
            h = prev
            if h['keep_cs'] and h['done'] is not None and c > h['done'] and _bit(p['csb'], h['csid']) == 0 and _bit(q['csb'], h['csid']) == 1:
                fail(c, 'csaat_hold', 'csb[%d] released after CSAAT segment %d with no later offered command (registers.md COMMAND.CSAAT 313-318)' % (h['csid'], h['id']))

        o = cur()
        if o is not None and o['progress'] and o['done'] is None and _bit(p['csb'], o['csid']) == 0 and _bit(q['csb'], o['csid']) == 1:
            fail(c, 'missing_byte_at_release', 'csb[%d] released with %d tx / %d rx bytes outstanding in segment %d (registers.md COMMAND.LEN 292-302)' % (o['csid'], o['wr_rem'], o['rd_rem'], o['id']))

        if a['valid'] and not accept and i + 1 < len(rows):
            n = rows[i + 1]['action']
            if n['rst_n'] == 1 and n['sw_reset'] == 0:
                if n['valid'] != 1 or any(n[k] != a[k] for k in CMD):
                    av(rows[i + 1].get('cycle', i + 1), 'hold', 'pending command dropped or changed before acceptance')

        for sw in switches:
            if sw['state'] != 'open':
                continue
            A = sw['A']
            B = sw['B']
            ab = A['csid']
            if sw['rise'] is None:
                if A['done'] is not None and c > A['done'] and _bit(p['csb'], ab) == 0 and _bit(q['csb'], ab) == 1:
                    sw['rise'] = c
                    sw['trail'] = None if st['le'][ab] is None else c - st['le'][ab]
            elif sw['fall'] is None:
                if p['csb'] != 3:
                    fail(c, 'switch_fresh_idle', 'a select was active after old-select release before an all-high gap (theory_of_operation 204-208)')
                    sw['state'] = 'failed'
                elif q['csb'] != 3:
                    sw['fall'] = c
                    sw['gap'] = c - sw['rise']
                    sel = 0 if q['csb'] == 2 else (1 if q['csb'] == 1 else None)
                    if sel != sw['off']['csid']:
                        fail(c, 'switch_target', 'new selection %r does not match accepted CSID %d' % (sel, B['csid']))
                        sw['state'] = 'failed'
            elif sw['lead'] is None:
                if edge and _bit(p['csb'], sw['off']['csid']) == 0:
                    sw['lead'] = c - sw['fall']

        for s in segs:
            if s['dummy'] or s['done'] is None or s['closed'] is not None:
                continue
            if _bit(p['csb'], s['csid']) == 0 and _bit(q['csb'], s['csid']) == 1:
                s['closed'] = c
            elif any(h > s['id'] for h in hs):
                s['closed'] = c

        for sw in switches:
            if sw['state'] == 'open' and sw['B'] is not None and sw['B']['closed'] is not None:
                finalize(sw, c)

        stl = st['stall']
        if stl is not None and stl['seg']['closed'] is not None:
            s = stl['seg']
            if stl['release'] is not None and s['done'] is not None and s['done'] >= stl['release'] and len(F) == stl['nf'] and wclean(stl['start'], c) and enough(s):
                E.append({'family': 'backpressure_then_recovery', 'kind': stl['kind'], 'start_cycle': stl['start'], 'end_cycle': c,
                          'evidence': {'segment': s['id'], 'stall_rows': stl['rows'], 'release_cycle': stl['release'], 'bytes': s['total'], 'edges': s['edges'], 'last_handshake_cycle': s['done']}})
            else:
                un(c, 'backpressure_not_witnessed', 'stall on segment %d did not yield a clean witnessed recovery' % s['id'])
            st['stall'] = None
        ab = st['abort']
        rs = st['restart']
        if ab is not None and rs is not None and rs['closed'] is not None:
            if ab['stale'] or len(F) > ab['nf'] or not wclean(ab['cycle'], c):
                un(c, 'restart_not_clean', 'restart after %s observed with failures; not counted' % ab['kind'])
            elif not enough(rs):
                un(c, 'insufficient_serial_evidence', 'restart segment %d closed with only %d SCK edges' % (rs['id'], rs['edges']))
            else:
                E.append({'family': 'abort_then_restart', 'kind': ab['kind'], 'start_cycle': ab['cycle'], 'end_cycle': c,
                          'evidence': {'interrupted_segment': ab['seg'], 'restart_segment': rs['id'], 'restart_accept': rs['cycle'], 'bytes': rs['total'], 'edges': rs['edges']}})
            st['abort'] = None
            st['restart'] = None

    endc = rows[-1].get('cycle', len(rows) - 1)
    for s in segs:
        if not s['dummy'] and s['closed'] is None:
            un(endc, 'pending_segment', 'segment %d accepted at cycle %d not completed by end of trace (%d tx, %d rx bytes outstanding); liveness inconclusive' % (s['id'], s['cycle'], s['wr_rem'], s['rd_rem']))
    if st['stall'] is not None:
        un(endc, 'pending_backpressure', 'stall recovery not completed by end of trace')
    if st['abort'] is not None:
        un(endc, 'pending_restart', 'restart after %s not completed by end of trace' % st['abort']['kind'])
    for sw in switches:
        if sw['state'] == 'open':
            un(endc, 'pending_switch', 'switch from segment %d not completed by end of trace' % sw['A']['id'])
    return result()

