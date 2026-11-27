"""Dependency-first reauthorization of checked scoped monitor proof paths.

Only exact typed primitive obligations are cached; no previous goal verdict is
used to certify a different context. The eager forest and native engine remain
unchanged. These stores are constructed from the verified chronological prefix,
not loaded from arbitrary serialized objects.
"""
from collections import Counter, defaultdict, deque
from copy import deepcopy

import z3

from egg_regression_facts import (SCOPE, SCHEMA_SHA256, _cache_key, _checked_assumptions,
                                  _guard_node, _receipt, certify, context_id, prepare)
from egg_regression_reuse import (_commitment, _digest, _evaluate_edge, _merge_atoms,
                                  _record, _validate_atoms)
from egg_txn_context import TIMEOUT_MS, _proposition
from egg_txn_terms import BV_WIDTHS, format_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import _plain
from predicates import parse


def require(ok, message):
    if not ok:
        raise ValueError(message)


class FactAuthority:
    """One exact-scope typed obligation cache, shared by discovery and rechecks."""

    def __init__(self):
        self.cache = {}
        self.counts = Counter()
        self.events = []

    def start_group(self):
        self.events = []

    def feasibility(self, guard):
        env = z3_env()
        query = z3_term(_guard_node(guard), env)
        key = _cache_key(guard, 'feasibility')
        hit = key in self.cache
        receipt = _receipt(self.cache, key, query, Counter())
        self.counts['guard_requests'] += 1
        self.counts['guard_hits' if hit else 'guard_misses'] += 1
        self.events.append({'kind': 'guard', 'guard': guard, 'cache': 'hit' if hit else 'miss', 'query': receipt})
        return receipt

    def discover(self, prepared, guard):
        evidence = certify(prepared, guard, self.cache)
        self.counts['full_discovery_groups'] += 1
        self.counts['full_requests'] += evidence['counts']['cache_hits'] + evidence['counts']['cache_misses']
        self.counts['full_hits'] += evidence['counts']['cache_hits']
        self.counts['full_misses'] += evidence['counts']['cache_misses']
        self.counts['full_fact_occurrences'] += len(evidence['facts'])
        self.events.append({'kind': 'full_discovery', 'evidence': evidence})
        return evidence

    def dependency(self, entry_id, record, dependency, guard, prepared, allow_fresh):
        """Return a re-certified named fact or a concrete conservative block.

        The historical atom namespace is valid even if that atom disappeared
        from both current endpoints (e.g. a transitive intermediate). The old
        equality is *not* placed in the current context without an exact hit or
        a new UNSAT query. Cached SAT is a valid reason to block a proof only.
        """
        old, receipt = dependency['rule'], dependency['receipt']
        commitment = _commitment(record['guard'], old, receipt, record['atoms'])
        left, right, typed_left, typed_right = commitment
        env = z3_env()
        query = z3.And(z3_term(_guard_node(guard), env), z3.Xor(
            z3_term(parse_term(typed_left), env), z3_term(parse_term(typed_right), env)))
        key = _cache_key(guard, 'primitive-xor', typed_left, typed_right)
        hit = key in self.cache
        active = context_id(guard)
        result = None if not hit and not allow_fresh else _receipt(self.cache, key, query, Counter())
        how = 'hit' if hit else 'missing' if result is None else 'miss'
        rhs = _plain(right)
        atoms = {left} | ({rhs[1]} if isinstance(rhs, tuple) else {rhs} if rhs not in ('true', 'false') else set())
        outside = sorted(atoms - prepared['atoms'].keys())
        event = {'kind': 'dependency', 'entry_id': entry_id, 'old_guard': record['guard'], 'new_guard': guard,
                 'old_rule': old['name'], 'typed_left': typed_left, 'typed_right': typed_right,
                 'outside_current_atoms': outside, 'cache': how, 'query': result,
                 'status': result['status'] if result is not None else 'missing', 'current_rule': None}
        self.counts['dependency_requests'] += 1
        self.counts['dependency_' + ('hits' if hit else 'missing' if result is None else 'misses')] += 1
        self.counts['dependency_status_' + event['status']] += 1
        self.counts['dependency_outside_vocabulary'] += bool(outside)
        if result is not None and result['status'] == 'unsat':
            row = {'name': 'ctx-' + _digest([active, left, right])[:24], 'left': left, 'right': right,
                   'event_context': active, 'proof_status': 'unsat'}
            new = {'guard': guard, 'typed_left': typed_left, 'typed_right': typed_right, 'query': result}
            merged = _merge_atoms(prepared['atoms'], record['atoms'])
            require(_commitment(guard, row, new, merged) == commitment, 'new typed fact binding changed')
            event['current_rule'] = row['name']
            self.events.append(event)
            return (commitment, row, new), None
        self.events.append(event)
        return None, {'entry_id': entry_id, 'old_guard': record['guard'], 'new_guard': guard,
                      'rule': old['name'], 'status': event['status'], 'typed_left': typed_left, 'typed_right': typed_right}


def _shortest(entries, left, right, guard, excluded, same_only):
    """Topological path only. Avoid probing deps for disconnected endpoints."""
    adj = defaultdict(list)
    for ident, rec in sorted(entries.items()):
        if ident in excluded or same_only and rec['guard'] != guard:
            continue
        if rec.get('kind') == 'exact' and rec['guard'] != guard:
            continue
        adj[rec['left']].append((rec['right'], ident))
        adj[rec['right']].append((rec['left'], ident))
    todo = deque([(left, [])]); seen = {left}
    while todo:
        source, path = todo.popleft()
        if source == right:
            return path
        for target, ident in adj[source]:
            if target not in seen:
                seen.add(target)
                todo.append((target, path+[(ident, source)]))
    return None


def _dependency_result(status, edges, blocked, attempts):
    return {'proved': status in ('identity', 'reused', 'revalidated'), 'status': status,
            'edges': edges, 'blocked': blocked, 'path_attempts': attempts}


def targeted_lookup(store, authority, left, right, guard, prepared, allow_fresh, *, kind='egg'):
    """Deterministically validate candidate historical paths, then reroute on failure.

    Guard feasibility must already have been established for this request. All
    returned rewrites replay against current certified fact names, and every
    path connects the requested exact typed source strings.
    """
    key = _cache_key(guard, 'feasibility')
    require(authority.cache.get(key, {}).get('status') == 'sat', 'reuse requires a certified feasible current guard')
    indexed = dict(zip(prepared['sources'], prepared['abstracts'], strict=True))
    require(prepared == prepare(prepared['sources']) and left in indexed and right in indexed,
            'wrong prepared endpoint binding')
    if indexed[left] == indexed[right]:
        return _dependency_result('identity', [], [], [])
    blocked, attempts, excluded, validated = [], [], set(), {}
    for same in (True, False):
        while (path := _shortest(store.entries, left, right, guard, excluded, same)) is not None:
            edges = []
            trial = {'same_guard_only': same, 'entries': [i for i,_ in path], 'blocked': None}
            for entry_id, source in path:
                if (entry_id, source) in validated:
                    edges.append(validated[entry_id, source]); continue
                rec = store.entries[entry_id]
                if kind == 'egg':
                    _record(entry_id, rec, SCOPE)
                else:
                    store.validate_record(entry_id, rec)
                deps, failure = {}, None
                for dep in rec.get('dependencies', []):
                    fact, failure = authority.dependency(entry_id, rec, dep, guard, prepared, allow_fresh)
                    if failure is not None:
                        break
                    commitment, row, receipt = fact
                    deps[commitment] = (row, receipt)
                if failure is not None:
                    excluded.add(entry_id); blocked.append(failure); trial['blocked'] = entry_id
                    break
                if kind == 'egg':
                    current = {'atoms': _merge_atoms(prepared['atoms'], rec['atoms']), 'bindings': deps}
                    edge, reason = _evaluate_edge(entry_id, rec, source, guard, current, SCOPE)
                    require(edge is not None and reason is None, 'authorized prerequisites did not replay the old Egg edge')
                else:
                    edge = store.replay(entry_id, rec, source, guard, deps)
                validated[entry_id, source] = edge
                edges.append(edge)
            attempts.append(trial)
            if trial['blocked'] is not None:
                continue
            cursor = left
            for edge in edges:
                require(edge['left'] == cursor and edge['new_guard'] == guard, 'broken replayed path')
                cursor = edge['right']
            require(cursor == right and edges, 'path does not reach current target')
            status = 'reused' if all(e['old_guard'] == guard for e in edges) else 'revalidated'
            return _dependency_result(status, edges, blocked, attempts)
    return _dependency_result('blocked' if blocked else 'miss', [], blocked, attempts)


def _solver():
    solver = z3.SolverFor('QF_BV')
    solver.set(timeout=TIMEOUT_MS)
    return solver


def _boolean_fact(row):
    return _proposition(parse(row['left'])) == _proposition(parse(row['right']))


def _boolean_goal(abstracts, direction='xor'):
    left, right = [_proposition(parse(t)) for t in abstracts]
    return (z3.Xor(left, right) if direction == 'xor' else
            z3.And(left, z3.Not(right)) if direction == 'old_only' else z3.And(right, z3.Not(left)))


def _core_check(abstracts, rows, direction='xor'):
    solver = _solver()
    solver.add(*[_boolean_fact(row) for row in rows], _boolean_goal(abstracts, direction))
    return str(solver.check())


class CoreSession:
    """Ordinary propositional implication with named-assumption unsat cores."""

    def __init__(self, prepared, evidence, counts):
        assumptions, vacuous = _checked_assumptions(prepared, evidence)
        require(not vacuous, 'infeasible guard cannot certify a core')
        self.prepared, self.counts = prepared, counts
        self.rows = {r['name']: r for r in evidence['facts']}
        self.labels = {name: z3.Bool('__assume_dependency_'+str(i)) for i,name in enumerate(self.rows)}
        self.solver = _solver()
        for label, formula in zip(self.labels.values(), assumptions, strict=True):
            self.solver.add(z3.Implies(label, formula))

    def compare(self, left, right, recorded=None):
        indexed = dict(zip(self.prepared['sources'], self.prepared['abstracts'], strict=True))
        endpoints = [indexed[left], indexed[right]]
        result = {}
        by_label = {label.decl().name(): name for name,label in self.labels.items()}
        for name in ('old_only','new_only'):
            self.solver.push()
            try:
                self.solver.add(_boolean_goal(endpoints, name))
                status = str(self.solver.check(*self.labels.values()))
                self.counts['boolean_direction_checks'] += 1
                core = sorted(by_label[label.decl().name()] for label in self.solver.unsat_core()) if status=='unsat' else []
            finally:
                self.solver.pop()
            if recorded is not None:
                # Independent audit: validate the saved sufficient core, not a
                # particular solver's (potentially different) core selection.
                old = recorded[name]
                require(old['status'] == status and isinstance(old['core'], list)
                        and old['core'] == sorted(set(old['core'])) and set(old['core']) <= self.rows.keys(),
                        'ordinary saved core status or membership mismatch')
                if status == 'unsat':
                    require(_core_check(endpoints, [self.rows[k] for k in old['core']], name) == 'unsat',
                            'ordinary saved directional core is insufficient')
                else:
                    require(not old['core'], 'non-UNSAT ordinary result has a core')
                core = old['core']
            result[name] = {'status': status, 'core': core}
        return result


class CoreStore:
    """Ordinary reusable solver cores, plus exact-guard prefix equivalences."""

    def __init__(self, counts):
        self.entries = {}
        self.counts = counts

    def add(self, case, prepared, evidence, core):
        names = sorted(set(core['old_only']['core']) | set(core['new_only']['core']))
        require(all(c['status']=='unsat' for c in core.values()), 'cannot store non-equality core')
        rows = {r['name']: r for r in evidence['facts']}
        indexed = dict(zip(prepared['sources'], prepared['abstracts'], strict=True))
        abstract = [indexed[case['left']], indexed[case['right']]]
        self.counts['boolean_core_creation_checks'] += 1
        require(_core_check(abstract,[rows[k] for k in names])=='unsat', 'ordinary union core is not sufficient')
        rec = {'kind':'core','scope':SCOPE,'schema_sha256':SCHEMA_SHA256,'guard':case['guard'],
               'left':case['left'],'right':case['right'],'abstracts':abstract,'atoms':prepared['atoms'],
               'dependencies':[{'rule':rows[k],'receipt':evidence['receipts'][k]} for k in names]}
        ident='ordinary-'+_digest(rec)
        self.validate_record(ident,rec)
        self.entries.setdefault(ident,deepcopy(rec))
        return ident

    def add_exact(self, case):
        rec={'kind':'exact','scope':SCOPE,'schema_sha256':SCHEMA_SHA256,'guard':case['guard'],
             'left':case['left'],'right':case['right'],'source_request':case['id']}
        ident='ordinary-'+_digest(rec)
        self.entries.setdefault(ident,deepcopy(rec));return ident

    @staticmethod
    def validate_record(ident, rec):
        require(ident=='ordinary-'+_digest(rec) and rec['scope']==SCOPE and rec['schema_sha256']==SCHEMA_SHA256,
                'ordinary proof content or typed schema changed')
        _guard_node(rec['guard'])
        prepared=prepare([rec['left'],rec['right']])
        if rec['kind']=='exact':
            require(set(rec)=={'kind','scope','schema_sha256','guard','left','right','source_request'},
                    'exact proof record malformed')
            return
        require(rec['kind']=='core' and set(rec)=={'kind','scope','schema_sha256','guard','left','right','abstracts','atoms','dependencies'}
                and rec['abstracts']==prepared['abstracts'] and all(rec['atoms'].get(k)==v for k,v in prepared['atoms'].items()),
                'ordinary core endpoints or atom binding changed')
        _validate_atoms(rec['atoms'])
        names=[]
        for dep in rec['dependencies']:
            _commitment(rec['guard'],dep['rule'],dep['receipt'],rec['atoms'])
            names.append(dep['rule']['name'])
        require(names==sorted(set(names)), 'duplicate or unordered core dependency')

    def replay(self, ident, rec, source, guard, deps):
        self.validate_record(ident,rec)
        if rec['kind']=='exact':
            require(rec['guard']==guard and not deps, 'cannot transfer typed prefix to another guard')
        else:
            require(len(deps)==len(rec['dependencies']), 'incomplete current core dependency bundle')
            self.counts['boolean_core_replay_checks'] += 1
            require(_core_check(rec['abstracts'],[row for row,_ in deps.values()])=='unsat', 'current ordinary core no longer entails equality')
        require(source in (rec['left'],rec['right']), 'disconnected ordinary edge')
        target=rec['right'] if source==rec['left'] else rec['left']
        return {'entry_id':ident, 'left':source, 'right':target, 'old_guard':rec['guard'], 'new_guard':guard,
                'kind':rec['kind'],'used_ground_rules':sorted(row['name'] for row,_ in deps.values())}


def includes(old, new):
    """Exact containment of feasible guards in the frozen unsigned threshold DSL."""
    def interval(g):
        node = _guard_node(g)
        if g=='true':
            return None
        op,var,k=node;limit=(1<<BV_WIDTHS[var])-1
        return var, (0 if op=='ult' else k if op=='eq' else k+1), (k-1 if op=='ult' else k if op=='eq' else limit)
    if old=='true' or old==new:
        return True
    a,b=interval(old),interval(new)
    if a[1]==0 and a[2]==(1<<BV_WIDTHS[a[0]])-1:
        return True
    return b is not None and a[0]==b[0] and a[1]<=b[1]<=b[2]<=a[2]


class ScopedMemory:
    """Stronger direct solver baseline: guard-contained prior exact equalities."""

    def __init__(self, subscope):
        self.subscope=subscope
        self.entries={}

    def add(self, case):
        self.entries[case['id']]={'left':format_term(parse_term(case['left'])),
                                 'right':format_term(parse_term(case['right'])),'guard':case['guard']}

    def lookup(self, case, *, audit=False):
        if parse_term(case['left'])==parse_term(case['right']):
            return []
        g=case['guard'];left,right=(format_term(parse_term(case[k])) for k in ('left','right'))
        candidates={i:r for i,r in self.entries.items() if r['guard']==g or self.subscope and includes(r['guard'],g)}
        path=_shortest(candidates,left,right,g,set(),True)
        if path is None:
            path=_shortest(candidates,left,right,g,set(),False)
        if path is None:
            return None
        if audit:
            env=z3_env()
            for ident,_ in path:
                old=candidates[ident]['guard']
                solver=_solver();solver.add(z3_term(_guard_node(g),env),z3.Not(z3_term(_guard_node(old),env)))
                require(solver.check()==z3.unsat,'guard inclusion failed independent typed verification')
        return [i for i,_ in path]
