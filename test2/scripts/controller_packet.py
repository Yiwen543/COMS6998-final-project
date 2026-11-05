#!/usr/bin/env python3
"""Lossless public-only B/C task packet, no recursive workspace reads."""
from collections import defaultdict
import json
from pathlib import Path
import re
from common import ROOT, BASE, dump, sha
from controller_prepare import INPUTS, OUTPUTS

TASK = BASE / 'tasks/axis_length_fifo_v1'
IDENTITY = ('source', 'line', 'column', 'type', 'outcome', 'hierarchy', 'span')


def identity(p):
    return tuple(p[k] for k in IDENTITY)


def rle(values):
    runs = []
    for value in values:
        if runs and runs[-1][0] == value:
            runs[-1][1] += 1
        else:
            runs.append([value, 1])
    return runs


def unrle(runs):
    return [value for value, count in runs for _ in range(count)]


def pack_coverage(pointsets):
    # Grouping is storage compression, never shared or transferred source hits.
    first = pointsets[0]
    by_trace = [{identity(p): p['hits'] for p in points} for points in pointsets]
    if any(set(d) != set(by_trace[0]) for d in by_trace):
        raise ValueError('Raw counter identity changed')
    sites = defaultdict(list)
    ordinary = []
    for p in first:
        match = re.fullmatch(r'(.+?)(?:\[(\d+)\])?:(0->1|1->0)', p['outcome'])
        if p['type'] != 'toggle' or not match or p['span'] is not None:
            ordinary.append([*[p[k] for k in IDENTITY], *[d[identity(p)] for d in by_trace]])
            continue
        base, bit, direction = match.groups()
        key = (p['source'], p['line'], p['column'], p['hierarchy'], base, bit is not None)
        sites[key].append((int(bit) if bit is not None else 0, direction, p))
    packed = []
    for key, points in sites.items():
        points.sort(key=lambda x: (x[0], x[1]))
        pairs = [(b, d) for b, d, _ in points]
        bits = sorted({b for b, _, _ in points})
        complete = pairs == [(b, d) for b in bits for d in ('0->1', '1->0')]
        if not complete:
            for _, _, p in points:
                ordinary.append([*[p[k] for k in IDENTITY], *[d[identity(p)] for d in by_trace]])
            continue
        packed.append({'site': list(key), 'bits': bits,
                       'hits_rle': [rle([d[identity(p)] for _, _, p in points]) for d in by_trace]})
    return {'encoding': 'separate_bit_direction_hits_rle_v1', 'ordinary_columns': list(IDENTITY),
            'ordinary_rows': ordinary, 'toggle_sites': packed, 'trace_count': len(pointsets),
            'counter_count': len(first),
            'rule': 'For each listed bit in order, keep separate0->1 and1->0 counters. Decode run[value,count] arrays; no source counter is merged.'}


def unpack_coverage(packed, trace):
    rows = [dict(zip(IDENTITY, r[:7]), hits=r[7+trace]) for r in packed['ordinary_rows']]
    for site in packed['toggle_sites']:
        source, line, column, hierarchy, base, indexed = site['site']
        hits = iter(unrle(site['hits_rle'][trace]))
        for bit in site['bits']:
            for direction in ('0->1', '1->0'):
                rows.append(dict(source=source, line=line, column=column, hierarchy=hierarchy,
                                 type='toggle', outcome=base+(f'[{bit}]' if indexed else '')+':'+direction,
                                 span=None, hits=next(hits)))
    return rows


def semantic_feedback():
    base = TASK / 'qualification/typed-v5/screen'
    screen = json.loads((base / 'screen.json').read_text())
    extraction = json.loads((base / 'extraction.json').read_text())
    targets = {t['id']: t for t in extraction['targets']}
    groups = []
    # Outcome-blind selection: transfer cutoff and padding exit, both polarities.
    for g in screen['groups']:
        if not g['nontrivial_static_candidate'] or {m['line'] for m in g['members']} not in ({327, 333}, {409, 421}):
            continue
        members = []
        for m in g['members']:
            t = targets[m['id']]
            point = {k: v for k, v in m['mapping']['point'].items() if k != 'hits'}
            members.append({'source_point': point, 'source_text': m['source_text'],
                            'complete_activation_guard': t['compact'],
                            'guard_depth': t['guard_depth'], 'mapping_basis': m['mapping']['basis']})
        groups.append({'eclass': g['eclass'], 'event_context': g['event_context'], 'members': members})
    if len(groups) != 4:
        raise ValueError('Predeclared semantic groups unavailable')
    atoms = set(re.findall(r'p_[a-f0-9]+', json.dumps(groups)))
    return {'scope': 'Two-state combinational equivalence with full activation and source context; not specification or sequential correctness',
            'engine': 'egg0.11.0 with independently certified typed definitions and QF_BV ground rules',
            'groups': groups, 'typed_atoms': {k: extraction['atoms'][k] for k in sorted(atoms)},
            'count_basis': 'No unhit claim: exact fixed per-development-trace counts are in the shared coverage packet.',
            'observer_boundary': 'Internal terms describe implementation; candidate monitors can observe public pins only.'}


def packet(arm):
    if arm not in ('B2_raw', 'C2_semantic'):
        raise ValueError('Unsupported arm')
    names = ['basic', 'boundary_pressure', 'reset_reuse']
    folder = TASK / 'qualification/observations-v2/verilator'
    pointsets = [json.loads((folder / n / 'raw-points.json').read_text()) for n in names]
    coverage = pack_coverage(pointsets)
    for i, points in enumerate(pointsets):
        original = {identity(p): p['hits'] for p in points}
        decoded = {identity(p): p['hits'] for p in unpack_coverage(coverage, i)}
        if original != decoded or len(original) != len(points):
            raise ValueError('Coverage compression changed a counter')
    development = {}
    for name in names:
        rows = json.loads((folder / name / 'rows.json').read_text())
        columns = ['cycle'] + ['input_'+k for k in INPUTS] + [p+'_'+k for p in ('pre', 'post') for k in OUTPUTS]
        packed = [[r['cycle']] + [r['inputs'][k] for k in INPUTS] + [r[p][k] for p in ('pre', 'post') for k in OUTPUTS] for r in rows]
        development[name] = {'columns': columns, 'rows': packed}
    files = ['rtl/axis_frame_length_adjust.v', 'rtl/axis_fifo.v', 'rtl/axis_frame_length_adjust_fifo.v', 'task_top_v3.sv']
    data = {'specification': (TASK / 'public/specification.md').read_text(),
            'observer_contract': (TASK / 'public/observer_contract.md').read_text(),
            'rtl': {name: (TASK / 'public' / name).read_text() for name in files},
            'development': development, 'coverage_trace_order': names, 'raw_coverage': coverage}
    if arm == 'C2_semantic':
        data['egraph_feedback'] = semantic_feedback()
    return data


def main():
    out = TASK / 'qualification/prompt-audit-v1'
    out.mkdir(exist_ok=False)
    b, c = packet('B2_raw'), packet('C2_semantic')
    common = dict(c)
    common.pop('egraph_feedback')
    if b != common:
        raise ValueError('B/C common information differs')
    for arm, data in [('B2_raw', b), ('C2_semantic', c)]:
        dump(out / (arm+'.json'), data)
    dump(out / 'summary.json', {'common_information_equal': True, 'raw_counters_roundtrip': b['raw_coverage']['counter_count'],
         'semantic_groups': len(c['egraph_feedback']['groups']), 'prompt_bytes': {a: (out/(a+'.json')).stat().st_size for a in ('B2_raw','C2_semantic')},
         'provider_token_count_status': 'PENDING_API_COUNT_NO_ESTIMATE_CLAIM', 'candidate_generation_allowed': False,
         'packet_source_sha256': sha(Path(__file__))})
    print((out / 'summary.json').read_text())


if __name__ == '__main__':
    main()
