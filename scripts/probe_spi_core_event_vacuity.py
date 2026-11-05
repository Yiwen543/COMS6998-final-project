"""Private, bounded event-vacuity controls; no model stimulus or target search.

Measure a late TX refill and brief RX drain delay without presuming they stall.
Event-absence labels require both no asserted stall and regular selected SCK.
"""
import argparse
import json
from pathlib import Path
import probe_spi_core_events as runner
from spi_core_interface import action,seed,validate
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def cases():
    out={}
    for when in (260,264,265,266,267,268,300):
        aa=seed()+[action() for _ in range(384)]
        aa[8].update(tx_data=0xa1b2c3d4,tx_be=15,tx_valid=1)
        aa[10].update(valid=1,write=1,length=4,clkdiv=3)
        aa[when].update(tx_data=0x11223344,tx_be=15,tx_valid=1)
        out['tx_refill_'+str(when)]=aa
    for when in (None,74):
        aa=seed()+[action(sd=2) for _ in range(176)]
        aa[8].update(valid=1,read=1,length=7)
        if when is not None:aa[when]['rx_ready']=0
        out['rx_regular' if when is None else 'rx_one_cycle_hold']=aa
    return out

def prepare(sim,out):
    out.mkdir(parents=True,exist_ok=False);data={};controls=[];observations={}
    for name in cases():
        rs=json.loads((sim/name/'trace.json').read_text());data[name]=rs
        validate({'actions':[r['action'] for r in rs]},392,initial=True)
        direction='tx' if name.startswith('tx_') else 'rx';half=4 if direction=='tx' else 1
        edges=[r['cycle'] for r in rs if r['pre']['sck']!=r['post']['sck'] and r['pre']['csb']==2 and r['post']['csb']==2]
        gaps=[b-a for a,b in zip(edges,edges[1:])]
        stall=[r['cycle'] for r in rs if r['pre'][direction+'_stall'] or r['post'][direction+'_stall']]
        held=[r['cycle'] for r in rs if r['pre']['rx_valid'] and not r['action']['rx_ready']]
        complete=len(edges)==(80 if direction=='tx' else 128) and rs[-1]['post']['csb']==3 and not rs[-1]['post']['active']
        absent=complete and not stall and all(g==half for g in gaps)
        observations[name]={'selected_sck_edges':len(edges),'half_period':half,'edge_gaps':sorted(set(gaps)),
            'stall_cycles':stall,'held_rx_valid_cycles':held,'public_completion_shape':complete,'no_stall_observed':absent,
            'note':'This shape does not establish payload correctness; independent checker still judges the whole transfer.'}
        meta={'name':name,'kind':'observational_positive','expected':'Report checker outcome; independently measured no-stall cases must not emit a recovery event'}
        if absent:meta['forbidden_event_family']=direction+('_starvation_resume' if direction=='tx' else '_backpressure_resume')
        controls.append(meta)
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (out/'observations.json').write_text(json.dumps(observations,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'independent event-vacuity probes after v3 review','script_sha256':sha(Path(__file__)),
      'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'cases':len(data),'no_checker_edits':True,
      'private_only':'No probe, calibration or source witness enters experimental prompts. All configured probes retained, no model/target selection.'},indent=2)+'\n')
    for name,r in observations.items():print(json.dumps({'case':name,'no_stall_observed':r['no_stall_observed'],'stall_cycles':len(r['stall_cycles']),'held_rx':r['held_rx_valid_cycles'],'edge_gaps':r['edge_gaps']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve()
    runner.cases=cases;runner.run(out/'simulation',BASE/'spi_host_core_v2/screen-v2/screen.json');prepare(out/'simulation',out/'controls')
