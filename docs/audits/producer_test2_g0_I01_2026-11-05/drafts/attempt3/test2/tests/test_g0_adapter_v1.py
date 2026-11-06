"""New G0 pure synthetic JSON/text fixtures. No API, native, RTL or oracle runs."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'g0_v1'))
import adapter as g0

RECORD=None

def put(root,path,obj):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n' if not isinstance(obj,str) else obj)

def get(root,path):return json.loads((root/path).read_text())
def h(root,path):return g0.sha((root/path).read_bytes())
def header(name,**kw):return dict(schema_name='g0.'+name,schema_version=1,**kw)

def seal(root):
    """Top-level fixture sealing only: never repairs inner identity/semantic links."""
    m=get(root,'manifest.json')
    for a in m['artifacts']:
        p=root/a['path']
        if p.is_file() and not p.is_symlink():a['sha256']=g0.sha(p.read_bytes())
    put(root,'manifest.json',m)
    rel=header('release',origin='SYNTHETIC_FIXTURE',run_id=m['run_id'],manifest_sha256=h(root,'manifest.json'),all_attempts_frozen=True,hidden_evaluation_started=False,execution_allowed=False,allow_overwrite=False,scientific_claim='NOT_EVALUATED',files=[dict(path=a['path'],sha256=a['sha256']) for a in m['artifacts']]+[dict(path='manifest.json',sha256=h(root,'manifest.json'))])
    put(root,'release.json',rel)


def build(root):
    root.mkdir(parents=True,exist_ok=False);art=[]
    def add(aid,role,obj,visibility='MAINTAINER',text=False):
        path=aid+('.txt' if text else '.json');put(root,path,obj);art.append(dict(artifact_id=aid,path=path,sha256=h(root,path),kind='TEXT' if text else 'JSON',role=role,visibility=visibility));return aid
    policy=header('registration',run_id='synth-run',registration_id='synth-registration',model='synth-model',tier='standard',input_cap=20,output_cap=8,count_quota=8,generation_quota=8,retry_cap=1,reserve_per_generation_units=10,generation_reserve_units=80,count_reserve_units=10,total_reserve_units=90,stream_format='strict_serial',cache_policy='synth-no-provider-cache')
    add('registration','registration',policy)
    add('grant','grant',header('offline_grant',grant_id='synth-offline-authority',run_id='synth-run',registration_id='synth-registration',registration_sha256=h(root,'registration.json'),scope='OFFLINE_SYNTHETIC_RECORD_VALIDATION_ONLY',execution_allowed=False,API_allowed=False))
    add('source','source','SYNTHETIC TEXT ONLY. No RTL or scientific source.\n','PUBLIC_DEV',True)
    add('toolchain','toolchain',{'declaration':'SYNTHETIC. No tool run.'})
    add('format','format',{'declaration':'SYNTHETIC output-format stub; no model request.'},'PUBLIC_DEV')
    add('pins','pins',header('pins',clock_domain='synth-clock',edge='posedge',reset_polarity='high',reset_kind='synchronous',phase_contract='synth-pre-post-contract',slot_count=6,pins=[dict(name='synth-signal',width=8,signedness='unsigned')]))
    add('prompt','prompt',{'declaration':'SYNTHETIC prompt stub; never sent anywhere.'},'PUBLIC_DEV')
    context=header('context',context_id='synth-context-1',run_id='synth-run',registration_id='synth-registration',registration_sha256=h(root,'registration.json'),arm_id='B',session_id='synth-session-1',round_index=1,attempt_index=1,prompt_artifact_id='prompt',prompt_sha256=h(root,'prompt.json'),messages_sha256=g0.sha(g0.canonical(get(root,'prompt.json'))),format_schema_sha256=h(root,'format.json'),source_sha256=h(root,'source.txt'),toolchain_sha256=h(root,'toolchain.json'),pin_contract_sha256=h(root,'pins.json'),candidate_input_artifact_ids=['source','prompt','format'])
    add('context-1','context',context)
    usage=dict(input_tokens=10,output_tokens=2,total_tokens=12,cached_input_tokens=3,reasoning_output_tokens=1)
    add('usage-1','usage',header('usage',usage=usage))
    add('response-1','response',header('response',response_id='synth-response-1',payload='Synthetic fixture response only;not a monitor.'))
    a=dict(attempt_id='synth-attempt-1',run_id='synth-run',arm_id='B',session_id='synth-session-1',round_index=1,attempt_index=1,context_id='synth-context-1',context_artifact_id='context-1',context_sha256=h(root,'context-1.json'),prompt_artifact_id='prompt',messages_sha256=context['messages_sha256'],accepted_response_artifact_id='response-1')
    add('attempts','attempts',header('attempts',run_id='synth-run',attempts=[a]))
    def event(i,kind,rid,payload):return dict(event_id='synth-event-'+str(i),event_sequence=i,run_id='synth-run',attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],request_id=rid,event_type=kind,payload=payload)
    events=[event(0,'count_dispatched','synth-count-1',dict(requested_model=policy['model'],format_schema_sha256=h(root,'format.json'),messages_sha256=a['messages_sha256'])),event(1,'count_returned','synth-count-1',dict(input_tokens=10)),event(2,'generation_dispatched','synth-generation-1',dict(requested_model=policy['model'],requested_tier=policy['tier'],parent_count_request_id='synth-count-1',input_tokens_counted=10,max_output_tokens=8,messages_sha256=a['messages_sha256'],format_schema_sha256=h(root,'format.json'),reserve_units=10,cumulative_reserve_units=10)),event(3,'generation_returned','synth-generation-1',dict(response_id='synth-response-1',returned_model=policy['model'],returned_tier=policy['tier'],usage=usage,raw_usage_artifact_id='usage-1',response_artifact_id='response-1'))]
    add('events','events',header('events',run_id='synth-run',events=events))
    call=dict(call_id='synth-call-1',run_id='synth-run',attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],count_request_issued=True,generation_request_issued=True,count_request_id='synth-count-1',generation_request_id='synth-generation-1',count_terminal_event_id=events[1]['event_id'],generation_terminal_event_id=events[3]['event_id'],status='COMPLETED',status_reason=None,accepted_response=True,input_token_count=10,response_id='synth-response-1',response_artifact_id='response-1',returned_model=policy['model'],returned_tier=policy['tier'],usage=usage,raw_usage_artifact_id='usage-1')
    add('calls','calls',header('calls',run_id='synth-run',calls=[call]))
    add('observations','observations',header('observations',run_id='synth-run',observations=[]))
    put(root,'manifest.json',header('bundle',origin='SYNTHETIC_FIXTURE',identity_origin='EXPLICIT',run_id='synth-run',registration_id='synth-registration',stream_format='strict_serial',artifacts=art,bindings={x:x for x in ['registration','grant','events','calls','attempts','observations','source','toolchain','pins','format']}));seal(root)


def edit(root,path,fn):
    d=get(root,path);fn(d);put(root,path,d)

def failed(root,missing=False,count_only=False):
    a=get(root,'attempts.json');a['attempts'][0]['accepted_response_artifact_id']=None;put(root,'attempts.json',a)
    c=get(root,'calls.json');call=c['calls'][0];call.update(status='TRANSPORT_ERROR',status_reason='Synthetic failure;not an actual request',accepted_response=False,response_id=None,response_artifact_id=None,returned_model=None,returned_tier=None,usage=None,raw_usage_artifact_id=None)
    e=get(root,'events.json')
    if count_only:
        call.update(generation_request_issued=False,generation_request_id=None,generation_terminal_event_id=None,input_token_count=None)
        if missing:e['events']=e['events'][:1];call['count_terminal_event_id']=None
        else:e['events']=e['events'][:2];e['events'][1].update(event_type='count_error',payload=dict(error_type='SyntheticTransportError'))
    else:
        if missing:e['events']=e['events'][:3];call['generation_terminal_event_id']=None
        else:e['events'][3].update(event_type='generation_error',payload=dict(error_type='SyntheticTransportError',usage_status='UNKNOWN_NOT_ZERO'))
    put(root,'calls.json',c);put(root,'events.json',e)


def halted(root,scope='retry',illegal=False,event_only=False,flag_only=False):
    """New canonical fixture: response binding is correct before any halt mutation."""
    aa=get(root,'attempts.json');cc=get(root,'calls.json');ee=get(root,'events.json');first=aa['attempts'][0];first['accepted_response_artifact_id']=None
    c=cc['calls'][0];c.update(status='INPUT_CAP_NO_GENERATION',status_reason='Synthetic count exceeds cap;no actual generation',accepted_response=False,generation_request_issued=False,generation_request_id=None,generation_terminal_event_id=None,input_token_count=21,response_id=None,response_artifact_id=None,returned_model=None,returned_tier=None,usage=None,raw_usage_artifact_id=None)
    ee['events']=ee['events'][:2];ee['events'][1]['payload']['input_tokens']=21
    halt=copy.deepcopy(ee['events'][0]);halt.update(event_id='synth-halt',event_sequence=2,event_type='resource_halt',request_id=None,payload=dict(reason='Synthetic persistent stop'));ee['events'].append(halt)
    second=copy.deepcopy(first);second.update(attempt_id='synth-attempt-2',context_id='synth-context-2',context_artifact_id='context-2',attempt_index=2,accepted_response_artifact_id='response-1' if illegal else None)
    ctx=get(root,'context-1.json');ctx['context_id']=second['context_id'];ctx['attempt_index']=2
    if scope=='round':second.update(round_index=2,attempt_index=1);ctx.update(round_index=2,attempt_index=1)
    if scope=='session':second.update(session_id='synth-session-2',attempt_index=1);ctx.update(session_id='synth-session-2',attempt_index=1)
    put(root,'context-2.json',ctx);second['context_sha256']=h(root,'context-2.json');aa['attempts'].append(second)
    m=get(root,'manifest.json');m['artifacts'].append(dict(artifact_id='context-2',path='context-2.json',sha256=h(root,'context-2.json'),kind='JSON',role='context',visibility='MAINTAINER'));put(root,'manifest.json',m)
    later=copy.deepcopy(c);later.update(call_id='synth-call-2',attempt_id=second['attempt_id'],context_id=second['context_id'],context_sha256=second['context_sha256'],count_request_issued=False,count_request_id=None,count_terminal_event_id=None,input_token_count=None,status='NOT_RUN',status_reason='Synthetic halt;no request or usage')
    if illegal:
        base=get(root,'calls.json')['calls'][0];later.update(base);later.update(call_id='synth-call-2',attempt_id=second['attempt_id'],context_id=second['context_id'],context_sha256=second['context_sha256'],count_request_issued=True,generation_request_issued=True,count_request_id='synth-count-2',generation_request_id='synth-generation-2',count_terminal_event_id='synth-event-4',generation_terminal_event_id='synth-event-6',input_token_count=10,status='COMPLETED',status_reason=None,accepted_response=True,response_id='synth-response-1',response_artifact_id='response-1',returned_model='synth-model',returned_tier='standard',usage=get(root,'usage-1.json')['usage'],raw_usage_artifact_id='usage-1')
        p=get(root,'context-2.json');u=get(root,'usage-1.json')['usage']
        for i,(kind,rid,payload) in enumerate([('count_dispatched','synth-count-2',dict(requested_model='synth-model',format_schema_sha256=h(root,'format.json'),messages_sha256=p['messages_sha256'])),('count_returned','synth-count-2',dict(input_tokens=10)),('generation_dispatched','synth-generation-2',dict(requested_model='synth-model',requested_tier='standard',parent_count_request_id='synth-count-2',input_tokens_counted=10,max_output_tokens=8,messages_sha256=p['messages_sha256'],format_schema_sha256=h(root,'format.json'),reserve_units=10,cumulative_reserve_units=10)),('generation_returned','synth-generation-2',dict(response_id='synth-response-1',returned_model='synth-model',returned_tier='standard',usage=u,raw_usage_artifact_id='usage-1',response_artifact_id='response-1'))],3):
            ee['events'].append(dict(event_id='synth-event-'+str(i),event_sequence=i,run_id='synth-run',attempt_id=second['attempt_id'],context_id=second['context_id'],context_sha256=second['context_sha256'],request_id=rid,event_type=kind,payload=payload))
    if flag_only:later.update(count_request_issued=True,count_request_id='synth-count-2')
    if event_only:
        extra=copy.deepcopy(ee['events'][0]);extra.update(event_id='synth-orphan',event_sequence=3,attempt_id=second['attempt_id'],context_id=second['context_id'],context_sha256=second['context_sha256'],request_id='synth-orphan-request');ee['events'].append(extra)
    cc['calls'].append(later);put(root,'attempts.json',aa);put(root,'calls.json',cc);put(root,'events.json',ee)


def observation(root,**override):
    m=get(root,'manifest.json')
    for aid,role in [('raw-meta','raw_metadata'),('reference-meta','reference_descriptor')]:
        put(root,aid+'.txt','SYNTHETIC METADATA SENTINEL ONLY. No VCD, rows, waveform, monitor or checker.\n');m['artifacts'].append(dict(artifact_id=aid,path=aid+'.txt',sha256=h(root,aid+'.txt'),kind='TEXT',role=role,visibility='MAINTAINER'))
    put(root,'manifest.json',m)
    o=dict(observation_id='synth-observation',source_artifact_id='source',source_sha256=h(root,'source.txt'),raw_metadata_artifact_id='raw-meta',raw_metadata_sha256=h(root,'raw-meta.txt'),checker_artifact_id='reference-meta',checker_sha256=h(root,'reference-meta.txt'),pin_contract_sha256=h(root,'pins.json'),clock_domain='synth-clock',edge='posedge',reset_polarity='high',reset_kind='synchronous',phase_contract='synth-pre-post-contract',cycle=1,phase='pre',slot=2,declared_vector_width=3,selected_knownness='KNOWN',reference_last_cycle=0,reference_last_phase='post',reference_verdict=None,reference_origin='NOT_EVALUATED',selected_alarm_confirmed=False,monitor_correctness_proved=False,completion128_proved=False,native_mode='NOT_EVALUATED',scientific_claim='NOT_EVALUATED',metadata_anchor='LOCAL_CONTENT_ONLY');o.update(override);put(root,'observations.json',header('observations',run_id='synth-run',observations=[o]))


def bind_contexts(root):
    aa=get(root,'attempts.json');ee=get(root,'events.json');cc=get(root,'calls.json')
    for a in aa['attempts']:
        path=a['context_artifact_id']+'.json';ctx=get(root,path);ctx['registration_sha256']=h(root,'registration.json');put(root,path,ctx);a['context_sha256']=h(root,path)
        for item in ee['events']+cc['calls']:
            if item['attempt_id']==a['attempt_id']:item['context_sha256']=a['context_sha256']
    put(root,'attempts.json',aa);put(root,'events.json',ee);put(root,'calls.json',cc)


def policy_change(root,**kw):
    edit(root,'registration.json',lambda d:d.update(kw));edit(root,'grant.json',lambda d:d.update(registration_sha256=h(root,'registration.json')));bind_contexts(root)


def two_sessions(root,duplicate_response=False):
    aa=get(root,'attempts.json');ee=get(root,'events.json');cc=get(root,'calls.json');m=get(root,'manifest.json')
    a=copy.deepcopy(aa['attempts'][0]);a.update(attempt_id='synth-attempt-2',arm_id='C',session_id='synth-session-2',context_id='synth-context-2',context_artifact_id='context-2',accepted_response_artifact_id='response-2')
    ctx=get(root,'context-1.json');ctx.update(arm_id='C',session_id='synth-session-2',context_id='synth-context-2');put(root,'context-2.json',ctx);a['context_sha256']=h(root,'context-2.json');aa['attempts'].append(a)
    response_id='synth-response-1' if duplicate_response else 'synth-response-2';put(root,'response-2.json',header('response',response_id=response_id,payload='Secondsyntheticresponse;not amonitor'))
    for aid,role in [('context-2','context'),('response-2','response')]:m['artifacts'].append(dict(artifact_id=aid,path=aid+'.json',sha256=h(root,aid+'.json'),kind='JSON',role=role,visibility='MAINTAINER'))
    for i,e in enumerate(copy.deepcopy(ee['events']),4):
        e.update(event_id='synth-event-'+str(i),event_sequence=i,attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],request_id='synth-count-2' if i<6 else 'synth-generation-2')
        if i==6:e['payload'].update(parent_count_request_id='synth-count-2',cumulative_reserve_units=20)
        if i==7:e['payload'].update(response_id=response_id,response_artifact_id='response-2')
        ee['events'].append(e)
    c=copy.deepcopy(cc['calls'][0]);c.update(call_id='synth-call-2',attempt_id=a['attempt_id'],context_id=a['context_id'],context_sha256=a['context_sha256'],count_request_id='synth-count-2',generation_request_id='synth-generation-2',count_terminal_event_id='synth-event-5',generation_terminal_event_id='synth-event-7',response_id=response_id,response_artifact_id='response-2');cc['calls'].append(c)
    put(root,'manifest.json',m);put(root,'attempts.json',aa);put(root,'events.json',ee);put(root,'calls.json',cc)


class G0Tests(unittest.TestCase):
    def run_case(self,mutate=None,status='REJECT',reseal=True):
        temp=None
        if RECORD is None:temp=tempfile.TemporaryDirectory();case=Path(temp.name).resolve()
        else:case=RECORD/self._testMethodName;case.mkdir(exist_ok=False)
        bundle=case/'bundle';build(bundle)
        if mutate:mutate(bundle)
        if reseal:seal(bundle)
        before={str(p.relative_to(bundle)):h(bundle,str(p.relative_to(bundle))) for p in bundle.rglob('*') if p.is_file() and not p.is_symlink()}
        result=g0.validate_bundle(bundle)
        put(case,'result.json',result);put(case,'fixture-binding.json',dict(symlinks={str(p.relative_to(bundle)):str(p.readlink()) for p in bundle.rglob('*') if p.is_symlink()},origin='PURE_SYNTHETIC_JSON_TEXT_NO_SCIENTIFIC_DATA',expected=status,actual=result['integrity']['status'],adapter_source_sha256=result['adapter_source_sha256'],schema_sha256=result['schema_sha256'],input_sha256=copy.deepcopy(before)))
        after={str(p.relative_to(bundle)):h(bundle,str(p.relative_to(bundle))) for p in bundle.rglob('*') if p.is_file() and not p.is_symlink()};self.assertEqual(before,after,'validator mutated fixtureinput');self.assertEqual(result['integrity']['status'],status,result['integrity']);self.assertEqual(result['scientific_attribution']['status'],'NOT_EVALUATED');self.assertFalse(any(result['execution_capabilities'].values()))
        if temp:temp.cleanup()
        return result
    def test_01_baseline(self):self.run_case(status='PASS_WITH_SCOPE')
    def test_02_bool_not_integer(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][0].update(event_sequence=True)))
    def test_03_duplicate_event(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][1].update(event_id=d['events'][0]['event_id'])))
    def test_04_orphan_terminal(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][3].update(request_id='synth-orphan')))
    def test_05_missing_returned_claims_success(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'].pop()))
    def test_06_missing_generation_terminal_unknown(self):
        x=self.run_case(lambda r:failed(r,missing=True),status='UNRESOLVED');self.assertIsNone(x['ledger']['attempts'][0]['actual_tokens']);self.assertIsNone(x['cost_knownness']['tokens']['value'])
    def test_07_generation_transport_error_unknown(self):self.run_case(lambda r:failed(r),status='UNRESOLVED')
    def test_08_count_transport_error_unknown(self):self.run_case(lambda r:failed(r,count_only=True),status='UNRESOLVED')
    def test_09_missing_request_identity(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][0].pop('request_id')))
    def test_10_context_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][0].update(context_id='synth-other')))
    def test_11_session_mismatch(self):self.run_case(lambda r:edit(r,'context-1.json',lambda d:d.update(session_id='synth-other')))
    def test_12_prompt_mismatch(self):self.run_case(lambda r:put(r,'prompt.json',{'changed':'synthetic'}))
    def test_13_schema_digest_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][0]['payload'].update(format_schema_sha256='0'*64)))
    def test_14_response_mismatch(self):self.run_case(lambda r:edit(r,'response-1.json',lambda d:d.update(response_id='synth-other')))
    def test_15_parent_count_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][2]['payload'].update(parent_count_request_id='synth-other')))
    def test_16_illegal_order(self):
        def change(r):
            d=get(r,'events.json');d['events'][1],d['events'][2]=d['events'][2],d['events'][1]
            for i,e in enumerate(d['events']):e['event_sequence']=i
            put(r,'events.json',d)
        self.run_case(change)
    def test_17_halt_retry(self):self.run_case(lambda r:halted(r,illegal=True))
    def test_18_halt_round(self):self.run_case(lambda r:halted(r,'round',illegal=True))
    def test_19_halt_session(self):self.run_case(lambda r:halted(r,'session',illegal=True))
    def test_20_halt_flags(self):self.run_case(lambda r:halted(r,flag_only=True))
    def test_21_halt_orphan_dispatch(self):self.run_case(lambda r:halted(r,event_only=True))
    def test_22_legal_halt_notrun(self):
        x=self.run_case(lambda r:halted(r),status='PASS_WITH_SCOPE');self.assertTrue(x['ledger']['halted']);self.assertIsNone(x['ledger']['attempts'][1]['actual_tokens'])
    def test_23_usage_arithmetic_correlated(self):
        def change(r):
            edit(r,'usage-1.json',lambda d:d['usage'].update(total_tokens=13));edit(r,'events.json',lambda d:d['events'][3]['payload']['usage'].update(total_tokens=13));edit(r,'calls.json',lambda d:d['calls'][0]['usage'].update(total_tokens=13))
        self.run_case(change)
    def test_24_usage_subset_correlated(self):
        def change(r):
            for p in ['usage-1.json','events.json','calls.json']:
                d=get(r,p);u=d['usage'] if p.startswith('usage') else d['events'][3]['payload']['usage'] if p.startswith('events') else d['calls'][0]['usage'];u['cached_input_tokens']=11;put(r,p,d)
        self.run_case(change)
    def test_25_model_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][2]['payload'].update(requested_model='synth-other')))
    def test_26_tier_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][2]['payload'].update(requested_tier='synth-other')))
    def test_27_count_mismatch(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][1]['payload'].update(input_tokens=11)))
    def test_28_count_quota(self):
        def change(r):policy_change(r,count_quota=0)
        self.run_case(change)
    def test_29_output_cap(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][2]['payload'].update(max_output_tokens=9)))
    def test_30_reserve(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][2]['payload'].update(cumulative_reserve_units=20)))
    def test_31_raw_usage_mismatch(self):self.run_case(lambda r:edit(r,'usage-1.json',lambda d:d['usage'].update(output_tokens=3)))
    def test_32_missing_usage_unknown(self):
        def change(r):
            edit(r,'attempts.json',lambda d:d['attempts'][0].update(accepted_response_artifact_id=None));edit(r,'calls.json',lambda d:d['calls'][0].update(status='REJECTED_RESPONSE',status_reason='Synthetic missingusage',accepted_response=False,usage=None,raw_usage_artifact_id=None));edit(r,'events.json',lambda d:d['events'][3]['payload'].update(usage=None,raw_usage_artifact_id=None))
        self.run_case(change,status='UNRESOLVED')
    def test_33_manifest_sha_tamper(self):self.run_case(lambda r:put(r,'source.txt','SYNTHETIC altered\n'),reseal=False)
    def test_34_release_digest(self):self.run_case(lambda r:edit(r,'release.json',lambda d:d.update(manifest_sha256='0'*64)),reseal=False)
    def test_35_release_inventory(self):self.run_case(lambda r:edit(r,'release.json',lambda d:d['files'].pop()),reseal=False)
    def test_36_template_not_release(self):self.run_case(lambda r:put(r,'release.json',{'status':'TEMPLATE_ONLY_NOT_A_VALID_RELEASE'}),reseal=False)
    def test_37_template_not_grant(self):self.run_case(lambda r:put(r,'grant.json',{'status':'TEMPLATE_ONLY_NOT_A_VALID_RELEASE'}))
    def test_38_no_historical_identity_fabrication(self):self.run_case(lambda r:edit(r,'manifest.json',lambda d:d.update(identity_origin='HISTORICAL_ABSENT')))
    def test_39_concurrency_unsupported(self):self.run_case(lambda r:edit(r,'manifest.json',lambda d:d.update(stream_format='concurrent')))
    def test_40_reduced_metadata_vector_scope_only(self):self.run_case(lambda r:observation(r),status='PASS_WITH_SCOPE')
    def test_41_slot_missing(self):self.run_case(lambda r:observation(r,slot=3))
    def test_42_phase_mismatch(self):self.run_case(lambda r:observation(r,phase_contract='synth-wrong'))
    def test_43_prefix_mismatch(self):self.run_case(lambda r:observation(r,reference_last_cycle=1))
    def test_44_unknown_bit_not_alarm(self):
        x=self.run_case(lambda r:observation(r,selected_knownness='UNKNOWN'),status='PASS_WITH_SCOPE');self.assertTrue(x['observations']['selected_unknown_declared']);self.assertFalse(x['scientific_attribution']['selected_alarm_confirmed'])
    def test_45_checker_sha_mismatch(self):self.run_case(lambda r:observation(r,checker_sha256='0'*64))
    def test_46_unanchored_metadata_upgrade(self):self.run_case(lambda r:observation(r,selected_alarm_confirmed=True))
    def test_47_completion_upgrade(self):self.run_case(lambda r:observation(r,completion128_proved=True))
    def test_48_fake_reference_verdict(self):self.run_case(lambda r:observation(r,reference_verdict='UNKNOWN'))
    def test_49_prompt_visibility_leak(self):self.run_case(lambda r:edit(r,'manifest.json',lambda d:next(a for a in d['artifacts'] if a['artifact_id']=='prompt').update(visibility='REFERENCE_ONLY')))
    def test_50_bad_sha_type(self):self.run_case(lambda r:edit(r,'manifest.json',lambda d:d['artifacts'][0].update(sha256=None)),reseal=False)
    def test_51_unknown_extra_field(self):self.run_case(lambda r:edit(r,'calls.json',lambda d:d['calls'][0].update(unreviewed_scientific_PASS=True)))
    def test_52_notreached_retained(self):
        def change(r):
            failed(r);edit(r,'calls.json',lambda d:d['calls'][0].update(status='NOT_REACHED',status_reason='Synthetic targetnotreached;errorcostunknown'))
        self.run_case(change,status='UNRESOLVED')
    def test_53_invalid_retained(self):
        def change(r):failed(r);edit(r,'calls.json',lambda d:d['calls'][0].update(status='INVALID',status_reason='Synthetic invalidresponse'))
        self.run_case(change,status='UNRESOLVED')
    def test_54_relative_path_escape(self):self.run_case(lambda r:edit(r,'manifest.json',lambda d:d['artifacts'][0].update(path='../outside.json')),reseal=False)
    def test_55_symlink_input(self):
        def change(r):
            p=r/'source.txt';p.unlink();p.symlink_to(r/'format.json')
        self.run_case(change,reseal=False)
    def test_56_output_refuses_overwrite(self):
        x=self.run_case(status='PASS_WITH_SCOPE')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();out=root/'g0-report';path=g0.publish(out,x,root);before=path.read_bytes()
            with self.assertRaises(g0.Reject):g0.publish(out,x,root)
            self.assertEqual(path.read_bytes(),before)
    def test_57_output_symlink(self):
        self.run_case(status='PASS_WITH_SCOPE')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();target=root/'old';target.mkdir();out=root/'g0-link';out.symlink_to(target,target_is_directory=True)
            with self.assertRaises(g0.Reject):g0.publish(out,{},root)
            self.assertEqual(list(target.iterdir()),[])
    def test_58_duplicate_json_key(self):self.run_case(lambda r:put(r,'prompt.json','{"x":1,"x":2}\n'))
    def test_59_missing_artifact(self):self.run_case(lambda r:(r/'format.json').unlink(),reseal=False)
    def test_60_wrong_phase_type(self):self.run_case(lambda r:observation(r,phase=1))

    def test_61_correlated_returned_model(self):
        def change(r):
            edit(r,'events.json',lambda d:d['events'][3]['payload'].update(returned_model='synth-other'));edit(r,'calls.json',lambda d:d['calls'][0].update(returned_model='synth-other'))
        self.run_case(change)
    def test_62_correlated_returned_tier(self):
        def change(r):
            edit(r,'events.json',lambda d:d['events'][3]['payload'].update(returned_tier='synth-other'));edit(r,'calls.json',lambda d:d['calls'][0].update(returned_tier='synth-other'))
        self.run_case(change)
    def test_63_generation_quota(self):
        def change(r):policy_change(r,generation_quota=0)
        x=self.run_case(change);self.assertIn('GENERATION_QUOTA',x['integrity']['reasons'][0])
    def test_64_missing_usage_subsets_null(self):
        x=self.run_case(lambda r:failed(r),status='UNRESOLVED');self.assertTrue(all(v is None for v in x['cost_knownness']['tokens']['subsets'].values()))
    def test_65_malformed_json(self):self.run_case(lambda r:put(r,'prompt.json','{"incomplete":'))
    def test_66_null_required_identity(self):self.run_case(lambda r:edit(r,'events.json',lambda d:d['events'][0].update(context_id=None)))

    def test_67_two_sessions_valid(self):self.run_case(lambda r:two_sessions(r),status='PASS_WITH_SCOPE')
    def test_68_duplicate_response_correlated(self):
        x=self.run_case(lambda r:two_sessions(r,True));self.assertIn('DUPLICATE_RESPONSE_ID',x['integrity']['reasons'][0])
    def test_69_retry_without_halt_valid(self):
        def change(r):
            halted(r,illegal=True);d=get(r,'events.json');d['events']=[e for e in d['events'] if e['event_type']!='resource_halt']
            for i,e in enumerate(d['events']):e['event_sequence']=i
            put(r,'events.json',d)
        self.run_case(change,status='PASS_WITH_SCOPE')
    def test_70_retry_cap_reached(self):
        def change(r):halted(r);policy_change(r,retry_cap=0)
        x=self.run_case(change);self.assertIn('RETRY_ORDER_OR_CAP',x['integrity']['reasons'][0])
    def test_71_duplicate_call(self):self.run_case(lambda r:edit(r,'calls.json',lambda d:d['calls'].append(copy.deepcopy(d['calls'][0]))))
    def test_72_orphan_dispatch(self):
        def change(r):
            d=get(r,'events.json');x=copy.deepcopy(d['events'][0]);x.update(event_id='synth-orphan',event_sequence=4,request_id='synth-extra');d['events'].append(x);put(r,'events.json',d)
        self.run_case(change)
    def test_73_hidden_candidate_input_correlated(self):
        def change(r):
            observation(r);edit(r,'context-1.json',lambda d:d['candidate_input_artifact_ids'].append('reference-meta'));bind_contexts(r)
        x=self.run_case(change);self.assertIn('CANDIDATE_INPUT_LEAK',x['integrity']['reasons'][0])
    def test_74_invalid_unreferenced_structured_artifact(self):
        def change(r):
            put(r,'extra.json',{'malformed':'syntheticusage'});m=get(r,'manifest.json');m['artifacts'].append(dict(artifact_id='extra',path='extra.json',sha256=h(r,'extra.json'),kind='JSON',role='usage',visibility='MAINTAINER'));put(r,'manifest.json',m)
        self.run_case(change)
    def test_75_unsupported_raw_parser_claim(self):self.run_case(lambda r:observation(r,native_mode='bmc'))
    def test_76_nan_json(self):self.run_case(lambda r:put(r,'prompt.json','{"x":NaN}'))
    def test_77_output_path_escape(self):
        self.run_case(status='PASS_WITH_SCOPE')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();other=root/'other';other.mkdir()
            with self.assertRaises(g0.Reject):g0.publish(other/'g0-report',{},root)
            self.assertEqual(list(other.iterdir()),[])
    def test_78_unknown_core_usage_must_not_be_accepted(self):
        def change(r):
            edit(r,'events.json',lambda d:d['events'][3]['payload'].update(usage=None,raw_usage_artifact_id=None));edit(r,'calls.json',lambda d:d['calls'][0].update(usage=None,raw_usage_artifact_id=None))
        self.run_case(change)


def main():
    global RECORD
    p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);a=p.parse_args();RECORD=a.record.resolve();RECORD.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();suite=unittest.defaultTestLoader.loadTestsFromTestCase(G0Tests)
    with (RECORD/'unittest.log').open('x') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    summary=dict(scope='ONLY_NEW_G0_LIGHT_SYNTHETIC_FIXTURES_NO_API_NATIVE_OR_SCIENCE',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),seconds=time.perf_counter()-start,adapter_source_sha256=g0.sha(Path(g0.__file__).read_bytes()),schema_sha256=g0.sha(g0.SCHEMA_BYTES),tests_source_sha256=g0.sha(Path(__file__).read_bytes()),fixture_case_directories=len(list(RECORD.glob('test_*'))),passed=result.wasSuccessful(),new_scientific_samples=0)
    put(RECORD,'summary.json',summary);print(json.dumps(summary));return int(not result.wasSuccessful())


if __name__=='__main__':raise SystemExit(main())
