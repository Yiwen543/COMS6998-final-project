"""Prepare bounded read-only contract/driver review; no checker authorship."""
import argparse
import ast
import json
import os
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_runtime import DRIVER,PREREG
from spi_core_safe_experiment import CONTRACT
from spi_core_experiment import CANDIDATE,BASE as OLD_BASE,verify_freeze
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE

PREFIX='''Independently review the protocol-safe SPI stimulus driver and experimental accounting, READ ONLY.
You may inspect private controls, not choose targets, generate stimulus, edit code or weaken the unchanged Claude checker.
Check queue holding/acceptance ordering, pre-edge versus post-edge ready, identical offers, reset cancellation,
no hidden cycles, EOF pending, prefix replay, failed-DUT versus driver-error classification, schema enforcement,
negative controls and fairness across future B/C. Do not infer checker correctness from simulation agreement.
This is a new transport version, NOT a repair of historical model responses. Author of DUT checker differs
from driver/stimulus author. Return ONLY JSON with ready_to_freeze:boolean, findings:[objects], limitations:[strings],
required_followup:[strings]. Say if any scope restriction or unvalidated claim blocks live B. No formal proof claim.
'''

def pack_vectors(cases):
    dictionary=[];lookup={};packed={}
    for name,vectors in cases.items():
        steps=[];last=vectors[0]
        for vector in vectors[1:]:
            changes=tuple((i,x) for i,x in enumerate(vector) if x!=last[i])
            if changes not in lookup:lookup[changes]=len(dictionary);dictionary.append([list(c) for c in changes])
            index=lookup[changes]
            if steps and steps[-1][1]==index:steps[-1][0]+=1
            else:steps.append([1,index])
            last=vector
        packed[name]={'first':vectors[0],'steps':steps}
    for name,p in packed.items():
        restored=[p['first']]
        for count,index in p['steps']:
            for _ in range(count):
                v=restored[-1].copy()
                for i,x in dictionary[index]:v[i]=x
                restored.append(v)
        if restored!=cases[name]:raise ValueError('Review encoding is not lossless')
    return {'change_dictionary':dictionary,'cases':packed}

def prepare(preflight,out):
    parent=verify_freeze();data=json.loads((preflight/'summary.json').read_text())
    if data['status']!='pass':raise ValueError('Offline gate failed')
    for p,h in data['hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Offline evidence source changed')
    out.mkdir(parents=True,exist_ok=False)
    from spi_core_safe_interface import FIELDS,STATE
    from spi_core_interface import FIELDS as PINS,OUTPUTS
    columns=[*[('request',k) for k in FIELDS],*[('action',k) for k in PINS],
             *[('pre',k) for k in OUTPUTS],*[('post',k) for k in OUTPUTS],*[('queue',k) for k in STATE if k!='cycle']]
    cases={};hashes={};evaluation={}
    for name,brief in data['cases'].items():
        folder=preflight/name/'verilator'
        requests=json.loads((folder/'requests.json').read_text())['actions'];trace=json.loads((folder/'trace.json').read_text())
        states=json.loads((folder/'transport.json').read_text())
        vectors=[]
        for a,r,q in zip(requests,trace,states):
            joined={'request':a,'action':r['action'],'pre':r['pre'],'post':r['post'],'queue':q}
            vectors.append([joined[section][k] for section,k in columns])
        cases[name]=vectors
        evaluation[name]={k:v for k,v in brief.items() if k!='groups'}
        for tool in ('verilator','iverilog'):
            for n in ('requests.json','trace.json','transport.json','result.json'):
                p=preflight/name/tool/n;hashes[str(p.relative_to(ROOT))]=sha(p)
    sources=[DRIVER,CONTRACT,ROOT/'scripts/spi_core_safe_interface.py',ROOT/'scripts/spi_core_safe_runtime.py',
             ROOT/'scripts/spi_core_safe_experiment.py',ROOT/'scripts/run_spi_core_safe_b.py',
             ROOT/'scripts/freeze_spi_core_safe_experiment.py',
             ROOT/'scripts/run_spi_core_b_development.py',ROOT/'scripts/spi_core_experiment.py',
             ROOT/'tests/test_spi_core_safe_driver.py',CANDIDATE/'contract.md',CANDIDATE/'checker.py']
    prereg=json.loads(PREREG.read_text())
    body={'role':'fresh independent Claude transport/contract reviewer; no tools',
        'preregistration':{k:v for k,v in prereg.items() if k not in ('targets','counter_identities')},
        'sources':{str(p.relative_to(ROOT)):p.read_text() for p in sources},
        'checker_prior_review':json.loads((OLD_BASE/'claude-checker-v4/review.json').read_text()),
        'checker_unchanged_sha256':parent['checker_sha256'],
        'evaluations':evaluation,'negative_controls':data['transport_negative_controls'],
        'all_trace_columns':columns,'all_traces':pack_vectors(cases),
        'encoding':'Each case first is cycle 0 vector. For each [repeat,dictionary_index] step, repeat: increment cycle, copy previous vector, apply each [column_index,value] in change_dictionary. All cases complete, lossless roundtrip checked. One Verilator trace copy shown; full Icarus equality tested, files separately hashed.',
        'honesty':'Two pending EOF controls may have raw checker pass: total verification_complete MUST remain false. Identical-two-offer short control is incomplete; a separate longer positive is included. Historical_failed_intent is a PRIVATE transport regression, never a new B result. No C outcome exists for this version. Finite controls are not proof.',
        'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},'trace_hashes':hashes,
        'scope':'Driver/JSON protocol and measurement only. Original DUT unchanged; raw denominator and 17 original targets held constant. No target relations, calibration coverage counts or DUT RTL in review packet.'}
    # Remove only duplicate historical runner/runtime code; include exact reused
    # functions plus whole-file hashes, and disclose the limited source view.
    for rel,names in {
        'scripts/run_spi_core_b_development.py':{'raw_page','diagnostics','messages','assess','token_totals'},
        'scripts/spi_core_experiment.py':{'verify_freeze','check_trace','group_status'}
    }.items():
        source=body['sources'].pop(rel)
        selected=[ast.get_source_segment(source,n) for n in ast.parse(source).body
                  if isinstance(n,ast.FunctionDef) and n.name in names]
        body.setdefault('reused_exact_source_excerpts',{})[rel]={'whole_file_sha256':sha(ROOT/rel),
            'functions':'\n\n'.join(selected),'omission':'Uncalled historical simulator/runner loop and CLI removed; new safe runner/runtime fully included.'}
    prompt=PREFIX+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:
        (out/'preparation-failure.json').write_text(json.dumps({'reason':'local byte cap','prompt_bytes':len(prompt.encode()),'API_calls':0})+'\n')
        raise ValueError('Review byte cap exceeded: '+str(len(prompt.encode())))
    (out/'packet.json').write_text(json.dumps(body,separators=(',',':'))+'\n');(out/'prompt.txt').write_text(prompt)
    manifest={'prompt_sha256':sha(out/'prompt.txt'),'packet_sha256':sha(out/'packet.json'),
              'preflight':str(preflight.relative_to(ROOT)),'preflight_sha256':sha(preflight/'summary.json'),
              'prompt_bytes':len(prompt.encode()),'all_trace_cases':len(cases),'all_traces_lossless':True,
              'maximum_calls':1,'cli_budget_usd':4,'source_hashes':body['source_hashes']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:v for k,v in manifest.items() if k!='source_hashes'}))

def run(packet,out):
    m=json.loads((packet/'manifest.json').read_text())
    if sha(packet/'prompt.txt')!=m['prompt_sha256'] or sha(packet/'packet.json')!=m['packet_sha256']:raise ValueError('Packet changed')
    for p,h in m['source_hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Prepared source changed')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:raise ValueError('Staged Anthropic key absent/unsafe')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    try:
        result=call((packet/'prompt.txt').read_text(),out,env,'SPI protocol-safe driver independent reviewer')
        (out/'review.json').write_text(json.dumps(result,indent=2)+'\n')
        (out/'packet-manifest.json').write_bytes((packet/'manifest.json').read_bytes())
        print(json.dumps({'ready_to_freeze':result.get('ready_to_freeze')}))
    finally:KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['prepare','live'],required=True)
    p.add_argument('--preflight',type=Path);p.add_argument('--packet',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.mode=='prepare':prepare(a.preflight.resolve(),a.output.resolve())
    else:run(a.packet.resolve(),a.output.resolve())
