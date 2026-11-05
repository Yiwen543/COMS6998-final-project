"""Protocol-safe driver runtime. Reuse immutable Claude v4 checker and DUT."""
import json
import subprocess
import time
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from real_parent_screen import configuration,verify
from run_midterm_fixed import ROOT,invoke
from spi_core_experiment import check_trace,group_status,verify_freeze as verify_parent
from spi_core_safe_interface import FIELDS,validate,parse,request_ids
from probe_spi_core_events import identity

DRIVER=ROOT/'examples/spi_core_integration/verif/tb_spi_core_safe.sv'
PREREG=ROOT/'configs/spi_core_safe_driver_prereg_v1.json'
BASE=ROOT/'results/spi_core_safe_20261104'

def compile_driver(out,simulator='verilator',driver=DRIVER):
    verify_parent();c=configuration('spi_host_core');verify(c);out.mkdir(parents=True,exist_ok=False)
    src=[str(Path(c['root'])/x) for x in c['sources']]
    inc=['-I'+str(Path(c['root'])/x) for x in c['include_dirs']]
    if simulator=='verilator':
        binary=out/'obj/Vtb_spi_core'
        cmd=['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr',
             '-Wno-fatal','--top-module','tb_spi_core','--Mdir',out/'obj','-j','2','-DSYNTHESIS',*inc,*src,driver]
    else:
        binary=out/'tb.vvp';cmd=['iverilog','-g2012','-s','tb_spi_core','-o',binary,'-DSYNTHESIS',*inc,*src,driver]
    seconds,_=invoke(cmd,out/'compile.log',timeout=300)
    return binary,{'simulator':simulator,'command':list(map(str,cmd)),'seconds':seconds}

class SafeExecutionError(RuntimeError):
    def __init__(self,stage,detail):
        super().__init__(detail);self.stage=stage

def checked_stage(out,name,fn):
    try:return fn()
    except Exception as error:
        detail=str(error)[:1000]
        (out/'failure.json').write_text(json.dumps({'stage':name,'error_type':type(error).__name__,'detail':detail},indent=2)+'\n')
        raise SafeExecutionError(name,detail) from error

def simulate(binary,requests,out,simulator='verilator'):
    parent=verify_parent();validate({'actions':requests},392,initial=True)
    out.mkdir(parents=True,exist_ok=False)
    (out/'requests.json').write_text(json.dumps({'actions':requests},indent=2)+'\n')
    vec=out/'vectors.txt';vec.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in requests))
    raw=out/'coverage.dat'
    cmd=([binary] if simulator=='verilator' else ['vvp',binary])+['+VECTORS='+str(vec)]
    if simulator=='verilator':cmd+=['+verilator+coverage+file+'+str(raw)]
    start=time.perf_counter()
    try:
        with (out/'simulation.log').open('w') as stream:
            p=subprocess.run(list(map(str,cmd)),cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=30)
        if p.returncode:raise SafeExecutionError('simulator','Simulator returned '+str(p.returncode))
    except subprocess.TimeoutExpired as error:
        raise SafeExecutionError('simulator','Simulation timeout; partial output preserved') from error
    finally:
        seconds=time.perf_counter()-start
        log=(out/'simulation.log').read_text() if (out/'simulation.log').exists() else ''
        execution={'simulator':simulator,'command':list(map(str,cmd)),'simulation_seconds':seconds,
                   'requested_cycles':len(requests),'executed_cycles':sum(x.startswith('TRACE ') for x in log.splitlines()),
                   'driver_complete':f'DRIVER_OK steps={len(requests)}' in log}
        (out/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    if not execution['driver_complete']:raise SafeExecutionError('simulator','Incomplete driver execution')
    trace,states=checked_stage(out,'transport',lambda:parse(log,requests))
    (out/'trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n')
    (out/'transport.json').write_text(json.dumps(states,indent=2)+'\n')
    points=[]
    if simulator=='verilator':
        c=configuration('spi_host_core');points=checked_stage(out,'coverage',lambda:load_all(raw,[str(Path(c['root'])/s) for s in c['sources']]))
        (out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
        if len(points)!=parent['raw_denominator'] or {identity(p) for p in points}!={tuple(i) for i in parent['counter_identities']}:
            raise SafeExecutionError('coverage','Original raw DUT denominator changed')
    checked=checked_stage(out,'checker_worker',lambda:check_trace(trace,out))
    transport={'last':states[-1],'cmd_max_pending':max(s['cmd_pending'] for s in states),
               'tx_max_pending':max(s['tx_pending'] for s in states),
               'pending':bool(states[-1]['cmd_pending'] or states[-1]['tx_pending']),
               'command_accept_ids':[s['cmd_accept_id'] for s in states if s['cmd_accept_id']!=-1],
               'tx_accept_ids':[s['tx_accept_id'] for s in states if s['tx_accept_id']!=-1]}
    transport.update(request_ids(states))
    result={**execution,'checker':checked,'transport':transport,'coverage':summary(points) if points else None,
            'groups':group_status(points,parent['targets']) if points else [],
            'delivery_complete':not transport['pending'],
            'verification_complete':not transport['pending'] and checked['verdict']=='pass',
            'checker_author':'unchanged claude-opus-5-5 v4; no GPT expected-output logic'}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result,points,trace,states
