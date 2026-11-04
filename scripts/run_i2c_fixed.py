"""Pinned I2C write-mode driver. No built-in DUT oracle; checker is separate."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT, invoke, sha
from coverage import load, summary
from i2c_fixture import validate_actions, write_vectors, parse

BASE=ROOT/'third_party/opentitan_candidate/hw/ip'
SOURCE=BASE/'i2c/rtl/i2c_controller_fsm.sv'
SOURCES=[BASE/'i2c/rtl/i2c_pkg.sv',SOURCE]
DRIVER=ROOT/'examples/heldout_i2c_controller/verif/tb_i2c_fixed.sv'
TOP='tb_i2c_fixed'
PIN=ROOT/'results/i2c_event_candidate_20261104/probe.json'


def verify_source():
    for name,digest in json.loads(PIN.read_text())['sources_sha256'].items():
        if sha(ROOT/name)!=digest: raise ValueError('Pinned source/spec changed: '+name)


def compile_driver(out,simulator='verilator'):
    verify_source();out.mkdir(parents=True,exist_ok=True)
    if simulator=='verilator':
        binary=out/'verilator-build'/('V'+TOP)
        cmd=['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr',
             '-Wno-fatal','-Wno-TIMESCALEMOD','--top-module',TOP,'--Mdir',binary.parent,'-j','2']
    elif simulator=='iverilog':
        binary=out/(TOP+'.vvp');cmd=['iverilog','-g2012','-s',TOP,'-o',binary]
    else:raise ValueError('Unknown simulator')
    cmd+=['-DSYNTHESIS','-I'+str(BASE/'prim/rtl'),*SOURCES,DRIVER]
    seconds,_=invoke(cmd,out/'compile.log',timeout=300)
    (out/'compile.json').write_text(json.dumps({'command':list(map(str,cmd)),'seconds':seconds,
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [*SOURCES,DRIVER,Path(__file__),ROOT/'scripts/i2c_fixture.py']}},indent=2)+'\n')
    return binary


def simulate(binary,actions,out,name,simulator='verilator'):
    validate_actions({'actions':actions},392)
    out.mkdir(parents=True,exist_ok=True)
    vector=out/(name+'.vectors');raw=out/(name+'.dat')
    write_vectors(actions,vector)
    (out/(name+'.actions.json')).write_text(json.dumps({'actions':actions},indent=2)+'\n')
    cmd=(['vvp',binary] if simulator=='iverilog' else [binary])+['+VECTORS='+str(vector)]
    if simulator=='verilator':cmd+=['+verilator+coverage+file+'+str(raw)]
    seconds,log=invoke(cmd,out/(name+'.sim.log'),timeout=60)
    if f'DRIVER_OK steps={len(actions)}' not in log:raise ValueError('Incomplete driver batch')
    rows=parse(actions,log)
    (out/(name+'.trace.json')).write_text(json.dumps(rows,indent=2)+'\n')
    points=load(raw,str(SOURCE.relative_to(ROOT)),include_descendants=True) if simulator=='verilator' else []
    result={'simulator':simulator,'steps':len(actions),'simulation_seconds':seconds,
            'coverage':summary(points),'checker_status':'not_evaluated_here',
            'environment_valid':not any(l.startswith('ENV_ERROR') for l in log.splitlines()),
            'environment_errors':[l for l in log.splitlines() if l.startswith('ENV_ERROR')],
            'raw_policy':'All original controller DUT counters, separate source identity; reset/initialization included; no TB counters. Fresh process, cumulative replay.',
            'rows_sha256':sha(out/(name+'.trace.json'))}
    (out/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result,rows


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--actions',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--simulator',choices=['verilator','iverilog'],default='verilator');a=p.parse_args()
    actions=validate_actions(json.loads(a.actions.read_text()),392)
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    print(json.dumps(simulate(compile_driver(out,a.simulator),actions,out,'batch',a.simulator)[0],indent=2))
