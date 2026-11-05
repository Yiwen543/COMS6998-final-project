"""Fixed experimental boundary. No expected-output logic; Claude owns checker."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from coverage import summary
from inventory_natural_coverage import load_all
from probe_spi_core_events import DRIVER, identity
from real_parent_screen import configuration, verify
from run_midterm_fixed import ROOT, invoke, sha
from spi_core_interface import FIELDS, parse, seed, schema, validate

BASE = ROOT/'results/real_parent_screen_20261104'
CANDIDATE = BASE/'claude-checker-v4/candidate'
CONTRACT = ROOT/'examples/spi_core_integration/docs/experimental_contract.md'
FREEZE = ROOT/'configs/spi_core_b_development.json'


def experiment_schema(limit=64):
    value = schema(limit)
    fields = value['properties']['actions']['items']['properties']
    fields['enable']['enum'] = [1]
    fields['sw_reset']['enum'] = [0]
    return value


def validate_experimental(payload, limit, initial=False):
    actions = validate(payload, limit, initial=initial)
    for a in actions[8:] if initial else actions:
        if a['enable'] != 1 or a['sw_reset'] != 0:
            raise ValueError('Qualified profile requires enable=1 and sw_reset=0')
        if a['valid'] and not (a['read'] or a['write']):
            raise ValueError('Dummy command outside qualified profile')
    return actions


def verify_freeze(path=FREEZE):
    f = json.loads(path.read_text())
    if not f['offline_gate_pass']:
        raise ValueError('Offline gate is not passed')
    for name, digest in f['hashes'].items():
        if sha(ROOT/name) != digest:
            raise ValueError('Frozen artifact changed: '+name)
    verify(configuration('spi_host_core'))
    return f


def compile_driver(out):
    c = configuration('spi_host_core'); verify(c)
    sources = [str(Path(c['root'])/p) for p in c['sources']]
    out.mkdir(parents=True, exist_ok=True)
    cmd = ['verilator', '--binary', '--timing', '--coverage-line', '--coverage-toggle',
           '--coverage-expr', '-Wno-fatal', '--top-module', 'tb_spi_core', '--Mdir',
           out/'obj', '-j', '2', '-DSYNTHESIS',
           *['-I'+str(Path(c['root'])/p) for p in c['include_dirs']], *sources, DRIVER]
    seconds, _ = invoke(cmd, out/'compile.log', timeout=300)
    return out/'obj/Vtb_spi_core', list(map(str, cmd)), seconds


def check_trace(trace, out):
    """Run exact authored code in a bounded credential-free subprocess."""
    meta = json.loads((CANDIDATE/'authorship.json').read_text())
    for name, digest in meta['artifact_sha256'].items():
        if sha(CANDIDATE/name) != digest:
            raise ValueError('Claude checker artifact changed')
    inputs = out/'checker-input.json'
    inputs.write_text(json.dumps({'batch': trace}, separators=(',', ':'))+'\n')
    result = out/'checker-output.json'
    cmd = [sys.executable, '-I', str(ROOT/'scripts/evaluate_spi_checker_candidate.py'),
           '--worker', '--candidate', str(CANDIDATE), '--inputs', str(inputs), '--output', str(result)]
    env = {k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='spi-core-check-') as cwd:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
    (out/'checker-worker.log').write_text(p.stdout+p.stderr)
    if p.returncode:
        raise RuntimeError('Checker worker failed')
    data = json.loads(result.read_text())
    if data['errors'] or not all(t['pass'] for t in data['selftests']):
        raise RuntimeError('Checker selftests failed')
    checked = data['cases']['batch']
    if checked.get('infrastructure_error'):
        raise RuntimeError('Checker batch failed')
    return checked


def simulate(binary, actions, out, denominator):
    validate_experimental({'actions': actions}, 392, initial=True)
    out.mkdir(parents=True, exist_ok=False)
    (out/'actions.json').write_text(json.dumps({'actions':actions}, indent=2)+'\n')
    vec = out/'vectors.txt'
    vec.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in actions))
    raw = out/'coverage.dat'
    cmd = [binary, '+VECTORS='+str(vec), '+verilator+coverage+file+'+str(raw)]
    started = time.perf_counter()
    try:
        # Stream to disk so timeout/crash accounting retains every emitted row.
        with (out/'simulation.log').open('w') as stream:
            p = subprocess.run(list(map(str,cmd)),cwd=ROOT,stdout=stream,
                               stderr=subprocess.STDOUT,timeout=30)
        seconds = time.perf_counter()-started
        log = (out/'simulation.log').read_text()
        if p.returncode:raise RuntimeError('Simulator failed; partial trace preserved')
    finally:
        text = (out/'simulation.log').read_text() if (out/'simulation.log').exists() else ''
        (out/'execution.json').write_text(json.dumps({
            'command':list(map(str,cmd)), 'simulation_seconds':time.perf_counter()-started,
            'requested_cycles':len(actions),
            'executed_cycles':sum(line.startswith('TRACE ') for line in text.splitlines()),
            'driver_complete':f'DRIVER_OK steps={len(actions)}' in text},indent=2)+'\n')
    if f'DRIVER_OK steps={len(actions)}' not in log:
        raise RuntimeError('Incomplete DUT batch')
    trace = parse(log, actions)
    (out/'trace.json').write_text(json.dumps(trace, separators=(',', ':'))+'\n')
    c = configuration('spi_host_core')
    points = load_all(raw, [str(Path(c['root'])/p) for p in c['sources']])
    (out/'raw-points.json').write_text(json.dumps(points, indent=2)+'\n')
    if len(points) != len(denominator) or {identity(p) for p in points} != denominator:
        raise ValueError('Original DUT counter denominator changed')
    # Simulation finishes and coverage is on disk BEFORE checker execution.
    checked = check_trace(trace, out)
    result = {'coverage':summary(points), 'checker':checked, 'simulation_seconds':seconds,
              'executed_cycles':len(actions), 'command':list(map(str,cmd))}
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    return result, points, trace


def group_status(points, targets):
    counts = {identity(p):p['hits'] for p in points}
    return [{'eclass':g['eclass'], 'nontrivial':g['nontrivial'],
             'raw_source_hits':[counts[tuple(i)] for i in g['counter_identities']],
             'all_hit':all(counts[tuple(i)] > 0 for i in g['counter_identities'])}
            for g in targets]
