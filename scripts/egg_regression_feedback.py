"""Scope-bound, independently checked comparison feedback for monitor maintenance.

All arms receive the same available full-width verdict and counterexamples.
Ordinary and egg additionally receive the same primitive facts; only egg
receives a checked equality path, reuse references, and blocked dependencies.
Neither saturation failure nor a blocked reuse path establishes non-equivalence.
"""
from collections import Counter
from pathlib import Path

from egg_regression_facts import OrdinarySession, certify, prepare, verify
from egg_regression_reuse import ProofStore, verify_reuse
from egg_regression_smt import fresh_compare, verify_result
from egg_txn_terms import parse_term, referenced_signals
from run_egg_regression import invoke, payload


MAX_EXPRESSION_BYTES = 16_384
MAX_PUBLIC_STEPS = 8
ARMS = ('raw', 'ordinary', 'egg')


def validate_output(output):
    """Limit the public adapter to one well-typed monitor, not arbitrary code."""
    if not isinstance(output, dict) or set(output) != {'monitor'} or not isinstance(output['monitor'], str):
        raise ValueError('expected exactly one monitor string')
    source = output['monitor']
    if len(source.encode('utf-8')) > MAX_EXPRESSION_BYTES:
        raise ValueError('monitor exceeds experiment byte budget')
    return source, parse_term(source)


def style(term, literal):
    """Syntactic maintenance objective: literal last index, not the dynamic equality.

    Scope-equivalence must still be independently established. A style pass alone
    cannot justify substitution. Accept either operand ordering for an equality.
    """
    def equal_to(node, a, b):
        return isinstance(node, tuple) and node[0] == 'eq' and node[1:] in ((a, b), (b, a))

    def visit(node):
        if isinstance(node, tuple):
            yield node
            for child in node[1:]:
                yield from visit(child)

    nodes = tuple(visit(term))
    contains_literal = any(equal_to(n, 'data_index', literal) for n in nodes)
    contains_dynamic = any(equal_to(n, 'data_index', 'data_n') for n in nodes)
    return {'qualified': contains_literal and not contains_dynamic,
            'required_literal_equality_present': contains_literal,
            'forbidden_dynamic_equality_present': contains_dynamic,
            'required_literal': literal}


def _facts_public(evidence):
    return [{'id': name, 'guard': receipt['guard'],
             'left': receipt['typed_left'], 'right': receipt['typed_right'],
             'receipt_sha256': receipt['query']['smt2_sha256']}
            for name, receipt in sorted(evidence['receipts'].items())]


def _step_excerpt(steps):
    return {'steps': steps[:MAX_PUBLIC_STEPS], 'step_count': len(steps),
            'complete': len(steps) <= MAX_PUBLIC_STEPS}


def _public_egg(lookup, proof, proof_id, prepared, guard):
    # The archived full certificate always remains authoritative. The public
    # prefix is explicitly labelled when truncated; it is not a full proof.
    details = {'guard': guard, 'lookup_status': lookup['status'],
               'blocked_dependencies': lookup['reasons'],
               'status': (lookup['status'] if lookup['proved'] else proof['status']),
               'proved': lookup['proved'] or proof['proved'],
               'proof_refs': ([e['entry_id'] for e in lookup['edges']] if lookup['proved']
                              else [proof_id] if proof_id is not None else []),
               'abstract_atoms': prepared['atoms']}
    if lookup['proved']:
        details['replayed_edges'] = [
            {**{k: e[k] for k in ('entry_id', 'direction', 'old_guard', 'new_guard', 'used_ground_rules')},
             **_step_excerpt(e['steps'])} for e in lookup['edges']]
    else:
        details['new_derivation'] = _step_excerpt(proof['steps'])
        details['used_ground_rules'] = proof['used_ground_rules']
    return details


class Feedback:
    """Per-arm proof/fact memory, retained across the predeclared guard changes."""
    def __init__(self, reference, arm, binary=None):
        self.reference = reference
        parse_term(reference)
        if arm not in ARMS:
            raise ValueError('unexpected feedback arm')
        self.arm = arm
        self.binary = Path(binary).resolve(strict=True) if arm == 'egg' else None
        self.fact_cache = {}
        self.audit_cache = {}
        self.store = ProofStore() if arm == 'egg' else None
        self.native_times = Counter()
        self.graph_calls = 0

    def assess(self, candidate, guard, literal):
        """Return archived evidence and a small prompt packet, never just a native merge."""
        try:
            source, term = validate_output({'monitor': candidate})
        except ValueError as exc:
            return {'public': {'guard': guard, 'reference_relation': 'invalid',
                               'qualified': False, 'parse_error': str(exc)},
                    'oracle': None, 'private': None}

        check = style(term, literal)
        oracle = fresh_compare(self.reference, source, guard)
        verify_result(self.reference, source, guard, oracle)
        if oracle['guard_status'] != 'sat':
            raise ValueError('unexpected infeasible controlled experiment guard')
        signals = referenced_signals(parse_term(self.reference)) | referenced_signals(term) | referenced_signals(parse_term(guard))
        directions = {}
        for name, record in oracle['directions'].items():
            witness = record.get('witness')
            directions[name] = {'status': record['status'],
                                'witness': {key: witness[key] for key in sorted(signals)} if witness is not None else None,
                                'receipt_sha256': record.get('smt2_sha256')}
        public = {'guard': guard, 'reference_relation': oracle['relation'], 'directions': directions,
                  'style': check, 'qualified': oracle['relation'] == 'equivalent' and check['qualified'],
                  'scope': 'current guard over all declared-width two-state snapshots; not RTL reachability'}
        private = None
        if self.arm != 'raw':
            prepared = prepare([self.reference, source])
            evidence = certify(prepared, guard, self.fact_cache)
            verify(prepared, guard, evidence, self.audit_cache)
            ordinary = OrdinarySession(prepared, evidence).compare(*prepared['abstracts'])
            public['ordinary'] = {'facts': _facts_public(evidence), 'directions': ordinary,
                                  'note': 'Abstract SAT is not a typed counterexample.'}
            private = {'prepared': prepared, 'evidence': evidence, 'ordinary': ordinary}
            for name in ('old_only', 'new_only'):
                if ordinary[name] == 'unsat' and oracle['directions'][name]['status'] != 'unsat':
                    raise ValueError('abstract implication disagrees with typed oracle')
            if self.arm == 'egg':
                lookup = self.store.lookup(self.reference, source, guard, evidence, prepared)
                verify_reuse(self.reference, source, guard, evidence, prepared, lookup, self.store.entries)
                proof = None
                proof_id = None
                graph = None
                request = None
                if not lookup['proved']:
                    ids = {self.reference: 'reference', source: 'candidate'}
                    request = payload(prepared, evidence, ids, [('reference', 'candidate')])
                    graph, results = invoke(request, self.binary, self.native_times, 'feedback')
                    self.graph_calls += 1
                    proof = results[('reference', 'candidate')]
                    proof_id = self.store.add(self.reference, source, guard, evidence, prepared, proof) if proof['proved'] else None
                if (lookup['proved'] or proof['proved']) and oracle['relation'] != 'equivalent':
                    raise ValueError('Egg certificate disagrees with typed oracle')
                public['egg'] = _public_egg(lookup, proof, proof_id, prepared, guard)
                public['egg']['note'] = 'A blocked dependency or unmerged target is not a typed counterexample. Only independently checked equality is asserted.'
                private['egg'] = {'lookup': lookup, 'proof': proof, 'proof_id': proof_id,
                                  'payload': request, 'graph': graph}
        return {'public': public, 'oracle': oracle, 'private': private}
