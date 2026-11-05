"""Post-run descriptive target analysis and separately accounted failure replay.

Never changes frozen targets, model prompts or checker logic. No API calls.
"""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_runtime import BASE,simulate
from spi_core_safe_experiment import verify_freeze

def read(p):return json.loads(p.read_text())

def diagnose(folder,out):
    f=verify_freeze(folder/'freeze.json');s=read(folder/'summary.json')
    if s['metadata']['status']!='completed':raise ValueError('Wait for frozen run completion')
    out.mkdir(parents=True,exist_ok=False)
    pre=ROOT/f['transport_preflight'];cal=read(pre/'summary.json')['cases']
    ordinary=[n for n in cal if n.startswith('calibration_ordinary')]
    def covered(names):
        hits={g['eclass']:[False]*len(g['counter_identities']) for g in f['targets']}
        for name in names:
            for g in cal[name]['groups']:hits[g['eclass']]=[a or b>0 for a,b in zip(hits[g['eclass']],g['raw_source_hits'])]
        return sorted(k for k,v in hits.items() if all(v))
    ordinary_hit=covered(ordinary)
    additional={n:sorted(set(covered(ordinary+[n]))-set(ordinary_hit)) for n in cal
                if n.startswith('calibration_') and n not in ordinary and n!='calibration_seed'}
    first=[]
    for r in s['rows']:
        if r['round']==1:
            first.append({'repetition':r['repetition'],'new_cycles':r['unique_generated_cycles'],
              'unhit_groups':[g['eclass'] for g in r['groups'] if not g['all_hit']],
              'stall_group_315':next(g for g in r['groups'] if g['eclass']==315),
              'passed_event_families':sorted({e['family'] for e in r['checker']['events'] if e['kind']=='pass'}),
              'checker_verdict':r['checker']['verdict']})
    failure_replays=[]
    # Use the existing fixed-driver Icarus binary from final preflight. This is
    # extra diagnostic work, not additional budget for the experimental model.
    for rep in range(1,4):
        failing=next((r for r in s['rows'] if r['repetition']==rep and r['status']=='simulated' and r['checker']['verdict']=='fail'),None)
        if not failing:continue
        batch=folder/f'rep{rep}'/f"round{failing['round']}"
        requests=read(batch/'requests.json')['actions']
        result,_,trace,ledger=simulate(pre/'iverilog/tb.vvp',requests,out/f'rep{rep}-round{failing["round"]}-icarus','iverilog')
        original=read(batch/'result.json')
        same=trace==read(batch/'trace.json') and ledger==read(batch/'transport.json') and result['checker']==original['checker']
        if not same:raise ValueError('Diagnostic cross-simulator mismatch; inspect preserved artifacts')
        failcycles=[a['cycle'] for a in result['checker']['failures']]
        excerpt=[r for r in trace if min(failcycles)-10<=r['cycle']<=max(failcycles)]
        failure_replays.append({'repetition':rep,'round':failing['round'],'dual_simulator_trace_queue_checker_equal':same,
          'new_executions':1,'new_cycles':len(trace),'seconds':result['simulation_seconds'],
          'failure_diagnostics':result['checker']['failures'],
          'distinct_categories':sorted({a['category'] for a in result['checker']['failures']}),
          'assumption_violations':result['checker']['assumption_violations'],
          'trace_excerpt':excerpt,
          'attribution':'Reproduced checker rejection on unchanged DUT and valid transport. DUT versus checker/spec-attribution remains unresolved; cross-simulator agreement is not a golden proof.'})
    evidence={'scope':'Post-run descriptive analysis, never used to select this run or modify its prompts/targets.',
      'ordinary_cases':ordinary,'ordinary_complete_groups':ordinary_hit,'additional_groups_by_multistep_calibration':additional,
      'first_round_observations':first,'source_evidence':{str(g['eclass']):[
        {'counter_identity':i,'text':(ROOT/i[0]).read_text().splitlines()[i[1]-1]} for i in g['counter_identities']]
        for g in f['targets'] if g['eclass'] in (51,315)},
      'failure_replays':failure_replays,'diagnostic_compilations':0,'diagnostic_executions':len(failure_replays),
      'diagnostic_executed_cycles':sum(r['new_cycles'] for r in failure_replays),'new_API_calls':0,
      'interpretation':'Group 315 observes stall activation, not completed starvation/backpressure recovery. Group 51 is FULLCYC mode. Natural source redundancy and reachability do not establish useful task difficulty.',
      'counterfactual_limit':'Old direct-pin B and new offer B are separate unpaired development runs. Do not attribute coverage/timing differences solely to driver changes.',
      'provenance':{'preflight_sha256':sha(pre/'summary.json'),'live_summary_sha256':sha(folder/'summary.json'),'script_sha256':sha(Path(__file__))}}
    (out/'diagnosis.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({k:evidence[k] for k in ('ordinary_complete_groups','diagnostic_executions','diagnostic_executed_cycles','new_API_calls')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();diagnose(a.input.resolve(),a.output.resolve())
