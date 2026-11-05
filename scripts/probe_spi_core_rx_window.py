"""Repair a private RX stimulus window; never change expected-output logic."""
import argparse
import copy
import json
from pathlib import Path
import probe_spi_core_events as runner
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def cases():
    src=BASE/'contract-repair-v2/probes/read_asymmetric_full0'
    rows=json.loads((src/'trace.json').read_text())
    aa=copy.deepcopy(json.loads((src/'actions.json').read_text())['actions'])
    for a in aa[8:]:a['sd']=0
    edges=[r['cycle'] for r in rows if r['pre']['sck']==0 and r['post']['sck']==1 and r['post']['csb']==2]
    bits=[(b>>i)&1 for b in (0xa5,0x5a,0x3c) for i in reversed(range(8))]
    if len(edges)!=len(bits):raise ValueError('Template edge count')
    for c,b in zip(edges,bits):
        for k in (c,c+1):aa[k]['sd']=b<<1
    return {'read_full0_aligned':aa}

def run(out,prior):
    runner.cases=cases;runner.run(out/'simulation',BASE/'spi_host_core_v2/screen-v2/screen.json')
    rs=json.loads((out/'simulation/read_full0_aligned/trace.json').read_text())
    data=json.loads((prior/'inputs.json').read_text());controls=json.loads((prior/'controls.json').read_text())
    for m in controls:
        if m['name']=='probe/read_asymmetric_full0':
            m['kind']='sampling_ambiguous_control';m['expected']='Legacy private stimulus used FULLCYC1 launch schedule for FULLCYC0; conservative unresolved is correct. Preserve as ambiguity control, not a checker false positive or DUT defect.'
    data['probe/read_full0_aligned']=rs;controls.append({'name':'probe/read_full0_aligned','kind':'observational_positive','expected':'Nonuniform RX using own FULLCYC0 clock schedule, not FULLCYC1; no expected-output patch'})
    d=out/'controls';d.mkdir()
    (d/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(d/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (d/'manifest.json').write_text(json.dumps({'status':'private stimulus repair before v3 checker','script_sha256':sha(Path(__file__)),
      'inputs_sha256':sha(d/'inputs.json'),'controls_sha256':sha(d/'controls.json'),'prior_inputs_sha256':sha(prior/'inputs.json'),'cases':len(data),
      'no_checker_edits':True,'source':'Actual re-simulated input change; preserved original ambiguous control'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prior',type=Path,required=True);a=p.parse_args();run(a.output.resolve(),a.prior.resolve())
