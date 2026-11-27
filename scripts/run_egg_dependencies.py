#!/usr/bin/env python3
"""Frozen dependency-first workload with eager, cached, ordinary and SMT controls."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import time

from audit_egg_regression import loads, read
from egg_dependency_reuse import FactAuthority, CoreSession, CoreStore, ScopedMemory, require, targeted_lookup
from egg_dependency_workload import ARCHIVE, LIVE_ARCHIVE, PROTOCOL, digest, plan
from predicates import ROOT
from egg_regression_check import PATTERN_RULES, check_graph
from egg_regression_facts import prepare, context_id
from egg_regression_reuse import ProofStore
from egg_regression_smt import IncrementalSMT, classify, fresh_compare, verify_result, verify_direction, _verify_receipt
from egg_txn_terms import parse_term
from run_egg_regression import groups, graph_count, payload, invoke, dump


ARMS = ('smt_exact','smt_subscope','egg_eager','egg_cache','egg_dependency','ordinary_dependency')
TRIAGE_ARMS = ('egg_dependency','ordinary_dependency','egg_dependency_triage','ordinary_dependency_triage')
TRIAGE_PROTOCOL = ROOT/'docs/egg_dependency_triage_protocol.md'


def _typed(solver, case, previous=None):
    result=solver.compare(case['left'],case['right'],case['guard'])
    if previous is not None:
        require(verify_result(case['left'],case['right'],case['guard'],previous)
                and previous['relation']==result['relation'], 'saved typed result differs')
        return previous
    return result


def _direction(solver, left, right, guard, previous=None):
    result=solver.check_direction(left,right,guard)
    if previous is not None:
        require(verify_direction(left,right,guard,previous) and
                previous['direction']['status']==result['direction']['status'], 'saved typed direction differs')
        return previous
    return result


class Arm:
    """Separate operational state per workload and comparison arm."""

    def __init__(self, name, binary):
        self.triage=name.endswith('_triage')
        self.name, self.binary = name.removesuffix('_triage'), binary
        name=self.name
        self.solver=IncrementalSMT()
        self.boolean=Counter();self.graphs=Counter();self.timing=Counter()
        self.memory=ScopedMemory(name=='smt_subscope') if name.startswith('smt') else None
        self.authority=None if self.memory else FactAuthority()
        self.store=(None if self.memory else CoreStore(self.boolean) if name=='ordinary_dependency' else ProofStore())
        self.rows=[];self.wall=0.0
        self.counters=Counter()

    def _direct(self, batch, replay):
        guard=batch[0]['guard']
        feasibility=self.solver._guard(guard,self.solver._group(guard))
        if replay is not None:
            _verify_receipt(replay['feasibility'],feasibility,guard)
            feasibility=replay['feasibility']
        rows=[]
        for c in batch:
            old=next((r for r in replay['rows'] if r['id']==c['id']),None) if replay is not None else None
            if feasibility['status']!='sat':
                record={'relation':'infeasible' if feasibility['status']=='unsat' else 'unknown','via':'guard'}
            else:
                route=self.memory.lookup(c,audit=replay is not None)
                if route is not None:
                    via='identity' if not route else 'same_scope' if all(self.memory.entries[i]['guard']==guard for i in route) else 'subscope'
                    record={'relation':'equivalent','via':via,'path':route}
                else:
                    result=_typed(self.solver,c,old.get('smt') if old else None)
                    record={'relation':result['relation'],'via':'typed_smt','smt':result}
                    if result['relation']=='equivalent':self.memory.add(c)
            rows.append({'id':c['id'],**record})
        return {'feasibility':feasibility,'rows':rows}

    def _native(self, prepared, evidence, source_ids, pending, replay):
        pairs={}
        for c in pending:
            pair=(source_ids[c['left']],source_ids[c['right']])
            require(pair[0]!=pair[1], 'identity must not require native graph')
            pairs.setdefault(frozenset(pair),pair)
        request=payload(prepared,evidence,source_ids,list(pairs.values()))
        if replay is None:
            graph,proofs=invoke(request,self.binary,self.timing,self.name)
        else:
            require(replay['native'] is not None and request==replay['native']['payload'], 'native replay request differs')
            graph=replay['native']['graph'];proofs=check_graph(request,graph)
        graph_count(self.graphs,graph,proofs)
        return {'payload':request,'graph':graph},pairs,proofs

    def _assisted(self,batch,replay):
        guard=batch[0]['guard']; authority=self.authority;authority.start_group()
        sources=list(dict.fromkeys(s for c in batch for s in (c['left'],c['right'])))
        prepared=prepare(sources); source_ids={s:f't{i:03}' for i,s in enumerate(sources)}
        old_rows={r['id']:r for r in replay['rows']} if replay is not None else {}
        eager=self.name=='egg_eager'; ordinary=self.name=='ordinary_dependency'
        needs_discovery=not all(parse_term(c['left'])==parse_term(c['right']) for c in batch)
        evidence=None
        if eager and needs_discovery:
            evidence=authority.discover(prepared,guard); feasibility=evidence['feasibility']
        else:
            feasibility=authority.feasibility(guard)
        if feasibility['status']!='sat':
            rel='infeasible' if feasibility['status']=='unsat' else 'unknown'
            return {'prepared':prepared,'feasibility':feasibility,'fact_events':authority.events,'native':None,
                    'rows':[{'id':c['id'],'relation':rel,'via':'guard'} for c in batch]}
        initial, second, verdicts={}, {}, {}
        for c in batch:
            if eager:
                # Identity-only batch needs no primitive enumeration.
                current=evidence if evidence is not None else {'guard':guard,'context_id':context_id(guard),
                    'feasibility':feasibility,'facts':[],'receipts':{}}
                lookup=self.store.lookup(c['left'],c['right'],guard,current,prepared)
            else:
                lookup=targeted_lookup(self.store,authority,c['left'],c['right'],guard,prepared,
                                       self.name!='egg_cache',kind='ordinary' if ordinary else 'egg')
            initial[c['id']]=lookup
            if lookup['proved']:
                verdicts[c['id']]={'relation':'equivalent','via':'identity' if lookup['status']=='identity' else 'history',
                                    'history_scope':lookup['status'] if lookup['status']!='identity' else None}
        pending=[c for c in batch if c['id'] not in verdicts]
        triaged={}
        if self.triage:
            for c in pending:
                if any(b['status']=='sat' for b in initial[c['id']]['blocked']):
                    result=_typed(self.solver,c,old_rows.get(c['id'],{}).get('triage'))
                    triaged[c['id']]=result
                    if result['relation'] in ('strengthened','weakened','incomparable'):
                        verdicts[c['id']]={'relation':result['relation'],'via':'triage_typed'}
            pending=[c for c in pending if c['id'] not in verdicts]
        if pending and not eager:
            evidence=authority.discover(prepared,guard)
            require(evidence['feasibility']['status']=='sat','guard feasibility changed')
            for c in pending:
                # Same full-forest lookup as eager Egg after a targeted miss.
                lookup=(targeted_lookup(self.store,authority,c['left'],c['right'],guard,prepared,False,kind='ordinary')
                        if ordinary else self.store.lookup(c['left'],c['right'],guard,evidence,prepared))
                second[c['id']]=lookup
                if lookup['proved']:
                    verdicts[c['id']]={'relation':'equivalent','via':'forest_history','history_scope':lookup['status']}
            pending=[c for c in pending if c['id'] not in verdicts]
        native=None
        if pending and not ordinary:
            native,pairs,proofs=self._native(prepared,evidence,source_ids,pending,replay)
            by_id={v:k for k,v in source_ids.items()}
            for c in pending:
                pair=pairs[frozenset((source_ids[c['left']],source_ids[c['right']]))]
                proof=proofs[pair]
                if proof['proved']:
                    ident=self.store.add(by_id[pair[0]],by_id[pair[1]],guard,evidence,prepared,proof)
                    verdict={'relation':'equivalent','via':'native_proof','proof':proof,'proof_id':ident,'graph_pair':list(pair)}
                else:
                    result=triaged.get(c['id'])
                    if result is None or result['relation']=='unknown':
                        result=_typed(self.solver,c,old_rows.get(c['id'],{}).get('smt'))
                    verdict={'relation':result['relation'],'via':'typed_fallback','proof':proof,
                             'proof_id':None,'graph_pair':list(pair),'smt':result}
                verdicts[c['id']]=verdict
        if pending and ordinary:
            session=CoreSession(prepared,evidence,self.boolean)
            for c in pending:
                old=old_rows.get(c['id'],{})
                core=session.compare(c['left'],c['right'],old.get('core') if replay is not None else None)
                if all(item['status']=='unsat' for item in core.values()):
                    ident=self.store.add(c,prepared,evidence,core)
                    verdict={'relation':'equivalent','via':'ordinary_core','core':core,'proof_id':ident}
                elif c['id'] in triaged and triaged[c['id']]['relation']=='equivalent':
                    # A full typed result is already available. Preserve this
                    # exact-scope result without another directional query.
                    ident=self.store.add_exact(c)
                    verdict={'relation':'equivalent','via':'typed_fallback','core':core,'typed_directions':{},
                             'proof_id':ident}
                else:
                    directions={};statuses={}
                    for direction,a,b in (('old_only',c['left'],c['right']),('new_only',c['right'],c['left'])):
                        if core[direction]['status']=='unsat':statuses[direction]='unsat'
                        else:
                            rec=_direction(self.solver,a,b,guard,old.get('typed_directions',{}).get(direction))
                            directions[direction]=rec;statuses[direction]=rec['direction']['status']
                    relation=classify(statuses['old_only'],statuses['new_only'])
                    ident=self.store.add_exact(c) if relation=='equivalent' else None
                    verdict={'relation':relation,'via':'typed_fallback','core':core,'typed_directions':directions,'proof_id':ident}
                verdicts[c['id']]=verdict
        rows=[{'id':c['id'],**verdicts[c['id']],'lookup':initial[c['id']],
               'forest_lookup':second.get(c['id']),**({'triage':triaged[c['id']]} if c['id'] in triaged else {})} for c in batch]
        return {'prepared':prepared,'feasibility':feasibility,'fact_events':authority.events,'native':native,'rows':rows}

    def group(self,batch,replay=None):
        start=time.perf_counter()
        result=self._direct(batch,replay) if self.memory else self._assisted(batch,replay)
        self.wall+=time.perf_counter()-start
        if replay is not None:
            require(result==replay, f'{self.name}: archived group evidence differs from independent replay')
        for c, r in zip(batch,result['rows'],strict=True):
            require(c['id']==r['id'], 'request order changed')
            self.rows.append((c,r))
        return result

    def summary(self):
        rows=self.rows;facts=dict(self.authority.counts) if self.authority else {}
        primitive=sum(facts.get(k,0) for k in ('guard_misses','full_misses','dependency_misses'))
        equivalents=[(c,r) for c,r in rows if c['expected_relation']=='equivalent' and c['left']!=c['right']]
        proof_routes=('history','forest_history','native_proof','ordinary_core')
        reuse=[r for c,r in rows if r['via'] in ('history','forest_history')]
        stores=self.memory.entries if self.memory else self.store.entries
        counts={'requests':len(rows),'correct':sum(c['expected_relation']==r['relation'] for c,r in rows),
                'false_equivalent':sum(c['expected_relation']!='equivalent' and r['relation']=='equivalent' for c,r in rows),
                'via':dict(Counter(r['via'] for c,r in rows)),
                'nonidentity_equivalent':len(equivalents),
                'nonidentity_equivalent_without_full_target_solver':sum(r['via'] not in ('typed_smt','typed_fallback') and 'triage' not in r for c,r in equivalents),
                'nonidentity_equivalent_with_proof_route':sum(r['via'] in proof_routes for c,r in equivalents),
                'history_scope':dict(Counter(r['history_scope'] for r in reuse)),
                'first_lookup_status':dict(Counter(r['lookup']['status'] for c,r in rows if 'lookup' in r)),
                'forest_lookup_status':dict(Counter(r['forest_lookup']['status'] for c,r in rows if r.get('forest_lookup') is not None)),
                'reuse_path_lengths':dict(Counter(str(len((r['forest_lookup'] if r['via']=='forest_history' else r['lookup'])['edges'])) for r in reuse)),
                'typed_solver_counts':dict(self.solver.counts),'fact_counts':facts,
                'boolean_checks':dict(self.boolean),'native_graph_counts':dict(self.graphs),
                'fact_typed_checks':primitive,'all_typed_checks':primitive+self.solver.counts['solver_checks'],
                'store_entries':len(stores),'store_dependency_count':sum(len(r.get('dependencies',[])) for r in stores.values()),
                'wall_seconds':self.wall,'native_timing':dict(self.timing)}
        if self.triage:
            counts['triage_checked']=sum('triage' in r for _,r in rows)
            counts['triage_relation_counts']=dict(Counter(r['triage']['relation'] for _,r in rows if 'triage' in r))
            counts['triage_discharge']=sum(r['via']=='triage_typed' for _,r in rows)
        return counts


def protocol(archive,live_archive,binary_sha,suites,*,triage=False):
    return {'schema':1,'protocol_sha256':digest(TRIAGE_PROTOCOL if triage else PROTOCOL),'archive_sha256':digest(archive),
            'live_archive_sha256':digest(live_archive),'binary_sha256':binary_sha,
            'arms':list(TRIAGE_ARMS if triage else ARMS),'rules':PATTERN_RULES,'workloads':suites,
            'group_policy':'round/property/guard; isolated workload and arm state'}


def without_times(summary):
    """Operational counters/relations are reproducible; timings are not."""
    return {k:{a:{m:v for m,v in row.items() if m not in ('wall_seconds','native_timing')}
               for a,row in value.items()} for k,value in summary['workloads'].items()}


def run(archive,live_archive,binary,output,*,replay_dir=None,triage=False):
    archive=Path(archive);live_archive=Path(live_archive);output=Path(output)
    start=time.perf_counter();suites=plan(archive,live_archive);source_seconds=time.perf_counter()-start
    replay=replay_dir is not None;arm_names=TRIAGE_ARMS if triage else ARMS
    if replay:
        root=Path(replay_dir);frozen=read(root/'protocol.json');binary_sha=frozen['binary_sha256']
        require(frozen==protocol(archive,live_archive,binary_sha,suites,triage=triage),'frozen workload/protocol changed')
        saved=iter(map(loads,gzip.open(root/'groups.jsonl.gz','rt',encoding='utf8')))
    else:
        binary=Path(binary).resolve(strict=True);binary_sha=digest(binary)
        output.mkdir(parents=True,exist_ok=False);dump(output/'protocol.json',protocol(archive,live_archive,binary_sha,suites,triage=triage))
        stream=gzip.open(output/'groups.jsonl.gz','wt',encoding='utf8')
    results,stores={},{ };oracle_seconds=0.0;group_total=0;request_total=0
    try:
        for workload, cases in suites.items():
            arms={a:Arm(a,binary) for a in arm_names}
            for group_index,(key,batch) in enumerate(groups(cases),1):
                group_total+=1;request_total+=len(batch)
                expected=next(saved) if replay else None
                if expected is not None:
                    require(expected['workload']==workload and expected['group']==group_index and
                            expected['key']==list(key) and expected['cases']==batch,'group order/source changed')
                record={'workload':workload,'group':group_index,'key':list(key),'cases':batch,'arms':{}}
                for name,arm in arms.items():
                    record['arms'][name]=arm.group(batch,expected['arms'][name] if replay else None)
                # Oracle is deliberately evaluated after operational choices and
                # its answers are never passed to a solver/cache or proof store.
                record['oracles']=[]
                for i,c in enumerate(batch):
                    start=time.perf_counter()
                    if replay:
                        verdict=expected['oracles'][i]
                        require(verify_result(c['left'],c['right'],c['guard'],verdict),'archived oracle mismatch')
                    else:verdict=fresh_compare(c['left'],c['right'],c['guard'])
                    oracle_seconds+=time.perf_counter()-start
                    require(verdict['relation']==c['expected_relation'],f'frozen label mismatch: {workload}/{c["id"]}')
                    for name,data in record['arms'].items():
                        require(data['rows'][i]['relation']==verdict['relation'],f'{name}: wrong classification {workload}/{c["id"]}')
                    record['oracles'].append(verdict)
                if replay:require(record==expected,'archived group schema/evidence mismatch')
                else:stream.write(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n');stream.flush()
            results[workload]={name:arm.summary() for name,arm in arms.items()}
            stores[workload]={name:arm.memory.entries if arm.memory else arm.store.entries for name,arm in arms.items()}
            print(f'{workload}: {len(cases)} comparisons; all {len(arm_names)} arms match fresh oracle',flush=True)
    finally:
        if not replay:stream.close()
    summary={'complete':True,'new_api_calls':0,'requests':request_total,'groups':group_total,
             'source_validation_seconds':source_seconds,'offline_oracle_seconds':oracle_seconds,
             'workloads':results,'scope':'Free typed two-state monitor snapshots; no sequential RTL or LLM-quality claim.'}
    if replay:
        require(next(saved,None) is None and stores==read(root/'stores.json'),'extra groups or mismatched final proof store')
        prior=read(root/'summary.json')
        require(without_times(summary)==without_times(prior) and all(summary[k]==prior[k] for k in ('complete','new_api_calls','requests','groups','scope')),
                'archived accounting differs from independently replayed operations')
        result={'complete':True,'new_api_calls':0,'requests':request_total,'groups':group_total,
                'arms':list(arm_names),'same_non_timing_summary':True,'all_stores_rebuilt':True,
                'native_search_invoked':False,'source_validation_seconds':source_seconds,'offline_oracle_seconds':oracle_seconds,
                'evidence_sha256':{f:digest(root/f) for f in ('protocol.json','groups.jsonl.gz','stores.json','summary.json')}}
        with output.open('x',encoding='utf8') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        return result
    dump(output/'stores.json',stores);dump(output/'summary.json',summary)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,default=ARCHIVE);parser.add_argument('--live-archive',type=Path,default=LIVE_ARCHIVE)
    parser.add_argument('--binary',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--triage',action='store_true',help='separately frozen post-primary typed-triage ablation')
    args=parser.parse_args();run(args.archive,args.live_archive,args.binary,args.output,triage=args.triage)
