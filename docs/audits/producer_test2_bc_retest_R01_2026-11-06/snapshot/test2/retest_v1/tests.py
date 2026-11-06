"""Focused pure adapter tests:all external process/network/key actions prohibited."""
from pathlib import Path
from unittest.mock import patch,Mock
import argparse,copy,json,hashlib,shutil,signal,subprocess,sys,time,unittest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
from resources import Halt,Retryable,Window,Ledger,verified_pricing
from supervision import child,owned_stage
from api import response_contract,action
from pipeline import execute_stage,APIClient,load,preflight_messages
from release import verify,release,freeze,ARMS
from cli import preserve_missing
import pipeline
REG=load(ROOT/'test2/configs/controller_done_bc_retest_v1.json');OUT=None
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
FAKE_PRICE=dict(count_reserve_micro_usd=1000,generation_reserve_micro_usd=241920,fixture='SYNTHETIC_NOT_LIVE_PRICING')
class Clock:
    def __init__(self,now=0):self.now=float(now)
    def __call__(self):return self.now
    def sleep(self,delay):self.now+=delay
class Process:
    def __init__(self):self.pid=999999;self.returncode=None
    def poll(self):return self.returncode
    def kill(self):self.returncode=-9
    def wait(self,timeout=None):
        if self.returncode is None:raise subprocess.TimeoutExpired('FAKE',timeout)
        return self.returncode

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir();self.inputs=self.folder/'inputs';self.inputs.mkdir();self.result=dict(actual_API_SDK_credential_SV_tools=0,scope='PURE_TEST_NOT_RESEARCH_TRIAL')
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n');(self.folder/'input-bindings.json').write_text(json.dumps({str(p.relative_to(self.inputs)):sha(p) for p in self.inputs.rglob('*') if p.is_file()},indent=2)+'\n')
    def ledger(self,pricing=FAKE_PRICE,clock=None):
        clock=clock or Clock();return Ledger(self.inputs/'ledger.json',REG,verified_pricing(pricing,REG,live=False),Window(0,REG,clock),'mock')
    def test_01_unknown_count_fee_blocks_whole_stage(self):
        data=dict(generation_reserve_micro_usd=241920,count_reserve_micro_usd=None)
        with self.assertRaisesRegex(Halt,'COUNT_PRICE_UNKNOWN'):verified_pricing(data,REG,live=False)
        b=Ledger(self.inputs/'ledger.json',REG,None,Window(0,REG,Clock()),'mock')
        with self.assertRaisesRegex(Halt,'COUNT_PRICE_UNKNOWN'):b.reserve_api('generation',{})
        self.assertEqual(b.state['generations_reserved'],0)
    def test_02_inclusive_USD20_boundary(self):
        p=dict(generation_reserve_micro_usd=241920,count_reserve_micro_usd=1068560)
        self.assertEqual(verified_pricing(p,REG,live=False)['maximum_micro_usd'],20000000)
        p['count_reserve_micro_usd']+=1
        with self.assertRaisesRegex(Halt,'EXCEED_USD20'):verified_pricing(p,REG,live=False)
    def test_03_failed_unknown_cost_not_refunded(self):
        b=self.ledger();i=b.reserve_api('generation',{});b.dispatched(i);b.api_result(i,dict(status='request_error',usage=None,actual_cost_usd=None))
        self.assertEqual(b.state['reserved_micro_usd'],241920);self.assertIsNone(b.state['events'][i]['actual_cost_usd']);self.assertEqual(b.state['generations_reserved'],1)
    def test_04_per_type_request_caps_no_reset(self):
        b=self.ledger()
        for i in range(16):b.reserve_api('count',{'i':i})
        with self.assertRaisesRegex(Halt,'REQUEST_CAP'):b.reserve_api('count',{})
        self.assertEqual(b.state['counts_reserved'],16)
    def test_05_persist_consumes_deadline_zero_dispatch(self):
        clock=Clock();b=self.ledger(clock=clock);save=b.save
        def slow():save();clock.now=3590
        with patch.object(b,'save',side_effect=slow):
            with self.assertRaisesRegex(Halt,'WORK_DEADLINE'):b.reserve_api('count',{})
        self.assertEqual(b.state['counts_reserved'],1);self.assertEqual(b.state['events'][0]['status'],'RESERVED_BEFORE_DISPATCH')
    def test_06_API_child_midcall_bound_by_remaining_stage(self):
        clock=Clock(3589.8);process=Process();factory=Mock(return_value=process)
        with self.assertRaisesRegex(Halt,'CHILD_TIMEOUT'):
            child(['FAKE_API'],self.inputs/'api.log',120,Window(0,REG,clock),{},clock=clock,sleep=clock.sleep,popen=factory)
        receipt=load(self.inputs/'api.log.process.json');self.assertAlmostEqual(receipt['absolute_deadline'],3590);self.assertFalse(factory.call_args.kwargs['start_new_session']);self.assertEqual(process.returncode,-9);self.result['receipt']=receipt
    def test_07_outer_parent_kills_stage_group_before60min(self):
        clock=Clock(3594.99);process=Process();signals=[]
        def killpg(pid,sig):
            signals.append(sig)
            if process.returncode is not None:raise ProcessLookupError()
            if sig==signal.SIGTERM:process.returncode=-15
        r=owned_stage(['FAKE_STAGE'],self.inputs,REG,Window(0,REG,clock),{},clock=clock,sleep=clock.sleep,popen=Mock(return_value=process),killpg=killpg)
        self.assertTrue(r['deadline_forced_stop']);self.assertTrue(r['within_total_wall']);self.assertIn(signal.SIGTERM,signals);self.assertFalse(r['child_inventory_complete']);self.result['parent']=r
    def test_08_cleanup_permission_failure_stays_failure(self):
        clock=Clock(3595);process=Process()
        r=owned_stage(['FAKE_STAGE'],self.inputs,REG,Window(0,REG,clock),{},clock=clock,sleep=clock.sleep,popen=Mock(return_value=process),killpg=Mock(side_effect=PermissionError('SYNTHETIC')))
        self.assertIn('PermissionError',r['mandatory_errors']);self.assertIsNone(r['returncode'])
    def test_09_live_gate_before_factory_or_credentials(self):
        factory=Mock(side_effect=AssertionError('NO_CLIENT'))
        with self.assertRaisesRegex(Halt,'EXACT_EXECUTE_ABSENT'):
            execute_stage(ROOT/REG['run_root'],'live',REG,Window(time.monotonic(),REG),execute=self.inputs/'absent.json',client_factory=factory)
        self.assertEqual(factory.call_count,0)
        with self.assertRaisesRegex(Halt,'EXACT_EXECUTE_ABSENT'):
            action(ROOT,self.inputs/'absent.json',self.inputs/'absent-request.json',self.inputs/'result.json')
        self.assertFalse((ROOT/REG['run_root']).exists())
    def test_10_usage_cap_and_model_mismatch_halt(self):
        r=dict(returned_model='wrong',returned_service_tier='default',provider_status='completed',output_text='{}',usage=dict(input_tokens=1000,output_tokens=1,total_tokens=1001))
        with self.assertRaisesRegex(Halt,'MODEL_OR_TIER'):response_contract(r,1000)
        r['returned_model']='gpt-6.1-sol';r['usage']['output_tokens']=8193;r['usage']['total_tokens']=9193
        with self.assertRaisesRegex(Halt,'TOKEN_BUDGET'):response_contract(r,1000)
    def test_11_incomplete_response_keeps_known_usage(self):
        r=dict(returned_model='gpt-6.1-sol',returned_service_tier='default',provider_status='incomplete',output_text='',usage=dict(input_tokens=1000,output_tokens=10,total_tokens=1010))
        with self.assertRaises(Retryable) as caught:response_contract(r,1000)
        self.assertEqual(caught.exception.record['usage']['output_tokens'],10)
    def test_12_prompt_isolation_and_exact_common_B_C(self):
        left=pipeline.old.messages('B2_raw',1);right=pipeline.old.messages('C2_semantic',1);b=json.loads(left[1]['content']);c=json.loads(right[1]['content']);self.assertIn('egraph_feedback',c);c.pop('egraph_feedback');self.assertEqual(b,c)
        for messages in [left,right]:
            blob=json.dumps(messages)
            for forbidden in ['checker.py','private/','probe_01','G1_qualification','SKILL.md','AGENTS.md']:self.assertNotIn(forbidden,blob)
        probes=preflight_messages();self.assertEqual(len(probes),4);self.assertTrue(all(json.loads(m[1]['content'])['round'] in [1,3] for _,_,m in probes))
    def test_13_full_final_mock_and_replay_shared_grade(self):
        root=self.inputs/'cohort';price=verified_pricing(FAKE_PRICE,REG,live=False)
        one=execute_stage(root,'mock',REG,Window(time.monotonic(),REG),price)
        two=execute_stage(self.inputs/'replay','replay',REG,Window(time.monotonic(),REG),None,replay_source=root)
        self.assertEqual((one['snapshots'],one['finals'],one['compile_calls'],one['monitor_replays'],one['monitor_cycles']),(6,2,12,990,204444));self.assertEqual(two['monitor_cycles'],204444)
        self.assertEqual(one['actual_API_requests'],0);self.assertEqual(two['actual_API_requests'],0)
        score1=load(root/'grade/scores.json');score2=load(self.inputs/'replay/grade/scores.json')
        self.assertEqual([r['unresolved_pairs'] for r in score1['rounds']],[38]*6);self.assertEqual(score1['selected_endpoints'],score2['selected_endpoints']);self.assertEqual(score1['inventory_cases'],162)
        self.assertEqual(len(verify(root,REG)),6);self.result.update(mock=one,replay=two,known_benchmark_unknowns_preserved=True)
    def test_14_failed_generation_retry_once_all_failures_frozen(self):
        class AlwaysFail(APIClient):
            def call(client,kind,messages,context,directory):
                if kind!='generation':return super(AlwaysFail,client).call(kind,messages,context,directory)
                directory.mkdir(parents=True,exist_ok=False);i=client.ledger.reserve_api(kind,context);client.ledger.dispatched(i);r=dict(status='request_error',usage=None,actual_cost_usd=None,simulated=True);client.ledger.api_result(i,r);raise Retryable('SYNTHETIC_FAILURE',r)
        out=self.inputs/'cohort';r=execute_stage(out,'mock',REG,Window(time.monotonic(),REG),verified_pricing(FAKE_PRICE,REG,live=False),client_factory=AlwaysFail)
        self.assertEqual(r['request_reservations'],dict(counts=16,generations=12));self.assertEqual(r['compile_calls'],0);self.assertEqual(len(verify(out,REG)),6)
        self.assertTrue(all(c['status']=='invalid' for c in load(out/'final-candidates.json')['candidates']));ledger=load(out/'ledger.json');self.assertEqual(sum(e['kind']=='generation' and e['usage'] is None for e in ledger['events']),12)
    def test_15_fatal_halt_escapes_legacy_case_exception(self):
        swallowed=False
        with self.assertRaises(Halt):
            try:raise Halt('STAGE_DEADLINE')
            except Exception:swallowed=True
        self.assertFalse(swallowed)
    def test_16_round_artifact_tamper_rejected(self):
        # Reuse the completed final mock read-only,copy only one snapshot fixture.
        src=OUT/'test_13_full_final_mock_and_replay_shared_grade/inputs/cohort';verify(src,REG)
        from release import checked
        row=load(src/'all-round-candidates.json')['rounds'][0]
        with patch('release.sha',return_value='0'*64):
            with self.assertRaisesRegex(Halt,'SNAPSHOT_DRIFT'):checked(src,row)
    def test_17_parent_recovery_freezes_missing_without_tools(self):
        out=self.inputs/'partial';out.mkdir();(out/'calls.jsonl').touch();(out/'run.json').write_text(json.dumps(dict(mode='mock',session_ids={'B2_raw':'B','C2_semantic':'C'})))
        preserve_missing(out,REG,'SYNTHETIC_PARENT_TIMEOUT');data=verify(out,REG);self.assertEqual(len(data),6);self.assertTrue(all('NOT_RUN' in x['status'] for x in data))
    def test_18a_scoring_halt_preserves972_planned_cases(self):
        def stop(*args,**kwargs):raise Halt('SYNTHETIC_SCORING_DEADLINE')
        out=self.inputs/'cohort'
        with patch.object(pipeline.grader,'execute',side_effect=stop):
            summary=execute_stage(out,'mock',REG,Window(time.monotonic(),REG),verified_pricing(FAKE_PRICE,REG,live=False))
        interrupted=load(out/'interrupted-grade.json');self.assertEqual(summary['status'],'INCOMPLETE_PRESERVED');self.assertEqual(interrupted['planned_case_pairs'],972)
        self.assertEqual(sum(len(r['cases']) for r in interrupted['rounds']),972);self.assertTrue(all(c['is_unresolved'] for r in interrupted['rounds'] for c in r['cases']))

    def test_18_pricing_artifact_cannot_claim_unknown_free(self):
        p=dict(record_kind='BC_RETEST_VERIFIED_INCLUSIVE_API_PRICING',status='VERIFIED',provider='OpenAI',model='gpt-6.1-sol',coverage={'generation':True,'input_token_count':True},official_evidence=['SYNTHETIC_FORMAT_ONLY'],generation_reserve_micro_usd=241920,count_reserve_micro_usd=None)
        with self.assertRaisesRegex(Halt,'COUNT_PRICE_UNKNOWN'):verified_pricing(p,REG,live=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',required=True,type=Path);a=p.parse_args();OUT=a.record;OUT.mkdir(parents=True,exist_ok=False);source=OUT/'executed-source';source.mkdir()
    files=[*HERE.glob('*.py'),ROOT/'test2/configs/controller_done_bc_retest_v1.json'];hashes={}
    for f in files:
        name=f.relative_to(ROOT).as_posix();t=source/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,t);hashes[name]=sha(f)
    start=time.monotonic()
    with patch('subprocess.Popen',side_effect=AssertionError('NO_REAL_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_REAL_RUN')),patch('os.killpg',side_effect=AssertionError('NO_REAL_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_REAL_SLEEP')):
        with (OUT/'unittest.log').open('x') as log:result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AdapterTests))
    summary=dict(status='PASS' if result.wasSuccessful() else 'FAIL_RETAINED',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),seconds=time.monotonic()-start,actual_API_SDK_credential_SV_tools=0,source_sha256=hashes,scope='Pure fake-tools stage/mock/replay,not a live B/C experiment')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
