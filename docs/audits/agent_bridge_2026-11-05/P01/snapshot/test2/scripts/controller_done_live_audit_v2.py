"""Post-release audit and descriptive tables; never calls a model or changes scores."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
from common import ROOT, BASE, dump, sha
from controller_done_generate_v2 import messages, verify_data, GEN_REG, LIVE_FREEZE, APPROVAL
from controller_done_model_v2 import fingerprint, RESERVE_PER_GENERATION
from controller_done_data import TASK, REG, SOURCES
from controller_done_grade_v4 import inventory
from controller_done_case_v4 import grade, summarize
from controller_monitor_live import ROW_INPUTS, OUTPUTS
from controller_release_live import verify_release, ARMS
from controller_done_formal_v3 import harness


def load(p): return json.loads(p.read_text())
def lines(p): return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def need(condition, message):
    if not condition: raise ValueError(message)
def key(r): return r['arm'], r['repetition'], r['round']
def without(r, omit): return {k:v for k,v in r.items() if k not in omit}


def audit(run, replay, scores, replay_scores, formal, out):
    verify_data(); out.mkdir(parents=True, exist_ok=False)
    snaps=verify_release(run); mirrors=verify_release(replay)
    need(len(snaps)==len(mirrors)==36, 'All36 rounds required')
    reg=load(REG); generation=load(GEN_REG); manifest=load(LIVE_FREEZE)
    old={}
    for n,h in reg['preserve_old_freezes'].items():
        p=ROOT/n; need(sha(p)==h, 'Parent manifest changed: '+n)
        members=load(p).get('files',load(p).get('artifact_sha256',{}))
        for name,digest in members.items(): need(sha(ROOT/name)==digest,'Parent member changed: '+name)
        old[n]=dict(sha256=h,members=len(members))
    for n,h in {'test2/results/controller-final-v1/scores.json':'f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651',
                'test2/results/live-final-v1/scores.json':'33003b33a7172d29704f85fa84da10bdbb30aebe78b72d400a4f97b73a2ef338'}.items():
        need(sha(ROOT/n)==h,'Old score changed')
    for n,h in manifest['files'].items(): need(sha(ROOT/n)==h,'Generation qualification changed: '+n)
    grant=load(APPROVAL); need(grant['freeze_sha256']==sha(LIVE_FREEZE),'Grant freeze mismatch')
    need(grant['registration_sha256']==sha(GEN_REG),'Grant registration mismatch')
    rr=load(run/'resource-release.json')
    for n,h in rr['files'].items(): need(sha(run/n)==h,'Resource release changed')
    need(rr['authorization_sha256']==sha(APPROVAL),'Resource grant mismatch')
    need(rr['generation_registration_sha256']==sha(GEN_REG),'Resource registration mismatch')
    calls=lines(run/'calls.jsonl'); events=lines(run/'api-dispatch.jsonl')
    need(not (replay/'api-dispatch.jsonl').exists(),'Replay must not dispatch API requests')
    counts=Counter(e['event'] for e in events)
    need(counts['generation_dispatched']==sum(bool(r['generation_request_issued']) for r in calls),'Generation dispatch accounting')
    need(counts['count_dispatched']==sum(bool(r['count_request_issued']) for r in calls),'Count dispatch accounting')
    need(counts['generation_dispatched']<=72 and counts['count_dispatched']<=72,'Dispatch cap')
    reserve=counts['generation_dispatched']*RESERVE_PER_GENERATION
    need(reserve<=17.5 and reserve+2.5<=20,'Monetary reserve cap')
    need(max(Counter(key(r) for r in calls).values())<=2,'Retry cap')
    bykey={key(s):s for s in snaps}; mirror={key(s):s for s in mirrors}
    accepted={key(c):c for c in calls if c.get('accepted_response')}
    for arm in ARMS:
        for rep in (1,2,3):
            previous=feedback=None
            for number in range(1,7):
                k=(arm,rep,number); d=run/bykey[k]['directory']; m=replay/mirror[k]['directory']
                need(load(d/'prompt.json')==messages(arm,number,previous,feedback),'Prompt allowlist/own history')
                for n in ('prompt.json','response.json','development-feedback.json'):
                    need(load(d/n)==load(m/n),'Saved-response replay mismatch: '+n)
                response=load(d/'response.json')
                if response is not None:
                    previous=response; need(k in accepted and accepted[k]['parsed']==response,'Response binding')
                feedback=load(d/'development-feedback.json')
    dispatch=[]; last_count=None
    for e in events:
        if e['event']=='count_returned':last_count=e
        if e['event']=='generation_dispatched':
            need(last_count is not None and e['messages_sha256']==last_count['messages_sha256'] and e['input_tokens_counted']==last_count['input_tokens'],'Generation count binding')
            need(0<e['input_tokens_counted']<=64000 and e['max_output_tokens']==8192,'Dispatched token cap')
            d=run/bykey[key(e['context'])]['directory']
            need(e['messages_sha256']==fingerprint(load(d/'prompt.json')),'Dispatch prompt binding')
            dispatch.append(e); last_count=None
    actual=[c for c in calls if c['generation_request_issued']]; known=[]
    for c in actual:
        u=c.get('usage')
        if not isinstance(u,dict):continue
        need(c['requested_model']==c['returned_model']=='gpt-6.1-sol','Returned model mismatch')
        need(c['returned_service_tier'] in (None,'default'),'Returned tier mismatch')
        need(u['input_tokens']==c['input_token_count']<=64000 and 0<=u['output_tokens']<=8192,'Actual token cap/count')
        need(u['total_tokens']==u['input_tokens']+u['output_tokens'],'Actual total tokens')
        for subset,total in [('cached_input_tokens','input_tokens'),('reasoning_output_tokens','output_tokens')]:
            need(u[subset] is None or 0<=u[subset]<=u[total],'Usage subset')
        known.append(c)
    usage={n:sum(c['usage'][n] for c in known) if all(c['usage'].get(n) is not None for c in known) else None for n in ('input_tokens','output_tokens','total_tokens','cached_input_tokens','reasoning_output_tokens')}
    estimate=0.; estimate_complete=True
    for c in known:
        u=c['usage']; details=c['raw_usage'].get('input_tokens_details') or {}
        cached=details.get('cached_tokens'); write=details.get('cache_write_tokens'); wd=details.get('cache_write_tokens_details') or {}
        need(not wd.get('ttl_12h_tokens'),'Unexpected12h cache writes')
        if cached is None or write is None:estimate_complete=False;continue
        need(0<=cached+write<=u['input_tokens'],'Cache subsets overlap/out of range')
        estimate+=((u['input_tokens']-cached-write)*2+write*2.5+cached*.1+u['output_tokens']*10)/1e6
    api=dict(dispatch_events=dict(counts),statuses=dict(Counter(c['status'] for c in calls)),generation_attempts=len(actual),
             unknown_generation_usage_attempts=len(actual)-len(known),known_usage_subtotal=usage,
             generation_token_rate_estimate_usd=estimate if estimate_complete and len(known)==len(actual) else None,
             estimate_is_not_invoice=True,count_endpoint_actual_usd=None,total_provider_invoice_usd=None,
             generation_conservative_reserve_usd=reserve,count_fee_reserve_usd=2.5,stage_authorized_ceiling_usd=20)
    a=load(scores/'scores.json'); b=load(replay_scores/'scores.json'); labels=inventory(load(TASK/'measurements-v1/summary.json')['records'])
    lookup={(r['source'],r['simulator'],r['trace']):r for r in labels}
    need(len(labels)==162 and len(lookup)==162,'Fixed unique evaluation inventory')
    need(a['release_sha256']==sha(run/'release.json') and b['release_sha256']==sha(replay/'release.json'),'Score release binding')
    need(len(a['rounds'])==len(b['rounds'])==36,'All-round scores')
    logs=cycles=path_differences=0; tables=[]
    for x,y in zip(a['rounds'],b['rounds']):
        need(without(x,('cases',))==without(y,('cases',)),'Round classification mismatch')
        need(len(x['cases'])==len(y['cases'])==162,'Fixed case inventory omitted')
        need(summarize(x['cases'])==without(x,('arm','repetition','round','candidate_status','cases')),'Summary differs from cases')
        for c,d in zip(x['cases'],y['cases']):
            need(without(c,('evidence_provenance','original_status'))==without(d,('evidence_provenance','original_status')),'Case classification mismatch')
            raw_pair=[]
            for case in (c,d):
                if 'evidence_provenance' not in case:continue
                p=ROOT/case['evidence_provenance']['result_path']; r=load(p); raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes())
                need(sha(p)==case['evidence_provenance']['result_sha256'],'Replay result changed')
                need(sha(p.parent/'replay.log.gz')==r['compressed_log_sha256'],'Replay gzip changed')
                label=lookup[case['source'],case['simulator'],case['trace']]; rows=(ROOT/label['directory']/'rows.json').read_bytes()
                need(grade(label,rows,r,raw)==without(case,('evidence_provenance','original_status')),'Raw replay reclassification mismatch')
                logs+=1;cycles+=r['cycles'];raw_pair.append(raw)
            if len(raw_pair)==2:
                path_differences+=int(raw_pair[0]!=raw_pair[1])
                need(raw_pair[0].replace(str(run).encode(),b'RUN_ROOT')==raw_pair[1].replace(str(replay).encode(),b'RUN_ROOT'),'Raw replay differs beyond known Icarus root diagnostic')
        cs=[c for c in calls if key(c)==key(x) and c['generation_request_issued']]; us=[c.get('usage') for c in cs]
        tokens=sum(u['total_tokens'] for u in us) if cs and all(isinstance(u,dict) for u in us) else None
        compile_path=run/bykey[key(x)]['directory']/'compiled/compile.json'
        compile_info=load(compile_path) if compile_path.exists() else {}
        row=dict(arm=x['arm'],repetition=x['repetition'],round=x['round'],candidate_status=x['candidate_status'],correct_gate=x['correct_control_gate'],
                 definite_types=len(x['union_definite_types_UNATTRIBUTED']),types=';'.join(x['union_definite_types_UNATTRIBUTED']),
                 correct_alarm_pairs=sum(bool(c['physical_reference_PASS_alarm_including_marker']) for c in x['cases'] if c['source']=='correct'),
                 correct_candidate_unknown_pairs=sum(bool(c['candidate_unknown_samples_including_marker']) for c in x['cases'] if c['source']=='correct'),
                 correct_unresolved_pairs=sum(c['is_unresolved'] for c in x['cases'] if c['source']=='correct'),
                 unresolved_pairs=x['unresolved_pairs'],candidate_unknown_pairs=x['candidate_unknown_pairs'],generation_attempts=len(cs),actual_tokens=tokens,
                 monitor_state_bits=compile_info.get('state_bits'),
                 vacuous_pairs=sum(c['vacuous'] is True for c in x['cases']))
        for category,v in x['categories'].items():
            for field in ('definite_pairs','fully_resolved_pairs','eligible_pairs'):row[category+'_'+field]=v[field]
        tables.append(row)
    vectors=set()
    for label in labels:
        if label['status']!='complete':continue
        rows=load(ROOT/label['directory']/'rows.json'); digest=fingerprint(rows)
        expected=''.join(' '.join('x' if v==-1 else f'{v:x}' for v in [r['cycle']]+[r['inputs'][n] for n in ROW_INPUTS]+[r[p][n] for p in ('pre','post') for n in OUTPUTS])+'\n' for r in rows)
        for root in (scores,replay_scores):
            if (root/'row-cache').exists():need((root/'row-cache'/(digest+'.hex')).read_text()==expected,'Actual physical replay vector mismatch')
        vectors.add(digest)
    f=load(formal/'summary.json'); need(len(f['jobs'])==540 and not f['finite_completion_proved'],'Fixed safety-only formal schedule')
    need(f['release_sha256']==sha(run/'release.json'),'Formal release binding')
    expected={(arm,rep,source,slot,mode) for arm in ARMS for rep in (1,2,3) for source in ['correct']+[r['id'] for r in reg['fault_catalogue']] for slot in range(6) for mode in (('bmc','prove','cover') if source=='correct' else ('bmc',))}
    actual_keys=[(j['arm'],j['repetition'],j['source'],j['slot'],j['mode']) for j in f['jobs']]
    need(len(set(actual_keys))==len(actual_keys) and set(actual_keys)==expected,'Formal fixed inventory/duplicates')
    selected=load(run/'final-candidates.json')['candidates'];formal_source_copies=0
    for j in f['jobs']:
        if j['status'] in ('INVALID_CANDIDATE','NOT_RUN_TOTAL_CAP'):continue
        folder=formal/j['arm']/f"rep{j['repetition']}"/j['source']/f"P{j['slot']}-{j['mode']}"
        native_result=load(folder/'result.json')
        need(all(j.get(k)==v for k,v in native_result.items()),'Formal summary/native result mismatch')
        need((folder/'harness.sv').read_text()==harness(j['slot']),'Formal harness drift')
        chosen=next(s for s in selected if s['arm']==j['arm'] and s['repetition']==j['repetition'])
        copy=folder/'work/src/candidate.sv'
        if copy.exists():need(sha(copy)==sha(run/chosen['directory']/'candidate.sv'),'Formal candidate source copy mismatch');formal_source_copies+=1
        else:need(j['status'] not in ('PASS','FAIL'),'Decisive formal result missing candidate copy')
        source=SOURCES[0] if j['source']=='correct' else ROOT/next(r for r in reg['fault_catalogue'] if r['id']==j['source'])['source']
        for name,original in [('dut.v',source)]+[(p.name,p) for p in SOURCES[1:]]:
            copy=folder/'work/src'/name
            if copy.exists():need(sha(copy)==sha(original),'Formal actual DUT/source copy mismatch: '+name)
            else:need(j['status'] not in ('PASS','FAIL'),'Decisive formal result missing DUT/source copy')
        if 'witness' in j:
            w=load(folder/'physical/result.json');need(w==j['witness'],'Formal witness summary drift')
            need(not w.get('reference_confirmed_selected_alarm') and not w.get('candidate_false_alarm_claim'),'Unjustified selected-alarm reference attribution')
    native=0
    for p in formal.rglob('result.json'):
        r=load(p)
        if r.get('scope')!='safety_projection':continue
        status=p.parent/'work/status'
        if status.exists():need(status.read_text().split()[0]==r['status'],'Native formal status changed')
        need("wire trace_done=1'b0" in (p.parent/'harness.sv').read_text(),'Formal marker projection changed')
        need(sha(p.parent/'sby.log')==r['log_sha256'],'Formal log changed'); native+=1
    need(native==sum(r['status'] not in ('INVALID_CANDIDATE','NOT_RUN_TOTAL_CAP') for r in f['jobs']),'Missing native formal jobs')
    per_arm={arm:dict(statuses=dict(Counter(j['status'] for j in f['jobs'] if j['arm']==arm)),
                     correct_statuses=dict(Counter(j['status'] for j in f['jobs'] if j['arm']==arm and j['source']=='correct')),
                     witness_statuses=dict(Counter(j['witness'].get('status','unspecified') for j in f['jobs'] if j['arm']==arm and 'witness' in j))) for arm in ARMS}
    formal_sessions=[]
    for arm in ARMS:
        for rep in (1,2,3):
            jobs=[j for j in f['jobs'] if j['arm']==arm and j['repetition']==rep]
            witnesses=[j for j in jobs if 'witness' in j]
            formal_sessions.append(dict(arm=arm,repetition=rep,statuses=dict(Counter(j['status'] for j in jobs)),
                statuses_by_source_mode={scope+'/'+mode:dict(Counter(j['status'] for j in jobs if (j['source']=='correct')==(scope=='correct') and j['mode']==mode)) for scope in ('correct','mutants') for mode in ('bmc','prove','cover')},
                earlier_physical_prefix_FAIL_mutant_types=sorted({j['source'] for j in witnesses if j['source']!='correct' and j['witness'].get('reference_verdict')=='FAIL' and j['witness'].get('physical_simulators_agree') and j['witness'].get('formal_alarm_reproduced')}),
                local_correct_prove_PASS_slots=[j['slot'] for j in jobs if j['source']=='correct' and j['mode']=='prove' and j['status']=='PASS'],
                witness_reference_verdicts=dict(Counter(j['witness'].get('reference_verdict','UNKNOWN') for j in witnesses)),
                witness_unknown_contexts=sum(bool(j['witness'].get('reference_unknown')) for j in witnesses),
                selected_alarm_reference_agreement='UNRESOLVED: oracle receives earlier prefix, not selected pre-sample/category'))
    for root in (run,replay):verify_release(root)
    sessions=[]; finals=load(run/'final-candidates.json')['candidates']
    for arm in ARMS:
        for rep in (1,2,3):
            selected=next(r for r in finals if r['arm']==arm and r['repetition']==rep)
            rs=[r for r in a['rounds'] if r['arm']==arm and r['repetition']==rep]
            cs=[c for c in actual if c['arm']==arm and c['repetition']==rep]
            tokens=sum(c['usage']['total_tokens'] for c in cs) if cs and all(isinstance(c.get('usage'),dict) for c in cs) else None
            target=next((r for r in rs if r['correct_control_gate'] and len(r['union_definite_types_UNATTRIBUTED'])==11),None)
            end=next((r for r in rs if r['round']==selected['selected_round']),None)
            prefix=[c for c in cs if target and c['round']<=target['round']]
            prefix_tokens=sum(c['usage']['total_tokens'] for c in prefix) if prefix and all(isinstance(c.get('usage'),dict) for c in prefix) else None
            sessions.append(dict(arm=arm,repetition=rep,selected_round=selected['selected_round'],final_status=selected['status'],
                                 generation_attempts=len(cs),actual_tokens=tokens,target_status='REACHED' if target else 'NOT_REACHED',
                                 first_target_round=target['round'] if target else None,tokens_to_target=prefix_tokens,
                                 tokens_until_censoring=tokens if target is None else None,
                                 endpoint_definite_types=end['union_definite_types_UNATTRIBUTED'] if end else None,
                                 endpoint_types_per_1000_API_tokens=len(end['union_definite_types_UNATTRIBUTED'])*1000/tokens if end and tokens else None,
                                 endpoint=end))
    arm_tokens={arm:sum(c['usage']['total_tokens'] for c in known if c['arm']==arm) for arm in ARMS}
    finite_input_diagnostic=[]
    for s in sessions:
        end=s['endpoint']
        if end is None:continue
        original=next(r for r in a['rounds'] if key(r)==key(end))
        eligible=[c for c in original['cases'] if c['eligible']['input_completion']]
        finite_input_diagnostic.append(dict(arm=s['arm'],repetition=s['repetition'],eligible=len(eligible),
            marker_alarm_pairs=sum(bool(c['marker_alarm']) for c in eligible),earlier_alarm_pairs=sum(bool(c['early_finite_alarm_samples']) for c in eligible),
            safety_overlap_pairs=sum(c['eligible']['safety'] for c in eligible),oracle_unknown_pairs=sum(bool(c['oracle_unknown_records']) for c in eligible),
            note='These cases cannot isolate input-completion skill: all eligible pairs may already have ordinary safety alarms. No retrospective scoring change.'))
    physical_executions=[]
    for log in formal.glob('**/physical/*/simulation.log'):
        p=log.parent/'execution.json';r=load(p) if p.exists() else {}
        physical_executions.append(dict(path=str(log.relative_to(ROOT)),log_sha256=sha(log),status=r.get('status','EXECUTION_METADATA_MISSING_UNKNOWN'),cycles=r.get('cycles'),seconds=r.get('seconds')))
    witness_replays=[]
    for p in formal.glob('**/physical/candidate-replay/result.json'):
        r=load(p);witness_replays.append(dict(path=str(p.relative_to(ROOT)),complete=r['complete'],cycles=r['cycles'],seconds=r['execution']['seconds']))
    physical_compile_logs=list((formal/'physical-cache').rglob('compile.json')) if (formal/'physical-cache').exists() else []
    native_development={}
    for name,root in [('live',run),('saved_response_replay',replay)]:
        yosys=list(root.glob('*/rep*/round*/compiled/compile.json')); ivl=list(root.glob('*/rep*/round*/compiled/iverilog.json'))
        costs=[load(p) for p in root.glob('*/rep*/round*/development-cost.json')]
        native_development[name]=dict(yosys_invocations=len(yosys),iverilog_invocations=len(ivl),
            native_compile_seconds=sum(load(p)['seconds'] for p in yosys+ivl),
            reported_compilation_attempts=sum(r['compilation_tool_invocations'] for r in costs),
            note='Runner increments compilation_tool_invocations before static validation. Use actual native compile records for tool invocations; preserve the original attempt counter.')
    qualification_failures=[]
    for s in snaps:
        if s['status']=='compiled':continue
        d=run/s['directory'];response=load(d/'response.json')
        qualification_failures.append(dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],status=s['status'],
            development_feedback=load(d/'development-feedback.json'),
            property_description_lengths=[len(p.get('description','')) for p in response.get('properties',[])] if isinstance(response,dict) else None))
    with (out/'rounds.csv').open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(tables[0]));w.writeheader();w.writerows(tables)
    evidence=[GEN_REG,LIVE_FREEZE,APPROVAL,REG,run/'release.json',run/'resource-release.json',replay/'release.json',scores/'scores.json',replay_scores/'scores.json',formal/'summary.json']
    result=dict(status='VERIFIED_WITH_UNRESOLVED_RETAINED',actual_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                API=api,old_freezes=old,qualification_members=len(manifest['files']),verified_raw_logs=logs,verified_replay_cycles=cycles,
                distinct_physical_vectors=len(vectors),known_Icarus_path_differences=path_differences,rounds=tables,
                endpoints=a['selected_endpoints'],formal_by_arm=per_arm,formal_costs=dict(jobs=len(f['jobs']),native_jobs=native,verified_candidate_source_copies=formal_source_copies,wall_seconds=f['wall_seconds'],elapsed_per_final=f['elapsed_per_final']),
                formal_sessions=formal_sessions,
                sessions=sessions,physical_witness_cost=dict(simulator_executions=len(physical_executions),executions=physical_executions,
                    known_cycles=sum(r['cycles'] for r in physical_executions if type(r['cycles'])==int),unknown_cycle_executions=sum(type(r['cycles'])!=int for r in physical_executions),compile_invocations=len(physical_compile_logs),
                    candidate_replays=len(witness_replays),candidate_replay_cycles=sum(r['cycles'] for r in witness_replays),candidate_replay_records=witness_replays),
                native_development_cost=native_development,
                qualification_failures=qualification_failures,
                arm_token_totals=arm_tokens,C_over_B_actual_tokens_percent=(arm_tokens[ARMS[1]]/arm_tokens[ARMS[0]]-1)*100 if arm_tokens[ARMS[0]] and len(known)==len(actual) else None,
                input_completion_diagnostic=finite_input_diagnostic,
                live_development_cost=load(run/'summary.json'),saved_response_replay_cost=load(replay/'summary.json'),fresh_score_cost=a['costs'],replay_score_cost=b['costs'],
                actual_count_fees_unknown=True,finite_completion_proved=False,comparison='Whole B/C feedback package; no token-matched placebo, small n, same inspected IP',
                evidence_sha256={str(p.relative_to(ROOT)):sha(p) for p in evidence},producer_sha256=sha(__file__))
    dump(out/'audit.json',result);return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('run','replay','scores','replay-scores','formal','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=audit(a.run.resolve(),a.replay.resolve(),a.scores.resolve(),a.replay_scores.resolve(),a.formal.resolve(),a.output.resolve())
    print(r['status'], 'rawlogs',r['verified_raw_logs'],'formal',r['formal_costs']['jobs'])
