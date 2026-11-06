import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import BASE,sha
from controller_done_data import TASK
from controller_done_codec_v2 import compact,encode_column,decode_column,restore
from controller_done_loop_v2 import count_messages
from controller_release_live import verify_release


class CodecV2Tests(unittest.TestCase):
    def test_column_roundtrip_preserves_json_types_and_nested_fields(self):
        for values in ([],[None]*20,[False,0,True,1,1.0],[[True],[1],[1,2],[1,2]],list(range(50))):
            self.assertEqual(compact(decode_column(encode_column(values))),compact(values))

    def test_full_packets_restore_all_information_and_common_B_C(self):
        packets=[]
        for arm in ('B2_raw','C2_semantic'):
            old=json.loads((TASK/'public/prompt-packets-v1'/(arm+'.json')).read_text());new=json.loads((TASK/'public/prompt-packets-v2'/(arm+'.json')).read_text())
            self.assertEqual(compact(restore(new)),compact(old));packets.append(new)
        c=copy.deepcopy(packets[1]);self.assertEqual(len(c.pop('egraph_feedback')['groups']),4);self.assertEqual(c,packets[0])

    def test_history_stress_and_all_caps_are_unchanged(self):
        from controller_done_loop import count_messages as previous
        for old,new in zip(previous(),count_messages()):
            self.assertEqual(old[:2],new[:2]);a=old[2];b=new[2];self.assertEqual(a[0],b[0]);x=json.loads(a[1]['content']);y=json.loads(b[1]['content'])
            self.assertEqual(compact(restore({k:v for k,v in y.items() if k not in ('module_header','round','previous_candidate','development_feedback')})),compact({k:v for k,v in x.items() if k not in ('module_header','round','previous_candidate','development_feedback')}))
            for k in ('module_header','round','previous_candidate','development_feedback'):self.assertEqual(x[k],y[k])

    def test_new_all36_freezes_replay_and_old_candidates_identical(self):
        r=BASE/'results';a=verify_release(r/'controller-done-mock-v2');b=verify_release(r/'controller-done-replay-v2');old=verify_release(r/'controller-done-mock-v1')
        self.assertEqual(len(a),36);self.assertEqual(len(b),36)
        for x in a:
            y=next(y for y in b if (x['arm'],x['repetition'],x['round'])==(y['arm'],y['repetition'],y['round']))
            z=next(y for y in old if (x['arm'],x['repetition'],x['round'])==(y['arm'],y['repetition'],y['round']))
            for f in ('prompt.json','response.json','development-feedback.json','compiled/candidate.sv'):self.assertEqual(sha(r/'controller-done-mock-v2'/x['directory']/f),sha(r/'controller-done-replay-v2'/y['directory']/f))
            self.assertEqual(sha(r/'controller-done-mock-v2'/x['directory']/'compiled/candidate.sv'),sha(r/'controller-done-mock-v1'/z['directory']/'compiled/candidate.sv'))

    def test_new_prompts_keep_private_evidence_out(self):
        for _,_,messages in count_messages():
            text=compact(messages)
            for forbidden in ('reference/frozen','private/','probe_01','N01.v','AGENTS.md','check_rows','expected_verdict'):self.assertNotIn(forbidden,text)


if __name__=='__main__':unittest.main()
