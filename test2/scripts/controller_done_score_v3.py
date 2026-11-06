"""Independent frozen-trace grading. No hidden result returns to the generator."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_loop_v2 import verify_data
from controller_done_runtime import replay
from controller_release_live import verify_release,ARMS


def position(p):return (p[0],0 if p[1]=='pre' else 1)


from controller_done_adjudication_v3 import adjudicate


def token_cost(records):
    attempted=[r for r in records if r.get('generation_request_issued')]
    known=[r.get('usage') for r in attempted if r.get('usage') and isinstance(r['usage'].get('input_tokens'),int) and isinstance(r['usage'].get('output_tokens'),int)]
    # Missing usage is unknown, never a zero-cost failed request.
    return dict(generation_requests=len(attempted),count_requests=sum(bool(r.get('count_request_issued')) for r in records),
                known_input_tokens=sum(u['input_tokens'] for u in known),known_output_tokens=sum(u['output_tokens'] for u in known),
                unknown_usage_requests=len(attempted)-len(known),
                actual_total_tokens=sum(u['input_tokens']+u['output_tokens'] for u in known) if attempted and len(known)==len(attempted) else None)


def evaluate(run_root,out):
    snapshots=verify_release(run_root)  # This must precede any hidden observation read.
    verify_data();out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
    labels=json.loads((TASK/'measurements-v1/summary.json').read_text())['records']
    finals=json.loads((run_root/'final-candidates.json').read_text())['candidates']
    calls=[json.loads(x) for x in (run_root/'calls.jsonl').read_text().splitlines()];rows=[];cycles=0;replay_seconds=0.;replays=0
    for s in sorted(snapshots,key=lambda s:(s['round'],s['repetition'],s['arm'])):
        tag=f"{s['arm']}/rep{s['repetition']}/round{s['round']}";cases=[];cost=token_cost([r for r in calls if r['arm']==s['arm'] and r['repetition']==s['repetition'] and r['round']<=s['round']])
        if s['status']=='compiled':
            for label in labels:
                case=dict(source=label['source'],simulator=label['simulator'],trace=label.get('trace'),reference_status=label['status'])
                if label['status']!='complete':case.update(status='reference_infrastructure_unresolved')
                else:
                    directory=out/tag/label['source']/label['simulator']/label['trace']
                    result=replay(run_root/s['directory']/'compiled',json.loads((ROOT/label['directory']/'rows.json').read_text()),directory,out/'row-cache')
                    case.update(status='graded',**adjudicate(label,result),result_path=str((directory/'result.json').relative_to(out)),result_sha256=sha(directory/'result.json'))
                    replays+=1;cycles+=result['cycles'];replay_seconds+=result['execution']['seconds']
                cases.append(case)
        correct=[c for c in cases if c['source']=='correct']
        correct_gate=len(correct)==18 and all(c.get('complete') and c.get('oracle_verdict')=='PASS' and not c.get('candidate_alarm_samples') and not c.get('candidate_unknown_samples') for c in correct)
        categories={}
        for category in ('safety','response_completion','input_completion'):
            eligible=[c for c in cases if c['source']!='correct' and c.get('eligible',{}).get(category)]
            definite=[c for c in eligible if c['definite_detection'][category] and correct_gate]
            resolved=[c for c in eligible if c['fully_resolved_detection'][category] and correct_gate]
            categories[category]=dict(eligible_pairs=len(eligible),eligible_types=sorted({c['source'] for c in eligible}),
                definite_detected_pairs=len(definite),definite_detected_types=sorted({c['source'] for c in definite}),
                fully_resolved_detected_pairs=len(resolved),fully_resolved_detected_types=sorted({c['source'] for c in resolved}),
                oracle_unknown_pairs=sum(bool(c.get('oracle_unknown_records')) for c in eligible))
        observable={c['source'] for c in cases if c['source']!='correct' and c.get('oracle_verdict')=='FAIL'}
        detected=set().union(*(set(v['definite_detected_types']) for v in categories.values()))
        resolved=set().union(*(set(v['fully_resolved_detected_types']) for v in categories.values()))
        n=cost['actual_total_tokens'];row=dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],candidate_status=s['status'],correct_control_gate=correct_gate,
            marker_only_safety_signal_pairs=sum(bool(c.get('marker_only_safety_signal')) for c in cases),category_attribution='UNATTRIBUTED_ANY_SLOT',correct_alarm_pairs=sum(bool(c.get('candidate_alarm_samples')) for c in correct),correct_unknown_pairs=sum(bool(c.get('candidate_unknown_samples')) for c in correct),
            raw_mutation_types=12,raw_mutation_pairs=144,observable_types=sorted(observable),unobserved_types=sorted(set(f'N{i:02}' for i in range(1,13))-observable),
            categories=categories,definite_detected_types=sorted(detected),fully_resolved_detected_types=sorted(resolved),
            unresolved_pairs=sum(c.get('status')!='graded' or not c.get('complete') or bool(c.get('candidate_unknown_samples')) or bool(c.get('oracle_unknown_records')) for c in cases),
            physical_reference_PASS_alarm_pairs=sum(bool(c.get('physical_reference_PASS_alarm')) for c in cases),
            cost=cost,distinct_definite_types_per_1000_tokens=len(detected)*1000/n if n else None,
            distinct_fully_resolved_types_per_1000_tokens=len(resolved)*1000/n if n else None,cases=cases)
        rows.append(row);dump(out/'progress.json',dict(rounds=rows));print('graded',tag,correct_gate,sorted(detected),flush=True)
    endpoints=[r for r in rows if any((r['arm'],r['repetition'],r['round'])==(f['arm'],f['repetition'],f['selected_round']) for f in finals)]
    costs=token_cost(calls)
    result=dict(status='offline_scoring_complete',mode=json.loads((run_root/'run.json').read_text())['mode'],not_new_model_evidence=json.loads((run_root/'run.json').read_text())['mode']!='live',
                rounds=rows,selected_endpoints=[{k:v for k,v in r.items() if k!='cases'} for r in endpoints],
                costs=dict(**costs,monitor_replays=replays,replayed_cycles=cycles,replay_seconds=replay_seconds,wall_seconds=time.perf_counter()-start,new_physical_DUT_simulations=0,new_formal_jobs=0),
                scoring_registration_sha256=sha(BASE/'configs/controller_done_scoring_v3.json'),registration_sha256=sha(REG),evaluation_freeze_sha256=sha(TASK/'evaluation-freeze.json'),release_sha256=sha(run_root/'release.json'),scorer_sha256=sha(__file__),
                causal_claim=None,scope='Finite physical rows, no formal completion proof; definite obligations with unknown context remain separate')
    dump(out/'scores.json',result);verify_release(run_root);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();evaluate(a.run.resolve(),a.output.resolve())
