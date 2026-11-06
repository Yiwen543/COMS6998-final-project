"""Fresh isolated copy for R04's small pure suite;preserves prior harness outputs."""
from pathlib import Path
import hashlib,json,runpy,shutil,sys
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_R04_2026-11-06';SNAP=AUDIT/'snapshot'
phase=json.loads((AUDIT/'phase.json').read_text());sources=json.loads((SNAP/phase['source_manifest']).read_text())['files']
work=OWN/'isolated-suite-copy';work.mkdir(exist_ok=False)
bindings={}
for rel,expected in sources.items():
    src=SNAP/rel
    if not src.exists():src=AUDIT/Path(rel).name
    assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
    dest=work/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);bindings[rel]=expected
rel='test2/g1_v3/observations.py';src=ROOT/rel
assert src.read_bytes()==(SNAP/'test2/g1_v4/observations.py').read_bytes()
dest=work/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
bindings[rel]=hashlib.sha256(src.read_bytes()).hexdigest()
(OWN/'isolated-suite-inputs.json').write_text(json.dumps(bindings,indent=2)+'\n')
code=work/'test2/g1_v4';sys.path.insert(0,str(code));sys.argv=[str(code/'r04_tests.py'),'--record',str(OWN/'fresh-r04-tests-isolated')]
try:runpy.run_path(str(code/'r04_tests.py'),run_name='__main__')
except SystemExit as e:assert e.code==0
summary=json.loads((OWN/'fresh-r04-tests-isolated/summary.json').read_text())
assert (summary['tests'],summary['failures'],summary['errors'])==(17,0,0)
assert all(hashlib.sha256((work/r).read_bytes()).hexdigest()==h for r,h in bindings.items())
print('ISOLATED17_PASS;copied bytes unchanged;no real tools')
