"""One stage PGID,one parent deadline;no ps or general scheduler."""
from pathlib import Path
import json,os,signal,subprocess,time
from resources import Halt,require,sha

def child(argv,log,timeout,window,env,clock=time.monotonic,sleep=time.sleep,popen=None):
    """All children inherit the supervised stage PGID;timeout aborts stage."""
    popen=popen or subprocess.Popen
    log=Path(log);log.parent.mkdir(parents=True,exist_ok=True);start=clock();limit=min(timeout,window.work-start);require(limit>0.05,'NO_CHILD_DISPATCH_WINDOW')
    deadline=start+limit;proc=None
    with log.open('xb') as output:
        proc=popen([str(x) for x in argv],stdout=output,stderr=subprocess.STDOUT,env=env,start_new_session=False)
        while proc.poll() is None and clock()<deadline:sleep(min(0.01,max(0,deadline-clock())))
        timed_out=proc.poll() is None
        if timed_out:
            proc.kill()  # parent will clean the entire stage PGID after worker exits
            try:proc.wait(timeout=max(0.001,min(0.1,window.hard-clock())))
            except subprocess.TimeoutExpired:pass
        else:proc.wait(timeout=max(0.001,min(0.1,window.hard-clock())))
    result=dict(argv=[str(x) for x in argv],returncode=proc.returncode,status='timeout' if timed_out else ('complete' if proc.returncode==0 else 'error'),seconds=clock()-start,log_sha256=sha(log),absolute_deadline=deadline,stage_pgid_inherited=True)
    (log.parent/(log.name+'.process.json')).write_text(json.dumps(result,indent=2)+'\n')
    require(not timed_out,'CHILD_TIMEOUT_REQUIRES_STAGE_HALT');require(clock()<window.work,'WORK_DEADLINE_AFTER_CHILD');return result

def owned_stage(argv,root,reg,window,env,clock=time.monotonic,sleep=time.sleep,popen=None,killpg=os.killpg):
    """Parent owns the sole new PGID;API/local children inherit it,including cleanup."""
    popen=popen or subprocess.Popen
    root=Path(root);stop=window.hard-5;proc=None;errors=[];expired=False;cleanup=[]
    with (root/'stage.stdout.log').open('xb') as out,(root/'stage.stderr.log').open('xb') as err:
        proc=popen([str(x) for x in argv],stdout=out,stderr=err,env=env,start_new_session=True)
        while proc.poll() is None and clock()<stop:sleep(min(0.02,max(0,stop-clock())))
        expired=proc.poll() is None
        if not expired:proc.wait(timeout=max(0.001,min(0.2,window.hard-clock())))
        try:
            killpg(proc.pid,0)
            killpg(proc.pid,signal.SIGTERM);cleanup.append('SIGTERM_OWNED_STAGE_GROUP')
            until=min(clock()+0.25,window.hard-1)
            while clock()<until:
                try:killpg(proc.pid,0)
                except ProcessLookupError:break
                sleep(min(0.01,max(0,until-clock())))
            try:killpg(proc.pid,signal.SIGKILL);cleanup.append('SIGKILL_OWNED_STAGE_GROUP')
            except ProcessLookupError:pass
        except ProcessLookupError:pass
        except OSError as error:errors.append(type(error).__name__)
        try:proc.wait(timeout=max(0.001,min(0.2,window.hard-clock())))
        except subprocess.TimeoutExpired:errors.append('OWNED_ROOT_WAIT_UNRESOLVED')
    result=dict(returncode=proc.returncode,deadline_forced_stop=expired,cleanup=cleanup,mandatory_errors=errors,elapsed_seconds=window.elapsed(),within_total_wall=clock()<=window.hard,child_inventory_complete=False,scope='Owned stage PGID only;not an OS/filesystem hard-realtime or adversarial detached-child proof.')
    (root/'parent-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
