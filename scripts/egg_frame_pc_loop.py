#!/usr/bin/env python3
"""Matched proof-carrying monitor refinement; only checked candidate-side evidence enters requests."""
import argparse
from functools import partial
import hashlib
import json
import os
from pathlib import Path

from egg_fifo_loop_provider import ProviderError, respond
from egg_frame_faults import load_corpus
from egg_frame_llm import SCHEMA, TASK as FRAME_TASK, validate
from egg_frame_observe import score_corpus
from egg_frame_pc_certificate import certify
from egg_frame_pc_diagnosis import diagnose
from egg_frame_pc_observation import prepare_common
from egg_frame_pc_seeds import SEEDS, fixture_revision
from egg_frame_proof import typed_oracle
from egg_frame_terms import REFERENCES
from predicates import ROOT

ARMS = ('raw', 'ordinary', 'egg')
SYSTEM = ('You verify the original RTL specification using passive assertion monitors. '
          'Revise the five violation formulas using the observed feedback; do not change the RTL or the specification. '
          'A diagnostic or checked proof explains the CURRENT candidate (or its negation) on a particular observation; '
          'it is not a proof that the candidate is equivalent to the specification.')
TASK = FRAME_TASK + ('\nThe selected mismatch may be a physical PRE observation or a symbolic two-state counterexample. '
                     'A sufficient-literal diagnosis, when present, states why the current candidate has its observed value. '
                     'An egg certificate, when present, shows a checked proof about the signed current candidate: '
                     'either an equivalent decomposition containing the observed sufficient clause, or a proof that the candidate '
                     'under that clause reduces to true. It does not justify the reference monitor. '
                     'Treat unavailable evidence as inconclusive. Use the specification and mismatch observations to fix the candidate.')


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')


def compact(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def grade(oracles, physical):
    counts = physical['totals_by_design']
    references = [name for name, row in counts.items() if name != 'original' and row['reference_alarms']]
    result = {
        'equivalent_properties': sum(row['equivalent'] is True for row in oracles.values()),
        'inequivalent_properties': sum(row['equivalent'] is False for row in oracles.values()),
        'unresolved_properties': sum(row['equivalent'] is None for row in oracles.values()),
        'reference_detectable_faults': references,
        'faults_with_matched_alarms': [name for name in references if counts[name]['matched_alarms']],
        'missed_reference_alarms': sum(row['missed'] for row in counts.values()),
        'extra_alarms': sum(row['false_alarm'] for row in counts.values()),
        'unknown_sample_comparisons': sum(row['unknown'] for row in counts.values()),
    }
    result['verified'] = (result['equivalent_properties'] == len(REFERENCES) and
                          result['missed_reference_alarms'] == result['extra_alarms'] ==
                          result['unknown_sample_comparisons'] == 0)
    return result


def packet_metrics(packet):
    """Size of a NEW feedback packet (not cumulative context, and not model token usage)."""
    result = {'feedback_utf8_bytes': len(packet.encode('utf-8')), 'diagnoses_sufficient': 0,
              'egg_checked_rewrites': 0, 'egg_checked_identities': 0, 'egg_unavailable': 0}
    if packet.startswith('Invalid candidate: '):
        return result
    data = json.loads(packet)
    result['diagnoses_sufficient'] = sum(x['status'] == 'sufficient' for x in data.get('candidate_diagnoses', {}).values())
    statuses = [x['status'] for x in data.get('egg_certificates', {}).values()]
    for field, value in [('egg_checked_rewrites', 'checked_rewrite'), ('egg_checked_identities', 'checked_identity'),
                         ('egg_unavailable', 'unavailable')]:
        result[field] = statuses.count(value)
    if sum(result[key] for key in ('egg_checked_rewrites', 'egg_checked_identities', 'egg_unavailable')) != len(statuses):
        raise ValueError('unknown certificate status')
    return result


def initial_messages(seed, packet):
    return [{'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': TASK + '\nInitial candidate (provided): ' +
             json.dumps(seed, sort_keys=True) + '\nInitial tool feedback: ' + packet}]


def append_revision(history, output, packet):
    history.extend([{'role': 'assistant', 'content': json.dumps(output, sort_keys=True)},
                    {'role': 'user', 'content': packet + '\nSubmit all five monitors again.'}])


class Evaluator:
    def __init__(self, corpus, binary, certificate_mode):
        if certificate_mode == "dnf":
            self.certify = certify
        elif certificate_mode == "cube":
            from egg_frame_pc_cube_certificate import certify_cube
            self.certify = certify_cube
        else:
            raise ValueError("unknown certificate mode")
        self.corpus = corpus
        self.binary = binary
        self.candidates, self.oracles, self.diagnoses, self.certificates = {}, {}, {}, {}

    def common(self, monitors):
        key = tuple(monitors[name] for name in REFERENCES)
        if key not in self.candidates:
            physical = score_corpus(self.corpus, monitors)
            oracles = {}
            for name, reference in REFERENCES.items():
                identity = (reference, monitors[name])
                if identity not in self.oracles:
                    self.oracles[identity] = typed_oracle(*identity)['oracle']
                oracles[name] = self.oracles[identity]
            common = prepare_common(monitors, self.corpus, oracles, physical)
            self.candidates[key] = (physical, oracles, common, grade(oracles, physical))
        return key, self.candidates[key]

    def stage(self, monitors, arm, path):
        key, (physical, oracles, common, assessment) = self.common(monitors)
        save(path / 'physical-score.json', physical)
        save(path / 'oracles.json', oracles)
        save(path / 'common.json', common)
        save(path / 'assessment.json', assessment)
        packet = dict(common['public'])
        if arm != 'raw':
            if key not in self.diagnoses:
                self.diagnoses[key] = {name: diagnose(monitors[name], obs['values'], obs['candidate_value'])
                                       for name, obs in common['observations'].items() if obs is not None}
            diagnoses = self.diagnoses[key]
            save(path / 'diagnoses.json', diagnoses)
            packet['candidate_diagnoses'] = {name: item['public'] for name, item in diagnoses.items()}
            if arm == 'egg':
                if key not in self.certificates:
                    self.certificates[key] = {name: self.certify(item, self.binary) for name, item in diagnoses.items()}
                certificates = self.certificates[key]
                save(path / 'certificates.json', certificates)
                packet['egg_certificates'] = {name: item['public'] for name, item in certificates.items()}
        text = compact(packet)
        (path / 'feedback.txt').write_text(text + '\n', encoding='utf-8')
        return assessment, text


def _validate_receipt(receipt, mode, config, ids, models):
    if not isinstance(receipt, dict) or not isinstance(receipt.get('id'), str) or not receipt['id'] or receipt['id'] in ids:
        raise ValueError('missing or repeated response identifier')
    ids.add(receipt['id'])
    if 'output' not in receipt:
        raise ValueError('missing structured output')
    if mode == 'fixture':
        if receipt.get('usage') is not None or receipt.get('dispatch_attempted') is not False or not receipt['id'].startswith('fixture-pc-'):
            raise ValueError('fixture must not claim real provider usage or dispatch')
        return
    if (receipt.get('dispatch_attempted') is not True or receipt.get('http_status') != 200 or
            receipt.get('status') != 'completed' or receipt.get('requested_model') != config['model'] or
            not isinstance(receipt.get('model'), str) or not receipt['model'] or not receipt['id'].startswith('resp_')):
        raise ValueError('invalid live provider receipt')
    usage = receipt.get('usage')
    if (not isinstance(usage, dict) or any(type(usage.get(key)) is not int or usage[key] < 0
        for key in ('input_tokens', 'output_tokens', 'total_tokens')) or
        usage['input_tokens'] + usage['output_tokens'] != usage['total_tokens'] or
            usage['output_tokens'] > config['max_output_tokens']):
        raise ValueError('invalid live usage')
    models.add(receipt['model'])
    if len(models) != 1:
        raise ValueError('provider model changed during paired experiment')


def run(*, corpus_dir, binary, out, mode, profiles, replicates, rounds, provider=None, provider_config=None, certificate_mode="dnf"):
    profiles = tuple(profiles)
    if (mode not in ('fixture', 'live') or certificate_mode not in ('dnf', 'cube') or not profiles or len(set(profiles)) != len(profiles) or
            not set(profiles) <= set(SEEDS) or type(rounds) is not int or not 1 <= rounds <= 3 or
            type(replicates) is not int or not 1 <= replicates <= 5):
        raise ValueError('invalid mode/profiles/rounds/trials')
    if mode == 'fixture' and (provider is not None or provider_config is not None):
        raise ValueError('fixture mode never accepts a provider or usage configuration')
    if mode == 'live' and (not callable(provider) or not isinstance(provider_config, dict) or
            not isinstance(provider_config.get('model'), str) or not provider_config['model'] or
            provider_config.get('transport') != 'OpenAI Responses API' or
            type(provider_config.get('max_output_tokens')) is not int or
            not 16 <= provider_config['max_output_tokens'] <= 4096):
        raise ValueError('live mode requires a provider and a valid budget configuration')
    binary = Path(binary).resolve(strict=True)
    corpus_dir, out = Path(corpus_dir), Path(out)
    corpus = load_corpus(corpus_dir)
    source = json.loads((corpus_dir / 'summary.json').read_bytes())
    out.mkdir(parents=True, exist_ok=False)
    config = {'schema': 1, 'mode': mode, 'arms': list(ARMS), 'profiles': list(profiles),
              'replicates': replicates, 'rounds_per_arm': rounds, 'provider': provider_config,
              'certificate_mode': certificate_mode,
              'corpus_sha256': source['corpus_sha256'], 'seeds': {name: SEEDS[name] for name in profiles},
              'visible_designs': ['original', 'F02', 'F05'],
              'diagnostic_binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest()}
    save(out / 'config.json', config)
    evaluator = Evaluator(corpus, binary, certificate_mode)
    if mode == 'fixture':
        # All future replies are frozen in this mode. Compute common sample selection
        # BEFORE either certificate algorithm runs, so incidental symbolic model choice
        # cannot be affected by the different sequence of certificate-side Z3 queries.
        # This does not expose future candidates to any provider or prompt.
        for profile in profiles:
            for turn in range(rounds + 1):
                evaluator.common(fixture_revision(profile, turn))
    ids, models, sessions = set(), set(), {}
    usage = {arm: {key: 0 for key in ('input_tokens', 'output_tokens', 'total_tokens')} for arm in ARMS} if mode == 'live' else None
    sequence = 0
    for profile_index, profile in enumerate(profiles):
        sessions[profile] = {}
        seed = validate({'monitors': SEEDS[profile]})
        for trial in range(1, replicates + 1):
            label = f'trial-{trial:02d}'
            folder = out / profile / label
            history, previous, session = {}, {}, {}
            for arm in ARMS:
                path = folder / arm / 'seed'
                path.mkdir(parents=True)
                assessment, packet = evaluator.stage(seed, arm, path)
                if assessment['inequivalent_properties'] != len(REFERENCES):
                    raise ValueError(f'{profile}: frozen seed not entirely wrong')
                history[arm] = initial_messages(seed, packet)
                previous[arm] = packet
                session[arm] = {'seed': assessment, 'rounds': [], 'first_verified_round': None, 'delivered': []}
            for turn in range(1, rounds + 1):
                offset = (profile_index + trial - 1 + turn - 1) % len(ARMS)
                for arm in ARMS[offset:] + ARMS[:offset]:
                    path = folder / arm / f'round-{turn:02d}'
                    path.mkdir()
                    messages = history[arm]
                    save(path / 'request.json', {'messages': messages, 'response_schema': SCHEMA})
                    session[arm]['delivered'].append(packet_metrics(previous[arm]))
                    sequence += 1
                    try:
                        if mode == 'fixture':
                            response = {'id': f'fixture-pc-{sequence:03d}', 'output': {'monitors': fixture_revision(profile, turn)},
                                        'usage': None, 'dispatch_attempted': False}
                        else:
                            response = provider([dict(message) for message in messages], SCHEMA)
                    except ProviderError as exc:
                        save(path / 'provider-error.json', {'error': str(exc), 'receipt': exc.receipt})
                        save(out / 'incomplete.json', {'completed_responses': len(ids), 'attempted_steps': sequence,
                                                       'profile': profile, 'trial': label, 'arm': arm, 'round': turn,
                                                       'completed_usage': usage})
                        raise
                    save(path / 'response.json', response)
                    _validate_receipt(response, mode, provider_config, ids, models)
                    if usage is not None:
                        for field in usage[arm]:
                            usage[arm][field] += response['usage'][field]
                    output = response['output']
                    try:
                        monitors = validate(output)
                    except ValueError as exc:
                        assessment = {'candidate_error': str(exc), 'verified': False}
                        packet = 'Invalid candidate: ' + str(exc)
                        save(path / 'assessment.json', assessment)
                        (path / 'feedback.txt').write_text(packet + '\n', encoding='utf-8')
                    else:
                        assessment, packet = evaluator.stage(monitors, arm, path)
                    append_revision(messages, output, packet)
                    previous[arm] = packet
                    session[arm]['rounds'].append(assessment)
                    if assessment['verified'] and session[arm]['first_verified_round'] is None:
                        session[arm]['first_verified_round'] = turn
            sessions[profile][label] = session
    if len(ids) != len(profiles) * replicates * len(ARMS) * rounds:
        raise ValueError('incomplete experiment')
    summary = {'schema': 1, 'mode': mode, 'profiles': list(profiles), 'replicates': replicates,
               'rounds_per_arm': rounds, 'certificate_mode': certificate_mode, 'responses': len(ids), 'provider_api_calls': len(ids) if mode == 'live' else 0,
               'sessions': sessions, 'provider_usage': usage}
    if mode == 'live':
        summary['requested_model'] = provider_config['model']
        summary['model'] = next(iter(models))
    save(out / 'summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', type=Path, default=ROOT / 'results/milestone3/frame-faults')
    parser.add_argument('--certificate-mode', choices=('dnf', 'cube'), default='dnf')
    parser.add_argument('--binary', type=Path, required=True, help='release egg_diagnostic_forms (dnf) or egg_cube_proofs (cube)')
    parser.add_argument('--output', type=Path, required=True, help='new run directory')
    parser.add_argument('--profiles', nargs='+', choices=tuple(SEEDS), default=list(SEEDS))
    parser.add_argument('--replicates', type=int, choices=range(1, 6), default=1)
    parser.add_argument('--rounds', type=int, choices=(1, 2, 3), default=2)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--fixture', action='store_true')
    mode.add_argument('--live', action='store_true')
    parser.add_argument('--model')
    parser.add_argument('--reasoning-effort', choices=('minimal', 'low', 'medium', 'high'))
    parser.add_argument('--max-output-tokens', type=int, default=3072)
    args = parser.parse_args()
    if args.live and (not args.model or not os.environ.get('OPENAI_API_KEY', '').strip()):
        parser.error('--live requires explicit --model and a configured OPENAI_API_KEY')
    if not 16 <= args.max_output_tokens <= 4096:
        parser.error('--max-output-tokens must be in 16..4096')
    config = None if not args.live else {'model': args.model, 'reasoning_effort': args.reasoning_effort,
                                         'max_output_tokens': args.max_output_tokens, 'transport': 'OpenAI Responses API'}
    provider = None if not args.live else partial(respond, model=args.model, max_output_tokens=args.max_output_tokens,
                                                         reasoning_effort=args.reasoning_effort)
    budget = len(args.profiles) * args.replicates * args.rounds * len(ARMS)
    print(f"{budget} {'live provider' if args.live else 'fixture'} responses planned", flush=True)
    result = run(corpus_dir=args.corpus, binary=args.binary, out=args.output, mode='live' if args.live else 'fixture',
                 profiles=args.profiles, replicates=args.replicates, rounds=args.rounds, provider=provider,
                 provider_config=config, certificate_mode=args.certificate_mode)
    print(f"{result['responses']} {result['mode']} responses, {result['provider_api_calls']} provider calls")


if __name__ == '__main__':
    main()
