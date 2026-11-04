"""Fixed cycle interface and independent public-pin SPI controller properties.

The checker uses accepted command lengths and SPI edge counts, never DUT state,
counter values, or the extracted predicates. It is a scoped protocol scoreboard,
not a bit-accurate serial data checker (the selected FSM has no data pins).
"""
from __future__ import annotations
from collections import deque

FIELDS = {'rst_n': 1, 'enable': 1, 'sw_reset': 1, 'valid': 1, 'csid': 1,
          'speed': 2, 'write': 1, 'read': 1, 'length': 20, 'keep_cs': 1,
          'clkdiv': 16, 'idle': 4, 'lead': 4, 'trail': 4, 'full_cycle': 1,
          'cpha': 1, 'cpol': 1, 'tx_ready': 1, 'rx_ready': 1}
COMMAND = tuple(k for k in FIELDS if k not in ('rst_n', 'enable', 'sw_reset', 'valid', 'tx_ready', 'rx_ready'))
OUTPUTS = ('ready', 'sck', 'csb', 'sd_en', 'last_read', 'last_write', 'wr', 'rd',
           'sample', 'shift', 'speed', 'full_cycle', 'rx_stall', 'tx_stall', 'active')


def action(**changes):
    base = {k: 0 for k in FIELDS}
    base.update(rst_n=1, enable=1, tx_ready=1, rx_ready=1)
    if set(changes)-set(base):
        raise ValueError('Unknown action field')
    return {**base, **changes}


def schema(limit=64):
    return {'type': 'object', 'additionalProperties': False, 'required': ['actions'],
        'properties': {'actions': {'type': 'array', 'minItems': 1, 'maxItems': limit,
            'items': {'type': 'object', 'additionalProperties': False, 'required': list(FIELDS),
                'properties': {k: {'type': 'integer', 'minimum': 0,
                                  'maximum': 2 if k == 'speed' else (1 << w)-1}
                               for k, w in FIELDS.items()}}}}}


def validate_actions(payload, limit, require_initial_reset=False):
    if not isinstance(payload, dict) or set(payload) != {'actions'}:
        raise ValueError('Expected only actions')
    actions = payload['actions']
    if not isinstance(actions, list) or not 1 <= len(actions) <= limit:
        raise ValueError('Invalid cycle budget')
    for i, a in enumerate(actions):
        if not isinstance(a, dict) or set(a) != set(FIELDS):
            raise ValueError(f'Invalid cycle fields: {i}')
        if any(type(a[k]) is not int or not 0 <= a[k] < (1 << w) for k, w in FIELDS.items()):
            raise ValueError(f'Invalid width/type: {i}')
        if a['speed'] == 3 or (a['speed'] != 0 and a['read'] and a['write']):
            raise ValueError(f'Illegal speed/direction: {i}')
        if (not a['rst_n'] or a['sw_reset']) and a['valid']:
            raise ValueError(f'Command offered during reset: {i}')
    if require_initial_reset and (len(actions) < 2 or any(a['rst_n'] for a in actions[:2])):
        raise ValueError('Replay must start with common two-clock reset')
    return actions


def write_vectors(actions, path):
    path.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in actions))


def parse(log, actions):
    rows = []
    for line in log.splitlines():
        if not line.startswith('TRACE '):
            continue
        parts = line.split()[1:]
        if len(parts) != 1 + len(FIELDS) + 2*len(OUTPUTS):
            raise ValueError('Malformed fixed-driver trace')
        try:
            v = list(map(int, parts))
        except ValueError as e:
            raise ValueError('Unknown public output in trace') from e
        idx = 1+len(FIELDS)
        rows.append({'cycle': v[0], 'action': dict(zip(FIELDS, v[1:idx])),
                     'pre': dict(zip(OUTPUTS, v[idx:idx+len(OUTPUTS)])),
                     'post': dict(zip(OUTPUTS, v[idx+len(OUTPUTS):]))})
    if len(rows) != len(actions) or any(r['cycle'] != i or r['action'] != actions[i] for i, r in enumerate(rows)):
        raise ValueError('Trace input/length/order mismatch')
    return rows


def check_rows(rows):
    failures, assumptions = [], []
    queues = {'wr': deque(), 'rd': deque()}
    accepted = completed = aborted = 0
    pending = None
    burst_edges = expected_edges = 0
    burst_csid = None
    burst_config = None
    burst_last_cycle = None
    min_half_period = 1

    def fail(cycle, category, **detail):
        failures.append({'cycle': cycle, 'category': category, **detail})

    for row in rows:
        i, a, p, q = (row[k] for k in ('cycle', 'action', 'pre', 'post'))
        for sample in (p, q):
            for name in OUTPUTS:
                bound = 15 if name == 'sd_en' else 3 if name in ('csb', 'speed') else 1
                if type(sample[name]) is not int or not 0 <= sample[name] <= bound:
                    fail(i, 'unknown_or_out_of_width', output=name)
            if sample['csb'] == 0:
                fail(i, 'multiple_chip_selects')
            if sample['csb'] == 3 and sample['sd_en'] != 0:
                fail(i, 'drive_while_deselected')
        if not a['rst_n'] or a['sw_reset']:
            if not a['rst_n'] and any(p[k] != expected or q[k] != expected
                                      for k, expected in {'sck': 0, 'csb': 3, 'active': 0}.items()):
                fail(i, 'asynchronous_reset')
            if a['sw_reset'] and (q['active'] != 0 or q['csb'] != 3):
                fail(i, 'software_reset')
            aborted += sum(len(q_) for q_ in queues.values())
            queues = {'wr': deque(), 'rd': deque()}
            pending = None
            burst_edges = expected_edges = 0
            burst_csid = None
            burst_config = None
            burst_last_cycle = None
            continue

        cmd = {k: a[k] for k in COMMAND}
        if pending is not None and (not a['valid'] or cmd != pending):
            assumptions.append({'cycle': i, 'category': 'command_not_held_until_handshake'})
        pending = cmd if a['valid'] and not p['ready'] else None
        if p['rx_stall'] or p['tx_stall']:
            if any(p[k] for k in ('ready', 'wr', 'rd', 'sample', 'shift')):
                fail(i, 'stall_controls_not_suppressed')
            if any(q[k] != p[k] for k in ('sck', 'csb')):
                fail(i, 'stall_clock_or_select_changed')
        if not a['enable'] and any(p[k] for k in ('ready', 'wr', 'rd', 'shift')):
            fail(i, 'disabled_transfer')

        if a['valid'] and p['ready']:
            accepted += 1
            for direction, enabled in (('wr', a['write']), ('rd', a['read'])):
                if enabled:
                    queues[direction].append({'remaining': a['length']+1, 'command': accepted})
            cycles_per_byte = (8 >> a['speed']) if a['write'] or a['read'] else 1
            expected_edges += 2 * (a['length']+1) * cycles_per_byte
            if burst_csid is not None and burst_csid != a['csid'] and p['csb'] != 3:
                # Controller may accept a following CSID while retiring the old burst.
                # Such overlapping bursts are explicitly outside this scoreboard.
                assumptions.append({'cycle': i, 'category': 'overlapping_csids_not_supported'})
            config = tuple(a[k] for k in ('clkdiv', 'idle', 'lead', 'trail', 'full_cycle', 'cpha', 'cpol'))
            if burst_config is not None and config != burst_config and p['csb'] != 3:
                assumptions.append({'cycle': i, 'category': 'overlapping_configuration_not_supported'})
            burst_csid = a['csid']
            burst_config = config
            min_half_period = a['clkdiv']+1

        for direction, ready, last in (('wr', 'tx_ready', 'last_write'), ('rd', 'rx_ready', 'last_read')):
            if p[last] and not (p[direction] and a[ready]):
                fail(i, 'last_without_transfer', direction=direction)
            if p[direction]:
                if not a[ready]:
                    fail(i, 'transfer_without_ready', direction=direction)
                if not queues[direction]:
                    fail(i, 'unexpected_byte_transfer', direction=direction)
                else:
                    front = queues[direction][0]
                    expected_last = front['remaining'] == 1
                    if bool(p[last]) != expected_last:
                        fail(i, 'segment_last_flag', direction=direction,
                             expected=int(expected_last), actual=p[last])
                    front['remaining'] -= 1
                    if front['remaining'] == 0:
                        queues[direction].popleft()
                        completed += 1

        # Count only serial edges during a continuously selected public CS.
        if p['csb'] != 3 and q['csb'] == p['csb'] and q['sck'] != p['sck']:
            burst_edges += 1
            if burst_last_cycle is not None and i-burst_last_cycle < min_half_period:
                fail(i, 'serial_clock_too_fast', minimum=min_half_period)
            burst_last_cycle = i
        if p['csb'] != 3 and q['csb'] == 3:
            if burst_config is not None and q['sck'] != burst_config[-1]:
                fail(i, 'serial_idle_polarity', expected=burst_config[-1], actual=q['sck'])
            if burst_edges != expected_edges:
                fail(i, 'serial_edge_count', expected=expected_edges, actual=burst_edges)
            if any(queues.values()):
                fail(i, 'missing_byte_at_deselect')
            burst_edges = expected_edges = 0
            burst_csid = None
            burst_config = None
            burst_last_cycle = None
        if q['csb'] != 3 and burst_csid is not None and q['csb'] != (3 ^ (1 << burst_csid)):
            fail(i, 'wrong_chip_select', expected=3 ^ (1 << burst_csid), actual=q['csb'])
        if q['csb'] != 3 and burst_csid is None:
            fail(i, 'unexpected_chip_select')
        if p['csb'] == 3 and q['csb'] != 3 and burst_config is not None and q['sck'] != burst_config[-1]:
            fail(i, 'serial_idle_polarity', expected=burst_config[-1], actual=q['sck'])

    return {'checks': len(rows), 'accepted_commands': accepted, 'completed_direction_segments': completed,
            'aborted_direction_segments': aborted, 'pending_direction_segments': sum(map(len, queues.values())),
            'incomplete_serial_burst': expected_edges != 0, 'failures': failures,
            'distinct_defects': sorted({f['category'] for f in failures}),
            'assumption_violations': assumptions,
            'scope': 'Public command/data-control handshake, byte/last counts, selected serial edge counts, reset, pause and stall safety. No serial payload, analog timing, bounded liveness or full formal proof.',
            'verdict': 'input_or_scope_invalid' if assumptions else 'dut_violation' if failures else 'scoped_pass'}


def check(actions, log):
    return check_rows(parse(log, actions))
