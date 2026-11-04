#!/usr/bin/env python3
"""Outcome-blind SPI source/event/counter and calibration gate. No LLM calls."""
import argparse
import json
import subprocess
import time
from pathlib import Path

from coverage import load, summary
from run_midterm_fixed import ROOT, invoke, sha
from run_spi_host_fixed import BASE, SOURCE, SOURCES, DRIVER, verify_source
from slang_guard_adapter import Adapter

SLANG = ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin/slang'
GATE = ROOT/'configs/spi_host_b_development.json'


def identity(point):
    return tuple(point[k] for k in ('source', 'line', 'column', 'type', 'outcome', 'hierarchy'))


def map_counter(target, points):
    anchor = target['counter_anchor']
    allowed = {('line', 'case')} if target['outcome'] == 'case' else (
        {('branch', 'if'), ('line', 'if'), ('line', 'elsif')} if target['outcome'] == 'if'
        else {('branch', 'cond_then')})
    candidates = [p for p in points if p['source'] == anchor['source'] and
                  p['line'] == anchor['line'] and p['column'] == anchor['column'] and
                  (p['type'], p['outcome']) in allowed]
    if len(candidates) == 1:
        return {'status': 'mapped', 'point': candidates[0],
                'basis': target.get('counter_anchor_basis', 'AST token')+'; exact file/line/column and true-path counter kind; no line-only fallback'}
    return {'status': 'unresolved', 'reason': 'No unique exact AST arm/keyword counter',
            'anchor': anchor, 'candidates': candidates}


def resolve_clock_alias(bits, net):
    """Only unique, width-preserving $buf connections; never infer inversion."""
    chain, seen = [], set()
    while True:
        key = tuple(bits)
        if key in seen:
            raise AssertionError('Clock alias cycle')
        seen.add(key)
        drivers = [(name, c) for name, c in net['cells'].items() if c['type'] == '$buf'
                   and c['connections']['Y'] == bits]
        if not drivers:
            return bits, chain
        if len(drivers) != 1:
            raise AssertionError('Ambiguous clock alias')
        name, cell = drivers[0]
        source = cell['connections']['A']
        if len(source) != len(bits) or int(cell['parameters']['WIDTH'], 2) != len(bits):
            raise AssertionError('Clock alias width mismatch')
        chain.append({'cell': name, 'from': bits, 'to': source, 'kind': '$buf'})
        bits = source


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, default=ROOT/'results/spi_host_preflight_20261104')
    cli.add_argument('--calibration', type=Path, default=ROOT/'results/spi_host_preflight_20261104/calibration')
    args = cli.parse_args()
    out, cal = args.output.resolve(), args.calibration.resolve()
    out.mkdir(parents=True, exist_ok=True)
    verify_source()
    ast = out/'ast.json'
    command = [SLANG, '--single-unit', '--top', 'spi_host_fsm', '-G', 'NumCS=2', '-D', 'SYNTHESIS',
               '-I', str((BASE/'prim/rtl').relative_to(ROOT)), '--ast-json', ast,
               '--ast-json-source-info', '--ast-json-detailed-types',
               *[s.relative_to(ROOT) for s in SOURCES]]
    frontend_seconds, _ = invoke(command, out/'slang.log', timeout=60)
    started = time.perf_counter()
    semantic = Adapter(json.loads(ast.read_text()), 'spi_host_fsm').extract().evidence()
    semantic_seconds = time.perf_counter()-started
    (out/'semantic.json').write_text(json.dumps(semantic, indent=2)+'\n')
    cases = json.loads((cal/'summary.json').read_text())['cases']
    if any(c['checker']['verdict'] != 'scoped_pass' for c in cases.values()):
        raise AssertionError('Calibration failed specification/assumption checks')
    seed = load(cal/'seed.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
    indexes = {}
    for name in cases:
        points = load(cal/f'{name}.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
        indexes[name] = {identity(p): p['hits'] for p in points}
        if set(indexes[name]) != {identity(p) for p in seed}:
            raise AssertionError('Calibration denominator changed')
    mappings = {t['id']: map_counter(t, seed) for t in semantic['targets']}
    groups = []
    for group in semantic['groups']:
        members = []
        for m in group['members']:
            mapping = mappings[m['id']]
            member = {'id': m['id'], 'line': m['line'], 'source_text': m['source_text'], 'mapping': mapping}
            if mapping['status'] == 'mapped':
                key = identity(mapping['point'])
                member['seed_hits'] = indexes['seed'][key]
                member['calibration_hits'] = {name: points[key] for name, points in indexes.items() if name != 'seed'}
            members.append(member)
        eligible_members = [m for m in members if m['mapping']['status'] == 'mapped' and m['seed_hits'] == 0
                            and any(m['calibration_hits'].values())]
        groups.append({'eclass': group['eclass'], 'event_context': group['event_context'],
            'distinct_expressions': group['distinct_expressions'], 'members': members,
            'qualified_member_ids': [m['id'] for m in eligible_members],
            'qualified_source_group': len(eligible_members) >= 2,
            'nontrivial_egg_group': len(eligible_members) >= 2 and group['distinct_expressions'] > 1})
    config = json.loads(GATE.read_text())
    threshold = config['static_acceptance']
    num_groups = sum(g['qualified_source_group'] for g in groups)
    num_rewrite = sum(g['nontrivial_egg_group'] for g in groups)
    qualified = num_groups >= threshold['min_source_groups'] and num_rewrite >= threshold['min_rewrite_groups']
    # Cross-check AST events against emitted top-level sequential cells. This
    # verifies clock/reset connection and polarity, not sequential equivalence.
    net = json.loads((ROOT/'results/natural_ip_parameter_screen_20261103/spi_host_slang/netlist.json').read_text())['modules']['spi_host_fsm']
    cells = {n: c for n, c in net['cells'].items() if c['type'] == '$aldff'}
    event_checks = []
    for name, c in cells.items():
        clock, clock_chain = resolve_clock_alias(c['connections']['CLK'], net)
        reset, reset_chain = resolve_clock_alias(c['connections']['ALOAD'], net)
        valid = (clock == net['ports']['clk_i']['bits'] and
                 reset == net['ports']['rst_ni']['bits'] and
                 int(c['parameters']['CLK_POLARITY'], 2) == 1 and
                 int(c['parameters']['ALOAD_POLARITY'], 2) == 0)
        event_checks.append({'cell': name, 'posedge_clk_negedge_reset': valid, 'source': c['attributes'].get('src'),
                             'clock_aliases': clock_chain, 'reset_aliases': reset_chain})
    if not cells or not all(c['posedge_clk_negedge_reset'] for c in event_checks):
        raise AssertionError('Yosys and Slang clock/reset evidence disagree')
    result = {'status': 'eligible_for_B_development' if qualified else 'rejected_at_static_gate',
        'model_calls': 0, 'qualified_for_model_trial': qualified, 'gate': threshold,
        'config_sha256': sha(GATE), 'qualified_source_groups': num_groups,
        'qualified_rewrite_groups': num_rewrite, 'groups': groups, 'source_mappings': mappings,
        'mapped_targets': sum(m['status'] == 'mapped' for m in mappings.values()),
        'unresolved_targets': sum(m['status'] != 'mapped' for m in mappings.values()),
        'unsupported': semantic['unsupported'], 'seed_coverage': summary(seed),
        'raw_counter_denominator': {kind: value['total'] for kind, value in summary(seed).items()},
        'coverage_identity': list(('source', 'line', 'column', 'type', 'outcome', 'hierarchy')),
        'reachability': 'Independent public-spec checker calibration; not a formal proof. No calibrated actions allowed in prompts.',
        'event_checks': event_checks, 'frontend_seconds': frontend_seconds, 'semantic_seconds': semantic_seconds,
        'slang_command': list(map(str, command)), 'hashes': {str(p.relative_to(ROOT)): sha(p) for p in [*SOURCES, DRIVER,
            ROOT/'scripts/slang_guard_adapter.py', ROOT/'scripts/spi_host_fixture.py',
            ROOT/'scripts/run_spi_host_fixed.py', ROOT/'scripts/run_spi_host_b_development.py',
            ROOT/'scripts/coverage.py', ROOT/'scripts/pilot_model.py', ROOT/'egraph/src/main.rs',
            ROOT/'examples/heldout_spi_host/contract.md', ROOT/'examples/heldout_spi_host/stimulus.schema.json',
            ROOT/'examples/heldout_spi_host/seed.json', Path(__file__), GATE]},
        'interpretation': 'AST-identical duplicates do not demonstrate a rewrite opportunity. Unsupported hierarchy is unresolved, not proved irrelevant. Do not run B or A/B/C/P unless all static gates pass.'}
    (out/'screen.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'qualified_source_groups', 'qualified_rewrite_groups',
        'mapped_targets', 'unresolved_targets', 'raw_counter_denominator', 'model_calls')}, indent=2))


if __name__ == '__main__':
    main()
