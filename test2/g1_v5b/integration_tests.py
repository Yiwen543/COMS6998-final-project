"""Focused R05B saved-evidence/gate/allocation checks;no real G1 job."""
from pathlib import Path
from unittest.mock import patch
import argparse,copy,hashlib,json,shutil,sys,time,unittest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.append(str(ROOT/'test2/g1_v5'))
from allocation import load_allocation,AllocationError,CUMULATIVE_CAPS
from budget import Budget,Refuse
from contracts import registration_contract
from observations import Unqualified
from native_results import read_native,judge_native
import reuse,runner
REG=json.loads((ROOT/'test2/configs/g1_qualification_registration_v5b.json').read_text());OUT=None
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir();self.inputs=self.folder/'inputs';self.inputs.mkdir();self.result={'real_G1_process_signal_sleep_calls':0,'scope':'PURE_INTEGRATION_NOT_EXECUTION_ACCEPTANCE'}
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n')
        (self.folder/'input-bindings.json').write_text(json.dumps({str(p.relative_to(self.inputs)):sha(p) for p in self.inputs.rglob('*') if p.is_file()},indent=2)+'\n')
    def allocation(self):return load_allocation(ROOT,REG,{'continuation_decision_sha256':REG['continuation_decision_sha256']})
    def test_01_actual_allocation_closed_lineage(self):
        a=self.allocation();self.assertEqual(dict(a.prior_reserved),dict(compile=6,native=4,physical=3,physical_cycles=12,setup=8));self.assertEqual((a.prior_charge_seconds,a.attempt_window_seconds),(15,1185));self.result['actual_allocation_loaded_without_EXECUTE']=True
    def test_02_plan_exact_remaining_and_unchanged_hardware(self):
        plan=read(ROOT/REG['job_plan']);registration_contract(ROOT,REG,read(ROOT/REG['user_authorization']),plan)
        old=read(ROOT/'test2/g1_v4/job-plan.json')['jobs'];report=read(ROOT/'test2/results/g1-qualification-v4/report.json');expected=[]
        for j in old:
            if report['jobs'][j['id']]['status']!='NOT_RUN':continue
            x=copy.deepcopy(j);x['argv']=[s.replace('/g1_v4/','/g1_v5/') for s in x['argv']]
            if x['kind']=='physical':x['argv']=[s.replace('{OUT}/build/','{ROOT}/test2/results/g1-qualification-v4/build/') for s in x['argv']]
            expected.append(x)
        self.assertEqual(plan['jobs'],expected)
        for pair in read(ROOT/REG['reuse_manifest'])['unchanged_hardware_and_input_pairs']:self.assertEqual(sha(ROOT/pair['new']),sha(ROOT/pair['old']))
        self.result.update(new_roots=72,new_cycles=120,no_flag_change=True)
    def test_03_decode_ten_exact_reused_jobs_preserves_failed_cover(self):
        decoded=reuse.decode(ROOT,REG,reuse.metadata(ROOT,REG));self.assertEqual(len(decoded['jobs']),10)
        self.assertTrue(all(j['new_execution'] is False for j in decoded['jobs'].values()))
        job=decoded['jobs']['QC01-cover'];out=job['native_evidence']
        self.assertEqual((out['tool_status'],out['process_exit_code'],out['activation'],out['assertion_observation']),('FAILED',1,'REACHED','FAILED'))
        self.assertEqual(job['original_job']['native_status'],'NOT_REACHED')
        self.assertFalse(job['target_judgment']['overall_tool_PASS_claimed']);self.assertEqual(len(decoded['physical']),2)
        self.result['QC01_cover']=job;self.result['all_reuse_is_not_new_trial']=True
    def test_04_unknown_native_never_meets_target(self):
        intent=read(ROOT/REG['interpretation'])['cases'][1]
        with self.assertRaisesRegex(Unqualified,'NATIVE_EVIDENCE_UNKNOWN'):judge_native({'evidence_complete':False,'issues':['SYNTHETIC_UNKNOWN']},'cover',intent)
    def test_05_actual_entry_missing_P16_no_claim(self):
        p=self.inputs/'not_EXECUTE_authority.json';p.write_text(json.dumps(dict(record_kind='G1_EXECUTE_R05B_AFTER_P16',stage='EXECUTE',continuation_decision_sha256=REG['continuation_decision_sha256'],fixture_origin='SYNTHETIC_NEGATIVE_NOT_AUTHORIZATION')))
        with patch.object(runner,'claim_attempt',side_effect=AssertionError('NO_CLAIM')) as claimed:
            with self.assertRaisesRegex(Unqualified,'MISSING_P16_REFERENCE'):runner.main(p)
        self.assertEqual(claimed.call_count,0);self.result['claim_calls']=0
    def test_06_old_EXECUTE_rejected(self):
        p=self.inputs/'old_EXECUTE.json';shutil.copy2(ROOT/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r04.json',p)
        with self.assertRaisesRegex(Unqualified,'WRONG_EXECUTE'):runner.review_gate(p)
    def test_07_prior_count_reset_rejected(self):
        reg=copy.deepcopy(REG);reg['prior_reserved']['native']=0;(self.inputs/'registration.json').write_text(json.dumps(reg))
        with self.assertRaisesRegex(AllocationError,'PRIOR_COUNT_DRIFT'):load_allocation(ROOT,reg,{'continuation_decision_sha256':REG['continuation_decision_sha256']})
    def test_08_changed_compiled_binary_binding_refuses(self):
        real_sha=reuse.sha
        with patch.object(reuse,'sha',side_effect=lambda p:'0'*64 if Path(p).name=='physical_sim' else real_sha(p)):
            with self.assertRaisesRegex(Unqualified,'REUSE_HASH_DRIFT'):reuse.metadata(ROOT,REG)
    def test_09_synthetic_budget_inherits_caps_no_setup(self):
        path=self.inputs/'SYNTHETIC_ONLY_ledger.json';b=Budget(path,CUMULATIVE_CAPS,clock=lambda:100.0,allocation=self.allocation(),started_at=100.0)
        self.assertEqual(b.state['reserved'],REG['prior_reserved']);self.assertEqual(b.attempt_window,1185);self.assertEqual(b.work_deadline,1280.0)
        with self.assertRaisesRegex(Refuse,'JOB_CAP_setup'):b.reserve('setup','synthetic-forbidden')
        self.result['synthetic_ledger_only']=True
    def native_fixture(self,mode):
        folder=ROOT/('test2/results/g1-qualification-v4/jobs/QC01-'+mode)
        for name in ['stdout.log','stderr.log','receipt.json','trace.vcd']:shutil.copy2(folder/name,self.inputs/name)
        return ROOT/'test2/g1_v4/sources/QC01_formal.sv'
    def test_10_truncated_reached_VCD_is_unknown(self):
        source=self.native_fixture('cover');p=self.inputs/'trace.vcd';text=p.read_text();self.assertIn('#25',text);p.write_text(text.split('#25')[0])
        out=read_native(self.inputs,source,'cover');self.assertEqual(out['activation'],'UNKNOWN');self.assertEqual(out['tool_status'],'FAILED');self.assertIn('TRUNCATED_OR_UNSUPPORTED_TRACE_END',out['issues']);self.result['out']=out
    def test_11_BMC_missing_assertion_witness_unknown(self):
        source=self.native_fixture('bmc');p=self.inputs/'stdout.log';p.write_text('\n'.join(s for s in p.read_text().splitlines() if 'Assert failed' not in s)+'\n')
        rp=self.inputs/'receipt.json';r=read(rp);r['stdout_sha256']=sha(p);rp.write_text(json.dumps(r))
        out=read_native(self.inputs,source,'bmc');self.assertEqual(out['tool_status'],'FAILED');self.assertFalse(out['evidence_complete']);self.assertIn('FAILED_WITHOUT_ASSERT_WITNESS',out['issues']);self.result['out']=out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record',required=True,type=Path);args=parser.parse_args();OUT=args.record;OUT.mkdir(parents=True,exist_ok=False);copydir=OUT/'executed-source';copydir.mkdir();files=[*HERE.glob('*.py'),ROOT/'test2/g1_v5/native_evidence.py',ROOT/'test2/g1_v5/observations.py',ROOT/'test2/configs/g1_qualification_registration_v5b.json',HERE/'job-plan.json',HERE/'interpretation.json']
    source_sha={}
    for p in files:
        name=p.relative_to(ROOT).as_posix();t=copydir/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);source_sha[name]=sha(p)
    start=time.monotonic()
    with patch('subprocess.Popen',side_effect=AssertionError('NO_REAL_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_REAL_RUN')),patch('os.killpg',side_effect=AssertionError('NO_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_SLEEP')):
        with (OUT/'unittest.log').open('x') as log:result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IntegrationTests))
    summary=dict(scope='R05B_PURE_INTEGRATION_NOT_G1_EXECUTION',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),seconds=time.monotonic()-start,real_G1_process_signal_sleep_calls=0,source_sha256=source_sha)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
