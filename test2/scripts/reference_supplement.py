"""Additional finite controls requested by the independent reviewer; no oracle edit."""
import copy
from common import BASE,dump
from reference_controls import controls,state
from prepare import action

def supplement():
    base=controls();out={}
    full=copy.deepcopy(base['legal_capacity']['rows'][:17])
    full.append({'cycle':17,'action':action(reset=1),'pre':state(16,1),'post':state(0)})
    full.append({'cycle':18,'action':action(),'pre':state(0),'post':state(0)})
    out['extra_legal_reset_full']={'rows':full,'expected_verdict':'PASS'}
    rows=copy.deepcopy(full);rows[17]['post']['fill']=16
    out['extra_bad_reset_full']={'rows':rows,'expected_verdict':'FAIL'}
    rows=copy.deepcopy(base['legal_capacity']['rows']);rows[17]['pre']['full']=0
    out['extra_bad_pre_full_flag']={'rows':rows,'expected_verdict':'FAIL'}
    rows=copy.deepcopy(base['legal_order_and_reset']['rows']);rows[6]['post']['fill']=31
    out['extra_underflow_empty']={'rows':rows,'expected_verdict':'FAIL'}
    return out

if __name__=='__main__':
    path=BASE/'private/reference-controls-supplement-v1.json'
    if path.exists():raise SystemExit('Supplement already registered')
    dump(path,supplement());print('Four reviewer-requested controls registered; fixed candidate stimuli unchanged')
