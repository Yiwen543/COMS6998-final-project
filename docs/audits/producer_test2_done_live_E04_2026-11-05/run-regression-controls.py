"""Persist pure in-memory P04-R1 regression inputs and observed outcomes."""
from pathlib import Path
import sys,json,copy,hashlib
R=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(R/'test2/tests'),str(R/'test2/scripts')]
import test_controller_done_ledger_audit_v2 as f
import test_controller_done_ledger_audit_v1 as base
from controller_done_ledger_audit_v2 import validate_ledger
from controller_done_ledger_audit_v1 import validate_ledger as old
A=Path(__file__).parent
rows=[]
def serialized(data):
    calls,events,snaps,policy,schema=copy.deepcopy(data)
    return dict(calls=calls,events=events,snapshots=[dict(key=list(k),value=v) for k,v in snaps.items()],policy=policy,schema_digest=schema)
def outcome(fn,data):
    try:return fn(*copy.deepcopy(data))
    except ValueError as e:return dict(status='REJECT',reason=str(e))
def run(name,data,expected,compare=False):
    result=outcome(validate_ledger,data);assert result['status']==expected,(name,result)
    if name.startswith('missing_usage'):assert result['attempts'][0]['actual_tokens'] is None and result['known_usage_token_totals']=={}
    row=dict(name=name,expected=expected,observed=result,fixture=serialized(data))
    if compare:row['old_v1_observed']=outcome(old,data)
    rows.append(row)
run('exact_saved_P04_fixture',f.reviewer_fixture(False),'REJECT',True)
run('same_round_retry_after_halt_binding_corrected_copy',f.reviewer_fixture(),'REJECT',True)
for field,value in [('round',2),('session_id','another-session'),('arm','C')]:
    data=list(f.reviewer_fixture());calls,events,snaps,policy,schema=data;c=calls[1];c[field]=value;c['attempt']=1;ctx=events[5]['context'];ctx[field]=value
    if field=='session_id':c['repetition']=ctx['repetition']=2
    snaps[('B',1,1)]['response']=None;key=(c['arm'],c['repetition'],c['round']);snaps[key]=dict(snaps[('B',1,1)],**{k:c[k] for k in ('arm','repetition','round','session_id')});snaps[key]['response']=copy.deepcopy(c['parsed']);run('posthalt_cross_'+field,data,'REJECT',True)
for flag in ['count_request_issued','generation_request_issued']:
    data=f.not_run();data[0][1][flag]=True;run('posthalt_flag_'+flag,data,'REJECT')
for event in ['count_dispatched','generation_dispatched']:
    data=f.not_run();data[1].append(dict(event=event));run('posthalt_event_'+event,data,'REJECT')
run('legal_halt_then_only_NOT_RUN',f.not_run(),'PASS',True)
calls,events,snaps,policy=base.fixture();c=calls[0];c.update(status='request_or_infrastructure_error',accepted_response=False,error_type='TimeoutError');snaps[('B',1,1)]['response']=None
for k in ['usage','raw_usage','response_id','parsed']:c.pop(k)
events[3]=dict(event='generation_error',error_type='TimeoutError',usage_status='UNKNOWN_NOT_ZERO');events.append(dict(event='resource_halt',reason='explicit halt after transport error'))
later=copy.deepcopy(c);later.update(attempt=2,status='not_run_resource_halt',count_request_issued=False,generation_request_issued=False);calls.append(later)
run('missing_usage_halt_then_NOT_RUN',(calls,events,snaps,policy,'schema'),'UNRESOLVED')
report=dict(scope='Synthetic saved-ledger fixtures and pure functions only; no API or scientific experiment.',status='PASS',new_source_sha256=hashlib.sha256((R/'test2/scripts/controller_done_ledger_audit_v2.py').read_bytes()).hexdigest(),P04_fixture_authority_sha256=f.AUTHORITY_SHA,controls=rows,reviewer_fixture_discrepancy='Exact saved original rejects in v1 on response binding; only a copied snapshot response is repaired to demonstrate genuine v1 halt false PASS. No original evidence changed.')
p=A/'regression-controls.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(len(rows),'controls verified; counterexamples REJECT, legal NOT_RUN PASS, missing usage UNRESOLVED/null.')
