"""Persist negative-control receipts from synthetic two-cycle file fixtures only."""
from pathlib import Path
import sys,json,tempfile,gzip
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'test2/tests'),str(ROOT/'test2/scripts')]
import test_controller_done_witness_chain_audit_v1 as f
import controller_done_witness_chain_audit_v1 as a
OUT=Path(__file__).parent
needles=['missing_vcd','truncated_vcd','literal_offset','rows_changed','raw_mon_changed_with_fresh_hashes','selected_phase','reference_prefix_shift','reference_verdict_changed','false_alarm_upgrade','hex_transport_changed','checker_hash_mismatch']
receipts=[]
for name in needles:
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve();job,checker=f.fixture(root);phy=job/'physical'
        if name=='missing_vcd':(job/'work/engine_0/trace.vcd').unlink()
        elif name=='truncated_vcd':
            p=job/'work/engine_0/trace.vcd';p.write_text('\n'.join(p.read_text().splitlines()[:-5]))
        elif name=='literal_offset':
            p=phy/'iverilog/inputs.txt';p.write_text(p.read_text().replace('0 0 0 0 0 0','0 0 1 0 0 0'))
        elif name=='rows_changed':
            p=phy/'iverilog/rows.json';x=json.loads(p.read_text());x[1]['pre']['s_ready']=1;f.write(p,x)
        elif name=='raw_mon_changed_with_fresh_hashes':
            d=phy/'candidate-replay';p=d/'replay.log.gz';raw=gzip.decompress(p.read_bytes()).replace(b'111110',b'111111');comp=gzip.compress(raw,mtime=0);f.write(p,comp);m=json.loads((d/'result.json').read_text());m['raw_log_sha256']=m['execution']['log_sha256']=a.sha(raw);m['compressed_log_sha256']=a.sha(comp);f.write(d/'result.json',m)
        elif name=='selected_phase':
            p=phy/'result.json';x=json.loads(p.read_text());x['selected_alarm']['phase']='post';f.write(p,x)
        elif name=='reference_prefix_shift':f.write(phy/'reference-prefix-rows.json',json.loads((phy/'iverilog/rows.json').read_text()))
        elif name=='reference_verdict_changed':
            p=phy/'reference.json';x=json.loads(p.read_text());x['verdict']='FAIL';f.write(p,x)
        elif name=='false_alarm_upgrade':
            p=phy/'result.json';x=json.loads(p.read_text());x['candidate_false_alarm_claim']=True;f.write(p,x)
        elif name=='hex_transport_changed':
            p=next((root/'cache').glob('*.hex'));p.write_text(p.read_text().replace('x','0'))
        elif name=='checker_hash_mismatch':f.write(root/'checker.py',"raise RuntimeError('forbidden execution')")
        try:
            if name=='checker_hash_mismatch':a.load_checker(root/'checker.py')
            else:a.inspect_chain(job,0,a.Saved(root),checker)
        except (ValueError,OSError,EOFError) as error:
            receipts.append(dict(case=name,expected='REJECT',observed='REJECT',error_type=type(error).__name__,reason=str(error),fixture_files_sha256={str(p.relative_to(root)):a.sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}))
        else:raise AssertionError('Mutation accepted: '+name)
for name,kw in [('reference_unknown',dict(verdict='UNRESOLVED')),('unreproduced_unknown_bit',dict(reproduced=False,unknown=True))]:
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve();job,checker=f.fixture(root,**kw);r,_=a.inspect_chain(job,0,a.Saved(root),checker);assert r['scientific_adjudication']=='UNRESOLVED';assert r['reference_confirmed_selected_alarm'] is False;receipts.append(dict(case=name,expected='scientifically UNRESOLVED',receipt=r))
p=OUT/'fixture-controls.json';assert not p.exists();p.write_text(json.dumps(dict(scope='Synthetic two-cycle saved-file integrity fixtures only; no physical DUT reachability, RTL coverage, monitor execution or scientific experiment.',status='PASS',negative_controls=len(needles),unknown_controls=2,receipts=receipts),indent=2)+'\n');print('11 mutations rejected; 2 explicit unknown controls retained; synthetic files only.')
