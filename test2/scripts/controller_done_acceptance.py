"""Read-only independent acceptance of new mock/replay and immutable parents."""
import argparse
import ast
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_loop import verify_data
from controller_monitor_live import ROW_INPUTS,OUTPUTS
from controller_release_live import verify_release


def load(p):return json.loads(p.read_text())


def verify(run_root,replay_root,score_root,replay_score,formal,controls,test_log,out):
    verify_data();a=verify_release(run_root);b=verify_release(replay_root);checks={};logs=0;cycles=0;path_differences=0
    for item in a:
        other=next(x for x in b if (x['arm'],x['repetition'],x['round'])==(item['arm'],item['repetition'],item['round']))
        for name in ('prompt.json','response.json','development-feedback.json','compiled/candidate.sv'):
            if sha(run_root/item['directory']/name)!=sha(replay_root/other['directory']/name):raise ValueError('Replay mismatch: '+name)
    for root in (run_root,replay_root):
        if sha(root/'runner-source.py')!=load(root/'run.json')['runner_sha256']:raise ValueError('Actual execution source not preserved')
    old=ast.parse((run_root/'runner-source.py').read_text());new=ast.parse((BASE/'scripts/controller_done_loop.py').read_text())
    for name in ('execute','messages','develop','plumbing','verify_data','live_gate','model','authorization','append'):
        before=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name==name)
        after=next(n for n in new.body if isinstance(n,ast.FunctionDef) and n.name==name)
        if ast.dump(before)!=ast.dump(after):raise ValueError('Execution function changed since mock: '+name)
    checks['current_execution_functions_match_actual_run']=True
    checks['all36_prompts_sources_feedback_match']=True
    s,t=load(score_root/'scores.json'),load(replay_score/'scores.json')
    labels=load(TASK/'measurements-v1/summary.json')['records'];digests={}
    for label in labels:
        if label['status']!='complete':continue
        rows=load(ROOT/label['directory']/'rows.json');digest=hashlib.sha256(json.dumps(rows,separators=(',',':'),sort_keys=True).encode()).hexdigest()
        lines=[]
        for row in rows:
            values=[row['cycle']]+[row['inputs'][k] for k in ROW_INPUTS]+[row[p][k] for p in ('pre','post') for k in OUTPUTS]
            lines.append(' '.join('x' if v==-1 else f'{v:x}' for v in values))
        digests[label['source'],label['simulator'],label['trace']]=(digest,'\n'.join(lines)+'\n')
    for root in (score_root,replay_score):
        for digest,expected in set(digests.values()):
            if (root/'row-cache'/(digest+'.hex')).read_text()!=expected:raise ValueError('Actual replay vectors differ from sealed physical observations')
    for x,y in zip(s['rounds'],t['rounds']):
        if len(x['cases'])!=len(y['cases']) or x['candidate_status']=='compiled' and len(x['cases'])!=len(labels):raise ValueError('Scoring cases omitted')
        if (x['arm'],x['repetition'],x['round'])!=(y['arm'],y['repetition'],y['round']):raise ValueError('Round order changed')
        for k in x:
            if k=='cases':continue
            if x[k]!=y[k]:raise ValueError('Independent score replay mismatch '+k)
        for c,d in zip(x['cases'],y['cases']):
            for k in c:
                if k not in ('result_path','result_sha256') and c[k]!=d[k]:raise ValueError('Case score differs')
            for root,case in ((score_root,c),(replay_score,d)):
                p=root/case['result_path']
                if sha(p)!=case['result_sha256']:raise ValueError('Scoring result changed')
                r=load(p);raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes())
                if r['rows_sha256']!=digests[case['source'],case['simulator'],case['trace']][0]:raise ValueError('Wrong physical trace graded')
                if hashlib.sha256(raw).hexdigest()!=r['raw_log_sha256'] or sha(p.parent/'replay.log.gz')!=r['compressed_log_sha256']:raise ValueError('Replay log mismatch')
                samples=[v.split() for v in raw.decode().splitlines() if v.startswith('MON ')]
                if len(samples)!=r['samples'] or sum(v[2]=='post' for v in samples)!=r['cycles']:raise ValueError('Actual sample accounting changed')
                for slot,prop in enumerate(r['properties']):
                    failures=[];unknown=[];count=0
                    for v in samples:
                        active,ok=v[3][5-slot],v[4][5-slot];sample=[int(v[1]),v[2]]
                        if active not in '01' or active=='1' and ok not in '01':unknown.append(sample)
                        elif active=='1':
                            count+=1
                            if ok=='0':failures.append(sample)
                    if (count,failures,unknown)!=(prop['checks'],prop['failures'],prop['unknown']):raise ValueError('Raw monitor bits disagree with reported property results')
                logs+=1;cycles+=r['cycles']
            left=gzip.decompress((score_root/c['result_path']).parent.joinpath('replay.log.gz').read_bytes())
            right=gzip.decompress((replay_score/d['result_path']).parent.joinpath('replay.log.gz').read_bytes())
            path_differences+=int(left!=right)
            # Icarus appends the compiled source path to its $finish diagnostic.
            # Normalize exactly the known run prefixes, retain every other byte.
            if left.replace(str(run_root).encode(),b'RUN_ROOT')!=right.replace(str(replay_root).encode(),b'RUN_ROOT'):raise ValueError('Monitor replay differs beyond known root prefix')
    checks['all36_independent_scores_raw_replays_match']=len(s['rounds'])==len(t['rounds'])==36
    checks['raw_bits_and_physical_replay_vectors_independently_checked']=True
    parents={}
    reg=load(REG)
    for name,h in reg['preserve_old_freezes'].items():
        p=ROOT/name
        if sha(p)!=h:raise ValueError('Parent manifest changed')
        f=load(p);members=f.get('files',f.get('artifact_sha256',{}))
        for n,v in members.items():
            if sha(ROOT/n)!=v:raise ValueError('Parent frozen member changed: '+n)
        parents[name]=dict(sha256=h,members=len(members))
    old_scores={'test2/results/controller-final-v1/scores.json':'f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651',
                'test2/results/live-final-v1/scores.json':'33003b33a7172d29704f85fa84da10bdbb30aebe78b72d400a4f97b73a2ef338'}
    for n,h in old_scores.items():
        if sha(ROOT/n)!=h:raise ValueError('Old score changed')
    checks['old_scores_and_parent_members_match']=True
    q=load(controls/'summary.json');f=load(formal/'summary.json');checks['formal_controls']=q['status']=='passed'
    native=[]
    for path in formal.rglob('result.json'):
        r=load(path)
        if r.get('scope')!='safety_projection':continue
        p=path.parent/'work/status';v=p.read_text().split()[0] if p.exists() else None
        if v is not None and v!=r['status']:raise ValueError('Native formal status changed')
        if "wire trace_done=1'b0" not in (path.parent/'harness.sv').read_text():raise ValueError('Projection marker changed')
        native.append(r['status'])
    checks['formal_schedule_all540_recorded']=len(f['jobs'])==540 and len(native)==sum(r['status'] not in ('INVALID_CANDIDATE','NOT_RUN_TOTAL_CAP') for r in f['jobs'])
    n=re.search(r'Ran (\d+) tests',test_log.read_text())
    checks['test_log_passed']=bool(n) and int(n.group(1))>=74 and test_log.read_text().rstrip().endswith('OK')
    evidence=[REG,TASK/'input-freeze.json',TASK/'evaluation-freeze.json',TASK/'public/prompt-packets-v1/audit.json',run_root/'release.json',replay_root/'release.json',score_root/'scores.json',replay_score/'scores.json',formal/'summary.json',controls/'summary.json',test_log]
    for p in sorted((BASE/'scripts').glob('controller_done_*.py')):evidence.append(p)
    evidence.append(BASE/'tests/test_controller_done_study.py')
    result=dict(status='accepted_offline_with_scope' if all(checks.values()) else 'failed',checks=checks,
        current_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),historical_audit_HEAD_not_reused=True,
        parent_freezes=parents,old_scores=old_scores,scoring_raw_logs_verified=logs,scoring_actual_monitor_cycles=cycles,
        raw_log_pairs_with_known_directory_difference=path_differences,raw_comparison='Every byte after replacing only exact known run root; original SHA checked separately',
        formal_status_counts=dict(Counter(native)),API_calls=0,new_model_trials=0,paid_authorization=False,
        actual_provider_tokens='UNKNOWN_NOT_CALLED',reference_review='PREPARED_NOT_RUN',finite_completion_proved=False,
        evidence_sha256={str(p.relative_to(ROOT)):sha(p) for p in evidence},limitations=['No new B/C effect estimate: identical arm-blind plumbing programs','Physical observed cases only; N10 unobserved retained','Oracle/candidate unknown contexts are not PASS','trace_done0 short formal projection cannot prove128cycle completion','No token-matched placebo: future B/C estimates whole feedback package only'])
    dump(out,result);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=BASE/'results'
    x=verify(r/'controller-done-mock-v1',r/'controller-done-replay-v1',r/'controller-done-score-mock-v1',r/'controller-done-score-replay-v1',r/'controller-done-formal-mock-v1',r/'controller-done-formal-controls-v3',r/'controller-done-tests-v4.log',a.output.resolve());print(json.dumps({k:v for k,v in x.items() if k not in ('evidence_sha256',)},indent=2))
