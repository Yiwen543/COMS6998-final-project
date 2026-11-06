"""R04 pure source/metadata/refusal checks. Never SV/native execution."""
import argparse,copy,hashlib,json,shutil,time,unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
from allocation import AllocationError,load_allocation,CUMULATIVE_CAPS
from budget import Budget,Refuse
from continuation_contracts import registration_contract,gate_contract
from native_reuse import load_reuse
from observations import Unqualified,parse_rows
import runner

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REG=json.loads((ROOT/'test2/configs/g1_qualification_registration_v4.json').read_text())
RECORD=None
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class R04Tests(unittest.TestCase):
    def setUp(self):
        self.folder=RECORD/self._testMethodName;self.folder.mkdir()
        self.inputs=self.folder/'inputs';self.inputs.mkdir()
        self.result={'scope':'PURE_R04_NOT_SV_FIX_VALIDATION','real_G1_process_signal_sleep_calls':0}
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n')
        (self.folder/'input-bindings.json').write_text(json.dumps({str(p.relative_to(self.inputs)):sha(p) for p in self.inputs.rglob('*') if p.is_file()},indent=2)+'\n')
    def note_input(self,name,value):
        (self.inputs/name).write_text(json.dumps(value,indent=2)+'\n')
    def test_01_positive_startup_schedule_arithmetic_only(self):
        text=(HERE/'sources/physical_tb.sv').read_text();(self.inputs/'physical_tb.sv').write_text(text)
        self.assertIn("step=3'd7",text);self.assertIn('#0.001;',text);self.assertIn('if(k==0) #0.999; else #1;',text)
        self.assertNotIn('#0;',text);self.assertEqual(text.count("clk=1'b1"),1)
        tick=Fraction('0.001')*1000;pre=[];edges=[];post=[]
        for c in range(4):
            tick+=(Fraction('0.999') if c==0 else 1)*1000;pre.append(int(tick))
            tick+=1000;edges.append(int(tick));tick+=1000;post.append(int(tick));tick+=1000
        self.assertEqual(pre,[1000,5000,9000,13000]);self.assertEqual(edges,[2000,6000,10000,14000])
        self.assertEqual(post,[3000,7000,11000,15000]);self.assertEqual(tick,16000)
        self.result.update(pre=pre,edges=edges,post=post,end=int(tick),SV_scheduling_executed=False)
    def test_02_twenty_three_dependencies_unchanged(self):
        m=json.loads((HERE/'native-reuse.json').read_text());self.assertEqual(len(m['unchanged_dependencies']),23)
        for p in m['unchanged_dependencies']:self.assertEqual(sha(ROOT/p['old']),sha(ROOT/p['new']))
        self.assertEqual(sha(HERE/'observations.py'),sha(ROOT/'test2/g1_v3/observations.py'))
    def test_03_saved_QC00_native_prefix_binds(self):
        self.result['reuse']=load_reuse(ROOT,REG)
        self.assertEqual(self.result['reuse']['new_native_jobs'],0)
        self.assertFalse(self.result['reuse']['rejected_QC00_physical_reused'])
        self.assertFalse(self.result['reuse']['full_QC_qualification'])
    def bundle(self):
        root=self.inputs/'bundle';root.mkdir()
        m=json.loads((HERE/'native-reuse.json').read_text())
        names=set(m['files'])|{p['new'] for p in m['unchanged_dependencies']}|{REG['native_reuse_manifest']}
        for name in names:
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,p)
        return root,m
    def test_04_changed_common_refuses_reuse(self):
        root,m=self.bundle();p=root/'test2/g1_v4/sources/common.sv';p.write_text(p.read_text()+'\n// SYNTHETIC_DRIFT\n')
        with self.assertRaisesRegex(Unqualified,'NATIVE_DEPENDENCY_CHANGED'):load_reuse(root,REG)
    def test_05_changed_saved_SMT_refuses_reuse(self):
        root,m=self.bundle();p=root/'test2/results/g1-qualification-v3/build/QC00/model.smt2';p.write_text(p.read_text()+'\n; SYNTHETIC_DRIFT\n')
        with self.assertRaisesRegex(Unqualified,'REUSE_HASH_DRIFT'):load_reuse(root,REG)
    def test_06_changed_native_depth_refuses(self):
        reg=copy.deepcopy(REG);reg['native_depth']=9;self.note_input('registration.json',reg)
        with self.assertRaisesRegex(Unqualified,'REUSE_PROFILE_DEPTH'):load_reuse(ROOT,reg)
    def test_07_changed_tool_pin_refuses(self):
        reg=copy.deepcopy(REG);reg['tools']['z3']['resolved_sha256']='0'*64;self.note_input('registration.json',reg)
        with self.assertRaisesRegex(Unqualified,'REUSE_TOOL_PIN'):load_reuse(ROOT,reg)
    def test_08_plan_and_resource_lower_bound(self):
        plan=json.loads((HERE/'job-plan.json').read_text());grant=json.loads((ROOT/REG['user_authorization']).read_text())
        registration_contract(ROOT,REG,grant,plan)
        counts={kind:sum(j['kind']==kind for j in plan['jobs']) for kind in ['setup','compile','native','physical']}
        self.assertEqual(counts,{'setup':0,'compile':17,'native':30,'physical':32})
        self.assertEqual(REG['prior_reserved']['physical']+counts['physical'],33)
        self.assertGreater(33,REG['original_caps']['physical_jobs'])
        self.result.update(new_jobs=counts,cumulative_compile=20,cumulative_native=32,cumulative_physical=33,
                           allocation_authority_recorded=True,EXECUTE_granted=False,without_native_reuse_cumulative_native=34)
    def test_09_missing_approval_hash_refuses(self):
        with self.assertRaisesRegex(AllocationError,'MISSING_APPROVED_CONTINUATION_DECISION_HASH'):load_allocation(ROOT,REG,{})
    def test_10_missing_approval_files_refuse(self):
        root=self.inputs/'no_authority';root.mkdir()
        gate={'continuation_decision_sha256':'1'*64,'budget_amendment_sha256':'2'*64};self.note_input('gate.json',gate)
        with self.assertRaisesRegex(AllocationError,'MISSING_OR_SYMLINK_AUTHORITY'):load_allocation(root,REG,gate)
    def test_11_pending_user_physical33_refuses(self):
        root=self.inputs/'synthetic_pending_authority';root.mkdir()
        gate={}
        for key,data in [('continuation_decision',{'status':'PENDING_NOT_AUTHORIZATION','fixture_origin':'SYNTHETIC_NEGATIVE'}),
                         ('budget_amendment',{'record_kind':'G1_CUMULATIVE_PHYSICAL_CAP_AMENDMENT','user_approved':False,'cumulative_physical_jobs':33,'fixture_origin':'SYNTHETIC_NEGATIVE'})]:
            p=root/REG[key];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data));gate[key+'_sha256']=sha(p)
        with self.assertRaisesRegex(AllocationError,'PHYSICAL33_NOT_USER_APPROVED'):load_allocation(root,REG,gate)
    def test_12_missing_P14_refuses(self):
        gate={'record_kind':'G1_EXECUTE_R04_AFTER_P14_AND_PHYSICAL33_APPROVAL','stage':'EXECUTE'}
        self.note_input('gate.json',gate)
        with self.assertRaisesRegex(Unqualified,'P14_ACCEPTANCE_REQUIRED'):gate_contract(gate,{}, {})
    def test_13_old_P12_receipt_refuses(self):
        gate={'record_kind':'G1_EXECUTE_CONTINUATION_AFTER_P12','stage':'EXECUTE'}
        self.note_input('old-gate.json',gate)
        with self.assertRaisesRegex(Unqualified,'OLD_OR_WRONG_EXECUTE'):gate_contract(gate,{}, {})
    def test_14_actual_entry_pending_approval_has_no_claim(self):
        p=self.inputs/'not_real_execute.json';p.write_text(json.dumps({'record_kind':'G1_EXECUTE_R04_AFTER_P14_AND_PHYSICAL33_APPROVAL','stage':'EXECUTE','fixture_origin':'SYNTHETIC_NEGATIVE'}))
        with patch.object(runner,'claim_attempt',side_effect=AssertionError('MUST_NOT_CLAIM')) as claim:
            with self.assertRaisesRegex(AllocationError,'MISSING_APPROVED_CONTINUATION_DECISION_HASH'):runner.main(p)
        self.assertEqual(claim.call_count,0)
        self.assertFalse((ROOT/REG['pool_state']).exists());self.assertFalse((ROOT/REG['attempt_lock']).exists())
        self.result['claim_calls']=0
    def test_15_no_allocation_no_ledger(self):
        p=self.folder/'synthetic-never-created-ledger.json'
        with self.assertRaisesRegex(Refuse,'MISSING_VERIFIED_CONTINUATION'):Budget(p,CUMULATIVE_CAPS)
        self.assertFalse(p.exists())
    def test_16_synthetic_X_first_row_still_rejects(self):
        case=json.loads((ROOT/REG['controls']).read_text())['cases'][0];rows=copy.deepcopy(case['physical_rows_expected_icarus']);rows[0]['a']='xxxx'
        lines=[]
        for row in rows:
            lines.append('OBS qc=0 '+' '.join(str(k)+'='+str(row[k]) for k in ['cycle','phase','tick','q','active','ok','marker','a','b','rst','en','valid']))
        text='\n'.join(lines)+'\nEND qc=0 cycles=4 posedges=4\n';(self.inputs/'SYNTHETIC_OBS.txt').write_text(text)
        with self.assertRaisesRegex(Unqualified,'PHYSICAL_EXPECTED_MISMATCH:a'):parse_rows(text,case,'icarus')
        self.result['synthetic_only']=True

    def test_17_real_approved_allocation_no_claim_or_ledger(self):
        gate={k+'_sha256':REG[k+'_sha256'] for k in ['continuation_decision','budget_amendment']}
        self.note_input('actual-authority-bindings.json',gate)
        allocation=load_allocation(ROOT,REG,gate)
        allocation.validate()
        self.assertEqual(dict(allocation.prior_reserved),REG['prior_reserved'])
        self.assertEqual(allocation.prior_charge_seconds,8)
        self.assertEqual(allocation.attempt_window_seconds,1192)
        self.assertFalse((ROOT/REG['pool_state']).exists())
        self.assertFalse((ROOT/REG['attempt_lock']).exists())
        with self.assertRaisesRegex(Unqualified,'P14_ACCEPTANCE_REQUIRED'):
            gate_contract({'record_kind':'G1_EXECUTE_R04_AFTER_P14_AND_PHYSICAL33_APPROVAL','stage':'EXECUTE'}, {}, {})
        self.result.update(real_authority_verified=True,claimed=False,ledger_created=False,P14_still_required=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',required=True,type=Path);args=p.parse_args()
    RECORD=args.record;RECORD.mkdir(exist_ok=False);source=RECORD/'executed-source';source.mkdir()
    for f in HERE.glob('*.py'):shutil.copy2(f,source/f.name)
    for name in ['job-plan.json','native-reuse.json']:
        shutil.copy2(HERE/name,source/name)
    shutil.copy2(ROOT/'test2/configs/g1_qualification_registration_v4.json',source/'registration.json')
    start=time.monotonic()
    with patch('subprocess.Popen',side_effect=AssertionError('REAL_PROCESS_FORBIDDEN')),patch('subprocess.run',side_effect=AssertionError('REAL_RUN_FORBIDDEN')),patch('os.killpg',side_effect=AssertionError('REAL_SIGNAL_FORBIDDEN')),patch('time.sleep',side_effect=AssertionError('REAL_SLEEP_FORBIDDEN')):
        with (RECORD/'unittest.log').open('x') as log:
            result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(R04Tests))
    summary={'scope':'R04_PURE_METADATA_STARTUP_ARITHMETIC_REUSE_REFUSALS_NOT_SV_VALIDATION','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'seconds':time.monotonic()-start,'real_G1_process_signal_sleep_calls':0,'source_sha256':{f.name:sha(f) for f in source.iterdir()}}
    (RECORD/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
