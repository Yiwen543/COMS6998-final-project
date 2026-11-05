"""Evidence ledger for contract v2; no model calls and no checker mutations."""
import json
from pathlib import Path
from real_parent_screen import configuration,verify,SCOPE
from probe_spi_core_events import identity
from run_midterm_fixed import ROOT,sha


def run():
    b=ROOT/'results/real_parent_screen_20261104';c=configuration('spi_host_core');verify(c)
    role=b/'claude-checker-v2';current=b/'contract-repair-v3/rx-window/prepatch-evaluation/summary.json'
    ledger=[]
    for label in ('author','review'):
        m=json.loads((role/label/'metadata.json').read_text());u=m['usage']
        ledger.append({'role':label,'requested_model':m['requested_model'],'returned_models':list(m['model_usage']),
          'status':m['status'],'input_tokens':sum(u.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens')),
          'output_tokens':u['output_tokens'],'thinking_tokens_subset_of_output':u.get('output_tokens_details',{}).get('thinking_tokens',0),
          'cost_usd':m['total_cost_usd'],'wall_seconds':m['wall_seconds'],'metadata_sha256':sha(role/label/'metadata.json')})
    old=json.loads((b/'spi_core_events-v3/seed/raw-points.json').read_text());denom={identity(p) for p in old}
    runs=[]
    for folder in (b/'contract-repair-v2/probes',b/'contract-repair-v3/rx-window/simulation'):
        r=json.loads((folder/'observations.json').read_text());runs.append(r)
        for case in r['cases']:
            points=json.loads((folder/case['case']/'raw-points.json').read_text())
            if {identity(p) for p in points}!=denom:raise ValueError('Raw counter denominator drift')
    for name in ('claude-checker-v1','claude-checker-v2'):
        p=b/name/'candidate';a=json.loads((p/'authorship.json').read_text())
        for f,h in a['artifact_sha256'].items():
            if sha(p/f)!=h:raise ValueError('Checker authorship drift')
    s=json.loads(current.read_text());initial=json.loads((b/'contract-repair-v2/evaluation/summary.json').read_text())
    report={'status':'contract_resolved_checker_not_frozen_waiting_author_repair','B_allowed':False,'C_allowed':False,
      'contract_id':'spi_host_core_public_contract_v2_lsb','authority_sha256':sha(b/'contract-repair-v2/authority/contract.json'),
      'authority_limit':'Project interpretation of conflicting pinned upstream documentation and unchanged parent boundary mapping, not a maintainer erratum.',
      'checker_version':'claude-checker-v2','checker_sha256':sha(role/'candidate/checker.py'),
      'review_ready':json.loads((role/'review.json').read_text())['ready_for_offline_gate'],
      'model_calls':ledger,'API_total_tokens':sum(r['input_tokens']+r['output_tokens'] for r in ledger),
      'reported_cost_usd':sum(r['cost_usd'] for r in ledger),'OpenAI_calls':0,
      'initial_control_counts':initial['control_counts'],'initial_evaluated_cases':len(initial['cases']),
      'expanded_controls':{'cases':len(s['cases']),'independent_positive':s['control_counts']['independent_positive'],
        'no_false_alarm':s['control_counts']['no_false_alarm'],'missing_events':s['event_integrity_errors'],
        'aligned_rx_full0':s['cases']['probe/read_full0_aligned']['verdict']},
      'blocking_distinct_issues':['checker CPOL1 idle setup misattributed as selected serial edge','checker TX starvation trigger/event omission'],
      'fixed_infrastructure_issue':'Evaluator now rejects missing required_event_family; 5 expanded controls flag omission. Earlier empty event_integrity_errors retained as historical measurement limitation.',
      'controls_correction':'Old FULLCYC0 private input used FULLCYC1 clock schedule and is retained as sampling-ambiguous. New resimulated aligned input passes existing v2 checker without checker changes.',
      'review_corrections':[
        'F4/F7 claim no real pending CSID control beyond selftests is too strong: calibration/partial_then_csid_switch was included in full, with valid newCSID before acceptance and checker pass.',
        'F5 first diagnostic is a half-period glitch, but full ledger ALSO has tx_underflow. The one-row output glitch still does not establish fault coverage for timing-clean illegal stall pulses.',
        'Review supplies useful hypotheses; full local evidence remains authoritative. CPOL and missing-event blockers independently reproduced using hand controls.'
      ],
      'simulation_accounting':{'compilations':sum(len(r['compilations']) for r in runs),'executions':sum(r['executions'] for r in runs),
        'actual_cycles_all_simulators':sum(r['total_executed_cycles'] for r in runs),
        'compile_seconds':sum(x['seconds'] for r in runs for x in r['compilations']),
        'simulate_seconds':sum(x['seconds'] for r in runs for c in r['cases'] for x in c['simulations']),
        'trace_agreement':all(c['trace_agreement'] for r in runs for c in r['cases']),
        'raw_DUT_denominator':len(denom),'reference_counter_identity_verified':True,'hand_trace_mutations_execute_zero_DUT_cycles':True},
      'unchanged_registration_sha256':sha(SCOPE),'next_patch_packet_sha256':sha(b/'contract-repair-v3/packet/packet.json'),
      'staged_anthropic_key_present':(ROOT/'build/private/anthropic-crosscheck-key').exists(),
      'limits':['Software reset remains unresolved; pass_unresolved is not counted as successful recovery.',
        'Independent checker controls are finite and not formal proof. No RTL mutant claim.',
        'Only41 of47 initial traces supplied losslessly to reviewer; omitted6 successful CPOL0 supplemental traces named in preflight. All47 evaluations supplied with disclosed diagnostic truncation.',
        'No development or formal A/B/C/placebo model calls. Original budget/gates and20 source groups unchanged.',
        'Ordinary traffic already hits16/20 groups; nothing here establishes a C advantage or held-out independence.']}
    p=b/'contract-repair-decision.json';p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'report':str(p),'B_allowed':False,'API_tokens':report['API_total_tokens'],'reported_cost_usd':report['reported_cost_usd'],'simulations':report['simulation_accounting']}))


if __name__=='__main__':run()
