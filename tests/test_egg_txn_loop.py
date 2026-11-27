"""Unassisted shared initial response, exact feedback fork and mock transport controls."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from egg_txn_loop import ARMS, FIXTURE_INITIAL, REFERENCES, SYSTEM, TASK, fixture_revision, run

BINARY=Path(os.environ.get('CARGO_TARGET_DIR',ROOT/'egraph/target'))/'release/egg_cube_proofs'
CORPUS=ROOT/'results/milestone3/frame-faults'
CONFIG={'model':'unit-test-model','reasoning_effort':'low','max_output_tokens':4096,'transport':'OpenAI Responses API'}

@unittest.skipUnless(BINARY.is_file(),'build egg_cube_proofs')
class TxnLoopTests(unittest.TestCase):
    def test_fixture_shared_initial_and_feedback_fork(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            r=run(corpus_dir=CORPUS,binary=BINARY,out=out,mode='fixture',trials=1,rounds=2)
            self.assertEqual(r['responses'],7);self.assertEqual(r['provider_api_calls'],0)
            t=out/'trial-01';initial=json.loads((t/'initial/request.json').read_text())['messages']
            self.assertEqual(initial,[{'role':'system','content':SYSTEM},{'role':'user','content':TASK}])
            self.assertNotIn('candidate_diagnoses',initial[-1]['content']);self.assertNotIn('egg_certificates',initial[-1]['content'])
            for arm in ARMS:
                p=t/arm
                one=json.loads((p/'round-01/request.json').read_text())['messages']
                self.assertEqual(one[:2],initial)
                self.assertEqual(json.loads(one[2]['content']),{'monitors':FIXTURE_INITIAL})
                two=json.loads((p/'round-02/request.json').read_text())['messages']
                self.assertEqual(json.loads(two[-2]['content']),{'monitors':fixture_revision(1)})
                self.assertIn((p/'round-01/feedback.txt').read_text().rstrip(),two[-1]['content'])
                self.assertTrue(r['sessions']['trial-01']['arms'][arm]['rounds'][-1]['verified'])
                self.assertEqual(r['sessions']['trial-01']['arms'][arm]['first_verified_round'],2)
            o=json.loads((t/'ordinary/seed/feedback.txt').read_text());e=json.loads((t/'egg/seed/feedback.txt').read_text())
            e.pop('egg_certificates');self.assertEqual(o,e)

    def test_mock_initial_ceiling_not_cherry_picked_or_counted_three_times(self):
        calls=[]
        def provider(messages,schema):
            calls.append(messages)
            return {'id':f'resp_mock_{len(calls)}','model':CONFIG['model'],'requested_model':CONFIG['model'],'status':'completed','http_status':200,'dispatch_attempted':True,'usage':{'input_tokens':100,'output_tokens':50,'total_tokens':150},'output':{'monitors':dict(REFERENCES)}}
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run';r=run(corpus_dir=CORPUS,binary=BINARY,out=out,mode='live',trials=1,rounds=1,provider=provider,provider_config=CONFIG)
            self.assertEqual(len(calls),4) # mocked transport only
            self.assertEqual(r['initial_usage']['total_tokens'],150)
            for arm in ARMS:
                self.assertEqual(r['provider_usage'][arm]['total_tokens'],150)
                self.assertEqual(r['sessions']['trial-01']['arms'][arm]['first_verified_round'],0)
                self.assertEqual(r['sessions']['trial-01']['arms'][arm]['delivered'][0]['egg_checked_rewrites'],0)

if __name__=='__main__':unittest.main()
