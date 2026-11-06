"""Exact R05 allocation;does not authorize execution or reset closed pools."""
from dataclasses import dataclass
from pathlib import Path
import hashlib,json
GRANT_SHA='bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab'
DECISION_SHA='ab841825fd80610bbf1f822a8baf276fc1dbce5b710cabd11effc70c44b23a8f'
POOL_SHA='2364e80999aaea35eb3e5da06e31d48331ee6be6b061c09bb3f92738bca8d1b8'
PRIOR=dict(compile=6,native=4,physical=3,physical_cycles=12,setup=8)
ACTUAL=11.770645541138947;CHARGED=14.572948167100549
CUMULATIVE_CAPS=dict(compile_jobs=32,native_jobs=32,physical_jobs=33,physical_cycles=1024,cycles_per_run=32,wall_seconds=1200,setup_jobs=8,compile_timeout=20,native_timeout=10,physical_timeout=2,setup_timeout=2)
class AllocationError(ValueError):pass
def check(ok,reason):
    if not ok:raise AllocationError(reason)
def digest(path):
    path=Path(path);check(path.is_file() and not path.is_symlink(),'MISSING_AUTHORITY:'+str(path));return hashlib.sha256(path.read_bytes()).hexdigest()
@dataclass(frozen=True)
class Allocation:
    prior_reserved:tuple
    prior_actual_seconds:float
    prior_charge_seconds:int
    attempt_window_seconds:int
    predecessor_bindings:tuple
    inventory_predecessor_error:str
    def validate(self):
        check(dict(self.prior_reserved)==PRIOR and all(type(v) is int for _,v in self.prior_reserved),'PRIOR_COUNT_DRIFT')
        check(type(self.prior_actual_seconds) is float and self.prior_actual_seconds==ACTUAL,'PRIOR_ACTUAL_DRIFT')
        check(type(self.prior_charge_seconds) is int and self.prior_charge_seconds==15,'PRIOR_CHARGE_DRIFT')
        check(type(self.attempt_window_seconds) is int and self.attempt_window_seconds==1185,'WINDOW_DRIFT')
        b=dict(self.predecessor_bindings);check(b.get('decision')==DECISION_SHA and b.get('pool')==POOL_SHA,'BINDING_DRIFT')
        check('/bin/ps' in self.inventory_predecessor_error and 'PermissionError' in self.inventory_predecessor_error,'PREDECESSOR_INVENTORY')
def load_allocation(root,reg,gate):
    root=Path(root)
    check(gate.get('continuation_decision_sha256')==reg.get('continuation_decision_sha256')==DECISION_SHA,'MISSING_OR_WRONG_R05_DECISION')
    check(digest(root/reg['continuation_decision'])==DECISION_SHA,'AUTHORITY_DRIFT')
    d=json.loads((root/reg['continuation_decision']).read_text())
    check(d.get('record_kind')=='G1_AUTHORIZED_R05_CUMULATIVE_CONTINUATION' and d.get('status')=='AUTHORIZED' and d.get('not_EXECUTE') is True,'WRONG_DECISION')
    for key in ['user_authorization','user_physical33_authorization','budget_amendment','first_pool','E02_pool','predecessor_pool','predecessor_phase','predecessor_manifest','predecessor_review']:
        h=key+'_sha256';check(reg[h]==d[h] and digest(root/reg[key])==d[h],'LINEAGE_DRIFT:'+key)
    check(d['user_authorization_sha256']==GRANT_SHA and d['predecessor_pool_sha256']==POOL_SHA,'ORIGINAL_GRANT_OR_POOL')
    check(d['permission_change_authorized'] is False and d['other_caps_unchanged'] is True and d['cross_IP_allowed'] is False and d['new_API_paid_keys_network_installs_old_experiment_reruns_allowed'] is False,'SCOPE_EXPANSION')
    pools=[json.loads((root/reg[k]).read_text()) for k in ['first_pool','E02_pool','predecessor_pool']]
    check(all(p['halted'] is True and p['completed'] is True for p in pools),'CLOSED_POOLS_REQUIRED')
    pool=pools[-1];check(pool['reserved']==reg['prior_reserved']==d['prior_reserved']==PRIOR,'PRIOR_COUNT_DRIFT')
    check(pool['cumulative_actual_window_seconds']==reg['prior_actual_window_seconds']==d['prior_actual_window_seconds']==ACTUAL,'PRIOR_ACTUAL_DRIFT')
    check(pool['cumulative_charged_window_seconds']==reg['prior_charged_checkpoint_seconds']==d['prior_charged_checkpoint_seconds']==CHARGED,'PRIOR_CHARGED_DRIFT')
    check(type(d['prior_wall_charge_seconds']) is int and d['prior_wall_charge_seconds']==reg['prior_wall_charge_seconds']==15,'PRIOR_CHARGE_DRIFT')
    check(type(d['attempt_maximum_window_seconds']) is int and d['attempt_maximum_window_seconds']==reg['attempt_maximum_window_seconds']==1185,'WINDOW_DRIFT')
    check(reg['caps']==d['cumulative_caps']==CUMULATIVE_CAPS and reg['native_depth']==d['native_depth']==8,'CAPS_OR_DEPTH_DRIFT')
    remaining=dict(compile_jobs=26,native_jobs=28,physical_jobs=30,setup_jobs=0,physical_cycles=1012,execution_wall_seconds=1185)
    check(reg['remaining_allocation']==d['remaining_allocation']==remaining,'REMAINING_DRIFT')
    check(reg['pool_state']==reg['result_root']+'/execution-state.json' and reg['process_supervision']=='owned_process_group_only','NEW_POOL_OR_SUPERVISION')
    allocation=Allocation(tuple(sorted(PRIOR.items())),ACTUAL,15,1185,tuple(sorted(dict(decision=DECISION_SHA,pool=POOL_SHA,grant=GRANT_SHA,review=d['predecessor_review_sha256']).items())),pools[0]['events'][0]['error'])
    allocation.validate();return allocation
