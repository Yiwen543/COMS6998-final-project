#!/usr/bin/env python3
"""A bounded stimulus-only agent on the pinned arbiter. No remote API in dry-run."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from agent_core import (OpenAIProvider, dump, feedback, output_json,
                        request_body, usage_counts, validate_batch)
from coverage import load, summary
from predicates import ROOT, DUT, extract
from run_step1 import result, run
from eda_build import build_verilator

STARTER = [
    {'reset': 1, 'req': 0, 'priority_override': 0},
    {'reset': 0, 'req': 0, 'priority_override': 0},
    {'reset': 0, 'req': 1, 'priority_override': 0},
    {'reset': 0, 'req': 0, 'priority_override': 1}]


@dataclass
class Config:
    group: str = 'C'
    model: str = 'gpt-6.1-sol'
    effort: str = 'medium'
    max_rounds: int = 5
    batch_size: int = 16
    max_checked_cycles: int = 512
    max_output_tokens: int = 4096
    stop_after_tokens: int = 50000
    plateau_rounds: int = 2
    run_id: str = 'run-01'


def stamp():
    return datetime.now(timezone.utc).isoformat()


def point_id(p):
    return tuple(p[k] for k in ('source', 'line', 'column', 'type', 'outcome'))


def hit_branches(points, kind='branch'):
    return {point_id(p) for p in points if p['type'] == kind and p['hits'] > 0}


def common_context(current, vectors, remaining, last_error):
    return {
        'simulation_protocol': 'Drive vectors on falling edges; check after the next rising edge settles.',
        'specification': (ROOT / 'examples/arbiter/docs/specification.md').read_text(),
        'rtl': DUT.read_text(),
        'starter_vectors_replayed_each_run': STARTER,
        'previous_submitted_vectors_replayed_each_run': vectors,
        'last_checker_result': current['checker'],
        'last_simulation_log': current['log'][:4000],
        'next_batch_limit': remaining,
        'last_response_error': last_error}


class ArbiterSimulator:
    """All arms execute the same immutable TB and DUT in fresh simulator processes."""
    name = 'verilator'

    def __init__(self, targets):
        self.targets = targets

    def prepare(self, out, group):
        env = dict(os.environ, CARGO_HOME=str(ROOT / '.cache/cargo'))
        self.graph = None
        costs = {}
        if group == 'C':
            elapsed, _ = run(['cargo', 'build', '--locked', '--offline',
                             '--manifest-path', 'egraph/Cargo.toml'],
                            out / 'egg-build.log', env=env)
            costs['egg_build_seconds'] = elapsed
            start = time.perf_counter()
            proc = subprocess.run(
                [str(ROOT / 'egraph/target/debug/rtl-predicate-egraph')],
                input=json.dumps(self.targets), text=True, capture_output=True,
                check=True, timeout=15, cwd=ROOT)
            self.graph = json.loads(proc.stdout)
            dump(out / 'egraph.json', self.graph)
            costs['semantic_preprocessing_seconds'] = time.perf_counter() - start
        self.binary, elapsed = build_verilator(ROOT, out, run)
        costs['simulator_build_seconds'] = elapsed
        return costs

    def simulate(self, vectors, folder):
        folder.mkdir(parents=True, exist_ok=True)
        counter_file = folder / 'coverage.dat'
        command = [self.binary, '+COLLECT',
                   f'+verilator+coverage+file+{counter_file}']
        if vectors:
            vf = folder / 'vectors.txt'
            vf.write_text(''.join(f"{v['reset']} {v['req']:02x} {v['priority_override']:02x}\n"
                                  for v in vectors))
            command += ['+MODE=1', f'+VECTORS={os.path.relpath(vf, ROOT)}']
        else:
            command += ['+MODE=0']
        seconds, log = run(command, folder / 'simulation.log')
        return {'checker': result(log), 'points': load(counter_file),
                'log': log, 'simulation_seconds': seconds}


def experiment(config, simulator, provider, out):
    """Provider and simulator injection permits offline controller tests."""
    started = time.perf_counter()
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'summary.json').exists():
        raise ValueError('Output already contains a run; choose a new output directory.')
    targets = simulator.targets
    starter = getattr(simulator, 'starter_vectors', STARTER)
    input_fields = getattr(simulator, 'input_fields', {'reset': 1, 'req': 255, 'priority_override': 255})
    coverage_kind = getattr(simulator, 'coverage_kind', 'branch')
    dut_path = getattr(simulator, 'dut_path', DUT)
    tb_path = getattr(simulator, 'tb_path', ROOT / 'examples/arbiter/verif/tb_fixed_priority_arbiter.sv')
    record = {
        'config': asdict(config), 'started_at': stamp(),
        'simulator': simulator.name, 'live_api': provider.is_live,
        'dut_sha256': hashlib.sha256(dut_path.read_bytes()).hexdigest(),
        'tb_sha256': hashlib.sha256(tb_path.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(getattr(simulator, 'checker_path', tb_path).read_bytes()).hexdigest(),
        'coverage_objective': coverage_kind, 'module': getattr(simulator, 'module_name', 'arbiter'),
        'rounds': [], 'api_attempts': 0, 'simulator_executions': 0,
        'total_checked_cycles': 0, 'usage_complete': True,
        'measured_usage': {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0},
        'stop_reason': 'not_started'}
    try:
        record['preparation'] = simulator.prepare(out, config.group)
        current = simulator.simulate([], out / 'initial')
        record['initial'] = {'checker': current['checker'], 'coverage': summary(current['points'])}
        record['final'] = record['initial']
        record['new_branch_points'] = 0
        record['new_coverage_points'] = 0
        record['simulator_executions'] = 1
        record['total_checked_cycles'] = current['checker']['checks']
        initial_hits = hit_branches(current['points'], coverage_kind)
        covered = set(initial_hits)
        universe = {point_id(p) for p in current['points']}
        vectors = []
        last_error = None
        plateau = 0
        record['stop_reason'] = 'round_budget'
        for index in range(1, config.max_rounds + 1):
            # Fresh runs replay the entire accumulated suite. Charge that replay.
            allowed = min(config.batch_size,
                          config.max_checked_cycles - record['total_checked_cycles'] - len(starter) - len(vectors))
            if allowed < 1:
                record['stop_reason'] = 'cycle_budget'
                break
            if record['measured_usage']['total_tokens'] >= config.stop_after_tokens:
                record['stop_reason'] = 'observed_token_threshold'
                break
            folder = out / f'round-{index:02d}'
            folder.mkdir()
            context_builder = getattr(simulator, 'context', common_context)
            context = context_builder(current, vectors, allowed, last_error)
            context.update(feedback(config.group, targets, simulator.graph, current['points']))
            body = request_body(config, context, targets, allowed, input_fields)
            dump(folder / 'request.json', body)
            # Hash the actual model payload; bytes are diagnostics, not tokenizer counts.
            request_hash = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            row = {'round': index, 'started_at': stamp(), 'status': 'requesting',
                   'request_sha256': request_hash}
            record['rounds'].append(row)
            record['api_attempts'] += 1
            t = time.perf_counter()
            try:
                response = provider.generate(body)
            except Exception:
                record['usage_complete'] = False
                row['status'] = 'api_error'
                raise
            row['api_seconds'] = time.perf_counter() - t
            dump(folder / 'response.json', response)
            row['response_id'] = response.get('id')
            row['returned_model'] = response.get('model')
            row['usage'] = usage_counts(response)
            if row['usage'] is None:
                record['usage_complete'] = False
            else:
                for key in record['measured_usage']:
                    record['measured_usage'][key] += row['usage'][key]
            # Invalid, incomplete and refused responses still consume a model call
            # and their returned usage is retained. No unrecorded retries.
            try:
                parsed = output_json(response)
                proposed = validate_batch(parsed, targets, allowed, input_fields)
            except (ValueError, TypeError, KeyError) as error:
                last_error = str(error)
                row.update(status='invalid_response', error=last_error)
                dump(folder / 'result.json', row)
                continue
            dump(folder / 'batch.json', parsed)
            input_key = lambda v: tuple(v[k] for k in input_fields)
            seen_inputs = {input_key(v) for v in starter + vectors}
            duplicate_inputs = 0
            for v in proposed:
                key = input_key(v)
                duplicate_inputs += key in seen_inputs
                seen_inputs.add(key)
            row['duplicate_input_count'] = duplicate_inputs
            row['repeated_target_count'] = len(proposed) - len({v['target_id'] for v in proposed})
            row['feedback_bytes'] = len(json.dumps(context, ensure_ascii=False).encode())
            vectors.extend(proposed)
            previous = covered
            row['status'] = 'simulating'
            current = simulator.simulate(vectors, folder)
            record['simulator_executions'] += 1
            record['total_checked_cycles'] += current['checker']['checks']
            if {point_id(p) for p in current['points']} != universe:
                raise ValueError('DUT coverage point identities changed during the run')
            covered = hit_branches(current['points'], coverage_kind)
            if not previous <= covered:
                raise ValueError('Replaying the accumulated suite lost earlier objective coverage')
            new_hits = covered - previous
            row.update(
                status='completed', batch_size=len(proposed), cumulative_vectors=len(vectors),
                new_coverage_points=len(new_hits),
                new_branch_points=len(new_hits) if coverage_kind == 'branch' else 0, checker=current['checker'],
                coverage=summary(current['points']),
                simulation_seconds=current['simulation_seconds'],
                cumulative_checked_cycles=record['total_checked_cycles'],
                cumulative_measured_tokens=record['measured_usage']['total_tokens'])
            dump(folder / 'coverage.json', current['points'])
            dump(folder / 'result.json', row)
            last_error = None
            plateau = 0 if new_hits else plateau + 1
            record['final'] = {'checker': current['checker'], 'coverage': summary(current['points'])}
            record['new_coverage_points'] = len(covered - initial_hits)
            record['new_branch_points'] = len(covered - initial_hits) if coverage_kind == 'branch' else 0
            if plateau >= config.plateau_rounds:
                record['stop_reason'] = 'coverage_plateau'
                break
    except Exception as error:
        record['stop_reason'] = 'error'
        record['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        total = record['measured_usage']['total_tokens']
        record['token_roi'] = (
            record.get('new_coverage_points', record.get('new_branch_points', 0)) * 1000 / total
            if record['usage_complete'] and provider.is_live and total else None)
        record['finished_at'] = stamp()
        record['wall_seconds_including_preparation'] = time.perf_counter() - started
        record['token_budget_note'] = (
            'stop_after_tokens is checked between calls, not a hard billing cap. '
            'max_output_tokens bounds each response including reasoning. '
            'Reasoning tokens are not added a second time.')
        dump(out / 'summary.json', record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', choices=list('ABCD'), default='C')
    parser.add_argument('--model', default='gpt-6.1-sol')
    parser.add_argument('--effort', choices=['low', 'medium', 'high'], default='medium')
    parser.add_argument('--max-rounds', type=int, default=5)
    parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--max-checked-cycles', type=int, default=512)
    parser.add_argument('--max-output-tokens', type=int, default=4096)
    parser.add_argument('--stop-after-tokens', type=int, default=50000)
    parser.add_argument('--plateau-rounds', type=int, default=2)
    parser.add_argument('--run-id', default='run-01', help='Repetition label, not an API random seed')
    parser.add_argument('--output', required=True)
    parser.add_argument('--dry-run', action='store_true',
                        help='Write a request from upstream saved fixtures; no API or EDA calls')
    args = parser.parse_args()
    config = Config(**{key: value for key, value in vars(args).items()
                       if key not in ('output', 'dry_run')})
    if any(value <= 0 for key, value in asdict(config).items() if type(value) is int):
        parser.error('All budgets and limits must be positive')
    if config.max_checked_cycles < 5:
        parser.error('Cycle budget must include the four starter cycles and one new vector')
    targets = extract()
    out = Path(args.output).resolve()
    if args.dry_run:
        if config.max_checked_cycles < 9:
            parser.error('Dry run needs at least 9 total checked cycles')
        if out.exists() and any(out.iterdir()):
            parser.error('Choose an empty dry-run output directory')
        out.mkdir(parents=True, exist_ok=True)
        saved = json.loads((ROOT / 'results/step1/initial-coverage.json').read_text())
        graph = json.loads((ROOT / 'results/step1/egraph.json').read_text()) if config.group == 'C' else None
        current = {'checker': {'checks': 4, 'functional_errors': 0, 'timing_errors': 0},
                   'log': 'Upstream initial fixture, not a new simulation.'}
        context = common_context(current, [], min(config.batch_size, config.max_checked_cycles - 8), None)
        # Baseline cost is four cycles; the next simulation replays another four.
        context.update(feedback(config.group, targets, graph, saved['points']))
        dump(out / 'request.json', request_body(config, context, targets, context['next_batch_limit']))
        dump(out / 'DRY_RUN.json', {'mode': 'request_preview_only', 'live_api': False,
              'new_simulator_executions': 0, 'input_tokens': None, 'output_tokens': None,
              'group': config.group, 'fixture_origin': 'SOURCE_SNAPSHOT.json'})
        print(f'Dry run only: {out / "request.json"}')
        return
    record = experiment(config, ArbiterSimulator(targets), OpenAIProvider(), out)
    print(json.dumps({key: record.get(key) for key in
          ('stop_reason', 'api_attempts', 'simulator_executions', 'total_checked_cycles',
           'new_branch_points', 'measured_usage', 'token_roi')}, indent=2))


if __name__ == '__main__':
    main()
