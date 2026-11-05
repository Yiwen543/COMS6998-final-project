"""Safe-offer experiment boundary; parent evidence is immutable."""
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_experiment import verify_freeze as verify_parent
from spi_core_safe_runtime import compile_driver as compile_safe,simulate as simulate_safe,BASE,PREREG
from spi_core_safe_interface import FIELDS,seed,action,schema as experiment_schema,validate as validate_experimental
from run_spi_core_b_development import messages as raw_messages

FREEZE=ROOT/'configs/spi_core_safe_b_development_v1.json'
CONTRACT=ROOT/'examples/spi_core_integration/docs/safe_offer_contract.md'

def verify_freeze(path=FREEZE):
    parent=verify_parent();c=json.loads(path.read_text())
    if not c['offline_gate_pass']:raise ValueError('Safe driver offline gate not passed')
    for p,h in c['hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Frozen safe-driver artifact changed: '+p)
    if c['targets']!=parent['targets'] or c['counter_identities']!=parent['counter_identities']:
        raise ValueError('Original targets/denominator changed')
    return c

def compile_driver(out):
    binary,m=compile_safe(out)
    return binary,m['command'],m['seconds']

def simulate(binary,actions,out,denominator):
    r,p,t,q=simulate_safe(binary,actions,out)
    return r,p,t

def messages(config,generated,prior,points,trace,round_no):
    old=raw_messages(config,[],prior,points,trace,round_no)
    body=json.loads(old[1]['content'])
    body['specification']={'offer_interface':CONTRACT.read_text(),
        'hardware_pin_contract':body['specification'],
        'distinction':'Response actions are offer requests, NOT raw DUT pins. The hardware contract describes actual pins checked downstream. The offer interface determines how those pins are driven.'}
    body['cycle_field_order']=list(FIELDS);body['field_widths']=FIELDS
    body['common_seed']=[[a[k] for k in FIELDS] for a in seed()]
    body['previous_generated_cycles']=[[a[k] for k in FIELDS] for a in generated]
    body['transport']={k:v for k,v in prior['transport'].items() if k not in ('command_accept_ids','tx_accept_ids')}
    body['delivery_complete']=prior['delivery_complete'];body['verification_complete']=prior['verification_complete']
    old[1]['content']=json.dumps(body,separators=(',',':'))
    return old
