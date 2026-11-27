#!/usr/bin/env python3
"""Independently audit a completed scoped monitor-maintenance transcript.

No model calls and no native Egg search: re-solve the typed obligations, replay
the archived derivations in chronological order, check the exact serialized
prompt, and reconstruct the stage/usage summaries. Provider receipts establish
what the local archive reports, not independent server-side billing evidence.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re

from audit_egg_regression import fields, native_payload, read, require
from egg_frame_pc_loop import _validate_receipt, compact
from egg_regression_check import check_graph
from egg_regression_facts import OrdinarySession, prepare, verify
from egg_regression_feedback import ARMS, _facts_public, _public_egg, style, validate_output
from egg_regression_live import SCHEMA, STAGES, TASK, _fixture_candidate, messages
from egg_regression_reuse import ProofStore, verify_reuse
from egg_regression_smt import fresh_compare, verify_result
from egg_regression_workload import ARCHIVE, ARCHIVE_INVENTORY_SHA256, load_versions
from egg_txn_terms import REFERENCES, parse_term, referenced_signals


USAGE_FIELDS = ('input_tokens', 'output_tokens', 'total_tokens')
DETAIL_FIELDS = ('cached_input_tokens', 'cache_write_tokens', 'reasoning_tokens')


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def nbytes(value):
    return len(compact(value).encode('utf-8'))


def usage_details(usage):
    """Keep optional provider detail counters separate from additive totals."""
    inputs = usage.get('input_tokens_details') or {}
    outputs = usage.get('output_tokens_details') or {}
    require(isinstance(inputs, dict) and isinstance(outputs, dict), 'malformed usage detail')
    detail = {'cached_input_tokens': inputs.get('cached_tokens'),
              'cache_write_tokens': inputs.get('cache_write_tokens'),
              'reasoning_tokens': outputs.get('reasoning_tokens')}
    for k, value in detail.items():
        limit = usage['output_tokens'] if k == 'reasoning_tokens' else usage['input_tokens']
        require(value is None or type(value) is int and 0 <= value <= limit, 'invalid optional usage detail')
    return detail


class AssessmentAudit:
    """One independent typed-fact cache and chronological proof store per arm."""

    def __init__(self, reference, arm):
        self.reference, self.arm = reference, arm
        self.facts = {}
        self.store = ProofStore() if arm == 'egg' else None
        self.counts = Counter()
        self.stop_counts = Counter()
        self.fact_counts = Counter()
        self.blocked = []

    def assessment(self, value, guard, literal, recorded, location):
        fields(recorded, ('public', 'oracle', 'private'), 'malformed assessment')
        try:
            candidate, term = validate_output(value)
        except ValueError as exc:
            require(recorded == {'public': {'guard': guard, 'reference_relation': 'invalid',
                                             'qualified': False, 'parse_error': str(exc)},
                                 'oracle': None, 'private': None}, 'invalid candidate assessment mismatch')
            self.counts['invalid_candidates'] += 1
            return None, recorded['public']

        result = recorded['oracle']
        require(verify_result(self.reference, candidate, guard, result) and result['guard_status'] == 'sat',
                'wrong or infeasible typed assessment')
        self.counts['typed_assessments'] += 1
        self.counts['typed_queries'] += 3  # one feasibility + two directions in verify_result
        self.counts['relation_' + result['relation']] += 1
        signals = (referenced_signals(parse_term(self.reference)) | referenced_signals(term)
                   | referenced_signals(parse_term(guard)))
        directions = {}
        for name, receipt in result['directions'].items():
            witness = receipt['witness']
            directions[name] = {'status': receipt['status'],
                                'witness': {k: witness[k] for k in sorted(signals)} if witness is not None else None,
                                'receipt_sha256': receipt['smt2_sha256']}
        objective = style(term, literal)
        public = {'guard': guard, 'reference_relation': result['relation'], 'directions': directions,
                  'style': objective, 'qualified': result['relation'] == 'equivalent' and objective['qualified'],
                  'scope': 'current guard over all declared-width two-state snapshots; not RTL reachability'}
        private = recorded['private']
        if self.arm == 'raw':
            require(private is None, 'raw arm has undeclared private proof evidence')
        else:
            keys = ('prepared', 'evidence', 'ordinary') + (('egg',) if self.arm == 'egg' else ())
            fields(private, keys, 'unexpected private assessment schema')
            prepared = prepare([self.reference, candidate])
            require(prepared == private['prepared'], 'typed endpoint preparation mismatch')
            evidence = private['evidence']
            require(verify(prepared, guard, evidence, self.facts), 'scoped fact receipt mismatch')
            self.fact_counts.update(evidence['counts'])
            self.fact_counts['fact_occurrences'] += len(evidence['facts'])
            ordinary = OrdinarySession(prepared, evidence).compare(*prepared['abstracts'])
            require(ordinary == private['ordinary'], 'ordinary abstract assessment mismatch')
            require(all(ordinary[k] != 'unsat' or directions[k]['status'] == 'unsat'
                        for k in ('old_only', 'new_only')), 'abstract implication disagrees with typed result')
            public['ordinary'] = {'facts': _facts_public(evidence), 'directions': ordinary,
                                  'note': 'Abstract SAT is not a typed counterexample.'}
            if self.arm == 'egg':
                stored = private['egg']
                fields(stored, ('lookup', 'proof', 'proof_id', 'payload', 'graph'), 'unexpected Egg evidence schema')
                lookup = self.store.lookup(self.reference, candidate, guard, evidence, prepared)
                require(lookup == stored['lookup'] and
                        verify_reuse(self.reference, candidate, guard, evidence, prepared, lookup, self.store.entries),
                        'lookup is not justified by the chronological prefix of checked proofs')
                self.counts['lookup_' + lookup['status']] += 1
                proof = proof_id = None
                if lookup['proved']:
                    require(all(stored[k] is None for k in ('proof', 'proof_id', 'payload', 'graph')),
                            'reused/identical assessment claims unneeded native graph')
                    self.counts['replayed_steps'] += sum(len(e['steps']) for e in lookup['edges'])
                else:
                    # A blocked path is not by itself a proof of a semantic change.
                    # Recheck each *named missing* prerequisite as a separate post-hoc obligation.
                    for reason in lookup['reasons']:
                        entry = self.store.entries[reason['entry_id']]
                        deps = {d['rule']['name']: d['receipt'] for d in entry['dependencies']}
                        for name in reason['missing_current_dependencies']:
                            dep = deps[name]
                            check = fresh_compare(dep['typed_left'], dep['typed_right'], guard)
                            self.blocked.append({'location': location, 'entry_id': reason['entry_id'],
                                                 'rule': name, 'previous_guard': entry['guard'],
                                                 'current_guard': guard, 'typed_left': dep['typed_left'],
                                                 'typed_right': dep['typed_right'], 'recheck': check})
                    payload = native_payload(prepared, evidence,
                                             {self.reference: 'reference', candidate: 'candidate'},
                                             [('reference', 'candidate')])
                    require(payload == stored['payload'], 'native graph endpoints or facts changed')
                    proof = check_graph(payload, stored['graph'])[('reference', 'candidate')]
                    require(proof == stored['proof'], 'archived proof replay mismatch')
                    self.counts['graph_calls'] += 1
                    self.stop_counts[str(proof['stop'])] += 1
                    if proof['proved']:
                        proof_id = self.store.add(self.reference, candidate, guard, evidence, prepared, proof)
                        self.counts['native_derivations'] += 1
                        self.counts['native_steps'] += len(proof['steps'])
                    require(proof_id == stored['proof_id'], 'proof ID not derived from checked content')
                require(not (lookup['proved'] or (proof is not None and proof['proved']))
                        or result['relation'] == 'equivalent', 'Egg proof disagrees with independent SMT')
                public['egg'] = _public_egg(lookup, proof, proof_id, prepared, guard)
                public['egg']['note'] = ('A blocked dependency or unmerged target is not a typed counterexample. '
                                         'Only independently checked equality is asserted.')
        require(public == recorded['public'], 'public feedback does not match checked private evidence')
        return candidate, public


def audit(run_dir, archive=ARCHIVE):
    run_dir = Path(run_dir)
    archive = Path(archive)
    inventory = {}

    def get(name):
        path = run_dir / name
        require(path.is_file() and not path.is_symlink() and name not in inventory, f'missing/repeated file {name}')
        inventory[name] = digest(path)
        return read(path)

    config = get('config.json')
    fields(config, ('schema', 'task', 'mode', 'arms', 'stages', 'max_attempts_per_stage', 'maximum_responses',
                    'provider', 'archive_members_sha256', 'seed_source', 'seed_response_id',
                    'seed_response_sha256', 'binary_sha256', 'grading'), 'configuration schema mismatch')
    mode, limit = config['mode'], config['max_attempts_per_stage']
    seed = load_versions(archive)['trial-01/initial']
    reference = seed['monitors']['data_last']
    require(config['schema'] == 1 and config['task'] == TASK and mode in ('fixture', 'live')
            and config['arms'] == list(ARMS) and config['stages'] == list(STAGES)
            and type(limit) is int and 1 <= limit <= 3
            and config['maximum_responses'] == len(ARMS) * len(STAGES) * limit
            and config['archive_members_sha256'] == ARCHIVE_INVENTORY_SHA256
            and config['seed_source'] == seed['source'] and config['seed_response_id'] == seed['response_id']
            and config['seed_response_sha256'] == seed['response_sha256']
            and isinstance(config['binary_sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', config['binary_sha256'])
            and config['grading'] == 'full typed equivalence in the current guard + requested literal syntax; no model judgement',
            'configuration differs from locked pilot')
    provider = config['provider']
    if mode == 'live':
        fields(provider, ('model', 'reasoning_effort', 'max_output_tokens', 'transport'), 'live provider schema mismatch')
        require(isinstance(provider['model'], str) and provider['model']
                and provider['reasoning_effort'] in (None, 'minimal', 'low', 'medium', 'high')
                and type(provider['max_output_tokens']) is int and 16 <= provider['max_output_tokens'] <= 4096
                and provider['transport'] == 'OpenAI Responses API', 'invalid live provider configuration')
    else:
        require(provider is None, 'fixture is not a live provider run')
    recorded_seed = get('seed.json')
    fields(recorded_seed, ('monitor', 'independent_full_domain_oracle'), 'seed schema mismatch')
    require(recorded_seed['monitor'] == reference and
            verify_result(REFERENCES['data_last'], reference, 'true', recorded_seed['independent_full_domain_oracle'])
            and recorded_seed['independent_full_domain_oracle']['relation'] == 'equivalent', 'unverified initial reference')

    ids, models, tiers = set(), set(), Counter()
    states = {arm: {'checker': AssessmentAudit(reference, arm), 'carry': reference, 'prior': None,
                    'stages': [], 'usage': dict.fromkeys(USAGE_FIELDS, 0), 'calls': [], 'preflights': []} for arm in ARMS}
    order_log = []
    for i, literal in enumerate(STAGES, 1):
        guard = f'(eq data_n {literal})'
        order = ARMS[(i-1) % len(ARMS):] + ARMS[:(i-1) % len(ARMS)]
        for arm in order:
            state = states[arm]
            prefix = f'{arm}/stage-{i:02}'
            initial, prior = state['carry'], state['prior']
            checker = state['checker']
            current, public = checker.assessment({'monitor': initial}, guard, literal,
                                                   get(prefix + '/preflight.json'), prefix + '/preflight')
            preflight = public
            state['preflights'].append({'stage': i, 'candidate': current, 'relation': public['reference_relation'],
                                        'directions': public['directions'], 'egg': public.get('egg')})
            records = []
            for attempt in range(1, limit+1):
                path = f'{prefix}/attempt-{attempt:02}'
                request = get(path + '/request.json')
                expected = messages(reference, current, guard, literal, public, prior)
                require(request == {'messages': expected, 'response_schema': SCHEMA},
                        'serialized request differs from checked current/historical assessment')
                response = get(path + '/response.json')
                if mode == 'live':
                    _validate_receipt(response, mode, provider, ids, models)
                    require(isinstance(response.get('service_tier'), str), 'missing service tier')
                    tiers[response['service_tier']] += 1
                    details = usage_details(response['usage'])
                    for key in USAGE_FIELDS:
                        state['usage'][key] += response['usage'][key]
                else:
                    expected_id = f'fixture-regression-{len(ids)+1:03}'
                    require(response == {'id': expected_id, 'output': _fixture_candidate(reference, i, attempt),
                                         'usage': None, 'dispatch_attempted': False}, 'fixture reply differs from authored control')
                    ids.add(expected_id)
                    details = None
                order_log.append({'arm': arm, 'stage': i, 'attempt': attempt, 'response_id': response['id']})
                value, after = checker.assessment(response['output'], guard, literal,
                                                   get(path + '/assessment.json'), path + '/assessment')
                records.append({'attempt': attempt, 'response_id': response['id'], 'relation': after['reference_relation'],
                                'qualified': after['qualified'], 'request_utf8_bytes': nbytes(expected),
                                'egg_lookup_status': after.get('egg', {}).get('lookup_status')})
                prior_egg = prior['last_assessment'].get('egg') if prior else None
                current_egg = public.get('egg')
                state['calls'].append({'stage': i, **records[-1], 'candidate': value,
                                       'usage': {k: response['usage'][k] for k in USAGE_FIELDS} if mode == 'live' else None,
                                       'usage_details': details,
                                       'current_feedback_bytes': nbytes(public),
                                       'previous_stage_bytes': nbytes(prior),
                                       'current_egg_bytes': nbytes(current_egg) if current_egg is not None else 0,
                                       'previous_egg_bytes': nbytes(prior_egg) if prior_egg is not None else 0,
                                       'current_proof_refs_sent': current_egg['proof_refs'] if current_egg else [],
                                       'historical_proof_refs_sent': prior_egg['proof_refs'] if prior_egg else [],
                                       'blocked_dependencies_sent': current_egg['blocked_dependencies'] if current_egg else [],
                                       'after_egg': after.get('egg')})
                if value is not None:
                    current = value
                public = after
                if public['qualified']:
                    state['carry'] = current
                    break
            state['prior'] = {'stage': i, 'guard': guard, 'qualified_response': public['qualified'], 'last_assessment': public}
            stage = {'stage': i, 'guard': guard, 'initial_candidate': initial, 'carried_candidate_next': state['carry'],
                     'qualified': public['qualified'], 'preflight_relation': preflight['reference_relation'],
                     'preflight_egg_lookup_status': preflight.get('egg', {}).get('lookup_status'), 'attempts': records}
            require(stage == get(prefix + '/stage-summary.json'), 'stage summary does not match audited attempts')
            state['stages'].append(stage)

    arms = {}
    detail_totals = {}
    for arm, state in states.items():
        checker = state['checker']
        if arm == 'egg':
            require(checker.store.entries == get('egg/proof_store.json'), 'archived proof store differs from checked chronological prefix')
        arms[arm] = {'stages': state['stages'], 'qualified_stages': sum(s['qualified'] for s in state['stages']),
                     'responses': len(state['calls']), 'usage': state['usage'] if mode == 'live' else None,
                     'new_graph_calls': checker.counts['graph_calls'],
                     'stored_proofs': len(checker.store.entries) if arm == 'egg' else 0}
        if mode == 'live':
            detail_totals[arm] = {k: (sum(c['usage_details'][k] for c in state['calls'])
                                      if all(c['usage_details'][k] is not None for c in state['calls']) else None)
                                  for k in DETAIL_FIELDS}
    total_usage = {k: sum(s['usage'][k] for s in states.values()) for k in USAGE_FIELDS}
    summary = {'schema': 1, 'mode': mode, 'task': TASK, 'complete': True, 'responses': len(ids),
               'provider_api_calls': len(ids) if mode == 'live' else 0,
               'provider_usage': total_usage if mode == 'live' else None,
               'maximum_responses': config['maximum_responses'], 'arms': arms,
               'limitations': ['single archived monitor, controlled scoped-refactor pilot',
                               'fixture outputs are deliberately authored, not model performance',
                               'no global equivalence, RTL reachability, or end-to-end verification claim']}
    if mode == 'live':
        summary.update(requested_model=provider['model'], model=next(iter(models)))
    require(summary == get('summary.json') and len(ids) <= config['maximum_responses'],
            'global summary or provider budget differs from audited transcript')
    actual_files = {str(p.relative_to(run_dir)) for p in run_dir.rglob('*') if p.is_file()}
    require(actual_files == set(inventory), 'unaccounted transcript members (including unexpected calls)')
    stage_comparison = []
    for i, literal in enumerate(STAGES, 1):
        qualified = {a: [c['candidate'] for c in states[a]['calls'] if c['stage'] == i and c['qualified']] for a in ARMS}
        pre = {a: states[a]['preflights'][i-1] for a in ARMS}
        stage_comparison.append({'stage': i, 'guard': f'(eq data_n {literal})', 'qualified_monitors': qualified,
                                 'same_qualified_text': all(len(v) == 1 for v in qualified.values())
                                 and len({v[0] for v in qualified.values()}) == 1,
                                 'same_carried_text': len({p['candidate'] for p in pre.values()}) == 1,
                                 'same_preflight_witnesses': all(pre[a]['directions'] == pre[ARMS[0]]['directions'] for a in ARMS)})
    return {'complete': True, 'mode': mode, 'task': TASK, 'new_api_calls': 0, 'configuration': config,
            'original_archive_sha256': digest(archive), 'audited_summary': summary,
            'receipt_order': order_log, 'service_tiers': dict(tiers), 'usage_details': detail_totals,
            'stage_comparison': stage_comparison,
            'unique_qualified_monitor_strings': len({c['candidate'] for s in states.values() for c in s['calls'] if c['qualified']}),
            'checked_history': {arm: {'counts': dict(s['checker'].counts), 'fact_counts': dict(s['checker'].fact_counts),
                                      'graph_stop_counts': dict(s['checker'].stop_counts), 'preflights': s['preflights'],
                                      'calls': s['calls']} for arm, s in states.items()},
            'blocked_dependency_rechecks': states['egg']['checker'].blocked,
            'member_sha256': dict(sorted(inventory.items()))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--archive', type=Path, default=ARCHIVE)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.run_dir, args.archive)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        stream.write('\n')
    print(f"Audited {result['audited_summary']['responses']} {result['mode']} responses, "
          f"{len(result['member_sha256'])} transcript files; no API calls.")
