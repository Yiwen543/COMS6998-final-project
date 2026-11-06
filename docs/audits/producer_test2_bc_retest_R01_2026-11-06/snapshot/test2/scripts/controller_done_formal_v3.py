"""Registered short safety projection, with full-depth infrastructure controls."""
import argparse
import json
from pathlib import Path
import time
from common import ROOT,dump,run,sha
from controller_done_data import TASK,REG,SOURCES
from controller_done_loop import plumbing,verify_data
from controller_done_runtime import compile_monitor,build_replay
from controller_monitor_live import formal_harness
from controller_done_witness_v3 import adjudicate
from controller_release_live import verify_release,ARMS


def harness(slot,variant='cone'):
    if variant not in ('cone','retained'):raise ValueError('Unknown profile')
    text=formal_harness(slot).replace('(* anyseq *)','(* anyseq, keep *)')
    if variant=='cone':text=text.replace('(* keep *) wire','wire')
    return text.replace('candidate_monitor monitor(.*);',"wire trace_done=1'b0;\ncandidate_monitor monitor(.*);")


def job(candidate,source,out,slot,mode,timeout,variant='cone'):
    out.mkdir(parents=True,exist_ok=False);(out/'harness.sv').write_text(harness(slot,variant))
    sources=[source]+SOURCES[1:];files='dut.v '+str(sources[0])+'\n'+'\n'.join(str(p) for p in sources[1:])
    files+='\ncandidate.sv '+str(candidate/'candidate.sv')+'\nharness.sv '+str(out/'harness.sv')
    (out/'job.sby').write_text(f'''[options]
mode {mode}
depth 24
timeout {timeout}
[engines]
smtbmc z3
[script]
read -formal -sv dut.v axis_fifo.v axis_frame_length_adjust_fifo.v task_top_v3.sv candidate.sv harness.sv
prep -top formal_top -flatten
[files]
{files}
''')
    r=run(['sby','-d',out/'work',out/'job.sby'],out/'sby.log',timeout+5);status=out/'work/status'
    r.update(status=status.read_text().split()[0] if status.exists() else 'TIMEOUT' if r['status']=='timeout' else 'ERROR',
             mode=mode,slot=slot,depth=24,variant=variant,solver_cap_seconds=timeout,trace_done=0,scope='safety_projection',finite_completion_proved=False)
    dump(out/'result.json',r);return r


def controls(out):
    verify_data();out.mkdir(parents=True,exist_ok=False);started=time.monotonic();records=[]
    for name,n in [('true',3),('false',1),('end_only',6)]:
        candidate=out/'candidates'/name;c=compile_monitor(plumbing(n),candidate)
        if c['status']!='complete':raise ValueError('Control compile failed')
        if build_replay(candidate)['status']!='complete':raise ValueError('Control replay compile failed')
        for variant in (('cone','retained') if name!='end_only' else ('cone',)):
            mode='cover' if name=='end_only' else 'bmc';d=out/'jobs'/name/variant;r=job(candidate,SOURCES[0],d,0,mode,10,variant)
            row=dict(r,name=name)
            if name=='false' and r['status']=='FAIL':row['witness']=adjudicate(d,candidate,SOURCES[0],0,d/'physical',out/'physical-cache')
            records.append(row);dump(out/'progress.json',records);print('formal-control',name,variant,r['status'],flush=True)
    # Public specification property; candidate is an infrastructure control, not a model trial.
    cand=plumbing(3);cand['body']="assign active={5'b00000,(h_valid && !rst)};assign ok={5'b11111,(!h_pad || h_length==16'd4)};"
    candidate=out/'candidates'/'pad_length';compile_monitor(cand,candidate);build_replay(candidate)
    for name,source in [('correct',SOURCES[0]),('mutant',TASK/'private/mutants/N05.v')]:
        d=out/'jobs'/'pad_length'/name;r=job(candidate,source,d,0,'bmc',10)
        row=dict(name='pad_length_'+name,**r)
        if r['status']=='FAIL':row['witness']=adjudicate(d,candidate,source,0,d/'physical',out/'physical-cache')
        records.append(row);dump(out/'progress.json',records);print('formal-control',row['name'],r['status'],flush=True)
    def get(n,v='cone'):return next(r for r in records if r['name']==n and r.get('variant')==v)
    gates=dict(full_depth_true=get('true')['status']=='PASS',full_depth_false=get('false')['status']=='FAIL',
        false_control_reference_prefix_PASS=get('false').get('witness',{}).get('reference_verdict')=='PASS',
        marker_only_unreached=get('end_only')['status']=='FAIL',
        physical_mutant_prefix_FAIL_unattributed_alarm=get('pad_length_mutant').get('witness',{}).get('reference_verdict')=='FAIL' and get('pad_length_mutant').get('witness',{}).get('formal_alarm_reproduced',False))
    result=dict(status='passed' if all(gates.values()) else 'qualification_failed',gates=gates,jobs=records,wall_seconds=time.monotonic()-started,
                profile_selection='cone fixed before candidate outcomes; controls only',API_calls=0,trace_done=0,finite_completion_proved=False,registration_sha256=sha(REG),producer_sha256=sha(__file__))
    dump(out/'summary.json',result);return result


def finals(run_root,qualification,out):
    verify_release(run_root);verify_data()
    q=json.loads((qualification/'summary.json').read_text())
    if q['status']!='passed':raise ValueError('Infrastructure controls failed')
    out.mkdir(parents=True,exist_ok=False);selected=json.loads((run_root/'final-candidates.json').read_text())['candidates'];reg=json.loads(REG.read_text());records=[];elapsed={};start=time.monotonic()
    faults=json.loads((TASK/'private/mutant-catalog.json').read_text())['faults']
    # Registered paired order, independent of arm outcomes. Global wall cap per final is enforced before every job.
    for rep in (1,2,3):
        for fault in [None]+faults:
            for slot in range(6):
                for mode in (('bmc','prove','cover') if fault is None else ('bmc',)):
                    for arm in (ARMS if (rep+slot)%2 else tuple(reversed(ARMS))):
                        f=next(f for f in selected if (f['arm'],f['repetition'])==(arm,rep));key=(arm,rep);elapsed.setdefault(key,0.)
                        timeout=reg['formal']['correct_timeout' if fault is None else 'mutant_timeout'];tag='correct' if fault is None else fault['id']
                        meta=dict(arm=arm,repetition=rep,source=tag,slot=slot,mode=mode)
                        if not f['directory']:row=dict(meta,status='INVALID_CANDIDATE')
                        elif elapsed[key]+timeout+5>reg['formal']['overall_seconds_per_final']:row=dict(meta,status='NOT_RUN_TOTAL_CAP')
                        else:
                            t=time.monotonic();d=out/arm/f'rep{rep}'/tag/f'P{slot}-{mode}';source=SOURCES[0] if fault is None else ROOT/fault['source']
                            r=job(run_root/f['directory'],source,d,slot,mode,timeout);row={**r,**meta}
                            if mode=='bmc' and r['status']=='FAIL':
                                deadline=t+reg['formal']['overall_seconds_per_final']-elapsed[key]
                                row['witness']=adjudicate(d,run_root/f['directory'],source,slot,d/'physical',out/'physical-cache',deadline=deadline)
                            elapsed[key]+=time.monotonic()-t
                        records.append(row);dump(out/'progress.json',records)
    result=dict(jobs=records,wall_seconds=time.monotonic()-start,elapsed_per_final={f'{a}/{r}':s for (a,r),s in elapsed.items()},API_calls=0,
                scope='trace_done0 safety projection only',finite_completion_proved=False,qualification_sha256=sha(qualification/'summary.json'),release_sha256=sha(run_root/'release.json'))
    dump(out/'summary.json',result);verify_release(run_root);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--controls',action='store_true');p.add_argument('--output',type=Path,required=True);p.add_argument('--run',type=Path);p.add_argument('--qualification',type=Path);a=p.parse_args()
    if a.controls:controls(a.output.resolve())
    else:finals(a.run.resolve(),a.qualification.resolve(),a.output.resolve())
