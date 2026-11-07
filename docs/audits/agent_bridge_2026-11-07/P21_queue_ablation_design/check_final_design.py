"""Bounded static P21 delta checks. No imports of project code or toolchain calls."""
import csv
import hashlib
import json
import math
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
EXPECTED = {
    'docs/designs/queue_efficiency_ablation_v1/plan.md': '251efaff2cfd32f08220747d32de1a72e248b3200f434a8128fa1d8dbc6d9774',
    'docs/designs/queue_efficiency_ablation_v1/plan.json': '0f50311b3e5b1e0066740d9e761a295bd04391b7769c37d8b87138f4c3cf73e4',
    'docs/designs/queue_efficiency_ablation_v1/old-pilot-summary.json': 'ec900807f5529bd02a7c141c129a2554c0b60eff1a89dd0ada63634f145be06e',
    'docs/designs/queue_efficiency_ablation_v1/reuse-inventory.json': '3661ea4b66fc8154364bd7be25a471e242a38ccae7deb193e162e560786727cb',
    'docs/designs/queue_efficiency_contract_v1.json': '229ab3b3d99c597bba92a367e7697ef39bc1c039098b395382773cff9b94cc64',
    'docs/designs/queue_property_author_v2/property-obligations-draft.md': '7a40800c4e7aa52520a01081f44c60dc5eb6911d808582007a4f92afc8cc9655',
    'docs/designs/queue_property_author_v2/role-inputs.json': '18dc3766cc9a419aedc9eec5cbbd7acd16212f2d60c9290f5bb7f9ade6850c4a',
    'docs/audits/queue_ablation_budget_2026-11-07/price-basis-and-estimate.json': '30fb95c89f8e137d633d0e89a90fc67bda2958a4061259b7f3b8e0bcdcdfa3b5',
}
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads((ROOT / p).read_text())
for name, digest in EXPECTED.items():
    assert sha(ROOT / name) == digest, name
plan = load('docs/designs/queue_efficiency_ablation_v1/plan.json')
summary = load('docs/designs/queue_efficiency_ablation_v1/old-pilot-summary.json')
reuse = load('docs/designs/queue_efficiency_ablation_v1/reuse-inventory.json')
roles = load('docs/designs/queue_property_author_v2/role-inputs.json')
e, r, b = plan['execution'], plan['resource_plan'], plan['budget']
assert plan['live_allowed'] is False and plan['paid_authorization'] is None
assert plan['new_candidate_runner'] is None and plan['old_USD20_inherited'] is False
assert plan['common_contract']['sha256'] == EXPECTED['docs/designs/queue_efficiency_contract_v1.json']
for item in roles['retained_v1']['files_preserved'] + roles['technical_inputs']:
    assert sha(ROOT / item['path']) == item['sha256']
source_bindings = {**summary['source_bindings'], **reuse['source_bindings']}
for name, digest in source_bindings.items():
    assert sha(ROOT / name) == digest, name
historical = {}
for name, row in reuse['historical_engine_and_frontend'].items():
    command = ['git', 'show', row['commit'] + ':' + name]
    result = subprocess.run(command, cwd=ROOT, capture_output=True)
    assert result.returncode == 0
    assert hashlib.sha256(result.stdout).hexdigest() == row['sha256']
    historical[name] = {'command': command, 'exit_code': result.returncode,
        'sha256': row['sha256'], 'current_sha256': sha(ROOT / name)}
schedule = e['scheduling']
counts = Counter((x['form'], x['arm'], x['session_index'], x['round']) for x in schedule)
expected_slots = {(f,a,s,n) for f in plan['forms'] for a in plan['arms']
    for s in range(1,4) for n in range(1,5)}
assert len(schedule) == 72 and set(counts) == expected_slots and set(counts.values()) == {1}
assert [x['round'] for x in schedule] == sorted(x['round'] for x in schedule)
assert e['normal_generation_slots'] == 72
assert e['max_transport_retries_per_session'] * e['total_sessions'] == e['max_extra_generation_dispatches'] == 18
assert e['max_generation_dispatches'] == 72 + 18 == 90
assert b['all_paid_dispatches_max'] == 90 + b['golden_author_max_calls'] == 92
assert b['recommended_new_USD_hard_ceiling'] == 15 and b['remote_count_calls'] == 0
assert b['GPT_full_context_reserve_microUSD'] == 5842584
assert b['Claude_full_context_reserve_microUSD'] == 5680224
per_session_cycles = sum(6+4*n for n in range(1,5))
assert per_session_cycles == e['max_replayed_stimulus_cycles_per_session'] == 64
assert r['future_main_replayed_cycles_max'] == 18 * 64 == 1152
assert r['total_sim_roots_max'] == 72 + r['seed_setup']['roots_max'] + r['private_reachability_smoke']['roots_max'] == 76
assert r['total_sim_cycles_max'] == 1152 + r['seed_setup']['cycles_max'] + r['private_reachability_smoke']['cycles_max'] == 1208
assert r['total_compile_builds_max'] == 2 and r['new_egg_or_Z3_proof_jobs'] == 0
assert e['shared_online_wall_seconds'] == 3600 and e['work_stop_before_cleanup_seconds'] < 3600
rounds_path = ROOT / 'results/queue_bc_gpt6sol_20261026/rounds.csv'
rounds = list(csv.DictReader(rounds_path.open()))
assert len(rounds) == 48 and len(summary['sessions']) == 12
retrospective = []
for session in summary['sessions']:
    selected = sorted([x for x in rounds if (x['version'],x['arm'],int(x['repetition'])) ==
        (session['form'],session['arm'],session['session_index'])], key=lambda x:int(x['round']))
    assert len(selected) == 4
    for key, predicate in [
        ('line_target', lambda x:int(x['line_covered'])>=41),
        ('joint_target_retrospective', lambda x:int(x['line_covered'])>=41 and int(x['branch_covered'])>=14 and int(x['toggle_covered'])>=344)]:
        first = next(x for x in selected if predicate(x))
        assert session[key]['first_round'] == int(first['round'])
        assert session[key]['tokens'] == int(first['cumulative_api_tokens'])
        assert session[key]['executed_cycles'] == int(first['cumulative_executed_cycles'])
    retrospective.append({k:session[k] for k in ('form','arm','session_index','line_target','joint_target_retrospective')})
for form in ('original','variant'):
    for arm in ('B','C'):
        sessions = [x for x in summary['sessions'] if x['form']==form and x['arm']==arm]
        for endpoint, metric in [('line_target','line_target_mean_tokens'),('joint_target_retrospective','joint_target_retrospective_mean_tokens')]:
            mean = sum(x[endpoint]['tokens'] for x in sessions)/3
            assert math.isclose(mean,summary['comparisons'][form]['by_arm'][arm][metric])
for endpoint, key in [('line_target','line_target_pairs'),('joint_target_retrospective','joint_target_retrospective_pairs')]:
    earlier=ties=0
    for form in ('original','variant'):
        for s in range(1,4):
            match={x['arm']:x[endpoint]['first_round'] for x in summary['sessions'] if x['form']==form and x['session_index']==s}
            earlier+=match['C']<match['B'];ties+=match['C']==match['B']
    assert (earlier,ties)==(summary[key]['C_earlier'],summary[key]['ties'])
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head == plan['actual_HEAD'] == '034a5a8db63f38878148aaac15ea69dbc150d29a'
for name, digest in EXPECTED.items():
    assert sha(ROOT/name)==digest
print(json.dumps({'status':'STATIC_DELTA_CHECKS_PASS','head':head,
    'exact_inputs_sha256':EXPECTED,'current_still_matches':True,
    'source_binding_count':len(source_bindings),'historical_read_only_objects':historical,
    'schedule_slots':len(schedule),'independent_session_cells':18,
    'rounds_csv_sha256':sha(rounds_path),'retrospective_checks':retrospective,
    'resource_arithmetic':{'generation_max':90,'golden_max':2,'paid_max':92,
        'simulation_roots_proposed':76,'simulation_cycles_proposed':1208,'compile_builds_proposed':2},
    'review_script_sha256':sha(Path(__file__)),
    'not_executed':['producer77checks','implementation/runtime/ABI qualification','API/count/model','compiler/simulator/Yosys/egg/Z3','credential access','Git mutation']},indent=2))
