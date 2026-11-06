"""R03 new pure tests. No real process, signal, sleep, version or inventory scan."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
from types import SimpleNamespace
import time
import unittest
from unittest.mock import patch
from allocation import (AllocationError, CUMULATIVE_CAPS, DECISION_SHA, POOL_SHA,
                        GRANT_SHA, PRIOR_ACTUAL, load_allocation)
from budget import Budget, Refuse
from continuation_contracts import gate_contract, registration_contract
from observations import Unqualified
from runtime import execute
from runner import claim_attempt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REG = json.loads((ROOT / 'test2/configs/g1_qualification_registration_v3.json').read_text())
ALLOC = load_allocation(ROOT, REG)
RECORD = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Clock:
    value = 0.0
    def now(self): return self.value
    def advance(self, seconds): self.value += seconds


class Child:
    pid = 987654322
    def __init__(self, finish_after=2, poll_error=False, wait_error=False, cleanup_timeout=False):
        self.returncode = 0 if finish_after == 0 else None
        self.finish_after = finish_after
        self.polls = self.waits = 0
        self.poll_error, self.wait_error, self.cleanup_timeout = poll_error, wait_error, cleanup_timeout
    def poll(self):
        if self.poll_error: raise OSError('MOCK_REQUIRED_POLL_DENIED')
        self.polls += 1
        if self.finish_after is not None and self.polls >= self.finish_after: self.returncode = 0
        return self.returncode
    def wait(self, timeout=None):
        self.waits += 1
        if self.wait_error: raise PermissionError('MOCK_REQUIRED_WAIT_DENIED')
        if self.cleanup_timeout and self.waits > 1: raise __import__('subprocess').TimeoutExpired('MOCK_WAIT', timeout)
        if self.returncode is None: raise __import__('subprocess').TimeoutExpired('MOCK_PENDING_WAIT', timeout)
        return self.returncode


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.folder = RECORD / self._testMethodName; self.folder.mkdir()
        self.inputs = self.folder / 'inputs'; self.inputs.mkdir()
        self.result = {'origin':'R03_PURE_MOCK_NOT_REAL_G1_QUALIFICATION','real_tool_signal_sleep_inventory_calls':0}
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n')
        (self.folder/'input-bindings.json').write_text(json.dumps({str(p.relative_to(self.inputs)):sha(p) for p in self.inputs.rglob('*') if p.is_file()},indent=2)+'\n')
    def budget(self, clock=None, caps=None, allocation=ALLOC):
        return Budget(self.folder/'synthetic-ledger.json', caps or CUMULATIVE_CAPS,
                      allocation=allocation, clock=(clock or Clock()).now)
    def run_child(self, inventory='permission', finish_after=2, group_error=False,
                  kill_error=False, poll_error=False, wait_error=False, cleanup_timeout=False):
        clock=Clock(); b=self.budget(clock)
        child=Child(finish_after,poll_error,wait_error,cleanup_timeout)
        config=dict(inventory=inventory,finish_after=finish_after,group_error=group_error,
                    kill_error=kill_error,poll_error=poll_error,wait_error=wait_error,cleanup_timeout=cleanup_timeout)
        (self.inputs/'mock-config.json').write_text(json.dumps(config,indent=2)+'\n')
        def probe(pid):
            self.assertEqual(pid,child.pid)
            if inventory=='permission': raise PermissionError('MOCK_OPTIONAL_INVENTORY_DENIED')
            if inventory=='oserror': raise OSError('MOCK_OPTIONAL_INVENTORY_OSERROR')
            if inventory=='timeout':
                clock.advance(.1)
                raise __import__('subprocess').TimeoutExpired('MOCK_OPTIONAL_INVENTORY',.1)
            return [{'pid':pid,'scope':'MOCK_OWNED_GROUP_ONLY'}]
        def killpg(pid,signum):
            self.assertEqual(pid,child.pid)
            if not signum:
                if group_error: raise PermissionError('MOCK_REQUIRED_GROUP_PROBE_DENIED')
                if child.returncode is not None: raise ProcessLookupError()
                return
            if kill_error: raise PermissionError('MOCK_REQUIRED_KILL_DENIED')
            child.returncode=-9
        job=dict(id='mock-root',kind='compile',argv=['MOCK_NO_EXECUTABLE'])
        with patch('runtime.time.monotonic',clock.now), patch('runtime.time.sleep',clock.advance), \
             patch('runtime.subprocess.Popen',return_value=child) as popen, \
             patch('runtime.subprocess.run',side_effect=AssertionError('REAL_INVENTORY_FORBIDDEN')) as run, \
             patch('runtime.os.killpg',side_effect=killpg):
            receipt=execute(b,job,self.folder/'job',{},inventory_probe=None if inventory=='none' else probe)
            calls,scanner_calls=popen.call_count,run.call_count
        self.result.update(receipt=receipt,ledger=copy.deepcopy(b.state),mocked_Popen_calls=calls,
                           external_command_scan_calls=scanner_calls,final_fake_clock=clock.value)
        self.assertEqual(scanner_calls,0)
        return b,receipt
    def assert_optional_nonfatal(self,mode,finish_after=2):
        b,d=self.run_child(mode,finish_after=finish_after)
        self.assertEqual(d['status'],'RETURNED');self.assertEqual(d['exit_code'],0)
        self.assertFalse(b.state['halted']);self.assertFalse(d['child_pid_inventory_complete'])
        self.assertEqual(d['inventory']['availability'],'UNAVAILABLE_OPTIONAL_ERROR')
        self.assertIsNotNone(d['inventory']['current_error']);self.assertFalse(d['mandatory_errors'])
    def test_01_optional_permission_running_child(self): self.assert_optional_nonfatal('permission')
    def test_02_optional_permission_already_exited_child(self): self.assert_optional_nonfatal('permission',0)
    def test_03_optional_oserror_nonfatal(self): self.assert_optional_nonfatal('oserror')
    def test_04_optional_timeout_nonfatal(self): self.assert_optional_nonfatal('timeout')
    def test_05_available_mock_inventory_is_not_complete_census(self):
        b,d=self.run_child('available');self.assertEqual(d['status'],'RETURNED');self.assertEqual(d['exit_code'],0)
        self.assertEqual(d['inventory']['availability'],'AVAILABLE_MOCK_RECORDS_ONLY');self.assertFalse(d['inventory']['complete'])
    def test_06_registered_path_has_no_inventory_attempt(self):
        b,d=self.run_child('none');self.assertEqual(d['status'],'RETURNED');self.assertEqual(d['inventory']['attempts'],0)
        self.assertEqual(d['inventory']['availability'],'UNAVAILABLE_KNOWN_FROM_PREDECESSOR')
        self.assertIn('PermissionError',d['inventory']['predecessor_error']);self.assertEqual(d['exit_code'],0)
    def test_07_pending_child_retains_original_timeout_and_group_kill(self):
        b,d=self.run_child('permission',finish_after=None)
        self.assertEqual(d['status'],'TIMEOUT');self.assertTrue(d['timed_out']);self.assertEqual(d['exit_code'],-9)
        self.assertEqual(d['absolute_job_deadline'],20);self.assertLessEqual(self.result['final_fake_clock'],20)
        self.assertTrue(b.state['halted'])
    def test_08_required_group_probe_failure_is_fatal(self):
        b,d=self.run_child('permission',finish_after=0,group_error=True)
        self.assertEqual(d['status'],'PROTECTION_UNRESOLVED');self.assertTrue(b.state['halted']);self.assertEqual(d['exit_code'],0)
        self.assertTrue(any(x['operation']=='OWNED_GROUP_PROBE' for x in d['mandatory_errors']))
    def test_09_required_kill_failure_is_fatal(self):
        b,d=self.run_child('permission',finish_after=None,kill_error=True)
        self.assertEqual(d['status'],'PROTECTION_UNRESOLVED');self.assertTrue(b.state['halted'])
        self.assertTrue(any('KILL' in x['operation'] for x in d['mandatory_errors']))
    def test_10_required_wait_failure_is_fatal(self):
        b,d=self.run_child('permission',finish_after=0,wait_error=True)
        self.assertEqual(d['status'],'PROTECTION_UNRESOLVED');self.assertTrue(b.state['halted'])
        self.assertEqual(d['exit_code'],0);self.assertTrue(d['mandatory_errors'])
    def test_11_required_poll_failure_is_fatal(self):
        b,d=self.run_child('permission',finish_after=None,poll_error=True)
        self.assertEqual(d['status'],'PROTECTION_UNRESOLVED');self.assertTrue(b.state['halted'])
        self.assertTrue(any(x['operation']=='POLL' for x in d['mandatory_errors']))
    def test_12_cleanup_wait_timeout_cannot_be_hidden(self):
        b,d=self.run_child('none',finish_after=0,cleanup_timeout=True)
        self.assertEqual(d['status'],'PROTECTION_UNRESOLVED');self.assertTrue(b.state['halted'])
    def test_13_prior_counts_actual_and_charge_are_separate(self):
        b=self.budget();self.assertEqual(b.state['reserved']['setup'],1);self.assertEqual(b.state['attempt_reserved']['setup'],0)
        self.assertEqual(b.state['prior_actual_window_seconds'],PRIOR_ACTUAL)
        self.assertEqual(b.state['prior_conservative_charge_seconds'],2);self.assertEqual(b.attempt_window,1198)
        self.assertEqual(b.work_deadline,1193);self.result['ledger']=b.state
    def test_14_seven_new_setups_exhaust_cumulative_eight(self):
        b=self.budget()
        for i in range(7):
            b.reserve('setup',f'mock{i}');b.terminal(f'mock{i}',{'status':'MOCK_RETURNED'})
        with self.assertRaises(Refuse): b.reserve('setup','eighth-new')
        self.assertEqual(b.state['reserved']['setup'],8);self.assertEqual(b.state['attempt_reserved']['setup'],7)
        self.result['ledger']=b.state
    def test_15_current_window_cannot_be_full1200(self):
        c=Clock();b=self.budget(c);c.value=1199;b.complete();self.assertTrue(b.state['halted'])
        self.assertGreater(b.state['cumulative_charged_window_seconds'],1200)
        self.assertEqual(b.state['prior_conservative_charge_seconds'],2);self.result['ledger']=b.state
    def test_16_missing_allocation_refuses_before_ledger(self):
        with self.assertRaises(Refuse): self.budget(allocation=None)
        self.assertFalse((self.folder/'synthetic-ledger.json').exists())
    def bad_reg(self,mutate,reason):
        reg=copy.deepcopy(REG);mutate(reg);(self.inputs/'final-mutated-registration.json').write_text(json.dumps(reg,indent=2)+'\n')
        with self.assertRaisesRegex(AllocationError,reason) as caught:load_allocation(ROOT,reg)
        self.result.update(outcome='REJECT',reason=str(caught.exception))
    def test_17_false_prior_zero_refuses(self): self.bad_reg(lambda d:d['prior_reserved'].update(setup=0),'FALSE_PRIOR_COUNTS')
    def test_18_expanded_remaining_refuses(self): self.bad_reg(lambda d:d['remaining_allocation'].update(execution_wall_seconds=1200),'EXPANDED_REMAINING')
    def test_19_predecessor_hash_drift_refuses(self): self.bad_reg(lambda d:d.update(predecessor_pool_sha256='0'*64),'PREDECESSOR_HASH_DRIFT')
    def test_20_missing_predecessor_refuses(self): self.bad_reg(lambda d:d.pop('predecessor_pool'),'MISSING_PREDECESSOR_FIELD')
    def test_21_false_prior_charge_zero_refuses(self): self.bad_reg(lambda d:d.update(prior_wall_charge_seconds=0),'FALSE_PRIOR_CONSERVATIVE_CHARGE')
    def test_22_duplicate_ledger_and_attempt_claim_refuse(self):
        self.budget()
        with self.assertRaises(FileExistsError): self.budget()
        lock=self.folder/'MOCK_ATTEMPT.lock';claim_attempt(lock,{'origin':'MOCK_ONLY'});before=sha(lock)
        with self.assertRaises(FileExistsError):claim_attempt(lock,{'origin':'MOCK_ONLY_DUPLICATE'})
        self.assertEqual(sha(lock),before)
    def test_23_caps_expansion_refuses(self):
        caps=copy.deepcopy(CUMULATIVE_CAPS);caps['native_jobs']=33
        with self.assertRaises(Refuse):self.budget(caps=caps)
    def gate_fixture(self):
        ids=dict(registration_sha256='1'*64,source_manifest_sha256='2'*64,user_authorization_sha256=GRANT_SHA,
                 preparation_manifest_sha256='3'*64,continuation_decision_sha256=DECISION_SHA,predecessor_pool_sha256=POOL_SHA)
        gate=dict(ids,record_kind='G1_EXECUTE_CONTINUATION_AFTER_P12',stage='EXECUTE')
        review=dict(phase='P12_PURE_MOCK',status='PASS_WITH_LIMITS',input_identity=dict(producer_manifest_sha256='3'*64,
                    registration_sha256='1'*64,continuation_decision_sha256=DECISION_SHA))
        return gate,review,ids
    def test_24_P12_gate_accepts_exact_mock_bindings_only(self):
        gate,review,ids=self.gate_fixture();gate_contract(gate,review,ids)
        self.result['scope']='MOCK_GATE_NOT_REAL_EXECUTE_RECEIPT'
    def test_25_old_receipt_and_old_review_refuse(self):
        gate,review,ids=self.gate_fixture();gate['record_kind']='G1_EXECUTE_AFTER_READONLY_P10'
        with self.assertRaises(Unqualified):gate_contract(gate,review,ids)
        gate,review,ids=self.gate_fixture();review['phase']='P10B_OLD'
        with self.assertRaises(Unqualified):gate_contract(gate,review,ids)
    def test_26_P12_wrong_continuation_refuses(self):
        gate,review,ids=self.gate_fixture();review['input_identity']['continuation_decision_sha256']='0'*64
        with self.assertRaises(Unqualified):gate_contract(gate,review,ids)
    def test_27_seven_setup_contract_and_unchanged_native_plan(self):
        grant=json.loads((ROOT/REG['user_authorization']).read_text());plan=json.loads((HERE/'job-plan.json').read_text())
        registration_contract(ROOT,REG,grant,plan)
        bad=copy.deepcopy(plan);bad['jobs'].append({'id':'setup-make','kind':'setup','argv':['MOCK_NEVER_EXECUTED']})
        with self.assertRaises(Unqualified):registration_contract(ROOT,REG,grant,bad)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);args=p.parse_args()
    RECORD=args.record;RECORD.mkdir(exist_ok=False);source_copy=RECORD/'executed-source';source_copy.mkdir()
    for f in HERE.glob('*.py'):shutil.copy2(f,source_copy/f.name)
    began=time.monotonic()
    with (RECORD/'unittest.log').open('x') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContinuationTests))
    summary=dict(scope='R03_NEW_PURE_OPTIONAL_INVENTORY_PROTECTION_CUMULATIVE_GATE_TESTS',tests=result.testsRun,
                 failures=len(result.failures),errors=len(result.errors),seconds=time.monotonic()-began,passed=result.wasSuccessful(),
                 actual_G1_tool_process_signal_sleep_inventory_calls=0,source_sha256={f.name:sha(f) for f in source_copy.iterdir()})
    (RECORD/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
