"""New API-free formal profile; old frozen monitor/harness/results stay unchanged."""
import json
from pathlib import Path
import time
from common import ROOT,BASE,dump,run,sha
from controller_monitor_live import TASK,formal_harness,compile_monitor,build_replay
from controller_loop_live import plumbing
from controller_physical_witness import adjudicate
from controller_release_live import verify_release

REG=BASE/'configs/controller_offline_qualification_v1.json'


def harness(slot,variant):
    if variant not in ('retained','cone'):raise ValueError('Unknown profile')
    text=formal_harness(slot).replace('(* anyseq *)','(* anyseq, keep *)')
    if variant=='cone':text=text.replace('(* keep *) wire','wire')
    return text


def job(candidate,source,out,slot,mode,timeout,variant):
    out.mkdir(parents=True,exist_ok=False);(out/'harness.sv').write_text(harness(slot,variant))
    sources=[source,TASK/'public/rtl/axis_fifo.v',TASK/'public/rtl/axis_frame_length_adjust_fifo.v',TASK/'public/task_top_v3.sv']
    files='dut.v '+str(sources[0])+'\n'+'\n'.join(str(p) for p in sources[1:])
    files+='\ncandidate.sv '+str(candidate/'candidate.sv')+'\nharness.sv '+str(out/'harness.sv')
    text=f'''[options]
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
'''
    (out/'job.sby').write_text(text);r=run(['sby','-d',out/'work',out/'job.sby'],out/'sby.log',timeout+5)
    native=out/'work/status';r.update(status=native.read_text().split()[0] if native.exists() else 'TIMEOUT' if r['status']=='timeout' else 'ERROR',
                                     mode=mode,slot=slot,depth=24,variant=variant,solver_cap_seconds=timeout)
    smt=out/'work/model/design_smt2.smt2';r['smt2_bytes']=smt.stat().st_size if smt.exists() else None
    dump(out/'result.json',r);return r


def calibration(run_root,out):
    reg=json.loads(REG.read_text());verify_release(run_root)
    out.mkdir(parents=True,exist_ok=False)
    dump(out/'registration.json',reg)
    (out/'producer.py').write_bytes(Path(__file__).read_bytes())
    started=time.monotonic();jobs=[];source=TASK/'public/rtl/axis_frame_length_adjust.v'
    controls={}
    for name,n in [('always_true',3),('always_false',1)]:
        d=out/'controls'/name;compile_monitor(plumbing(n),d);build_replay(d);controls[name]=d
    # Both profiles use identical logic/assumptions; output retention is the only variant.
    for name,variants in [('always_true',('retained','cone')),('always_false',('cone','retained'))]:
        for variant in variants:
            d=out/'jobs'/name/variant;r=job(controls[name],source,d,0,'bmc',5,variant)
            rec=dict(name=name,variant=variant,slot=0,mode='bmc',status=r['status'],seconds=r['seconds'],smt2_bytes=r['smt2_bytes'],directory=str(d.relative_to(out)))
            if name=='always_false' and r['status']=='FAIL':
                rec['witness']=adjudicate(d,controls[name],source,0,d/'physical-witness',out/'physical-build-cache')
            jobs.append(rec);dump(out/'progress.json',dict(jobs=jobs));print('calibration',name,variant,r['status'],flush=True)
    gate=all(next(j['status'] for j in jobs if j['name']==name and j['variant']=='cone')==expected for name,expected in [('always_true','PASS'),('always_false','FAIL')])
    gate &= all(j.get('witness',{}).get('reference_verdict')=='PASS' and j['witness'].get('formal_alarm_reproduced') for j in jobs if j['name']=='always_false')
    if gate:
        for p in reg['formal']['probes']:
            candidate=run_root/p['arm']/f'rep{p["rep"]}'/f'round{p["round"]}'/'compiled'
            name=p['arm']+f'-rep{p["rep"]}-P{p["slot"]}'
            for mode in ('bmc','prove','cover'):
                for variant in (('retained','cone') if mode!='prove' else ('cone','retained')):
                    if time.monotonic()-started>345:
                        jobs.append(dict(name=name,mode=mode,variant=variant,status='NOT_RUN_TOTAL_CAP'));continue
                    d=out/'jobs'/name/(mode+'-'+variant);r=job(candidate,source,d,p['slot'],mode,10,variant)
                    rec=dict(name=name,variant=variant,mode=mode,slot=p['slot'],status=r['status'],seconds=r['seconds'],smt2_bytes=r['smt2_bytes'],directory=str(d.relative_to(out)))
                    if r['status']=='FAIL' and mode=='bmc':rec['witness']=adjudicate(d,candidate,source,p['slot'],d/'physical-witness',out/'physical-build-cache')
                    jobs.append(rec);dump(out/'progress.json',dict(jobs=jobs));print('calibration',name,mode,variant,r['status'],flush=True)
        p=reg['formal']['mutant_probe'];candidate=run_root/p['arm']/f'rep{p["rep"]}'/f'round{p["round"]}'/'compiled'
        source=ROOT/next(f['source'] for f in json.loads((TASK/'private/mutant-catalog-v1.json').read_text())['faults'] if f['id']==p['mutant'])
        for variant in ('cone','retained'):
            name='mutant-anchor-'+p['mutant'];d=out/'jobs'/name/variant;r=job(candidate,source,d,p['slot'],'bmc',5,variant)
            rec=dict(name=name,mode='bmc',slot=p['slot'],variant=variant,status=r['status'],seconds=r['seconds'],smt2_bytes=r['smt2_bytes'],directory=str(d.relative_to(out)))
            if r['status']=='FAIL':rec['witness']=adjudicate(d,candidate,source,p['slot'],d/'physical-witness',out/'physical-build-cache')
            jobs.append(rec);print('calibration',name,variant,r['status'],flush=True)
        anchor=[j for j in jobs if j['name'].startswith('mutant-anchor') and j['variant']=='cone']
        gate &= bool(anchor) and anchor[0].get('witness',{}).get('reference_verdict')=='FAIL' and anchor[0]['witness'].get('formal_alarm_reproduced')
    result=dict(status='passed' if gate else 'qualification_failed',jobs=jobs,wall_seconds=time.monotonic()-started,API_calls=0,
                candidate_loop_unchanged=True,not_new_model_or_causal_effect_evidence=True,producer_sha256=sha(__file__),registration_sha256=sha(REG))
    dump(out/'summary.json',result);verify_release(run_root);return result


def balanced_correct(run_root,calibration_dir,out):
    qualification=json.loads((calibration_dir/'summary.json').read_text())
    if qualification['status']!='passed':raise ValueError('New profile/witness qualification gate failed')
    verify_release(run_root);out.mkdir(parents=True,exist_ok=False)
    finals=json.loads((run_root/'final-candidates.json').read_text())['candidates']
    jobs=[];source=TASK/'public/rtl/axis_frame_length_adjust.v';started=time.monotonic()
    for rep in (1,2,3):
        for slot in range(6):
            for mode in ('bmc','prove','cover'):
                arms=('B2_raw','C2_semantic') if (rep+slot+('bmc','prove','cover').index(mode))%2==0 else ('C2_semantic','B2_raw')
                for arm in arms:
                    f=next(f for f in finals if (f['arm'],f['repetition'])==(arm,rep));d=out/arm/f'rep{rep}'/f'P{slot}-{mode}'
                    if not f['directory']:
                        jobs.append(dict(arm=arm,repetition=rep,slot=slot,mode=mode,status='INVALID_CANDIDATE'));continue
                    candidate=run_root/f['directory'];r=job(candidate,source,d,slot,mode,10,'cone')
                    rec=dict(arm=arm,repetition=rep,slot=slot,mode=mode,status=r['status'],seconds=r['seconds'],smt2_bytes=r['smt2_bytes'],directory=str(d.relative_to(out)))
                    if r['status']=='FAIL' and mode=='bmc':rec['witness']=adjudicate(d,candidate,source,slot,d/'physical-witness',out/'physical-build-cache')
                    jobs.append(rec);dump(out/'progress.json',dict(jobs=jobs));print('balanced',arm,rep,slot,mode,r['status'],flush=True)
    result=dict(jobs=jobs,wall_seconds=time.monotonic()-started,API_calls=0,depth=24,timeout=10,variant='cone',balanced_order=True,
                not_new_model_trials=True,old_scores_unchanged=True,qualification_sha256=sha(calibration_dir/'summary.json'),producer_sha256=sha(__file__))
    dump(out/'summary.json',result);verify_release(run_root);return result
