"""Read Verilator Coverage-3 counters, keeping source/outcome identity intact."""
import re
from pathlib import Path

DUT_SOURCE = 'examples/arbiter/rtl/fixed_priority_arbiter.sv'

def load(path, dut_source=DUT_SOURCE, dut_instance='dut', include_descendants=False):
    text = Path(path).read_text()
    if not text.startswith('# SystemC::Coverage-3'):
        raise ValueError('Unsupported coverage format')
    points = []
    for row in text.splitlines()[1:]:
        if not row.strip(): continue
        m = re.fullmatch(r"C '(.*)' (\d+)", row)
        if not m: raise ValueError(f'Malformed coverage row: {row!r}')
        fields = dict(part.split('\x02', 1) for part in m[1].split('\x01') if part)
        source = fields.get('f', '').replace('\\', '/')
        if not (source == dut_source or source.endswith('/' + dut_source)):
            continue
        hierarchy = fields.get('h', '')
        if include_descendants:
            parts = hierarchy.split('.')
            if dut_instance not in parts:
                continue
        elif not hierarchy.endswith('.' + dut_instance):
            continue
        points.append({'source': dut_source, 'line': int(fields['l']),
                       'column': int(fields.get('n', 0)), 'type': fields['t'],
                       'outcome': fields.get('o', ''), 'hierarchy': fields['h'],
                       'span': fields.get('S'), 'hits': int(m[2])})
    if not points: raise ValueError('No DUT counters found')
    return points

def summary(points):
    result = {}
    for kind in sorted({p['type'] for p in points}):
        group = [p for p in points if p['type'] == kind]
        covered = sum(p['hits'] > 0 for p in group)
        result[kind] = {'covered': covered, 'total': len(group),
                        'percent': round(100 * covered / len(group), 3)}
    return result

def join(targets, graph, points):
    roots = {t['id']: t for t in graph['targets']}
    feedback = []
    for target in targets:
        matches = [p for p in points if p['line'] == target['line']
                   and p['type'] == target['counter_type']
                   and p['outcome'] == target['counter_outcome']]
        if len(matches) != 1:
            raise ValueError(f'Expected unique coverage mapping for {target["id"]}: {matches}')
        p = matches[0]
        feedback.append({**target, **roots[target['id']], 'hits': p['hits'],
                         'coverage_point': p, 'uncovered': p['hits'] == 0})
    return feedback
