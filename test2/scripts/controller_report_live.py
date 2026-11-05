#!/usr/bin/env python3
"""Descriptive registered controller B/C report; no post-outcome model feedback."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import statistics
from common import dump, sha
from controller_release_live import ARMS,verify_release
from controller_loop_live import REG,load,verify_task
from controller_score_live import measured_tokens


def report(run,scoring,out):
    verify_release(run);reg=load(REG);verify_task(reg)
    scores=load(scoring/'scores.json')
    if sha(scoring/'scores.json')!=load(scoring/'completion.json')['scores_sha256']:raise ValueError('Incomplete/changed scoring')
    calls=[json.loads(s) for s in (run/'calls.jsonl').read_text().splitlines()]
    out.mkdir(parents=True,exist_ok=False)
    accounting=[]
    for r in calls:
        usage=r.get('usage') or {}
        accounting.append({k:r.get(k) for k in ('arm','repetition','round','attempt','status','generation_request_issued','count_request_issued','accepted_response','input_token_count')} | usage | {'input_count_matches_usage':r.get('input_token_count')==usage.get('input_tokens') if usage.get('input_tokens') is not None else None})
    generated=[r for r in accounting if r['generation_request_issued']]
    budget_violations=[r for r in generated if (r.get('input_tokens') is not None and r['input_tokens']>64000) or (r.get('output_tokens') is not None and r['output_tokens']>8192)]
    initial_counts=sum(load(REG.parent.parent.parent/p)['count_requests'] for p in reg['token_count_reports'])
    summary={'mode':scores['mode'],'candidate_generation_requests':len(generated),'count_requests_during_generation':sum(r['count_request_issued'] for r in accounting),'initial_count_requests':initial_counts,
             'failed_or_unaccepted_generation_requests':sum(not r['accepted_response'] for r in generated),
             'missing_usage_generation_requests':sum(r.get('input_tokens') is None or r.get('output_tokens') is None for r in generated),
             'budget_violations':budget_violations,'arms':{},'call_accounting':accounting,'scoring_costs':scores['costs'],'formal':[],
             'reference_freeze_sha256':scores['reference_freeze_sha256'],'run_release_sha256':sha(run/'release.json'),'scores_sha256':sha(scoring/'scores.json')}
    for arm in ARMS:
        totals=[measured_tokens(calls,arm,rep,6) for rep in (1,2,3)]
        finals=[f for f in scores['finals'] if f['selection']['arm']==arm]
        targets=[]
        for rep in (1,2,3):
            hits=[r for r in scores['rounds'] if r['arm']==arm and r['repetition']==rep and r['metrics'] and r['metrics']['suite_sound_on_fixed_controls'] and len(r['metrics']['distinct_mutants_killed'])==11]
            first=min(hits,key=lambda r:r['round']) if hits else None
            targets.append(dict(repetition=rep,reached=first is not None,round=first['round'] if first else None,tokens=first['tokens'] if first else None))
        values=[len(f['score']['metrics']['distinct_mutants_killed']) if f['score'] and f['score']['metrics'] else 0 for f in finals]
        summary['arms'][arm]=dict(total_tokens_by_session=totals,mean_total_tokens=statistics.mean(totals) if all(t is not None for t in totals) else None,
                                 final_distinct_kills_by_session=values,mean_final_distinct_kills=statistics.mean(values),cost_to_all11=targets)
    b=summary['arms'][ARMS[0]]['mean_total_tokens'];c=summary['arms'][ARMS[1]]['mean_total_tokens']
    summary['C_token_increase_percent']=(c/b-1)*100 if b and c else None
    for f in scores['formal']:
        jobs=f['jobs'];witnesses=[j['witness'] for j in jobs if 'witness' in j]
        summary['formal'].append(dict(arm=f['arm'],repetition=f['repetition'],status_counts=dict(Counter(j['status'] for j in jobs)),
                                     correct_status_counts=dict(Counter(j['status'] for j in jobs if j['source']=='correct')),
                                     mutant_status_counts=dict(Counter(j['status'] for j in jobs if j['source']!='correct')),
                                     witness_classifications=dict(Counter(w['classification'] for w in witnesses)),wall_seconds=f.get('wall_seconds')))
    dump(out/'audit.json',summary)
    columns=['arm','repetition','round','status','sound_on_fixed_controls','distinct_kills','correct_alarms','correct_unknown','eligible_pair_kills','tokens','kills_per_1000_tokens']
    with (out/'rounds.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns);writer.writeheader()
        for r in scores['rounds']:
            m=r['metrics'] or {};writer.writerow(dict(arm=r['arm'],repetition=r['repetition'],round=r['round'],status=r['status'],sound_on_fixed_controls=m.get('suite_sound_on_fixed_controls'),distinct_kills=len(m['distinct_mutants_killed']) if m else None,correct_alarms=m.get('correct_control_alarm_records'),correct_unknown=m.get('correct_control_unknown_records'),eligible_pair_kills=m.get('valid_mutant_trace_kills'),tokens=r['tokens'],kills_per_1000_tokens=m.get('distinct_mutant_kills_per_1000_tokens')))
    text=['# Controller B/C matched-cap experiment','',f'Mode: {scores["mode"]}. Independent finite-trace reference unchanged; all36 snapshots frozen before hidden scoring. Fixed stimuli and raw3168 coverage counters do not change across monitor rounds.','',
          '| Arm | Rep | Selected round | No alarms/unknown on correct controls | Valid distinct faults /11 observable (/12 raw) | Eligible pairs /106 | Input+output tokens through round6 |',
          '|---|---:|---:|---|---:|---:|---:|']
    for f in scores['finals']:
        s=f['selection'];r=f['score'];m=(r or {}).get('metrics') or {}
        total=measured_tokens(calls,s['arm'],s['repetition'],6)
        text.append(f'| {s["arm"]} | {s["repetition"]} | {s["selected_round"]} | {m.get("suite_sound_on_fixed_controls","unresolved")} | {len(m.get("distinct_mutants_killed",[]))} | {m.get("valid_mutant_trace_kills","unresolved")} | {total} |')
    text+=['','## Predeclared strata','', '| Arm | Rep | Stratum | Observable / raw faults | Killed types | Eligible-pair kills / pairs |','|---|---:|---|---:|---|---:|']
    for f in scores['finals']:
        s=f['selection'];r=f['score']
        for name in reg['strata_before_outcomes']:
            m=(r or {}).get('strata',{}).get(name,{})
            text.append(f'| {s["arm"]} | {s["repetition"]} | {name} | {len(m.get("eligible_mutants",[]))} / {m.get("raw_mutant_denominator",4)} | {", ".join(m.get("distinct_mutants_killed",[])) or "none"} | {m.get("valid_mutant_trace_kills","unresolved")} / {m.get("eligible_mutant_trace_count","unresolved")} |')
    text+=['','## Actual token accounting','',f'Generation requests: {len(generated)}; unaccepted: {summary["failed_or_unaccepted_generation_requests"]}; usage missing: {summary["missing_usage_generation_requests"]}; count requests during generation: {summary["count_requests_during_generation"]}; initial count requests:{initial_counts}, including the retained over-cap first representation. Failed attempts are included in cumulative tokens. Cached input/reasoning output are subsets, never added twice. Budget violations: {len(budget_violations)}. Actual prompt lengths need not be equal under matched caps.','']
    for arm,d in summary['arms'].items():
        text.append(f'- {arm}: total tokens/session {d["total_tokens_by_session"]}; mean {d["mean_total_tokens"]}; cost-to-all11 {d["cost_to_all11"]}.')
    text+=[f'- C mean token change: {summary["C_token_increase_percent"]}%.','','## Formal scope','', 'Final six candidates only. Correct source:6 slots × bmc/prove/cover ×10s;12 faults ×6 slots ×bmc ×5s. Depth24, Z3, flatten;540s declared solver caps and720s overall cap/candidate. PASS in bounded/cover modes is separate from proof. TIMEOUT/ERROR/NOT_RUN and failed induction remain unresolved. Reachable BMC witnesses are classified only by the frozen independent reference.','']
    for f in summary['formal']:text.append(f'- {f["arm"]} rep{f["repetition"]}: {f["status_counts"]}; witness classifications {f["witness_classifications"]}; wall {f["wall_seconds"]}s.')
    text+=['','## Limits','', 'Three sessions per arm on one previously inspected IP family. Descriptive comparisons only; no significance claim. C is a larger feedback package without a token-matched placebo, so this does not isolate pure E-graph semantics. All four supplied semantic groups already have development source hits; representation/guard interpretation rather than uncovered-source discovery is being tested. M08 is retained among12 raw faults with no independently confirmed fixed-trace violation. The other11 have106/144 eligible simulator/trace pairs; ineligible and unknown outcomes remain in raw records. Correct-control acceptance is finite evidence, not complete monitor soundness or proof of full design correctness. Formal assumes legal held input offers, reset, and1..12 accepted bytes per frame; no fairness/liveness proof.','', 'Machine evidence: `audit.json`, `rounds.csv`, immutable generation release and scoring completion hashes above.']
    (out/'report.md').write_text('\n'.join(text)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('call_accounting','formal')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--scoring',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();report(a.run.resolve(),a.scoring.resolve(),a.output.resolve())
