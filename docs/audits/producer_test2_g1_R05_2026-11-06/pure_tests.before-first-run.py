"""Focused saved-log reader regressions; no native/simulator/authority execution."""
from pathlib import Path
from unittest.mock import patch
import argparse,hashlib,json,re,shutil,time,unittest
from native_evidence import cover_evidence
from observations import parse_vcd
R=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;OUT=None
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class SavedCoverTests(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/self._testMethodName;self.folder.mkdir();self.inputs=self.folder/'inputs';self.inputs.mkdir()
        self.result={'scope':'OFFLINE_READER_ONLY_NO_QUALIFICATION','real_tool_calls':0}
    def tearDown(self):
        (self.folder/'result.json').write_text(json.dumps(self.result,indent=2)+'\n')
        files={str(p.relative_to(self.inputs)):sha(p) for p in self.inputs.rglob('*') if p.is_file()}
        (self.folder/'input-bindings.json').write_text(json.dumps(files,indent=2)+'\n')
    def fixture(self,qc='QC01'):
        version='v4' if qc=='QC01' else 'v3'
        old=R/f'test2/results/g1-qualification-{version}/jobs/{qc}-cover'
        old_source=R/f'test2/g1_{version}/sources/{qc}_formal.sv'
        for name in ['stdout.log','stderr.log','receipt.json','trace.vcd']:shutil.copy2(old/name,self.inputs/name)
        self.source=self.inputs/'source.sv';shutil.copy2(old_source,self.source)
        self.binding={'source_log_path':str(old_source),'argv':json.loads((old/'receipt.json').read_text())['argv'],'fixture_origin':'ACTUAL_SAVED_'+version+'_'+qc}
        self.rebind();return old
    def rebind(self):
        for name in ['stdout.log','stderr.log','receipt.json','trace.vcd']:
            self.binding[name+'_sha256']=sha(self.inputs/name) if (self.inputs/name).exists() else None
        self.binding['source_sha256']=sha(self.source)
    def replace_stdout(self,transform):
        p=self.inputs/'stdout.log';p.write_text(transform(p.read_text()));self.binding['fixture_origin']='SYNTHETIC_MUTATION_OF_ACTUAL_SAVED_BYTES'
    def check(self,activation):
        (self.inputs/'reader-binding.json').write_text(json.dumps(self.binding,indent=2)+'\n')
        out=cover_evidence(self.inputs,self.source,self.binding);self.result['reader_result']=out
        self.assertEqual(out['activation'],activation);self.assertFalse(out['qualification_credit'])
        self.assertEqual(out['evidence_complete'],activation!='UNKNOWN');return out
    def test_01_real_QC00_passed_reached(self):
        self.fixture('QC00');out=self.check('REACHED')
        self.assertEqual(out['tool_status'],'PASSED');self.assertEqual(out['process_exit_code'],0)
        self.assertEqual(out['assertion_observation'],'NO_FAILURE_REPORTED')
    def test_02_real_QC01_failed_still_reached(self):
        self.fixture();out=self.check('REACHED')
        self.assertEqual(out['tool_status'],'FAILED');self.assertEqual(out['process_exit_code'],1)
        self.assertEqual(out['assertion_observation'],'FAILED');self.assertEqual(out['raw_reached_steps'],[2])
    def test_03_failed_without_target_record_is_unknown(self):
        self.fixture();self.replace_stdout(lambda s:'\n'.join(x for x in s.splitlines() if 'Reached cover statement' not in x)+'\n');self.rebind();self.check('UNKNOWN')
    def test_04_reached_and_unreached_is_unknown(self):
        self.fixture();path=self.binding['source_log_path']
        self.replace_stdout(lambda s:s+f'##   0:00:00  Unreached cover statement at formal_top: {path}:17.5-17.18 ($cover${path}:17$21)\n')
        self.rebind();self.check('UNKNOWN')
    def test_05_wrong_source_id_is_unknown(self):
        self.fixture();self.replace_stdout(lambda s:s.replace('QC01_formal.sv','QC02_formal.sv'));self.rebind();self.check('UNKNOWN')
    def test_06_missing_reached_trace_is_unknown(self):
        self.fixture();(self.inputs/'trace.vcd').unlink();self.rebind();self.check('UNKNOWN')
    def test_07_status_exit_conflict_is_unknown(self):
        self.fixture('QC00');p=self.inputs/'receipt.json';d=json.loads(p.read_text());d['exit_code']=1;p.write_text(json.dumps(d));self.rebind();self.check('UNKNOWN')
    def test_08_trace_activation_conflict_is_unknown(self):
        self.fixture();p=self.inputs/'trace.vcd';v=parse_vcd(p);identifier=v['wires']['formal_top.sampled_active'][0]
        text,count=re.subn(r'(?m)^b[01xz]+ '+re.escape(identifier)+r'$', 'b0 '+identifier,p.read_text());self.assertGreater(count,0);p.write_text(text);self.rebind();self.check('UNKNOWN')
    def test_09_missing_final_status_is_unknown(self):
        self.fixture();self.replace_stdout(lambda s:'\n'.join(x for x in s.splitlines() if 'Status:' not in x)+'\n');self.rebind();self.check('UNKNOWN')
    def test_10_multiple_source_covers_is_unknown(self):
        self.fixture();self.source.write_text(self.source.read_text()+'\n// SYNTHETIC_UNSUPPORTED\ncover(active);\n');self.rebind();self.check('UNKNOWN')
    def test_11_unbound_log_tamper_is_unknown(self):
        self.fixture();self.replace_stdout(lambda s:s+'\n');self.check('UNKNOWN')
    def test_12_explicit_unreached_synthetic_finite_control(self):
        self.fixture();path=self.binding['source_log_path'];p=self.inputs/'stdout.log'
        p.write_text(f'##   0:00:00  Unreached cover statement at formal_top: {path}:17.5-17.18 ($cover${path}:17$21)\n##   0:00:00  Status: FAILED\n')
        (self.inputs/'trace.vcd').unlink();receipt=self.inputs/'receipt.json';d=json.loads(receipt.read_text());d['stdout_sha256']=sha(p);receipt.write_text(json.dumps(d))
        self.binding['fixture_origin']='SYNTHETIC_UNREACHED_FORMAT_CONTROL_NOT_A_REAL_QC_RESULT';self.rebind();out=self.check('UNREACHED')
        self.assertEqual(out['tool_status'],'FAILED');self.assertEqual(out['finite_depth'],8)
    def test_13_failed_reached_without_assert_explanation_unknown(self):
        self.fixture();self.replace_stdout(lambda s:'\n'.join(x for x in s.splitlines() if 'Assert failed' not in x)+'\n');self.rebind();self.check('UNKNOWN')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record',required=True,type=Path);args=parser.parse_args()
    OUT=args.record;OUT.mkdir(exist_ok=False);sources=OUT/'executed-source';sources.mkdir()
    for p in [HERE/'native_evidence.py',HERE/'observations.py',Path(__file__)]:shutil.copy2(p,sources/p.name)
    start=time.monotonic()
    with patch('subprocess.Popen',side_effect=AssertionError('NO_REAL_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_REAL_RUN')),patch('os.killpg',side_effect=AssertionError('NO_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_SLEEP')):
        with (OUT/'unittest.log').open('x') as log:result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SavedCoverTests))
    summary=dict(scope='R05_FOCUSED_SAVED_LOG_READER_NOT_G1_QUALIFICATION',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),seconds=time.monotonic()-start,real_tool_process_signal_sleep_calls=0,source_sha256={p.name:sha(p) for p in sources.iterdir()})
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(int(not result.wasSuccessful()))
