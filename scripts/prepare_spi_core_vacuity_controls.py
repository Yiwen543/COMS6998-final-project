"""Merge immutable controls and add explicit false-success controls."""
import copy
import json
from pathlib import Path
from spi_core_interface import validate
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def prepare(out):
    out.mkdir(parents=True,exist_ok=False);data={};meta=[];parents=[]
    for prefix,folder in [('',BASE/'contract-repair-v3/rx-window/controls'),('vacuity/',BASE/'contract-repair-v3/vacuity/controls'),('boundary/',BASE/'contract-repair-v3/boundaries-v2/controls')]:
        m=json.loads((folder/'manifest.json').read_text())
        if any(sha(folder/(x+'.json'))!=m[x+'_sha256'] for x in ('inputs','controls')):raise ValueError('Parent control drift')
        d=json.loads((folder/'inputs.json').read_text())
        for c in json.loads((folder/'controls.json').read_text()):
            z=copy.deepcopy(c);z['name']=prefix+c['name']
            if 'baseline' in z:z['baseline']=prefix+z['baseline']
            if z['name']=='boundary/same_csid_config_change':
                z['kind']='spec_conflict_observation';z['expected']='Retain DUT-vs-pinned-document disagreement, not checker false-alarm credit: public theory241-249 requires idle gap before config change after CSAAT; actual valid-input trace has no gap. Do not weaken checker or overwrite DUT; upstream interpretation remains to be confirmed.'
            meta.append(z);data[z['name']]=d[c['name']]
        parents.append({'directory':str(folder.relative_to(ROOT)),'inputs_sha256':sha(folder/'inputs.json'),'controls_sha256':sha(folder/'controls.json')})
    for family,base,flag in [('tx_starvation_resume','vacuity/tx_refill_268','tx_stall'),('rx_backpressure_resume','vacuity/rx_one_cycle_hold','rx_stall')]:
        rs=copy.deepcopy(data[base]);i=267 if flag=='tx_stall' else 74
        for side in ('pre','post'):rs[i][side][flag]=1
        name='flag_only/'+family;data[name]=rs
        meta.append({'name':name,'kind':'event_false_success_control','baseline':base,'forbidden_success_event_family':family,
            'expected':'One contradictory output flag without any paused SCK. A stall flag alone cannot justify a successful recovery; diagnostic failure/pending is not a DUT-mutant coverage claim.',
            'changes':[{'cycle':i,'sides':['pre','post'],'field':flag,'after':1}]})
    for rs in data.values():validate({'actions':[r['action'] for r in rs]},392,initial=True)
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(meta,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_before_v4_evaluation','parents':parents,'script_sha256':sha(Path(__file__)),
      'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'schema_validator_sha256':sha(ROOT/'scripts/spi_core_interface.py'),
      'cases':len(data),'all_input_width_schema_checks_pass':True,'no_new_simulation':True,'no_checker_edits':True},indent=2)+'\n')
    print(json.dumps({'cases':len(data),'schema_valid':True}))

if __name__=='__main__':prepare(BASE/'contract-repair-v4/controls')
