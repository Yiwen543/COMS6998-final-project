#!/usr/bin/env python3
"""Guarded B-only SPI development runner. Refuses live calls on failed preflight."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from coverage import load
from pilot_model import OpenAIModel, ModelResponseError, usage_record
from preflight_spi_host import identity
from run_midterm_b_development import KEY_FILE, append, raw_feedback
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import SOURCE, SOURCES, DRIVER, FOLDER, compile_driver, simulate, verify_source
from spi_host_fixture import FIELDS, action, schema, validate_actions

CONFIG = ROOT/'configs/spi_host_b_development.json'
SCREEN = ROOT/'results/spi_host_preflight_20261104/screen.json'
INSTRUCTIONS = ('Generate only JSON cycle actions for the fixed SPI controller. Change stimulus only. '
    'Maximize uncovered original DUT line and branch counters under the cycle budget. '
    'Follow the public interface contract. Checker failures are evidence, not a reason to weaken checks. '
    'The entire cumulative sequence is replayed from the fixed reset seed. No implicit drain is inserted.')


def require_gate(screen, config):
    gate = config['static_acceptance']
    if not screen['qualified_for_model_trial'] or screen['qualified_source_groups'] < gate['min_source_groups'] or \
            screen['qualified_rewrite_groups'] < gate['min_rewrite_groups']:
        raise ValueError('Static gate failed: no live B or A/B/C/P calls authorized by this configuration')
    for name, digest in screen['hashes'].items():
        if sha(ROOT/name) != digest:
            raise ValueError('Preflight evidence stale: '+name)
    if screen['config_sha256'] != sha(CONFIG):
        raise ValueError('Configuration differs from screened configuration')


def messages(seed, generated, prior, log, points, rnd, limit):
    common = {'specification': (FOLDER/'contract.md').read_text(),
        'rtl': {str(p.relative_to(ROOT)): p.read_text() for p in SOURCES},
        'cycle_field_order': list(FIELDS), 'common_seed': [[a[k] for k in FIELDS] for a in seed],
        'previous_generated_cycles': [[a[k] for k in FIELDS] for a in generated],
        'round': rnd, 'max_new_cycles': limit,
        'checker': prior['checker'],
        'execution_log': [line for line in log.splitlines() if line.startswith('TRACE ')][-20:],
        'raw_uncovered_dut_coverage': raw_feedback(points, [SOURCE])}
    return [{'role': 'system', 'content': INSTRUCTIONS},
            {'role': 'user', 'content': json.dumps(common, separators=(',', ':'))}]


def group_status(points, screen):
    index = {identity(p): p['hits'] for p in points}
    result = []
    for g in screen['groups']:
        if not g['qualified_source_group']:
            continue
        members = [m for m in g['members'] if m['id'] in g['qualified_member_ids']]
        hits = [index[identity(m['mapping']['point'])] for m in members]
        result.append({'eclass': g['eclass'], 'source_lines': [m['line'] for m in members],
                       'raw_source_hits': hits, 'all_hit': all(h > 0 for h in hits)})
    return result


def evaluate(rows, config, live):
    detail = []
    for rep in range(1, config['repetitions']+1):
        rounds = [r for r in rows if r['repetition'] == rep]
        complete = len(rounds) == config['rounds'] and all(r['status'] == 'simulated' for r in rounds)
        valid = complete and all(not r['checker']['assumption_violations'] for r in rounds)
        first = sum(not g['all_hit'] for g in rounds[0]['groups']) if rounds else None
        last = sum(not g['all_hit'] for g in rounds[-1]['groups']) if rounds else None
        detail.append({'repetition': rep, 'complete_and_valid': valid,
            'groups_unhit_round_one': first, 'groups_unhit_final': last,
            'later_progress': valid and last < first})
    threshold = config['acceptance']
    passed = (live and all(d['complete_and_valid'] for d in detail) and
        sum(d['complete_and_valid'] and d['groups_unhit_round_one'] >= 2 for d in detail) >=
            threshold['min_repetitions_with_two_groups_unhit_after_round_one'] and
        sum(d['later_progress'] for d in detail) >= threshold['min_repetitions_with_later_group_progress'])
    return {'passed': passed, 'details': detail, 'mock_can_qualify': False}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--mode', choices=('mock', 'live'), required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--screen', type=Path, default=SCREEN,
                     help='Explicit separately versioned static screen; old default stays frozen')
    args = cli.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    config = json.loads(CONFIG.read_text())
    screen_path = args.screen.resolve()
    screen = json.loads(screen_path.read_text())
    # Preserve the exact selection evidence even if a later preflight is rerun.
    (out/'input-config.json').write_bytes(CONFIG.read_bytes())
    (out/'input-screen.json').write_bytes(screen_path.read_bytes())
    if args.mode == 'live':
        try:
            require_gate(screen, config)  # Before key read, model creation, or networking.
        except ValueError as error:
            (out/'blocked.json').write_text(json.dumps({'status': 'not_run', 'model_calls': 0,
                'reason': str(error), 'screen_sha256': sha(screen_path)}, indent=2)+'\n')
            raise SystemExit(str(error))
    else:
        config = {**config, 'repetitions': 1, 'rounds': 2, 'max_new_cycles': 8}
    verify_source()
    start = time.perf_counter()
    metadata = {'mode': args.mode, 'config': config, 'static_gate_passed': screen['qualified_for_model_trial'],
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'hashes': {str(p.relative_to(ROOT)): sha(p) for p in [*SOURCES, DRIVER, FOLDER/'contract.md',
            ROOT/'scripts/spi_host_fixture.py', Path(__file__), CONFIG, screen_path]},
        'api_model_calls': 0, 'count_requests': 0, 'compilations': 0,
        'scope': 'B development only; mock never provides acceptance evidence'}
    (out/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    model = None
    consumed_key = False
    rows = []
    try:
        if args.mode == 'live':
            if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
                raise RuntimeError('Missing private staged key or unsafe permissions')
            os.environ['OPENAI_API_KEY'] = KEY_FILE.read_text().strip()
            consumed_key = True
            model = OpenAIModel(config, schema=schema(config['max_new_cycles']), schema_name='spi_host_actions')
        shared = out/'shared'
        shared.mkdir()
        metadata['compilations'] += 1
        binary, command, seconds = compile_driver(shared)
        metadata.update(compile_seconds=seconds, compile_command=list(map(str, command)))
        seed = json.loads((FOLDER/'seed.json').read_text())['actions']
        for rep in range(1, config['repetitions']+1):
            folder = out/f'rep{rep}'
            folder.mkdir()
            prior = simulate(binary, seed, folder, 'seed')
            points = load(folder/'seed.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
            denominator = {identity(p) for p in points}
            log = folder/'seed.sim.log'
            history, calls = [], []
            cycles, simulations = len(seed), 1
            requested_cycles = len(seed)
            sim_seconds = prior['simulation_seconds']
            for rnd in range(1, config['rounds']+1):
                rendered = messages(seed, history, prior, log.read_text(), points, rnd, config['max_new_cycles'])
                accepted = None
                for attempt in range(1, config['max_retries']+2):
                    path = folder/f'prompt-{rnd}-{attempt}.json'
                    path.write_text(json.dumps(rendered, indent=2)+'\n')
                    record = {'repetition': rep, 'round': rnd, 'attempt': attempt, 'mode': args.mode,
                        'prompt': str(path.relative_to(out)), 'accepted': False,
                        'requested_model': config['model'] if model else 'mock',
                        'usage': usage_record(None), 'settings': config}
                    started = time.perf_counter()
                    try:
                        if model:
                            count_start = time.perf_counter()
                            metadata['count_requests'] += 1
                            try:
                                count = model.count_input_tokens(rendered)
                                append(out/'counts.jsonl', {'repetition': rep, 'round': rnd, 'attempt': attempt,
                                    'input_tokens': count, 'seconds': time.perf_counter()-count_start})
                            except Exception as error:
                                append(out/'counts.jsonl', {'repetition': rep, 'round': rnd, 'attempt': attempt,
                                    'error_type': type(error).__name__, 'seconds': time.perf_counter()-count_start})
                                raise
                            if count > config['max_input_tokens']:
                                raise ValueError('Input token cap exceeded')
                            metadata['api_model_calls'] += 1
                            record.update(model.generate(rendered, {}))
                        else:
                            data = {'actions': [action() for _ in range(config['max_new_cycles'])]}
                            record.update(returned_model='mock', parsed=data, output_text=json.dumps(data))
                        accepted = validate_actions(record['parsed'], config['max_new_cycles'])
                        record.update(accepted=True, actions=accepted)
                    except ModelResponseError as error:
                        record.update(error.record, validation_failure=error.reason)
                    except Exception as error:
                        record.update(error_type=type(error).__name__, http_status=getattr(error, 'status_code', None))
                    finally:
                        record['request_wall_seconds'] = time.perf_counter()-started
                        calls.append(record)
                        append(out/'calls.jsonl', record)
                    if accepted is not None:
                        break
                    rendered = [*rendered, {'role': 'user', 'content': 'The previous request failed validation or execution. Return only valid schema-conforming actions.'}]
                status = 'no_valid_actions'
                if accepted is not None:
                    history.extend(accepted)
                    (folder/f'round{rnd}.actions.json').write_text(json.dumps({'actions': seed+history}, indent=2)+'\n')
                    requested_cycles += len(seed)+len(history)
                    simulations += 1
                    accounted = False
                    try:
                        prior = simulate(binary, seed+history, folder, f'round{rnd}')
                        cycles += len(seed)+len(history)
                        accounted = True
                        sim_seconds += prior['simulation_seconds']
                        points = load(folder/f'round{rnd}.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
                        if {identity(p) for p in points} != denominator:
                            raise AssertionError('DUT counter denominator changed')
                        log = folder/f'round{rnd}.sim.log'
                        status = 'simulated'
                    except Exception as error:
                        partial = folder/f'round{rnd}.sim.log'
                        observed = sum(line.startswith('TRACE ') for line in partial.read_text().splitlines()) if partial.exists() else 0
                        # If simulate returned, cycles were already counted even if
                        # a subsequent denominator check failed.
                        if not accounted:
                            cycles += observed
                        append(out/'failures.jsonl', {'repetition': rep, 'round': rnd, 'stage': 'simulation', 'error_type': type(error).__name__})
                        status = 'simulation_failed'
                tokens = sum((c['usage']['input_tokens'] or 0)+(c['usage']['output_tokens'] or 0) for c in calls)
                row = {'repetition': rep, 'round': rnd, 'status': status, 'mode': args.mode,
                    'groups': group_status(points, screen), 'coverage': prior['coverage'], 'checker': prior['checker'],
                    'api_tokens': tokens if model else None, 'calls': len(calls),
                    'unknown_usage_calls': sum(c['usage']['input_tokens'] is None for c in calls),
                    'failed_attempts': sum(not c['accepted'] for c in calls),
                    'executed_cycles_including_replays': cycles, 'simulator_executions': simulations,
                    'requested_cycles_including_replays': requested_cycles,
                    'simulation_seconds': sim_seconds, 'elapsed_run_seconds': time.perf_counter()-start}
                rows.append(row)
                append(out/'rounds.jsonl', row)
                print(f"SPI B {args.mode} rep {rep} round {rnd}: {status}, "
                      f"unhit groups={sum(not g['all_hit'] for g in row['groups'])}, "
                      f"input violations={len(row['checker']['assumption_violations'])}, "
                      f"DUT symptoms={len(row['checker']['failures'])}", flush=True)
                if status == 'simulation_failed':
                    break
        (out/'summary.json').write_text(json.dumps({'mode': args.mode, 'gate': evaluate(rows, config, bool(model)),
            'rows': rows, 'elapsed_seconds': time.perf_counter()-start}, indent=2)+'\n')
    finally:
        (out/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
        if consumed_key:
            os.environ.pop('OPENAI_API_KEY', None)
            KEY_FILE.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
