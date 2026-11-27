#!/usr/bin/env python3
"""Replay versioned RTL monitor changes: exact SMT, ordinary facts, pairwise and shared egg.

No provider calls. Native graph output is not trusted: every equivalence used for
reuse is supported by an independently replayed derivation plus scoped typed facts.
"""
import argparse
from collections import Counter, defaultdict, deque
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

from egg_regression_workload import workload
from egg_regression_facts import prepare, certify, OrdinarySession
from egg_regression_check import check_graph, PATTERN_RULES
from egg_regression_smt import IncrementalSMT, fresh_compare, classify
from egg_regression_reuse import ProofStore
from egg_txn_terms import parse_term
from predicates import ROOT

ARMS = ('smt', 'ordinary', 'pairwise_egg', 'shared_egg')
ARCHIVE = ROOT/'results/milestone3/frame-txn-live/transcript.tar.gz'
PROTOCOL = ROOT/'docs/egg_regression_protocol.md'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')


def groups(cases):
    by = {}
    require(len({c['id'] for c in cases}) == len(cases), 'duplicate request IDs')
    for c in cases:
        by.setdefault((c['round'], c['property'], c['guard']), []).append(c)
    return [(key, rows) for key, rows in by.items()]


class EqualityMemory:
    """Strong non-egg baseline: transitive exact-scope connectivity of accepted equivalences."""
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(list))

    @staticmethod
    def key(text):
        return parse_term(text)

    def lookup(self, left, right, guard):
        a, b = self.key(left), self.key(right)
        if a == b:
            return []
        graph = self.graph[guard]
        todo = deque([(a, [])]); seen = {a}
        while todo:
            node, path = todo.popleft()
            for other, edge in graph[node]:
                if other in seen:
                    continue
                route = path + [edge]
                if other == b:
                    return route
                seen.add(other); todo.append((other, route))
        return None

    def add(self, left, right, guard, ident):
        a, b = self.key(left), self.key(right)
        if a != b:
            self.graph[guard][a].append((b, ident))
            self.graph[guard][b].append((a, ident))


def payload(prepared, evidence, source_ids, ordered_pairs):
    index = dict(zip(prepared['sources'], prepared['abstracts'], strict=True))
    keys = {k for pair in ordered_pairs for k in pair}
    targets = [{'id': ident, 'compact': index[s], 'event_context': evidence['context_id']}
               for s, ident in source_ids.items() if ident in keys]
    return {'context_id': evidence['context_id'], 'targets': targets, 'pairs': [list(t) for t in ordered_pairs],
            'pattern_rules': PATTERN_RULES, 'ground_rules': evidence['facts']}


def invoke(request, binary, time_counter, arm):
    start = time.perf_counter()
    try:
        proc = subprocess.run([str(binary)], input=json.dumps(request), text=True, capture_output=True,
                              check=True, timeout=30)
        graph = json.loads(proc.stdout)
    except subprocess.TimeoutExpired:
        graph = None
    time_counter[arm+'_native'] += time.perf_counter()-start
    start = time.perf_counter()
    proofs = check_graph(request, graph)
    time_counter[arm+'_replay'] += time.perf_counter()-start
    return graph, proofs


def _orientation(case, source_ids):
    l, r = source_ids[case['left']], source_ids[case['right']]
    return l, r


def exact_record(case, solver, via='typed_smt'):
    result = solver.compare(case['left'], case['right'], case['guard'])
    return {'relation': result['relation'], 'via': via, 'smt': result}


def ordinary_record(case, prepared, session, memory, solver):
    lhs, rhs, guard = case['left'], case['right'], case['guard']
    path = memory.lookup(lhs, rhs, guard)
    if path is not None:
        return {'relation': 'equivalent', 'via': 'identity' if not path else 'connectivity', 'path': path}
    index = dict(zip(prepared['sources'], prepared['abstracts'], strict=True))
    abstract = session.compare(index[lhs], index[rhs])
    if abstract['old_only'] == abstract['new_only'] == 'unsat':
        rec = {'relation': 'equivalent', 'via': 'common_facts', 'abstract': abstract}
    else:
        # Preserve the independently proven directions; only check typed SAT/unknown directions.
        directions={}; statuses={}
        for name, a, b in (('old_only',lhs,rhs),('new_only',rhs,lhs)):
            if abstract[name]=='unsat':
                statuses[name]='unsat'
            else:
                directions[name]=solver.check_direction(a,b,guard)
                statuses[name]=directions[name]['direction']['status']
        rec={'relation':classify(statuses['old_only'],statuses['new_only']),
             'via':'typed_fallback','abstract':abstract,'typed_directions':directions}
    if rec['relation'] == 'equivalent':
        memory.add(lhs, rhs, guard, case['id'])
    return rec


def direct_record(case, memory, solver):
    lhs, rhs, guard = case['left'], case['right'], case['guard']
    path = memory.lookup(lhs, rhs, guard)
    if path is not None:
        return {'relation': 'equivalent', 'via': 'identity' if not path else 'connectivity', 'path': path}
    rec = exact_record(case, solver)
    if rec['relation'] == 'equivalent':
        memory.add(lhs, rhs, guard, case['id'])
    return rec


def proof_record(case, proof, solver, **extra):
    if proof['proved']:
        return {'relation': 'equivalent', 'via': 'identity' if proof['status']=='structural_identity' else 'egg_proof',
                'proof': proof, **extra}
    return {**exact_record(case, solver, 'typed_fallback'), 'proof': proof, **extra}


def summarize(records, solvers, time_counter, facts_totals, graph_totals, entries):
    counts = {}
    for name in (*sorted({r['case']['cohort'] for r in records}), 'all'):
        rows = [r for r in records if name=='all' or r['case']['cohort']==name]
        result = {'requests': len(rows), 'different_strings': sum(r['case']['left']!=r['case']['right'] for r in rows),
                  'oracle': dict(Counter(r['oracle']['relation'] for r in rows)), 'arms': {}}
        for arm in ARMS:
            items = [r['arms'][arm] for r in rows]
            result['arms'][arm] = {'correct': sum(a['relation']==r['oracle']['relation'] for a,r in zip(items,rows,strict=True)),
                'via': dict(Counter(a['via'] for a in items)),
                'nonidentity_equivalent':sum(r['case']['left']!=r['case']['right'] and a['relation']=='equivalent' for a,r in zip(items,rows,strict=True)),
                'fallback_equivalent':sum(a['via']=='typed_fallback' and a['relation']=='equivalent' for a in items),
                'false_equivalent':sum(a['relation']=='equivalent' and r['oracle']['relation']!='equivalent' for a,r in zip(items,rows,strict=True))}
            if arm=='shared_egg':
                result['arms'][arm]['reuse_lookup'] = dict(Counter(a['reuse']['status'] for a in items if 'reuse' in a))
                result['arms'][arm]['path_lengths'] = dict(Counter(str(len(a['reuse']['edges'])) for a in items if a.get('reuse',{}).get('proved') and a['reuse']['edges']))
        counts[name] = result
    return {'complete': True, 'new_api_calls': 0, 'cohorts': counts,
            'typed_operational_counts':{a:dict(s.counts) for a,s in solvers.items()},
            'common_fact_counts': dict(facts_totals), 'graphs': {k:dict(v) for k,v in graph_totals.items()},
            'proof_store_entries':len(entries), 'wall_seconds':dict(time_counter),
            'limitations':['offline replay of recorded outputs, not live feedback experiment',
                'bounded typed snapshots, not arbitrary temporal SVA or DUT reachability',
                'common fact discovery cost applies to each fact-based arm',
                'shared graphs batched by round/property/guard, checked proof store persists, native graph does not']}


def graph_count(counter, graph, proofs):
    counter['graphs'] += 1; counter['requested_pairs'] += len(proofs)
    counter['proved_pairs'] += sum(p['proved'] for p in proofs.values())
    counter['checked_steps'] += sum(len(p['steps']) for p in proofs.values())
    if graph is not None:
        counter['enodes_sum'] += graph['enodes']; counter['iterations_sum'] += graph['iterations']
        counter['targets_sum'] += len(graph['targets']); counter['stop_'+graph['stop_reason'].split('(')[1]] += 1
    else:
        counter['timeout'] += 1


def run(archive, binary, output):
    archive, binary, output = Path(archive), Path(binary).resolve(strict=True), Path(output)
    cases = workload(archive); output.mkdir(parents=True, exist_ok=False)
    dump(output/'protocol.json', {'schema':1,'archive_sha256':digest(archive),'protocol_sha256':digest(PROTOCOL),
        'binary_sha256':digest(binary),'requests':cases,'rules':PATTERN_RULES,'group_policy':'round/property/guard'})
    solvers = {a: IncrementalSMT() for a in ARMS}
    memories = {a: EqualityMemory() for a in ('smt','ordinary')}
    store = ProofStore(); cache = {}; time_counter=Counter(); facts_totals=Counter()
    graph_totals={a:Counter() for a in ('pairwise_egg','shared_egg')}; records=[]
    with gzip.open(output/'groups.jsonl.gz','wt',encoding='utf8') as stream:
        for group_id,(key,batch) in enumerate(groups(cases),1):
            round_no, prop, guard=key
            start=time.perf_counter()
            sources=list(dict.fromkeys(s for c in batch for s in (c['left'],c['right'])))
            prepared=prepare(sources)
            identities_only=all(parse_term(c['left'])==parse_term(c['right']) for c in batch)
            # Identical revisions need scope feasibility, not primitive discovery.
            facts_prepared=prepare(['true']) if identities_only else prepared
            evidence=certify(facts_prepared,guard,cache)
            require(evidence['feasibility']['status']=='sat','infeasible group in frozen workload')
            time_counter['common_fact_certification']+=time.perf_counter()-start
            facts_totals.update(evidence['counts']); facts_totals['groups']+=1; facts_totals['fact_occurrences']+=len(evidence['facts'])
            source_ids={s:f't{i:03}' for i,s in enumerate(sources)}
            g={'id':group_id,'round':round_no,'property':prop,'guard':guard,'prepared':prepared,'facts_prepared':facts_prepared,'evidence':evidence,
               'pairwise_graphs':[],'shared_graph':None,'requests':[]}
            start=time.perf_counter(); session=None if identities_only else OrdinarySession(prepared,evidence)
            time_counter['ordinary']+=time.perf_counter()-start
            # Fresh oracle grades each request, never supplies operational facts or chooses proof targets.
            for c in batch:
                start=time.perf_counter(); reference=fresh_compare(c['left'],c['right'],guard)
                time_counter['offline_oracle']+=time.perf_counter()-start
                require(reference['relation']==c['expected_relation'],f"frozen relation mismatch {c['id']}: {reference['relation']} != {c['expected_relation']}")
                row={'case':c,'oracle':reference,'arms':{}}
                for arm in ('smt','ordinary'):
                    start=time.perf_counter()
                    row['arms'][arm]=(direct_record(c,memories[arm],solvers[arm]) if arm=='smt' else ordinary_record(c,prepared,session,memories[arm],solvers[arm]))
                    time_counter[arm]+=time.perf_counter()-start
                if parse_term(c['left'])==parse_term(c['right']):
                    row['arms']['pairwise_egg']={'relation':'equivalent','via':'identity'}
                else:
                    pair=_orientation(c,source_ids); req=payload(prepared,evidence,source_ids,[pair])
                    graph,proofs=invoke(req,binary,time_counter,'pairwise_egg'); graph_count(graph_totals['pairwise_egg'],graph,proofs)
                    g['pairwise_graphs'].append({'request_id':c['id'],'payload':req,'graph':graph})
                    start=time.perf_counter(); row['arms']['pairwise_egg']=proof_record(c,proofs[pair],solvers['pairwise_egg'])
                    time_counter['pairwise_egg_fallback']+=time.perf_counter()-start
                start=time.perf_counter(); reuse=store.lookup(c['left'],c['right'],guard,evidence,prepared)
                time_counter['shared_egg_lookup']+=time.perf_counter()-start
                row['lookup']=reuse; g['requests'].append(row)
            # Only pairs not already justified by old checked evidence are sent to native multi-target graph.
            pending={}
            for row in g['requests']:
                if row['lookup']['proved']:
                    continue
                c=row['case']; pair=_orientation(c,source_ids)
                require(pair[0]!=pair[1], 'identity should have a checked reuse result')
                pending.setdefault(frozenset(pair),pair)
            shared_proofs={}
            if pending:
                req=payload(prepared,evidence,source_ids,list(pending.values()))
                graph,shared_proofs=invoke(req,binary,time_counter,'shared_egg'); graph_count(graph_totals['shared_egg'],graph,shared_proofs)
                g['shared_graph']={'payload':req,'graph':graph}
            for row in g['requests']:
                c=row['case']; reuse=row.pop('lookup'); pair=_orientation(c,source_ids)
                start=time.perf_counter()
                if reuse['proved']:
                    # Lookup itself independently checks steps. Replay again in external audit.
                    rec={'relation':'equivalent','via':'identity' if not reuse['edges'] else 'proof_reuse','reuse':reuse}
                else:
                    chosen=pending[frozenset(pair)]; proof=shared_proofs[chosen]
                    # Add the checked path in the actual orientation used by the engine.
                    by_id={v:k for k,v in source_ids.items()}
                    proof_id=store.add(by_id[chosen[0]],by_id[chosen[1]],guard,evidence,prepared,proof) if proof['proved'] else None
                    rec=proof_record(c,proof,solvers['shared_egg'],reuse=reuse,proof_id=proof_id,graph_pair=list(chosen))
                time_counter['shared_egg_finalize']+=time.perf_counter()-start
                row['arms']['shared_egg']=rec
                for arm in ARMS:
                    require(row['arms'][arm]['relation']==row['oracle']['relation'],f"{arm} verdict mismatches oracle for {c['id']}")
                records.append(row)
            stream.write(json.dumps(g,sort_keys=True,separators=(',',':'))+'\n'); stream.flush()
            print(f"{group_id} round={round_no} {prop} {guard}: {len(batch)} requests, {len(pending)} distinct new pairs",flush=True)
    dump(output/'proof_store.json',store.entries)
    summary=summarize(records,solvers,time_counter,facts_totals,graph_totals,store.entries)
    dump(output/'summary.json',summary)
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,default=ARCHIVE); p.add_argument('--binary',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True); a=p.parse_args(); run(a.archive,a.binary,a.output)
