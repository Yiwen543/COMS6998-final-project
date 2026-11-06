"""Read-only independent comparison and old-evidence checks for the shared grader."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_loop_v2 import verify_data
from controller_release_live import verify_release


def load(p):return json.loads(p.read_text())


def audit(out):
    verify_data();r=BASE/'results';a=load(r/'controller-done-grade-v4-fresh/scores.json');b=load(r/'controller-done-grade-v4-reuse/scores.json')
    verify_release(r/'controller-done-mock-v2');verify_release(r/'controller-done-replay-v2');checks={};logs=0;cycles=0
    if len(a['rounds'])!=36 or len(b['rounds'])!=36:raise ValueError('Incomplete all-round grading')
    for x,y in zip(a['rounds'],b['rounds']):
        if {k:v for k,v in x.items() if k!='cases'}!={k:v for k,v in y.items() if k!='cases'} or len(x['cases'])!=162 or len(y['cases'])!=162:raise ValueError('Round metrics/inventory differ')
        for c,d in zip(x['cases'],y['cases']):
            omit=('evidence_provenance','original_status')
            if {k:v for k,v in c.items() if k not in omit}!={k:v for k,v in d.items() if k not in omit}:raise ValueError('Case classification differs')
            for case in (c,d):
                p=ROOT/case['evidence_provenance']['result_path'];result=load(p);raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes())
                if sha(p)!=case['evidence_provenance']['result_sha256'] or hashlib.sha256(raw).hexdigest()!=result['raw_log_sha256']:raise ValueError('Original raw evidence changed')
                if case is c:logs+=1;cycles+=result['cycles']
    checks['all36_all5832_cases_fresh_reuse_metrics_equal']=True;checks['all162_cases_each_round_retained']=True
    if a['oracle_unknown_by_type']!=b['oracle_unknown_by_type']:raise ValueError('Unknown by-type drift')
    if sum(v['FAIL_with_oracle_unknown_pairs'] for v in a['oracle_unknown_by_type'].values())!=38:raise ValueError('Oracle unknown context omitted')
    checks['explicit_FAIL_with_unknown_both_paths']=True
    for n,h in load(REG)['preserve_old_freezes'].items():
        p=ROOT/n;f=load(p)
        if sha(p)!=h or any(sha(ROOT/k)!=v for k,v in f.get('files',f.get('artifact_sha256',{})).items()):raise ValueError('Old frozen member changed')
    old=load(r/'controller-done-acceptance-v4/acceptance.json')
    for n,h in {**old['old_scores'],**old['evidence_sha256']}.items():
        if sha(ROOT/n)!=h:raise ValueError('Old score/source/evidence changed')
    checks['old_freezes_scores_negative_evidence_preserved']=True
    counts=load(r/'controller-done-preflight-v2/counts/summary.json')
    if counts['status']!='passed' or any(not c['within_cap'] for c in counts['counts']):raise ValueError('Actual token gate did not pass')
    from controller_done_loop_v2 import count_messages
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        for arm,kind,messages in count_messages():
            p=Path(temp)/'prompt.json';dump(p,messages);rec=next(c for c in counts['counts'] if (c['arm'],c['kind'])==(arm,kind))
            if sha(p)!=rec['prompt_sha256']:raise ValueError('Candidate prompt changed since actual count')
    checks['actual_provider_counts_still_valid_no_recount']=True
    source=BASE/'configs/controller_done_scoring_v4.json';reg=load(source)
    for n,h in reg['code_sha256'].items():
        if sha(BASE/'scripts'/n)!=h:raise ValueError('Registered new grading source changed')
    log=r/'controller-done-grade-v4-tests-v2.log';text=log.read_text()
    if 'Ran 9 tests' not in text or not text.rstrip().endswith('OK'):raise ValueError('Failure injection tests failed')
    checks['nine_failure_injection_tests_passed']=True
    files=[source,r/'controller-done-grade-v4-fresh/scores.json',r/'controller-done-grade-v4-reuse/scores.json',log,r/'controller-done-review-v3/review.json',r/'controller-done-review-v3/metadata.json',TASK/'reference/scope-v4/manifest.json',TASK/'qualification/api-shared-grading-review-v4/proposal.json']
    result=dict(status='OFFLINE_SHARED_GRADING_VERIFIED_FRESH_REVIEW_PENDING',checks=checks,verified_fresh_logs=logs,verified_fresh_cycles=cycles,
        full_unknown_by_type=a['oracle_unknown_by_type'],fresh_costs=a['costs'],reuse_costs=b['costs'],new_API_calls=0,oracle_changed=False,
        actual_candidate_generations=0,original_LLM_scores_unchanged=True,independent_review='LIMITED_SCOPE_REPAIRED_NOT_YET_REVIEWED',
        evidence_sha256={str(p.relative_to(ROOT)):sha(p) for p in files},producer_sha256=sha(__file__))
    dump(out,result);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(audit(a.output.resolve())['status'])
