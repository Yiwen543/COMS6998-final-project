"""Conditional R04 allocation. Proposed physical33 is never its own authority."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import re

GRANT_SHA='bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab'
FIRST_POOL_SHA='6da4346144d65356f57c5762058675f1acca9f1dad4ee8599c889dc49e1a7400'
POOL_SHA='1bfe56363ae08fd288be7050fff2ddb05ae7af7eb537e357273222a81483c15e'
PHASE_SHA='3750f51dc2c5825ba2f386a633dd7e480f303ab06f312f7f940462c450b9c190'
REVIEW_SHA='2fcee5eb22542449744ba43a8967efd11adb0bcda29afda10b9f64a3fd37ab29'
PRIOR={'compile':3,'native':2,'physical':1,'physical_cycles':4,'setup':8}
PRIOR_ACTUAL=5.197697583120316
PRIOR_CHARGED=7.151973249856383
# This constant is a proposed ceiling. Only load_allocation after actual approval
# and the independent gate may authorize a Budget using it.
CUMULATIVE_CAPS=dict(compile_jobs=32,native_jobs=32,physical_jobs=33,
    physical_cycles=1024,cycles_per_run=32,wall_seconds=1200,setup_jobs=8,
    compile_timeout=20,native_timeout=10,physical_timeout=2,setup_timeout=2)
ORIGINAL_CAPS=dict(CUMULATIVE_CAPS,physical_jobs=32)

class AllocationError(ValueError): pass

def check(ok,reason):
    if not ok: raise AllocationError(reason)

def digest(path):
    path=Path(path)
    check(path.is_file() and not path.is_symlink(),'MISSING_OR_SYMLINK_AUTHORITY:'+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def exact_hash(value): return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None

@dataclass(frozen=True)
class Allocation:
    prior_reserved: tuple
    prior_actual_seconds: float
    prior_charge_seconds: int
    attempt_window_seconds: int
    predecessor_bindings: tuple
    inventory_predecessor_error: str
    def validate(self):
        check(dict(self.prior_reserved)==PRIOR and all(type(v) is int for _,v in self.prior_reserved),'FALSE_PRIOR_COUNTS')
        check(type(self.prior_actual_seconds) is float and self.prior_actual_seconds==PRIOR_ACTUAL,'FALSE_PRIOR_ACTUAL')
        check(type(self.prior_charge_seconds) is int and self.prior_charge_seconds==8,'FALSE_PRIOR_CHARGE')
        check(type(self.attempt_window_seconds) is int and self.attempt_window_seconds==1192,'EXPANDED_WINDOW')
        b=dict(self.predecessor_bindings)
        expected={'grant':GRANT_SHA,'first_pool':FIRST_POOL_SHA,'pool':POOL_SHA,'phase':PHASE_SHA,'review':REVIEW_SHA}
        check(all(b.get(k)==v for k,v in expected.items()),'PREDECESSOR_BINDINGS')
        check(all(exact_hash(b.get(k)) for k in ['decision','amendment']),'MISSING_APPROVAL_BINDINGS')
        check('PermissionError' in self.inventory_predecessor_error and '/bin/ps' in self.inventory_predecessor_error,'INVENTORY_PREDECESSOR')

def load_allocation(root,reg,gate):
    root=Path(root)
    # Missing/unapproved decisions fail before any new lock,ledger or tool.
    for key in ['continuation_decision','budget_amendment']:
        value=gate.get(key+'_sha256')
        check(exact_hash(value),'MISSING_APPROVED_'+key.upper()+'_HASH')
        check(digest(root/reg[key])==value,'AUTHORITY_HASH_DRIFT:'+key)
    amendment=json.loads((root/reg['budget_amendment']).read_text())
    check(amendment.get('record_kind')=='G1_CUMULATIVE_PHYSICAL_CAP_AMENDMENT' and
          amendment.get('user_approved') is True,'PHYSICAL33_NOT_USER_APPROVED')
    check(amendment.get('original_user_authorization_sha256')==GRANT_SHA and
          amendment.get('original_physical_jobs')==32 and type(amendment.get('cumulative_physical_jobs')) is int and
          amendment['cumulative_physical_jobs']==33,'WRONG_PHYSICAL_AMENDMENT')
    check(amendment.get('other_caps_unchanged') is True and amendment.get('permission_change_authorized') is False,
          'AMENDMENT_SCOPE_EXPANDED')
    check(type(amendment.get('user_approval_evidence')) is str and bool(amendment['user_approval_evidence'].strip()),
          'MISSING_USER_APPROVAL_EVIDENCE')
    decision=json.loads((root/reg['continuation_decision']).read_text())
    check(decision.get('record_kind')=='G1_AUTHORIZED_R04_CUMULATIVE_CONTINUATION' and
          decision.get('status')=='AUTHORIZED','CONTINUATION_NOT_AUTHORIZED')
    check(decision.get('budget_amendment_sha256')==gate['budget_amendment_sha256'],'AMENDMENT_NOT_BOUND')
    fixed=[('user_authorization','user_authorization_sha256',GRANT_SHA),
           ('first_pool','first_pool_sha256',FIRST_POOL_SHA),('predecessor_pool','predecessor_pool_sha256',POOL_SHA),
           ('predecessor_phase','predecessor_phase_sha256',PHASE_SHA),('predecessor_review','predecessor_review_sha256',REVIEW_SHA)]
    for path_key,sha_key,expected in fixed:
        check(reg.get(sha_key)==expected and digest(root/reg[path_key])==expected,'PREDECESSOR_DRIFT:'+path_key)
        check(decision.get(sha_key)==expected,'DECISION_LINEAGE:'+sha_key)
    old=json.loads((root/reg['predecessor_pool']).read_text());first=json.loads((root/reg['first_pool']).read_text())
    check(old['halted'] is True and old['completed'] is True and first['halted'] is True and first['completed'] is True,'CLOSED_PREDECESSORS_REQUIRED')
    check(old['reserved']==reg['prior_reserved']==decision.get('prior_reserved')==PRIOR,'FALSE_PRIOR_COUNTS')
    check(all(type(v) is int for v in reg['prior_reserved'].values()),'PRIOR_COUNT_TYPES')
    check(old['cumulative_actual_window_seconds']==reg['prior_actual_window_seconds']==decision.get('prior_actual_window_seconds')==PRIOR_ACTUAL,'PRIOR_ACTUAL_DRIFT')
    check(old['cumulative_charged_window_seconds']==reg['prior_charged_checkpoint_seconds']==decision.get('prior_charged_checkpoint_seconds')==PRIOR_CHARGED,'PRIOR_CHARGE_CHECKPOINT_DRIFT')
    check(type(decision.get('prior_wall_charge_seconds')) is int and decision['prior_wall_charge_seconds']==reg['prior_wall_charge_seconds']==8,'PRIOR_CHARGE_MUST_BE8_NOT_SPEND')
    check(type(decision.get('attempt_maximum_window_seconds')) is int and decision['attempt_maximum_window_seconds']==reg['attempt_maximum_window_seconds']==1192,'EXPANDED_WINDOW')
    check(reg['original_caps']==ORIGINAL_CAPS and reg['caps']==decision.get('cumulative_caps')==CUMULATIVE_CAPS,'CAPS_DRIFT')
    remaining={k+'_jobs':CUMULATIVE_CAPS[k+'_jobs']-PRIOR[k] for k in ['compile','native','physical','setup']}
    remaining.update(physical_cycles=1020,execution_wall_seconds=1192)
    check(reg['remaining_allocation']==decision.get('remaining_allocation')==remaining,'REMAINING_DRIFT')
    check(reg['native_depth']==decision.get('native_depth')==8 and decision.get('permission_change_authorized') is False,'DEPTH_OR_PERMISSION')
    check(reg['process_supervision']=='owned_process_group_only','SUPERVISION_DRIFT')
    check(reg['pool_state']==reg['result_root']+'/execution-state.json' and reg['pool_state'] not in [reg['predecessor_pool'],reg['first_pool']],'MUST_NOT_REOPEN_PREDECESSORS')
    b={'grant':GRANT_SHA,'first_pool':FIRST_POOL_SHA,'pool':POOL_SHA,'phase':PHASE_SHA,'review':REVIEW_SHA,
       'decision':gate['continuation_decision_sha256'],'amendment':gate['budget_amendment_sha256']}
    allocation=Allocation(tuple(sorted(PRIOR.items())),PRIOR_ACTUAL,8,1192,tuple(sorted(b.items())),first['events'][0]['error'])
    allocation.validate();return allocation
