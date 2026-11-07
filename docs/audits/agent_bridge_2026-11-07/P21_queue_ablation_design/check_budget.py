"""Arithmetic under the coordinator's saved price basis, not a live tariff lookup."""
import hashlib
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
path = ROOT / 'docs/audits/queue_ablation_budget_2026-11-07/price-basis-and-estimate.json'
raw = path.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '30fb95c89f8e137d633d0e89a90fc67bda2958a4061259b7f3b8e0bcdcdfa3b5'
basis = json.loads(raw)
calls_path = ROOT / basis['old_evidence']['path']
assert hashlib.sha256(calls_path.read_bytes()).hexdigest() == basis['old_evidence']['sha256']
calls = [json.loads(x) for x in calls_path.read_text().splitlines() if x.strip()]
assert len(calls) == 48
totals = {k: sum(x['usage'][k] for x in calls) for k in basis['old_evidence']['totals']}
assert totals == basis['old_evidence']['totals']
assert totals['input_tokens'] + totals['output_tokens'] == totals['total_tokens']
assert max(x['usage']['input_tokens'] for x in calls) == 42716
assert max(x['usage']['output_tokens'] for x in calls) == 447
D = Decimal
def ceil(x):
    return int(x.to_integral_value(rounding=ROUND_CEILING))
scenarios = []
for row in basis['planning_scenarios']:
    n = row['generation_attempts']
    # Two of three arms carry the proposed 1000-token structural appendix.
    i = ceil(D(totals['input_tokens']) * D(n) / 48 + D(n) * 2 / 3 * 1000)
    o = ceil(D(totals['output_tokens']) * D(n) / 48)
    price = (D(i) * D('2.5') + D(o) * 10) / 1000000 * D('1.1')
    assert (i, o) == (row['planning_input_tokens'], row['planning_output_tokens_including_reasoning'])
    assert price == D(str(row['cachewrite_plus10percent_USD']))
    scenarios.append({'attempts': n, 'input_planning': i, 'output_planning': o, 'USD_estimate': str(price)})
gpt_reserve_micro = ceil((D(1050000) * 5 + D(4096) * 15) * D('1.1'))
claude_reserve_micro = ceil((D(1000000) * 5 + D(8192) * 20) * D('1.1'))
assert gpt_reserve_micro == 5842584
assert claude_reserve_micro == 5680224
print(json.dumps({'price_basis_sha256': hashlib.sha256(raw).hexdigest(),
    'old_calls_sha256': hashlib.sha256(calls_path.read_bytes()).hexdigest(),
    'saved_usage_totals': totals, 'scenarios': scenarios,
    'GPT_reserve_microUSD': gpt_reserve_micro, 'Claude_reserve_microUSD': claude_reserve_micro,
    'proposed_normal_sessions': 18, 'proposed_normal_slots': 72,
    'proposed_transport_retry_slots': 18, 'proposed_generation_cap': 90,
    'proposed_golden_call_cap': 2, 'proposed_paid_call_cap': 92,
    'tariffs_independently_fetched_by_this_reviewer': False,
    'tariff_evidence': 'Coordinator saved basis with four official-source URLs and opened=true; no network used here.',
    'limits': ['Conditional arithmetic only; no live budget implementation or execution accepted.',
        '4-7 USD is a planning estimate, 15 USD is proposed and not authorized.',
        'Codex maintenance costs and actual invoices remain UNKNOWN.',
        'Unknown failed calls keep full reservation; caps do not guarantee all slots complete.'],
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
