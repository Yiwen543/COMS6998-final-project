"""New live boundary using the reviewed reference checker; legacy freezes stay intact."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from run_midterm_fixed import ROOT, sha
from wbxbar_experiment import (schema, validate_generated, seed, action, group_status,
    messages, FIELDS, validate, parse, compile_driver, verify_freeze as verify_original)
from replay_wbxbar_cancel import verify_replay_freeze
from freeze_wbxbar_reference_replay import verify_registration as verify_replay_registration

BASE = ROOT / 'results/wbxbar_reference_bc_20261104'
REG = ROOT / 'configs/wbxbar_reference_bc_v1.json'
FREEZE = ROOT / 'configs/wbxbar_reference_bc_freeze_v1.json'
REPLAY_FREEZE = ROOT / 'configs/wbxbar_reference_replay_freeze_v1.json'
CANDIDATE = ROOT / 'results/wbxbar_reference_replay_20261104/frozen-checker'
FIXED_FIELDS = ('candidate', 'targets', 'development_budget', 'model_limits', 'arms',
                'session_policy', 'counter_identities', 'semantic_relations', 'rtl_prompt_view',
                'prompt_representation', 'feedback_selection')


def read(path):
    return json.loads(path.read_text())


def verify_registration():
    original = verify_original()
    replay, _ = verify_replay_freeze(REPLAY_FREEZE)
    verify_replay_registration(ROOT / replay['registration'])
    reg = read(REG)
    for name in FIXED_FIELDS:
        if reg[name] != original[name]:
            raise ValueError('Original registered setting changed: ' + name)
    if reg['checker_candidate'] != str(CANDIDATE.relative_to(ROOT)) or reg['checker_sha256'] != sha(CANDIDATE / 'checker.py'):
        raise ValueError('Reviewed checker boundary changed')
    for path, digest in reg['evidence_hashes'].items():
        if sha(ROOT / path) != digest:
            raise ValueError('Preserved evidence changed: ' + path)
    return reg


def verify_freeze(path=FREEZE):
    reg = verify_registration()
    frozen = read(path)
    if frozen['registration_sha256'] != sha(REG) or not frozen.get('offline_gate_pass'):
        raise ValueError('Registration or offline gate mismatch')
    for key in (*FIXED_FIELDS, 'checker_candidate', 'checker_sha256', 'id'):
        if frozen[key] != reg[key]:
            raise ValueError('Frozen setting differs: ' + key)
    for name, digest in frozen['hashes'].items():
        if sha(ROOT / name) != digest:
            raise ValueError('Frozen artifact changed: ' + name)
    if frozen['status'] == 'live_frozen':
        validation = read(ROOT / frozen['runner_validation'])
        if not validation.get('pass') or not all(frozen.get('live_' + arm + '_allowed') for arm in ('B', 'C')):
            raise ValueError('Live runner validation missing')
    elif frozen['status'] != 'offline_prepared' or any(frozen.get('live_' + arm + '_allowed') for arm in ('B', 'C')):
        raise ValueError('Offline configuration cannot permit live')
    return frozen


def check_trace(trace,out):
    auth=json.loads((CANDIDATE/'authorship.json').read_text())
    for name,h in auth['artifact_sha256'].items():
        if sha(CANDIDATE/name)!=h:raise ValueError('Checker changed')
    inp=out/'checker-input.json';res=out/'checker-output.json'
    inp.write_text(json.dumps({'batch':trace},separators=(',',':'))+'\n')
    command=[sys.executable,'-I',str(ROOT/'scripts/evaluate_spi_checker_candidate.py'),
        '--worker','--candidate',str(CANDIDATE),'--inputs',str(inp),'--output',str(res)]
    env={k:v for k,v in os.environ.items() if not any(s in k for s in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-check-') as cwd:
        p=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
    (out/'checker-worker.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('Checker process failed')
    d=json.loads(res.read_text())
    if d['errors'] or not all(t['pass'] for t in d['selftests']) or d['cases']['batch'].get('infrastructure_error'):
        raise RuntimeError('Checker infrastructure error')
    return d['cases']['batch']


def simulate(binary,actions,out,manifest,denominator):
    validate(actions);out.mkdir(parents=True,exist_ok=False)
    (out/'actions.json').write_text(json.dumps({'actions':actions},indent=2)+'\n')
    vec=out/'vectors.txt';vec.write_text(''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions))
    command=list(map(str,[binary,'+VECTORS='+str(vec),'+verilator+coverage+file+'+str(out/'coverage.dat')]))
    start=time.perf_counter()
    try:
        with (out/'simulation.log').open('w') as stream:
            p=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=30)
        if p.returncode:raise RuntimeError('Simulation failed; partial evidence retained')
    finally:
        log=(out/'simulation.log').read_text()
        execution={'command':command,'simulation_seconds':time.perf_counter()-start,
            'requested_cycles':len(actions),'executed_cycles':sum(l.startswith('PRE ') for l in log.splitlines()),
            'driver_complete':'DRIVER_OK steps='+str(len(actions)) in log}
        (out/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    if not execution['driver_complete']:raise ValueError('Incomplete driver')
    trace,transport=parse(log,actions,manifest['inputs'],manifest['outputs'])
    (out/'trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n')
    points=load_all(out/'coverage.dat',manifest['sources'])
    (out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
    if len(points)!=len(denominator) or {identity(p) for p in points}!=denominator:
        raise ValueError('DUT denominator changed')
    # Coverage has already been flushed before checking. Violations never abort measurement.
    checked=check_trace(trace,out)
    result={'coverage':summary(points),'checker':checked,'transport':transport,
        'delivery_complete':transport['delivery_complete'],
        'verification_complete':transport['delivery_complete'] and checked['verdict']=='scoped_pass',
        **execution}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result,points,trace

