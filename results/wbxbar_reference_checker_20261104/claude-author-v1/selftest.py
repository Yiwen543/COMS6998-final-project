KI = ['i_reset', 'i_mcyc', 'i_mstb', 'i_mwe', 'i_maddr', 'i_mdata', 'i_msel', 'i_sstall', 'i_sack', 'i_sdata', 'i_serr']
KO = ['o_mstall', 'o_mack', 'o_mdata', 'o_merr', 'o_scyc', 'o_sstb', 'o_swe', 'o_saddr', 'o_sdata', 'o_ssel']


def _row(c, **kw):
    pre = {}
    for k in KI + KO:
        pre[k] = 0
    post = {}
    for k in KO:
        post[k] = 0
    for k in kw:
        if k.startswith('post_'):
            post[k[5:]] = kw[k]
        else:
            pre[k] = kw[k]
    return {'cycle': c, 'pre': pre, 'post': post}


def _rst():
    return [_row(0, i_reset=1), _row(1, i_reset=1)]


def _shift(rows, off):
    return [{'cycle': r['cycle'] + off, 'pre': r['pre'], 'post': r['post']} for r in rows]


def _write(sd=0xAB, ss=0, sel=0xF):
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=0x05, i_mdata=0xAB, i_msel=sel))
    r.append(_row(3, i_mcyc=1, o_scyc=1 << ss, o_sstb=1 << ss, o_swe=1 << ss, o_saddr=0x05 << (8 * ss), o_sdata=sd << (32 * ss), o_ssel=sel << (4 * ss)))
    r.append(_row(4, i_mcyc=1, o_scyc=1 << ss, i_sack=1 << ss))
    r.append(_row(5, i_mcyc=1, o_mack=1))
    r.append(_row(6))
    return r


def _cross(swap=False):
    r = _rst()
    r.append(_row(2, i_mcyc=3, i_mstb=3, i_maddr=0x12 | (0x03 << 8), i_msel=0xFF))
    r.append(_row(3, i_mcyc=3, o_scyc=3, o_sstb=3, o_saddr=0x03 | (0x12 << 8), o_ssel=0xFF))
    r.append(_row(4, i_mcyc=3, o_scyc=3, i_sack=3, i_sdata=0x1111 | (0x2222 << 32)))
    md = (0x1111 | (0x2222 << 32)) if swap else (0x2222 | (0x1111 << 32))
    r.append(_row(5, i_mcyc=3, o_mack=3, o_mdata=md))
    r.append(_row(6))
    return r


def _heads(bad=False):
    r = _rst()
    r.append(_row(2, i_mcyc=3, i_mstb=3, i_maddr=5 | (5 << 8), i_msel=0xFF))
    r.append(_row(3, i_mcyc=3, o_scyc=1, o_sstb=1, o_saddr=5, o_ssel=0xF))
    r.append(_row(4, i_mcyc=3, o_scyc=1, i_sack=1, i_sdata=0x11, o_sstb=1, o_saddr=5, o_ssel=0xF))
    r.append(_row(5, i_mcyc=3, o_scyc=1, i_sack=1, i_sdata=0x22, o_mack=1, o_mdata=0x22 if bad else 0x11))
    r.append(_row(6, i_mcyc=3, o_mack=2, o_mdata=0x22 << 32))
    r.append(_row(7))
    return r


def _unmapped(ack=False):
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_maddr=0x40, i_msel=0xF))
    r.append(_row(3, i_mcyc=1))
    if ack:
        r.append(_row(4, i_mcyc=1, o_mack=1))
    else:
        r.append(_row(4, i_mcyc=1, o_merr=1))
    r.append(_row(5))
    return r


def _early_err():
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_maddr=0x05, i_msel=0xF))
    r.append(_row(3, i_mcyc=1, o_merr=1))
    r.append(_row(4))
    return r


def _held(ack=False, edge=False):
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=1, i_msel=0xF, o_mstall=1))
    if ack:
        r.append(_row(3, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=1, i_msel=0xF, o_mstall=1, o_mack=1))
    else:
        r.append(_row(3, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=1, i_msel=0xF, o_mstall=0 if edge else 1, o_merr=1))
    r.append(_row(4))
    return r


def _abort(n):
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=0x10, i_msel=0xF))
    r.append(_row(3))
    c = 4
    for _ in range(n):
        r.append(_row(c, o_scyc=1, o_sstb=1, o_swe=1, o_saddr=5, o_sdata=0x10, o_ssel=0xF))
        r.append(_row(c + 1, o_scyc=1, i_sack=1))
        c += 2
    r.append(_row(c))
    return r


def _abort_reset():
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=0x10, i_msel=0xF))
    r.append(_row(3))
    r.append(_row(4, i_reset=1))
    r.append(_row(5, o_scyc=1, o_sstb=1, o_swe=1, o_saddr=5, o_sdata=0x10, o_ssel=0xF))
    r.append(_row(6, o_scyc=1, i_sack=1))
    r.append(_row(7))
    return r


def _prefix(bad=False):
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_maddr=5, i_msel=0xF))
    r.append(_row(3, i_mcyc=1, o_scyc=1, o_sstb=1, o_saddr=5, o_ssel=0xF))
    r.append(_row(4, i_mcyc=1, o_scyc=1, i_sack=1, i_sdata=0x77))
    r.append(_row(5, i_mcyc=1, o_mack=1, o_mdata=0x78 if bad else 0x77))
    r.append(_row(6, i_mcyc=1, i_mstb=1, i_maddr=7, i_msel=0xF, o_mstall=1))
    r.append(_row(7, i_mcyc=1, i_mstb=1, i_maddr=8, i_msel=0xF, o_mstall=1))
    return r


def _mixed():
    r = _rst()
    r.append(_row(2, i_mcyc=3, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=1, i_msel=0xF, o_mstall=1))
    r.append(_row(3, i_mcyc=3, i_mstb=1, i_mwe=1, i_maddr=6, i_mdata=1, i_msel=0xF, o_mstall=1, o_mack=2))
    return r


def _two():
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_maddr=5, i_msel=0xF))
    r.append(_row(3, i_mcyc=1, i_mstb=1, i_maddr=6, i_msel=0xF))
    r.append(_row(4, i_mcyc=1, o_scyc=1, o_sstb=1, o_saddr=5, o_ssel=0xF))
    r.append(_row(5, i_mcyc=1, o_scyc=1, o_sstb=1, o_saddr=6, o_ssel=0xF, i_sack=1, i_sdata=1))
    r.append(_row(6, i_mcyc=1, o_scyc=1, i_sack=1, i_sdata=2, o_mack=1, o_mdata=1))
    r.append(_row(7, i_mcyc=1, o_mack=1, o_mdata=2))
    r.append(_row(8))
    return r


def _pool2():
    r = _rst()
    r.append(_row(2, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=5, i_mdata=1, i_msel=0xF))
    r.append(_row(3, i_mcyc=1, i_mstb=1, i_mwe=1, i_maddr=6, i_mdata=2, i_msel=0xF))
    r.append(_row(4))
    r.append(_row(5))
    return r


def _has(res, item):
    for u in res['unresolved']:
        if u['item'] == item:
            return True
    return False


def run(check_rows):
    rs_bad = _write()
    rs_bad[1] = _row(1, i_reset=1, post_o_scyc=1)
    tests = [
        ('write_positive', lambda: check_rows(_write())['verdict'] == 'scoped_pass'),
        ('write_payload_corruption', lambda: check_rows(_write(sd=0xAC))['verdict'] == 'dut_violation'),
        ('write_misroute', lambda: check_rows(_write(ss=1))['verdict'] == 'dut_violation'),
        ('masked_lane_write_positive', lambda: check_rows(_write(sd=0x5500AB, sel=0x1))['verdict'] == 'scoped_pass'),
        ('enabled_lane_corruption', lambda: check_rows(_write(sd=0xAC, sel=0x1))['verdict'] == 'dut_violation'),
        ('cross_slave_reads_positive', lambda: check_rows(_cross())['verdict'] == 'scoped_pass'),
        ('cross_slave_wrong_retirement_data', lambda: check_rows(_cross(swap=True))['verdict'] == 'dut_violation'),
        ('identical_heads_ambiguity_resolved', lambda: check_rows(_heads())['verdict'] == 'scoped_pass'),
        ('identical_heads_corruption', lambda: check_rows(_heads(bad=True))['verdict'] == 'dut_violation'),
        ('unmapped_err_positive', lambda: check_rows(_unmapped())['verdict'] == 'scoped_pass'),
        ('unmapped_ack_fault', lambda: check_rows(_unmapped(ack=True))['verdict'] == 'dut_violation'),
        ('invented_ack', lambda: check_rows(_rst() + [_row(2, i_mcyc=1), _row(3, i_mcyc=1, o_mack=1), _row(4)])['verdict'] == 'dut_violation'),
        ('pending_unresolved', lambda: _has(check_rows(_write()[:4]), 'pending_at_batch_end') and check_rows(_write()[:4])['verdict'] == 'unresolved'),
        ('early_mapped_err_unresolved', lambda: _has(check_rows(_early_err()), 'unexplained_mapped_err')),
        ('uncertainty_survives_reset', lambda: check_rows(_early_err() + [_row(5, i_reset=1)] + _shift(_write()[2:], 4))['verdict'] == 'unresolved'),
        ('held_err_unresolved', lambda: _has(check_rows(_held()), 'possible_starvation_err') and check_rows(_held())['verdict'] == 'unresolved'),
        ('held_ack_invented', lambda: check_rows(_held(ack=True))['verdict'] == 'dut_violation'),
        ('acceptance_edge_err_unresolved', lambda: check_rows(_held(edge=True))['verdict'] == 'unresolved'),
        ('abort_none_forwarded_pass', lambda: check_rows(_abort(0))['verdict'] == 'scoped_pass'),
        ('post_abort_forward_unresolved', lambda: _has(check_rows(_abort(1)), 'post_abort_forward')),
        ('abort_double_consumption', lambda: check_rows(_abort(2))['verdict'] == 'dut_violation'),
        ('abort_reset_forward', lambda: check_rows(_abort_reset())['verdict'] == 'dut_violation'),
        ('reset_output_fault', lambda: check_rows(rs_bad)['verdict'] == 'dut_violation'),
        ('k13_cyc_low_response', lambda: check_rows(_rst() + [_row(2), _row(3, o_mack=1), _row(4)])['verdict'] == 'dut_violation'),
        ('k13_same_edge_unresolved', lambda: _has(check_rows(_rst() + [_row(2, i_mcyc=1), _row(3, o_merr=1), _row(4)]), 'same_edge_response_after_abort')),
        ('unsolicited_slave_ack_env', lambda: check_rows(_rst() + [_row(2, o_scyc=1, i_sack=1), _row(3)])['verdict'] == 'input_or_scope_invalid'),
        ('no_initial_reset_env', lambda: check_rows([_row(0), _row(1)])['verdict'] == 'input_or_scope_invalid'),
        ('clean_prefix_before_invalid', lambda: check_rows(_prefix())['verdict'] == 'input_or_scope_invalid' and check_rows(_prefix())['counts']['prefix_status'] == 'prefix_scoped_pass'),
        ('violation_before_invalid_kept', lambda: check_rows(_prefix(bad=True))['verdict'] == 'dut_violation'),
        ('mixed_same_edge_explicit', lambda: check_rows(_mixed())['verdict'] == 'input_or_scope_invalid' and _has(check_rows(_mixed()), 'mixed_same_edge')),
        ('two_live_default_pass', lambda: check_rows(_two())['verdict'] == 'scoped_pass'),
        ('live_limit_exhaustion', lambda: _has(check_rows(_two(), {'MAX_LIVE_PER_MASTER': 1}), 'unresolved_on_limit') and check_rows(_two(), {'MAX_LIVE_PER_MASTER': 1})['verdict'] == 'unresolved'),
        ('hyp_limit_exhaustion', lambda: check_rows(_heads(), {'MAX_HYP': 1})['verdict'] == 'unresolved' and check_rows(_heads(), {'MAX_HYP': 1})['counts']['checked_scope']['suspended_rows'] > 0),
        ('pool_default_pass', lambda: check_rows(_pool2())['verdict'] == 'scoped_pass'),
        ('pool_limit_exhaustion', lambda: check_rows(_pool2(), {'MAX_CANCELED_POOL': 1})['verdict'] == 'unresolved'),
        ('invalid_limit_zero', lambda: check_rows(_write(), {'MAX_HYP': 0})['verdict'] == 'input_or_scope_invalid'),
        ('invalid_limit_bool', lambda: check_rows(_write(), {'MAX_HYP': True})['verdict'] == 'input_or_scope_invalid'),
        ('defaults_unchanged', lambda: check_rows(_heads())['counts']['limits'] == {'MAX_HYP': 4096, 'MAX_LIVE_PER_MASTER': 64, 'MAX_CANCELED_POOL': 256}),
        ('k5_excluded_reported', lambda: check_rows(_write())['counts']['property_status']['K5_forward_order'] == 'excluded_not_judged'),
    ]
    out = []
    for name, fn in tests:
        try:
            ok = bool(fn())
        except Exception:
            ok = False
        out.append({'name': name, 'pass': ok})
    return out

