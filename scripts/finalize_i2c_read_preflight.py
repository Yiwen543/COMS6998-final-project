"""Publish a bounded offline checker snapshot, never an A/B/C qualification."""
import json
import subprocess
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from run_i2c_read_fixed import verify_source,DRIVER,SOURCES
from i2c_read_fixture import schema

BASE=ROOT/'results/i2c_read_candidate_20261104'
ROLE=BASE/'claude-v2'
FOLDER=ROOT/'examples/heldout_i2c_read'


def finalize():
    verify_source()
    e=json.loads((ROLE/'controls-qualified/evaluation.json').read_text())
    review=json.loads((ROLE/'review.json').read_text())
    auth=json.loads((ROLE/'candidate/authorship.json').read_text())
    assert e['checker_sha256']==sha(ROLE/'candidate/checker.py')
    assert review['ready_for_offline_gate']
    assert all(t['pass'] for t in e['author_selftests'])
    assert all(t['credited_detection'] for t in e['event_controls'])
    assert all(t['credited_detection'] for t in e['negative_controls'].values())
    assert all(e['pending_controls'].values())
    assert e['address_stretch_not_read_event']
    for name,h in e['trace_inputs'].items():assert sha(BASE/'driver-v2'/name)==h
    for name,h in auth['artifact_sha256'].items():
        assert sha(ROLE/'candidate'/name)==h
        (FOLDER/name).write_bytes((ROLE/'candidate'/name).read_bytes())
    (FOLDER/'authorship.json').write_bytes((ROLE/'candidate/authorship.json').read_bytes())
    (FOLDER/'stimulus.schema.json').write_text(json.dumps(schema(),indent=2)+'\n')
    files=[*SOURCES,DRIVER,*[FOLDER/n for n in [*auth['artifact_sha256'],'authorship.json','stimulus.schema.json']],
        *[ROOT/'scripts'/n for n in ['i2c_read_fixture.py','i2c_read_gate.py','run_i2c_read_fixed.py','run_i2c_read_checked.py']],
        ROOT/'configs/i2c_read_screen.json',BASE/'spec-packet/packet.json',ROLE/'controls-qualified/evaluation.json',ROLE/'review.json']
    manifest={'schema':'i2c_read_offline_v1','offline_checker_qualified':True,'formal_B_eligible':False,
        'research_target_qualified':False,'full_ip_correctness_claim':False,'defect_classification_qualified':False,
        'scope':'Bounded single-controller ACKing-target READB/write-address behavior. Public-wire data/ACK/count and fixture FIFO ordering only.',
        'qualified_event_families':['multi_byte_read','rcont_chain','read_then_restart'],
        'limits':['No general formal proof, analog/timing/liveness/arbitration/NACK recovery validation.',
            'Stretch only observed while READB current; excluded from qualified events.',
            'Extra STOP mutant is rejected but verdict invalid rather than fail; defect attribution remains unresolved.',
            'RX delivered before pop is a fixture requirement, not an independently proved upstream timing guarantee.',
            'Single setup clock rise before START/STOP can mask one spurious edge.',
            'FBYTE0 DUT trace is pending; full256-byte completion tested only in author control.',
            'Checker repair is development-outcome-informed; no claim of a permanently blind author.'],
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in files}}
    old=FOLDER/'freeze.json'
    if old.exists() and json.loads(old.read_text())!=manifest:raise ValueError('Refuse to replace a different frozen boundary')
    old.write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def accounting():
    compiles=[];simulations=[];calls=[]
    for p in sorted(BASE.rglob('compile.json')):
        r=json.loads(p.read_text());compiles.append({'path':str(p.relative_to(ROOT)),'seconds':r['seconds']})
    for p in sorted(BASE.rglob('*.json')):
        r=json.loads(p.read_text())
        if isinstance(r,dict) and {'simulator','steps','simulation_seconds','checker_status','environment_valid'}<=r.keys() and p.name!='checked.json':
            simulations.append({'path':str(p.relative_to(ROOT)),'simulator':r['simulator'],'cycles':r['steps'],
                'seconds':r['simulation_seconds'],'environment_valid':r['environment_valid']})
        if p.name=='metadata.json' and isinstance(r,dict) and 'model_usage' in r:
            u=r.get('usage',{});calls.append({'path':str(p.relative_to(ROOT)),'role':r['role'],'model':r['requested_model'],
              'status':r['status'],'cost_usd':r.get('total_cost_usd',0),'seconds':r['wall_seconds'],
              'input_tokens_total':sum(u.get(k,0) for k in ['input_tokens','cache_creation_input_tokens','cache_read_input_tokens']),
              'output_tokens':u.get('output_tokens',0),'reasoning_tokens_included_in_output':u.get('output_tokens_details',{}).get('thinking_tokens')})
    result={'scope':'READB extension development only, including discarded driver attempts. Old write profile and natural-IP probes excluded.',
      'compilations':compiles,'simulations':simulations,'claude_calls':calls,
      'totals':{'compilations':len(compiles),'simulation_executions':len(simulations),
         'executed_cycles':sum(r['cycles'] for r in simulations),'environment_invalid_simulations':sum(not r['environment_valid'] for r in simulations),
         'compilation_seconds':sum(r['seconds'] for r in compiles),'simulation_seconds':sum(r['seconds'] for r in simulations),
         'claude_calls':len(calls),'claude_cost_usd':sum(r['cost_usd'] for r in calls),
         'claude_wall_seconds':sum(r['seconds'] for r in calls),'claude_input_tokens':sum(r['input_tokens_total'] for r in calls),
         'claude_output_tokens':sum(r['output_tokens'] for r in calls),'openai_calls':0},
      'policy':'Fresh simulator process per batch; full replay including initial reset/initialization, no appended counters; private checker rows are not simulator cycles. Thinking tokens are subsets of output, not added twice. Independent API-review overhead is development, not stimulus Token ROI.',
      'credential_file_present':(ROOT/'build/private/anthropic-crosscheck-key').exists()}
    (BASE/'accounting.json').write_text(json.dumps(result,indent=2)+'\n');return result


if __name__=='__main__':
    finalize();print(json.dumps(accounting()['totals'],indent=2))
