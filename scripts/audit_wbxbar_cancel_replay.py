"""Recompute retrospective replay evidence and map old alarms without editing verdicts."""
import argparse
import collections
import json
import re
import tempfile
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from replay_wbxbar_cancel import verify_replay_freeze
from wbxbar_exploratory_driver import parse,FIELDS
from inventory_natural_coverage import load_all
from wbxbar_cancel_validation import worker


def audit(run,output):
    f,original=verify_replay_freeze(run/'freeze.json');old=ROOT/f['original_run']
    records=json.loads((run/'comparison.json').read_text());meta=json.loads((run/'metadata.json').read_text())
    if meta['status']!='complete':raise ValueError('Replay incomplete')
    expected={(f'rep{rep}-{arm}',batch) for rep in range(1,4) for arm in ('B','C') for batch in ['seed',*[f'round{i}' for i in range(1,7)]]}
    if {(r['session'],r['batch']) for r in records}!=expected or len(records)!=42:raise ValueError('Scheduled replay differs')
    manifest=json.loads((old/'shared/manifest.json').read_text());cycles=0;inputs={};correspondence=[];finals=[]
    for row in records:
        name=row['session']+'/'+row['batch'];p=run/name;q=old/name
        actions=json.loads((p/'actions.json').read_text())['actions']
        if (p/'actions.json').read_bytes()!=(q/'actions.json').read_bytes():raise ValueError('Saved actions changed')
        vectors=''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions)
        if (p/'vectors.txt').read_text()!=vectors:raise ValueError('Vectors differ from actions')
        trace,transport=parse((p/'simulation.log').read_text(),actions,manifest['inputs'],manifest['outputs'])
        if trace!=json.loads((p/'trace.json').read_text()) or trace!=json.loads((q/'trace.json').read_text()):raise ValueError('Public pin replay drift')
        points=load_all(p/'coverage.dat',manifest['sources'])
        if points!=json.loads((q/'raw-points.json').read_text()) or points!=json.loads((p/'raw-points.json').read_text()) or len(points)!=len(original['counter_identities']):raise ValueError('Raw DUT coverage drift')
        execution=json.loads((p/'execution.json').read_text());n=sum(l.startswith('PRE ') for l in (p/'simulation.log').read_text().splitlines())
        if n!=execution['executed_cycles'] or n!=len(actions):raise ValueError('Cycle accounting mismatch')
        cycles+=n;inputs[name]=trace
        before=json.loads((q/'result.json').read_text());after=json.loads((p/'checker-output.json').read_text())
        if transport!=row['transport'] or transport!=before['transport']:raise ValueError('Transport changed')
        if row['old_verdict']!=before['checker']['verdict'] or row['new_verdict']!=after['verdict']:raise ValueError('Verdict summary drift')
        for field,key in [('new_failures','failures'),('new_unresolved','unresolved'),('new_assumption_violations','assumption_violations')]:
            if row[field]!=len(after[key]):raise ValueError('Diagnostic summary drift')
        if row['old_failures']!=len(before['checker']['failures']):raise ValueError('Old count drift')
        candidates=list(enumerate(after['unresolved']));used=set()
        for failure in before['checker']['failures']:
            slave=re.search(r'slave (\d+)',failure['detail'])
            matches=[(i,u) for i,u in candidates if i not in used and u['cycle']==failure['cycle'] and u['item']=='post_abort_forward'
                     and slave and re.search(r'slave (\d+)',u['detail']) and re.search(r'slave (\d+)',u['detail']).group(1)==slave.group(1)]
            if len(matches)!=1:raise ValueError('Old alarm has no unique same-cycle/slave cancellation record: '+name)
            index,item=matches[0];used.add(index)
            correspondence.append({'session':row['session'],'batch':row['batch'],'old_failure':failure,'new_unresolved_index':index,'new_unresolved':item,
                'classification':'same-cycle same-slave explicit post_abort_forward; not merely suppressed by a prior ownership ambiguity'})
        if row['batch']=='round6':
            finals.append({k:v for k,v in row.items() if k!='transport'}|{'unresolved_categories':dict(collections.Counter(x['item'] for x in after['unresolved']))})
    if cycles!=8360 or cycles!=meta['executed_cycles'] or meta['simulator_executions']!=42:raise ValueError('Replay costs differ')
    with tempfile.TemporaryDirectory(prefix='wbxbar-cancel-audit-') as temp:
        rerun=worker(ROOT/f['candidate'],inputs,Path(temp)/'checker')
    if rerun!=json.loads((run/'checker/evaluations.json').read_text()):raise ValueError('Fresh checker execution differs')
    for name,result in rerun['cases'].items():
        if result!=json.loads((run/name/'checker-output.json').read_text()):raise ValueError('Per-batch checker output differs')
    verify_replay_freeze(run/'freeze.json')
    result={'pass':True,'batches_checked':len(records),'source_points_per_batch':len(original['counter_identities']),
        'simulator_executions_in_replay':42,'executed_cycles_in_replay':cycles,'new_simulations_in_audit':0,'new_model_calls_in_audit':0,
        'fresh_checker_batches_checked':len(rerun['cases']),'original_evidence_preserved':True,
        'old_repeated_diagnostics':len(correspondence),'old_final_diagnostics':sum(x['batch']=='round6' for x in correspondence),
        'old_alarm_mapping':'Every instance uniquely maps by cycle and slave to an explicit unresolved post_abort_forward; original verdicts remain unchanged.',
        'finals':finals,'checker_sha256':sha(ROOT/f['candidate']/'checker.py'),'freeze_sha256':sha(run/'freeze.json'),
        'source_sha256':sha(Path(__file__))}
    output.mkdir(parents=True,exist_ok=False)
    (output/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'diagnostic-correspondence.json').write_text(json.dumps(correspondence,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='finals'},indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();audit(a.run.resolve(),a.output.resolve())
