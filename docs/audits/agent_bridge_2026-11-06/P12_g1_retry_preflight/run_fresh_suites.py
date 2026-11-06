import hashlib
import json
from pathlib import Path
import runpy
import sys
from unittest.mock import patch

OWN = Path(__file__).resolve().parent
CODE = OWN/'review-copy/test2/g1_v3'
sys.path.insert(0,str(CODE))

def forbidden(*a,**kw):
    raise AssertionError('REVIEW_FORBIDS_REAL_PROCESS_SIGNAL_OR_SLEEP')

outcomes=[]
for name,label in [('continuation_tests.py','fresh-continuation'),('regression_tests.py','fresh-deadline-vcd')]:
    target=OWN/label
    sys.argv=[str(CODE/name),'--record',str(target)]
    exit_code=None
    with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
        try:
            runpy.run_path(str(CODE/name),run_name='__main__')
        except SystemExit as result:
            exit_code=result.code
    summary=json.loads((target/'summary.json').read_text())
    outcomes.append(dict(entrypoint=name,exit_code=exit_code,tests=summary['tests'],failures=summary['failures'],errors=summary['errors'],summary_sha256=hashlib.sha256((target/'summary.json').read_bytes()).hexdigest()))
(OWN/'fresh-suites.json').write_text(json.dumps(outcomes,indent=2)+'\n')
print(json.dumps(outcomes))
assert all(o['exit_code']==0 for o in outcomes)
