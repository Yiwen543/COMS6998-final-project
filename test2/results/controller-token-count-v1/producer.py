#!/usr/bin/env python3
"""Registered controller monitor loop/count gate; hidden scoring is separate."""
import argparse
import json
import os
from pathlib import Path
import random
import time
import uuid
from common import ROOT, BASE, dump, sha
from controller_monitor_live import HEADER, SCHEMA, compile_monitor, build_replay, replay
from controller_release_live import ARMS, freeze_round, release
from pilot_model import OpenAIModel, ModelResponseError

TASK = BASE / 'tasks/axis_length_fifo_v1'
REG = BASE / 'configs/controller_run_v1.json'
LIVE_FREEZE = BASE / 'configs/controller_live_freeze_v1.json'
SYSTEM = '''Write a passive SystemVerilog frame_task monitor using only this packet.
Return JSON with body and exactly six properties P0..P5, each with id and description.
The fixed module header is supplied. Max body16000UTF8bytes and private state8192bits.
Supported body: declarations, initial assignments, combinational logic and posedge clk processes.
No additional modules, hierarchy, files, system calls, delays, assumptions or direct assert/cover constructs.
Use active[j]/ok[j] for property checks; active=1,ok=0 is an alarm. Never drive an input.
Check sound specification obligations, reset timing, independent response channels and useful fault detection.
Internal RTL/e-graph terms are implementation facts, not expected answers or sequential correctness proofs.
The candidate cannot change fixed DUT observations or raw coverage. All six rounds run at the same caps.
You see only your own prior candidate and development feedback. No hidden outcomes or reference source are available.'''


def load(path):
    return json.loads(Path(path).read_text())


def model_config(reg):
    b = reg['candidate_model_budget']
    return dict(model=b['model'], reasoning_effort=b['reasoning_effort'], max_input_tokens=b['input_tokens'],
                max_output_tokens=b['output_tokens'], timeout_seconds=b['request_timeout_seconds'], max_retries=b['max_retries'])


def model(reg):
    key = ROOT / 'build/private/midterm-openai-key'
    if not key.is_file() or key.stat().st_mode & 0o077:
        raise RuntimeError('Missing staged OpenAI key or unsafe permissions')
    # Client retains the credential; never expose it to compiler/replay children.
    old = os.environ.get('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = key.read_text().strip()
    try:
        return OpenAIModel(model_config(reg), SCHEMA, 'controller_monitor')
    finally:
        if old is None:
            os.environ.pop('OPENAI_API_KEY', None)
        else:
            os.environ['OPENAI_API_KEY'] = old


def messages(arm, round_no, previous=None, feedback=None):
    # Literal public-only frozen packet; never recursive workspace access.
    data = load(TASK / 'qualification/prompt-audit-v2' / (arm+'.json'))
    data.update(module_header=HEADER, round=round_no, previous_candidate=previous, development_feedback=feedback)
    return [{'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': json.dumps(data, separators=(',', ':'), sort_keys=True)}]


def verify_task(reg):
    if sha(ROOT / reg['reference']['freeze_path']) != reg['reference']['freeze_sha256']:
        raise ValueError('Reference freeze changed')
    ref = load(ROOT / reg['reference']['freeze_path'])
    for name, h in ref['artifact_sha256'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Frozen task/reference changed: '+name)
    for name, h in reg['active_contract'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Active contract changed')


def live_gate():
    reg = load(REG)
    f = load(LIVE_FREEZE)
    if not f['candidate_live_allowed'] or not all(f['gates'].values()):
        raise ValueError('Live gates not complete')
    for name, h in f['files'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Live frozen artifact changed: '+name)
    verify_task(reg)
    return f


def plumbing(round_no):
    active = "6'b000000" if round_no == 2 else "6'b111111"
    ok = "6'b000000" if round_no == 1 else "6'b111111"
    return {'body': f'assign active={active}; assign ok={ok};',
            'properties': [{'id': f'P{i}', 'description': 'Arm-blind offline plumbing only'} for i in range(6)]}


def develop(candidate, directory, cache):
    started = time.perf_counter()
    calls, cycles, seconds, replay_seconds = 0, 0, 0.0, 0.0
    try:
        calls += 1
        c = compile_monitor(candidate, directory / 'compiled')
        seconds += c['seconds']
        if c['status'] != 'complete':
            log = (directory / 'compiled/yosys.log').read_text()
            lines = [s for s in log.splitlines() if any(x in s.lower() for x in ('error', 'warning', 'syntax'))]
            feedback = dict(status='compile_error', log='\n'.join(lines).replace(str(directory), 'ROUND_DIR')[-6000:])
        else:
            calls += 1
            b = build_replay(directory / 'compiled')
            seconds += b['seconds']
            if b['status'] != 'complete':
                feedback = dict(status='compile_error', log='Replay compilation failed; raw log retained')
            else:
                feedback = {'status': 'compiled', 'development': {}}
                for name in ('basic', 'boundary_pressure', 'reset_reuse'):
                    rows = load(TASK / 'qualification/observations-v2/verilator' / name / 'rows.json')
                    result = replay(directory / 'compiled', rows, directory / name, cache)
                    cycles += result['cycles']
                    replay_seconds += result['execution']['seconds']
                    feedback['development'][name] = dict(complete=result['complete'], properties=[
                        dict(id=p['id'], checks=p['checks'], failure_count=len(p['failures']), first_failures=p['failures'][:8],
                             unknown_count=len(p['unknown']), first_unknown=p['unknown'][:8]) for p in result['properties']])
    except ValueError as error:
        feedback = dict(status='invalid_candidate', reason=str(error))
    except Exception as error:
        feedback = dict(status='infrastructure_error', error_type=type(error).__name__)
    cost = dict(compilation_tool_invocations=calls, compile_seconds=seconds, replay_seconds=replay_seconds, replayed_cycles=cycles,
                monitor_replays=len(feedback.get('development', {})), wall_seconds=time.perf_counter()-started)
    dump(directory / 'development-feedback.json', feedback)
    dump(directory / 'development-cost.json', cost)
    return feedback, cost


def append(path, data):
    with path.open('a') as f:
        f.write(json.dumps(data, separators=(',', ':'), sort_keys=True)+'\n')


def budget_count(out):
    reg = load(REG)
    verify_task(reg)
    out.mkdir(parents=True, exist_ok=False)
    client = model(reg)
    rng = random.Random(699855)
    body = "assign active=6'b111111;assign ok=6'b111111;"
    body += '/*'+''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(16000-len(body)-4))+'*/'
    previous = {'body': body, 'properties': [{'id': f'P{i}', 'description': ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(400))} for i in range(6)]}
    records = []
    for arm in ARMS:
        for kind, prompt in [('initial', messages(arm, 1)), ('maximum_history_probe', messages(arm, 6, previous, {'status': 'compile_error', 'log': 'x'*6000}))]:
            path = out / (arm+'-'+kind+'.json')
            dump(path, prompt)
            before = time.perf_counter()
            count = client.count_input_tokens(prompt)
            records.append(dict(arm=arm, kind=kind, input_tokens=count, within_cap=count<=64000,
                                seconds=time.perf_counter()-before, prompt_sha256=sha(path)))
            dump(out / 'partial.json', records)
    summary = dict(status='passed' if all(r['within_cap'] for r in records) else 'input_cap_exceeded',
                   counts=records, input_cap=64000, generation_requests=0, count_requests=4,
                   scope='Actual provider counts including structured response schema; history probe is a calibration, not a guarantee for arbitrary future text',
                   runner_sha256=sha(Path(__file__)), registration_sha256=sha(REG))
    dump(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


def execute(mode, out, replay_source=None):
    reg = load(REG)
    verify_task(reg)
    if mode == 'live':
        live_gate()
    out.mkdir(parents=True, exist_ok=False)
    client = model(reg) if mode == 'live' else None
    saved = {}
    if mode == 'replay':
        for line in (replay_source / 'calls.jsonl').read_text().splitlines():
            r = json.loads(line)
            if r.get('accepted_response'):
                saved[r['arm'], r['repetition'], r['round']] = r
    sessions = {(a, r): dict(id=str(uuid.uuid4()), previous=None, feedback=None) for a in ARMS for r in (1, 2, 3)}
    dump(out / 'run.json', dict(mode=mode, registration_sha256=sha(REG), runner_sha256=sha(Path(__file__)),
         session_ids={f'{a}/{r}': s['id'] for (a, r), s in sessions.items()}, provider_tools=[],
         provider_history='stateless explicit own last candidate/development feedback only', replay_origin=str(replay_source) if replay_source else None))
    snapshots, costs = [], []
    (out / 'calls.jsonl').touch()
    started = time.perf_counter()
    for number in range(1, 7):
        for rep in (1, 2, 3):
            for arm in (ARMS if (number+rep)%2 == 0 else tuple(reversed(ARMS))):
                if mode == 'live':
                    live_gate()
                session = sessions[arm, rep]
                context = dict(mode=mode, arm=arm, repetition=rep, round=number, session_id=session['id'])
                d = out / arm / f'rep{rep}' / f'round{number}'
                d.mkdir(parents=True)
                prompt = messages(arm, number, session['previous'], session['feedback'])
                dump(d / 'prompt.json', prompt)
                parsed = None
                for attempt in range(2 if mode == 'live' else 1):
                    record = dict(context, attempt=attempt+1, prompt_sha256=sha(d / 'prompt.json'),
                                  generation_request_issued=False, count_request_issued=False, accepted_response=False)
                    try:
                        if mode == 'live':
                            record['count_request_issued'] = True
                            record['input_token_count'] = client.count_input_tokens(prompt)
                            if record['input_token_count'] > 64000:
                                record['status'] = 'input_cap_exceeded_no_generation'
                                append(out / 'calls.jsonl', record)
                                break
                            record['generation_request_issued'] = True
                            record.update(client.generate(prompt, context))
                            parsed = record['parsed']
                        elif mode == 'mock':
                            parsed = plumbing(number)
                            record.update(parsed=parsed, requested_model='mock-plumbing', returned_model='mock-plumbing', usage=None, status='completed')
                        else:
                            old = saved.get((arm, rep, number))
                            if old is None:
                                record['status'] = 'replayed_unresolved'
                            else:
                                if old['prompt_sha256'] != sha(d / 'prompt.json'):
                                    raise ValueError('Replay prompt mismatch')
                                parsed = old['parsed']
                                record.update(parsed=parsed, usage=None, original_usage=old.get('usage'), status='completed')
                        record['accepted_response'] = parsed is not None
                    except ModelResponseError as error:
                        record.update(error.record, status='model_response_error', error_type=error.reason)
                    except Exception as error:
                        if mode == 'replay':
                            raise
                        record.update(status='request_or_infrastructure_error', error_type=type(error).__name__)
                    append(out / 'calls.jsonl', record)
                    if parsed is not None or mode != 'live':
                        break
                dump(d / 'response.json', parsed)
                if parsed is None:
                    feedback, cost = dict(status='generation_unresolved'), dict(compilation_tool_invocations=0, monitor_replays=0, replayed_cycles=0, wall_seconds=0)
                    dump(d / 'development-feedback.json', feedback)
                    dump(d / 'development-cost.json', cost)
                else:
                    session['previous'] = parsed
                    feedback, cost = develop(parsed, d, out / 'development-row-cache')
                session['feedback'] = feedback
                costs.append(cost)
                snapshots.append(freeze_round(out, d, context, feedback['status']))
                print(f'{mode} {arm} rep{rep} round{number}: {feedback["status"]}', flush=True)
    release(out, snapshots, mode)
    records = [json.loads(s) for s in (out / 'calls.jsonl').read_text().splitlines()]
    summary = dict(mode=mode, rounds=36, frozen_rounds=len(snapshots), wall_seconds=time.perf_counter()-started,
                   generation_requests=sum(r['generation_request_issued'] for r in records), count_requests=sum(r['count_request_issued'] for r in records),
                   compile_invocations=sum(c['compilation_tool_invocations'] for c in costs), monitor_replays=sum(c['monitor_replays'] for c in costs),
                   replayed_cycles=sum(c['replayed_cycles'] for c in costs), new_DUT_simulations=0, hidden_scoring_started=False)
    dump(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['mock', 'replay', 'live', 'count'], required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--replay-source', type=Path)
    a = p.parse_args()
    if a.mode == 'count':
        budget_count(a.output.resolve())
    else:
        execute(a.mode, a.output.resolve(), a.replay_source.resolve() if a.replay_source else None)
