import collections

FIELDS_SIG = ('scl', 'sda')


def _g(d, k, default=0):
    if not isinstance(d, dict):
        return default
    v = d.get(k, default)
    try:
        return int(v)
    except Exception:
        return default


def check_rows(rows):
    failures = []
    assumption_violations = []
    events = []
    unresolved = []

    def fail(c, cat, det):
        failures.append({'cycle': c, 'category': cat, 'detail': det})

    def assume(c, det):
        assumption_violations.append({'cycle': c, 'detail': det})

    # expected FIFO model of pushed commands (write mode only)
    fifo = collections.deque()
    expected = collections.deque()  # popped commands awaiting wire completion
    # wire decoder state
    prev_scl, prev_sda = 1, 1
    in_txn = False
    bits = []
    cur_bytes = []  # completed wire bytes in current window: dicts
    started_at = None
    pending_start = False  # START seen before first bit of a byte
    halted_nack = None  # cycle of unexpected NACK
    halt_info = None
    stop_after_timeout = False
    stretch_active = False
    stretch_seen_cycle = None
    stretch_pending = None
    timeout_seen = None
    cleared_after_nack = None
    restart_after_clear = None
    clean_window = True
    reset_active = True
    stretch_events_pending = []
    nak_events = []
    timeout_events = []
    last_ack_bit = None
    cur_cmd = None
    byte_start_flag = False
    ack_wire = None
    seen_low_after_stretch = False

    counts = collections.Counter()

    def on_byte_done(c, value, ackbit, startflag):
        nonlocal halted_nack, halt_info, clean_window, cur_cmd
        counts['wire_bytes'] += 1
        if not expected:
            fail(c, 'scoreboard', 'wire byte 0x%02x with no popped command' % value)
            clean_window = False
            return None
        cmd = expected.popleft()
        cur_cmd = cmd
        if cmd['byte'] != value:
            fail(c, 'scoreboard', 'wire byte 0x%02x expected 0x%02x' % (value, cmd['byte']))
            clean_window = False
        if cmd['start'] and not startflag:
            fail(c, 'scoreboard', 'byte 0x%02x missing START' % value)
            clean_window = False
        if startflag and not cmd['start']:
            fail(c, 'scoreboard', 'unexpected START before byte 0x%02x' % value)
            clean_window = False
        if ackbit == 1 and not cmd['nak_ok']:
            halted_nack = c
            halt_info = {'cycle': c, 'cmd': cmd}
            counts['unexpected_nack'] += 1
            # remaining expected commands for this transfer were not consumed
        elif ackbit == 1:
            counts['expected_nack'] += 1
            events.append({'family': 'expected_nack', 'kind': 'event', 'start_cycle': c, 'end_cycle': c,
                           'evidence': 'NAKOK byte 0x%02x NACKed' % value})
        return cmd

    for idx, row in enumerate(rows):
        c = _g(row, 'cycle', idx) if isinstance(row, dict) and 'cycle' in row else idx
        act = row.get('action', row.get('actions', {})) if isinstance(row, dict) else {}
        pre = row.get('pre', {}) if isinstance(row, dict) else {}
        post = row.get('post', {}) if isinstance(row, dict) else {}
        for k, v in list(act.items()) if isinstance(act, dict) else []:
            if not isinstance(v, int) or v < 0:
                assume(c, 'action %s not nonnegative int' % k)
        rst = _g(act, 'rst_n', 1)
        if rst == 0:
            fifo.clear(); expected.clear(); bits = []; in_txn = False
            halted_nack = None; halt_info = None; timeout_seen = None
            cleared_after_nack = None; restart_after_clear = None
            stretch_pending = None; pending_start = False
            reset_active = True
            for ph in (pre, post):
                if _g(ph, 'scl_o', 1) == 0 or _g(ph, 'sda_o', 1) == 0:
                    fail(c, 'reset', 'controller drives bus during reset')
            prev_scl = _g(post, 'scl', 1); prev_sda = _g(post, 'sda', 1)
            continue
        reset_active = False
        if _g(act, 'flush', 0):
            if halted_nack is None and not _g(pre, 'idle', 1) and expected:
                assume(c, 'flush outside halted/idle context')
            fifo.clear()
            expected.clear()
        if _g(act, 'push', 0):
            if len(fifo) >= 64:
                assume(c, 'push into full FIFO')
            else:
                fifo.append({'byte': _g(act, 'byte') & 0xff, 'start': _g(act, 'start'),
                             'stop': _g(act, 'stop'), 'nak_ok': _g(act, 'nak_ok')})
        if _g(act, 'clear_events', 0):
            if halted_nack is not None or timeout_seen is not None:
                cleared_after_nack = c
        if _g(act, 'stretch', 0) and _g(pre, 'scl', 0) == 1 and not stretch_active:
            assume(c, 'stretch asserted while SCL high')
        # FIFO head consistency
        if _g(pre, 'valid', 0):
            if not fifo:
                fail(c, 'fifo', 'valid with empty model FIFO')
            else:
                h = fifo[0]
                if _g(pre, 'fmt_byte') != h['byte'] or _g(pre, 'fmt_start') != h['start'] or \
                   _g(pre, 'fmt_stop') != h['stop'] or _g(pre, 'fmt_nak_ok') != h['nak_ok']:
                    fail(c, 'fifo', 'head mismatch')
                if _g(pre, 'depth', len(fifo)) != len(fifo):
                    fail(c, 'fifo', 'depth %d model %d' % (_g(pre, 'depth'), len(fifo)))
        if _g(pre, 'ready', 0) and _g(pre, 'valid', 0) and fifo:
            fifo.popleft()  # pop after processing; wire already carried it
        # wire-level: commands are attributed to head in chronological order
        # (we score wire bytes against the push order instead of pop timing)
        # process physical edges previous post -> pre -> post
        for ph in (pre, post):
            scl = _g(ph, 'scl', prev_scl); sda = _g(ph, 'sda', prev_sda)
            if _g(ph, 'scl_o', 1) == 0 and scl != 0 or _g(ph, 'sda_o', 1) == 0 and sda != 0:
                fail(c, 'bus', 'wired-AND violated')
            if prev_scl == 1 and scl == 1 and prev_sda != sda:
                if sda == 0:
                    if in_txn and bits:
                        fail(c, 'protocol', 'START mid-byte')
                    in_txn = True; bits = []; pending_start = True
                    counts['start'] += 1
                    if cleared_after_nack is not None and halt_info is not None:
                        restart_after_clear = c
                else:
                    if bits and len(bits) % 9 != 0:
                        fail(c, 'protocol', 'STOP mid-byte')
                    counts['stop'] += 1
                    in_txn = False; bits = []
                    if timeout_seen is not None and halt_info is not None and not halt_info.get('stopped'):
                        halt_info['stopped'] = c
                    if cur_cmd is not None and not cur_cmd['stop'] and halt_info is None:
                        fail(c, 'scoreboard', 'STOP without STOP flag')
                    if stretch_pending is not None and stretch_pending.get('byte_done'):
                        events.append({'family': 'stretch_recovery', 'kind': 'success', 'start_cycle': stretch_pending['c'],
                                       'end_cycle': c, 'evidence': 'clock extended then byte+STOP'})
                        stretch_pending = None
                    if halt_info is not None and halt_info.get('new_ok'):
                        fam = 'nak_timeout_recovery' if halt_info.get('stopped') else 'nak_restart'
                        events.append({'family': fam, 'kind': 'success', 'start_cycle': halt_info['cycle'],
                                       'end_cycle': c, 'evidence': 'NACK, halt, clear, START, clean byte, STOP'})
                        halt_info = None; halted_nack = None; timeout_seen = None; cleared_after_nack = None
                    cur_cmd = None
            elif prev_scl == 0 and scl == 1 and in_txn:
                bits.append(sda)
                if len(bits) == 9:
                    val = 0
                    for b in bits[:8]:
                        val = (val << 1) | b
                    hb = halt_info
                    cmd = on_byte_done(c, val, bits[8], pending_start)
                    if hb is not None and halt_info is hb and cleared_after_nack is not None and restart_after_clear is not None and bits[8] == 0:
                        hb['new_ok'] = True
                    if stretch_pending is not None:
                        stretch_pending['byte_done'] = True
                    pending_start = False
                    bits = []
            elif prev_scl == 1 and scl == 1 and halted_nack is not None and cleared_after_nack is None and timeout_seen is None and in_txn:
                fail(c, 'halt', 'SCL released during NACK halt')
            prev_scl, prev_sda = scl, sda
        if _g(pre, 'stretch', 0) or _g(act, 'stretch', 0):
            if in_txn and stretch_pending is None:
                stretch_pending = {'c': c}
        if _g(pre, 'nak_timeout', 0) and halt_info is not None:
            timeout_seen = c
        if halt_info is not None and timeout_seen is not None and halt_info.get('stopped') and halt_info.get('stopped') != True:
            if (_g(post, 'scl_o', 1) == 0 or _g(post, 'sda_o', 1) == 0) and cleared_after_nack is None:
                fail(c, 'timeout', 'bus not released after timeout STOP')
    # pending
    if expected:
        unresolved.append('%d popped commands without wire completion' % len(expected))
    if halt_info is not None:
        unresolved.append('NACK recovery incomplete from cycle %d' % halt_info['cycle'])
    if stretch_pending is not None:
        unresolved.append('stretch recovery incomplete')
    if fifo:
        unresolved.append('%d FIFO entries pending' % len(fifo))
    for e in events:
        counts['event_' + e['family']] += 1
    verdict = 'fail' if failures else ('invalid' if assumption_violations else ('pass' if not unresolved else 'pending'))
    return {'failures': failures, 'assumption_violations': assumption_violations, 'events': events,
            'unresolved': unresolved, 'verdict': verdict, 'counts': dict(counts)}

