"""Narrow R04 plan/reuse and P14+budget gates. No execution here."""
from collections import Counter
from observations import need
from allocation import ORIGINAL_CAPS,CUMULATIVE_CAPS,POOL_SHA

def registration_contract(root,reg,grant,plan):
    need(reg['original_caps']==ORIGINAL_CAPS and reg['caps']==CUMULATIVE_CAPS,'PROPOSED_CAPS_DRIFT')
    need(grant['caps']['physical_simulator_runs_total']==32,'ORIGINAL_GRANT_IS32')
    need(reg['profile']=='G1_PUBLIC_SINGLE_PROFILE_V1' and reg['native_depth']==8,'PROFILE_DEPTH')
    jobs=plan['jobs'];need(len({j['id'] for j in jobs})==len(jobs),'DUPLICATE_JOB')
    need(Counter(j['kind'] for j in jobs)=={'compile':17,'native':30,'physical':32},'R04_PLAN_COUNTS')
    need(not any(j['kind']=='setup' or j['id'] in ['compile-QC00','QC00-bmc','QC00-cover'] for j in jobs),'NO_SETUP_OR_REEXECUTED_PREFIX')
    need(sum(j.get('cycles',0) for j in jobs)==128,'PHYSICAL_CYCLES')
    for n in range(16):
        cid=f'QC{n:02}'
        native=[j for j in jobs if j.get('qc')==cid and j['kind']=='native']
        physical=[j for j in jobs if j.get('qc')==cid and j['kind']=='physical']
        need([j['mode'] for j in native]==([] if n==0 else ['bmc','cover']),'NATIVE_PREFIX_REUSE_ONLY')
        need([j['simulator'] for j in physical]==['icarus','verilator'],'DUAL_SIM')
        need(all(j['argv'][j['argv'].index('-t')+1]=='8' for j in native),'DEPTH8')
        need(all(j['cycles']==4 for j in physical),'FOUR_CYCLES')
    need(all(reg[k] is False for k in ['API','count','generation','key_access','network','installation','G2_G3_G4_G5']),'FORBIDDEN_SCOPE')

def gate_contract(gate,review,identities):
    need(gate.get('record_kind')=='G1_EXECUTE_R04_AFTER_P14_AND_PHYSICAL33_APPROVAL' and gate.get('stage')=='EXECUTE','OLD_OR_WRONG_EXECUTE')
    need(review.get('phase','').startswith('P14') and review.get('status') in ['PASS','PASS_WITH_LIMITS'],'P14_ACCEPTANCE_REQUIRED')
    for key,value in identities.items():need(gate.get(key)==value,'GATE_IDENTITY_DRIFT:'+key)
    need(gate.get('predecessor_pool_sha256')==POOL_SHA,'WRONG_E02_POOL')
    for key in ['producer_manifest_sha256','registration_sha256','continuation_decision_sha256','budget_amendment_sha256']:
        target='preparation_manifest_sha256' if key=='producer_manifest_sha256' else key
        need(review.get('input_identity',{}).get(key)==gate.get(target) and gate.get(target) is not None,'P14_INPUT_DRIFT:'+key)
