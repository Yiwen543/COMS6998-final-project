"""Role-separated, bounded execution and control accounting. No checker edits."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from evaluate_spi_checker_candidate import worker
from run_midterm_fixed import sha

def clean(r):
    return not r.get('infrastructure_error') and not r.get('failures') and not r.get('assumption_violations')

def scoped_pass(r):
    # The author prompt did not fix verdict enum strings. Retain raw labels;
    # accept the documented author contract's "pass" as scoped pass only when
    # no unresolved obligations or failures remain. Never modify checker logic.
    return clean(r) and r.get('verdict') in ('scoped_pass','pass') and not r.get('unresolved')

def successful_events(r):
    return [e for e in r.get('events',[]) if e.get('kind')=='pass']

def evaluate(candidate,controls,out):
    meta=json.loads((candidate/'authorship.json').read_text())
    for f,h in meta['artifact_sha256'].items():
        if sha(candidate/f)!=h:raise ValueError('Author artifact changed: '+f)
    cm=json.loads((controls/'manifest.json').read_text())
    for name in ('inputs','controls'):
        if sha(controls/(name+'.json'))!=cm[name+'_sha256']:raise ValueError('Control evidence changed')
    out.mkdir(parents=True,exist_ok=False)
    command=[sys.executable,'-I',str(Path(__file__).resolve()),'--worker','--candidate',str(candidate),'--controls',str(controls),'--output',str(out/'evaluations.json')]
    env={k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='spi-core-evaluation-') as cwd:
        p=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    (out/'worker.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('Worker failed; preserved log')
    evaluated=json.loads((out/'evaluations.json').read_text());rs=evaluated['cases'];account=[]
    for c in json.loads((controls/'controls.json').read_text()):
        r=rs[c['name']];row={**c,'verdict':r.get('verdict'),'failure_count':len(r.get('failures',[])),'assumption_count':len(r.get('assumption_violations',[])),'unresolved':r.get('unresolved',[]),'infrastructure_error':r.get('infrastructure_error')}
        if c['kind']=='independent_positive':row['no_false_alarm']=clean(r);row['scoped_pass']=scoped_pass(r)
        if c['kind']=='single_fault':
            b=rs[c['baseline']];row['baseline_clean']=clean(b);row['baseline_scoped_pass']=scoped_pass(b)
            row['raw_failure_flag']=bool(r.get('failures'));row['credited_detection']=row['baseline_scoped_pass'] and row['raw_failure_flag'] and not r.get('assumption_violations') and not r.get('infrastructure_error')
        if c['kind']=='incomplete':row['success_events_emitted']=successful_events(r);row['all_events']=r.get('events',[])
        if c['kind']=='input_protocol':row['correct_input_classification']=bool(r.get('assumption_violations')) and not r.get('failures')
        account.append(row)
    event_errors=[]
    for c in json.loads((controls/'controls.json').read_text()):
        family=c.get('required_event_family')
        if family and not any(e.get('family')==family for e in rs[c['name']].get('events',[])):
            event_errors.append({'case':c['name'],'required_event_family':family,
                'reason':'Required triggered event missing; an empty event list is not a passing integrity check'})
        forbidden=c.get('forbidden_event_family')
        false_events=[e for e in rs[c['name']].get('events',[]) if e.get('family')==forbidden] if forbidden else []
        if false_events:
            event_errors.append({'case':c['name'],'forbidden_event_family':forbidden,'events':false_events,
                'reason':'Recovery event claimed on independently verified no-stall control'})
        forbidden_success=c.get('forbidden_success_event_family')
        false_success=[e for e in successful_events(rs[c['name']]) if e.get('family')==forbidden_success] if forbidden_success else []
        if false_success:
            event_errors.append({'case':c['name'],'forbidden_success_event_family':forbidden_success,'events':false_success,
                'reason':'Successful recovery credited from flag evidence without a real paused operation'})
    for name,r in rs.items():
        for e in successful_events(r):
            if not isinstance(e,dict) or not isinstance(e.get('start_cycle'),int) or not isinstance(e.get('end_cycle'),int):
                event_errors.append({'case':name,'event':e,'reason':'Missing integer event window'});continue
            if e['end_cycle']<e['start_cycle']:event_errors.append({'case':name,'event':e,'reason':'Reversed window'})
            violations=[v for v in r.get('failures',[])+r.get('assumption_violations',[]) if isinstance(v,dict) and isinstance(v.get('cycle'),int) and e['start_cycle']<=v['cycle']<=e['end_cycle']]
            if violations:event_errors.append({'case':name,'event':e,'reason':'Successful event overlaps checker/assumption violation','violations':violations})
    brief={name:{'verdict':r.get('verdict'),'failures':r.get('failures',[]),'assumption_violations':r.get('assumption_violations',[]),'events':r.get('events',[]),'unresolved':r.get('unresolved',[]),'counts':r.get('counts'),'infrastructure_error':r.get('infrastructure_error')} for name,r in rs.items()}
    result={'status':'evaluated_not_frozen','checker_author':'claude-opus-5-5','controls_author':'GPT/Codex','B_allowed':False,
       'selftests':evaluated['selftests'],'worker_errors':evaluated['errors'],'controls':account,'cases':brief,'event_integrity_errors':event_errors,
       'successful_events_on_unresolved_cases':{name:successful_events(r) for name,r in rs.items() if r.get('unresolved') and successful_events(r)},
       'control_counts':{'independent_positive':sum(c['kind']=='independent_positive' for c in account),'no_false_alarm':sum(c.get('no_false_alarm',False) for c in account),'baseline_scoped_pass_negatives':sum(c.get('baseline_scoped_pass',False) for c in account),'negative_total':sum(c['kind']=='single_fault' for c in account),'credited_detections':sum(c.get('credited_detection',False) for c in account),'raw_negative_flags':sum(c.get('raw_failure_flag',False) for c in account)},
       'limits':['No calibration trace presumed correct because it came from the DUT.','Raw failure flags on a failing baseline are not detection credit.','Selftests do not independently validate the checker.','Pending/unresolved is not pass. No new simulation or API call in evaluation.'],
       'hashes':{str(p):sha(p) for p in [candidate/'checker.py',candidate/'selftest.py',controls/'inputs.json',controls/'controls.json',Path(__file__)]}}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['control_counts']))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--controls',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--worker',action='store_true');a=p.parse_args()
    if a.worker:worker(a.candidate,a.controls/'inputs.json',a.output)
    else:evaluate(a.candidate.resolve(),a.controls.resolve(),a.output.resolve())
