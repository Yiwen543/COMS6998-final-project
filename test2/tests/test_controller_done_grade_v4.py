import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from controller_monitor_live import ROW_INPUTS,OUTPUTS
from controller_done_case_v4 import grade,unresolved,summarize,oracle_by_type
from controller_done_grade_v4 import assess,inventory


class GradeV4Tests(unittest.TestCase):
    def fixture(self,alarms=(),unknown=(),complete=True):
        rows=[dict(cycle=i,inputs={k:int(k in ('m_ready','h_ready') or i==0 and k=='rst') for k in ROW_INPUTS},pre={k:0 for k in OUTPUTS},post={k:0 for k in OUTPUTS}) for i in range(4)]
        blob=json.dumps(rows,sort_keys=True,indent=2).encode();n=len(rows);samples=[(i,p) for i in range(n) for p in ('pre','post') if i or p=='post']
        if not complete:samples=samples[:3]
        raw=''.join(f"MON {i} {p} 000001 11111{'x' if (i,p) in unknown else '0' if (i,p) in alarms else '1'}\n" for i,p in samples)+('REPLAY_COMPLETE\n' if complete else '')
        props=[]
        for slot in range(6):
            u=[list(p) for p in samples if p in unknown] if slot==0 else [];f=[list(p) for p in samples if p in alarms] if slot==0 else []
            props.append(dict(id=f'P{slot}',checks=len(samples)-len(u) if slot==0 else 0,failures=f,unknown=u,end_sample_checks=int(slot==0 and complete and (n-1,'post') not in unknown)))
        result=dict(complete=complete,properties=props,cycles=sum(p=='post' for _,p in samples),samples=len(samples),attempted_cycles=n,rows_sha256=hashlib.sha256(json.dumps(rows,separators=(',',':'),sort_keys=True).encode()).hexdigest(),raw_log_sha256=hashlib.sha256(raw.encode()).hexdigest(),trace_done_sample=[n-1,'post'],safety_projection=False)
        label=dict(source='N01',simulator='iverilog',trace='unit_synthetic',status='complete',cycles=n,rows_sha256=hashlib.sha256(blob).hexdigest(),verdict='FAIL',unknown_records=0,first_safety_failure=dict(cycle=1,phase='post'),end_only=False,response_completion=False,input_completion=True)
        return label,blob,result,raw.encode()

    def test_ordinary_and_marker_paths_stay_separate(self):
        r=grade(*self.fixture(alarms={(3,'post')}));self.assertFalse(r['definite_detection']['safety']);self.assertTrue(r['definite_detection']['input_completion']);self.assertTrue(r['marker_only_safety_signal'])
        r=grade(*self.fixture(alarms={(2,'pre'),(3,'post')}));self.assertTrue(r['definite_detection']['safety']);self.assertFalse(r['definite_detection']['input_completion'])

    def test_row_and_cycle_mismatches_are_unresolved_not_detection(self):
        for field in ('label_cycle','replay_cycle','label_hash','replay_hash','marker'):
            l,b,r,raw=self.fixture(alarms={(3,'post')})
            if field=='label_cycle':l['cycles']+=1
            elif field=='replay_cycle':r['attempted_cycles']+=1
            elif field=='label_hash':l['rows_sha256']='wrong'
            elif field=='replay_hash':r['rows_sha256']='wrong'
            else:r['trace_done_sample']=[0,'post']
            case=grade(l,b,r,raw);self.assertEqual(case['status'],'replay_binding_unresolved');self.assertTrue(case['is_unresolved']);self.assertFalse(any(case['definite_detection'].values()))

    def test_saved_non_graded_case_is_carried_without_result_keys(self):
        label,_,_,_=self.fixture();saved=dict(status='reference_infrastructure_unresolved',reason='synthetic failure')
        case,result=assess(label,lambda:dict(non_graded_case=saved));self.assertIsNone(result);self.assertEqual(case['carried_saved_case'],saved);self.assertTrue(case['is_unresolved'])

    def test_reference_failure_never_reads_missing_rows(self):
        label,_,_,_=self.fixture();label['status']='compile_error'
        case,result=assess(label,lambda:(_ for _ in ()).throw(AssertionError('must not read rows')))
        self.assertEqual(case['status'],'reference_infrastructure_unresolved');self.assertIsNone(result)

    def test_candidate_unknown_and_incomplete_replay_retained(self):
        r=grade(*self.fixture(alarms={(3,'post')},unknown={(1,'pre')}));self.assertTrue(r['is_unresolved']);self.assertEqual(r['candidate_unknown_samples_including_marker'],1);self.assertTrue(r['definite_detection']['input_completion']);self.assertFalse(r['fully_resolved_detection']['input_completion'])
        r=grade(*self.fixture(alarms={(1,'post')},complete=False));self.assertEqual(r['status'],'replay_infrastructure_unresolved');self.assertTrue(r['is_unresolved']);self.assertFalse(any(r['definite_detection'].values()))

    def test_raw_bit_disagreement_and_malformed_result_are_unresolved(self):
        l,b,r,raw=self.fixture(alarms={(3,'post')});r['properties'][0]['failures']=[]
        self.assertEqual(grade(l,b,r,raw)['status'],'replay_binding_unresolved')
        r.pop('rows_sha256');self.assertEqual(grade(l,b,r,raw)['status'],'replay_binding_unresolved')

    def test_all_planned_pairs_retained_even_if_reference_inventory_missing(self):
        labels=inventory([]);self.assertEqual(len(labels),162)
        s=summarize([unresolved(l,'reference_infrastructure_unresolved') for l in labels]);self.assertEqual(s['raw_fault_pairs'],144);self.assertEqual(s['raw_fault_types'],12);self.assertEqual(s['unresolved_pairs'],162);self.assertFalse(s['correct_control_gate'])

    def test_explicit_per_type_FAIL_with_unknown(self):
        label,_,_,_=self.fixture();a=unresolved(label,'test');b=copy.deepcopy(a);b['oracle_unknown_records']=1
        x=oracle_by_type([a,b])['N01'];self.assertEqual(x['FAIL_with_oracle_unknown_pairs'],1);self.assertEqual(x['FAIL_without_oracle_unknown_pairs'],1);self.assertEqual(x['raw_pairs'],2)

    def test_backend_loading_failure_becomes_a_case(self):
        label,_,_,_=self.fixture();case,_=assess(label,lambda:(_ for _ in ()).throw(FileNotFoundError('syntheticmissing')))
        self.assertEqual(case['status'],'evidence_infrastructure_unresolved');self.assertTrue(case['is_unresolved'])


if __name__=='__main__':unittest.main()
