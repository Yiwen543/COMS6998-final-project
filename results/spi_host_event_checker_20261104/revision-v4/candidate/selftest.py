IN = ['rst_n', 'enable', 'sw_reset', 'valid', 'csid', 'speed', 'write', 'read', 'length', 'keep_cs', 'clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol', 'tx_ready', 'rx_ready']
OUT = ['ready', 'sck', 'csb', 'sd_en', 'last_read', 'last_write', 'wr', 'rd', 'sample', 'shift', 'speed', 'full_cycle', 'rx_stall', 'tx_stall', 'active']


def _new():
    return {'sck': 0, 'csb': 3, 'rows': []}


def _step(t, act=None, pre=None, csb=None, tog=False, pcsb=None):
    a = dict((k, 0) for k in IN)
    a['rst_n'] = 1
    a['enable'] = 1
    a['tx_ready'] = 1
    a['rx_ready'] = 1
    a.update(act or {})
    if pcsb is not None:
        t['csb'] = pcsb
    p = dict((k, 0) for k in OUT)
    p['sck'] = t['sck']
    p['csb'] = t['csb']
    p.update(pre or {})
    ns = t['sck'] ^ 1 if tog else t['sck']
    nc = t['csb'] if csb is None else csb
    q = dict((k, 0) for k in OUT)
    q['sck'] = ns
    q['csb'] = nc
    t['rows'].append({'cycle': len(t['rows']), 'action': a, 'pre': p, 'post': q})
    t['sck'] = ns
    t['csb'] = nc


def _reset(t, n=2):
    for _ in range(n):
        _step(t, {'rst_n': 0}, pcsb=3, csb=3)


def _toggle(t, n):
    for _ in range(2 * n):
        _step(t, tog=True)


def _single(fault=None, pending=False):
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1, 'keep_cs': 1 if fault == 'csaat' else 0}, {'ready': 1})
    _step(t, csb=0 if fault == 'both' else 2)
    pre = {'wr': 1, 'last_write': 0 if fault == 'last' else 1}
    if fault == 'stallwr':
        pre['tx_stall'] = 1
    _step(t, pre=pre)
    if pending:
        _toggle(t, 3)
        return t['rows']
    _toggle(t, 8)
    if fault == 'extra':
        _step(t, pre={'wr': 1, 'last_write': 1})
    _step(t, csb=3)
    if fault == 'idlesck':
        _step(t, tog=True)
    _step(t)
    return t['rows']


def _hold():
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1}, {'ready': 0})
    _step(t)
    _step(t)
    return t['rows']


def _bp(fault=None):
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1, 'length': 1}, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 0})
    _toggle(t, 8)
    for k in range(3):
        _step(t, {'tx_ready': 0}, {'tx_stall': 1}, tog=(fault == 'sck' and k == 1), csb=(3 if fault == 'csb' and k == 1 else None))
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 4 if fault == 'short' else 8)
    _step(t, csb=3)
    _step(t)
    return t['rows']


def _same_edge(fault=None):
    t = _new()
    _reset(t)
    act = {'valid': 1, 'write': 1}
    pre = {'ready': 1, 'wr': 1, 'last_write': 1}
    if fault == 'notready':
        act['tx_ready'] = 0
    if fault in ('read', 'rdnotready'):
        act = {'valid': 1, 'read': 1, 'rx_ready': 0 if fault == 'rdnotready' else 1}
        pre = {'ready': 1, 'rd': 1, 'last_read': 1}
    _step(t, act, pre, csb=2)
    if fault == 'extra':
        _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    _step(t, csb=3)
    _step(t)
    return t['rows']


def _early_switch(fault=None):
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1, 'keep_cs': 1, 'idle': 3}, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    off = {'valid': 1, 'write': 1, 'csid': 1, 'idle': 3}
    _step(t, off, csb=3)
    if fault != 'short':
        _step(t, off)
        _step(t, off)
    _step(t, off, {'ready': 1})
    _step(t, csb=2 if fault == 'wrong' else 1)
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    _step(t, csb=3)
    _step(t)
    return t['rows']


def _missing(pending=False):
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1, 'length': 1}, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 0})
    _toggle(t, 8)
    if pending:
        return t['rows']
    _step(t, csb=3)
    _step(t)
    return t['rows']


def _abort(kind, stale=False, mut=False):
    t = _new()
    _reset(t)
    _step(t, {'valid': 1, 'write': 1, 'length': 1}, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 0})
    _toggle(t, 4)
    if kind == 'sw':
        _step(t, {'sw_reset': 1}, csb=3)
        _step(t, {'sw_reset': 1}, pcsb=(2 if mut else None), csb=3)
    else:
        _step(t, {'rst_n': 0}, pcsb=(2 if mut else 3), csb=3)
        _step(t, {'rst_n': 0}, pcsb=3, csb=3)
    if stale:
        _step(t, pre={'wr': 1, 'last_write': 1})
    _step(t, {'valid': 1, 'write': 1}, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    _step(t, csb=3)
    _step(t)
    return t['rows']


def _switch(fault=None):
    t = _new()
    _reset(t)
    o1 = {'valid': 1, 'write': 1, 'keep_cs': 1, 'idle': 3, 'trail': 3 if fault == 'trail' else 0}
    o2 = {'valid': 1, 'write': 1, 'csid': 1, 'idle': 2 if fault == 'additive' else 3, 'lead': 3 if fault == 'lead' else 0}
    _step(t, o1, {'ready': 1})
    _step(t, csb=2)
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    _step(t, o2, {'ready': 1})
    if fault == 'noidle':
        _step(t, csb=1)
    else:
        _step(t, csb=3)
        for _ in range(1 if fault == 'short' else 3):
            _step(t)
        _step(t, csb=1)
    _step(t, pre={'wr': 1, 'last_write': 1})
    _toggle(t, 8)
    _step(t, csb=3)
    _step(t)
    return t['rows']


def run(check_rows):
    res = []

    def cats(r):
        return set(f['category'] for f in r.get('failures', []))

    def fams(r):
        return [(e['family'], e['kind']) for e in r.get('events', [])]

    def famset(r):
        return set(e['family'] for e in r.get('events', []))

    def t(name, build, pred):
        try:
            r = check_rows(build())
            ok = bool(pred(r))
            res.append({'name': name, 'pass': ok, 'verdict': r.get('verdict'), 'failure_categories': sorted(cats(r))})
        except Exception as ex:
            res.append({'name': name, 'pass': False, 'error': repr(ex)})

    clean = lambda r: not r['failures'] and not r['assumption_violations']
    t('single_write_positive', lambda: _single(), lambda r: r['verdict'] == 'scoped_pass' and clean(r))
    t('fault_last_flag', lambda: _single('last'), lambda r: 'last_flag' in cats(r) and r['verdict'] == 'dut_violation')
    t('fault_extra_wr', lambda: _single('extra'), lambda r: 'byte_accounting' in cats(r))
    t('fault_both_selects', lambda: _single('both'), lambda r: 'select_exclusive' in cats(r))
    t('fault_wr_during_stall', lambda: _single('stallwr'), lambda r: 'stall_safety' in cats(r))
    t('fault_csaat_released', lambda: _single('csaat'), lambda r: 'csaat_hold' in cats(r))
    t('assumption_hold_violation', _hold, lambda r: r['verdict'] == 'input_or_scope_invalid' and any(a['category'] == 'hold' for a in r['assumption_violations']))
    t('missing_initial_reset', lambda: _single()[2:], lambda r: r['verdict'] == 'input_or_scope_invalid')
    t('empty_trace_unresolved', lambda: [], lambda r: r['verdict'] == 'unresolved')
    t('pending_not_failed', lambda: _single(pending=True), lambda r: clean(r) and any(u['category'] == 'pending_segment' for u in r['unresolved']) and not r['events'])
    t('backpressure_positive', lambda: _bp(), lambda r: clean(r) and ('backpressure_then_recovery', 'tx') in fams(r))
    t('fault_sck_during_stall', lambda: _bp('sck'), lambda r: 'stall_safety' in cats(r) and 'backpressure_then_recovery' not in famset(r))
    t('abort_sw_positive', lambda: _abort('sw'), lambda r: clean(r) and ('abort_then_restart', 'sw_reset') in fams(r))
    t('abort_async_positive', lambda: _abort('async'), lambda r: clean(r) and ('abort_then_restart', 'async_reset') in fams(r))
    t('fault_stale_byte', lambda: _abort('async', True), lambda r: 'stale_byte' in cats(r) and 'abort_then_restart' not in famset(r))
    t('switch_positive', lambda: _switch(), lambda r: clean(r) and ('constrained_transaction_switch', 'csid_change') in fams(r))
    t('fault_switch_short_gap', lambda: _switch('short'), lambda r: 'switch_timing' in cats(r) and 'constrained_transaction_switch' not in famset(r))
    t('fault_switch_no_idle', lambda: _switch('noidle'), lambda r: 'switch_fresh_idle' in cats(r) and 'constrained_transaction_switch' not in famset(r))
    t('same_edge_accept_wr_positive', lambda: _same_edge(), lambda r: r['verdict'] == 'scoped_pass' and clean(r))
    t('fault_same_edge_extra_wr', lambda: _same_edge('extra'), lambda r: 'byte_accounting' in cats(r))
    t('fault_wr_without_tx_ready', lambda: _same_edge('notready'), lambda r: 'handshake_without_ready' in cats(r))
    t('early_release_switch_positive', lambda: _early_switch(), lambda r: clean(r) and ('constrained_transaction_switch', 'csid_change') in fams(r))
    t('fault_early_release_short_gap', lambda: _early_switch('short'), lambda r: 'switch_timing' in cats(r) and 'constrained_transaction_switch' not in famset(r))
    t('fault_missing_byte_at_release', _missing, lambda r: 'missing_byte_at_release' in cats(r))
    t('short_burst_no_recovery_event', lambda: _bp('short'), lambda r: 'backpressure_then_recovery' not in famset(r) and any(u['category'] == 'backpressure_not_witnessed' for u in r['unresolved']))
    nsw = lambda r: 'constrained_transaction_switch' not in famset(r)
    t('fault_idle_sck_against_cpol', lambda: _single('idlesck'), lambda r: 'spurious_sck' in cats(r))
    t('fault_csb_change_during_stall_window', lambda: _bp('csb'), lambda r: 'stall_safety' in cats(r) and 'backpressure_then_recovery' not in famset(r))
    t('same_edge_accept_rd_positive', lambda: _same_edge('read'), lambda r: r['verdict'] == 'scoped_pass' and clean(r))
    t('fault_rd_without_rx_ready', lambda: _same_edge('rdnotready'), lambda r: 'handshake_without_ready' in cats(r))
    t('fault_early_release_wrong_target', lambda: _early_switch('wrong'), lambda r: ('switch_target' in cats(r) or 'select_target' in cats(r)) and nsw(r))
    t('incomplete_pending_not_failed', lambda: _missing(True), lambda r: clean(r) and any(u['category'] == 'pending_segment' for u in r['unresolved']) and not r['events'])
    t('fault_sw_reset_second_cycle_select_window', lambda: _abort('sw', mut=True), lambda r: 'reset_separation' in cats(r) and 'abort_then_restart' not in famset(r))
    t('fault_async_reset_select_window', lambda: _abort('async', mut=True), lambda r: 'reset_separation' in cats(r) and 'abort_then_restart' not in famset(r))
    t('fault_sw_stale_byte', lambda: _abort('sw', True), lambda r: 'stale_byte' in cats(r) and 'abort_then_restart' not in famset(r))
    t('fault_switch_short_trail', lambda: _switch('trail'), lambda r: 'switch_timing' in cats(r) and nsw(r))
    t('fault_switch_short_lead', lambda: _switch('lead'), lambda r: 'switch_timing' in cats(r) and nsw(r))
    t('switch_additive_idle_unresolved', lambda: _switch('additive'), lambda r: clean(r) and r['verdict'] == 'unresolved' and nsw(r))
    t('scope_last_read_without_transfer', lambda: (lambda rows: [rows[k]['pre'].update({'last_read': 1}) if k == 6 else None for k in range(len(rows))] and rows)(_single()), lambda r: r['verdict'] == 'scoped_pass')
    return res

