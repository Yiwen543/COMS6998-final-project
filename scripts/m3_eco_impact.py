#!/usr/bin/env python3
"""Audit guard proof reuse for the closed, source-checked arbiter ECO family."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

from m3_eco_formal import certify_eco, detector_table
from m3_eco_replay import variants
from m3_guard_inputs import profiles
from m3_proof_dependencies import validate_proof_dependencies
from predicates import ROOT, parse


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def direct_receipts(payload):
    """Record names applied by a single top-down ground rewrite to the two input trees."""
    rules = {parse(r['left']): (r['name'], parse(r['right'])) for r in payload['verified_rules']}

    def rewrite(node, used):
        if node in rules:
            name, replacement = rules[node]
            used.add(name)
            return replacement
        if isinstance(node, str):
            return node
        return (node[0], *(rewrite(ch, used) for ch in node[1:]))

    pairs = defaultdict(list)
    for target in payload['targets']:
        pairs[target['source_target']].append(parse(target['compact']))
    receipts = {}
    for name, (lhs, rhs) in pairs.items():
        used = set()
        if rewrite(lhs, used) != rewrite(rhs, used):
            raise ValueError(f'ordinary method could not justify {name}')
        receipts[name] = sorted(used)
    return receipts


def compare_replay(cases, formal, evidence):
    """Bind the independent exhaustive decisions to the identical RTL bytes."""
    records = evidence.get("cases")
    if not isinstance(records, dict) or set(records) != set(cases) or set(formal) != set(cases):
        raise ValueError("independent replay case inventory differs")
    counts = Counter()
    statuses = Counter()
    for case, source in cases.items():
        row = records[case]
        if not isinstance(row, dict) or row.get("source_sha256") != sha(source.encode()):
            raise ValueError(f"independent replay RTL hash differs: {case}")
        for family in ("rules", "claims"):
            independent = row.get(family)
            reference = formal[case][family]
            if not isinstance(independent, dict) or set(independent) != set(reference):
                raise ValueError(f"independent replay inventory differs: {case}/{family}")
            for name, truth in reference.items():
                match = independent[name]
                if (not isinstance(match, dict) or match.get("status") not in ("sat", "unsat") or
                        match["status"] != truth["status"]):
                    raise ValueError(f"independent replay status differs: {case}/{family}/{name}")
                counts[family] += 1
                statuses[truth["status"]] += 1
    return {"source_hashes_checked": len(records), "statuses_checked": sum(counts.values()),
            "families": dict(counts), "outcomes": dict(statuses)}


def check_case(source, table, reference_table, deps, ordinary, full):
    same = table == reference_table
    rules = certify_eco(table, claim_names=[])['rules'] if not same else {}
    failed = sorted(k for k, v in rules.items() if v['status'] == 'sat')
    if any(v['status'] not in ('sat', 'unsat') for v in rules.values()):
        raise ValueError('inconclusive premise')
    recheck = sorted(k for k, labels in deps.items() if set(labels).intersection(failed))
    ordinary_recheck = sorted(k for k, labels in ordinary.items() if set(labels).intersection(failed))
    post = certify_eco(table, rule_names=[], claim_names=recheck)['claims']
    ordinary_post = certify_eco(table, rule_names=[], claim_names=ordinary_recheck)['claims']
    direct = full['claims']
    if (set(direct) != set(deps) or set(post) != set(recheck) or
            set(ordinary_post) != set(ordinary_recheck)):
        raise ValueError('unmatched claim inventory')
    if not same and ({name: r['status'] for name, r in rules.items()} !=
                     {name: r['status'] for name, r in full['rules'].items()}):
        raise ValueError('premise rechecks disagree with full reference')
    disposition = {}
    for name, expected in direct.items():
        result = post[name]['status'] if name in post else 'unsat'
        if result != expected['status'] or result not in ('sat', 'unsat'):
            raise ValueError(f'proof reuse disagrees with exhaustive claim audit: {name}')
        structural = ordinary_post[name]['status'] if name in ordinary_post else 'unsat'
        if structural != expected['status']:
            raise ValueError(f'ordinary proof reuse disagrees with full claim audit: {name}')
        disposition[name] = ('confirmed-invalid' if result == 'sat' else
                             'reproved' if name in post else 'retained-by-proof')
    return {'rtl_sha256': sha(source.encode()), 'detector_sha256': sha(bytes(table)),
            'same_detector_semantics': same, 'changed_detector_rows': sum(a != b for a,b in zip(table, reference_table)),
            'failed_rules': failed, 'rule_rechecks': rules, 'egg_claims_to_recheck': recheck,
            'ordinary_claims_to_recheck': ordinary_recheck, 'rechecked_claims': post,
            'ordinary_rechecked_claims': ordinary_post, 'full_reference': direct,
            'full_rule_reference': full['rules'], 'disposition': disposition,
            'queries': {'egg_rule_plus_target': len(rules)+len(post),
                        'ordinary_rule_plus_target': len(rules)+len(ordinary_post),
                        'direct_same_semantic_skip': 0 if same else len(direct),
                        'direct_oracle_always': len(direct)}}


DEFAULT_REPLAY = ROOT / 'results/milestone3/eco-replay/summary.json'


def run(binary, out, replay_evidence=DEFAULT_REPLAY):
    saved = ROOT / 'results/milestone3/arbiter-inputs/ground.json'
    data = saved.read_bytes()
    payload = json.loads(data)
    targets, rules, _ = profiles()
    original_rules = [dict(name=n, left=a, right=b, proof_status='unsat') for n, a, b in rules]
    if payload != {'targets': targets, 'verified_rules': original_rules}:
        raise ValueError('saved guards do not match the pinned DUT adapter')
    proc = subprocess.run([binary.resolve(), 'indexed'], input=data, capture_output=True, check=True, timeout=60)
    if json.loads(proc.stderr)['mode'] != 'indexed':
        raise ValueError('incorrect engine mode')
    graph = json.loads(proc.stdout)
    # Timings do not form part of the proof and would vary on identical reruns.
    del graph['saturation_seconds']
    audit = validate_proof_dependencies(payload, graph)
    deps = {}
    for edge in audit['edges']:
        parts = [i.rsplit('/', 1) for i in (edge['left'], edge['right'])]
        if parts[0][0] != parts[1][0] or {p[1] for p in parts} != {'source','alternate'}:
            raise ValueError('unexpected endpoints')
        deps[parts[0][0]] = edge['ground_rules']
    ordinary = direct_receipts(payload)
    if len(deps) != 16 or set(deps) != set(ordinary):
        raise ValueError('incomplete proof inventory')
    cases = variants()
    replay_bytes = replay_evidence.read_bytes()
    reference_table = detector_table(cases['baseline'])
    rows = {}
    formal = {}
    rule_ids = {r['name'] for r in original_rules}
    for name, source in cases.items():
        table = reference_table if name == 'baseline' else detector_table(source)
        full = certify_eco(table)
        if set(full['rules']) != rule_ids or set(full['claims']) != set(deps):
            raise ValueError(f'incomplete full reference for {name}')
        formal[name] = full
        if name == 'baseline':
            if any(r['status'] != 'unsat' for family in full.values() for r in family.values()):
                raise ValueError('uncertified starting claim or rule')
        else:
            rows[name] = check_case(source, table, reference_table, deps, ordinary, full)
    replay_check = compare_replay(cases, formal, json.loads(replay_bytes))
    replay_check['evidence_sha256'] = sha(replay_bytes)

    out.mkdir(parents=True, exist_ok=False)
    write_json(out / 'proofs.json', graph)
    write_json(out / 'receipts.json', {'egg': audit, 'ordinary_ground_rules_by_claim': ordinary,
                                      'payload_sha256': sha(data), 'engine_sha256': sha(binary.read_bytes()),
                                      'baseline_rtl_sha256': sha(cases['baseline'].encode()),
                                      'baseline_rule_and_target_checks': formal['baseline']})
    costs = Counter()
    claims = Counter()
    for row in rows.values():
        costs.update(row['queries'])
        claims.update(row['disposition'].values())
    write_json(out / 'cases.json', rows)
    write_json(out / 'summary.json', {'cases':len(rows),'claims_per_case':len(deps),
               'all_reference_outcomes_agree':True, 'dispositions':dict(claims),
               'independent_replay_comparison': replay_check,
               'executed_egg_target_rechecks': sum(len(r['rechecked_claims']) for r in rows.values()),
               'executed_ordinary_target_rechecks': sum(len(r['ordinary_rechecked_claims']) for r in rows.values()),
               'same_recheck_set_as_ordinary': all(r['egg_claims_to_recheck']==r['ordinary_claims_to_recheck'] for r in rows.values()),
               'queries_after_baseline':dict(costs),
               'scope':'Only the ten source-checked edits. Counts exclude detector truth tables and initial certification.'})


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--binary', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--replay-evidence', type=Path, default=DEFAULT_REPLAY,
                    help='independent full-domain enumeration and Icarus replay summary')
    args = ap.parse_args()
    run(args.binary, args.output, args.replay_evidence)
