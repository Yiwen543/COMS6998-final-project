"""Fixed private controls for held CS, pending CPOL and zero enabled lanes."""
import argparse
import copy
import json
from pathlib import Path
import probe_spi_core_events as runner
from spi_core_interface import action,seed,validate
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def cases():
    out={}
    a=seed()+[action(sd=2) for _ in range(176)]
    a[8].update(valid=1,read=1,length=2,keep_cs=1)
    a[88].update(valid=1,read=1,length=1)
    out['held_cs_continuation']=a
    a=seed()+[action(sd=2) for _ in range(176)]
    a[8].update(valid=1,read=1,length=2,keep_cs=1)
    a[88].update(valid=1,read=1,length=1,cpol=1)
    out['same_csid_config_change']=a
    a=seed()+[action(sd=2) for _ in range(176)]
    a[8].update(valid=1,read=1,length=2,keep_cs=1)
    for t in range(88,91):a[t].update(valid=1,read=1,length=1,cpol=1,csid=1)
    out['pending_cpol_csid_change']=a
    a=seed()+[action() for _ in range(176)]
    a[8].update(tx_data=0xdeadbeef,tx_be=0,tx_valid=1)
    a[16].update(tx_data=0x003c5aa5,tx_be=7,tx_valid=1)
    a[20].update(valid=1,write=1,length=2)
    out['zero_be_then_payload']=a
    return out

def prepare(sim,out):
    out.mkdir(parents=True,exist_ok=False);data={};meta=[]
    for n in cases():
        rs=json.loads((sim/n/'trace.json').read_text());validate({'actions':[r['action'] for r in rs]},392,initial=True);data[n]=rs
        meta.append({'name':n,'kind':'observational_positive','expected':'Judge complete public protocol trace; do not assume DUT correct'})
    base='held_cs_continuation';rs=copy.deepcopy(data[base])
    # Output mutation after the first complete segment but before any new offer.
    for c in (70,71):
        for side in ('pre','post'):rs[c][side]['csb']=3
    data['negative/premature_held_cs_release']=rs
    meta.append({'name':'negative/premature_held_cs_release','kind':'single_fault','baseline':base,'expected':'CSAAT release without valid changed offer must fail; trace mutation, not RTL mutant'})
    # Wrong CPOL at assertion; post and next-pre agree to avoid a tiny glitch.
    base='pending_cpol_csid_change';rs=copy.deepcopy(data[base]);i=next(r['cycle'] for r in rs if r['cycle']>88 and r['pre']['csb']==3 and r['post']['csb']==1)
    rs[i]['post']['sck']=0;rs[i+1]['pre']['sck']=0
    data['negative/wrong_cpol_at_select']=rs
    meta.append({'name':'negative/wrong_cpol_at_select','kind':'single_fault','baseline':base,'expected':'CPOL violation at a real new select assertion'})
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(meta,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'script_sha256':sha(Path(__file__)),'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),
        'status':'post-v3-review independent boundary probes','no_checker_edits':True,'cases':len(data)},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve()
    runner.cases=cases;runner.run(out/'simulation',BASE/'spi_host_core_v2/screen-v2/screen.json');prepare(out/'simulation',out/'controls')
