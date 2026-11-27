#!/usr/bin/env python3
"""Compare frozen PC fixture transcripts after exact common-input pairing (no model calls)."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from audit_egg_fifo_live import read_archive
from audit_egg_frame_pc import audit
from egg_frame_pc_loop import ARMS, compact, packet_metrics
from predicates import ROOT


def require(condition, text):
    if not condition:
        raise ValueError(text)


def read(files, name):
    return json.loads(files[name])


def compare(dnf_archive, cube_archive, corpus):
    archives = {'dnf': dnf_archive, 'cube': cube_archive}
    files = {name: read_archive(path) for name, path in archives.items()}
    audited = {name: audit(f, corpus, None) for name, f in files.items()}
    left, right = files['dnf'], files['cube']
    settings = {name: read(f, 'config.json') for name, f in files.items()}
    ignore = {'certificate_mode', 'diagnostic_binary_sha256'}
    require(settings['dnf']['certificate_mode'] == 'dnf' and settings['cube']['certificate_mode'] == 'cube' and
            settings['dnf']['mode'] == settings['cube']['mode'] == 'fixture' and
            {k:v for k,v in settings['dnf'].items() if k not in ignore} ==
            {k:v for k,v in settings['cube'].items() if k not in ignore}, 'non-matched mode or fixture config')
    shared_names = [n for n in left if n.rsplit('/',1)[-1] in
                    ('assessment.json','physical-score.json','oracles.json','common.json','diagnoses.json','response.json')]
    require(set(shared_names) == {n for n in right if n.rsplit('/',1)[-1] in
                    ('assessment.json','physical-score.json','oracles.json','common.json','diagnoses.json','response.json')},
            'shared stage inventory differs')
    require(all(left[n] == right[n] for n in shared_names), 'a common candidate, observation, oracle, diagnosis or score differs')
    common_requests = [n for n in left if n.endswith('/request.json') and any(f'/{arm}/' in n for arm in ('raw','ordinary'))]
    require(all(left[n] == right[n] for n in common_requests), 'raw or ordinary request changed between modes')
    config = settings['dnf']
    counts = {mode: Counter() for mode in files}
    totals = {mode: {arm: Counter() for arm in ARMS} for mode in files}
    per_profile = {mode: defaultdict(Counter) for mode in files}
    cases, identities = [], {}
    for profile in config['profiles']:
        for trial in range(1,config['replicates']+1):
            for turn in range(1,config['rounds_per_arm']+1):
                stage = 'seed' if turn == 1 else f'round-{turn-1:02d}'
                for arm in ARMS:
                    base = f'{profile}/trial-{trial:02d}/{arm}'
                    for mode, f in files.items():
                        feedback = f[f'{base}/{stage}/feedback.txt'].decode().rstrip('\n')
                        totals[mode][arm].update(packet_metrics(feedback))
                        req = read(f, f'{base}/round-{turn:02d}/request.json')
                        totals[mode][arm]['request_messages_json_utf8_bytes'] += len(compact(req['messages']).encode())
                    if arm != 'egg':
                        continue
                    common = read(left, f'{base}/{stage}/common.json')
                    diags = read(left, f'{base}/{stage}/diagnoses.json')
                    certs = {name:read(f, f'{base}/{stage}/certificates.json') for name,f in files.items()}
                    for name,d in diags.items():
                        obs = common['observations'][name]
                        identity = hashlib.sha256(compact([name,d['candidate'],d['sample'],d['public']['candidate_value']]).encode()).hexdigest()
                        record = {'profile':profile, 'trial':trial, 'delivered_in_round':turn,
                                  'property':name, 'identity':identity, 'origin':obs['origin'],
                                  'candidate_value':d['public']['candidate_value'], 'literal_count':d['public']['literal_count'],
                                  'methods':{}}
                        for mode,method in certs.items():
                            cert = method[name]
                            public,evidence = cert['public'], cert['evidence']
                            graph = (evidence or {}).get('engine') or {}
                            checked = (evidence or {}).get('checked_steps') or []
                            data = {'status':public['status'], 'reason':public.get('reason'),
                                    'stop':graph.get('stop_reason'), 'enodes':graph.get('enodes'),
                                    'proof_steps_in_archive':len(checked), 'public_steps':len(public.get('steps',[])),
                                    'public_utf8_bytes':len(compact(public).encode())}
                            record['methods'][mode] = data
                            counts[mode][public['status']] += 1
                            counts[mode]['with_checked_archive_rewrite'] += bool(checked)
                            if data['reason']:
                                counts[mode]['reason:'+data['reason']] += 1
                            if data['stop']:
                                counts[mode]['stop:'+data['stop']] += 1
                            per_profile[mode][profile][public['status']] += 1
                        signatures = {m:(x['status'],x['reason'],x['proof_steps_in_archive']) for m,x in record['methods'].items()}
                        require(identities.setdefault(identity,signatures)==signatures, 'repeated diagnostic proof changed')
                        cases.append(record)
    unique = {mode:dict(Counter(v[mode][0] for v in identities.values())) for mode in files}
    return {'complete':True, 'mode':'fixture_certificate_policy_comparison', 'new_api_calls':0,
            'archive_sha256':{name:hashlib.sha256(Path(path).read_bytes()).hexdigest() for name,path in archives.items()},
            'audited':{name:record['passed'] for name,record in audited.items()},
            'byte_identical_common_artifacts':len(shared_names), 'byte_identical_raw_ordinary_requests':len(common_requests),
            'delivered_opportunities':len(cases), 'unique_candidate_observation_opportunities':len(identities),
            'observation_sources':dict(Counter(r['origin'] for r in cases)),
            'candidate_values':dict(Counter(str(r['candidate_value']).lower() for r in cases)),
            'totals_by_method':counts, 'unique_by_method':unique, 'per_profile':per_profile,
            'feedback_and_request_bytes_by_arm':totals, 'cases':cases}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dnf', type=Path, required=True)
    p.add_argument('--cube', type=Path, required=True)
    p.add_argument('--corpus', type=Path, default=ROOT/'results/milestone3/frame-faults')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = compare(args.dnf,args.cube,args.corpus)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('Matched certificate opportunities:', result['delivered_opportunities'])
