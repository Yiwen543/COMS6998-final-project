"""Recompute the conditional-domain and ordinary-exclusion evidence.

Never changes historical results or commissions a model. Transport validation
does not supply expected functional outputs and is not a specification checker.
"""
import json
import subprocess
import sys
from pathlib import Path

from run_midterm_fixed import ROOT, sha
from prove_wbxbar_index import configuration, SCOPE
from wbxbar_conditional_semantics import verify_certificate, CERTIFICATE
from probe_wbxbar_ordinary import cases, validate, driver, parse, comparable
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from probe_natural_frontends import TOOLS
from spi_core_safe_experiment import verify_freeze

BASE = ROOT / 'results/wbxbar_conditional_20261104'


def audit():
    scope, candidate = configuration()
    parent = json.loads((ROOT / scope['parent_scope']['path']).read_text())
    for key in ('development_budget', 'model_limits', 'development_acceptance',
                'offline_acceptance', 'event_discrimination', 'roles'):
        assert scope[key] == parent[key], ('Changed preregistered constraint', key)
    cert = verify_certificate()
    verify_freeze()
    hash_checks = len(cert['hashes'])
    # Verify, but do not rewrite or rerun, prior candidate evidence.
    for old in (ROOT / 'results/transaction_recovery_screen_20261104').glob('*-final'):
        for name in ('decision.json', 'proof/proof.json', 'screen/screen.json'):
            path = old / name
            if path.exists():
                for file, digest in json.loads(path.read_text()).get('hashes', {}).items():
                    assert sha(Path(file)) == digest, file
                    hash_checks += 1
    screen_dir = BASE / 'screen-v2'
    screen = json.loads((screen_dir / 'screen/screen.json').read_text())
    proof = json.loads((screen_dir / 'proof/proof.json').read_text())
    for name in ('decision.json', 'proof/proof.json', 'screen/screen.json'):
        for file, digest in json.loads((screen_dir / name).read_text()).get('hashes', {}).items():
            assert sha(Path(file)) == digest, file
            hash_checks += 1
    assert proof['status'] == 'pass' and proof['environment_satisfiable']
    assert all(row['z3'] == 'unsat' for row in proof['definition_checks'])
    assert not proof['unsafe_free_combinational_values']
    membership = json.loads((screen_dir / 'inventory/exact-counter-membership.json').read_text())
    assert sha(screen_dir / 'inventory/seed.dat') == membership['raw_sha256']
    for file, digest in membership['generated_hashes'].items():
        assert sha(Path(file)) == digest, file
        hash_checks += 1

    ordinary = BASE / 'ordinary-v1'
    summary = json.loads((ordinary / 'summary.json').read_text())
    assert summary['script_sha256'] == sha(ROOT / 'scripts/probe_wbxbar_ordinary.py')
    assert summary['scope_sha256'] == sha(SCOPE)
    assert summary['screen_sha256'] == sha(screen_dir / 'screen/screen.json')
    ports = json.loads((screen_dir / 'netlist.json').read_text())['modules']['wbxbar']['ports']
    tb, ins, outs = driver(candidate, ports)
    assert tb == (ordinary / 'tb_natural_inventory.sv').read_text()
    assert summary['driver_sha256'] == sha(ordinary / 'tb_natural_inventory.sv')
    registered_cases = cases()
    assert registered_cases == json.loads((ordinary / 'cases.json').read_text())
    raw_seed = json.loads((screen_dir / 'inventory/raw-points.json').read_text())
    denominator = {identity(point) for point in raw_seed}
    assert len(denominator) == len(raw_seed) == summary['raw_denominator']
    files = [str(Path(candidate['root']) / file) for file in candidate['sources']]
    evidence_hashes = {}
    executions, union_counts, first_hits, per_kind = [], {}, {}, {}
    for name, actions in registered_cases.items():
        validate(actions)
        traces = {}
        for simulator in ('verilator', 'iverilog'):
            folder = ordinary / name / simulator
            log = (folder / 'simulation.log').read_text()
            execution = json.loads((folder / 'execution.json').read_text())
            assert execution['cycles'] == len(actions)
            assert 'DRIVER_OK steps=' + str(len(actions)) in log
            traces[simulator] = parse(log, actions, ins, outs)
            assert traces[simulator] == json.loads((folder / 'trace.json').read_text())
            executions.append({'case': name, 'simulator': simulator, **execution})
            for file in folder.glob('*'):
                if file.is_file(): evidence_hashes[str(file)] = sha(file)
        assert comparable(traces['verilator'], outs) == comparable(traces['iverilog'], outs), name
        points = load_all(ordinary / name / 'verilator/coverage.dat', files)
        assert {identity(point) for point in points} == denominator
        for point in points:
            key = identity(point)
            union_counts[key] = union_counts.get(key, 0) + point['hits']
            per_kind[key] = point['type']
            if point['hits'] > 0:
                first_hits.setdefault(key, {'case': name, 'hits': point['hits']})
    union = {key for key, count in union_counts.items() if count > 0}
    assert len(union) == summary['ordinary_union_covered']
    assert len(executions) == summary['executions']
    assert sum(e['cycles'] for e in executions) == summary['executed_cycles']
    groups = []
    for group in screen['groups']:
        if not group['static_candidate_group']: continue
        members = {identity(m['mapping']['point']) for m in group['members'] if m['seed_zero_dynamic_candidate']}
        groups.append({'eclass': group['eclass'], 'nontrivial': group['nontrivial_static_candidate'],
                       'all_members_hit_by_ordinary': members <= union,
                       'sources': [{'identity': key, 'sum_hits_separate_runs': union_counts[key],
                                    'first_case_in_registered_order': first_hits.get(key)} for key in sorted(members)]})
    assert len(groups) == 8 and all(g['all_members_hit_by_ordinary'] for g in groups)
    assert not summary['surviving_groups'] and not summary['ordinary_gate_pass']
    assert not summary['B_allowed'] and not summary['C_allowed']
    tests = []
    for pattern in ('test_wbxbar*.py', 'test_transaction*.py', 'test_multistep_event_screen.py',
                    'test_spi_core_safe_driver.py', 'test_spi_core_safe_accounting.py'):
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v']
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
        path = BASE / (pattern.replace('*', '_').replace('.py', '') + '.log')
        path.write_text(result.stdout + result.stderr)
        tests.append({'pattern': pattern, 'returncode': result.returncode, 'command': command,
                      'log': str(path), 'sha256': sha(path)})
        assert result.returncode == 0, path
    versions = {}
    for name, command in {'python': [sys.executable, '--version'], 'verilator': ['verilator', '--version'],
                          'icarus': ['iverilog', '-V'], 'yosys': [str(TOOLS / 'yosys'), '-V'],
                          'sby': [str(TOOLS / 'sby'), '--version'], 'slang': [str(TOOLS / 'slang'), '--version'],
                          'z3': ['z3', '--version'], 'formal_z3': [str(TOOLS / 'z3'), '--version'],
                          'rust': ['rustc', '--version'],
                          'cargo': ['cargo', '--version']}.items():
        result = subprocess.run(command, text=True, capture_output=True, check=True, timeout=30)
        versions[name] = result.stdout.splitlines()[0]
    egg = json.loads((screen_dir / 'screen/egg.json').read_text())
    versions['egg'] = egg['engine']
    formal = [{'path': str(p.relative_to(ROOT)), **json.loads(p.read_text())} for p in sorted(BASE.glob('formal*/*-result.json'))]
    inventories = [json.loads(p.read_text()) for p in sorted(BASE.glob('screen-*/inventory/inventory.json'))]
    probes = [r for p in BASE.glob('screen-*/probe.json') for r in json.loads(p.read_text())['runs']]
    decisions = [json.loads(p.read_text()) for p in BASE.glob('screen-*/decision.json')]
    kind_counts = {kind: {'covered': sum(k in union for k in denominator if per_kind[k] == kind),
                          'total': sum(per_kind[k] == kind for k in denominator)} for kind in sorted(set(per_kind.values()))}
    result = {'status': 'conditional_semantics_pass_ordinary_gate_rejected', 'scope_sha256': sha(SCOPE),
              'script_sha256': sha(Path(__file__)), 'certificate_sha256': sha(CERTIFICATE),
              'baseline_commit': scope['repository_commit'], 'old_freeze_and_prior_evidence_unchanged': True,
              'budget_and_role_constraints_unchanged': True, 'provenance_hash_checks': hash_checks,
              'conditional_lemma': cert['lemma'], 'definition_checks': len(proof['definition_checks']),
              'mapped': screen['mapped'], 'unresolved': screen['unresolved'], 'static_groups': groups,
              'ordinary_coverage_union': kind_counts, 'ordinary_execution_evidence_hashes': evidence_hashes,
              'accounting': {'formal_jobs': len(formal), 'formal_seconds': sum(r['seconds'] for r in formal),
                             'screen_attempts': len(decisions), 'frontend_invocations': len(probes),
                             'frontend_failures': sum(r['returncode'] != 0 for r in probes),
                             'inventory_compilations': len(inventories), 'ordinary_compilations': len(summary['compilations']),
                             'inventory_executions': len(inventories), 'ordinary_executions': len(executions),
                             'inventory_cycles': sum(r['cycles'] for r in inventories),
                             'ordinary_cycles': sum(r['cycles'] for r in executions),
                             'compile_seconds': sum(r['compile_seconds'] for r in inventories) + sum(r['seconds'] for r in summary['compilations']),
                             'simulation_seconds': sum(r['simulation_seconds'] for r in inventories) + sum(r['seconds'] for r in executions),
                             'sum_screen_seconds': sum(r['elapsed_seconds'] for r in decisions),
                             'model_calls': 0, 'api_tokens': 0, 'api_cost_usd': 0,
                             'scope': 'Saved DUT runs including failed screen; test fixture tool calls only in test logs. Timings overlap by stage and are not end-to-end wall time.'},
              'formal_jobs': formal, 'versions': versions, 'tests': tests,
              'ordinary_gate_pass': False, 'checker_commissioned': False, 'B_allowed': False, 'C_allowed': False,
              'limits': 'Two-state conditional semantic proof, not whole-IP correctness. Negative ordinary exclusion uses transport controls, no golden-output checker. Raw source counts remain separate; unresolved points retained.'}
    (BASE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'provenance_hash_checks', 'accounting', 'ordinary_coverage_union', 'versions')}, indent=2))


if __name__ == '__main__':
    audit()
