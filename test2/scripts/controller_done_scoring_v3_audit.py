"""Read-only acceptance of repaired scoring, actual counts and scoped witnesses."""
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
    verify_data();r=BASE/'results';fresh=r/'controller-done-score-v3-fresh-mock';old=r/'controller-done-score-mock-v1'
    verify_release(r/'controller-done-mock-v2');verify_release(r/'controller-done-replay-v2')
    a=load(fresh/'scores.json');b=load(r/'controller-done-rescore-v3-mock/scores.json');c=load(r/'controller-done-rescore-v3-replay/scores.json');past=load(old/'scores.json')
    if len(a['rounds'])!=36 or b['selected_endpoints']!=c['selected_endpoints']:raise ValueError('All-round score alignment failed')
    logs=0;cycles=0
    for new,reused,previous in zip(a['rounds'],b['rounds'],past['rounds']):
        key=lambda x:(x['arm'],x['repetition'],x['round'])
        if key(new)!=key(reused) or key(new)!=key(previous) or len(new['cases'])!=162:raise ValueError('Missing round/case')
        for cat in reused['categories']:
            if reused['categories'][cat]['definite_pairs']!=new['categories'][cat]['definite_detected_pairs'] or reused['categories'][cat]['fully_resolved_pairs']!=new['categories'][cat]['fully_resolved_detected_pairs']:raise ValueError('Fresh/reused grading differs')
        for newcase,oldcase in zip(new['cases'],previous['cases']):
            if (newcase['source'],newcase['simulator'],newcase['trace'])!=(oldcase['source'],oldcase['simulator'],oldcase['trace']):raise ValueError('Case order changed')
            p=fresh/newcase['result_path'];q=old/oldcase['result_path']
            if sha(p)!=newcase['result_sha256'] or sha(q)!=oldcase['result_sha256']:raise ValueError('Replay result changed')
            x,y=load(p),load(q);raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes());original=gzip.decompress((q.parent/'replay.log.gz').read_bytes())
            if hashlib.sha256(raw).hexdigest()!=x['raw_log_sha256'] or sha(p.parent/'replay.log.gz')!=x['compressed_log_sha256']:raise ValueError('Fresh raw replay hash failed')
            if raw.replace(str(r/'controller-done-mock-v2').encode(),b'RUN_ROOT')!=original.replace(str(r/'controller-done-mock-v1').encode(),b'RUN_ROOT'):raise ValueError('Raw bits/samples differ beyond exact compiled-root prefix')
            if x['properties']!=y['properties'] or x['cycles']!=y['cycles'] or x['rows_sha256']!=y['rows_sha256']:raise ValueError('Physical/candidate observations differ')
            vector=x['rows_sha256']+'.hex'
            if (fresh/'row-cache'/vector).read_bytes()!=(old/'row-cache'/vector).read_bytes():raise ValueError('Replay input transport differs')
            logs+=1;cycles+=x['cycles']
    q=load(r/'controller-done-formal-controls-v4/summary.json')
    if q['status']!='passed':raise ValueError('New prefix/witness controls failed')
    for j in q['jobs']:
        w=j.get('witness')
        if w and (w['reference_confirmed_selected_alarm'] or w['candidate_false_alarm_claim'] or not w['formal_alarm_reproduced']):raise ValueError('Witness conclusion overstates reference scope')
        if w and ('reference_failures' not in w or 'reference_unknown' not in w):raise ValueError('Reference diagnostic omitted')
    count=load(r/'controller-done-preflight-v2/counts/summary.json')
    if count['status']!='passed' or len(count['counts'])!=4 or any(not x['within_cap'] for x in count['counts']):raise ValueError('Actual provider count gate failed')
    old_accept=load(r/'controller-done-acceptance-v4/acceptance.json')
    for n,h in old_accept['evidence_sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Old offline evidence changed')
    for n,h in old_accept['old_scores'].items():
        if sha(ROOT/n)!=h:raise ValueError('Old score changed')
    for n,h in load(REG)['preserve_old_freezes'].items():
        p=ROOT/n;f=load(p)
        if sha(p)!=h or any(sha(ROOT/name)!=value for name,value in f.get('files',f.get('artifact_sha256',{})).items()):raise ValueError('Old freeze changed')
    files=[fresh/'scores.json',r/'controller-done-rescore-v3-mock/scores.json',r/'controller-done-rescore-v3-replay/scores.json',r/'controller-done-formal-controls-v4/summary.json',r/'controller-done-preflight-v2/counts/summary.json',r/'controller-done-preflight-v2/review/review.json',BASE/'configs/controller_done_scoring_v3.json',TASK/'reference/scope-v3/manifest.json',TASK/'qualification/api-adapter-review-v3/proposal.json']
    for n,expected in [(6,'controller-done-scoring-v3-tests.log'),(2,'controller-done-review-v3-unit.log')]:
        p=r/expected;text=p.read_text()
        if f'Ran {n} tests' not in text or not text.rstrip().endswith('OK'):raise ValueError('New scoped tests failed')
        files.append(p)
    result=dict(status='OFFLINE_REPAIR_ACCEPTED_FRESH_CLAUDE_REVIEW_PENDING',verified_fresh_logs=logs,verified_fresh_cycles=cycles,
        grading_new_replays=5832,scoring_registration_sha256=sha(BASE/'configs/controller_done_scoring_v3.json'),ordinary_safety_excludes_marker=True,finite_any_slot_attribution='UNATTRIBUTED',
        reference_prefix_never_selected_alarm_confirmation=True,oracle_unchanged=True,old_scores_and_timeouts_preserved=True,actual_count_gate='PASS',review_gate='LIMITED_SCOPE_REPAIRED_NOT_YET_REVIEWED',
        extra_paid_calls=0,unknown_by_type=b['oracle_unknown_by_type'],formal_statuses=[j['status'] for j in q['jobs']],
        files_sha256={str(p.relative_to(ROOT)):sha(p) for p in files},producer_sha256=sha(__file__))
    dump(out,result);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();x=audit(a.output.resolve());print(x['status'],x['verified_fresh_logs'])
