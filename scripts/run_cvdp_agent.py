#!/usr/bin/env python3
"""Run the bounded stimulus-only agent on reviewed CVDP modules."""
import argparse
import json
import os
import subprocess
import time
from dataclasses import asdict
from pathlib import Path
from agent_core import OpenAIProvider, dump, feedback, request_body
from cvdp_modules import FIELDS, NAMES, initial, source, targets, verify_source
from cvdp_simulator import CVDPSimulator
from predicates import ROOT
from run_agent import Config, experiment
from run_cvdp_suite import validate_representatives
from run_step1 import run


class CVDPAgentSimulator:
    name = 'verilator-cvdp'

    def __init__(self, module):
        self.module_name = module
        self.targets = targets(module)
        self.input_fields = FIELDS[module]
        self.starter_vectors = initial(module)
        self.coverage_kind = 'line' if module == 'caesar_cipher' else 'branch'
        self.dut_path = ROOT / source(module)
        self.tb_path = ROOT / 'examples/cvdp' / module / 'verif/tb.sv'
        self.checker_path = ROOT / 'scripts/cvdp_modules.py'
        self.graph = None

    def prepare(self, out, group):
        costs = {}
        if group == 'C':
            env = dict(os.environ, CARGO_HOME=str(ROOT / '.cache/cargo'))
            elapsed, _ = run(['cargo', 'build', '--locked', '--offline',
                             '--manifest-path', 'egraph/Cargo.toml'], out / 'egg-build.log', env=env)
            costs['egg_build_seconds'] = elapsed
            start = time.perf_counter()
            proc = subprocess.run([str(ROOT / 'egraph/target/debug/rtl-predicate-egraph')],
                                  input=json.dumps(self.targets), text=True, capture_output=True,
                                  check=True, timeout=20)
            self.graph = json.loads(proc.stdout)
            validation = validate_representatives(self.module_name, self.targets, self.graph)
            dump(out / 'semantic-validation.json', validation)
            dump(out / 'egraph.json', self.graph)
            costs['semantic_preprocessing_seconds'] = time.perf_counter() - start
        self.sim = CVDPSimulator(self.module_name, out)
        costs['simulator_build_seconds'] = self.sim.build_seconds
        return costs

    def context(self, current, vectors, remaining, last_error):
        folder = ROOT / 'examples/cvdp' / self.module_name
        problem = json.loads((folder / 'upstream_problem.json').read_text())
        return {
            'simulation_protocol': ('Drive inputs with clock low; sample after the next rising edge settles.'
                if self.module_name == 'universal_shift_register' else
                'Combinational module without clock; drive inputs, wait 2 ns, sample output.'),
            'specification': problem['prompt'],
            'verification_scope': (folder / 'verification_scope.md').read_text(),
            'rtl': self.dut_path.read_text(),
            'predicate_atoms': self.targets[0]['atom_definitions'],
            'input_integer_bounds': self.input_fields,
            'starter_vectors_replayed_each_run': self.starter_vectors,
            'previous_submitted_vectors_replayed_each_run': vectors,
            'last_checker_result': current['checker'],
            'last_simulation_log': current['log'][:4000],
            'coverage_objective': self.coverage_kind,
            'next_batch_limit': remaining, 'last_response_error': last_error}

    def simulate(self, vectors, folder):
        # All repeats run exactly the same immutable checker and starter prefix.
        result = self.sim.simulate(self.starter_vectors + vectors, folder)
        result['log'] = (folder / 'simulation.log').read_text()
        return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--module', required=True, choices=NAMES)
    p.add_argument('--group', choices=list('ABCD'), default='C')
    p.add_argument('--model', default='gpt-6.1-sol')
    p.add_argument('--effort', choices=['low', 'medium', 'high'], default='medium')
    p.add_argument('--max-rounds', type=int, default=5)
    p.add_argument('--batch-size', type=int, default=16)
    p.add_argument('--max-checked-cycles', type=int, default=512)
    p.add_argument('--max-output-tokens', type=int, default=4096)
    p.add_argument('--stop-after-tokens', type=int, default=50000)
    p.add_argument('--plateau-rounds', type=int, default=2)
    p.add_argument('--run-id', default='run-01')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--fixture-root', type=Path, default=ROOT / 'results/cvdp-suite-20261017')
    a = p.parse_args()
    config = Config(**{k: v for k, v in vars(a).items()
                       if k not in ('module', 'output', 'dry_run', 'fixture_root')})
    if any(v <= 0 for v in asdict(config).values() if type(v) is int):
        p.error('All budgets must be positive')
    sim = CVDPAgentSimulator(a.module)
    if config.max_checked_cycles < 2 * len(sim.starter_vectors) + 1:
        p.error('Cycle budget must include initial suite, replay, and one new vector')
    out = a.output.resolve()
    if a.dry_run:
        if out.exists() and any(out.iterdir()):
            p.error('Choose an empty preview output directory')
        fixture = a.fixture_root / a.module
        provenance = verify_source(a.module)
        if json.loads((fixture / 'summary.json').read_text())['provenance'] != provenance:
            p.error('Fixture/source provenance mismatch; regenerate EDA fixtures')
        from hashlib import sha256
        manifest = json.loads((fixture / 'build-inputs.json').read_text())
        for path in (sim.dut_path, sim.tb_path):
            if manifest['sources'][str(path.relative_to(ROOT))] != sha256(path.read_bytes()).hexdigest():
                p.error('Fixture DUT/TB changed; regenerate EDA fixtures')
        current = json.loads((fixture / 'initial/result.json').read_text())
        current['log'] = 'Saved EDA fixture; no new simulation in this preview.'
        graph = json.loads((fixture / 'egraph.json').read_text()) if a.group == 'C' else None
        allowed = min(config.batch_size, config.max_checked_cycles - 2 * len(sim.starter_vectors))
        context = sim.context(current, [], allowed, None)
        context.update(feedback(a.group, sim.targets, graph, current['points']))
        out.mkdir(parents=True, exist_ok=True)
        dump(out / 'request.json', request_body(config, context, sim.targets, allowed, sim.input_fields))
        dump(out / 'DRY_RUN.json', {'module': a.module, 'live_api': False,
                                   'mode': 'saved-fixture-preview', 'new_simulator_executions': 0,
                                   'fixture': str(fixture), 'coverage_objective': sim.coverage_kind})
        print(out / 'request.json')
    else:
        provider = OpenAIProvider()
        record = experiment(config, sim, provider, out)
        print(json.dumps({k: record.get(k) for k in
                          ('module', 'stop_reason', 'coverage_objective', 'new_coverage_points',
                           'measured_usage', 'token_roi')}, indent=2))

if __name__ == '__main__':
    main()
