"""Independent P09 probes: disk fixtures copied before mutation; no producer builders."""
from pathlib import Path
import json,hashlib,copy,shutil,importlib.util,sys
P=Path(__file__).resolve().parent
SRC=P/'exec_tree/test2/g0_v1/adapter.py'
s=importlib.util.spec_from_file_location('p09_adapter',SRC);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
OUT=P/'independent-probes'
BASE=P/'fresh-suite/test_01_baseline/bundle'
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(r,n):return json.loads((r/n).read_text())
def put(r,n,v):(r/n).write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n')
def edit(r,n,fn):
    v=get(r,n);fn(v);put(r,n,v)
def seal(r):
    m=get(r,'manifest.json')
    for a in m['artifacts']:a['sha256']=H(r/a['path'])
    put(r,'manifest.json',m)
    rel=get(r,'release.json');rel['manifest_sha256']=H(r/'manifest.json');rel['files']=[{'path':a['path'],'sha256':a['sha256']} for a in m['artifacts']]+[{'path':'manifest.json','sha256':H(r/'manifest.json')}];put(r,'release.json',rel)
def two(r,scope='session'):
    aa=get(r,'attempts.json');ee=get(r,'events.json');cc=get(r,'calls.json');m=get(r,'manifest.json')
    a=copy.deepcopy(aa['attempts'][0]);a.update(attempt_id='review-attempt-2',context_id='review-context-2',context_artifact_id='review-context-2',accepted_response_artifact_id='review-response-2')
    if scope=='session':a.update(arm_id='C',session_id='review-session-2')
    elif scope=='round':a.update(round_index=2)
    else:a.update(attempt_index=2)
    ctx=copy.deepcopy(get(r,'context-1.json'))
    for k in ['context_id','arm_id','session_id','round_index','attempt_index']:ctx[k]=a[k]
    put(r,'review-context-2.json',ctx);a['context_sha256']=H(r/'review-context-2.json');aa['attempts'].append(a)
    resp=copy.deepcopy(get(r,'response-1.json'));resp['response_id']='review-response-id-2';put(r,'review-response-2.json',resp)
    for aid,role in [('review-context-2','context'),('review-response-2','response')]:m['artifacts'].append({'artifact_id':aid,'path':aid+'.json','sha256':H(r/(aid+'.json')),'kind':'JSON','role':role,'visibility':'MAINTAINER'})
    second=[]
    for i,e in enumerate(copy.deepcopy(ee['events'])):
        e.update(event_id='review-event-'+str(i),attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],request_id='review-count-2' if i<2 else 'review-generation-2')
        if i==2:e['payload'].update(parent_count_request_id='review-count-2',cumulative_reserve_units=20)
        if i==3:e['payload'].update(response_id='review-response-id-2',response_artifact_id='review-response-2')
        second.append(e)
    c=copy.deepcopy(cc['calls'][0]);c.update(call_id='review-call-2',attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],count_request_id='review-count-2',generation_request_id='review-generation-2',count_terminal_event_id='review-event-1',generation_terminal_event_id='review-event-3',response_id='review-response-id-2',response_artifact_id='review-response-2')
    cc['calls'].append(c);ee['events']+=second
    for i,e in enumerate(ee['events']):e['event_sequence']=i
    for n,v in [('manifest.json',m),('attempts.json',aa),('events.json',ee),('calls.json',cc)]:put(r,n,v)
def first_failure(r,kind='generation',missing=False):
    aa=get(r,'attempts.json');aa['attempts'][0]['accepted_response_artifact_id']=None;put(r,'attempts.json',aa)
    cc=get(r,'calls.json');c=cc['calls'][0]
    c.update(status='TRANSPORT_ERROR',status_reason='Independent synthetic transport failure',accepted_response=False,response_id=None,response_artifact_id=None,returned_model=None,returned_tier=None,usage=None,raw_usage_artifact_id=None)
    ee=get(r,'events.json');first=ee['events'][:4];rest=ee['events'][4:]
    if kind=='count':
        c.update(generation_request_issued=False,generation_request_id=None,generation_terminal_event_id=None,input_token_count=None)
        first=first[:1] if missing else first[:2]
        if missing:c['count_terminal_event_id']=None
        else:first[1].update(event_type='count_error',payload={'error_type':'ReviewSyntheticError'})
        for e in rest:
            if e['event_type']=='generation_dispatched':e['payload']['cumulative_reserve_units']=10
    else:
        if missing:first=first[:3];c['generation_terminal_event_id']=None
        else:first[3].update(event_type='generation_error',payload={'error_type':'ReviewSyntheticError','usage_status':'UNKNOWN_NOT_ZERO'})
    ee['events']=first+rest
    for i,e in enumerate(ee['events']):e['event_sequence']=i
    put(r,'events.json',ee);put(r,'calls.json',cc)
def late_halt(r,accept=False):
    ee=get(r,'events.json');event=copy.deepcopy(ee['events'][2]);event.update(event_id='review-halt',event_type='resource_halt',request_id=None,payload={'reason':'Independent synthetic halt before return'});ee['events'].insert(3,event)
    for i,e in enumerate(ee['events']):e['event_sequence']=i
    put(r,'events.json',ee)
    if not accept:
        edit(r,'calls.json',lambda d:d['calls'][0].update(status='REJECTED_RESPONSE',status_reason='Late after halt;no candidate credit',accepted_response=False))
        edit(r,'attempts.json',lambda d:d['attempts'][0].update(accepted_response_artifact_id=None))
def unknown_usage(r):
    edit(r,'calls.json',lambda d:d['calls'][0].update(status='REJECTED_RESPONSE',status_reason='Missing usage declaration',accepted_response=False,usage=None,raw_usage_artifact_id=None))
    edit(r,'events.json',lambda d:d['events'][3]['payload'].update(usage=None,raw_usage_artifact_id=None))
    edit(r,'attempts.json',lambda d:d['attempts'][0].update(accepted_response_artifact_id=None))
CASES=[]
def case(name,expected,fn=None,base=BASE,expect_reason=None,check=None,reseal=True):
    root=OUT/name;root.mkdir();bundle=root/'bundle';shutil.copytree(base,bundle,symlinks=True)
    if fn:fn(bundle)
    if reseal:seal(bundle)
    before={str(f.relative_to(bundle)):H(f) for f in bundle.rglob('*') if f.is_file() and not f.is_symlink()}
    result=g.validate_bundle(bundle)
    after={str(f.relative_to(bundle)):H(f) for f in bundle.rglob('*') if f.is_file() and not f.is_symlink()};assert before==after
    put(root,'result.json',result)
    record={'case':name,'expected':expected,'actual':result['integrity']['status'],'expected_reason':expect_reason,'source_sha256':H(SRC),'schema_sha256':H(SRC.with_name('schema.json')),'input_sha256':copy.deepcopy(before),'result_sha256':H(root/'result.json')}
    put(root,'fixture-binding.json',record);record['fixture_binding_sha256']=H(root/'fixture-binding.json')
    record['expectation_met']=record['actual']==expected and (not expect_reason or any(expect_reason in str(x) for x in result['integrity']['reasons']))
    if check:record['extra_check']=check(result)
    CASES.append(record);print(name,record['actual'],result['integrity']['reasons'])
def run():
    OUT.mkdir(exist_ok=False)
    case('baseline','PASS_WITH_SCOPE')
    for scope in ['retry','round','session']:
        for kind in ['count','generation']:
            for missing in [True,False]:
                name=scope+'-'+kind+('-missing-next-dispatch' if missing else '-error-valid-next')
                def mutate(r,s=scope,k=kind,m=missing):two(r,s);first_failure(r,k,m)
                case(name,'REJECT' if missing else 'UNRESOLVED',mutate,expect_reason='REQUEST_AFTER_MISSING_TERMINAL' if missing else None,check=(lambda x:x['cost_knownness']['tokens']['value'] is None and all(v is None for v in x['cost_knownness']['tokens']['subsets'].values())) if not missing and kind=='generation' else None)
    case('late-usage-after-halt','UNRESOLVED',late_halt,check=lambda x:x['ledger']['halted'] and not x['ledger']['attempts'][0]['accepted_response'] and x['ledger']['attempts'][0]['actual_tokens']==12)
    case('late-return-cannot-be-accepted','REJECT',lambda r:late_halt(r,True),expect_reason='ACCEPTED_WITH_HALT')
    case('halted-next-session','REJECT',lambda r:(two(r),late_halt(r)),expect_reason='REQUEST_FLAGS_AFTER_GLOBAL_HALT')
    case('missing-usage-subsets-null','UNRESOLVED',unknown_usage,check=lambda x:x['cost_knownness']['tokens']['value'] is None and all(v is None for v in x['cost_knownness']['tokens']['subsets'].values()))
    def correlated_bool(r):
        for n in ['usage-1.json','events.json','calls.json']:
            v=get(r,n);u=v['usage'] if n=='usage-1.json' else v['events'][3]['payload']['usage'] if n=='events.json' else v['calls'][0]['usage'];u['input_tokens']=True;put(r,n,v)
    case('correlated-bool-usage','REJECT',correlated_bool)
    case('duplicate-json-key','REJECT',lambda r:(r/'prompt.json').write_text('{"x":1,"x":2}\n'))
    case('nonfinite-nan','REJECT',lambda r:(r/'prompt.json').write_text('{"x":NaN}\n'))
    case('null-grant','REJECT',lambda r:edit(r,'grant.json',lambda d:d.update(grant_id=None)))
    case('placeholder-source-sha','REJECT',lambda r:edit(r,'context-1.json',lambda d:d.update(source_sha256='<PLACEHOLDER:SOURCE>')))
    case('release-claims-science','REJECT',lambda r:edit(r,'release.json',lambda d:d.update(scientific_claim='PASS')),reseal=False)
    def missing_raw(r):
        edit(r,'calls.json',lambda d:d['calls'][0].update(raw_usage_artifact_id=None));edit(r,'events.json',lambda d:d['events'][3]['payload'].update(raw_usage_artifact_id=None))
    case('raw-usage-missing','UNRESOLVED',missing_raw)
    case('session-arm-reuse','REJECT',lambda r:(two(r),edit(r,'attempts.json',lambda d:d['attempts'][1].update(session_id=d['attempts'][0]['session_id']))))
    # Correlated changes cannot conceal a changed raw usage total.
    case('raw-usage-tamper-rehashed','REJECT',lambda r:edit(r,'usage-1.json',lambda d:d['usage'].update(total_tokens=13)),expect_reason='RAW_USAGE_BINDING')
    # Core source and generation prompt digests are independent of outer manifest hashes.
    case('source-tamper-rehashed','REJECT',lambda r:(r/'source.txt').write_text('Different synthetic source\n'),expect_reason='CONTEXT_SOURCE_FORMAT_OR_TOOL')
    case('parent-count-cross-session','REJECT',lambda r:(two(r),edit(r,'events.json',lambda d:d['events'][6]['payload'].update(parent_count_request_id='synth-count-1'))),expect_reason='PARENT_COUNT')
    summary={'source_sha256':H(SRC),'schema_sha256':H(SRC.with_name('schema.json')),'probe_count':len(CASES),'expectation_failures':[c for c in CASES if not c['expectation_met'] or c.get('extra_check') is False],'cases':CASES,'all_science_NOT_EVALUATED':all(get(OUT/c['case'],'result.json')['scientific_attribution']['status']=='NOT_EVALUATED' for c in CASES)}
    put(OUT,'summary.json',summary);print('SUMMARY',len(CASES),'expectation failures',len(summary['expectation_failures']))
if __name__=='__main__':run()

