"""Private observational calibration of original SPI core. NOT a checker/B run.

Fixed public-pin sequences are excluded from experimental and checker-author
prompts. Observed events/coverage alone never establish specification correctness.
"""
import argparse
import json
from pathlib import Path
from spi_core_interface import FIELDS,seed,action,validate,parse
from real_parent_screen import configuration,verify
from run_midterm_fixed import ROOT,invoke,sha
from inventory_natural_coverage import load_all
from coverage import summary

DRIVER=ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv'

def cases():
    def batch(n,**kw):return seed()+[action(**kw) for _ in range(n)]
    def setat(a,cycle,**kw):a[8+cycle].update(kw)
    out={'seed':seed()}
    a=batch(56);setat(a,0,tx_data=0xa1b2c3d4,tx_be=15,tx_valid=1)
    setat(a,2,valid=1,write=1);out['ordinary_standard_write']=a
    a=batch(176)
    for cycle,speed in [(0,0),(56,1),(112,2)]:
        setat(a,cycle,tx_data=0xa1b2c3d4,tx_be=15,tx_valid=1)
        setat(a,cycle+2,valid=1,write=1,speed=speed)
    out['ordinary_three_speeds']=a
    a=batch(256);setat(a,0,tx_data=0xa1b2c3d4,tx_be=15,tx_valid=1)
    setat(a,2,valid=1,write=1,length=7)
    setat(a,120,tx_data=0x11223344,tx_be=15,tx_valid=1)
    out['tx_starvation_resume']=a
    a=batch(384,rx_ready=0,sd=10);setat(a,0,valid=1,read=1,length=11)
    for x in a[8+220:]:x['rx_ready']=1
    out['rx_backpressure_resume']=a
    a=batch(176,sd=10);setat(a,0,valid=1,read=1,length=2,keep_cs=1)
    # Hold the offered command through the configuration/CSID closing gap.
    # A one-cycle pulse is not legal when command_ready is deasserted.
    for t in range(80,83):setat(a,t,valid=1,read=1,length=1,csid=1)
    out['partial_then_csid_switch']=a
    a=batch(176,sd=10);setat(a,0,valid=1,read=1,length=19)
    for t in range(40,44):setat(a,t,sw_reset=1)
    setat(a,50,valid=1,read=1,length=1)
    out['software_reset_restart']=a
    a=batch(112,sd=10);setat(a,0,valid=1,read=1,length=2,full_cycle=1)
    out['ordinary_fullcycle_read']=a
    return out

def identity(p):
    # Driver top is not part of DUT identity. Actual child instance still is.
    return tuple(p[k] for k in ('source','line','column','type','outcome'))+(
        p['hierarchy'].split('.dut',1)[1],)

def run(out,screen):
    c=configuration('spi_host_core');verify(c);out.mkdir(parents=True,exist_ok=False)
    sources=[str(Path(c['root'])/p) for p in c['sources']]
    inc=['-I'+str(Path(c['root'])/p) for p in c['include_dirs']]
    bins={};comp=[]
    for simulator in ('verilator','iverilog'):
        folder=out/simulator;folder.mkdir()
        if simulator=='verilator':
            binary=folder/'obj/Vtb_spi_core'
            cmd=['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_spi_core','--Mdir',folder/'obj','-j','2','-DSYNTHESIS',*inc,*sources,DRIVER]
        else:
            binary=folder/'tb.vvp';cmd=['iverilog','-g2012','-s','tb_spi_core','-o',binary,'-DSYNTHESIS',*inc,*sources,DRIVER]
        sec,_=invoke(cmd,folder/'compile.log',timeout=300);bins[simulator]=binary
        comp.append({'simulator':simulator,'command':list(map(str,cmd)),'seconds':sec})
    static=json.loads(screen.read_text());groups=[g for g in static['groups'] if g['static_candidate_group']]
    reports=[];denominator=None
    for name,aa in cases().items():
        validate({'actions':aa},392,initial=True)
        folder=out/name;folder.mkdir();(folder/'actions.json').write_text(json.dumps({'actions':aa},indent=2)+'\n')
        vec=folder/'vectors.txt';vec.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in aa))
        traces={};simulations=[];points=[]
        for simulator,binary in bins.items():
            cmd=([binary] if simulator=='verilator' else ['vvp',binary])+['+VECTORS='+str(vec)]
            raw=folder/'coverage.dat'
            if simulator=='verilator':cmd+=['+verilator+coverage+file+'+str(raw)]
            sec,log=invoke(cmd,folder/(simulator+'.log'),timeout=30)
            if f'DRIVER_OK steps={len(aa)}' not in log:raise ValueError('Incomplete execution')
            traces[simulator]=parse(log,aa)
            simulations.append({'simulator':simulator,'seconds':sec,'command':list(map(str,cmd)),'executed_cycles':len(aa)})
            if simulator=='verilator':points=load_all(raw,sources)
        if traces['verilator']!=traces['iverilog']:raise ValueError('Independent simulators disagree: '+name)
        (folder/'trace.json').write_text(json.dumps(traces['verilator'],indent=2)+'\n')
        (folder/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
        counts={identity(p):p['hits'] for p in points}
        if len(counts)!=len(points):raise ValueError('Ambiguous physical counters')
        if denominator is None:denominator=set(counts)
        if set(counts)!=denominator:raise ValueError('Raw denominator changed')
        gs=[]
        for g in groups:
            selected=[m for m in g['members'] if m['seed_zero_dynamic_candidate']]
            hits=[{'id':m['id'],'point':m['mapping']['point'],'hits':counts[identity(m['mapping']['point'])]} for m in selected]
            gs.append({'eclass':g['eclass'],'nontrivial':g['nontrivial_static_candidate'],'all_source_counters_hit':all(x['hits']>0 for x in hits),'source_counters':hits})
        rows=traces['verilator']
        observations={
            'accepted_commands':[r['cycle'] for r in rows if r['action']['valid'] and r['pre']['ready']],
            'accepted_tx_words':[r['cycle'] for r in rows if r['action']['tx_valid'] and r['pre']['tx_ready']],
            'received_words':[{'cycle':r['cycle'],'data':r['pre']['rx_data']} for r in rows if r['pre']['rx_valid'] and r['action']['rx_ready']],
            'tx_stall_cycles':[r['cycle'] for r in rows if r['pre']['tx_stall']],
            'rx_stall_cycles':[r['cycle'] for r in rows if r['pre']['rx_stall']],
            'last_public_outputs':rows[-1]['post']}
        report={'case':name,'status':'observations_only_no_checker','cycles_per_simulator':len(aa),'trace_agreement':True,'simulations':simulations,'observations':observations,'coverage':summary(points),'groups':gs}
        (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
    result={'status':'private_observations_only','B_allowed':False,'checker_started':False,'compilations':comp,
        'executions':sum(len(r['simulations']) for r in reports),'total_executed_cycles':sum(r['cycles_per_simulator']*2 for r in reports),
        'coverage_policy':'All original DUT counters; fresh simulator process per case; seed/reset included; TB excluded; counter denominator unchanged across cases.',
        'limitation':'Trace agreement and raw hits do not prove correctness or legal temporal recovery. Independent specification checker still required.',
        'screen':str(screen),'screen_sha256':sha(screen),'cases':reports,
        'hashes':{str(p):sha(p) for p in [Path(__file__),DRIVER,ROOT/'scripts/spi_core_interface.py']}}
    (out/'observations.json').write_text(json.dumps(result,indent=2)+'\n')
    for r in reports:
        print(json.dumps({'case':r['case'],'cycles':r['cycles_per_simulator'],'commands':r['observations']['accepted_commands'],
              'TX_stalls':len(r['observations']['tx_stall_cycles']),'RX_stalls':len(r['observations']['rx_stall_cycles']),
              'groups_hit':sum(g['all_source_counters_hit'] for g in r['groups'])}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--screen',type=Path,required=True);a=p.parse_args();run(a.output.resolve(),a.screen.resolve())
