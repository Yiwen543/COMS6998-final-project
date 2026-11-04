#!/usr/bin/env python3
"""Certify discovered SPI guard relations, saturate egg, then apply the old gate."""
import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path

from coverage import load
from preflight_spi_host import identity, map_counter
from preflight_heldout import verify_rewrites
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import SOURCE, verify_source

BASE = ROOT/'results/spi_host_semantic_v2_20261104'


def mapping(target, points):
    if target['outcome'] not in ('else', 'cond_else'):
        return map_counter(target, points)
    a = target['counter_anchor']
    hits = [p for p in points if p['source'] == a['source'] and p['line'] == a['line']
            and p['column'] == a['column'] and p['type'] == 'branch' and p['outcome'] == target['outcome']]
    return {'status': 'mapped', 'point': hits[0], 'basis': target['counter_anchor_basis']} if len(hits) == 1 else {
        'status': 'unresolved', 'reason': 'No unique exact opposite-polarity raw counter', 'candidates': hits}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--base', type=Path, default=BASE)
    args = cli.parse_args()
    base = args.base.resolve()
    verify_source()
    audit = json.loads((base/'ssa_audit/audit.json').read_text())
    extraction = json.loads((base/'ssa_audit/extraction.json').read_text())
    proof = json.loads((base/'netlist_proof/proof.json').read_text())
    if proof['status'] != 'pass' or not proof['environment_satisfiable']:
        raise AssertionError('Independent netlist proof has not passed')
    targets = {t['id']: t for t in audit['supported_targets']}
    rules = []
    for pair in audit['equivalent_pairs']:
        if not pair['source_expressions_differ']:
            continue
        a, b = targets[pair['left']], targets[pair['right']]
        if a['event_context'] != b['event_context']:
            raise AssertionError('Cannot import temporal-context mismatch')
        # Ground rules are drawn from every proved different pair, without
        # looking at coverage, calibration, or future model outcomes.
        rules.append({'name': f"qfbv-{a['id']}-{b['id']}", 'left': a['compact'], 'right': b['compact'],
            'proof_status': 'unsat', 'event_context': a['event_context'],
            'pair_proof': 'ssa_audit/pairs.smt2', 'source_ids': [a['id'], b['id']]})
    payload = {'targets': list(targets.values()), 'verified_rules': rules}
    (base/'egg-input.json').write_text(json.dumps(payload, indent=2)+'\n')
    response = subprocess.run([str(ROOT/'egraph/target/debug/guard_proofs')], input=json.dumps(payload),
                              text=True, capture_output=True, check=True, timeout=30)
    graph = json.loads(response.stdout)
    (base/'egg.json').write_text(json.dumps(graph, indent=2)+'\n')
    roots = {t['id']: t for t in graph['targets']}
    buckets = defaultdict(list)
    for t in targets.values():
        buckets[(tuple(t['event_context']), roots[t['id']]['eclass'])].append(t)
    statuses = {tuple(sorted(p)): status for p, status in zip(audit['pair_order'], audit['statuses'])}
    cal = ROOT/'results/spi_host_preflight_20261104/calibration'
    seed = load(cal/'seed.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
    indexes = {path.stem: {identity(p): p['hits'] for p in load(path, str(SOURCE.relative_to(ROOT)), include_descendants=True)}
               for path in sorted(cal.glob('*.dat'))}
    denomin = {identity(p) for p in seed}
    if any(set(i) != denomin for i in indexes.values()):
        raise AssertionError('Calibration denominator drift')
    mappings = {t['id']: mapping(t, seed) for t in targets.values()}
    groups = []
    for (context, eclass), members in buckets.items():
        if len({(t['source'], t['line'], t['column']) for t in members}) < 2:
            continue
        # Independently check every cross-source merge, not just imported pairs.
        for i, a in enumerate(members):
            for b in members[i+1:]:
                if (a['source'], a['line'], a['column']) == (b['source'], b['line'], b['column']):
                    continue
                if statuses[tuple(sorted((a['id'], b['id'])))] != 'unsat':
                    raise AssertionError('egg introduced a relation not certified by QF_BV')
        records = []
        for t in members:
            m = mappings[t['id']]
            r = {'id': t['id'], 'line': t['line'], 'source_text': t['source_text'], 'compact': t['compact'], 'mapping': m,
                 'eclass_before': roots[t['id']]['eclass_before']}
            if m['status'] == 'mapped':
                key = identity(m['point'])
                r['seed_hits'] = indexes['seed'][key]
                r['calibration_hits'] = {name: v[key] for name, v in indexes.items() if name != 'seed'}
            records.append(r)
        eligible = [r for r in records if r['mapping']['status'] == 'mapped' and r['seed_hits'] == 0
                    and any(r['calibration_hits'].values())]
        distinct_sites = {(r['mapping']['point']['source'], r['mapping']['point']['line'],
                           r['mapping']['point']['column']) for r in eligible}
        nontrivial = len(distinct_sites) >= 2 and len({r['eclass_before'] for r in eligible}) > 1
        groups.append({'eclass': eclass, 'event_context': list(context), 'members': records,
                       'qualified_member_ids': [r['id'] for r in eligible],
                       'qualified_source_group': len(distinct_sites) >= 2, 'nontrivial_egg_group': nontrivial})
    old = json.loads((ROOT/'results/spi_host_preflight_20261104/screen.json').read_text())
    config = ROOT/'configs/spi_host_b_development.json'
    threshold = json.loads(config.read_text())['static_acceptance']
    count = sum(g['qualified_source_group'] for g in groups)
    rewritten = sum(g['nontrivial_egg_group'] for g in groups)
    passed = count >= threshold['min_source_groups'] and rewritten >= threshold['min_rewrite_groups']
    additional = [ROOT/'scripts/spi_semantic_v2.py', ROOT/'scripts/spi_netlist_proof.py', Path(__file__),
                  ROOT/'configs/spi_host_v2_analysis_plan.json',
                  ROOT/'scripts/run_spi_host_b_development.py',
                  ROOT/'egraph/src/bin/guard_proofs.rs', base/'ssa_audit/audit.json',
                  base/'netlist_proof/proof.json', base/'egg-input.json', base/'egg.json']
    result = {**old, 'status': 'eligible_for_B_development' if passed else 'rejected_at_static_gate',
        'method_version': 'v2: Slang SSA + independent Yosys-cell proof + QF_BV ground-rule discovery + bounded egg saturation',
        'discovery_attribution': 'Z3 discovers/proves design-dependent relations; egg saturates certified ground rules and records explanations. Not pure six-rule discovery.',
        'qualified_for_model_trial': passed, 'groups': groups, 'source_mappings': mappings,
        'qualified_source_groups': count, 'qualified_rewrite_groups': rewritten,
        'mapped_targets': sum(m['status'] == 'mapped' for m in mappings.values()),
        'unresolved_targets': sum(m['status'] != 'mapped' for m in mappings.values()),
        'unsupported': extraction['unsupported']+audit['unresolved_definitions'],
        'config_sha256': sha(config), 'hashes': {**old['hashes'], **{str(p.relative_to(ROOT)): sha(p) for p in additional}},
        'rewrite_proofs': verify_rewrites(), 'pair_audit_counts': audit['counts'],
        'interpretation': 'Development eligibility only. Retain separate raw counters. Must pass independent B progress gate and independent checker audit before formal A/B/C/P.'}
    (base/'screen.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'qualified_source_groups', 'qualified_rewrite_groups',
        'mapped_targets', 'unresolved_targets')}, indent=2))
    for g in groups:
        if g['nontrivial_egg_group']:
            print('NONTRIVIAL', [(m['line'], m['mapping']['point']['outcome']) for m in g['members'] if m['id'] in g['qualified_member_ids']])


if __name__ == '__main__':
    main()
