"""Exact public G1 text/VCD subset. Not a legacy-run or G0 adapter."""
from pathlib import Path
import re


class Unqualified(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Unqualified(message)


def parse_rows(text, case, simulator):
    pattern = re.compile(r'^OBS qc=(\d+) cycle=(\d+) phase=(pre|post) tick=(\d+) '
        r'q=([01xz]{4}) active=([01xz]) ok=([01xz]) marker=([01xz]) '
        r'a=([01xz]{4}) b=([01xz]{4}) rst=([01xz]) en=([01xz]) valid=([01xz])$', re.M)
    matches = list(pattern.finditer(text))
    need(len(matches) == 8, 'EXPECTED_EXACTLY_EIGHT_OBSERVATIONS')
    need(len(re.findall(r'^OBS ', text, re.M)) == len(matches), 'MALFORMED_EXTRA_OBSERVATION')
    rows = []
    expected = case['physical_rows_expected_icarus']
    for index, match in enumerate(matches):
        vals = match.groups()
        need(int(vals[0]) == int(case['id'][2:]), 'QC_ID')
        row = dict(zip(['cycle', 'phase', 'tick', 'q', 'active', 'ok', 'marker',
                        'a', 'b', 'rst', 'en', 'valid'], vals[1:]))
        row['cycle'] = int(row['cycle'])
        row['tick'] = int(row['tick'])
        for field, value in expected[index].items():
            if field == 'ok' and simulator == 'verilator' and case['id'] in ['QC12', 'QC13']:
                continue  # preregistered four-state exclusion, never semantic credit
            need(row[field] == value, 'PHYSICAL_EXPECTED_MISMATCH:' + field)
        rows.append(row)
    need(re.search(r'^END qc=' + str(int(case['id'][2:])) +
                   r' cycles=4 posedges=4$', text, re.M), 'EDGE_COUNT_TRAILER')
    return rows


def parse_vcd(path):
    path = Path(path)
    need(path.stat().st_size <= 2_000_000, 'VCD_SIZE_LIMIT')
    text = path.read_text()
    header, body = text.split('$enddefinitions $end', 1)
    scale = re.search(r'\$timescale\s+(\d+)\s*(s|ms|us|ns|ps|fs)\s+\$end', header)
    need(scale is not None, 'VCD_TIMESCALE')
    scopes, wires = [], {}
    for line in header.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == '$scope':
            scopes.append(parts[2])
        elif parts[0] == '$upscope':
            need(bool(scopes), 'VCD_SCOPE_UNDERFLOW')
            scopes.pop()
        elif parts[0] == '$var':
            width = int(parts[2])
            need(0 < width <= 4096, 'VCD_WIDTH')
            wires['.'.join(scopes + [parts[4]])] = (parts[3], width)
    need(bool(wires), 'VCD_EMPTY_HEADER')
    values, samples, tick = {}, [], 0
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith('$'):
            continue
        if line.startswith('#'):
            samples.append((tick, values.copy()))
            new_tick = int(line[1:])
            need(new_tick >= tick, 'VCD_TIME_ORDER')
            tick = new_tick
        elif line[0] in 'bB':
            bits, identifier = line[1:].split()
            need(set(bits.lower()) <= set('01xz'), 'VCD_VECTOR_VALUE')
            values[identifier] = bits.lower()
        elif line[0].lower() in '01xz':
            values[line[1:]] = line[0].lower()
        else:
            raise Unqualified('UNSUPPORTED_VCD_VALUE:' + line[:30])
    samples.append((tick, values.copy()))
    return {'scale': scale.groups(), 'wires': wires, 'samples': samples}


def signal(vcd, state, suffix, width):
    hits = [(name, desc) for name, desc in vcd['wires'].items()
            if name == suffix or name.endswith('.' + suffix)]
    need(len(hits) == 1, 'VCD_SIGNAL_AMBIGUOUS_OR_ABSENT:' + suffix)
    identifier, declared_width = hits[0][1]
    need(declared_width == width, 'VCD_DECLARED_WIDTH:' + suffix)
    need(identifier in state, 'VCD_VALUE_ABSENT:' + suffix)
    bits = state[identifier]
    need(len(bits) <= width, 'VCD_VALUE_TOO_WIDE:' + suffix)
    return bits.rjust(width, bits[0] if bits[0] in 'xz' else '0')


def bind_physical_vcd(vcd, rows, case):
    need(vcd['scale'] == ('1', 'ps'), 'PHYSICAL_VCD_SCALE_NOT_REGISTERED_1PS')
    unit = 'physical_tb.units[' + str(int(case['id'][2:])) + '].u.'
    for row in rows:
        states = [state for tick, state in vcd['samples'] if tick <= row['tick']]
        need(bool(states), 'VCD_NO_PRIOR_SAMPLE')
        state = states[-1]
        for field, width in [('a', 4), ('b', 4), ('rst', 1), ('en', 1),
                             ('valid', 1), ('marker', 1)]:
            need(signal(vcd, state, 'physical_tb.' + field, width) == row[field],
                 'VCD_ROW_MISMATCH:' + field)
        for field, width in [('q', 4), ('active', 1), ('ok', 1)]:
            need(signal(vcd, state, unit + field, width) == row[field],
                 'VCD_ROW_OUTPUT:' + field)
        need(signal(vcd, state, 'physical_tb.clk', 1) ==
             ('0' if row['phase'] == 'pre' else '1'), 'VCD_ROW_CLOCK_PHASE')
    # No comparison of physical post to a delayed native pre sample.


def selected_native_alarm(vcd):
    hits = []
    for tick, state in vcd['samples']:
        try:
            active = signal(vcd, state, 'formal_top.sampled_active', 1)
            ok = signal(vcd, state, 'formal_top.sampled_ok', 1)
            cycle = signal(vcd, state, 'formal_top.sampled_cycle', 3)
            q = signal(vcd, state, 'formal_top.sampled_q', 4)
        except Unqualified:
            continue
        if active == '1' and ok == '0' and set(cycle + q) <= set('01'):
            hits.append(dict(native_tick=tick, cycle=int(cycle, 2), phase='pre',
                             slot=0, q=q, active=active, ok=ok))
    need(bool(hits), 'NO_KNOWN_REGISTERED_PRE_ALARM')
    return hits[-1]


def eligibility(case):
    return case['eligibility'] not in ['INELIGIBLE_VACUOUS', 'UNSUPPORTED_FOUR_STATE_EQUIVALENCE']


def phase_binding(case):
    need(case['selected_phase'] == 'pre', 'UNSUPPORTED_SELECTED_PHASE')
    return 'MATCH' if case['reported_phase_claim'] == case['selected_phase'] else 'REJECT'
