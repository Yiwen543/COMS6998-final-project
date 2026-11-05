#!/usr/bin/env python3
"""Score frozen candidate artifacts on held-out inputs; never revise a candidate."""
import argparse
import csv
import json
import time
from pathlib import Path
from common import BASE,ROOT,dump,sha
from monitor import compile_monitor,build_replay,replay,run_formal
from score import score
from formal_witness import adjudicate

def verify_reference():
    path=BASE/'reference/frozen-v1/freeze.json'
    ref=json.loads(path.read_text())
    for name,h in ref['artifact_sha256'].items():
        if sha(ROOT/name)!=h:raise ValueError('Reference freeze changed: '+name)
    return ref

def verify_candidates(root):
    manifest=json.loads((root/'final-candidates.json').read_text())
    expected={(a,r) for a in ('B_prime','C_prime') for r in (1,2,3)}
    if {(r['arm'],r['repetition']) for r in manifest['candidates']}!=expected or len(manifest['candidates'])!=6:
        raise ValueError('All six candidates must freeze before final evaluation')
    for r in manifest['candidates']:
        if r['status']=='invalid':continue
        p=Path(r['candidate_dir']).resolve()
        if not p.is_relative_to(root.resolve()):raise ValueError('Candidate outside run')
        if sha(p/'candidate.sv')!=r['candidate_sha256'] or sha(p/'candidate.json')!=r['metadata_sha256']:
            raise ValueError('Final candidate was changed')
    return manifest

def evaluate(root,preflight,out,formal=False):
    started=time.perf_counter()
    manifest=verify_candidates(root);reference=verify_reference()
    # This check and release record happen BEFORE any hidden rows are loaded.
    out.mkdir(parents=True,exist_ok=False)
    dump(out/'release.json',{'final_candidates_sha256':sha(root/'final-candidates.json'),
        'reference_freeze_sha256':sha(BASE/'reference/frozen-v1/freeze.json'),
        'mode':manifest['mode'],'candidate_revision_allowed':False,'all_candidates_checked':True})
    if manifest['mode']=='live' and not formal:raise ValueError('Live final scoring requires the registered formal schedule')
    oracle=json.loads((BASE/'reference/evaluation-v3/evaluations.json').read_text())['cases']
    frozen_eligibility=json.loads((BASE/'reference/frozen-v1/fault-eligibility.json').read_text())
    calls=[json.loads(s) for s in (root/'calls.jsonl').read_text().splitlines()]
    reports=[];compiles=0;replays=0;cycles=0;formal_calls=0
    compile_seconds=0;replay_seconds=0;formal_seconds=0;reference_seconds=0
    for c in manifest['candidates']:
        d=out/c['arm']/f'rep{c["repetition"]}';d.mkdir(parents=True)
        records=[r for r in calls if r['arm']==c['arm'] and r['repetition']==c['repetition']]
        usages=[r.get('usage') for r in records if r.get('generation_request_issued')]
        known=[u for u in usages if u and u.get('input_tokens') is not None and u.get('output_tokens') is not None]
        known_tokens=sum(u['input_tokens']+u['output_tokens'] for u in known)
        unreported=sum(r.get('generation_request_issued') and (not r.get('usage') or r['usage'].get('input_tokens') is None or r['usage'].get('output_tokens') is None) for r in records)
        tokens=known_tokens if manifest['mode']=='live' and not unreported else None
        if c['status']=='invalid':
            reports.append({'arm':c['arm'],'repetition':c['repetition'],'status':'invalid_candidate',
                            'api_known_tokens':known_tokens,'unreported_generation_attempts':unreported,
                            'api_tokens':tokens,'valid_mutant_kills':0,'observable_mutant_recall':0,
                            'distinct_mutant_kills_per_1000_tokens':0 if tokens else None});continue
        candidate=json.loads((Path(c['candidate_dir'])/'candidate.json').read_text())
        compiles+=1
        info=compile_monitor(candidate,d/'compiled')
        compile_seconds+=info['seconds']
        if info['status']!='complete':raise RuntimeError('Frozen candidate no longer compiles')
        compiles+=1
        build=build_replay(d/'compiled');compile_seconds+=build['seconds']
        if build['status']!='complete':raise RuntimeError('Frozen replay compile failure')
        if sha(d/'compiled/candidate.sv')!=c['candidate_sha256']:raise ValueError('Candidate rendering changed')
        per_sim={}
        for sim in ('verilator','iverilog'):
            correct=[];faults={}
            for control in ('correct_stress','correct_original','M01','M02','M03','M04','M05','M06'):
                for case in ('final_boundary','final_wrap_reset','final_mixed'):
                    rows=json.loads((preflight/control/sim/case/'rows.json').read_text())
                    if control.startswith('correct') and oracle[f'{control}/{sim}/{case}']['verdict']!='PASS':
                        raise ValueError('Reference did not pass correct control')
                    r=replay(d/'compiled',rows,d/sim/control/case);replays+=1;cycles+=r['cycles']
                    replay_seconds+=r['execution']['seconds']
                    if control.startswith('correct'):correct.append(r)
                    else:faults[control,case]=r
            eligible=[]
            for e in frozen_eligibility:
                r=oracle[f'{e["mutant"]}/{sim}/{e["trace"]}']
                key='verilator_two_state' if sim=='verilator' else 'icarus_four_state_observations'
                status=e['eligible_by_simulator'][key]
                assert status==(r['verdict']=='FAIL' and bool(r['failures']))
                eligible.append({'mutant':e['mutant'],'trace':e['trace'],'eligible':status,
                                 'first_reference_failure':r['failures'][0] if r['failures'] else None})
            per_sim[sim]=score(correct,faults,eligible,tokens)
        formal_results=[]
        if formal:
            for label,source in [('correct_stress',BASE/'public/sfifo.v'),('correct_original',BASE/'private/original_noformal.v')]+[(f'M{i:02d}',BASE/'private/mutants'/f'M{i:02d}.v') for i in range(1,7)]:
                modes=('bmc','prove','cover') if label.startswith('correct') else ('bmc',)
                for mode in modes:
                    r=run_formal(d/'compiled',source,d/'formal'/label/mode,mode);formal_calls+=1
                    formal_seconds+=r['seconds']
                    witness=adjudicate(d/'formal'/label/mode,BASE/'reference/frozen-v1') if r['status']=='FAIL' and mode in ('bmc','prove') else None
                    if witness:reference_seconds+=witness.get('reference_seconds',0)
                    formal_results.append({'control':label,'mode':mode,'status':r['status'],'depth':r['depth'],'seconds':r['seconds'],
                        'witness_review':witness,
                        'classification':'candidate property counterexample relative to RTL; requires specification adjudication' if r['status']=='FAIL' else 'tool status only; do not infer unbounded proof from bmc'})
        result={'arm':c['arm'],'repetition':c['repetition'],'mode':manifest['mode'],
                'status':'evaluated','candidate_sha256':c['candidate_sha256'],
                'api_known_tokens':known_tokens,'unreported_generation_attempts':unreported,
                'simulation':per_sim,'formal':formal_results,'formal_skipped_mock_only':not formal}
        dump(d/'score.json',result);reports.append(result)
    dump(out/'scores.json',reports)
    with (out/'summary.csv').open('w',newline='') as f:
        fields=['arm','repetition','simulator','status','sound','eligible_pairs','eligible_mutants','killed_mutants','recall','api_tokens','roi']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for r in reports:
            if r['status']=='invalid_candidate':
                for sim,key in [('verilator','verilator_two_state'),('iverilog','icarus_four_state_observations')]:
                    eligible=[e for e in frozen_eligibility if e['eligible_by_simulator'][key]]
                    writer.writerow({'arm':r['arm'],'repetition':r['repetition'],'simulator':sim,'status':'invalid_candidate',
                        'sound':False,'eligible_pairs':len(eligible),'eligible_mutants':len({e['mutant'] for e in eligible}),
                        'killed_mutants':0,'recall':0,'api_tokens':r['api_tokens'],'roi':r['distinct_mutant_kills_per_1000_tokens']})
                continue
            for sim,s in r['simulation'].items():
                writer.writerow({'arm':r['arm'],'repetition':r['repetition'],'simulator':sim,'status':r['status'],
                    'sound':s['suite_sound_on_fixed_controls'],'eligible_pairs':s['eligible_mutant_trace_count'],
                    'eligible_mutants':len(s['eligible_mutants']),'killed_mutants':len(s['distinct_mutants_killed']),
                    'recall':s['observable_mutant_recall'],'api_tokens':s['api_input_plus_output_tokens'],
                    'roi':s['distinct_mutant_kills_per_1000_tokens']})
    summary={'mode':manifest['mode'],'compilation_tool_invocations':compiles,'monitor_replays':replays,
        'wall_seconds':time.perf_counter()-started,'compile_seconds':compile_seconds,
        'monitor_replay_seconds':replay_seconds,'formal_seconds':formal_seconds,'witness_reference_seconds':reference_seconds,
        'replayed_cycles':cycles,'formal_tasks':formal_calls,'new_dut_simulations':0,'model_calls':0,
        'not_a_model_effectiveness_result':manifest['mode']!='live'}
    dump(out/'summary.json',summary);return summary

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('run','preflight','output'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--formal',action='store_true');a=p.parse_args()
    print(json.dumps(evaluate(a.run.resolve(),a.preflight.resolve(),a.output.resolve(),a.formal),indent=2))
