"""Replay the frozen I2C driver, then run the Claude-authored scoped checker.

Every action executes before checking; failures cannot suppress coverage.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from i2c_fixture import validate_actions
from run_i2c_fixed import compile_driver,simulate,verify_source
from run_midterm_fixed import ROOT,sha

FOLDER=ROOT/'examples/heldout_i2c_controller'


def verify_freeze():
    manifest=json.loads((FOLDER/'freeze.json').read_text())
    for name,h in manifest['hashes'].items():
        if sha(ROOT/name)!=h:raise ValueError('Frozen verification boundary changed: '+name)
    if not manifest['offline_checker_qualified']:raise ValueError('Checker not qualified')
    verify_source()
    return manifest


def check_trace(path):
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['KEY','TOKEN','SECRET','PASSWORD','CREDENTIAL'])}
    code='''import json,sys,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
sys.path.insert(0,sys.argv[1])
from run_spi_checker_author import validate_source
source=Path(sys.argv[2]).read_text();validate_source(source);ns={}
exec(compile(source,sys.argv[2],'exec'),ns)
print(json.dumps(ns['check_rows'](json.loads(Path(sys.argv[3]).read_text()))))
'''
    with tempfile.TemporaryDirectory(prefix='i2c-frozen-check-') as cwd:
        p=subprocess.run([sys.executable,'-I','-c',code,str(ROOT/'scripts'),str(FOLDER/'checker.py'),str(path)],
                         env=env,cwd=cwd,text=True,capture_output=True,timeout=30,check=True)
    return json.loads(p.stdout)


def main():
    p=argparse.ArgumentParser();p.add_argument('--actions',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--simulator',choices=['verilator','iverilog'],default='verilator');a=p.parse_args()
    manifest=verify_freeze()
    actions=validate_actions(json.loads(a.actions.read_text()),392)
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    result,_=simulate(compile_driver(out,a.simulator),actions,out,'batch',a.simulator)
    checked=check_trace(out/'batch.trace.json')
    passed=result['environment_valid'] and not checked['failures'] and not checked['assumption_violations'] and not checked['unresolved']
    result.update(checker=checked,checker_status='evaluated',scoped_pass=passed,
                  credited_events=checked['events'] if passed else [],
                  formal_B_eligible=False,freeze_sha256=sha(FOLDER/'freeze.json'))
    (out/'checked.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'scoped_pass':passed,'failures':len(checked['failures']),
                      'executed_cycles':result['steps'],'coverage':result['coverage']}))


if __name__=='__main__':main()
