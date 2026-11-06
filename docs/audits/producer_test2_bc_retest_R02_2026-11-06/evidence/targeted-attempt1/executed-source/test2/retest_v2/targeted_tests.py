"""R02 delta checks only: no live API, keys, processes, SV or full mock replay."""
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch
from types import SimpleNamespace
import argparse,copy,json,shutil,socket,ssl,time,unittest
import api,pipeline
from resources import Halt,Ledger,Window,financial_policy,fingerprint,sha,trusted_success
from gates import authorize
from release import verify

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REG_PATH=ROOT/'test2/configs/controller_done_bc_retest_v2.json'
REG=json.loads(REG_PATH.read_text())
BASIS=financial_policy(ROOT,REG)
OUT=None

def success(inputs=64000,outputs=8192):
    return dict(status='completed',provider_status='completed',returned_model='gpt-6.1-sol',returned_service_tier='default',long_cache_write=False,unexpected_output_type=False,usage=dict(input_tokens=inputs,output_tokens=outputs,total_tokens=inputs+outputs,cached_input_tokens=None,reasoning_output_tokens=None),output_text=json.dumps(pipeline.mock_candidate()),request_issued=True)

class DeltaChecks(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir()
        self.window=Window(0,REG,clock=lambda:100)
        self.ledger=Ledger(self.folder/'ledger.json',REG,BASIS,self.window,'mock')
        self.result=dict(scope='R02_TARGETED_PURE_CHECK_NOT_LIVE_OR_FULL_MOCK',actual_API_key_process_SV=0)
    def tearDown(self):
        pipeline.dump(self.folder/'check.json',self.result)
    def reserve(self):
        index=self.ledger.reserve_api('generation',{'synthetic':True});self.ledger.dispatched(index);return index
    def test_01_exact_policy_and_user_confirmation(self):
        self.assertEqual(BASIS,dict(generation=5910168,input_times10=55,output_times10=165,ceiling=20000000))
        self.assertEqual(sha(ROOT/REG['user_zero_count_confirmation']),REG['user_zero_count_confirmation_sha256'])
        altered=copy.deepcopy(REG);altered['cost_basis_sha256']='0'*64
        with self.assertRaisesRegex(Halt,'FINANCIAL_SOURCE_DRIFT'):financial_policy(ROOT,altered)
    def test_02_remote_count_is_disabled_before_reservation(self):
        before=sha(self.ledger.path)
        with self.assertRaisesRegex(Halt,'REMOTE_COUNT_DISABLED'):self.ledger.reserve_api('count',{})
        self.assertEqual(before,sha(self.ledger.path));self.assertEqual(self.ledger.state['counts_reserved'],0)
    def test_03_three_unknown_reserves_refuse_fourth(self):
        for _ in range(3):
            index=self.reserve();self.ledger.api_result(index,dict(status='request_error',usage=None,request_issued='UNKNOWN_NOT_ZERO'))
        self.assertEqual(self.ledger.state['financial_commitment_micro_usd'],17730504)
        with self.assertRaisesRegex(Halt,'USD20_PRE_DISPATCH_REFUSAL'):self.reserve()
        self.assertEqual(self.ledger.state['generations_reserved'],3)
        self.assertTrue(all(e['settled_upper_micro_usd'] is None for e in self.ledger.state['events']))
    def test_04_twelve_trusted_successes_settle_upper_once_each(self):
        for _ in range(12):
            index=self.reserve();record=success();self.ledger.api_result(index,record)
            self.assertEqual(self.ledger.settle(index,record),487168)
        state=self.ledger.state
        self.assertEqual(state['settled_upper_micro_usd'],5846016)
        self.assertEqual(state['financial_commitment_micro_usd'],5846016)
        self.assertEqual(state['unresolved_reservations_micro_usd'],0)
        self.assertEqual(state['total_reservations_micro_usd'],12*5910168)
        self.assertEqual(state['unused_reservation_released_micro_usd'],12*(5910168-487168))
        self.assertEqual(len(state['journal']),24);self.assertIsNone(state['actual_invoice_usd'])
        with self.assertRaisesRegex(Halt,'API_REQUEST_CAP'):self.reserve()
    def test_05_invalid_or_unknown_response_keeps_full_reservation(self):
        variants=[]
        for field,value in [('provider_status','incomplete'),('returned_model','OTHER'),('returned_service_tier','flex'),('long_cache_write',True),('unexpected_output_type',True),('output_text','INVALID_JSON'),('output_text','[]')]:
            r=success();r[field]=value;variants.append(r)
        for field,value in [('input_tokens',None),('input_tokens',True),('output_tokens',8193),('total_tokens',1),('cached_input_tokens',64001),('reasoning_output_tokens',8193)]:
            r=success();r['usage'][field]=value;variants.append(r)
        r=success();r['usage']=None;variants.append(r)
        index=self.reserve()
        for record in variants:
            with self.assertRaises(Halt):self.ledger.settle(index,record)
            self.assertEqual(self.ledger.state['financial_commitment_micro_usd'],5910168)
            self.assertEqual(len(self.ledger.state['journal']),1)
        self.result['failure_contract_fixtures']=len(variants)
    def test_06_actual_input_over_target_not_qualified(self):
        index=self.reserve();record=success(inputs=64001);self.ledger.api_result(index,record)
        with self.assertRaisesRegex(Halt,'ACTUAL_INPUT_OVER_TARGET_OR_INVALID_NOT_QUALIFIED'):self.ledger.settle(index,record)
        saved=json.loads(self.ledger.path.read_text())
        self.assertEqual(saved['events'][0]['result']['usage']['input_tokens'],64001)
        self.assertEqual(saved['financial_commitment_micro_usd'],5910168)
        self.assertIsNone(saved['events'][0]['settled_upper_micro_usd'])
    def test_07_optional_usage_subsets_unknown_are_not_free_tokens(self):
        r=success();usage,parsed=trusted_success(r)
        self.assertIsNone(usage['cached_input_tokens']);self.assertIsNone(usage['reasoning_output_tokens'])
        index=self.reserve();self.ledger.api_result(index,r)
        self.assertEqual(self.ledger.settle(index,r),487168)
        self.assertEqual(parsed,pipeline.mock_candidate())
    def test_08_duplicate_settlement_is_refused(self):
        index=self.reserve();r=success();self.ledger.api_result(index,r);self.ledger.settle(index,r);before=sha(self.ledger.path)
        with self.assertRaisesRegex(Halt,'DUPLICATE_OR_INVALID_SETTLEMENT'):self.ledger.settle(index,r)
        self.assertEqual(before,sha(self.ledger.path))
    def test_09_complete_initial_payload_estimates_are_not_exact_counts(self):
        values=pipeline.local_admissions()
        for arm in pipeline.ARMS:
            payload=api.request_payload(pipeline.old.messages(arm,1),pipeline.runtime.SCHEMA)
            self.assertEqual(set(payload),api.PAYLOAD_KEYS);self.assertEqual(payload['input'][0]['role'],'system')
            self.assertEqual(payload['text']['format']['schema'],pipeline.runtime.SCHEMA)
            admission=values[arm];self.assertEqual(admission['UTF8bytes'],len(api.payload_bytes(payload)))
            self.assertEqual(admission['value'],(admission['UTF8bytes']*2+4)//5+4096)
            self.assertLessEqual(admission['value'],64000);self.assertTrue(admission['not_exact_token_count'])
            self.assertTrue(admission['not_server_input_hardcap'])
        self.result['complete_initial_payload_admissions']=values
    def test_10_over_estimate_refused_before_reserve_or_child(self):
        client=pipeline.APIClient(self.folder,REG,self.ledger,self.window,'live')
        messages=[dict(role='system',content='SYNTHETIC'),dict(role='user',content='x'*160000)]
        with self.assertRaisesRegex(Halt,'LOCAL_ESTIMATE_OVER_TARGET_NO_DISPATCH'):client.call('generation',messages,{},self.folder/'attempt')
        self.assertEqual(self.ledger.state['generations_reserved'],0)
        self.assertTrue((self.folder/'attempt/input-estimate.json').is_file())
    def test_11_fixed_https_single_post_no_sdk(self):
        calls=[];body=json.dumps(dict(status='completed',fixture='NOT_PROVIDER')).encode()
        class FakeConnection:
            def __init__(self,host,timeout,context):
                calls.append(('connect',host,timeout));self.context=context
                if context.verify_mode!=ssl.CERT_REQUIRED or not context.check_hostname:raise AssertionError('TLS_INSECURE')
            def request(self,method,path,body,headers):
                calls.append(('request',method,path));self.payload=json.loads(body)
                if headers.get('Authorization')!='Bearer SYNTHETIC_NOT_CREDENTIAL':raise AssertionError('HEADER_FIXTURE')
            def getresponse(self):return SimpleNamespace(status=200,read=lambda limit:body)
            def close(self):calls.append(('close',))
        payload=api.request_payload([dict(role='user',content='PUBLIC_SYNTHETIC')],{})
        data,status=api.post_json(payload,'SYNTHETIC_NOT_CREDENTIAL',10,FakeConnection)
        self.assertEqual(status,200);self.assertEqual(data['fixture'],'NOT_PROVIDER')
        self.assertEqual(calls,[('connect','api.openai.com',10),('request','POST','/v1/responses'),('close',)])
        self.result['calls_without_headers_or_credentials']=calls
    def test_12_http_errors_do_not_redirect_read_body_or_retry(self):
        for status in [301,400,401,429,500]:
            events=[]
            class FakeConnection:
                def __init__(self,*args,**kw):events.append('connect')
                def request(self,*args,**kw):events.append('POST')
                def getresponse(self):return SimpleNamespace(status=status,read=lambda limit:(_ for _ in ()).throw(AssertionError('NO_ERROR_BODY')))
                def close(self):events.append('close')
            with self.assertRaises(api.HTTPFailure) as ctx:api.post_json(api.request_payload([],{}),'SYNTHETIC_NOT_CREDENTIAL',10,FakeConnection)
            self.assertEqual(ctx.exception.status,status);self.assertEqual(events,['connect','POST','close'])
    def test_13_explicit_ca_validation_no_network(self):
        context=ssl.create_default_context(cafile=api.CA_FILE)
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED);self.assertTrue(context.check_hostname);self.assertGreater(context.cert_store_stats()['x509_ca'],0)
        self.result['TLS_metadata']=dict(cafile=api.CA_FILE,x509_ca=context.cert_store_stats()['x509_ca'],CERT_REQUIRED=True,check_hostname=True,network_probe=False)
        empty=SimpleNamespace(verify_mode=ssl.CERT_REQUIRED,check_hostname=True,cert_store_stats=lambda:{'x509_ca':0})
        with patch.object(api.ssl,'create_default_context',return_value=empty),patch.object(api.http.client,'HTTPSConnection',side_effect=AssertionError('NO_CONNECT')):
            with self.assertRaisesRegex(Halt,'TLS_TRUST_STORE_REQUIRED'):api.post_json(api.request_payload([],{}),'SYNTHETIC_NOT_CREDENTIAL',10)
    def test_14_bad_deadline_and_request_rejected_before_connection(self):
        with patch.object(api.http.client,'HTTPSConnection',side_effect=AssertionError('NO_CONNECT')):
            for timeout in [0,0.05,121,None]:
                with self.assertRaisesRegex(Halt,'HTTP_DEADLINE_EXHAUSTED'):api.post_json(api.request_payload([],{}),'SYNTHETIC_NOT_CREDENTIAL',timeout)
            payload=api.request_payload([],{});payload['tools']=[]
            with self.assertRaisesRegex(Halt,'HTTP_REQUEST_CONTRACT'):api.post_json(payload,'SYNTHETIC_NOT_CREDENTIAL',10)
    def test_15_zero_count_financial_lease_guard(self):
        root=self.folder/'SYNTHETIC_ROOT';out=(root/REG['run_root']).resolve();out.mkdir(parents=True)
        messages=[dict(role='user',content='PUBLIC_SYNTHETIC')];schema={'fixture':True}
        ledger=Ledger(out/'ledger.json',REG,BASIS,self.window,'live')
        index=ledger.reserve_api('generation',dict(messages_sha256=fingerprint(messages),schema_sha256=fingerprint(schema)));ledger.dispatched(index)
        lease=Path(str(out)+'-supervision')/'worker-lease.json';lease.parent.mkdir();pipeline.dump(lease,dict(start=0,out=str(out),mode='live',supervisor_pid=111,synthetic_not_authority=True))
        request=dict(kind='generation',ledger_path=str(ledger.path),stage_start=0,deadline_monotonic=3590,reservation_index=index,messages=messages,schema=schema,lease_path=str(lease),lease_sha256=sha(lease),parent_worker_pid=222,stage_pgid=222)
        check=lambda:api.verify_reservation(root,REG,request,BASIS,clock=lambda:100,parent_pid=222,group=222)
        self.assertEqual(check(),out)
        ledger.state['financial_commitment_micro_usd']-=1;ledger.save()
        with self.assertRaisesRegex(Halt,'FINANCIAL_LEDGER_INVARIANT'):check()
        ledger.state['financial_commitment_micro_usd']+=1;ledger.state['counts_reserved']=1;ledger.save()
        with self.assertRaisesRegex(Halt,'LEDGER_LIMIT_DRIFT'):check()
    def test_16_exclusive_claim_and_no_execute_fail_closed(self):
        api.claim_reservation(self.folder,0,'generation');before=sha(self.folder/'api-claims/0.json')
        with self.assertRaises(FileExistsError):api.claim_reservation(self.folder,0,'generation')
        self.assertEqual(before,sha(self.folder/'api-claims/0.json'))
        with self.assertRaisesRegex(Halt,'EXACT_EXECUTE_ABSENT'):authorize(ROOT,REG,self.folder/'ABSENT_EXECUTE.json')
    def test_17_narrow_six_round_stub_zero_count_not_full_mock(self):
        target=self.folder/'NARROW_STUB_STAGE';order=[]
        def develop(candidate,directory,tools):
            compiled=directory/'compiled';compiled.mkdir()
            for name in ['candidate.sv','candidate.json','replay.vvp']:(compiled/name).write_text('INERT_STUB_NOT_COMPILED')
            return dict(status='compiled',fixture='STUB_NO_COMPILER_OR_REPLAY')
        def grade(root,out):
            rounds=verify(root,REG);self.assertEqual(len(rounds),6);order.append('all6_frozen_before_stub_grade')
            return dict(rounds=[dict(arm=r['arm'],round=r['round'],score='NOT_SCORED_STUB') for r in rounds])
        with patch.object(pipeline.old,'verify_data'),patch.object(pipeline,'develop',side_effect=develop),patch.object(pipeline.grader,'execute',side_effect=grade):
            summary=pipeline.execute_stage(target,'mock',REG,self.window,BASIS)
        ledger=json.loads((target/'ledger.json').read_text());calls=[json.loads(line) for line in (target/'calls.jsonl').read_text().splitlines()]
        self.assertEqual([(row['arm'],row['round']) for row in calls],[tuple(row) for row in REG['schedule']])
        self.assertEqual(ledger['counts_reserved'],0);self.assertEqual(ledger['generations_reserved'],6)
        self.assertEqual(ledger['compile_calls'],0);self.assertEqual(ledger['monitor_replays'],0);self.assertEqual(ledger['monitor_cycles'],0)
        self.assertEqual(summary['actual_API_requests'],0);self.assertEqual(order,['all6_frozen_before_stub_grade'])
        self.assertTrue(summary['not_new_model_evidence']);self.result['not_full_mock_or_grading']=True
    def test_18_unknown_failure_halts_remaining_and_retains_972_pairs(self):
        target=self.folder/'NARROW_FAILURE_STAGE'
        class FailureClient(pipeline.APIClient):
            def generate(self,messages,context,directory):
                index=self.ledger.reserve_api('generation',context);self.ledger.dispatched(index)
                self.ledger.api_result(index,dict(status='request_error',usage=None,request_issued='UNKNOWN_NOT_ZERO'))
                raise Halt('SYNTHETIC_UNKNOWN_KEEP_FULL_RESERVE')
        with patch.object(pipeline.old,'verify_data'),patch.object(pipeline,'develop',side_effect=AssertionError('NO_DEVELOP')),patch.object(pipeline.grader,'execute',side_effect=AssertionError('NO_GRADE')):
            summary=pipeline.execute_stage(target,'mock',REG,self.window,BASIS,client_factory=FailureClient)
        ledger=json.loads((target/'ledger.json').read_text());grade=json.loads((target/'interrupted-grade.json').read_text())
        self.assertEqual(len(verify(target,REG)),6);self.assertEqual(ledger['generations_reserved'],1)
        self.assertEqual(ledger['financial_commitment_micro_usd'],5910168);self.assertEqual(ledger['unresolved_reservations_micro_usd'],5910168)
        self.assertEqual(summary['status'],'INCOMPLETE_PRESERVED');self.assertEqual(grade['planned_case_pairs'],972)
        self.assertEqual(sum(len(r['cases']) for r in grade['rounds']),972)
        self.result['remaining_cases_unresolved_not_pass']=972

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record',required=True,type=Path);args=parser.parse_args();OUT=args.record.resolve();OUT.mkdir(parents=True,exist_ok=False)
    source=OUT/'executed-source';source.mkdir();bindings={}
    paths=[*HERE.glob('*.py'),REG_PATH,*[ROOT/REG[k] for k in ['financial_policy','method_addendum','cost_basis','original_authorization','user_zero_count_confirmation']]]
    for path in paths:
        name=path.relative_to(ROOT).as_posix();dest=source/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest);bindings[name]=sha(path)
    original_read_text=Path.read_text;original_read_bytes=Path.read_bytes
    def checked_read(method):
        def read(path,*args,**kw):
            if '/build/private/' in path.absolute().as_posix():raise AssertionError('NO_PRIVATE_CREDENTIAL_READ_OR_HASH')
            return method(path,*args,**kw)
        return read
    start=time.monotonic()
    with ExitStack() as stack:
        for name in ['subprocess.Popen','subprocess.run','os.killpg','time.sleep','socket.create_connection','socket.socket.connect']:
            stack.enter_context(patch(name,side_effect=AssertionError('NO_PROCESS_SIGNAL_SLEEP_OR_NETWORK')))
        stack.enter_context(patch.object(Path,'read_text',checked_read(original_read_text)))
        stack.enter_context(patch.object(Path,'read_bytes',checked_read(original_read_bytes)))
        with (OUT/'unittest.log').open('x') as log:result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DeltaChecks))
    summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),seconds=time.monotonic()-start,executed_source_sha256=bindings,actual_API_key_process_SV=0,completed_full_mock_rerun=False,G1_rerun=False,scope='Only R02 changed financial/transport/admission/orchestration branches;stub grade is not scientific score')
    pipeline.dump(OUT/'summary.json',summary);print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
