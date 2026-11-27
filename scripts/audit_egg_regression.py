#!/usr/bin/env python3
"""Audit an archived versioned-monitor regression run without invoking native egg.

Reconstruct all requests from the frozen source archive, independently re-solve
typed premises and directional classifications, replay native derivations and
current-scope reuse edges, and reconstruct proof-store history. This validates
logical evidence and accounting; it does not repeat native search or timings.
"""
import argparse
from collections import Counter, defaultdict, deque
import gzip
from hashlib import sha256
import json
import math
from pathlib import Path
import time

from egg_regression_workload import ARCHIVE, workload
from egg_regression_facts import prepare, verify, OrdinarySession
from egg_regression_check import PATTERN_RULES, check_graph
from egg_regression_reuse import ProofStore, verify_reuse
from egg_regression_smt import classify, verify_direction, verify_result
from egg_txn_terms import format_term, parse_term
from predicates import ROOT

ARMS = ('smt', 'ordinary', 'pairwise_egg', 'shared_egg')
PROTOCOL = ROOT/'docs/egg_regression_protocol.md'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def no_duplicates(items):
    out = {}
    for key, value in items:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def loads(text):
    return json.loads(text, object_pairs_hook=no_duplicates)


def read(path):
    return loads(Path(path).read_text(encoding='utf8'))


def fields(value, names, message):
    require(isinstance(value, dict) and set(value) == set(names), message)


def canonical(text):
    return format_term(parse_term(text))


def groups(cases):
    grouped = {}
    require(len({case['id'] for case in cases}) == len(cases), 'unexpected duplicate source requests')
    for case in cases:
        grouped.setdefault((case['round'], case['property'], case['guard']), []).append(case)
    return list(grouped.items())


def native_payload(prepared, evidence, source_ids, pairs):
    ids = {v for pair in pairs for v in pair}
    targets = [{'id': source_ids[source], 'compact': compact, 'event_context': evidence['context_id']}
               for source, compact in zip(prepared['sources'], prepared['abstracts'], strict=True)
               if source_ids[source] in ids]
    return dict(context_id=evidence['context_id'], targets=targets,
                pairs=[list(pair) for pair in pairs], pattern_rules=PATTERN_RULES,
                ground_rules=evidence['facts'])


class PriorConnectivity:
    """Audit paths using only already established equations in this exact guard."""
    def __init__(self):
        self.adj = defaultdict(lambda: defaultdict(list))

    def path(self, case):
        left, right = canonical(case['left']), canonical(case['right'])
        if left == right:
            return []
        graph = self.adj[case['guard']]
        visited = {left}
        queue = deque([(left, [])])
        while queue:
            node, path = queue.popleft()
            for nxt, edge in graph[node]:
                if nxt not in visited:
                    if nxt == right:
                        return path + [edge]
                    visited.add(nxt)
                    queue.append((nxt, path + [edge]))
        return None

    def remember(self, case):
        left, right = canonical(case['left']), canonical(case['right'])
        if left != right:
            graph = self.adj[case['guard']]
            graph[left].append((right, case['id']))
            graph[right].append((left, case['id']))


class QueryAccounting:
    """Recount actual queries based on canonical typed solver keys/receipts."""
    def __init__(self):
        self.counts = dict.fromkeys(('compare_calls', 'solver_checks', 'guard_checks',
                                     'direction_checks', 'cache_hits', 'guard_cache_hits',
                                     'solver_groups'), 0)
        self.guards, self.directions, self.groups = set(), set(), set()

    def guard(self, guard, status):
        if guard not in self.groups:
            self.groups.add(guard)
            self.counts['solver_groups'] += 1
        if guard in self.guards:
            self.counts['guard_cache_hits'] += 1
        else:
            self.counts['guard_checks'] += 1
            self.counts['solver_checks'] += 1
            if status != 'unknown':
                self.guards.add(guard)

    def direction(self, guard, left, right, status):
        key = (guard, left, right)
        if key in self.directions:
            self.counts['cache_hits'] += 1
        else:
            self.counts['direction_checks'] += 1
            self.counts['solver_checks'] += 1
            if status != 'unknown':
                self.directions.add(key)

    def full(self, receipt):
        self.counts['compare_calls'] += 1
        self.guard(receipt['guard'], receipt['guard_status'])
        if receipt['guard_status'] == 'sat':
            for k, left, right in (('old_only', receipt['left'], receipt['right']),
                                    ('new_only', receipt['right'], receipt['left'])):
                self.direction(receipt['guard'], left, right, receipt['directions'][k]['status'])

    def single(self, receipt):
        self.guard(receipt['guard'], receipt['guard_query']['status'])
        if receipt['guard_query']['status'] == 'sat':
            self.direction(receipt['guard'], receipt['left'], receipt['right'],
                           receipt['direction']['status'])


def audit_smt(case, receipt, accounting):
    require(verify_result(case['left'], case['right'], case['guard'], receipt),
            'typed query receipt failed verification')
    accounting.full(receipt)
    return receipt['relation']


def verify_fallback(case, record, accounting, abstract=None):
    """Verify a complete typed receipt or a one-direction hybrid fallback.

    An ordinary abstract UNSAT may discharge a direction. Abstract SAT is
    never taken as a concrete difference: the remaining directions must have
    standalone exact typed receipts.
    """
    if abstract is None:
        require('smt' in record, 'native miss lacks complete typed fallback receipt')
        return audit_smt(case, record['smt'], accounting), {'smt'}
    # The hybrid record is accepted only with an independently replayed
    # ordinary session and individually checked typed query receipts.
    require(abstract is not None and 'typed_directions' in record, 'missing typed fallback receipt')
    typed = record['typed_directions']
    statuses = {}
    needed = {k for k in ('old_only', 'new_only') if abstract[k] != 'unsat'}
    require(isinstance(typed, dict) and set(typed) == needed, 'wrong hybrid fallback direction set')
    for name, left, right in (('old_only', case['left'], case['right']),
                              ('new_only', case['right'], case['left'])):
        if name not in needed:
            statuses[name] = 'unsat'
        else:
            rec = typed[name]
            require(verify_direction(left, right, case['guard'], rec), 'invalid typed direction')
            accounting.single(rec)
            statuses[name] = rec['direction']['status']
    return classify(statuses['old_only'], statuses['new_only']), {'typed_directions'}


def audit_baseline(case, record, memory, accounting, *, ordinary_session=None, prepared=None):
    path = memory.path(case)
    if path is not None:
        require(record == {'relation': 'equivalent', 'via': 'identity' if not path else 'connectivity',
                           'path': path}, 'invalid prefix-only baseline connectivity path')
        return
    if ordinary_session is None:
        fields(record, ('relation', 'via', 'smt'), 'invalid direct SMT arm schema')
        require(record['via'] == 'typed_smt' and
                record['relation'] == audit_smt(case, record['smt'], accounting),
                'direct SMT arm receipt mismatch')
    else:
        compact = dict(zip(prepared['sources'], prepared['abstracts'], strict=True))
        abstract = ordinary_session.compare(compact[case['left']], compact[case['right']])
        require(abstract == record.get('abstract'), 'ordinary common-facts replay mismatch')
        if abstract['old_only'] == abstract['new_only'] == 'unsat':
            require(record == {'relation': 'equivalent', 'via': 'common_facts', 'abstract': abstract},
                    'invalid ordinary proof arm')
        else:
            relation, extra = verify_fallback(case, record, accounting, abstract)
            fields(record, {'relation', 'via', 'abstract'} | extra, 'invalid ordinary fallback schema')
            require(record['via'] == 'typed_fallback' and record['relation'] == relation,
                    'ordinary typed fallback mismatch')
    if record['relation'] == 'equivalent':
        memory.remember(case)


def audit_native_arm(case, record, proof, accounting, extras):
    require(record.get('proof') == proof, 'native per-pair proof replay mismatch')
    if proof['proved']:
        fields(record, {'relation', 'via', 'proof'} | set(extras), 'invalid checked native proof arm')
        require(record['relation'] == 'equivalent' and record['via'] ==
                ('identity' if proof['status'] == 'structural_identity' else 'egg_proof'),
                'native proved pair not classified as equivalent')
    else:
        relation, receipt_keys = verify_fallback(case, record, accounting)
        fields(record, {'relation', 'via', 'proof'} | receipt_keys | set(extras),
               'invalid native fallback schema')
        require(record['via'] == 'typed_fallback' and record['relation'] == relation,
                'native fallback directional evidence mismatch')
    require(all(record[k] == v for k, v in extras.items()), 'native proof-store metadata mismatch')


def count_graph(counter, graph, proofs):
    counter.update(graphs=1, requested_pairs=len(proofs),
                   proved_pairs=sum(p['proved'] for p in proofs.values()),
                   checked_steps=sum(len(p['steps']) for p in proofs.values()))
    if graph is None:
        counter['timeout'] += 1
    else:
        counter.update(enodes_sum=graph['enodes'], iterations_sum=graph['iterations'],
                       targets_sum=len(graph['targets']))
        counter['stop_'+graph['stop_reason'].split('(')[1]] += 1


def summary_cohorts(records):
    by_cohort = defaultdict(list)
    for row in records:
        by_cohort[row['case']['cohort']].append(row)
        by_cohort['all'].append(row)
    result = {}
    for name, rows in by_cohort.items():
        cohort = dict(requests=len(rows),
                      different_strings=sum(row['case']['left'] != row['case']['right'] for row in rows),
                      oracle=dict(Counter(row['oracle']['relation'] for row in rows)), arms={})
        for arm in ARMS:
            answers = [(r['arms'][arm], r['oracle']['relation'], r['case']) for r in rows]
            counts = dict(correct=sum(a['relation'] == oracle for a, oracle, _ in answers),
                          via=dict(Counter(a['via'] for a, _, _ in answers)),
                          nonidentity_equivalent=sum(c['left'] != c['right'] and a['relation'] == 'equivalent'
                                                     for a, _, c in answers),
                          fallback_equivalent=sum(a['via'] == 'typed_fallback' and a['relation'] == 'equivalent'
                                                  for a, _, _ in answers),
                          false_equivalent=sum(a['relation'] == 'equivalent' and oracle != 'equivalent'
                                               for a, oracle, _ in answers))
            if arm == 'shared_egg':
                counts['reuse_lookup'] = dict(Counter(a['reuse']['status'] for a, _, _ in answers if 'reuse' in a))
                counts['path_lengths'] = dict(Counter(str(len(a['reuse']['edges'])) for a, _, _ in answers
                                                     if a.get('reuse',{}).get('proved') and a['reuse']['edges']))
            cohort['arms'][arm] = counts
        result[name] = cohort
    return result


def audit(run_dir, archive=ARCHIVE):
    start = time.perf_counter()
    run_dir, archive = Path(run_dir), Path(archive)
    cases = workload(archive)
    proto = read(run_dir/'protocol.json')
    fields(proto, ('schema', 'archive_sha256', 'protocol_sha256', 'binary_sha256', 'requests',
                   'rules', 'group_policy'), 'bad protocol schema')
    require(proto['schema'] == 1 and proto['archive_sha256'] == digest(archive) and
            proto['protocol_sha256'] == digest(PROTOCOL) and proto['requests'] == cases and
            proto['rules'] == PATTERN_RULES and proto['group_policy'] == 'round/property/guard',
            'protocol does not bind frozen workload, source archive, or rules')
    require(isinstance(proto['binary_sha256'], str) and len(proto['binary_sha256']) == 64
            and all(c in '0123456789abcdef' for c in proto['binary_sha256']), 'malformed native provenance hash')

    facts_cache = {}
    facts_totals = Counter()
    graphs = {a: Counter() for a in ('pairwise_egg', 'shared_egg')}
    accounting = {a: QueryAccounting() for a in ARMS}
    memories = {a: PriorConnectivity() for a in ('smt', 'ordinary')}
    store = ProofStore()
    records = []
    by_group = groups(cases)
    with gzip.open(run_dir/'groups.jsonl.gz', 'rt', encoding='utf8') as stream:
        for group_id, ((round_no, prop, guard), batch) in enumerate(by_group, 1):
            line = stream.readline()
            require(line, f'missing expected group {group_id}')
            g = loads(line)
            fields(g, ('id', 'round', 'property', 'guard', 'prepared', 'facts_prepared', 'evidence',
                       'pairwise_graphs', 'shared_graph', 'requests'), 'invalid group schema')
            require((g['id'], g['round'], g['property'], g['guard']) ==
                    (group_id, round_no, prop, guard), 'group identity or order changed')
            sources = list(dict.fromkeys(s for c in batch for s in (c['left'], c['right'])))
            prepared = prepare(sources)
            require(g['prepared'] == prepared, 'typed binding differs from source archive')
            identities_only = all(parse_term(c['left']) == parse_term(c['right']) for c in batch)
            facts_prepared = prepare(['true']) if identities_only else prepared
            require(g['facts_prepared'] == facts_prepared, 'invalid minimal identity fact-discovery source')
            evidence = g['evidence']
            require(verify(facts_prepared, guard, evidence, cache=facts_cache),
                    'common typed facts failed independent verification')
            require(evidence['feasibility']['status'] == 'sat', 'infeasible frozen group')
            facts_totals.update(evidence['counts'])
            facts_totals.update(groups=1, fact_occurrences=len(evidence['facts']))
            ordinary_session = None if identities_only else OrdinarySession(prepared, evidence)
            source_ids = {s: f't{i:03}' for i,s in enumerate(sources)}
            by_id = {v:k for k,v in source_ids.items()}
            rows = g['requests']
            require(isinstance(rows, list) and len(rows) == len(batch), 'incorrect request count in group')
            native_pairs = iter(g['pairwise_graphs'])
            pending = {}
            # All shared lookups refer only to the store *before* this group.
            # Even an earlier row in this batch cannot authorize a later lookup.
            for case, row in zip(batch, rows, strict=True):
                fields(row, ('case', 'oracle', 'arms'), 'invalid request row schema')
                require(row['case'] == case, 'request missing, substituted or reordered')
                require(verify_result(case['left'], case['right'], guard, row['oracle']), 'invalid full-width oracle receipt')
                require(row['oracle']['relation'] == case['expected_relation'], 'independent oracle disagrees with frozen label')
                fields(row['arms'], ARMS, 'missing or extra experiment arm')
                for arm, record in row['arms'].items():
                    require(record['relation'] == row['oracle']['relation'],
                            f'{arm}: classification disagrees with independently verified oracle')
                audit_baseline(case, row['arms']['smt'], memories['smt'], accounting['smt'])
                audit_baseline(case, row['arms']['ordinary'], memories['ordinary'], accounting['ordinary'],
                               ordinary_session=ordinary_session, prepared=prepared)
                pair = (source_ids[case['left']], source_ids[case['right']])
                pairwise = row['arms']['pairwise_egg']
                if parse_term(case['left']) == parse_term(case['right']):
                    require(pairwise == {'relation':'equivalent', 'via':'identity'}, 'false pairwise identity')
                else:
                    saved = next(native_pairs, None)
                    fields(saved, ('request_id', 'payload', 'graph'), 'missing or malformed pairwise native graph')
                    req = native_payload(prepared, evidence, source_ids, [pair])
                    require(saved['request_id'] == case['id'] and saved['payload'] == req,
                            'pairwise native graph detached from exact request endpoints')
                    proofs = check_graph(req, saved['graph'])
                    count_graph(graphs['pairwise_egg'], saved['graph'], proofs)
                    audit_native_arm(case, pairwise, proofs[pair], accounting['pairwise_egg'], {})
                reuse = row['arms']['shared_egg']['reuse']
                require(verify_reuse(case['left'], case['right'], guard, evidence, prepared, reuse, store.entries),
                        'shared proof failed independent current-context replay')
                require(reuse == store.lookup(case['left'], case['right'], guard, evidence, prepared),
                        'reuse lookup differs from deterministic prior-group store')
                if not reuse['proved']:
                    require(pair[0] != pair[1], 'structural identity not recovered')
                    pending.setdefault(frozenset(pair), pair)
            require(next(native_pairs, None) is None, 'unexpected extra pairwise graph')
            shared_proofs = {}
            saved = g['shared_graph']
            if pending:
                fields(saved, ('payload', 'graph'), 'missing shared native graph')
                req = native_payload(prepared, evidence, source_ids, list(pending.values()))
                require(saved['payload'] == req, 'shared graph pair inventory or endpoint binding changed')
                shared_proofs = check_graph(req, saved['graph'])
                count_graph(graphs['shared_egg'], saved['graph'], shared_proofs)
            else:
                require(saved is None, 'unexpected shared native graph')
            for case, row in zip(batch, rows, strict=True):
                record = row['arms']['shared_egg']; reuse = record['reuse']
                if reuse['proved']:
                    require(record == {'relation':'equivalent', 'via':'identity' if not reuse['edges'] else 'proof_reuse',
                                       'reuse':reuse}, 'invalid reused-proof classification')
                else:
                    chosen = pending[frozenset((source_ids[case['left']], source_ids[case['right']]))]
                    proof = shared_proofs[chosen]
                    pid = store.add(by_id[chosen[0]], by_id[chosen[1]], guard, evidence, prepared, proof) if proof['proved'] else None
                    audit_native_arm(case, record, proof, accounting['shared_egg'],
                                     {'reuse': reuse, 'proof_id': pid, 'graph_pair': list(chosen)})
                records.append(row)
        require(stream.readline() == '', 'unexpected extra group')
    require(read(run_dir/'proof_store.json') == store.entries, 'stored proof inventory differs from replayed history')
    summary = read(run_dir/'summary.json')
    require(summary.get('complete') is True and summary.get('new_api_calls') == 0, 'unexpected completion/API declaration')
    cohorts = summary_cohorts(records)
    require(summary.get('cohorts') == cohorts, 'cohort metrics do not match audited evidence')
    actual_counts = {a: x.counts for a,x in accounting.items()}
    require(summary.get('typed_operational_counts') == actual_counts, 'typed query accounting mismatch')
    require(summary.get('common_fact_counts') == dict(facts_totals), 'common-fact accounting mismatch')
    graphs_summary = {a: dict(x) for a,x in graphs.items()}
    require(summary.get('graphs') == graphs_summary, 'graph accounting mismatch')
    require(summary.get('proof_store_entries') == len(store.entries), 'proof store size counter mismatch')
    wall = summary.get('wall_seconds')
    require(isinstance(wall, dict) and all(type(v) in (int,float) and math.isfinite(v) and v >= 0 for v in wall.values()),
            'invalid runtime counter')
    return {'complete': True, 'new_api_calls': 0, 'native_reruns': 0, 'groups': len(by_group),
            'requests': len(records), 'cohorts': cohorts, 'typed_operational_counts': actual_counts,
            'common_fact_counts': dict(facts_totals), 'graphs': graphs_summary,
            'proof_store_entries': len(store.entries), 'evidence_sha256':
            {name:digest(run_dir/name) for name in ('protocol.json','groups.jsonl.gz','proof_store.json','summary.json')},
            'audit_seconds': time.perf_counter()-start, 'limitations': [
                'Logical evidence and deterministic request accounting audited independently of native search.',
                'Native graph search counters and elapsed time cannot be independently proven by replay.',
                'Offline replay of recorded outputs; typed snapshots do not establish RTL reachability.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-dir', required=True, type=Path)
    p.add_argument('--archive', default=ARCHIVE, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    report = audit(a.run_dir, a.archive)
    with a.output.open('x', encoding='utf8') as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(f"Audited {report['requests']} requests in {report['groups']} groups; {report['proof_store_entries']} proof-store entries.")
