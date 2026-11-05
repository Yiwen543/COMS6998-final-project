KEYS = ('rst_n', 'enable', 'sw_reset', 'valid', 'csid', 'speed', 'write', 'read', 'length', 'keep_cs', 'clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol', 'tx_data', 'tx_be', 'tx_valid', 'rx_ready', 'sd')
BASE = {'ready': 0, 'tx_ready': 0, 'tx_full': 0, 'rx_data': 0, 'rx_valid': 0, 'sck': 0, 'csb': 3, 'sd': 0, 'sd_en': 0, 'rx_stall': 0, 'tx_stall': 0, 'active': 0}


def _gen(wr=1, rd=0, txb=0xA5, rxb=0x3C, flip=False, early=False, short=False, drop=False, dummy=False, spur=False, rxpad=0, keep=0, pend=None):
    fall = 4 if short else 3
    posts = []
    acts = []
    for c in range(26):
        a = dict((k, 0) for k in KEYS)
        a['rst_n'] = 0 if c < 2 else 1
        a['enable'] = 1
        a['rx_ready'] = 1
        if c == 2:
            a['valid'] = 1
            a['write'] = 0 if dummy else wr
            a['read'] = 0 if dummy else rd
            a['keep_cs'] = keep
            if wr:
                a['tx_valid'] = 1
                a['tx_data'] = 0xC3B2E100 | txb
                a['tx_be'] = 1
        if pend and c >= 20:
            a['csid'] = 1
            a['write'] = 1
            a['valid'] = 1 if pend == 'valid' else 0
        if rd and 4 <= c <= 19:
            j = (c - 4) // 2
            a['sd'] = ((rxb >> (7 - j)) & 1) << 1
        o = dict(BASE)
        o['ready'] = 0 if (c < 1 or (drop and c == 1) or (pend and c >= 19)) else 1
        o['tx_ready'] = 1 if c >= 1 else 0
        lowcs = fall <= c <= 20 and not (early and c >= 12)
        o['csb'] = 2 if lowcs else 3
        if 4 <= c <= 19:
            o['sck'] = 1 if (c - 4) % 2 == 0 else 0
        if spur and c == 23:
            o['sck'] = 1
        if wr and 3 <= c <= 18:
            j = (c - 3) // 2
            b = (txb >> (7 - j)) & 1
            if flip and j == 3:
                b ^= 1
            o['sd'] = b
        if wr and lowcs:
            o['sd_en'] = 1
        o['active'] = 1 if 2 <= c <= 20 else 0
        if rd and c == 21:
            o['rx_valid'] = 1
            o['rx_data'] = rxb | (rxpad << 8)
        posts.append(o)
        acts.append(a)
    rows = []
    for c in range(26):
        rows.append({'cycle': c, 'action': acts[c], 'pre': dict(posts[c - 1]) if c else dict(BASE), 'post': posts[c]})
    return rows


def run(check_rows):
    out = []

    def cats(r):
        return set(f['category'] for f in r['failures'])

    def acats(r):
        return set(x['category'] for x in r['assumption_violations'])

    cases = [
        ('std_tx_good_passes', lambda: _gen(), lambda r: r['verdict'] == 'pass' and not r['failures']),
        ('std_tx_bitflip_fails', lambda: _gen(flip=True), lambda r: 'tx_payload' in cats(r)),
        ('cs_rise_midsegment_fails', lambda: _gen(early=True), lambda r: 'cs_rise_midsegment' in cats(r)),
        ('csnlead_violation_fails', lambda: _gen(short=True), lambda r: 'csnlead' in cats(r)),
        ('withdrawn_command_is_assumption_violation', lambda: _gen(drop=True), lambda r: 'cmd_transport' in acats(r)),
        ('std_rx_partial_word_passes', lambda: _gen(wr=0, rd=1), lambda r: r['verdict'] == 'pass' and not r['failures']),
        ('rx_nonzero_padding_fails', lambda: _gen(wr=0, rd=1, rxpad=0x11), lambda r: 'rx_padding' in cats(r)),
        ('rx_wrong_byte_fails', lambda: _gen(wr=0, rd=1, rxb=0x3C, rxpad=0) and [dict(x, pre=dict(x['pre'], rx_data=0x3D) if x['cycle'] == 22 else x['pre']) for x in _gen(wr=0, rd=1)], lambda r: 'rx_payload' in cats(r)),
        ('dummy_segment_scope_unresolved', lambda: _gen(dummy=True), lambda r: r['verdict'] == 'inconclusive' and not r['assumption_violations']),
        ('csaat_rise_without_change_fails', lambda: _gen(keep=1), lambda r: 'csaat' in cats(r)),
        ('csaat_rise_pending_csid_change_ok', lambda: _gen(keep=1, pend='valid'), lambda r: 'csaat' not in cats(r)),
        ('csaat_rise_invalid_offer_fails', lambda: _gen(keep=1, pend='invalid'), lambda r: 'csaat' in cats(r)),
        ('truncated_trace_inconclusive', lambda: _gen()[:12], lambda r: r['verdict'] == 'inconclusive' and not r['failures']),
        ('spurious_sck_fails', lambda: _gen(spur=True), lambda r: 'spurious_sck' in cats(r)),
    ]
    for name, mk, pred in cases:
        try:
            out.append({'name': name, 'pass': bool(pred(check_rows(mk())))})
        except Exception:
            out.append({'name': name, 'pass': False})
    return out


