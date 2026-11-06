"""Independent P19 saved HTTP/journal/prompt/release/log/score analysis only."""
from pathlib import Path
from collections import Counter,defaultdict
import ast,gzip,hashlib,json,re,subprocess
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3];A=ROOT/'docs/audits/producer_test2_bc_retest_E01_2026-11-06';R=ROOT/'test2/results/controller-done-bc-retest-v3';C=ROOT/'test2/results/controller-done-bc-retest-v3-supervision'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':')).encode()
fingerprint=lambda v:hashlib.sha256(canon(v)).hexdigest()
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
assert sha(A/'phase.json')=='60b31b2a07b8dffe8d6be1ecda97fefff1dafa02650716a7e56c1fda71946a3d'
assert sha(A/'snapshot-manifest.json')=='e518db3d81c0316b14e482b9f8d03aca02e4e228528d8de34d33feee6de470a5'
manifest=read(A/'snapshot-manifest.json')['files']
for n,h in manifest.items():assert '/build/private/' not in '/'+n and sha(ROOT/n)==h,n
reg=read(ROOT/'test2/configs/controller_done_bc_retest_v3.json');sources=read(ROOT/reg['source_manifest'])['files']
for n,h in sources.items():assert sha(ROOT/n)==h,n
anchors={'ledger.json':'afde54da71e13a988ccc7c8de36f7f180f841b67d048fd2a4074e9dcb35660ac','summary.json':'8cf6c221a572c3ea6cf2fd0ec4714102404a88723ec86727a222166b707f453d','release.json':'52b7b7c3a9b2eeac57d52284b1221b316ee13b40de28409c94928bf2d1520c44','calls.jsonl':'ce5a53715363042a88d8ac29d5b326fafd147fcad947a0841d868928315d913d','grade/scores.json':'3019f89eebbf298bfddcdfb6e54a69484776487e0987f9fbed0a4aa3d52932a6'}
for n,h in anchors.items():assert sha(R/n)==h,n
for row in read(A/'bindings.json').values():assert sha(ROOT/row['path'])==row['sha256']
ledger=read(R/'ledger.json');calls=[json.loads(x) for x in (R/'calls.jsonl').read_text().splitlines()];run=read(R/'run.json');lease=read(C/'worker-lease.json');parent=read(C/'parent-receipt.json');scores=read(R/'grade/scores.json')
assert ledger['completed'] and not ledger['halted'] and len(calls)==len(ledger['events'])==6
assert ledger['counts_reserved']==0 and ledger['generations_reserved']==ledger['api_dispatch_attempts']==ledger['api_provider_confirmed_requests']==6
assert ledger['start_monotonic']==lease['start'] and ledger['work_deadline']==lease['start']+3590 and ledger['hard_deadline']==lease['start']+3600
assert parent['returncode']==0 and not parent['deadline_forced_stop'] and parent['mandatory_errors']==[] and parent['within_total_wall'] and parent['elapsed_seconds']<3600
assert parent['child_inventory_complete'] is False
bindings=read(A/'bindings.json');assert lease['execute_sha256']==bindings['EXECUTE']['sha256']=='d76cc02a53361929e6f1595fa17a1a6ccffd5991da641e8343f57a9cd97cc1f8'
review=read(ROOT/bindings['review']['path']);execute=read(ROOT/bindings['EXECUTE']['path']);assert execute['review_sha256']==bindings['review']['sha256']=='11794461f16a1c77bd395f2d2cf4dc29b900cc6cd2468ea9fac904707bc498ca' and review['status']=='PASS_WITH_LIMITS'
for k,v in review['input_identity'].items():
    if k!='producer_manifest_sha256':assert execute[k]==v,k
released=read(R/'release.json');assert released['all_rounds_frozen'] and not released['candidate_revision_allowed']
for n,h in released['files'].items():assert sha(R/n)==h,n
snaps=[]
for row in read(R/'all-round-candidates.json')['rounds']:
    assert sha(R/row['snapshot'])==row['sha256'];snap=read(R/row['snapshot']);assert snap['mode']=='live' and snap['status']=='compiled'
    for n,h in snap['files'].items():assert sha(R/n)==h,n
    snaps.append(snap)
assert len(snaps)==6 and {(x['arm'],x['round']) for x in snaps}==set(map(tuple,reg['schedule'])) and len(set(run['session_ids'].values()))==2
for arm in run['session_ids']:assert {x['session_id'] for x in snaps if x['arm']==arm}=={run['session_ids'][arm]}
finals=read(R/'final-candidates.json')['candidates'];assert len(finals)==2 and all(x['selected_round']==3 for x in finals)
def literal(path,name):
    node=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets));return ast.literal_eval(node.value)
system=literal(ROOT/'test2/scripts/controller_done_generate_v2.py','SYSTEM');pins=literal(ROOT/'test2/scripts/controller_monitor_live.py','PINS');schema=literal(ROOT/'test2/scripts/monitor.py','SCHEMA')
header='module candidate_monitor(\n'+',\n'.join('input wire '+(f'[{w-1}:0] ' if w>1 else '')+n for n,w in pins.items())+',\noutput wire [5:0] active,ok);\n';header=header.replace('output wire [5:0] active,ok);','input wire trace_done,\noutput wire [5:0] active,ok);')
history={arm:None for arm in run['session_ids']};feedback={arm:None for arm in run['session_ids']};usage_by_arm=defaultdict(Counter);cost_by_arm=Counter();http_records=[]
for index,((arm,number),call,event) in enumerate(zip(reg['schedule'],calls,ledger['events'])):
    assert call['arm']==event['context']['arm']==arm and call['round']==event['context']['round']==number and call['attempt']==1 and call['accepted_response'] and call['mode']=='live'
    f=R/arm/'rep1'/f'round{number}';prompt=read(f/'prompt.json');packet=read(ROOT/f'test2/tasks/axis_length_done_v1/public/prompt-packets-v2/{arm}.json');packet.update(module_header=header,round=number,previous_candidate=history[arm],development_feedback=feedback[arm])
    assert prompt==[{'role':'system','content':system},{'role':'user','content':canon(packet).decode()}]
    assert sha(f/'prompt.json')==call['prompt_sha256'] and fingerprint(prompt)==event['context']['messages_sha256']
    request=read(f/'attempt1/generation/request.json');result=read(f/'attempt1/generation/result.json');raw=result['provider_response'];u=result['usage']
    assert request['kind']=='generation' and request['messages']==prompt and request['schema']==schema and fingerprint(schema)==event['context']['schema_sha256']
    assert request['reservation_index']==index and request['stage_pgid']==request['parent_worker_pid'] and request['stage_start']==lease['start'] and request['deadline_monotonic']==ledger['work_deadline']
    assert sha(Path(request['lease_path']))==request['lease_sha256'] and Path(request['ledger_path'])==R/'ledger.json'
    payload={'model':'gpt-6.1-sol','input':prompt,'reasoning':{'effort':'low'},'text':{'format':{'type':'json_schema','name':'controller_done_monitor','strict':True,'schema':schema}},'store':False,'max_output_tokens':8192,'service_tier':'default','prompt_cache_options':{'mode':'implicit','ttl':'30m'}}
    blob=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();payload_h=hashlib.sha256(blob).hexdigest();est=request['input_estimate']
    assert payload_h==request['payload_sha256']==event['context']['payload_sha256']==est['payload_sha256']
    assert est['kind']=='ESTIMATE' and est['not_exact_token_count'] and est['not_server_input_hardcap'] and est['value']==(len(blob)*2+4)//5+4096<=64000
    assert result['HTTP_status']==200 and raw['status']==result['provider_status']=='completed' and raw['model']==result['returned_model']=='gpt-6.1-sol' and raw['service_tier']==result['returned_service_tier']=='default'
    assert not result['long_cache_write'] and not result['unexpected_output_type'] and result['request_issued'] is True and result['remote_count_requests']==0
    assert all(type(u[k]) is int and u[k]>=0 and raw['usage'][k]==u[k] for k in ['input_tokens','output_tokens','total_tokens'])
    assert 0<u['input_tokens']<=64000 and u['output_tokens']<=8192 and u['input_tokens']+u['output_tokens']==u['total_tokens']
    for field,detail,total in [('cached_input_tokens',raw['usage']['input_tokens_details'].get('cached_tokens'),'input_tokens'),('reasoning_output_tokens',raw['usage']['output_tokens_details'].get('reasoning_tokens'),'output_tokens')]:assert detail==u[field] and type(detail) is int and 0<=detail<=u[total]
    text=''.join(c['text'] for item in raw['output'] if item['type']=='message' for c in item['content'] if c['type']=='output_text');assert text==call['output_text']==result['output_text']
    parsed=json.loads(text);assert parsed==call['parsed']==read(f/'response.json')==read(f/'compiled/candidate.json')
    assert call['usage']==u==event['usage'] and call['provider_response']==raw==event['result']['provider_response']
    assert not call['count_request_issued'] and call['generation_request_issued'] and not event['simulated'] and event['kind']=='generation'
    upper=(55*u['input_tokens']+165*u['output_tokens']+9)//10;assert upper==event['settled_upper_micro_usd']==event['commitment_micro_usd'] and event['unused_reservation_released_micro_usd']==5910168-upper
    assert event['actual_cost_usd'] is None and event['reserved_micro_usd']==5910168
    history[arm]=parsed;feedback[arm]=read(f/'development-feedback.json');assert feedback[arm]['status']=='compiled'
    usage_by_arm[arm].update(u);cost_by_arm[arm]+=upper
    http_records.append({'arm':arm,'round':number,'response_id':raw['id'],'usage':u,'ESTIMATE':est['value'],'settled_upper_microUSD':upper,'raw_response_result_sha256':sha(f/'attempt1/generation/result.json')})
committed=0;peak=0;settled={};open_reserves={};gross=0;released_total=0;journal_steps=[]
for e in ledger['journal']:
    idx=e['index']
    if e['op']=='RESERVE':assert idx not in open_reserves and idx not in settled and e['micro_usd']==5910168;open_reserves[idx]=5910168;committed+=5910168;gross+=5910168
    else:
        assert e['op']=='SETTLE_UPPER_AND_RELEASE_UNUSED' and open_reserves.pop(idx)==5910168 and e['settled_upper_micro_usd']==ledger['events'][idx]['settled_upper_micro_usd'];settled[idx]=e['settled_upper_micro_usd'];released_total+=e['unused_reservation_released_micro_usd'];committed-=e['unused_reservation_released_micro_usd']
    assert committed==sum(settled.values())+sum(open_reserves.values()) and committed<=20000000
    peak=max(peak,committed);journal_steps.append({'op':e['op'],'index':idx,'commitment_microUSD':committed})
assert committed==ledger['financial_commitment_micro_usd']==ledger['settled_upper_micro_usd']==1569371 and not open_reserves and ledger['unresolved_reservations_micro_usd']==0
assert gross==ledger['total_reservations_micro_usd']==35461008 and released_total==ledger['unused_reservation_released_micro_usd']==33891637 and ledger['actual_invoice_usd'] is None and peak==7207377

# Independent MON parser and registered case-rule calculation;no grader import.
labels=read(ROOT/'test2/tasks/axis_length_done_v1/measurements-v1/summary.json')['records'];labelmap={(x['source'],x['simulator'],x['trace']):x for x in labels};assert len(labelmap)==162
round_summaries=[];grade_cycles=0;raw_files=0
for round in scores['rounds']:
    arm,n=round['arm'],round['round'];assert len(round['cases'])==162 and {(x['source'],x['simulator'],x['trace']) for x in round['cases']}==set(labelmap)
    types=defaultdict(set);pairs=Counter();resolved=Counter();correct=0;unknownpairs=0;candidateunknown=0;markeronly=0
    for case in round['cases']:
        key=case['source'],case['simulator'],case['trace'];label=labelmap[key];assert label['status']=='complete'
        p=ROOT/case['evidence_provenance']['result_path'];assert sha(p)==case['evidence_provenance']['result_sha256'];res=read(p);gz=p.parent/'replay.log.gz';assert sha(gz)==res['compressed_log_sha256'];raw=gzip.decompress(gz.read_bytes());assert hashlib.sha256(raw).hexdigest()==res['raw_log_sha256']
        rows_blob=(ROOT/label['directory']/'rows.json').read_bytes();assert hashlib.sha256(rows_blob).hexdigest()==label['rows_sha256'];rows=json.loads(rows_blob);cycles=len(rows);assert res['rows_sha256']==fingerprint(rows) and cycles==label['cycles']==res['attempted_cycles']==res['cycles']
        samples=[]
        for line in raw.decode().splitlines():
            if not line.startswith('MON '):continue
            w=line.split();assert len(w)==5 and w[2] in ['pre','post'] and re.fullmatch('[01xz]{6}',w[3]) and re.fullmatch('[01xz]{6}',w[4]);samples.append((int(w[1]),w[2],w[3],w[4]))
        assert [(x[0],x[1]) for x in samples]==[(i,phase) for i in range(cycles) for phase in ['pre','post'] if i or phase=='post']
        assert b'REPLAY_COMPLETE' in raw and res['complete'] and res['samples']==len(samples) and res['trace_done_sample']==[cycles-1,'post'] and not res['safety_projection']
        alarms=set();unknown=set()
        for slot,prop in enumerate(res['properties']):
            failures=[];unk=[];checks=0;end_checks=0
            for cycle,phase,active,ok in samples:
                a,k=active[5-slot],ok[5-slot]
                if a not in '01' or (a=='1' and k not in '01'):unk.append([cycle,phase])
                elif a=='1':
                    checks+=1;end_checks+=int((cycle,phase)==(cycles-1,'post'))
                    if k=='0':failures.append([cycle,phase])
            assert prop['id']==f'P{slot}' and prop['checks']==checks and prop['failures']==failures and prop['unknown']==unk and prop['end_sample_checks']==end_checks
            alarms.update(map(tuple,failures));unknown.update(map(tuple,unk))
        end=(cycles-1,'post');ordinary=alarms-{end};onset=label.get('first_safety_failure');pos=lambda p:(p[0],0 if p[1]=='pre' else 1)
        eligible={'safety':bool(onset),'response_completion':bool(label.get('end_only') and label.get('response_completion')),'input_completion':bool(label.get('input_completion'))}
        early_safety=[x for x in alarms if onset and pos(x)<pos((onset['cycle'],onset['phase']))]
        det={'safety':bool(onset and not early_safety and any(pos(x)>=pos((onset['cycle'],onset['phase'])) for x in ordinary)),'response_completion':bool(eligible['response_completion'] and end in alarms and not ordinary),'input_completion':bool(eligible['input_completion'] and end in alarms and not ordinary)}
        unresolved=bool(unknown) or bool(label['unknown_records']) or label['verdict'] not in ['PASS','FAIL']
        assert case['eligible']==eligible and case['definite_detection']==det and case['fully_resolved_detection']=={k:bool(v and not unresolved) for k,v in det.items()}
        assert case['is_unresolved']==unresolved and case['oracle_unknown_records']==label['unknown_records'] and case['oracle_verdict']==label['verdict']
        assert case['candidate_unknown_samples_including_marker']==len(unknown) and case['alarm_samples_including_marker']==len(alarms)
        if key[0]=='correct':assert label['verdict']=='PASS' and not unresolved and not alarms;correct+=1
        else:
            for k in eligible:
                if eligible[k]:pairs[k]+=1
                if det[k]:types[k].add(key[0]);pairs[k+'_detected']+=1;resolved[k]+=int(not unresolved)
        markeronly+=int(bool(onset and end in alarms and not ordinary));unknownpairs+=int(bool(label['unknown_records']));candidateunknown+=int(bool(unknown));grade_cycles+=cycles;raw_files+=1
    assert correct==18 and round['correct_control_gate'] and unknownpairs==round['oracle_unknown_pairs']==38 and candidateunknown==round['candidate_unknown_pairs']==0 and markeronly==round['marker_only_safety_signal_pairs']==0
    for k in types:
        saved=round['categories'][k];assert sorted(types[k])==saved['definite_types'] and pairs[k]==saved['eligible_pairs'] and pairs[k+'_detected']==saved['definite_pairs'] and resolved[k]==saved['fully_resolved_pairs']
    union=sorted(set().union(*types.values()));assert union==round['union_definite_types_UNATTRIBUTED'] and len(union)==11 and 'N10' not in union
    assert all(x['verdict']=='PASS' and not any([x.get('first_safety_failure'),x.get('input_completion'),x.get('response_completion') and x.get('end_only')]) for x in labels if x['source']=='N10')
    round_summaries.append({'arm':arm,'round':n,'correct_controls':correct,'inventory':162,'raw_fault_pairs':144,'raw_fault_types':12,'oracle_unknown_pairs':38,'candidate_unknown_pairs':0,'union_definite_types_UNATTRIBUTED':union,'categories':round['categories'],'marker_only_safety_pairs':markeronly})
assert raw_files==972 and grade_cycles==203064
processcounts=Counter();devcycles=0;timings=[]
for p in R.rglob('*.process.json'):
    x=read(p);assert x['returncode']==0 and x['status']=='complete' and x['stage_pgid_inherited'] is True
    name=Path(x['argv'][0]).name;kind='API' if x['argv'][2].endswith('/api.py') else ('replay' if name=='vvp' else 'compile')
    assert name in ['yosys','iverilog','vvp','python3'];processcounts[kind]+=1
    cap={'API':120,'compile':60,'replay':15}[kind];assert x['seconds']<=cap and x['absolute_deadline']<=ledger['work_deadline'] and x['absolute_deadline']-cap>=ledger['start_monotonic']-0.001
    log=p.with_name(p.name.removesuffix('.process.json'))
    if log.exists():assert sha(log)==x['log_sha256']
    else:
        raw=gzip.decompress(log.with_suffix(log.suffix+'.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()==x['log_sha256']
    timings.append({'path':str(p.relative_to(R)),'kind':kind,'seconds':x['seconds'],'deadline':x['absolute_deadline']})
assert processcounts==Counter(API=6,compile=12,replay=990)
for arm,n in reg['schedule']:
    for p in (R/arm/'rep1'/f'round{n}').glob('*/result.json'):
        res=read(p)
        if 'attempted_cycles' in res:devcycles+=res['attempted_cycles'];assert res['complete']
assert devcycles==1380 and grade_cycles+devcycles==ledger['monitor_cycles']==204444 and ledger['monitor_replays']==990 and ledger['compile_calls']==12
assert max((R/snap['directory']/'snapshot.json').stat().st_mtime for snap in snaps)<=(R/'release.json').stat().st_mtime<min(p.stat().st_mtime for p in (R/'grade').rglob('*.process.json'))
for n,h in manifest.items():assert sha(ROOT/n)==h,n
for n,h in sources.items():assert sha(ROOT/n)==h,n
index=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest();assert index=='9f59799646fc88a655125b45990361109a5754ff0f5253882dca56761a5df313'
write(OWN/'journal-recalculation.json',{'steps':journal_steps,'peak_committed_microUSD':peak,'settled_upper_microUSD':committed,'gross_reservation_flow_microUSD':gross,'unused_released_microUSD':released_total,'unresolved_microUSD':0,'invoice':None,'not_invoice_or_refund':True})
write(OWN/'independent-analysis.json',{'status':'SAVED_EVIDENCE_CHECKS_PASS','snapshot_members':len(manifest),'source_dependencies':len(sources),'actual_generation_requests':6,'actual_remote_counts':0,'retry':0,'http_calls':http_records,'usage_by_arm':dict(usage_by_arm),'upper_cost_by_arm_microUSD':dict(cost_by_arm),'rounds':round_summaries,'saved_monitor_logs_independently_parsed':raw_files,'grade_cycles':grade_cycles,'development_cycles':devcycles,'process_counts':dict(processcounts),'timings':timings,'parent_elapsed_seconds_including_cleanup':parent['elapsed_seconds'],'worker_summary_elapsed_seconds':read(R/'summary.json')['global_elapsed_seconds'],'candidate_freeze_before_grade_code_and_mtime_consistent':True,'peak_committed_microUSD':peak,'index_sha256':index,'real_new_API_key_compile_sim_native_process':0,'method':'Standalone Python AST/JSON/Fraction-compatible integer/log/gzip parsing;no producer scoring or runtime imported/executed.'})
print(json.dumps({'status':'PASS','generation':6,'counts':0,'logs':raw_files,'settled_upper_microUSD':committed,'peak_microUSD':peak,'usage_by_arm':dict(usage_by_arm),'processes':dict(processcounts)}))
