"""R02 metadata-gate-only probes. Never call runner.main/Budget/tool launcher."""
from pathlib import Path
import sys,json,hashlib,shutil,copy
P=Path(__file__).resolve().parent;BASE=P/'exec_tree';sys.path.insert(0,str(BASE/'test2/g1_v2'))
import runner
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
O=P/'gate-probes';O.mkdir(exist_ok=False)
PROD=P.parent.parent/'producer_test2_g1_R02_2026-11-05'
SM=json.loads((BASE/'test2/g1_v2/source-manifest.json').read_text())
# Supply only additional exact hash-bound metadata absent from snapshot layout.
for n,h in SM['files'].items():
    dest=BASE/n
    if not dest.exists():
        actual=(PROD/n[len(str(PROD)) + 1:]) if n.startswith(str(PROD)+'/') else Path(n)
        # PROD is absolute but stored source names are repo-relative.
        if not actual.is_file():actual=Path.cwd()/n
        assert actual.is_file() and H(actual)==h,(n,actual)
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(actual,dest)
    assert H(dest)==h
prep='docs/audits/producer_test2_g1_R02_2026-11-05/snapshot-manifest.json'
dest=BASE/prep;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROD/'snapshot-manifest.json',dest)
old=json.loads((BASE/'docs/audits/agent_bridge_2026-11-06/P10_g1_registration/review.json').read_text())
rows=[]
def put(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def run(name,mutation=None,expected='REJECT',reason=None):
    d=O/name;d.mkdir();root=d/'tree';shutil.copytree(BASE,root,symlinks=True)
    regpath=root/'test2/configs/g1_qualification_registration_v2.json';reg=json.loads(regpath.read_text())
    reviewrel='docs/audits/agent_bridge_2026-11-06/P10B_METADATA_PROBE/review.json'
    review={'phase':'P10B_SYNTHETIC_METADATA_GATE_PROBE_NOT_REAL_ACCEPTANCE','status':'PASS_WITH_LIMITS','input_identity':{'producer_manifest_sha256':H(root/prep),'registration_sha256':H(regpath)},'origin':'REVIEW_OWNED_METADATA_FIXTURE_NEVER_AN_ACTUAL_EXECUTE_RECEIPT'}
    put(root/reviewrel,review)
    gate={'record_kind':'G1_EXECUTE_AFTER_READONLY_P10','stage':'EXECUTE','registration_sha256':H(regpath),'source_manifest_sha256':H(root/reg['source_manifest']),'user_authorization_sha256':H(root/reg['user_authorization']),'p10_review_path':reviewrel,'p10_review_sha256':H(root/reviewrel),'preparation_manifest_sha256':H(root/prep),'origin':'PURE_METADATA_GATE_PROBE_NOT_ACTUAL_AUTHORIZATION'}
    if mutation:mutation(root,reg,review,gate,reviewrel)
    receipt=d/'metadata-fixture-receipt.json';put(receipt,gate)
    deps={n:H(root/n) for n in SM['files']};deps[prep]=H(root/prep);deps[reviewrel]=H(root/reviewrel)
    put(d/'input-bindings-before.json',{'files':deps,'receipt_sha256':H(receipt),'executed_runner_source_sha256':H(BASE/'test2/g1_v2/runner.py'),'ROOT_override':str(root),'REGISTRATION_override':str(regpath)})
    runner.ROOT=root;runner.REGISTRATION=regpath
    actual='ACCEPT_METADATA_ONLY';error=None
    try:runner.review_gate(receipt)
    except Exception as e:actual='REJECT';error=type(e).__name__+':'+str(e)
    assert all(H(root/n)==h for n,h in deps.items())
    x={'case':name,'expected':expected,'actual':actual,'error':error,'expectation_met':actual==expected and (reason is None or reason in (error or '')),'input_bindings_sha256':H(d/'input-bindings-before.json'),'real_tool_main_or_pool_calls':0}
    put(d/'result.json',x);rows.append(x);print(name,actual,error)
run('exact-R02-binding',expected='ACCEPT_METADATA_ONLY')
def old_decision(root,reg,review,gate,rel):
    gate['p10_review_path']='docs/audits/agent_bridge_2026-11-06/P10_g1_registration/review.json';gate['p10_review_sha256']=H(root/gate['p10_review_path'])
run('original-P10-CHANGES_REQUIRED',old_decision,reason='P10_NOT_ACCEPTED')
run('old-R01-preparation',lambda root,reg,review,gate,rel:gate.update(preparation_manifest_sha256='ba96cf663df3a7aa7cef9ca43d660e80bdefe09a9482178bd8fe6a198f5c12c7'),reason='PREPARATION_MANIFEST_DRIFT')
run('old-v1-registration',lambda root,reg,review,gate,rel:gate.update(registration_sha256='8feb9918911177827b53bc9669d1faaad68bfb75af3380ce019df4a80ca174ba'),reason='REGISTRATION_DRIFT')
def old_accepted_identity(root,reg,review,gate,rel):
    review['input_identity']['producer_manifest_sha256']='ba96cf663df3a7aa7cef9ca43d660e80bdefe09a9482178bd8fe6a198f5c12c7';put(root/rel,review);gate['p10_review_sha256']=H(root/rel)
run('old-identity-even-with-PASS-label',old_accepted_identity,reason='P10_REVIEW_WRONG_PREPARATION')
def drift_source(root,reg,review,gate,rel):
    p=root/'test2/g1_v2/runtime.py';p.write_bytes(p.read_bytes()+b'\n# ONLY REVIEW FIXTURE DRIFT\n')
run('source-hash-drift',drift_source,reason='FROZEN_INPUT_DRIFT')
run('grant-hash-drift',lambda root,reg,review,gate,rel:gate.update(user_authorization_sha256='0'*64),reason='GRANT_DRIFT')
def drift_review(root,reg,review,gate,rel):review['note']='REVIEW FIXTURE DRIFT';put(root/rel,review)
run('review-hash-drift',drift_review,reason='P10_REVIEW_DRIFT')
def old_key(root,reg,review,gate,rel):gate['r01_manifest_sha256']=gate.pop('preparation_manifest_sha256')
run('legacy-receipt-key-only',old_key,reason='preparation_manifest_sha256')
put(O/'summary.json',{'scope':'Pure metadata gate checks with review-owned copied ROOT overrides;no actual approval/EXECUTE receipt or main invocation','cases':rows,'count':len(rows),'failed_expectations':[x['case'] for x in rows if not x['expectation_met']],'real_tool_calls':0})
assert all(x['expectation_met'] for x in rows)

