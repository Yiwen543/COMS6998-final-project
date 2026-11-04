#!/usr/bin/env python3
"""Evaluate immutable Claude checker candidates; GPT role supplies test inputs only."""
import argparse
import copy
import json
import os
import resource
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_midterm_fixed import ROOT, sha
from run_spi_checker_author import validate_source
from spi_host_fixture import parse


def load_candidate(path):
    source = path.read_text()
    validate_source(source)
    space = {'__name__':'checker_candidate'}
    exec(compile(source, str(path), 'exec'), space)
    return space


def worker(candidate, inputs, output):
    resource.setrlimit(resource.RLIMIT_CPU, (30,30))
    checker = load_candidate(candidate/'checker.py')['check_rows']
    selftest = load_candidate(candidate/'selftest.py')['run']
    report = {'selftests':None,'cases':{},'errors':[]}
    try:
        report['selftests'] = selftest(checker)
    except Exception as e:
        report['errors'].append({'stage':'selftest','type':type(e).__name__,'detail':str(e)})
    for name, rows in json.loads(inputs.read_text()).items():
        try:
            report['cases'][name] = checker(copy.deepcopy(rows))
        except Exception as e:
            report['cases'][name] = {'infrastructure_error':type(e).__name__,'detail':str(e)}
    output.write_text(json.dumps(report,indent=2)+'\n')


def prepare_inputs(calibration):
    data, controls = {}, []
    info = json.loads((calibration/'summary.json').read_text())
    for name in info['candidate_cases']:
        data['calibration/'+name] = json.loads((calibration/name/'rows.json').read_text())
    # Existing specification-derived GPT trace is independently authored relative
    # to the Claude candidate. It is not an experimental test-generation prompt.
    sys.path.insert(0,str(ROOT/'tests'))
    from test_spi_host_fixture import reference_trace
    data['independent_reference/one_byte_write'] = reference_trace()

    def mutate(name, source, predicate, side, field, value):
        rows = copy.deepcopy(data['calibration/'+source])
        row = next((r for r in rows if predicate(r)), None)
        if row is None:
            controls.append({'name':name,'status':'inapplicable'})
            return
        old = row[side][field]
        row[side][field] = value(row) if callable(value) else value
        if row[side][field] == old:
            raise AssertionError('Mutation does not change trace')
        data['negative/'+name] = rows
        controls.append({'name':name,'status':'applied','source_case':source,
                         'cycle':row['cycle'],'side':side,'signal':field,
                         'before':old,'after':row[side][field]})

    mutate('clock_moves_during_stall','tx_recovery',lambda r:r['pre']['tx_stall'],
           'post','sck',lambda r:1-r['pre']['sck'])
    mutate('missing_last_write','tx_recovery',lambda r:r['pre']['last_write'], 'pre','last_write',0)
    mutate('dropped_receive_byte','rx_recovery',lambda r:r['pre']['rd'] and not r['pre']['last_read'],'pre','rd',0)
    mutate('asynchronous_reset_wrong_select','asynchronous_abort_restart',
           lambda r:r['cycle']>8 and not r['action']['rst_n'],'pre','csb',2)
    mutate('software_reset_not_idle','software_abort_restart',
           lambda r:r['action']['sw_reset'],'post','active',1)
    mutate('multiple_selects_during_switch','csid_switch',lambda r:r['post']['csb']==1,'post','csb',0)
    mutate('last_read_without_transfer','asynchronous_abort_restart',
           lambda r:r['cycle']>9 and r['pre']['csb']==3 and not r['pre']['rd'] and r['action']['rst_n'],
           'pre','last_read',1)
    mutate('held_software_reset_wrong_select','software_abort_restart',
           lambda r:r['action']['sw_reset'] and r['cycle']>0 and
             data['calibration/software_abort_restart'][r['cycle']-1]['action']['sw_reset'],
           'pre','csb',2)
    mutate('select_changes_during_stall','tx_recovery',lambda r:r['pre']['tx_stall'], 'post','csb',3)
    mutate('read_without_sink_ready','rx_recovery',lambda r:r['pre']['rx_stall'] and not r['action']['rx_ready'],
           'pre','rd',1)
    mutate('async_reset_stale_write','asynchronous_abort_restart',
           lambda r:r['cycle']>8 and r['action']['rst_n'] and
             not data['calibration/asynchronous_abort_restart'][r['cycle']-1]['action']['rst_n'],
           'pre','wr',1)
    mutate('spurious_idle_clock','tx_recovery',lambda r:r['cycle']>100 and r['pre']['csb']==3,
           'post','sck',lambda r:1-r['pre']['sck'])
    for name in info['candidate_cases']:
        rows=data['calibration/'+name]
        if 'switch' in name:
            # No restarted command completed yet; never count switch completion.
            cutoff=next((r['cycle'] for r in rows if r['cycle']>12 and r['pre']['csb']!=3), 13)
        elif 'abort' in name:
            cutoff=next(r['cycle']+1 for r in rows if r['cycle']>8 and
                        (not r['action']['rst_n'] or r['action']['sw_reset']))
        else:
            cutoff=next(r['cycle']+1 for r in rows if r['pre']['tx_stall'] or r['pre']['rx_stall'])
        data['truncated/'+name]=rows[:cutoff]
    # Deliberately bad driver input is an assumption failure, not a DUT defect.
    rows=copy.deepcopy(data['calibration/csid_switch'])
    pending=next((r for r in rows if r['action']['valid'] and not r['pre']['ready']),None)
    if pending and pending['cycle']+1<len(rows):
        rows[pending['cycle']+1]['action']['valid']=0
        data['invalid_driver/dropped_pending_valid']=rows
    return data, controls


def evaluate(candidate, calibration, output):
    output.mkdir(parents=True,exist_ok=False)
    (output/'evaluator-source.py').write_bytes(Path(__file__).read_bytes())
    metadata=json.loads((candidate/'metadata.json').read_text())
    for name,digest in metadata['artifact_sha256'].items():
        if sha(candidate/name)!=digest:
            raise ValueError('Checker author artifact was edited: '+name)
    data, controls=prepare_inputs(calibration)
    inputs=output/'private-validation-inputs.json'
    inputs.write_text(json.dumps(data,separators=(',',':'))+'\n')
    command=[sys.executable,'-I',str(Path(__file__).resolve()),'--worker','--candidate',str(candidate),
             '--inputs',str(inputs),'--output',str(output/'evaluations.json')]
    # No model credentials are inherited by generated checker execution.
    env={k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='spi-checker-eval-') as cwd:
        run=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    (output/'worker.log').write_text(run.stdout+run.stderr)
    if run.returncode:
        raise RuntimeError('Candidate worker failed; see log')
    evaluated=json.loads((output/'evaluations.json').read_text())
    concise={}
    for name,value in evaluated['cases'].items():
        concise[name]={'verdict':value.get('verdict'), 'infrastructure_error':value.get('infrastructure_error'),
            'failure_count':len(value.get('failures',[])),
            'categories':sorted({f.get('category','missing') for f in value.get('failures',[])}),
            'assumption_count':len(value.get('assumption_violations',[])),
            'events':value.get('events',[]),'unresolved':value.get('unresolved',[])}
    result={'checker_role':'claude-opus-5-5','stimulus_role':'GPT integration',
        'checker_sha256':sha(candidate/'checker.py'),'author_response_sha256':sha(candidate/'response.json'),
        'evaluation_script_sha256':sha(Path(__file__)), 'selftests':evaluated['selftests'],
        'errors':evaluated['errors'],'controls':controls,'cases':concise,
        'decision':'Requires explicit review of scope, positive controls, negatives and incomplete-event handling; not auto-frozen',
        'new_model_calls':0,'new_simulations':0}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--candidate',type=Path,required=True)
    cli.add_argument('--calibration',type=Path)
    cli.add_argument('--inputs',type=Path)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--worker',action='store_true')
    args=cli.parse_args()
    if args.worker:
        worker(args.candidate,args.inputs,args.output)
    else:
        result=evaluate(args.candidate.resolve(),args.calibration.resolve(),args.output.resolve())
        print(json.dumps({'cases':len(result['cases']),'selftests':result['selftests'],'errors':result['errors']},indent=2))
