"""Distinguish an early cutoff from a strictly witnessed paused interval.

The old mandatory-event expectations were based on the first stall flag. That
criterion conflicts with flag-only vacuity controls. Preserve original ledgers;
add prefixes with independently observed overdue edges before requiring events.
"""
import copy
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def prepare():
    prior=BASE/'contract-repair-v4/controls';out=BASE/'contract-repair-v4/qualified-controls';out.mkdir(parents=True,exist_ok=False)
    data=json.loads((prior/'inputs.json').read_text());meta=json.loads((prior/'controls.json').read_text());audit=[];extra=[]
    names=('truncated/tx_starvation_resume','truncated/rx_backpressure_resume','hand/truncated_starvation')
    for m in meta:
        if m['name'] not in names:continue
        old=data[m['name']];base=data[m['baseline']];family=m['required_event_family']
        command=next(r['action'] for r in base if r['action']['valid'] and r['pre']['ready']);half=command['clkdiv']+1
        old_edges=[r['cycle'] for r in old if r['pre']['sck']!=r['post']['sck']]
        if old[-1]['cycle']-old_edges[-1]!=half:raise ValueError('Early-cutoff premise changed')
        last=None;found=None
        for r in base:
            if r['pre']['sck']!=r['post']['sck']:last=r['cycle']
            if r['cycle']>old[-1]['cycle'] and last is not None and r['cycle']-last>half and r['pre']['csb']==r['post']['csb']!=3:
                found=r['cycle'];break
        if found is None:raise ValueError('No independently overdue prefix')
        name='confirmed_prefix/'+m['name'].replace('/','_');data[name]=copy.deepcopy(base[:found+1])
        extra.append({'name':name,'kind':'incomplete','baseline':m['baseline'],'required_event_family':family,
            'forbidden_success_event_family':family,'expected':'Strictly overdue selected edge while operation unfinished; explicit pending/failed episode, never success'})
        audit.append({'original_control':m['name'],'old_last_cycle':old[-1]['cycle'],'last_edge':old_edges[-1],'half_period':half,
            'old_elapsed_equals_half':True,'confirmed_control':name,'confirmed_last_cycle':found,'reason':'At the original integer cutoff elapsed time equals one nominal half-period; no strictly overdue interval yet. A flag alone must not force a real-stall event. One later cycle independently witnesses a pause.'})
        m['superseded_required_event_family']=m.pop('required_event_family')
        m['forbidden_success_event_family']=family
        m['expected']='Early incomplete cutoff at exactly one nominal half-period since last edge. Generic inconclusive or pending is valid; successful recovery is forbidden. Original mandatory-presence assertion retained in prior immutable controls and audit.'
    meta+=extra
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(meta,indent=2)+'\n')
    (out/'prefix-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'event evidence criterion reconciled before independent v4 review; no checker edits','script_sha256':sha(Path(__file__)),
        'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'prior_inputs_sha256':sha(prior/'inputs.json'),
        'prior_controls_sha256':sha(prior/'controls.json'),'cases':len(data),'no_new_simulations':True,'prefix_audit_sha256':sha(out/'prefix-audit.json')},indent=2)+'\n')
    print(json.dumps(audit))

if __name__=='__main__':prepare()
