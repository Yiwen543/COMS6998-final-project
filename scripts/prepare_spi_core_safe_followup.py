"""Prepare a bounded, read-only followup to the preserved Claude transport audit.

No API use. Exact rendered B prompt, actual faulty-SV evidence, full previously
omitted scripts, and diffs to previously reviewed sources are included. Old
accepted controls are bound by hashes, not represented as re-reviewed here.
"""
import argparse
import ast
import difflib
import hashlib
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_runtime import BASE
from spi_core_safe_experiment import messages
from review_spi_core_safe_driver import PREFIX

def read(p):return json.loads(p.read_text())

def prepare(out):
    pre=BASE/'preflight-v3';faults=BASE/'transport-faults-v1'
    prior_packet=BASE/'review-packet-v3';prior_review=BASE/'claude-review-v1'
    previous=read(prior_packet/'packet.json');data=read(pre/'summary.json')
    parent=read(ROOT/'configs/spi_core_b_development.json')
    for rel,h in data['hashes'].items():
        if sha(ROOT/rel)!=h:raise ValueError('Offline source drift: '+rel)
    seed=pre/'calibration_seed/verilator'
    rendered=messages(parent,[],read(seed/'result.json'),read(seed/'raw-points.json'),read(seed/'trace.json'),1)
    mock=BASE/'mock-v2';replay=BASE/'replay-v2'
    if read(mock/'summary.json')['metadata']['status']!='completed':raise ValueError('Mock incomplete')
    if read(replay/'summary.json')['metadata']['status']!='completed':raise ValueError('Replay incomplete')
    if read(mock/'rep1/prompt-1-1.json')!=rendered:raise ValueError('Rendered prompt differs from actual runner')
    agreements=[]
    for rep in range(1,4):
        for stage in ['seed',*[f'round{r}' for r in range(1,7)]]:
            for name in ('requests.json','trace.json','transport.json','raw-points.json'):
                a=mock/f'rep{rep}'/stage/name;b=replay/f'rep{rep}'/stage/name
                # calls.jsonl sorts object keys; replayed requests can therefore
                # differ in key order while every action/value is identical.
                if (read(a)!=read(b)) if name=='requests.json' else (a.read_bytes()!=b.read_bytes()):
                    raise ValueError('Replay mismatch: '+str(a))
            a=read(mock/f'rep{rep}'/stage/'result.json');b=read(replay/f'rep{rep}'/stage/'result.json')
            if a['checker']!=b['checker']:raise ValueError('Checker replay mismatch')
            agreements.append(f'rep{rep}/{stage}')
    trace_same={}
    for name in data['cases']:
        for filename in ('requests.json','trace.json','transport.json'):
            rel=f'{name}/verilator/{filename}'
            p=pre/rel;old=BASE/'preflight-v2'/rel
            if sha(p)!=sha(old):raise ValueError('Previously reviewed control changed: '+rel)
            trace_same[rel]=sha(p)
        left=read(pre/name/'verilator/result.json');right=read(pre/name/'iverilog/result.json')
        for k in ('checker','transport','delivery_complete','verification_complete','executed_cycles'):
            if left[k]!=right[k]:raise ValueError('Cross-simulator semantic result differs: '+k)
    full=['scripts/create_spi_core_safe_driver.py','scripts/preflight_spi_core_safe_driver.py',
          'scripts/review_spi_core_safe_driver.py','scripts/test_spi_core_safe_faults.py',
          'scripts/pilot_model.py','tests/test_spi_core_safe_accounting.py']
    diffs={};bound={}
    for rel,old in previous['sources'].items():
        if rel in full:continue
        new=(ROOT/rel).read_text();bound[rel]={'previous_sha256':previous['source_hashes'][rel],'current_sha256':sha(ROOT/rel)}
        if new!=old:
            diffs[rel]=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='reviewed/'+rel,tofile='current/'+rel,n=1))
    compact_pre={k:v for k,v in data.items() if k not in ('cases','hashes','compilations')}
    compact_pre['compilations']=[{'simulator':c['simulator'],'seconds':c['seconds']} for c in data['compilations']]
    compact_pre['group_order']=[g['eclass'] for g in parent['targets']]
    compact_pre['cases']={name:{**{k:v for k,v in c.items() if k not in ('checker','transport','groups')},
        'raw_source_hits_by_group':[g['raw_source_hits'] for g in c['groups']],
        'checker':{k:c['checker'].get(k) for k in ('verdict','assumption_violations')},
        'passed_event_families':sorted({e['family'] for e in c['checker']['events'] if e['kind']=='pass'})} for name,c in data['cases'].items()}
    fs=read(faults/'summary.json')
    fs['boundary_queue_columns']=list(fs['boundary_queue_excerpt'][0])
    fs['boundary_queue_excerpt']=[[q[k] for k in fs['boundary_queue_columns']] for q in fs['boundary_queue_excerpt']]
    for f in fs['faults']:
        f.pop('compile');f.pop('execution')
    review=read(prior_review/'review.json')
    # Unrelated arbiter schema, random mock and validator are not called here.
    client=(ROOT/'scripts/pilot_model.py').read_text()
    client_nodes=[n for n in ast.parse(client).body if isinstance(n,(ast.Import,ast.ImportFrom)) or
                  isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in
                  ('usage_record','ModelResponseError','OpenAIModel','ReplayModel')]
    client_excerpt='\n\n'.join(ast.get_source_segment(client,n) for n in client_nodes)
    source_names=sorted({i[0] for g in parent['targets'] for i in g['counter_identities']})
    source_instances=sorted({i[-1] for g in parent['targets'] for i in g['counter_identities']})
    body={
      'task':'Followup only: decide whether the separate B development transport can freeze. Not approval for C/P or full IP correctness.',
      'prior_review':{'ready_to_freeze':False,'required_followup':review['required_followup'],
          'findings_index':[{k:f[k] for k in ('id','severity','result')} for f in review['findings']],
          'limitations':review['limitations']},
      'prior_accepted_source_hashes':bound,
      'prior_reviewed_packet_sha256':sha(prior_packet/'packet.json'),
      'omission':'Unchanged previously reviewed driver/oracle/checker and full old control traces are hash-bound here, not reprinted. This is a focused followup; do not claim to re-review omitted bodies. Modified previously reviewed sources are supplied as exact diffs. Previously omitted generation/preflight/review/client sources are supplied in full.',
      'source_diffs':diffs,'previously_missing_full_sources':{n:(ROOT/n).read_text() for n in full if n!='scripts/pilot_model.py'},
      'model_client_exact_excerpt':{'whole_file_sha256':sha(ROOT/'scripts/pilot_model.py'),'source':client_excerpt,
           'omitted':'Uncalled arbiter schema/validator, token estimate and random mock only.'},
      'actual_round_one_messages':rendered,
      'actual_prompt_evidence':{'runner_prompt':str((mock/'rep1/prompt-1-1.json').relative_to(ROOT)), 'sha256':sha(mock/'rep1/prompt-1-1.json'), 'equals_fresh_render':True},
      'preflight_summary_projection':compact_pre,
      'projection_note':'Only long per-case checker and transport details/compile command are reduced; all 17 group source-hit arrays per case, seed zeros, and all pass event families are included. Full originals hashed below. Original finite-control traces are byte-identical to the prior packet controls.',
      'target_source_identities':{'sources':source_names,'instances':source_instances,
          'identity_columns':['source_index','line','column','type','outcome','instance_index'],
          'groups':[{'eclass':g['eclass'],'nontrivial':g['nontrivial'],
             'identities':[[source_names.index(i[0]),*i[1:-1],source_instances.index(i[-1])] for i in g['counter_identities']]} for g in parent['targets']]},
      'unchanged_reviewed_traces':{'files_compared':len(trace_same),'all_equal':True,
          'trace_hash_manifest_sha256':hashlib.sha256(json.dumps(trace_same,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
          'files':'For each of the 13 named cases: requests.json, trace.json, transport.json (Verilator) equal prior reviewed preflight-v2 artifacts. Full manifest retained outside prompt.'},
      'faulty_sv_and_pending_replay':fs,
      'mock_replay':{'mode':'offline only; zero live evidence','equal_batches':agreements,'fields_compared':['requests','actual trace','queue ledger','all raw source counts','checker'],
        'equality':'Requests and checker compared as parsed JSON. Trace, ledger and raw-point files byte-identical. Request key order changes because calls.jsonl sorts keys.',
        'mock':{k:read(mock/'metadata.json')[k] for k in ('api_generation_calls','simulation_executions','executed_cycles','status')},
        'replay':{k:read(replay/'metadata.json')[k] for k in ('api_generation_calls','simulation_executions','executed_cycles','status')}},
      'clarifications':[
        'The historical system prompt contains no manual valid-holding instruction; its exact text and all user content are supplied, verified against the runner artifact.',
        'One action is one physical cycle. Accepted and pending IDs are transport diagnostics; no new calibrated solution or target is supplied to B.',
        'Complete result.json differs by simulator, command/path/timing, and coverage (Verilator only). checker, transport, completion flags and cycles agree exactly; actual trace and ledger files are byte-identical.',
        'No independent-author claim for Python transport oracle versus SV driver: both GPT/Codex. Claude DUT checker v4 remains unchanged and separately authored; finite controls and cross-simulator equality are not proof.',
        'Future C/P builders are not approved by this review. They require byte-identical common transport information and their own feedback-isolation checks before formal trials.',
        'No budget/target change: three repetitions, six rounds, 64 new cycles, seed eight, fixed 17 groups and 3107 raw counters. The one fresh B run still must meet the unchanged gate before C.'
      ]}
    evidence=[pre/'summary.json',pre/'case-definition.json',faults/'summary.json',prior_packet/'packet.json',prior_review/'review.json',
              mock/'summary.json',replay/'summary.json',mock/'rep1/prompt-1-1.json',ROOT/'configs/spi_core_safe_driver_prereg_v1.json']
    body['evidence_hashes']={str(p.relative_to(ROOT)):sha(p) for p in evidence}
    hashes={n:sha(ROOT/n) for n in set(full)|set(bound)|{'scripts/prepare_spi_core_safe_followup.py'}}
    prompt=PREFIX+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Local followup cap exceeded: '+str(len(prompt.encode())))
    out.mkdir(parents=True,exist_ok=False)
    (out/'packet.json').write_text(json.dumps(body,separators=(',',':'))+'\n');(out/'prompt.txt').write_text(prompt)
    (out/'trace-comparison.json').write_text(json.dumps(trace_same,sort_keys=True,separators=(',',':')))
    manifest={'prompt_sha256':sha(out/'prompt.txt'),'packet_sha256':sha(out/'packet.json'),
       'preflight':str(pre.relative_to(ROOT)),'preflight_sha256':sha(pre/'summary.json'),
       'prompt_bytes':len(prompt.encode()),'maximum_calls':1,'cli_budget_usd':4,'source_hashes':hashes,
       'evidence_hashes':body['evidence_hashes'],'scope':'Focused followup to preserved transport audit; live B only'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_hashes','evidence_hashes')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();prepare(a.output.resolve())
