import hashlib
import json
from pathlib import Path
import shutil

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[3]
packet = json.loads((OWN/'phase-packet.json').read_text())
AUDIT = (ROOT/packet['producer_phase']).parent
SNAP = AUDIT/'snapshot'
WORK = OWN/'review-copy'
WORK.mkdir(exist_ok=False)
sources = json.loads((SNAP/packet['source_manifest']).read_text())['files']
paths = dict(sources)
for rel in [packet[k] for k in ['registration','source_manifest','producer_phase','producer_manifest']]:
    src = SNAP/rel
    if not src.exists(): src = ROOT/rel
    paths[rel] = hashlib.sha256(src.read_bytes()).hexdigest()
copied = {}
for rel, expected in paths.items():
    src = SNAP/rel
    if not src.exists(): src = AUDIT/Path(rel).name
    assert hashlib.sha256(src.read_bytes()).hexdigest() == expected, rel
    dst = WORK/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst)
    copied[rel] = hashlib.sha256(dst.read_bytes()).hexdigest()
    assert copied[rel] == expected
(OWN/'review-copy-inputs.json').write_text(json.dumps(copied,indent=2)+'\n')
print(json.dumps({'review_copy_files':len(copied),'all_match':True}))
