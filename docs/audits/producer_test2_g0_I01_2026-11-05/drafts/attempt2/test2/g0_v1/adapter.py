"""G0 v1: offline synthetic metadata adapter; no clients, tools, oracle or dispatch.

Closed-shape DSL is explicit in schema.json (not a general JSON Schema engine).
Raw scientific parsers and independent truth/labels are deliberately unsupported.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
MAX_BYTES=2_000_000


class Reject(ValueError):pass

def require(ok,code):
    if not ok:raise Reject(code)

def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pairs(items):
    out={}
    for k,v in items:
        require(k not in out,'DUPLICATE_JSON_KEY:'+k);out[k]=v
    return out

def parse_json(raw):
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Reject('NONFINITE_JSON')))

SCHEMA_BYTES=(HERE/'schema.json').read_bytes()
DEFS=parse_json(SCHEMA_BYTES)['definitions']


def shape(name,value,path='$',depth=0):
    """Validate the finite bundled closed-shapes DSL with exact Python types."""
    require(depth<32,'SCHEMA_DEPTH')
    spec=DEFS[name] if isinstance(name,str) else name
    if value is None:
        require(spec.get('nullable') is True or spec.get('type')=='null','NULL_NOT_ALLOWED:'+path);return
    if 'ref' in spec:return shape(spec['ref'],value,path,depth+1)
    kind=spec['type'];types={'string':str,'integer':int,'boolean':bool,'object':dict,'array':list}
    require(kind in types and type(value)is types[kind],'TYPE:'+path)
    if 'const' in spec:require(type(value)is type(spec['const']) and value==spec['const'],'CONST:'+path)
    if 'enum' in spec:require(value in spec['enum'],'ENUM:'+path)
    if kind=='string':
        require(len(value)>=spec.get('min_length',1) and len(value)<=spec.get('max_length',4096),'STRING_SIZE:'+path)
        if 'pattern' in spec:require(re.fullmatch(spec['pattern'],value) is not None,'PATTERN:'+path)
    elif kind=='integer':require(spec.get('minimum',0)<=value<=spec.get('maximum',2**53-1),'INTEGER_RANGE:'+path)
    elif kind=='array':
        require(len(value)<=spec.get('max_items',2048),'ARRAY_SIZE:'+path)
        for i,v in enumerate(value):shape(spec['items'],v,f'{path}[{i}]',depth+1)
    elif kind=='object':
        props=spec['properties'];require(set(props)<=set(value),'MISSING_FIELDS:'+path)
        require(spec.get('allow_extra') is True or set(value)==set(props),'EXTRA_FIELDS:'+path)
        for k,s in props.items():shape(s,value[k],path+'.'+k,depth+1)


class Reader:
    def __init__(self,root):
        given=Path(root).absolute();require(not given.is_symlink(),'SYMLINK_ROOT');self.root=given.resolve()
        parts=self.root.parts;require(not any(parts[i:i+2]==('build','private') for i in range(len(parts)-1)),'PRIVATE_ROOT')
        require(not any(x in ('.ssh','.aws','secrets') for x in parts),'PRIVATE_ROOT')
        self.hashes={};self.total_bytes=0
    def path(self,name):
        require(type(name)is str and len(name)<512,'PATH_TYPE')
        pp=PurePosixPath(name);require(not pp.is_absolute() and str(pp)==name and name not in ('','.'),'PATH_NOT_RELATIVE')
        require(all(re.fullmatch(r'[A-Za-z0-9_.-]+',p) and p not in ('.','..','private','secrets','.ssh','.aws') for p in pp.parts),'PATH_COMPONENT')
        require(pp.suffix in ('.json','.txt'),'UNSUPPORTED_ARTIFACT_EXTENSION')
        current=self.root
        for part in pp.parts:
            current=current/part;require(not current.is_symlink(),'SYMLINK_ARTIFACT')
        require(current.resolve().is_relative_to(self.root),'PATH_ESCAPE');return current
    def raw(self,name):
        p=self.path(name)
        fd=os.open(p,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
        with os.fdopen(fd,'rb') as f:
            info=os.fstat(f.fileno());require(stat.S_ISREG(info.st_mode) and info.st_size<=MAX_BYTES,'ARTIFACT_SIZE_OR_TYPE');raw=f.read(MAX_BYTES+1)
        require(len(raw)<=MAX_BYTES,'ARTIFACT_SIZE');h=sha(raw);require(name not in self.hashes or self.hashes[name]==h,'INPUT_CHANGED_DURING_VALIDATION');self.hashes[name]=h;self.total_bytes+=len(raw);return raw
    def json(self,name):return parse_json(self.raw(name))


class Bundle:
    def __init__(self,reader):
        self.r=reader;self.manifest=reader.json('manifest.json');shape('Manifest',self.manifest);self.run=self.manifest['run_id'];self.art={};paths=set()
        for a in self.manifest['artifacts']:
            require(a['artifact_id'] not in self.art and a['path'] not in paths,'DUPLICATE_ARTIFACT_ID_OR_PATH');paths.add(a['path']);self.art[a['artifact_id']]=a
            raw=reader.raw(a['path']);require(sha(raw)==a['sha256'],'ARTIFACT_SHA:'+a['artifact_id'])
            if a['kind']=='JSON':parse_json(raw)
        require('manifest.json' not in paths and 'release.json' not in paths,'RESERVED_ARTIFACT_PATH')
        for role,aid in self.manifest['bindings'].items():require(aid in self.art and self.art[aid]['role']==role,'ROLE_BINDING:'+role)
    def artifact(self,aid,role=None):
        require(aid in self.art,'MISSING_ARTIFACT_REFERENCE');a=self.art[aid]
        if role:require(a['role']==role,'ARTIFACT_ROLE:'+role)
        return a
    def obj(self,aid,schema,role=None):
        a=self.artifact(aid,role);require(a['kind']=='JSON','EXPECTED_JSON_ARTIFACT');v=self.r.json(a['path']);shape(schema,v);return v
    def core(self,role,schema):return self.obj(self.manifest['bindings'][role],schema,role)
    def digest(self,role):return self.artifact(self.manifest['bindings'][role])['sha256']
    def release(self):
        v=self.r.json('release.json');shape('Release',v);require(v['run_id']==self.run and v['manifest_sha256']==self.r.hashes['manifest.json'],'RELEASE_MANIFEST_BINDING')
        files={}
        for x in v['files']:require(x['path'] not in files,'DUPLICATE_RELEASE_FILE');files[x['path']]=x['sha256']
        expected={a['path']:a['sha256'] for a in self.art.values()};expected['manifest.json']=self.r.hashes['manifest.json'];require(files==expected,'RELEASE_INVENTORY_OR_SHA')


def check_usage(u,policy,count):
    shape('Usage',u);require(u['input_tokens']==count<=policy['input_cap'],'USAGE_INPUT_COUNT_OR_CAP');require(u['output_tokens']<=policy['output_cap'],'USAGE_OUTPUT_CAP')
    require(u['total_tokens']==u['input_tokens']+u['output_tokens'],'USAGE_ARITHMETIC')
    for subset,total in [('cached_input_tokens','input_tokens'),('reasoning_output_tokens','output_tokens')]:require(u[subset] is None or u[subset]<=u[total],'USAGE_SUBSET:'+subset)


def attempts_and_contexts(b,policy):
    data=b.core('attempts','Attempts');require(data['run_id']==b.run,'ATTEMPTS_RUN');planned={};session_arms={};contexts=set();per_round=Counter()
    pins=b.core('pins','Pins');require(len({x['name'] for x in pins['pins']})==len(pins['pins']),'DUPLICATE_PIN')
    for a in data['attempts']:
        aid=a['attempt_id'];require(aid not in planned and a['run_id']==b.run,'DUPLICATE_ATTEMPT_OR_RUN');require(a['round_index']>0 and a['attempt_index']>0,'ATTEMPT_INDEX')
        require(session_arms.setdefault(a['session_id'],a['arm_id'])==a['arm_id'],'SESSION_ARM_REUSE')
        k=(a['session_id'],a['round_index']);per_round[k]+=1;require(a['attempt_index']==per_round[k] and a['attempt_index']<=policy['retry_cap']+1,'RETRY_ORDER_OR_CAP')
        require(a['context_id'] not in contexts,'DUPLICATE_CONTEXT');contexts.add(a['context_id'])
        c=b.obj(a['context_artifact_id'],'Context','context');require(b.artifact(a['context_artifact_id'])['sha256']==a['context_sha256'],'CONTEXT_SHA')
        require(all(c[k]==a[k] for k in ('context_id','run_id','arm_id','session_id','round_index','attempt_index','prompt_artifact_id','messages_sha256')),'CONTEXT_IDENTITY')
        require(c['registration_id']==b.manifest['registration_id'],'CONTEXT_REGISTRATION')
        p=b.artifact(a['prompt_artifact_id'],'prompt');require(p['kind']=='JSON' and p['visibility']=='PUBLIC_DEV','PROMPT_VISIBILITY_OR_TYPE');content=b.r.json(p['path'])
        require(c['prompt_sha256']==p['sha256'] and sha(canonical(content))==c['messages_sha256'],'PROMPT_BYTES_OR_MESSAGES')
        require(c['format_schema_sha256']==b.digest('format') and c['source_sha256']==b.digest('source') and c['toolchain_sha256']==b.digest('toolchain') and c['pin_contract_sha256']==b.digest('pins'),'CONTEXT_SOURCE_FORMAT_OR_TOOL')
        require(len(c['candidate_input_artifact_ids'])==len(set(c['candidate_input_artifact_ids'])),'DUPLICATE_CANDIDATE_INPUT')
        for ref in c['candidate_input_artifact_ids']:
            x=b.artifact(ref);require(x['visibility']=='PUBLIC_DEV' and x['role'] not in ('reference_descriptor','grant','events','calls','observations','raw_metadata'),'CANDIDATE_INPUT_LEAK')
        planned[aid]=(a,c)
    require(bool(planned),'EMPTY_ATTEMPT_INVENTORY');return planned,pins


def ledger(b,policy,planned):
    ev=b.core('events','Events');cl=b.core('calls','Calls');require(ev['run_id']==cl['run_id']==b.run,'LEDGER_RUN')
    events=ev['events'];calls=cl['calls'];require([c['attempt_id'] for c in calls]==list(planned),'CALL_ORDER_OR_INVENTORY');require(len({c['call_id'] for c in calls})==len(calls),'DUPLICATE_CALL')
    ids=set()
    for i,e in enumerate(events):
        require(e['event_sequence']==i and e['event_id'] not in ids,'EVENT_SEQUENCE_OR_DUPLICATE');ids.add(e['event_id'])
        require(e['run_id']==b.run and e['attempt_id'] in planned,'EVENT_IDENTITY');a,_=planned[e['attempt_id']]
        require(e['context_id']==a['context_id'] and e['context_sha256']==a['context_sha256'],'EVENT_CONTEXT');shape(e['event_type'],e['payload'])
        require((e['request_id'] is None)==(e['event_type']=='resource_halt'),'EVENT_REQUEST_ID')
    cursor=0;halted=False;gap=False;issued=set();response_ids=set();counts=gens=0;accepted_rounds=set();unknown=[];known=Counter();subsets={'cached_input_tokens':0,'reasoning_output_tokens':0};usage_missing=[];receipts=[]
    def peek():return events[cursor] if cursor<len(events) else None
    def take(kind,aid):
        nonlocal cursor
        e=peek();require(e is not None and e['event_type']==kind and e['attempt_id']==aid,'EVENT_ORDER_OR_MISSING:'+kind);cursor+=1
        if kind.endswith('_dispatched'):
            require(not halted and not gap,'DISPATCH_AFTER_HALT_OR_GAP');require(e['request_id'] not in issued,'DUPLICATE_REQUEST');issued.add(e['request_id'])
        return e
    def terminal(kind,aid,rid):
        nonlocal gap
        e=peek()
        if e is None or e['attempt_id']!=aid or e['event_type']=='resource_halt':gap=True;return None
        require(e['event_type'] in (kind+'_returned',kind+'_error'),'INTERLEAVED_OR_UNSUPPORTED_EVENT')
        t=take(e['event_type'],aid);require(t['request_id']==rid,'TERMINAL_REQUEST_ID');return t
    for call in calls:
        aid=call['attempt_id'];a,c=planned[aid];require((a['session_id'],a['round_index']) not in accepted_rounds,'ATTEMPT_AFTER_ACCEPTANCE');require((call['status_reason'] is None)==(call['status']=='COMPLETED'),'CALL_STATUS_REASON');require(call['run_id']==b.run and call['context_id']==a['context_id'] and call['context_sha256']==a['context_sha256'],'CALL_CONTEXT')
        if halted:
            require(not call['count_request_issued'] and not call['generation_request_issued'],'REQUEST_FLAGS_AFTER_GLOBAL_HALT')
            require(call['status']=='NOT_RUN' and not call['accepted_response'],'POSTHALT_NOT_RUN_ONLY')
            require(all(call[k] is None for k in ('usage','raw_usage_artifact_id','response_id','response_artifact_id','count_request_id','generation_request_id','count_terminal_event_id','generation_terminal_event_id','input_token_count','returned_model','returned_tier')),'POSTHALT_PAYLOAD')
            require(peek() is None or peek()['event_type']=='resource_halt','EVENT_AFTER_GLOBAL_HALT')
        if gap:require(not call['count_request_issued'] and not call['generation_request_issued'],'REQUEST_AFTER_MISSING_TERMINAL')
        require(call['count_request_issued']==(call['count_request_id'] is not None) and call['generation_request_issued']==(call['generation_request_id'] is not None),'CALL_REQUEST_FLAGS')
        require(not call['generation_request_issued'] or call['count_request_issued'],'GENERATION_WITHOUT_COUNT')
        count=None;count_id=None;count_term=None;gen_term=None
        if call['count_request_issued']:
            counts+=1;require(counts<=policy['count_quota'],'COUNT_QUOTA');e=take('count_dispatched',aid);count_id=e['request_id'];require(count_id==call['count_request_id'],'CALL_COUNT_REQUEST_ID')
            p=e['payload'];require(p['requested_model']==policy['model'] and p['format_schema_sha256']==b.digest('format') and p['messages_sha256']==a['messages_sha256'],'COUNT_MODEL_FORMAT_OR_PROMPT')
            count_term=terminal('count',aid,count_id)
            if count_term and count_term['event_type']=='count_returned':count=count_term['payload']['input_tokens'];require(count>0 and call['input_token_count']==count,'COUNT_VALUE')
            elif count_term:require(call['input_token_count'] is None,'COUNT_ERROR_CLAIMS_COUNT');unknown.append({'attempt_id':aid,'reason':'COUNT_ERROR_FEE_UNKNOWN'})
            else:require(call['input_token_count'] is None,'MISSING_COUNT_TERMINAL');unknown.append({'attempt_id':aid,'reason':'COUNT_TERMINAL_MISSING'})
        else:require(call['input_token_count'] is None,'UNDISPATCHED_COUNT_VALUE')
        require(call['count_terminal_event_id']==(count_term['event_id'] if count_term else None),'CALL_COUNT_TERMINAL_ID')
        if call['generation_request_issued']:
            require(count is not None and count<=policy['input_cap'],'PRECOUNT_MISSING_OR_INPUT_CAP');gens+=1;require(gens<=policy['generation_quota'],'GENERATION_QUOTA')
            e=take('generation_dispatched',aid);require(e['request_id']==call['generation_request_id'],'CALL_GENERATION_REQUEST_ID');p=e['payload']
            require(p['parent_count_request_id']==count_id and p['input_tokens_counted']==count,'PARENT_COUNT')
            require(p['requested_model']==policy['model'] and p['requested_tier']==policy['tier'],'REQUESTED_MODEL_OR_TIER')
            require(p['messages_sha256']==a['messages_sha256'] and p['format_schema_sha256']==b.digest('format'),'GENERATION_PROMPT_OR_FORMAT')
            require(p['max_output_tokens']==policy['output_cap'],'OUTPUT_CAP');reserve=gens*policy['reserve_per_generation_units'];require(p['reserve_units']==policy['reserve_per_generation_units'] and p['cumulative_reserve_units']==reserve and reserve<=policy['generation_reserve_units'],'RESERVE_OR_CAP')
            gen_term=terminal('generation',aid,e['request_id'])
            if gen_term and gen_term['event_type']=='generation_returned':
                p=gen_term['payload'];require(all(call[k]==p[k] for k in ('response_id','returned_model','returned_tier','usage','raw_usage_artifact_id','response_artifact_id')),'CALL_RETURNED_BINDING')
                rid=p['response_id'];require(rid not in response_ids,'DUPLICATE_RESPONSE_ID');response_ids.add(rid)
                if p['returned_model'] is None or p['returned_tier'] is None:unknown.append({'attempt_id':aid,'reason':'RETURNED_MODEL_TIER_UNKNOWN'});require(not call['accepted_response'],'ACCEPTED_UNKNOWN_MODEL_TIER')
                else:require(p['returned_model']==policy['model'] and p['returned_tier']==policy['tier'],'RETURNED_MODEL_OR_TIER')
                if p['response_artifact_id'] is not None:
                    resp=b.obj(p['response_artifact_id'],'Response','response');require(resp['response_id']==rid,'RESPONSE_ARTIFACT_ID')
                else:require(not call['accepted_response'],'ACCEPTED_MISSING_RESPONSE_ARTIFACT');unknown.append({'attempt_id':aid,'reason':'RESPONSE_ARTIFACT_MISSING'})
                u=p['usage']
                if u is None:
                    require(not call['accepted_response'],'ACCEPTED_MISSING_USAGE');usage_missing.append(e['request_id']);subsets={k:None for k in subsets};unknown.append({'attempt_id':aid,'reason':'USAGE_UNKNOWN_NOT_ZERO'})
                else:
                    check_usage(u,policy,count)
                    if p['raw_usage_artifact_id'] is not None:require(b.obj(p['raw_usage_artifact_id'],'RawUsage','usage')['usage']==u,'RAW_USAGE_BINDING')
                    else:unknown.append({'attempt_id':aid,'reason':'RAW_USAGE_MISSING'})
                    known.update({k:u[k] for k in ('input_tokens','output_tokens','total_tokens')})
                    for k in subsets:subsets[k]=None if subsets[k] is None or u[k] is None else subsets[k]+u[k]
            else:
                require(not call['accepted_response'] and all(call[k] is None for k in ('response_id','response_artifact_id','returned_model','returned_tier','usage','raw_usage_artifact_id')),'ERROR_OR_MISSING_TERMINAL_CLAIMS_RETURNED')
                usage_missing.append(e['request_id']);subsets={k:None for k in subsets};unknown.append({'attempt_id':aid,'reason':'GENERATION_ERROR_OR_MISSING_TERMINAL_USAGE_UNKNOWN_NOT_ZERO'})
        else:require(all(call[k] is None for k in ('response_id','response_artifact_id','returned_model','returned_tier','usage','raw_usage_artifact_id')),'UNDISPATCHED_RETURNED_PAYLOAD')
        require(call['generation_terminal_event_id']==(gen_term['event_id'] if gen_term else None),'CALL_GENERATION_TERMINAL_ID')
        while peek() is not None and peek()['attempt_id']==aid and peek()['event_type']=='resource_halt':
            take('resource_halt',aid);halted=True;require(not call['accepted_response'],'ACCEPTED_WITH_HALT')
        if call['accepted_response']:
            require(call['status']=='COMPLETED' and call['response_artifact_id']==a['accepted_response_artifact_id'] and call['response_artifact_id'] is not None,'ACCEPTED_RESPONSE_SNAPSHOT')
            k=(a['session_id'],a['round_index']);require(k not in accepted_rounds,'DUPLICATE_ACCEPTED_ROUND');accepted_rounds.add(k)
        else:require(call['status']!='COMPLETED' and a['accepted_response_artifact_id'] is None,'SUCCESS_STATUS_OR_SNAPSHOT_WITHOUT_ACCEPTANCE')
        if call['status']=='NOT_RUN':require(not call['count_request_issued'] and not call['generation_request_issued'],'NOT_RUN_WITH_REQUEST')
        if call['status']=='INPUT_CAP_NO_GENERATION':require(count is not None and count>policy['input_cap'] and not call['generation_request_issued'],'INPUT_CAP_STATUS')
        receipts.append({'attempt_id':aid,'status':call['status'],'accepted_response':call['accepted_response'],'actual_tokens':call['usage']['total_tokens'] if call['usage'] is not None else None})
    require(cursor==len(events),'ORPHAN_EVENT_OR_POSTHALT_DISPATCH')
    require(gens*policy['reserve_per_generation_units']+policy['count_reserve_units']<=policy['total_reserve_units'],'TOTAL_RESERVE_CAP')
    return {'integrity_status':'UNRESOLVED' if unknown else 'PASS_WITH_SCOPE','gaps':unknown,'halted':halted,'calls':len(calls),'events':len(events),'declared_issuance':{'counts':counts,'generations':gens},'known_token_subtotal':dict(known),'subset_totals':subsets if gens else {k:None for k in subsets},'usage_missing_requests':usage_missing,'attempts':receipts}


def observations(b,pins):
    doc=b.core('observations','Observations');require(doc['run_id']==b.run,'OBSERVATION_RUN');seen=set();unknown=False
    for o in doc['observations']:
        require(o['observation_id'] not in seen,'DUPLICATE_OBSERVATION');seen.add(o['observation_id'])
        require(b.artifact(o['source_artifact_id'],'source')['sha256']==o['source_sha256'],'OBS_SOURCE_SHA')
        require(b.artifact(o['raw_metadata_artifact_id'],'raw_metadata')['sha256']==o['raw_metadata_sha256'],'OBS_RAW_METADATA_SHA')
        require(o['pin_contract_sha256']==b.digest('pins') and all(o[k]==pins[k] for k in ('clock_domain','edge','reset_polarity','reset_kind','phase_contract')),'OBS_PHASE_RESET_OR_PINS')
        require(o['slot']<o['declared_vector_width']<=pins['slot_count'],'OBS_SLOT_WIDTH')
        require((o['checker_artifact_id'] is None)==(o['checker_sha256'] is None),'OBS_CHECKER_NULLABILITY')
        if o['checker_artifact_id'] is not None:require(b.artifact(o['checker_artifact_id'],'reference_descriptor')['sha256']==o['checker_sha256'],'OBS_CHECKER_SHA')
        require((o['reference_last_cycle'] is None)==(o['reference_last_phase'] is None),'REFERENCE_BOUNDARY_NULLABILITY')
        if o['reference_last_cycle'] is not None:require(o['phase']=='pre' and o['cycle']>0 and o['reference_last_cycle']==o['cycle']-1 and o['reference_last_phase']=='post','REFERENCE_PREFIX_BOUNDARY')
        unknown|=o['selected_knownness']=='UNKNOWN'
    return {'metadata_observations':len(doc['observations']),'selected_unknown_declared':unknown,'raw_parser_status':'OUT_OF_SCOPE_NOT_IMPLEMENTED','reference_evaluation':'NOT_EVALUATED'}


def validate_bundle(root):
    started=time.perf_counter();r=None
    try:
        r=Reader(root);b=Bundle(r);policy=b.core('registration','Policy');grant=b.core('grant','Grant')
        require(policy['run_id']==grant['run_id']==b.run and policy['registration_id']==grant['registration_id']==b.manifest['registration_id'],'REGISTRATION_GRANT_ID')
        require(grant['registration_sha256']==b.digest('registration'),'GRANT_REGISTRATION_SHA')
        planned,pins=attempts_and_contexts(b,policy);result=ledger(b,policy,planned);obs=observations(b,pins);b.release();integrity={'status':result['integrity_status'],'scope':'G0_V1_STRICT_SERIAL_SYNTHETIC_METADATA_BINDINGS_ONLY','reasons':result['gaps']}
        costs={'scope':'DECLARED_SYNTHETIC_RECORDS_NOT_PROVIDER_AUTHENTICATED','tokens':{'knownness':'UNKNOWN' if result['usage_missing_requests'] else 'KNOWN_SUBTOTAL_ONLY' if result['declared_issuance']['generations'] else 'NOT_APPLICABLE_NO_GENERATION','value':None if result['usage_missing_requests'] else result['known_token_subtotal'] or None,'known_subtotal':result['known_token_subtotal'],'missing_requests':result['usage_missing_requests'],'subsets':result['subset_totals']},'requests':result['declared_issuance'],'count_fee':{'knownness':'UNKNOWN','value':None},'provider_invoice':{'knownness':'UNKNOWN','value':None},'native_physical_replay':{'knownness':'NOT_EVALUATED','value':None}}
    except (Reject,ValueError,KeyError,TypeError,OSError,RecursionError) as error:
        integrity={'status':'REJECT','scope':'G0_V1_STRICT_SERIAL_SYNTHETIC_METADATA_BINDINGS_ONLY','reasons':[str(error)],'error_type':type(error).__name__};result={};obs={};costs={'knownness':'UNKNOWN','value':None,'provider_invoice':None,'count_fee':None}
    return {'schema_name':'g0.adapter_result','schema_version':1,'adapter_source_sha256':sha(Path(__file__).read_bytes()),'schema_sha256':sha(SCHEMA_BYTES),'integrity':integrity,'scientific_attribution':{'status':'NOT_EVALUATED','raw_parsers_implemented':False,'independent_labels_available':False,'oracle_executed':False,'DUT_or_monitor_correctness_proved':False,'selected_alarm_confirmed':False,'completion128_proved':False},'cost_knownness':costs,'ledger':result,'observations':obs,'input_sha256':r.hashes if r else {},'input_bytes_read':r.total_bytes if r else 0,'parse_seconds':time.perf_counter()-started,'execution_capabilities':{'API':False,'native':False,'monitor':False,'credentials':False,'dispatch':False},'authorization_assessment':'OFFLINE_SYNTHETIC_CLAIM_BINDING_ONLY_NOT_A_LIVE_GRANT'}


def publish(out,result,allowed_parent):
    """Exclusive local report publication; untrusted bundles cannot choose paths."""
    out=Path(out).absolute();parent=Path(allowed_parent).resolve();require(out.parent.resolve()==parent and out.name.startswith('g0-'),'OUTPUT_NAMESPACE')
    require(not out.is_symlink() and not out.exists(),'OUTPUT_EXISTS_OR_SYMLINK')
    require(not Path(allowed_parent).is_symlink(),'OUTPUT_PARENT_SYMLINK')
    out.mkdir(exist_ok=False)
    with (out/'result.json').open('x') as stream:stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    return out/'result.json'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    out=a.out.absolute();relative=out.resolve().relative_to(REPO/'test2/results');require(relative.parts[0].startswith('g0-'),'OUTPUT_NAMESPACE')
    result=validate_bundle(a.bundle);path=publish(out,result,out.parent);print(json.dumps({'status':result['integrity']['status'],'result':str(path)}));return 1 if result['integrity']['status']=='REJECT' else 2 if result['integrity']['status']=='UNRESOLVED' else 0


if __name__=='__main__':raise SystemExit(main())
