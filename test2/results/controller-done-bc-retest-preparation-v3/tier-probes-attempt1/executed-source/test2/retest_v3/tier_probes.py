"""Only P18-R1 repair probes; no API, key, compiler, replay or base suite."""
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch
import argparse,copy,json,shutil,time,unittest
import api,pipeline
from resources import Ledger,Window,financial_policy,sha,fingerprint,require
from release import verify

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
REG_PATH=ROOT/'test2/configs/controller_done_bc_retest_v3.json'
REG=json.loads(REG_PATH.read_text());BASIS=financial_policy(ROOT,REG);OUT=None
COUNTEREXAMPLE=ROOT/'docs/audits/agent_bridge_2026-11-06/P18_bc_retest_preflight/R02-preseal-changed-evidence/missing_tier.input.json'

def provider_fixture():
    original=json.loads(COUNTEREXAMPLE.read_text())['case']['record']
    return dict(status=original['provider_status'],model=original['returned_model'],service_tier=original['returned_service_tier'],usage={k:original['usage'][k] for k in ['input_tokens','output_tokens','total_tokens']},output=[dict(type='message',content=[dict(type='output_text',text=original['output_text'])])],fixture_only=True)

def fixture_client(data):
    class FixtureClient(pipeline.APIClient):
        def call(self,kind,messages,context,directory):
            require(kind=='generation','REMOTE_COUNT_DISABLED');directory.mkdir(parents=True,exist_ok=False)
            admission=api.estimate(api.request_payload(messages,pipeline.runtime.SCHEMA))
            index=self.ledger.reserve_api(kind,dict(context,messages_sha256=fingerprint(messages),schema_sha256=fingerprint(pipeline.runtime.SCHEMA),payload_sha256=admission['payload_sha256'],input_estimate=admission))
            self.ledger.dispatched(index);self.last_index=index
            record=api.provider_result(data,200,admission);record['simulated_contract_fixture']=True
            pipeline.dump(directory/'result.json',record);self.ledger.api_result(index,record)
            return record
    return FixtureClient

class TierProbes(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir();self.window=Window(0,REG,clock=lambda:100)
    def rejected_before_accept_compile_or_next_request(self,data):
        pipeline.dump(self.folder/'raw-provider.fixture.json',data)
        output=self.folder/'SYNTHETIC_FAILURE_STAGE'
        with patch.object(pipeline.old,'verify_data'),patch.object(pipeline,'develop',side_effect=AssertionError('MUST_NOT_ACCEPT_OR_COMPILE')),patch.object(pipeline.grader,'execute',side_effect=AssertionError('MUST_NOT_GRADE')):
            summary=pipeline.execute_stage(output,'mock',REG,self.window,BASIS,client_factory=fixture_client(data))
        ledger=json.loads((output/'ledger.json').read_text());calls=[json.loads(line) for line in (output/'calls.jsonl').read_text().splitlines()]
        self.assertEqual(len(calls),1);self.assertFalse(calls[0]['accepted_response'])
        self.assertEqual(calls[0]['status'],'resource_or_contract_halt');self.assertIn('MODEL_OR_TIER_CONTRACT',summary['halt'])
        self.assertEqual(ledger['generations_reserved'],1);self.assertEqual(ledger['counts_reserved'],0)
        self.assertEqual(ledger['financial_commitment_micro_usd'],5910168);self.assertEqual(ledger['unresolved_reservations_micro_usd'],5910168)
        self.assertEqual(ledger['settled_upper_micro_usd'],0);self.assertEqual(ledger['unused_reservation_released_micro_usd'],0)
        self.assertEqual([item['op'] for item in ledger['journal']],['RESERVE'])
        self.assertEqual(ledger['events'][0]['result']['provider_response'],data)
        self.assertEqual(ledger['events'][0]['result']['usage']['input_tokens'],64000)
        self.assertEqual(ledger['events'][0]['result']['usage']['output_tokens'],8192)
        self.assertEqual(ledger['compile_calls'],0);self.assertEqual(ledger['monitor_replays'],0)
        self.assertEqual(summary['status'],'INCOMPLETE_PRESERVED')
        self.assertTrue(all(item['status']=='NOT_RUN_OR_UNRESOLVED' for item in verify(output,REG)))
        pipeline.dump(self.folder/'probe.json',dict(status='PASS_REJECTED',candidate_accepted=False,compilation_calls=0,next_requests=0,reserve_retained_micro_usd=5910168,SETTLE_events=0,provider_JSON_preserved=True,not_live_model_evidence=True))
    def test_01_missing_tier_field_halts(self):
        data=provider_fixture();del data['service_tier'];self.rejected_before_accept_compile_or_next_request(data)
    def test_02_explicit_null_tier_halts(self):self.rejected_before_accept_compile_or_next_request(provider_fixture())
    def test_03_nondefault_tier_halts(self):
        data=provider_fixture();data['service_tier']='flex';self.rejected_before_accept_compile_or_next_request(data)
    def test_04_explicit_default_64000_8192_settles(self):
        data=provider_fixture();data['service_tier']='default';pipeline.dump(self.folder/'raw-provider.fixture.json',data)
        ledger=Ledger(self.folder/'ledger.json',REG,BASIS,self.window,'mock')
        client=fixture_client(data)(self.folder,REG,ledger,self.window,'mock')
        record,parsed=client.generate([dict(role='user',content='PUBLIC_SYNTHETIC_TIER_PROBE')],{'fixture_only':True},self.folder/'generation')
        self.assertEqual(record['provider_response'],data);self.assertEqual(parsed,json.loads(data['output'][0]['content'][0]['text']))
        self.assertEqual(ledger.state['settled_upper_micro_usd'],487168);self.assertEqual(ledger.state['financial_commitment_micro_usd'],487168)
        self.assertEqual(ledger.state['unresolved_reservations_micro_usd'],0);self.assertEqual(ledger.state['unused_reservation_released_micro_usd'],5423000)
        self.assertEqual([item['op'] for item in ledger.state['journal']],['RESERVE','SETTLE_UPPER_AND_RELEASE_UNUSED'])
        self.assertIsNone(ledger.state['actual_invoice_usd'])
        pipeline.dump(self.folder/'probe.json',dict(status='PASS_TRUSTED_DEFAULT',settled_upper_micro_usd=487168,unused_reservation_released_micro_usd=5423000,not_invoice_or_refund=True,SV_compilation_performed=False,not_live_model_evidence=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record',required=True,type=Path);args=parser.parse_args();OUT=args.record.resolve();OUT.mkdir(parents=True,exist_ok=False)
    bindings={}
    for path in [*HERE.glob('*.py'),REG_PATH,COUNTEREXAMPLE,ROOT/REG['repair_of']['review']]:
        name=path.relative_to(ROOT).as_posix();dest=OUT/'executed-source'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest);bindings[name]=sha(path)
    original_text=Path.read_text;original_bytes=Path.read_bytes
    def protected(method):
        def read(path,*args,**kw):
            if '/build/private/' in path.absolute().as_posix():raise AssertionError('NO_CREDENTIAL_READ_HASH')
            return method(path,*args,**kw)
        return read
    start=time.monotonic()
    with ExitStack() as stack:
        for name in ['subprocess.Popen','subprocess.run','os.killpg','time.sleep','socket.create_connection','socket.socket.connect']:
            stack.enter_context(patch(name,side_effect=AssertionError('NO_PROCESS_NETWORK_SIGNAL_SLEEP')))
        stack.enter_context(patch.object(Path,'read_text',protected(original_text)));stack.enter_context(patch.object(Path,'read_bytes',protected(original_bytes)))
        with (OUT/'unittest.log').open('x') as log:result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TierProbes))
    summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),seconds=time.monotonic()-start,executed_source_sha256=bindings,actual_API_network_keycontent_SV_process_signal=0,R01_R02_base_suites_rerun=False,G1_rerun=False,scope='Only explicit returned tier P18-R1;three synthetic early-halt paths and one trusted default settlement,no real candidate/grade/compiler/replay')
    pipeline.dump(OUT/'summary.json',summary);print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
