"""Rescore sealed raw replays using new registered attribution rules; no simulations."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK
from controller_done_loop_v2 import verify_data
from controller_release_live import verify_release
from controller_done_adjudication_v3 import adjudicate

REG=BASE/'configs/controller_done_scoring_v3.json'


def load(p):return json.loads(p.read_text())


def execute(run_root,original_run,source_scores,out):
    rounds=verify_release(run_root);old=verify_release(original_run);verify_data()
    out.mkdir(parents=True,exist_ok=False);labels=load(TASK/'measurements-v1/summary.json')['records']
    lookup={(r['source'],r['simulator'],r.get('trace')):r for r in labels};saved=load(source_scores/'scores.json');results=[];logs=0
    for row in saved['rounds']:
        key=(row['arm'],row['repetition'],row['round']);s=next(s for s in rounds if (s['arm'],s['repetition'],s['round'])==key);o=next(s for s in old if (s['arm'],s['repetition'],s['round'])==key)
        if sha(run_root/s['directory']/'compiled/candidate.sv')!=sha(original_run/o['directory']/'compiled/candidate.sv'):raise ValueError('Frozen program changed; replay reuse prohibited')
        cases=[]
        for case in row['cases']:
            label=lookup[case['source'],case['simulator'],case['trace']];p=source_scores/case['result_path']
            if sha(p)!=case['result_sha256']:raise ValueError('Original result changed')
            result=load(p);raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes())
            if hashlib.sha256(raw).hexdigest()!=result['raw_log_sha256']:raise ValueError('Original raw replay changed')
            cases.append(dict(source=case['source'],simulator=case['simulator'],trace=case['trace'],**adjudicate(label,result),
                original_result_path=str(p.relative_to(ROOT)),original_result_sha256=sha(p),original_raw_log_sha256=result['raw_log_sha256']));logs+=1
        correct=[c for c in cases if c['source']=='correct'];gate=len(correct)==18 and all(c['complete'] and c['oracle_verdict']=='PASS' and not c['candidate_alarm_samples'] and not c['candidate_unknown_samples'] for c in correct)
        categories={}
        for category in ('safety','response_completion','input_completion'):
            eligible=[c for c in cases if c['source']!='correct' and c['eligible'][category]]
            detected=[c for c in eligible if gate and c['definite_detection'][category]];resolved=[c for c in eligible if gate and c['fully_resolved_detection'][category]]
            categories[category]=dict(eligible_pairs=len(eligible),definite_pairs=len(detected),fully_resolved_pairs=len(resolved),
                definite_types=sorted({c['source'] for c in detected}),fully_resolved_types=sorted({c['source'] for c in resolved}),
                oracle_unknown_pairs=sum(bool(c['oracle_unknown_records']) for c in eligible))
        results.append(dict(arm=row['arm'],repetition=row['repetition'],round=row['round'],correct_control_gate=gate,categories=categories,
            marker_only_safety_signal_pairs=sum(c['marker_only_safety_signal'] for c in cases),
            unknown_pairs=sum(bool(c['oracle_unknown_records']) for c in cases),raw_fault_types=12,raw_fault_pairs=144,
            attribution='Case-level detection strata only, no slot/category causal attribution',cost=row['cost'],cases=cases))
    by_type={}
    for name in sorted({r['source'] for r in labels if r['source']!='correct'}):
        values=[r for r in labels if r['source']==name]
        by_type[name]=dict(raw_pairs=len(values),verdicts=dict(Counter(r.get('verdict','UNKNOWN') for r in values)),
            oracle_unknown_pairs=sum(bool(r.get('unknown_records')) for r in values),
            fully_resolved_FAIL_pairs=sum(r.get('verdict')=='FAIL' and not r.get('unknown_records') for r in values))
    final=load(run_root/'final-candidates.json')['candidates'];endpoints=[{k:v for k,v in r.items() if k!='cases'} for r in results if any((r['arm'],r['repetition'],r['round'])==(f['arm'],f['repetition'],f['selected_round']) for f in final)]
    summary=dict(status='OFFLINE_RESCORED_WITH_SCOPE',rounds=results,selected_endpoints=endpoints,oracle_unknown_by_type=by_type,
        verified_reused_raw_logs=logs,new_monitor_replays=0,new_DUT_simulations=0,new_formal_jobs=0,API_calls=0,
        actual_model_tokens=None,not_new_LLM_evidence=True,registration_sha256=sha(REG),source_score_sha256=sha(source_scores/'scores.json'),
        current_release_sha256=sha(run_root/'release.json'),original_release_sha256=sha(original_run/'release.json'),
        old_scores_overwritten=False,formal_or_completion_proof=False)
    dump(out/'scores.json',summary);return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['mock','replay'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=BASE/'results'
    x=execute(r/f'controller-done-{a.mode}-v2',r/f'controller-done-{a.mode}-v1',r/f'controller-done-score-{a.mode}-v1',a.output.resolve());print(x['status'],x['verified_reused_raw_logs'])
