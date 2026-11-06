"""Synthetic saved-file fixtures; no DUT, monitor, solver, API or replacement oracle."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import controller_done_witness_chain_audit_v1 as a


def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(value,bytes):p.write_bytes(value)
    elif isinstance(value,str):p.write_text(value)
    else:p.write_text(json.dumps(value,sort_keys=True)+'\n')


def fixture(root,reproduced=True,verdict='PASS',unknown=False):
    job=root/'job';phy=job/'physical';inputs=[dict(zip(a.INPUTS,[1,0,0,0,0,0])),dict(zip(a.INPUTS,[0,0,0,0,0,0]))]
    output=dict(zip(a.OUTPUTS,[0,-1,0,-1,0,-1,-1,-1,-1]));rows=[dict(cycle=i,inputs=x,pre=copy.deepcopy(output),post=copy.deepcopy(output)) for i,x in enumerate(inputs)]
    pins=list(a.INPUTS)+list(a.OUTPUTS)+['active','ok'];ids={n:'v'+str(i) for i,n in enumerate(pins)}
    header=['$var integer 32 t smt_step $end','$scope module formal_top $end']
    header += [f'$var wire {1 if n in ("active","ok") else a.WIDTHS[n]} {ids[n]} {n} $end' for n in pins]
    header+=['$upscope $end','$enddefinitions $end'];body=[]
    for i in range(2):
        body += [f'#{i*10}',f'b{i:b} t']
        for n in pins:
            v=inputs[i][n] if n in a.INPUTS else output[n] if n in a.OUTPUTS else 1 if n=='active' else int(i==0)
            body.append('b'+('x' if v==-1 else format(v,'b'))+' '+ids[n])
    vcd='\n'.join(header+body)+'\n';vp=job/'work/engine_0/trace.vcd';write(vp,vcd)
    write(phy/'formal-inputs.json',inputs)
    for sim in ['iverilog','verilator']:
        d=phy/sim;write(d/'inputs.txt',''.join(' '.join(str(x[n]) for n in a.INPUTS)+'\n' for x in inputs));lines=[]
        for i,x in enumerate(inputs):
            pre=[x[n] for n in a.INPUTS]+[output[n] for n in a.OUTPUTS];post=[output[n] for n in a.OUTPUTS]
            for label,vals in [('PRE',pre),('POST',post)]:lines.append(f'{label} {i} '+' '.join('x' if v==-1 else str(v) for v in vals))
        raw=('\n'.join(lines)+'\nLITERAL_COMPLETE 2\n').encode();write(d/'simulation.log',raw);write(d/'rows.json',rows);write(d/'execution.json',dict(status='complete',returncode=0,cycles=2,log_sha256=a.sha(raw),argv=['fixture-only','+INPUTS='+str(d/'inputs.txt')]))
    mon=[]
    for cycle,phase in [(0,'post'),(1,'pre'),(1,'post')]:
        ok='111110' if reproduced and cycle==1 else '11111x' if unknown and cycle==1 else '111111'
        mon.append(f'MON {cycle} {phase} 111111 {ok}')
    raw=('\n'.join(mon)+'\nREPLAY_COMPLETE\n').encode();compressed=gzip.compress(raw,mtime=0);samples,props=a.parse_mon(raw,2);rowhash=a.sha(a.canon(rows));hp=root/'cache'/(rowhash+'.hex');write(hp,a.encode_hex(rows));d=phy/'candidate-replay';write(d/'replay.log.gz',compressed)
    m=dict(complete=True,cycles=2,attempted_cycles=2,samples=len(samples),trace_done_sample=None,safety_projection=True,DUT_inputs_unchanged=True,rows_sha256=rowhash,compressed_log_sha256=a.sha(compressed),raw_log_sha256=a.sha(raw),execution=dict(status='complete',returncode=0,log_sha256=a.sha(raw),argv=['fixture-only','+ROWS='+str(hp),'+LAST=-1']),properties=props);write(d/'result.json',m)
    ref=dict(verdict=verdict,failures=[],unknown=[dict(category='fixture_unknown')] if verdict=='UNRESOLVED' else [])
    p=dict(status='physically_reproduced_prefix_checked' if reproduced else 'unresolved',trace_done=0,finite_completion_proved=False)
    if reproduced:
        write(phy/'reference-prefix-rows.json',rows[:1]);write(phy/'reference.json',ref);p.update(reference_verdict=verdict,reference_failures=ref['failures'],reference_unknown=ref['unknown'],selected_alarm=dict(cycle=1,phase='pre',slot=0,category='UNATTRIBUTED'),reference_last_sample=dict(cycle=0,phase='post'),reference_rows=1,reference_confirmed_selected_alarm=False,formal_alarm_reproduced=True,witness_sha256=a.sha(vcd.encode()),formal_states=2,physical_cycles=4,candidate_monitor_cycles=2,observed_alarm_state=1)
    write(phy/'result.json',p)
    def checker(prefix,**kw):
        assert prefix==rows[:1] and kw==dict(require_drained=False,min_tail=32)
        return copy.deepcopy(ref)
    return job,checker


class WitnessChainTests(unittest.TestCase):
    def run_fixture(self,change=None,**kw):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);job,checker=fixture(root,**kw)
            if change:change(job,root)
            return a.inspect_chain(job,0,a.Saved(root),checker)[0]

    def test_reproduced_prefix_pass_is_not_selected_alarm_confirmation(self):
        r=self.run_fixture();self.assertTrue(r['physical_alarm_reproduced']);self.assertEqual(r['reference_verdict'],'PASS');self.assertFalse(r['reference_confirmed_selected_alarm']);self.assertEqual(r['scientific_adjudication'],'UNRESOLVED')

    def test_reference_unknown_retained(self):
        r=self.run_fixture(verdict='UNRESOLVED');self.assertEqual(r['reference_verdict'],'UNRESOLVED');self.assertTrue(r['reference_unknown'])

    def test_unreproduced_has_no_oracle_verdict(self):
        r=self.run_fixture(reproduced=False);self.assertFalse(r['physical_alarm_reproduced']);self.assertIsNone(r['reference_verdict']);self.assertTrue(r['reference_not_evaluated'])

    def test_candidate_unknown_stays_unresolved_not_physical_alarm(self):
        r=self.run_fixture(reproduced=False,unknown=True);self.assertFalse(r['physical_alarm_reproduced']);self.assertEqual(r['scientific_adjudication'],'UNRESOLVED')

    def test_missing_and_truncated_vcd(self):
        def missing(j,r):(j/'work/engine_0/trace.vcd').unlink()
        self.assertRaises(ValueError,self.run_fixture,missing)
        def truncated(j,r):
            p=j/'work/engine_0/trace.vcd';s=p.read_text().splitlines();p.write_text('\n'.join(s[:-5])+'\n')
        self.assertRaises(ValueError,self.run_fixture,truncated)

    def test_reduced_monitor_width_valid_but_selected_bit_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            job,_=fixture(Path(tmp));text=(job/'work/engine_0/trace.vcd').read_text();self.assertEqual(a.decode_vcd(text,0)[2],1);self.assertRaisesRegex(ValueError,'selected slot',a.decode_vcd,text,1)

    def test_literal_input_and_cycle_shift_rejected(self):
        for target in ['formal-inputs.json','iverilog/inputs.txt']:
            def alter(j,r):
                p=j/'physical'/target
                if p.suffix=='.json':x=json.loads(p.read_text());x[1]['s_data']=1;write(p,x)
                else:p.write_text(p.read_text().replace('0 0 0 0 0 0','0 0 1 0 0 0'))
            with self.subTest(target=target):self.assertRaisesRegex(ValueError,'input|transport',self.run_fixture,alter)

    def test_raw_physical_change_even_if_execution_hash_updated(self):
        def alter(j,r):
            d=j/'physical/iverilog';p=d/'simulation.log';p.write_text(p.read_text().replace('POST 1 0 x','POST 1 1 x'));e=json.loads((d/'execution.json').read_text());e['log_sha256']=a.sha(p.read_bytes());write(d/'execution.json',e)
        self.assertRaisesRegex(ValueError,'raw physical log/rows',self.run_fixture,alter)

    def test_saved_rows_tamper(self):
        def alter(j,r):
            p=j/'physical/verilator/rows.json';x=json.loads(p.read_text());x[1]['pre']['s_ready']=1;write(p,x)
        self.assertRaisesRegex(ValueError,'raw physical log/rows',self.run_fixture,alter)

    def test_missing_physical_phase_and_duplicate_row(self):
        for duplicate in [False,True]:
            def alter(j,r):
                p=j/'physical/iverilog/simulation.log';s=p.read_text();p.write_text(s+s.splitlines()[0]+'\n' if duplicate else '\n'.join(x for x in s.splitlines() if not x.startswith('POST 1')))
            with self.subTest(duplicate=duplicate):self.assertRaisesRegex(ValueError,'missing/truncated/duplicate',self.run_fixture,alter)

    def test_mon_alteration_with_fresh_log_hashes_still_detected(self):
        def alter(j,r):
            d=j/'physical/candidate-replay';p=d/'replay.log.gz';raw=gzip.decompress(p.read_bytes()).replace(b'111110',b'111111');comp=gzip.compress(raw,mtime=0);write(p,comp);m=json.loads((d/'result.json').read_text());m['raw_log_sha256']=m['execution']['log_sha256']=a.sha(raw);m['compressed_log_sha256']=a.sha(comp);write(d/'result.json',m)
        self.assertRaisesRegex(ValueError,'MON/property',self.run_fixture,alter)

    def test_raw_mon_phase_offset(self):
        raw=b'MON 0 post 111111 111111\nMON 1 post 111111 111110\nMON 1 pre 111111 111110\nREPLAY_COMPLETE\n';self.assertRaisesRegex(ValueError,'wrong phase',a.parse_mon,raw,2)

    def test_prefix_wrong_phase_length_and_slot(self):
        for field in ['prefix','slot','phase','scope']:
            def alter(j,r):
                d=j/'physical'
                if field=='prefix':write(d/'reference-prefix-rows.json',json.loads((d/'iverilog/rows.json').read_text()));return
                p=d/'result.json';x=json.loads(p.read_text())
                if field in ['slot','phase']:x['selected_alarm'][field]=1 if field=='slot' else 'post'
                else:x['reference_last_sample']['cycle']=1
                write(p,x)
            with self.subTest(field=field):self.assertRaisesRegex(ValueError,'prefix|slot/phase',self.run_fixture,alter)

    def test_selected_alarm_confirmation_upgrade_rejected(self):
        def alter(j,r):
            p=j/'physical/result.json';x=json.loads(p.read_text());x['reference_confirmed_selected_alarm']=True;write(p,x)
        self.assertRaisesRegex(ValueError,'upgraded',self.run_fixture,alter)

    def test_unreproduced_cannot_claim_oracle_unknown(self):
        def alter(j,r):
            p=j/'physical/result.json';x=json.loads(p.read_text());x['reference_verdict']='UNKNOWN';write(p,x)
        self.assertRaisesRegex(ValueError,'unexpected reference',self.run_fixture,alter,reproduced=False)

    def test_hex_rows_transport_tamper(self):
        def alter(j,r):
            p=next((r/'cache').glob('*.hex'));p.write_text(p.read_text().replace('x','0'))
        self.assertRaisesRegex(ValueError,'HEX transport',self.run_fixture,alter)

    def test_reference_result_tamper(self):
        def alter(j,r):
            p=j/'physical/reference.json';x=json.loads(p.read_text());x['verdict']='FAIL';write(p,x)
        self.assertRaisesRegex(ValueError,'pure-reference',self.run_fixture,alter)

    def test_wrong_checker_hash_never_executes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'checker.py';p.write_text("raise RuntimeError('must not execute')");self.assertRaisesRegex(ValueError,'checker hash',a.load_checker,p)

    def test_missing_reference_file_and_broken_gzip(self):
        def missing(j,r):(j/'physical/reference.json').unlink()
        self.assertRaises(OSError,self.run_fixture,missing)
        def broken(j,r):write(j/'physical/candidate-replay/replay.log.gz',b'invalid gzip')
        self.assertRaises(OSError,self.run_fixture,broken)

    def test_independent_anchor_rejects_correlated_file_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'raw.log';write(p,'old');reader=a.Saved(root,{'raw.log':a.sha(p.read_bytes())});write(p,'new');self.assertRaisesRegex(ValueError,'independent saved-input anchor',reader.raw,p)

    def test_native_job_slot_source_copy_and_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();job=root/'job';candidate=root/'candidate';source=root/'axis_frame_length_adjust.v';write(source,'// fixture source')
            harness="wire trace_done=1'b0;\nassert(!active[0] || ok[0]);\ncover(active[0]);\n";write(job/'harness.sv',harness);write(candidate/'candidate.sv','// synthetic fixture monitor')
            files={'dut.v':source,'candidate.sv':candidate/'candidate.sv','harness.sv':job/'harness.sv'}
            for n in ['axis_fifo.v','axis_frame_length_adjust_fifo.v','task_top_v3.sv']:
                p=root/n;write(p,'// fixture dependency');files[n]=p
            for name,p in files.items():write(job/'work/src'/name,p.read_bytes())
            config='[options]\nmode bmc\ndepth 24\n[files]\n'+''.join(n+' '+str(p)+'\n' for n,p in files.items());write(job/'job.sby',config);write(job/'sby.log','fixture native log');write(job/'work/status','FAIL\n')
            result=dict(mode='bmc',status='FAIL',slot=0,trace_done=0,scope='safety_projection',log_sha256=a.sha((job/'sby.log').read_bytes()));write(job/'result.json',result);row=dict(result,source='correct')
            self.assertEqual(a.check_native(job,row,a.Saved(root),candidate),source)
            write(job/'work/src/candidate.sv','// changed');self.assertRaisesRegex(ValueError,'copied source',a.check_native,job,row,a.Saved(root),candidate)
            write(job/'work/src/candidate.sv',(candidate/'candidate.sv').read_bytes());bad=dict(row,slot=1);write(job/'result.json',dict(result,slot=1));self.assertRaisesRegex(ValueError,'selected slot',a.check_native,job,bad,a.Saved(root),candidate)

    def test_physical_transport_argv_wrong_path(self):
        def alter(j,r):
            p=j/'physical/iverilog/execution.json';x=json.loads(p.read_text());x['argv']=['fixture-only','+INPUTS='+str(r/'other-inputs.txt')];write(p,x)
        self.assertRaisesRegex(ValueError,'argv transport',self.run_fixture,alter)

    def test_missing_declared_output_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            job,_=fixture(Path(tmp));p=job/'work/engine_0/trace.vcd';text='\n'.join(x for x in p.read_text().splitlines() if not x.startswith('$var wire 16') or 'h_length' not in x)
            self.assertRaisesRegex(ValueError,'missing declared',a.decode_vcd,text,0)

    def test_unattributed_prefix_cannot_assert_candidate_false_alarm(self):
        def alter(j,r):
            p=j/'physical/result.json';x=json.loads(p.read_text());x['candidate_false_alarm_claim']=True;write(p,x)
        self.assertRaisesRegex(ValueError,'false-alarm claim',self.run_fixture,alter)

    def test_exact_hash_pure_checker_load_does_not_write_reference_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'checker.py';p.write_text("import copy\ndef check_rows(rows, **kw):\n    return copy.deepcopy(rows)\n")
            checker=a.load_checker(p,a.sha(p.read_bytes()));self.assertEqual(checker([1]),[1]);self.assertFalse((root/'__pycache__').exists())


if __name__=='__main__':unittest.main()
