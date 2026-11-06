"""Small exact-profile and P16 gates;no execution."""
from collections import Counter
from observations import need
from allocation import CUMULATIVE_CAPS,DECISION_SHA,POOL_SHA

def registration_contract(root,reg,grant,plan):
    need(reg['caps']==CUMULATIVE_CAPS and reg['native_depth']==8,'PROFILE_CAPS')
    jobs=plan['jobs'];need(len({j['id'] for j in jobs})==72,'JOB_COUNT_OR_DUPLICATE')
    need(Counter(j['kind'] for j in jobs)==dict(compile=14,native=28,physical=30),'PLAN_COUNTS')
    need(sum(j.get('cycles',0) for j in jobs)==120,'CYCLE_COUNT')
    need(not any(j['kind']=='setup' or j.get('qc')=='QC00' or j['id'] in ['QC01-bmc','QC01-cover','compile-QC01'] for j in jobs),'REUSED_JOB_REEXECUTION')
    for i in range(1,16):
        cid=f'QC{i:02}';native=[j for j in jobs if j.get('qc')==cid and j['kind']=='native'];physical=[j for j in jobs if j.get('qc')==cid and j['kind']=='physical']
        need([j['mode'] for j in native]==([] if i==1 else ['bmc','cover']),'NATIVE_ORDER')
        need([j['simulator'] for j in physical]==['icarus','verilator'] and all(j['cycles']==4 for j in physical),'PHYSICAL_PROFILE')
        need(all(j['argv'][j['argv'].index('-t')+1]=='8' for j in native),'NATIVE_DEPTH')
    need(all(reg[k] is False for k in ['API','count','generation','key_access','network','installation','G2_G3_G4_G5']),'FORBIDDEN_SCOPE')

def gate_contract(gate,review,identities):
    need(gate.get('record_kind')=='G1_EXECUTE_R05B_AFTER_P16' and gate.get('stage')=='EXECUTE','WRONG_EXECUTE')
    need(review.get('phase','').startswith('P16') and review.get('status') in ['PASS','PASS_WITH_LIMITS'],'P16_ACCEPTANCE_REQUIRED')
    need(gate.get('continuation_decision_sha256')==DECISION_SHA and gate.get('predecessor_pool_sha256')==POOL_SHA,'AUTHORITY_OR_POOL')
    for key,value in identities.items():need(gate.get(key)==value,'GATE_IDENTITY_DRIFT:'+key)
    for key in ['producer_manifest_sha256','registration_sha256','source_manifest_sha256','continuation_decision_sha256','reuse_manifest_sha256','budget_amendment_sha256']:
        target='preparation_manifest_sha256' if key=='producer_manifest_sha256' else key
        need(review.get('input_identity',{}).get(key)==gate.get(target) and gate.get(target) is not None,'P16_BINDING_DRIFT:'+key)
