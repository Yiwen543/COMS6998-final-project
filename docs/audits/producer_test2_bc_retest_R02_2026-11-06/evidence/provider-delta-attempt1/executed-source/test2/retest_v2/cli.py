"""Single new-stage parent/worker entry;no automatic live operation."""
from pathlib import Path
import argparse,json,sys,time,os,uuid
from resources import Window,Halt,require,financial_policy,sha
from gates import authorize
from supervision import owned_stage
from pipeline import ROOT,load,dump,clean_env,execute_stage
from release import freeze,release,ARMS

REG=ROOT/'test2/configs/controller_done_bc_retest_v2.json'

def preserve_missing(out,reg,reason):
    """Bounded metadata recovery after worker death;never recompiles or scores."""
    out=Path(out)
    if not (out/'run.json').exists():return
    run=load(out/'run.json');snapshots=[]
    if (out/'release.json').exists():return
    for arm,number in reg['schedule']:
        d=out/arm/'rep1'/f'round{number}';d.mkdir(parents=True,exist_ok=True)
        if (d/'snapshot.json').exists():snapshots.append(dict(snapshot=str((d/'snapshot.json').relative_to(out)),sha256=sha(d/'snapshot.json')))
        else:
            dump(d/'termination.json',dict(status='NOT_RUN_OR_PARTIAL_AFTER_TERMINATION',reason=reason,score=None))
            ctx=dict(mode=run['mode'],arm=arm,repetition=1,round=number,session_id=run['session_ids'][arm])
            snapshots.append(freeze(out,d,ctx,'NOT_RUN_OR_PARTIAL_AFTER_TERMINATION'))
    if not (out/'calls.jsonl').exists():(out/'calls.jsonl').touch()
    release(out,snapshots,run['mode'],reg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['live','mock','replay'],required=True);p.add_argument('--output',required=True,type=Path);p.add_argument('--execute',type=Path);p.add_argument('--replay-source',type=Path);p.add_argument('--worker',action='store_true');p.add_argument('--start',type=float);p.add_argument('--lease',type=Path);p.add_argument('--lease-sha');a=p.parse_args();reg=load(REG)
    start=a.start if a.worker else time.monotonic();window=Window(start,reg);out=a.output.resolve()
    if a.mode=='live':require(a.execute is not None,'EXACT_EXECUTE_REQUIRED');_,pricing=authorize(ROOT,reg,a.execute)
    else:pricing=financial_policy(ROOT,reg)
    if a.worker:
        require(a.lease is not None and sha(a.lease)==a.lease_sha,'WORKER_LEASE_REQUIRED')
        lease=load(a.lease);require(lease['start']==start and lease['out']==str(out) and lease['mode']==a.mode and lease['supervisor_pid']==os.getppid() and os.getpgrp()==os.getpid(),'WORKER_LEASE_OWNER_OR_CLOCK')
        require(0<=time.monotonic()-start<reg['wall']['stop_work_seconds'],'WORKER_LEASE_EXPIRED');window.lease_path=a.lease.resolve()
        try:return execute_stage(out,a.mode,reg,window,pricing,a.execute,a.replay_source)
        except (Halt,Exception) as error:
            if out.exists():dump(out/'worker-error.json',dict(status='ERROR_PRESERVED',error_type=type(error).__name__,reason=str(error)[:300],new_requests_allowed=False))
            raise
    require(not out.exists(),'RUN_ALREADY_EXISTS_NO_RESTART');control=out.parent/(out.name+'-supervision');control.mkdir(parents=True,exist_ok=False)
    env=clean_env(control);(control/'tmp').mkdir();lease=control/'worker-lease.json';dump(lease,dict(start=start,out=str(out),mode=a.mode,supervisor_pid=os.getpid(),nonce=uuid.uuid4().hex,execute_sha256=sha(a.execute) if a.execute else None))
    argv=[sys.executable,'-B',str(Path(__file__).resolve()),'--worker','--start',repr(start),'--mode',a.mode,'--output',str(out),'--lease',str(lease.resolve()),'--lease-sha',sha(lease)]
    if a.execute:argv+=['--execute',str(a.execute.resolve())]
    if a.replay_source:argv+=['--replay-source',str(a.replay_source.resolve())]
    result=owned_stage(argv,control,reg,window,env)
    if result['returncode']!=0 or result['deadline_forced_stop'] or result['mandatory_errors']:
        if window.clock()<window.hard-1:preserve_missing(out,reg,'PARENT_TERMINATION_OR_ERROR')
        dump(control/'final-status.json',dict(status='INCOMPLETE_PRESERVED',parent=result,remaining_outputs_unknown=True,planned_rounds=6,planned_case_pairs=972,unwritten_cases_remain_unresolved=True,within_total_wall=window.clock()<=window.hard));returncode=1
    else:
        require((out/'summary.json').is_file(),'WORKER_SUMMARY_MISSING');summary=load(out/'summary.json');returncode=0 if summary['status']=='COMPLETE_WITH_UNRESOLVED_RETAINED' else 1
    require(window.clock()<=window.hard,'TOTAL_WALL_LIMIT_EXCEEDED');return returncode

if __name__=='__main__':
    value=main()
    if isinstance(value,int):raise SystemExit(value)
