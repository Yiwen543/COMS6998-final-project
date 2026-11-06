"""Persist non-authorizing fixture envelopes before every pure predicate probe."""
from pathlib import Path
import copy,hashlib,json,sys
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
CODE=OWN/'integration-evidence/executed-source'
sys.path[:0]=[str(CODE/'test2/g1_v5b'),str(CODE/'test2/g1_v5')]
from contracts import gate_contract
from native_results import judge_native
from observations import Unqualified
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
reg=read(ROOT/'docs/audits/producer_test2_g1_R05B_2026-11-06/snapshot/test2/configs/g1_qualification_registration_v5b.json')
ids=dict(registration_sha256=sha(ROOT/'test2/configs/g1_qualification_registration_v5b.json'),source_manifest_sha256=sha(ROOT/reg['source_manifest']),preparation_manifest_sha256=sha(ROOT/reg['preparation_snapshot_manifest']),continuation_decision_sha256=reg['continuation_decision_sha256'],predecessor_pool_sha256=reg['predecessor_pool_sha256'],reuse_manifest_sha256=sha(ROOT/reg['reuse_manifest']),user_authorization_sha256=reg['user_authorization_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256'])
g=dict(record_kind='G1_EXECUTE_R05B_AFTER_P16',stage='EXECUTE',**ids)
r=dict(phase='P16_SYNTHETIC_UNIT_INPUT_NOT_A_REVIEW',status='PASS_WITH_LIMITS',input_identity={('producer_manifest_sha256' if k=='preparation_manifest_sha256' else k):v for k,v in ids.items()})
cases=[dict(name='matching_exact_gate',gate=g,review=r,identities=ids,expect='ACCEPT_PREDICATE_ONLY')]
for key in ['producer_manifest_sha256','registration_sha256','source_manifest_sha256','continuation_decision_sha256','reuse_manifest_sha256','budget_amendment_sha256']:
    bad=copy.deepcopy(r);bad['input_identity'][key]='0'*64
    cases.append(dict(name='drift_'+key,gate=g,review=bad,identities=ids,expect='P16_BINDING_DRIFT'))
cases.append(dict(name='missing_review',gate=g,review={},identities=ids,expect='P16_ACCEPTANCE_REQUIRED'))
for intent in read(ROOT/reg['interpretation'])['cases']:
    for mode in ['bmc','cover']:cases.append(dict(name=intent['id']+'_unknown_'+mode,intent=intent,mode=mode,evidence={'evidence_complete':False,'issues':['FROZEN_UNKNOWN']},expect='NATIVE_EVIDENCE_UNKNOWN'))
out=OWN/'frozen-predicate-probes';out.mkdir()
for c in cases:write(out/(c['name']+'.input.json'),{'fixture_only_not_review_or_EXECUTE':True,'case':c})
hashes={p.name:sha(p) for p in out.glob('*.input.json')};write(out/'inputs-before.json',hashes)
results=[]
for name,h in hashes.items():
    p=out/name;assert sha(p)==h;c=read(p)['case']
    try:
        if 'gate' in c:gate_contract(c['gate'],c['review'],c['identities'])
        else:judge_native(c['evidence'],c['mode'],c['intent'])
        actual='ACCEPT_PREDICATE_ONLY'
    except Unqualified as e:actual=str(e)
    assert c['expect'] in actual,(name,actual)
    results.append(dict(input=name,input_sha256=h,actual=actual,expected=c['expect']))
assert all(sha(out/n)==h for n,h in hashes.items())
write(out/'results.json',dict(tests=len(results),passed=len(results),results=results,real_tools=0,executed_source_manifest_sha256=sha(OWN/'integration-evidence/executed-source-sha256.json')))
print(json.dumps(dict(tests=len(results),passed=len(results),real_tools=0)))
