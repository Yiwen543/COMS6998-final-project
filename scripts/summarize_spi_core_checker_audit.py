"""Reconcile raw role calls, immutable checker controls and reviewer corrections."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from run_claude_divider_audit import KEY_FILE

def summarize(base):
    role=base/'claude-checker-v1';candidate=role/'candidate';auth=json.loads((candidate/'authorship.json').read_text())
    for f,h in auth['artifact_sha256'].items():
        if sha(candidate/f)!=h:raise ValueError('Claude author artifact changed')
    calls=[]
    for name in ('author','review'):
        m=json.loads((role/name/'metadata.json').read_text());u=m['usage']
        inp=sum(u.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
        calls.append({'role':name,'requested_model':m['requested_model'],'returned_models':list(m['model_usage']),
            'normal_input_tokens':u.get('input_tokens',0),'cache_creation_input_tokens':u.get('cache_creation_input_tokens',0),'cache_read_input_tokens':u.get('cache_read_input_tokens',0),
            'input_tokens_total':inp,'output_tokens':u['output_tokens'],'input_plus_output_tokens':inp+u['output_tokens'],
            'thinking_tokens_subset_of_output':u.get('output_tokens_details',{}).get('thinking_tokens'),
            'total_cost_usd':m['total_cost_usd'],'wall_seconds':m['wall_seconds'],'status':m['status'],
            'prompt_sha256':m['prompt_sha256'],'tools':m['tools'],'CLI_budget_usd':m['budget_usd']})
    initial=json.loads((base/'spi-checker-evaluation-v1/summary.json').read_text())
    full=json.loads((base/'spi-checker-evaluation-v1/evaluations.json').read_text())
    follow=json.loads((base/'spi-checker-postreview-v1/evaluation/summary.json').read_text())
    review=json.loads((role/'review.json').read_text())
    tx=json.loads((base/'spi_core_events-v3/tx_starvation_resume/trace.json').read_text())
    stall=[r for r in tx if r['pre']['tx_stall']]
    underflow=[f for f in full['cases']['calibration/tx_starvation_resume']['failures'] if f['category']=='tx_underflow']
    observed_moves=[r['cycle'] for r in stall if r['pre']['sck']!=r['post']['sck']]
    if underflow or observed_moves:raise ValueError('Reviewer correction no longer supported')
    evidence_rows=[r for r in tx if r['cycle'] in (73,74,127,128,129,130)]
    corrections=[{'finding':'F3','disposition':'Event-reporting gap confirmed; reviewer underflow/park-edge interpretation contradicted by full evidence.',
        'full_failure_categories':sorted({f['category'] for f in full['cases']['calibration/tx_starvation_resume']['failures']}),
        'tx_underflow_failures':0,'pre_stall_cycles':len(stall),'SCK_changes_pre_to_post_while_pre_stall':observed_moves,'rows':evidence_rows,
        'integration_analysis':'Cycle73 is the final sample of byte3. SCK holds high over stalled pre cycles74..128. New word handshakes128, trailing edge129, next leading sample130. fetch()/starve only tests at the sample; previous last edge is129, so wc=128 > last=129 is false. It misses the actual 55-cycle stall. No original-DUT clock-under-stall defect is established by this trace.'},
        {'finding':'F4','disposition':'Replaced invalid copied-output control with causally re-simulated offered-then-withdrawn command on a clean uniform-byte baseline. Original control remains uncredited.'},
        {'finding':'F6','disposition':'Added actual in-flight hardware reset/restart, reset-CS mutation and truncated reset control. These post-review controls were not seen by the first reviewer.'},
        {'finding':'F1','disposition':'Pinned RTL packer inspection independently confirms low-byte-first behavior at this core boundary, contrary to supplied pinned documentation. Documentation authority/contract resolution remains blocking. Do not silently change checker or RTL.'}]
    sim=json.loads((base/'spi-checker-postreview-v1/simulation/observations.json').read_text())
    result={'status':'checker_candidate_not_frozen_B_disabled','B_allowed':False,'checker_ready':False,'review_ready_for_offline_gate':review['ready_for_offline_gate'],
        'roles':{'author':'claude-opus-5-5 spec/interface only','controls_driver':'GPT/Codex','reviewer':'fresh isolated claude-opus-5-5 session; read-only','final_evidence_reconciliation':'Tool results and integration audit; reviewer is not an oracle'},
        'initial_controls':initial['control_counts'],'author_selftests':{'passed':sum(bool(x['pass']) for x in initial['selftests']),'total':len(initial['selftests'])},
        'initial_cases':len(initial['cases']),'supplementary_cases':len(follow['cases']),
        'supplementary_results':{n:{k:r[k] for k in ('verdict','failures','assumption_violations','events','unresolved')} for n,r in follow['cases'].items()},
        'review_corrections_and_followups':corrections,
        'blocking':['Pinned public byte-order contract disagrees with actual core behavior; original source/checker preserved.',
            'Checker uses accepted queue instead of pending offer for CSAAT/CSID release.',
            'TX starvation event is silently omitted by checker despite an observed stall.',
            'Software-reset completeness, broader mode/timing controls and nonuniform RX recovery still insufficient.',
            'Most source groups are ordinary-traffic covered; no B-development or C-effectiveness acceptance established.'],
        'accounting':{'generation_calls':1,'review_calls':1,'OpenAI_calls':0,'calls':calls,
            'input_tokens_total':sum(x['input_tokens_total'] for x in calls),'output_tokens_total':sum(x['output_tokens'] for x in calls),'input_plus_output_tokens':sum(x['input_plus_output_tokens'] for x in calls),
            'thinking_tokens_included_not_added':sum(x['thinking_tokens_subset_of_output'] or 0 for x in calls),'reported_total_cost_usd':sum(x['total_cost_usd'] for x in calls),'API_call_wall_seconds_sum':sum(x['wall_seconds'] for x in calls),
            'new_simulation_compilations':len(sim['compilations']),'new_simulation_executions':sim['executions'],'new_executed_cycles_both_simulators':sim['total_executed_cycles'],
            'new_compile_seconds':sum(x['seconds'] for x in sim['compilations']),'new_simulation_seconds':sum(s['seconds'] for c in sim['cases'] for s in c['simulations']),
            'oversized_review_packets_rejected_locally':1,'failed_review_API_calls':0,'credential_deleted':not KEY_FILE.exists(),
            'tokens_policy':'Use top-level reported usage once. Anthropic normal input + cache creation + cache read = total input. Output already includes thinking. Do not add iterations/modelUsage/cache sub-breakdowns again.'},
        'next':'Resolve normative core byte-order contract before author repairs. Preserve original contradictory contract result. Claude must author checker logic corrections; do not make GPT patches to expected outputs. No additional API call authorized by this result.',
        'hashes':{str(p):sha(p) for p in [candidate/'checker.py',candidate/'properties.json',role/'review.json',base/'spi-byte-order-diagnosis.json',base/'spi-checker-evaluation-v1/evaluations.json',base/'spi-checker-postreview-v1/evaluation/evaluations.json',Path(__file__)]}}
    (base/'checker-audit-decision.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'calls':len(calls),'cost_usd':result['accounting']['reported_total_cost_usd'],'tokens':result['accounting']['input_plus_output_tokens'],'credential_deleted':result['accounting']['credential_deleted']}))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);summarize(p.parse_args().base.resolve())
