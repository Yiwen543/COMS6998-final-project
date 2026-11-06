"""API-free postprocessing of the already launched, USD20-authorized live run.

All outputs are new directories. This deliberately refuses to overwrite stages.
It never starts generation, modifies candidates, or supplies hidden feedback.
"""
import json
from pathlib import Path
import sys
import time
from common import ROOT, BASE, dump, run
from controller_release_live import verify_release


def main():
    live=BASE/'results/controller-done-live-v2'
    out=BASE/'results/controller-done-live-post-v2';out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic(); stages=[]
    dump(out/'progress.json',dict(status='WAITING_FOR_ALL36_RELEASE',stages=stages,API_calls=0))
    while not (live/'summary.json').exists():
        log=Path(str(live)+'.stdout.log')
        if log.exists() and 'Traceback (most recent call last):' in log.read_text():
            raise ValueError('Live process failed; preserve it and diagnose, never restart automatically')
        if time.monotonic()-start>3600:raise TimeoutError('No complete live summary; inspect current run')
        time.sleep(2)
    verify_release(live)
    python=sys.executable; script=BASE/'scripts'; results=BASE/'results'
    replay=results/'controller-done-live-replay-v2'; scores=results/'controller-done-live-grade-v2'
    replay_scores=results/'controller-done-live-replay-grade-v2'; formal=results/'controller-done-live-formal-v2'
    audit=results/'controller-done-live-acceptance-v2'
    commands=[
        ('saved-response-replay',1200,[python,'-B',str(script/'controller_done_generate_v2.py'),'--mode','replay','--replay-source',str(live),'--output',str(replay)]),
        ('fresh-independent-grade',1200,[python,'-B',str(script/'controller_done_grade_v4.py'),'--run',str(live),'--output',str(scores)]),
        ('fresh-replay-grade',1200,[python,'-B',str(script/'controller_done_grade_v4.py'),'--run',str(replay),'--output',str(replay_scores)]),
        ('fixed-formal-schedule',5000,[python,'-B',str(script/'controller_done_formal_v3.py'),'--run',str(live),'--qualification',str(results/'controller-done-formal-controls-v4'),'--output',str(formal)]),
        ('raw-evidence-audit',1200,[python,'-B',str(script/'controller_done_live_audit_v2.py'),'--run',str(live),'--replay',str(replay),'--scores',str(scores),'--replay-scores',str(replay_scores),'--formal',str(formal),'--output',str(audit)])]
    for name,timeout,argv in commands:
        dump(out/'progress.json',dict(status='RUNNING',active_stage=name,command=argv,stages=stages,API_calls=0))
        print('post-stage-start',name,flush=True)
        result=run(argv,out/(name+'.log'),timeout)
        stages.append(dict(name=name,**result));dump(out/'progress.json',dict(status='RUNNING' if result['status']=='complete' else 'FAILED_PRESERVED',stages=stages,API_calls=0))
        print('post-stage-end',name,result['status'],flush=True)
        if result['status']!='complete':raise ValueError('Postprocessing failed: '+name+'; inspect saved log')
    dump(out/'summary.json',dict(status='POSTPROCESSING_VERIFIED_WITH_LIMITS',stages=stages,wall_seconds=time.monotonic()-start,API_calls=0))


if __name__=='__main__':main()
