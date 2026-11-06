#!/usr/bin/env python3
"""Post-release controller scoring. Never used by candidate generation."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
from common import ROOT, BASE, dump, sha
from controller_monitor_live import TASK, PINS, ROW_INPUTS, OUTPUTS, replay, formal_job
from controller_release_live import verify_release
from controller_loop_live import load, verify_task, REG, live_gate
from score import score, sample_time


def measured_tokens(calls, arm, rep, round_no):
    attempts=[r for r in calls if (r['arm'],r['repetition'])==(arm,rep) and r['round']<=round_no and r['generation_request_issued']]
    if not attempts or any(not r.get('usage') or any(r['usage'].get(k) is None for k in ('input_tokens','output_tokens')) for r in attempts):
        return None
    return sum(r['usage']['input_tokens']+r['usage']['output_tokens'] for r in attempts)


def strict_score(correct, faulty, eligibility, tokens):
    result=score(correct,faulty,eligibility,tokens)
    for e,d in zip(eligibility,result['details']):
        first=e.get('first_reference_failure');r=faulty.get((e['mutant'],e['trace']))
        onset=sample_time((first['cycle'],first['phase'])) if first else None
        early=bool(onset is not None and r and any(sample_time(f)<onset for p in r['properties'] for f in p['failures']))
        d['early_alarm_before_reference_violation']=early
        d['valid_kill']=d['valid_kill'] and not early
    killed={d['mutant'] for d in result['details'] if d['valid_kill']}
    result.update(distinct_mutants_killed=sorted(killed),observable_mutant_recall=len(killed)/len(result['eligible_mutants']),
                  valid_mutant_trace_kills=sum(d['valid_kill'] for d in result['details']),
                  distinct_mutant_kills_per_1000_tokens=len(killed)*1000/tokens if tokens else None)
    result['eligible_pair_detection_rate']=result['valid_mutant_trace_kills']/result['eligible_mutant_trace_count']
    return result


def decode_witness(path):
    ports={k:v for k,v in PINS.items() if k!='clk'}
    scopes=[]; ids={};step_id=None;header=True;values={};frames={};touched=set();partial={}
    def flush():
        if step_id in values:
            step=values[step_id]
            if step<0:raise ValueError('Unknown step')
            if set(ids.values())<=touched:frames[step]=dict(values)
            else:partial[step]=set(ids.values())&touched
    for raw in path.read_text().splitlines():
        line=raw.strip();words=line.split()
        if header:
            if line.startswith('$scope '):scopes.append(words[2])
            elif line.startswith('$upscope'):scopes.pop()
            elif line.startswith('$var '):
                if words[4]=='smt_step' and not scopes:step_id=words[3]
                if scopes==['formal_top'] and words[4] in ports:
                    if int(words[2])!=ports[words[4]] or words[4] in ids:raise ValueError('Port layout changed')
                    ids[words[4]]=words[3]
            elif line.startswith('$enddefinitions'):header=False
        elif line.startswith('#'):flush()
        elif line.startswith('b'):
            bits,ident=line[1:].split();value=-1 if any(x in bits.lower() for x in 'xz') else int(bits,2)
            if ident==step_id and values.get(step_id)!=value:touched.clear()
            values[ident]=value;touched.add(ident)
        elif line and line[0] in '01xz':
            values[line[1:]]=-1 if line[0] in 'xz' else int(line[0]);touched.add(line[1:])
    flush()
    if set(ids)!=set(ports) or step_id is None:raise ValueError('Missing public pins')
    if len(frames)<2 or sorted(frames)!=list(range(len(frames))):raise ValueError('Incomplete reachable witness')
    if any(s not in frames and (s!=len(frames) or fields) for s,fields in partial.items()):raise ValueError('Truncated witness')
    pins=[{k:frames[i][v] for k,v in ids.items()} for i in range(len(frames))]
    rows=[dict(cycle=i,inputs={k:a[k] for k in ROW_INPUTS},pre={k:a[k] for k in OUTPUTS},post={k:b[k] for k in OUTPUTS}) for i,(a,b) in enumerate(zip(pins,pins[1:]))]
    if rows[0]['inputs']['rst']!=1:raise ValueError('Missing initial reset')
    return rows


def witness_review(job, checker):
    result=dict(status='unresolved',classification='No complete reachable BMC witness')
    paths=sorted((job/'work').glob('engine_*/trace.vcd'))
    try:
        if len(paths)!=1:raise ValueError('Expected exactly one reachable trace')
        rows=decode_witness(paths[0]);dump(job/'witness-rows.json',rows)
        oracle=checker.check_rows(rows,require_drained=False,min_tail=32)
        dump(job/'witness-reference.json',oracle)
        classification={'PASS':'candidate_false_alarm_on_this_legal_trace','FAIL':'reference_confirmed_DUT_violation_on_this_trace','UNRESOLVED':'reference_unresolved','INVALID_INPUT':'invalid_witness_interface'}
        result.update(status='adjudicated' if oracle['verdict'] in ('PASS','FAIL') else 'unresolved',classification=classification[oracle['verdict']],reference_verdict=oracle['verdict'],witness_sha256=sha(paths[0]),rows=len(rows))
    except Exception as error:result.update(error_type=type(error).__name__,detail=str(error))
    dump(job/'witness-review.json',result);return result


def execute(run_root,out,formal=False):
    snapshots=verify_release(run_root)
    reg=load(REG);verify_task(reg)
    mode=load(run_root/'release.json')['mode']
    if mode=='live':live_gate()
    out.mkdir(parents=True,exist_ok=False)
    dump(out/'scoring-start.json',dict(release_sha256=sha(run_root/'release.json'),all36_frozen_before_hidden_access=True,mode=mode,scorer_sha256=sha(Path(__file__))))
    # First private/reference reads occur strictly after complete immutable release.
    eligibility=load(TASK/'reference/frozen-v2/fault-eligibility.json')
    faults=load(TASK/'private/mutant-catalog-v1.json')['faults']
    calls=[json.loads(s) for s in (run_root/'calls.jsonl').read_text().splitlines()]
    correct_rows={}
    for sim in ('iverilog','verilator'):
        for name in ('basic','boundary_pressure','reset_reuse'):
            correct_rows[sim+'/'+name]=load(TASK/'qualification/observations-v2'/sim/name/'rows.json')
        for i in range(1,7):
            name=f'heldout_{i:02}';correct_rows[sim+'/'+name]=load(TASK/'private/observations'/sim/name/'rows.json')
    faulty_rows={}
    for e in eligibility:
        path=TASK/'private/mutant-observations-v1'/e['mutant']/e['simulator']/e['trace']/'rows.json'
        if sha(path)!=e['rows_sha256']:raise ValueError('Frozen eligibility rows changed')
        faulty_rows[e['mutant'],e['simulator']+'/'+e['trace']]=load(path)
    transformed=[dict(mutant=e['mutant'],trace=e['simulator']+'/'+e['trace'],eligible=e['sampled_safety_eligible'],first_reference_failure=e['first_failure'],stratum=e['stratum']) for e in eligibility]
    rounds=[];total_cycles=0;replays=0;replay_seconds=0.0
    for s in sorted(snapshots,key=lambda s:(s['arm'],s['repetition'],s['round'])):
        d=out/'simulation'/s['arm']/f'rep{s["repetition"]}'/f'round{s["round"]}'
        tokens=measured_tokens(calls,s['arm'],s['repetition'],s['round'])
        if s['status']!='compiled':
            rounds.append(dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],status=s['status'],metrics=None,tokens=tokens))
            continue
        candidate=run_root/s['directory']/'compiled';correct=[];faulty={}
        for name,rows in correct_rows.items():
            r=replay(candidate,rows,d/'correct'/name,out/'row-cache');correct.append(r)
            total_cycles+=r['cycles'];replays+=1;replay_seconds+=r['execution']['seconds']
        for (mid,name),rows in faulty_rows.items():
            r=replay(candidate,rows,d/'faults'/mid/name,out/'row-cache');faulty[mid,name]=r
            total_cycles+=r['cycles'];replays+=1;replay_seconds+=r['execution']['seconds']
        metrics=strict_score(correct,faulty,transformed,tokens)
        strata={}
        for stratum in reg['strata_before_outcomes']:
            es=[e for e in transformed if e['stratum']==stratum]
            ms=strict_score(correct,faulty,es,tokens)
            strata[stratum]={k:v for k,v in ms.items() if k not in ('details',)}
            strata[stratum]['raw_mutant_denominator']=sum(f['stratum']==stratum for f in faults)
        result=dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],status=s['status'],metrics=metrics,strata=strata,tokens=tokens)
        rounds.append(result);dump(d/'metrics.json',result)
        dump(out/'round-scores.partial.json',rounds)
        print(f'scored {s["arm"]} rep{s["repetition"]} round{s["round"]}: sound={metrics["suite_sound_on_fixed_controls"]} kills={len(metrics["distinct_mutants_killed"])}/11',flush=True)
    finals=load(run_root/'final-candidates.json')['candidates'];selected=[]
    for f in finals:
        row=next((r for r in rounds if (r['arm'],r['repetition'],r['round'])==(f['arm'],f['repetition'],f['selected_round'])),None)
        selected.append(dict(selection=f,score=row))
    report=dict(mode=mode,not_new_model_evidence=mode!='live',reference_freeze_sha256=reg['reference']['freeze_sha256'],rounds=rounds,finals=selected,
                costs=dict(monitor_replays=replays,replayed_cycles=total_cycles,replay_seconds=replay_seconds,new_DUT_simulations=0),
                raw_mutants=12,observable_mutants=11,eligible_pairs=sum(e['eligible'] for e in transformed),formal=[])
    dump(out/'scores.json',report)
    if formal:
        from controller_reference_evaluate import module
        checker=module(TASK/'reference/frozen-v2/checker.py','frozen_controller_oracle')
        for f in finals:
            jobs=[];started=time.monotonic()
            if f['directory'] is None:
                report['formal'].append(dict(arm=f['arm'],repetition=f['repetition'],status='INVALID_CANDIDATE',jobs=[]));continue
            planned=[('correct',TASK/'public/rtl/axis_frame_length_adjust.v',slot,mode,10) for slot in range(6) for mode in ('bmc','prove','cover')]
            planned += [(m['id'],ROOT/m['source'],slot,'bmc',5) for m in faults for slot in range(6)]
            for name,source,slot,jobmode,timeout in planned:
                label=dict(source=name,slot=slot,mode=jobmode,depth=24,solver_cap_seconds=timeout)
                if 720-(time.monotonic()-started)<timeout+5:
                    jobs.append(dict(label,status='NOT_RUN_TOTAL_CAP'));continue
                job=out/'formal'/f['arm']/f'rep{f["repetition"]}'/name/f'P{slot}-{jobmode}'
                r=formal_job(run_root/f['directory'],source,job,slot,jobmode,timeout)
                label.update(status=r['status'],seconds=r['seconds'],directory=str(job.relative_to(out)))
                if r['status']=='FAIL' and jobmode=='bmc':label['witness']=witness_review(job,checker)
                if r['status']=='FAIL' and jobmode=='prove':label['classification']='Induction/prove failure retained; not a reachable DUT violation claim'
                jobs.append(label)
                print(f'formal {f["arm"]} rep{f["repetition"]} {name} P{slot}-{jobmode}: {r["status"]}',flush=True)
                dump(out/'formal-progress.json',dict(arm=f['arm'],repetition=f['repetition'],jobs=jobs))
            report['formal'].append(dict(arm=f['arm'],repetition=f['repetition'],jobs=jobs,wall_seconds=time.monotonic()-started,status_counts=dict(Counter(j['status'] for j in jobs))))
            dump(out/'scores.json',report)
    verify_release(run_root);verify_task(reg)
    dump(out/'scores.json',report)
    dump(out/'completion.json',dict(scores_sha256=sha(out/'scores.json'),release_sha256=sha(run_root/'release.json'),all36_verified_after_scoring=True,scorer_sha256=sha(Path(__file__))))
    print(json.dumps(dict(costs=report['costs'],formal=[dict(arm=r['arm'],repetition=r['repetition'],counts=r.get('status_counts',{})) for r in report['formal']]),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--formal',action='store_true');a=p.parse_args()
    execute(a.run.resolve(),a.output.resolve(),a.formal)
