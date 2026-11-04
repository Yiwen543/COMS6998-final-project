"""Lossless delta/RLE trace packing with a hard prompt-size gate before API use."""
import copy
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha


def unpack(packet):
    rows=[copy.deepcopy(packet['first'])]
    for d in packet['steps']:
        for _ in range(d['repeat']):
            r=copy.deepcopy(rows[-1]);r['cycle']+=1
            for key in ('action','pre','post'):r[key].update(d.get(key,{}))
            rows.append(r)
    return rows


def pack(rows):
    steps=[]
    for prev,row in zip(rows,rows[1:]):
        if row['cycle']!=prev['cycle']+1:raise ValueError('Noncontiguous trace')
        d={key:{k:v for k,v in row[key].items() if prev[key].get(k)!=v} for key in ('action','pre','post')}
        d={k:v for k,v in d.items() if v}
        if steps and {k:v for k,v in steps[-1].items() if k!='repeat'}==d:steps[-1]['repeat']+=1
        else:steps.append({'repeat':1,**d})
    p={'first':rows[0],'steps':steps}
    if unpack(p)!=rows:raise ValueError('Lossless packing failed')
    return p


def prepare(base):
    role=base/'claude-checker-v3'
    old=json.loads((role/'review-packet.json').read_text())
    controls=old.pop('private_independent_controls')
    names=['independent_write','reference_stretch_recovery','reference_nak_restart','reference_nak_timeout_recovery',
           'premature_timeout_stop','missing_nak_status']
    old['lossless_controls']={name:pack(controls[name]) for name in names}
    old['packing_semantics']='First row then steps; each step applies deltas repeat times to prior action/pre/post and increments cycle by1. Unpack reproduces the selected full input rows exactly.'
    old['packing_implementation']=Path(__file__).read_text()
    prompt='Independent read-only final audit of Claude-authored checker patches and evidence. Return JSON with ready_for_offline_gate, findings, limitations. No tools or editing. Only offline scoped validity, not B/C effectiveness.\n'+json.dumps(old,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Review packet size exceeds preflight cap')
    out=role/'compact-review';out.mkdir(parents=True,exist_ok=False)
    (out/'prompt.txt').write_text(prompt)
    (out/'preflight.json').write_text(json.dumps({'prompt_bytes':len(prompt.encode()),'size_cap_bytes':150000,
        'lossless_roundtrip':True,'control_names':names,'prompt_sha256':sha(out/'prompt.txt')},indent=2)+'\n')
    return out


if __name__=='__main__':
    out=prepare(ROOT/'results/i2c_event_candidate_20261104');print((out/'preflight.json').read_text())
