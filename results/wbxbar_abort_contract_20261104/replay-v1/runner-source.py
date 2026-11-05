"""Freeze a reviewed checker, then replay unchanged saved actions; no model API."""
import argparse
import csv
import json
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from prepare_wbxbar_cancel_contract import BASE,OLD,REG,FILES,verify_registration
from wbxbar_cancel_validation import candidate_hashes,worker
from wbxbar_experiment import verify_freeze
from wbxbar_exploratory_driver import FIELDS,validate,parse
from inventory_natural_coverage import load_all
from preflight_spi_host import identity


def approval_ready(evaluation,review):
    if evaluation.get('pass') is not True or not evaluation.get('accounts') or not all(x.get('pass') is True for x in evaluation['accounts']):
        raise ValueError('Independent controls have not passed')
    if review.get('ready_for_offline_gate') is not True:raise ValueError('Fresh Claude review not ready')


def freeze(candidate,evaluation,review,output):
    verify_registration();candidate_hashes(candidate)
    if candidate.resolve()==(OLD/'claude-v3/candidate').resolve():raise ValueError('Cannot freeze known-limited prior as revision')
    e=json.loads((evaluation/'summary.json').read_text());r=json.loads(review.read_text())
    approval_ready(e,r)
    if e['checker_sha256']!=sha(candidate/'checker.py'):raise ValueError('Evaluation mismatch')
    role=candidate.parent;review_packet=role/'review-packet.json'
    packet=json.loads(review_packet.read_text())
    if packet['candidate']!={f:(candidate/f).read_text() for f in FILES} or packet['evaluation']!=e:raise ValueError('Reviewed artifacts mismatch')
    metadata=json.loads((role/'review/metadata.json').read_text())
    if metadata.get('status')!='complete' or metadata.get('requested_model')!='claude-opus-5-5':raise ValueError('Missing completed model review')
    prefix='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'
    if (role/'review/prompt.txt').read_text()!=prefix+json.dumps(packet):raise ValueError('Review prompt differs')
    response=json.loads((role/'review/response.json').read_text());body=response['result'].strip()
    if body.startswith('```'):body='\n'.join(body.splitlines()[1:-1])
    if json.loads(body)!=r:raise ValueError('Review is not the exact model response')
    old_run=OLD/'live-v1';execution=json.loads((old_run/'rep1-B/round1/execution.json').read_text())
    binary=Path(execution['command'][0])
    paths=[REG,Path(__file__),ROOT/'scripts/wbxbar_cancel_validation.py',ROOT/'scripts/evaluate_spi_checker_candidate.py',
        ROOT/'scripts/run_spi_checker_author.py',candidate/'authorship.json',*(candidate/f for f in FILES),
        evaluation/'summary.json',evaluation/'evaluations.json',evaluation/'inputs.json',review,review_packet,
        role/'review/metadata.json',role/'review/prompt.txt',role/'review/response.json',binary,old_run/'shared/manifest.json']
    result={'status':'frozen_for_retrospective_replay_only','candidate':str(candidate.relative_to(ROOT)),
        'original_run':str(old_run.relative_to(ROOT)),'binary':str(binary.relative_to(ROOT)),
        'new_model_stimulus_calls':0,'new_live_experiment_allowed':False,
        'independent_review_findings':r.get('findings',[]),'independent_review_limitations':r.get('limitations',[]),
        'attribution_scope':'Accept limited cancellation-repair replay only. Preserve every raw checker verdict. Inherited cross-slave forwarding-order inference is not a normative DUT-defect oracle; any such alarm requires separate source-based attribution. Ownership ambiguity remains unresolved; no whole-IP correctness claim.',
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in paths},
        'limits':'Original generated trajectories reflect old checker feedback. Reclassification is not a new independently generated B/C result.'}
    if output.exists():raise ValueError('Never overwrite freeze')
    output.write_text(json.dumps(result,indent=2)+'\n');return result


def verify_replay_freeze(path):
    verify_registration();old=verify_freeze();f=json.loads(path.read_text())
    if f.get('status')!='frozen_for_retrospective_replay_only' or f.get('new_model_stimulus_calls')!=0:raise ValueError('Replay-only freeze required')
    for p,h in f['hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Replay freeze drift: '+p)
    return f,old


def replay(freeze_path,output):
    f,original=verify_replay_freeze(freeze_path)
    output.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
    (output/'freeze.json').write_bytes(freeze_path.read_bytes());(output/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    source=ROOT/f['original_run'];candidate=ROOT/f['candidate'];binary=ROOT/f['binary']
    manifest=json.loads((source/'shared/manifest.json').read_text());denominator={tuple(i) for i in original['counter_identities']}
    meta={'status':'started','simulator_executions':0,'executed_cycles':0,'simulation_seconds':0.0,
        'new_model_calls':0,'compilations':0,'reused_binary_sha256':sha(binary),'primary_budget_changed':False,
        'accounting':'Additional retrospective replay, not added to primary live metrics. Checker consumes complete public-pin batches after coverage flush.'}
    inputs={};records=[]
    try:
        for rep in range(1,4):
            for arm in ('B','C'):
                session=f'rep{rep}-{arm}'
                for batch in ['seed',*[f'round{i}' for i in range(1,7)]]:
                    name=session+'/'+batch;old=source/name;out=output/name;out.mkdir(parents=True)
                    actions=json.loads((old/'actions.json').read_text())['actions'];validate(actions)
                    (out/'actions.json').write_bytes((old/'actions.json').read_bytes())
                    vec=out/'vectors.txt';vec.write_text(''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions))
                    command=[str(binary),'+VECTORS='+str(vec),'+verilator+coverage+file+'+str(out/'coverage.dat')]
                    t=time.perf_counter();meta['simulator_executions']+=1
                    try:
                        with (out/'simulation.log').open('w') as log:
                            result=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=30)
                    finally:
                        log=(out/'simulation.log').read_text();cycles=sum(l.startswith('PRE ') for l in log.splitlines())
                        elapsed=time.perf_counter()-t;meta['executed_cycles']+=cycles;meta['simulation_seconds']+=elapsed
                        (out/'execution.json').write_text(json.dumps({'command':command,'executed_cycles':cycles,'requested_cycles':len(actions),'simulation_seconds':elapsed},indent=2)+'\n')
                    if result.returncode or cycles!=len(actions) or 'DRIVER_OK steps='+str(len(actions)) not in log:raise ValueError('Replay execution incomplete')
                    trace,transport=parse(log,actions,manifest['inputs'],manifest['outputs'])
                    if trace!=json.loads((old/'trace.json').read_text()):raise ValueError('Pin replay differs: '+name)
                    points=load_all(out/'coverage.dat',manifest['sources'])
                    if len(points)!=len(denominator) or {identity(p) for p in points}!=denominator or points!=json.loads((old/'raw-points.json').read_text()):raise ValueError('Raw counters differ: '+name)
                    previous=json.loads((old/'result.json').read_text())
                    if transport!=previous['transport']:raise ValueError('Transport ledger differs: '+name)
                    (out/'trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n');(out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
                    inputs[name]=trace;records.append({'session':session,'batch':batch,'cycles':cycles,'old_verdict':previous['checker']['verdict'],
                        'old_failures':len(previous['checker']['failures']),'raw_coverage_unchanged':True,'pins_unchanged':True,'transport':transport})
        checked=worker(candidate,inputs,output/'checker')
        if checked['errors'] or not all(x['pass'] for x in checked['selftests']):raise ValueError('Checker selftests failed during replay')
        for row in records:
            name=row['session']+'/'+row['batch'];c=checked['cases'][name]
            if c.get('infrastructure_error'):raise ValueError('Checker failed: '+name)
            row.update(new_verdict=c['verdict'],new_failures=len(c['failures']),new_unresolved=len(c['unresolved']),new_assumption_violations=len(c['assumption_violations']))
            (output/name/'checker-output.json').write_text(json.dumps(c,indent=2)+'\n')
        if len(records)!=42 or meta['executed_cycles']!=8360:raise ValueError('Expected all saved batches/cycles')
        verify_replay_freeze(freeze_path);meta['status']='complete'
        (output/'comparison.json').write_text(json.dumps(records,indent=2)+'\n')
        with (output/'comparison.csv').open('w',newline='') as stream:
            fields=[k for k in records[0] if k!='transport'];w=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(records)
    finally:
        meta['wall_seconds']=time.perf_counter()-start
        (output/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta


if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
    a=sub.add_parser('freeze')
    for name in ('candidate','evaluation','review','output'):a.add_argument('--'+name,type=Path,required=True)
    b=sub.add_parser('replay');b.add_argument('--freeze',type=Path,required=True);b.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.mode=='freeze':r=freeze(args.candidate.resolve(),args.evaluation.resolve(),args.review.resolve(),args.output.resolve());print(r['status'])
    else:print(json.dumps(replay(args.freeze.resolve(),args.output.resolve()),indent=2))
