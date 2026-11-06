"""Only new lease/reservation deltas;does not rerun completed full mock/replay."""
from pathlib import Path
from unittest.mock import patch
import argparse,copy,hashlib,json,shutil,time,unittest
from api import verify_reservation,claim_reservation
from resources import Halt,fingerprint,sha
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REG=json.loads((ROOT/'test2/configs/controller_done_bc_retest_v1.json').read_text());OUT=None
class Guards(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir();self.root=self.folder/'SYNTHETIC_ROOT';self.root.mkdir();self.out=(self.root/REG['run_root']).resolve();self.out.mkdir(parents=True)
        self.messages=[dict(role='user',content='SYNTHETIC_PUBLIC_FIXTURE')];self.schema={'synthetic':True};lease=Path(str(self.out)+'-supervision')/'worker-lease.json';lease.parent.mkdir()
        lease.write_text(json.dumps(dict(start=0,out=str(self.out),mode='live',supervisor_pid=111,fixture='SYNTHETIC_NOT_AUTHORITY')))
        event=dict(kind='count',status='DISPATCH_ATTEMPTED',dispatch_attempted=True,reserved_micro_usd=1000,context=dict(messages_sha256=fingerprint(self.messages),schema_sha256=fingerprint(self.schema)))
        self.ledger=dict(mode='live',completed=False,halted=None,start_monotonic=0,work_deadline=3590,hard_deadline=3600,counts_reserved=1,generations_reserved=0,reserved_micro_usd=1000,events=[event],fixture='SYNTHETIC_NOT_AUTHORITY')
        (self.out/'ledger.json').write_text(json.dumps(self.ledger));self.request=dict(kind='count',ledger_path=str(self.out/'ledger.json'),stage_start=0,deadline_monotonic=3590,reservation_index=0,messages=self.messages,schema=self.schema,lease_path=str(lease),lease_sha256=sha(lease),parent_worker_pid=222,stage_pgid=222);self.result={'scope':'PURE_GUARD_ONLY_NOT_LIVEAUTHORITY','actual_SDK_API_key_process':0}
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n');(self.folder/'input-bindings.json').write_text(json.dumps({str(p.relative_to(self.root)):sha(p) for p in self.root.rglob('*') if p.is_file()},indent=2)+'\n')
    def check(self,request=None,**kw):return verify_reservation(self.root,REG,request or self.request,{'count':1000},clock=lambda:100,parent_pid=222,group=222,**kw)
    def test_01_matching_synthetic_reservation_no_SDK(self):self.assertEqual(self.check(),self.out)
    def test_02_payload_drift_rejected(self):
        r=copy.deepcopy(self.request);r['messages'][0]['content']='ALTERED'
        with self.assertRaisesRegex(Halt,'PAYLOAD_OR_PRICE_DRIFT'):self.check(r)
    def test_03_clock_reset_rejected(self):
        r=dict(self.request,stage_start=1000)
        with self.assertRaisesRegex(Halt,'STAGE_CLOCK_DRIFT'):self.check(r)
    def test_04_wrong_parent_group_rejected(self):
        r=dict(self.request,stage_pgid=333)
        with self.assertRaisesRegex(Halt,'PARENT_GROUP_REQUIRED'):self.check(r)
    def test_05_claim_exclusive_no_duplicate_dispatch(self):
        claim_reservation(self.out,0,'count');before=sha(self.out/'api-claims/0.json')
        with self.assertRaises(FileExistsError):claim_reservation(self.out,0,'count')
        self.assertEqual(sha(self.out/'api-claims/0.json'),before)
    def test_06_missing_live_ledger_rejected(self):
        r=dict(self.request,ledger_path=str(self.out/'absent.json'))
        with self.assertRaisesRegex(Halt,'WRONG_LIVE_LEDGER'):self.check(r)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',required=True,type=Path);a=p.parse_args();OUT=a.record;OUT.mkdir(parents=True,exist_ok=False);source=OUT/'executed-source';source.mkdir();hashes={}
    for f in [*HERE.glob('*.py'),ROOT/'test2/configs/controller_done_bc_retest_v1.json']:
        name=f.relative_to(ROOT).as_posix();t=source/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,t);hashes[name]=sha(f)
    start=time.monotonic()
    with patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_RUN')),patch('os.killpg',side_effect=AssertionError('NO_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_SLEEP')):
        with (OUT/'unittest.log').open('x') as log:r=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Guards))
    summary=dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful(),seconds=time.monotonic()-start,source_sha256=hashes,actual_SDK_API_key_process=0,completed_full_mock_rerun=False)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not r.wasSuccessful()))
