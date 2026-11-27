#!/usr/bin/env python3
"""Prove actual transaction-monitor equivalences with independently certified context-local egg graphs."""
import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

import z3
from audit_egg_fifo_live import read_archive
from egg_frame_proof import _check
from egg_txn_context import prepare, contexts, certify_facts, verify_partition, verify_facts, ordinary
from egg_txn_context_check import PATTERN_RULES, check_graph
from egg_txn_loop import FIXTURE_INITIAL
from egg_txn_terms import REFERENCES, parse_term, z3_env, z3_term, evaluate_term
from predicates import ROOT

SCOPE = 'Unrestricted declared-width two-state transaction snapshot variables; local typed guards only.'
TIMEOUT_MS = 5000
BINARY_TIMEOUT = 30


def require(ok, reason):
    if not ok: raise ValueError(reason)


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def workload(archive):
    """Freeze all actual nonidentical pairs and predeclared derived/negative controls."""
    files=read_archive(archive)
    cfg=json.loads(files['config.json'])
    require(cfg['mode']=='live' and cfg['task']=='frame-transaction-v1' and cfg['trials']==3,'expected actual 3-trial archive')
    trials={i:json.loads(files[f'trial-{i:02d}/initial/response.json'])['output']['monitors'] for i in range(1,4)}
    pairs={}
    for n in sorted(REFERENCES):
        for a,b in combinations(trials,2):
            left,right=sorted((trials[a][n],trials[b][n]))
            if left!=right:pairs.setdefault((n,left,right),[]).append([a,b])
    require(len(pairs)==12 and sum(map(len,pairs.values()))==18,'archived actual pair inventory changed')
    result=[]
    for i,((n,left,right),occ) in enumerate(pairs.items(),1):
        result.append({'id':f'L{i:02d}','cohort':'real','property':n,'left':left,'right':right,'expected_equivalent':True,'trial_pairs':occ})
    for i,n in enumerate(REFERENCES,1):
        result.append({'id':f'N{i:02d}','cohort':'fixture_negative','property':n,'left':REFERENCES[n],
                       'right':FIXTURE_INITIAL[n],'expected_equivalent':False})
    # Fixed controls span true conditional conversion, near miss, 8-bit lower/upper
    # extreme guards, and one actual model monitor with a missing exact-four branch.
    header='(or (and (ult header_n 8) (eq h_length header_n)) (and (uge header_n 8) (eq h_length 8)))'
    tlast=trials[1]['data_last'];require(tlast.count('(uge data_n 4)')==1,'actual T1 boundary anchor changed')
    controls=[
        ('C01','guard_equal_boundary','(and (eq data_n 4) (eq data_index data_n))','(and (eq data_n 4) (eq data_index 4))',True),
        ('C02','guard_wide_nearmiss','(and (ule data_n 4) (eq data_index data_n))','(and (ule data_n 4) (eq data_index 4))',False),
        ('C03','header_8_equal',header,'(or (and (ule header_n 8) (eq h_length header_n)) (and (ugt header_n 8) (eq h_length 8)))',True),
        ('C04','header_8_gap',header,'(or (and (ult header_n 8) (eq h_length header_n)) (and (ugt header_n 8) (eq h_length 8)))',False),
        ('C05','byte_boundary_0','(and (eq m_data 0) (eq data_byte m_data))','(and (eq m_data 0) (eq data_byte 0))',True),
        ('C06','byte_boundary_255','(and (eq m_data 255) (eq data_byte m_data))','(and (eq m_data 255) (eq data_byte 255))',True),
        ('C07','byte_255_wrong','(and (eq m_data 255) (eq data_byte m_data))','(and (eq m_data 255) (eq data_byte 254))',False),
        ('C08','data_last_exact_four_gap',tlast,tlast.replace('(uge data_n 4)','(ugt data_n 4)'),False),
    ]
    for ident,label,left,right,expected in controls:
        result.append({'id':ident,'cohort':'boundary_control','property':label,'left':left,'right':right,'expected_equivalent':expected})
    return result


def typed_oracle(left,right):
    env=z3_env();a,b=[z3_term(parse_term(t),env) for t in (left,right)]
    query,model=_check(z3.Xor(a,b),TIMEOUT_MS)
    record={**query,'equivalent':{'unsat':True,'sat':False}.get(query['status']),
            'counterexample':None,'reference_value':None,'candidate_value':None}
    if model is not None:
        values={n:z3.is_true(model.eval(v,model_completion=True)) if z3.is_bool(v) else model.eval(v,model_completion=True).as_long() for n,v in env.items()}
        x,y=evaluate_term(parse_term(left),values),evaluate_term(parse_term(right),values)
        require(x != y and (x,y)==tuple(z3.is_true(model.eval(v,model_completion=True)) for v in (a,b)), 'unreplayed typed counterexample')
        record.update(counterexample=values,reference_value=x,candidate_value=y)
    return record


def run_branch(prepared,ctx,binary):
    if ctx['feasibility']['status']=='unsat':
        return {'context':ctx,'skipped':'infeasible'}
    require(ctx['feasibility']['status']=='sat','inconclusive context feasibility')
    start=time.perf_counter();facts=certify_facts(prepared,ctx);verify_facts(prepared,ctx,facts)
    preprocessing=time.perf_counter()-start
    payload={'context_id':ctx['id'], 'targets':[{'id':name,'compact':term,'event_context':ctx['id']}
              for name,term in zip(('left','right'),prepared['abstracts'],strict=True)],
             'pattern_rules':PATTERN_RULES,'ground_rules':facts['facts']}
    start=time.perf_counter()
    try:
        proc=subprocess.run([str(binary)],input=json.dumps(payload),text=True,capture_output=True,check=True,timeout=BINARY_TIMEOUT)
    except subprocess.TimeoutExpired:
        graph=None;proof={'status':'subprocess_timeout','proved':False,'steps':[],'stop':'subprocess_timeout','used_ground_rules':[]}
    else:
        graph=json.loads(proc.stdout);proof=check_graph(payload,graph)
    engine=time.perf_counter()-start
    start=time.perf_counter();baseline=ordinary(prepared,ctx,facts);baseline_seconds=time.perf_counter()-start
    require(not proof['proved'] or baseline['status']!='sat','egg proof contradicts common propositional facts')
    return {'context':ctx,'facts':facts,'payload':payload,'graph':graph,'proof':proof,'ordinary':baseline,
            'wall_seconds':{'certification_and_check':preprocessing,'egg':engine,'ordinary':baseline_seconds}}


def run_method(case,prepared,binary,split):
    plan=contexts(case['left'],case['right'],split=split)
    verify_partition(plan,prepared)
    branches=[run_branch(prepared,ctx,binary) for ctx in plan['contexts']]
    feasible=[b for b in branches if 'skipped' not in b]
    require(feasible,'partition cannot be entirely infeasible')
    return {'plan':plan,'branches':branches,'proved':all(b['proof']['proved'] for b in feasible),
            'ordinary_proved':all(b['ordinary']['status']=='unsat' for b in feasible)}


def summarize(rows):
    by={}
    for cohort in ('real','fixture_negative','boundary_control','all'):
        subset=[r for r in rows if cohort=='all' or r['case']['cohort']==cohort]
        positives=[r for r in subset if r['case']['expected_equivalent']]
        negatives=[r for r in subset if not r['case']['expected_equivalent']]
        arms={}
        for method in ('global','contextual'):
            records=[r['methods'][method] for r in subset]; branches=[b for m in records for b in m['branches']]
            feasible=[b for b in branches if 'proof' in b]
            arms[method]={'true_proved':sum(r['methods'][method]['proved'] for r in positives),
                          'ordinary_true_proved':sum(r['methods'][method]['ordinary_proved'] for r in positives),
                          'false_proved':sum(r['methods'][method]['proved'] for r in negatives),
                          'ordinary_false_proved':sum(r['methods'][method]['ordinary_proved'] for r in negatives),
                          'split_pairs':sum(m['plan']['threshold'] is not None for m in records),
                          'branches':len(branches),'feasible_branches':len(feasible),'infeasible_branches':len(branches)-len(feasible),
                          'checked_steps':sum(len(b['proof']['steps']) for b in feasible),
                          'scoped_facts':sum(len(b['facts']['facts']) for b in feasible),
                          'proof_status_counts':dict(Counter(b['proof']['status'] for b in feasible)),
                          'ordinary_statuses':dict(Counter(b['ordinary']['status'] for b in feasible)),
                          'stop_counts':dict(Counter(b['proof']['stop'] for b in feasible))}
        by[cohort]={'cases':len(subset),'true_pairs':len(positives),'false_pairs':len(negatives),'methods':arms}
    return {'complete':True,'new_api_calls':0,'scope':SCOPE,'comparisons':by,
            'case_results':[{'id':r['case']['id'],'property':r['case']['property'],'cohort':r['case']['cohort'],
                'expected_equivalent':r['case']['expected_equivalent'],'oracle':r['oracle']['status'],
                **{m:{'proved':data['proved'],'ordinary_proved':data['ordinary_proved'],'threshold':data['plan']['threshold'],
                      'branches':[{ 'guard':b['context']['guard'], 'proved':b.get('proof',{}).get('proved'),
                                    'status':b.get('proof',{}).get('status',b.get('skipped')),'fact_count':len(b.get('facts',{}).get('facts',[]))}
                                  for b in data['branches']]} for m,data in r['methods'].items()}} for r in rows]}


def run(archive,binary,out):
    binary=Path(binary).resolve(strict=True);archive=Path(archive);out=Path(out)
    cases=workload(archive)
    out.mkdir(parents=True,exist_ok=False)
    protocol={'schema':1,'scope':SCOPE,'cases':cases,'pattern_rules':PATTERN_RULES,
              'archive_sha256':digest(archive),'binary_sha256':digest(binary),
              'protocol_sha256':digest(ROOT/'docs/egg_txn_context_protocol.md'),
              'limits':{'iterations':20,'enodes':20000,'seconds':5,'outer_timeout_seconds':BINARY_TIMEOUT,'smt_timeout_ms':TIMEOUT_MS}}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2,sort_keys=True)+'\n')
    rows=[]
    with gzip.open(out/'cases.jsonl.gz','wt',encoding='utf-8') as stream:
        for case in cases:
            prepared=prepare(case['left'],case['right'])
            oracle=typed_oracle(case['left'],case['right'])
            require(oracle['equivalent'] is case['expected_equivalent'],f"frozen workload oracle differs for {case['id']}")
            methods={m:run_method(case,prepared,binary,split) for m,split in [('global',False),('contextual',True)]}
            if not case['expected_equivalent']:
                require(not any(x['proved'] or x['ordinary_proved'] for x in methods.values()),f"false proof of {case['id']}")
            row={'case':case,'prepared':prepared,'oracle':oracle,'methods':methods}
            rows.append(row);stream.write(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n');stream.flush()
            print(f"{case['id']} {case['property']}: typed={oracle['status']} global={methods['global']['proved']} context={methods['contextual']['proved']}",flush=True)
    summary=summarize(rows);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,default=ROOT/'results/milestone3/frame-txn-live/transcript.tar.gz')
    p.add_argument('--binary',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.archive,a.binary,a.output)
