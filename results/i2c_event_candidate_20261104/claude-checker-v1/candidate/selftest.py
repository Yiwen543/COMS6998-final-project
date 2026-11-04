def _bus(rows, cyc, scl, sda):
    rows.append({'cycle': cyc, 'action': {'rst_n': 1}, 'pre': {'scl': scl, 'sda': sda}, 'post': {'scl': scl, 'sda': sda}})


def _trace(byte, ack, flip=None):
    rows = []
    rows.append({'cycle': 0, 'action': {'rst_n': 0}, 'pre': {'scl': 1, 'sda': 1}, 'post': {'scl': 1, 'sda': 1}})
    rows.append({'cycle': 1, 'action': {'rst_n': 1, 'push': 1, 'byte': byte, 'start': 1, 'stop': 1}, 'pre': {'scl': 1, 'sda': 1}, 'post': {'scl': 1, 'sda': 1}})
    c = 2
    _bus(rows, c, 1, 0); c += 1
    bitsl = [(byte >> (7 - i)) & 1 for i in range(8)]
    if flip is not None:
        bitsl[flip] ^= 1
    for b in bitsl + [0 if ack else 1]:
        _bus(rows, c, 0, b); c += 1
        _bus(rows, c, 1, b); c += 1
    _bus(rows, c, 0, 0); c += 1
    _bus(rows, c, 1, 0); c += 1
    _bus(rows, c, 1, 1); c += 1
    return rows


def run(check_rows):
    out = []
    r = check_rows(_trace(0xA5, True))
    out.append({'name': 'clean_byte_no_failures', 'pass': not r['failures']})
    r = check_rows(_trace(0xA5, True, flip=3))
    out.append({'name': 'bit_flip_detected', 'pass': any(f['category'] == 'scoreboard' for f in r['failures'])})
    r = check_rows(_trace(0x3C, False))
    out.append({'name': 'unexpected_nack_unresolved_not_success', 'pass': not any(e['kind'] == 'success' for e in r['events']) and r['verdict'] != 'pass'})
    rows = _trace(0xA5, True)
    rows[0]['pre']['scl_o'] = 0
    r = check_rows(rows)
    out.append({'name': 'reset_drive_detected', 'pass': any(f['category'] == 'reset' for f in r['failures'])})
    return out

