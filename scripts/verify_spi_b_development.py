#!/usr/bin/env python3
"""Recompute saved SPI B evidence; no simulation, solver, or model invocation."""
import argparse
import hashlib
import json
from pathlib import Path

from coverage import load, summary
from preflight_spi_host import identity
from run_midterm_fixed import ROOT, sha
from run_spi_host_b_development import group_status, messages, require_gate
from run_spi_host_fixed import FOLDER, SOURCE, verify_source
from spi_host_fixture import check, validate_actions


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def verify(run):
    meta = json.loads((run/'metadata.json').read_text())
    screen = json.loads((run/'input-screen.json').read_text())
    config = json.loads((run/'input-config.json').read_text())
    require_gate(screen, config)
    verify_source()
    for name, digest in meta['hashes'].items():
        assert sha(ROOT/name) == digest, name
    assert meta['config'] == config
    calls, rows = jsonl(run/'calls.jsonl'), jsonl(run/'rounds.jsonl')
    counts = jsonl(run/'counts.jsonl')
    # This audit is for this completed, all-success live run. Failed runs must
    # retain their failures and require an explicitly different accounting path.
    assert len(calls) == len(rows) == config['repetitions']*config['rounds']
    assert all(c['accepted'] and c['attempt'] == 1 for c in calls)
    assert all(c['requested_model'] == c['returned_model'] == config['model'] for c in calls)
    assert len({c['response_id'] for c in calls}) == len(calls)
    assert all(c['input_tokens'] <= config['max_input_tokens'] for c in counts)
    assert all(c['usage']['output_tokens'] <= config['max_output_tokens'] for c in calls)
    seed = json.loads((FOLDER/'seed.json').read_text())['actions']
    total_cycles = simulations = checked_prompts = 0
    all_files = []
    denominator = None
    for rep in range(1, config['repetitions']+1):
        folder = run/f'rep{rep}'
        actions = list(seed)
        rep_cycles = rep_tokens = 0
        for rnd in range(config['rounds']+1):
            label = 'seed' if rnd == 0 else f'round{rnd}'
            if rnd:
                call = next(c for c in calls if (c['repetition'], c['round']) == (rep, rnd))
                prompt = json.loads((run/call['prompt']).read_text())
                expected = messages(seed, actions[len(seed):], previous, previous_log, points,
                                    rnd, config['max_new_cycles'])
                assert prompt == expected, f'Prompt differs from B-only evidence: {rep}/{rnd}'
                additions = validate_actions(call['parsed'], config['max_new_cycles'])
                assert additions == call['actions']
                actions.extend(additions)
                assert json.loads((folder/f'{label}.actions.json').read_text())['actions'] == actions
                rep_tokens += call['usage']['input_tokens']+call['usage']['output_tokens']
                checked_prompts += 1
            validate_actions({'actions': actions}, len(actions), require_initial_reset=True)
            log = (folder/f'{label}.sim.log').read_text()
            assert f'DRIVER_OK steps={len(actions)}' in log
            assert sum(line.startswith('TRACE ') for line in log.splitlines()) == len(actions)
            points = load(folder/f'{label}.dat', str(SOURCE.relative_to(ROOT)), include_descendants=True)
            ids = {identity(p) for p in points}
            assert len(ids) == len(points) == 1299
            if denominator is None:
                denominator = ids
            assert ids == denominator
            saved = json.loads((folder/f'{label}.json').read_text())
            assert saved['steps'] == len(actions)
            assert saved['checker'] == check(actions, log)
            assert saved['coverage'] == summary(points)
            rep_cycles += len(actions)
            simulations += 1
            total_cycles += len(actions)
            if rnd:
                row = next(r for r in rows if (r['repetition'], r['round']) == (rep, rnd))
                assert row['status'] == 'simulated'
                assert row['checker'] == saved['checker']
                assert row['coverage'] == saved['coverage']
                assert row['groups'] == group_status(points, screen)
                assert row['executed_cycles_including_replays'] == rep_cycles
                assert row['simulator_executions'] == rnd+1
                assert row['api_tokens'] == rep_tokens
            previous, previous_log = saved, log
            all_files.extend(folder/f'{label}{ext}' for ext in ('.dat', '.json', '.sim.log'))
    all_files.extend(run/f for f in ('input-screen.json', 'input-config.json', 'metadata.json',
                                    'calls.jsonl', 'counts.jsonl', 'rounds.jsonl', 'summary.json'))
    result = {'status': 'pass', 'mode': meta['mode'], 'hashes_checked': len(meta['hashes'])+len(screen['hashes']),
        'prompts_reconstructed_from_own_raw_B_history': checked_prompts,
        'raw_counter_denominator': len(denominator), 'raw_simulations_rechecked': simulations,
        'actual_trace_cycles': total_cycles,
        'new_model_calls': 0, 'new_simulations': 0,
        'scope': 'Saved-log and counter recomputation, not independent checker correctness proof.',
        'evidence_sha256': {str(p.relative_to(ROOT)): sha(p) for p in all_files},
        'verification_script_sha256': sha(Path(__file__))}
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--run', type=Path, required=True)
    args = cli.parse_args()
    run = args.run.resolve()
    result = verify(run)
    (run/'recheck.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'evidence_sha256'}, indent=2))


if __name__ == '__main__':
    main()
