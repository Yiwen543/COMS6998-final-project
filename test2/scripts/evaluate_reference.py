#!/usr/bin/env python3
"""Run immutable Claude reference code in an isolated worker; no candidate scoring."""
import argparse
import copy
import json
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BASE, clean_env, dump, sha
from run_spi_checker_author import validate_source

def load(path):
    source=path.read_text();validate_source(source)
    scope={'__name__':'reference_checker'}
    exec(compile(source,str(path),'exec'),scope)
    return scope

def worker(candidate,inputs,out):
    resource.setrlimit(resource.RLIMIT_CPU,(45,45))
    check=load(candidate/'checker.py')['check_rows']
    test=load(candidate/'selftest.py')['run']
    report={'selftests':None,'selftest_error':None,'cases':{}}
    try:report['selftests']=test(check)
    except Exception as e:report['selftest_error']={'type':type(e).__name__,'detail':str(e)}
    for name,rows in json.loads(inputs.read_text()).items():
        try:
            result=check(copy.deepcopy(rows))
            if not isinstance(result,dict) or result.get('verdict') not in ('PASS','FAIL','UNRESOLVED','INVALID_INPUT'):
                raise ValueError('Reference result schema')
            report['cases'][name]=result
        except Exception as e:report['cases'][name]={'verdict':'INFRASTRUCTURE_ERROR','type':type(e).__name__,'detail':str(e)}
    dump(out,report)

def evaluate(candidate,preflight,out,supplement=None):
    out.mkdir(parents=True,exist_ok=False)
    meta=json.loads((candidate/'metadata.json').read_text())
    for name,h in meta['artifact_sha256'].items():
        if sha(candidate/name)!=h:raise ValueError('Claude artifact edited')
    controls=json.loads((BASE/'private/reference-controls-v1.json').read_text())
    if supplement:
        extra=json.loads(supplement.read_text())
        if set(extra)&set(controls):raise ValueError('Supplement must not replace registered controls')
        controls.update(extra)
    inputs={'independent/'+k:v['rows'] for k,v in controls.items()}
    for control in ('correct_stress','correct_original','M01','M02','M03','M04','M05','M06'):
        for sim in ('verilator','iverilog'):
            for name in ('basic','boundary','wrap_reset','final_boundary','final_wrap_reset','final_mixed'):
                inputs[f'{control}/{sim}/{name}']=json.loads((preflight/control/sim/name/'rows.json').read_text())
    dump(out/'inputs.json',inputs)
    cmd=[sys.executable,'-I',str(Path(__file__).resolve()),'--worker','--candidate',str(candidate),
         '--inputs',str(out/'inputs.json'),'--output',str(out/'evaluations.json')]
    with tempfile.TemporaryDirectory(prefix='test2-reference-') as cwd:
        p=subprocess.run(cmd,cwd=cwd,env=clean_env(),capture_output=True,text=True,timeout=60)
    (out/'worker.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('Reference worker failed')
    report=json.loads((out/'evaluations.json').read_text())
    controls_report=[{'name':n,'expected':c['expected_verdict'],'actual':report['cases']['independent/'+n]['verdict'],
                      'match':c['expected_verdict']==report['cases']['independent/'+n]['verdict']} for n,c in controls.items()]
    correct={k:v['verdict'] for k,v in report['cases'].items() if k.startswith('correct_')}
    eligibility=[]
    for mid in ('M01','M02','M03','M04','M05','M06'):
        for name in ('final_boundary','final_wrap_reset','final_mixed'):
            result=report['cases'][f'{mid}/verilator/{name}']
            failures=result.get('failures',[])
            eligible=result['verdict']=='FAIL' and bool(failures)
            eligibility.append({'mutant':mid,'trace':name,'two_state_reference_verdict':result['verdict'],
                'icarus_reference_verdict':report['cases'][f'{mid}/iverilog/{name}']['verdict'],
                'eligible_provisional_until_review':eligible,
                'eligible_by_simulator':{'verilator_two_state':eligible,
                    'icarus_four_state_observations':report['cases'][f'{mid}/iverilog/{name}']['verdict']=='FAIL' and bool(report['cases'][f'{mid}/iverilog/{name}'].get('failures'))},
                'first_reference_failure':failures[0] if failures else None})
    result={'checker_sha256':sha(candidate/'checker.py'),'selftests':report['selftests'],
        'selftest_error':report['selftest_error'],'independent_controls':controls_report,
        'correct_control_verdicts':correct,'fault_eligibility':eligibility,
        'ready_for_read_only_review':report['selftest_error'] is None and isinstance(report['selftests'],dict) and report['selftests'].get('passed') is True and all(c['match'] for c in controls_report) and all(v=='PASS' for v in correct.values()),
        'comparison_metrics':{k:{'author_checks':v.get('checks',0),
            'unknown_comparisons':len(v.get('unresolved',[])),
            'definite_comparisons':v.get('checks',0)-len(v.get('unresolved',[])),
            'partial_findings_authoritative':v.get('verdict')!='INVALID_INPUT'} for k,v in report['cases'].items()},
        'property_reporting':{'direct_field_checks':['P2_FILL','P3_FULL','P4_EMPTY','P5_DATA_ORDER'],
                              'reset':'P1 is realized through field checks at reset; no separate activation count',
                              'acceptance':'P6 is indirect via expected queue transitions; no independent P6 activation/detection credit'},
        'not_a_freeze':True,'new_model_calls':0}
    dump(out/'summary.json',result)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',action='store_true');p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--preflight',type=Path);p.add_argument('--inputs',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--supplement',type=Path)
    a=p.parse_args()
    if a.worker:worker(a.candidate,a.inputs,a.output)
    else:
        r=evaluate(a.candidate.resolve(),a.preflight.resolve(),a.output.resolve(),a.supplement.resolve() if a.supplement else None)
        print(json.dumps({k:r[k] for k in ('checker_sha256','ready_for_read_only_review','selftest_error')},indent=2))
