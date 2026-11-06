"""Review-owned CLI/output controls; only copied G0 Python executes."""
from pathlib import Path
import os,json,hashlib,subprocess,sys
P=Path(__file__).resolve().parent
S=P/'exec_tree/test2/g0_v1/adapter.py'
R=P/'exec_tree/test2/results';R.mkdir()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
def run(name,bundle,out,expect):
    argv=[sys.executable,str(S),'--bundle',str(bundle),'--out',str(out)]
    z=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    row={'name':name,'argv':argv,'exit_code':z.returncode,'expected_exit_code':expect,'stdout':z.stdout,'stderr':z.stderr,'source_sha256':h(S)}
    if (out/'result.json').is_file():row.update(result_sha256=h(out/'result.json'),result=json.loads((out/'result.json').read_text()))
    rows.append(row);assert z.returncode==expect,(name,row)
    return row
run('PASS',P/'independent-probes/baseline/bundle',R/'g0-cli-pass',0)
run('UNRESOLVED',P/'independent-probes/missing-usage-subsets-null/bundle',R/'g0-cli-unknown',2)
run('REJECT',P/'independent-probes/duplicate-json-key/bundle',R/'g0-cli-reject',1)
old=R/'g0-cli-pass/result.json';before=old.read_bytes()
run('OVERWRITE_REFUSED',P/'independent-probes/duplicate-json-key/bundle',R/'g0-cli-pass',1);assert old.read_bytes()==before
# Direct and ancestor symlink escape attempts point exclusively into review-owned sentinel directory.
outside=P/'output-sentinel';outside.mkdir();sent=outside/'kept.txt';sent.write_text('REVIEW OWNED SENTINEL\n');sh=h(sent)
link=R/'g0-link';link.symlink_to(outside,target_is_directory=True)
run('SYMLINK_OUTPUT_REFUSED',P/'independent-probes/baseline/bundle',link,1)
child=outside/'child';child.mkdir()
run('ANCESTOR_ESCAPE_REFUSED',P/'independent-probes/baseline/bundle',link/'child/g0-escaped',1)
assert h(sent)==sh and not (child/'g0-escaped').exists()
obj={'controls':len(rows),'all_expected_exits':True,'overwrite_bytes_preserved':True,'symlink_sentinel_preserved':True,'rows':rows}
(P/'cli-controls.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in obj.items() if k!='rows'}))

