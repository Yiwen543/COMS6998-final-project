#!/usr/bin/env python3
"""Execute fixed FIFO controls without a candidate model or a GPT scoring oracle."""
import argparse
import json
from pathlib import Path
import subprocess
from common import BASE, ROOT, dump, run, sha
from coverage import load, summary
from sfifo_fixture import parse_trace, validate_actions, write_vectors
from semantic_candidate_scan import scan, map_true_counter

TOP = 'tb_sfifo_stress_fixed'

def verify_inputs():
    manifest = json.loads((BASE/'configs/input_manifest_v1.json').read_text())
    assert manifest['registration_sha256'] == sha(BASE/'configs/registration_v1.json')
    for name, digest in manifest['files'].items():
        if sha(BASE/name) != digest: raise ValueError('Registered input changed: '+name)
    return manifest

def rows(actions, log):
    observations = parse_trace(log)
    if len(observations) != len(actions): raise ValueError('Incomplete trace')
    out = []
    for i, (action, observed) in enumerate(zip(actions, observations)):
        if observed['step'] != i: raise ValueError('Trace ordering')
        out.append({'cycle':i, 'action':action, **{phase: {
            key: observed[f'{phase}_{key}'] for key in ('fill','full','empty','data')}
            for phase in ('pre','post')}})
    return out

def normalize(trace):
    # Compare only defined observations: first pre excluded, empty data ignored.
    out = json.loads(json.dumps(trace))
    for row in out:
        if row['cycle'] == 0: row['pre'] = None
        for phase in ('pre', 'post'):
            if row[phase] and row[phase]['empty'] == 1: row[phase]['data'] = None
    return out

def compile_source(source, sim, out):
    out.mkdir(parents=True)
    driver = BASE/'public/driver.sv'
    if sim == 'iverilog':
        binary = out/'driver.vvp'
        argv = ['iverilog','-g2012','-s',TOP,'-o',binary,source,driver]
    else:
        binary = out/'verilator-build'/f'V{TOP}'
        argv = ['verilator','--binary','--timing','--coverage-line','--coverage-toggle',
                '--coverage-expr','-Wno-fatal','--top-module',TOP,'--Mdir',binary.parent,
                '-j','2',source,driver]
    info = run(argv, out/'compile.log', 240)
    dump(out/'compile.json', info)
    if info['status'] != 'complete': raise RuntimeError(str(out/'compile.log'))
    return binary

def simulate(source, sim, binary, actions, out):
    out.mkdir(parents=True)
    write_vectors(actions, out/'actions.hex')
    argv = ([binary] if sim == 'verilator' else ['vvp',binary]) + [f'+VECTORS={out/"actions.hex"}']
    if sim == 'verilator': argv += [f'+verilator+coverage+file+{out/"coverage.dat"}']
    info = run(argv,out/'simulation.log',60)
    log = (out/'simulation.log').read_text()
    if info['status'] != 'complete' or f'DRIVER_OK steps={len(actions)}' not in log:
        raise RuntimeError('Incomplete simulation')
    trace = rows(actions, log)
    dump(out/'rows.json', trace)
    points = []
    if sim == 'verilator':
        points = load(out/'coverage.dat',str(source.relative_to(ROOT)),include_descendants=True)
        dump(out/'coverage.json', points)
    info.update(cycles=len(actions), trace_sha256=sha(out/'rows.json'),
                coverage=summary(points), reference_status='not_yet_evaluated')
    dump(out/'simulation.json', info)
    return trace, points

def equivalence(out):
    # No upstream FORMAL assumptions/assertions enabled in this comparison.
    original = ROOT/'examples/heldout_sfifo/rtl/sfifo.v'
    variant = BASE/'public/sfifo.v'
    settings = '-set BW 8 -set LGFLEN 4 -set OPT_ASYNC_READ 1 -set OPT_WRITE_ON_FULL 0 -set OPT_READ_ON_EMPTY 0 sfifo'
    program = (f'read_verilog -sv {original}; chparam {settings}; rename sfifo gold; '
               f'read_verilog -sv {variant}; chparam {settings}; rename sfifo gate; '
               'proc; memory; equiv_make gold gate equiv; hierarchy -top equiv; '
               'equiv_simple; equiv_induct -seq 24; equiv_status -assert')
    info = run(['yosys','-Q','-T','-p',program], out/'equivalence.log',180)
    if info['status'] != 'complete' or 'Equivalence successfully proven!' not in (out/'equivalence.log').read_text():
        raise RuntimeError('Equivalence not proved')
    info['scope'] = 'Fixed-parameter two-state implementation correspondence, not specification correctness'
    dump(out/'equivalence.json', info)
    return info

def main():
    p = argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True)
    args = p.parse_args(); out = args.output.resolve(); out.mkdir(parents=True,exist_ok=False)
    verify_inputs()
    versions = {}
    for tool, flag in [('verilator','--version'),('iverilog','-V'),('yosys','-V'),('sby','--version'),('z3','--version')]:
        result=run([tool,flag],out/f'{tool}-version.log')
        versions[tool]={'result':result,'first_line':(out/f'{tool}-version.log').read_text().splitlines()[0]}
    dump(out/'versions.json', versions)
    equivalence(out)
    semantic = scan([BASE/'public/sfifo.v'], 'sfifo', flatten=False)
    dump(out/'semantic.json',semantic)
    sources={'correct_stress':BASE/'public/sfifo.v', 'correct_original':BASE/'private/original_noformal.v'}
    sources.update({x.stem:x for x in sorted((BASE/'private/mutants').glob('*.v'))})
    action_files=sorted((BASE/'public/development').glob('*.json'))+sorted((BASE/'private/final').glob('*.json'))
    all_rows, raw = {}, {}
    for label, source in sources.items():
        for sim in ('iverilog','verilator'):
            build=out/label/sim
            binary=compile_source(source,sim,build)
            for f in action_files:
                actions=validate_actions(json.loads(f.read_text()),1024)
                trace, points=simulate(source,sim,binary,actions,build/f.stem)
                all_rows[label,sim,f.stem]=trace
                if label=='correct_stress' and sim=='verilator': raw[f.stem]=points
        print('compiled and replayed',label,flush=True)
    agreements=[]
    for label in sources:
        for f in action_files:
            agree=normalize(all_rows[label,'iverilog',f.stem])==normalize(all_rows[label,'verilator',f.stem])
            agreements.append({'control':label,'trace':f.stem,'defined_public_pins_equal':agree})
    divergence=[]
    for label in sources:
        if not label.startswith('M'): continue
        for f in action_files:
            a=normalize(all_rows['correct_stress','verilator',f.stem]); b=normalize(all_rows[label,'verilator',f.stem])
            diffs=[x['cycle'] for x,y in zip(a,b) if x!=y]
            divergence.append({'mutant':label,'trace':f.stem,'first_public_divergence':diffs[0] if diffs else None,
                'divergent_cycles':len(diffs),'scorable_fault':None,'eligibility':'pending independent Claude reference'})
    baseline_equal=all(normalize(all_rows['correct_stress','verilator',f.stem])==normalize(all_rows['correct_original','verilator',f.stem]) for f in action_files)
    mapped=[]
    for group in semantic['groups']:
        if not group['requires_egg_rewrite_to_merge']: continue
        members=[]
        for m in group['members']:
            mapping=map_true_counter(m,raw['basic'])
            members.append({'line':m['line'],'mapping':mapping})
        mapped.append({'eclass':group['eclass'],'members':members})
    dump(out/'source-mappings.json',mapped)
    dump(out/'cross-simulator.json',agreements)
    dump(out/'fault-observability-precheck.json',divergence)
    result={'status':'offline_measurements_complete_reference_pending',
        'baseline_defined_pins_equal':baseline_equal,'cross_simulator_matches':sum(x['defined_public_pins_equal'] for x in agreements),
        'cross_simulator_pairs':len(agreements),'compilations':len(sources)*2,
        'simulator_executions':len(sources)*2*len(action_files),
        'executed_cycles':sum(len(json.loads(f.read_text())['actions']) for f in action_files)*len(sources)*2,
        'raw_denominators':{n:{k:v['total'] for k,v in summary(p).items()} for n,p in raw.items()},
        'no_reference_or_candidate_model_called':True,'fault_eligibility_not_yet_established':True}
    dump(out/'summary.json',result)
    # A mutant can expose uninitialized storage. Keep the X/two-state difference
    # visible instead of treating it as a disagreement between binary outputs.
    from audit_observations import audit
    classified=audit(out,out/'cross-tool-classification.json')
    if not baseline_equal or classified['exact_control_matches']!=12:
        raise RuntimeError('Control comparison mismatch; inspect retained evidence')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
