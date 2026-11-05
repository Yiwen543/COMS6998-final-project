"""Run the immutable Claude checker on saved experimental-driver observations."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from run_midterm_fixed import ROOT,sha


def evaluate(candidate, driver, output):
    auth=json.loads((candidate/'authorship.json').read_text())
    for name,digest in auth['artifact_sha256'].items():
        if sha(candidate/name)!=digest:raise ValueError('Checker drift')
    preflight=json.loads((driver/'summary.json').read_text())
    for name,digest in preflight['hashes'].items():
        if sha(Path(name))!=digest:raise ValueError('Driver preflight drift')
    rows={r['case']:json.loads((driver/r['case']/'verilator/trace.json').read_text()) for r in preflight['cases']}
    output.mkdir(parents=True,exist_ok=False)
    inputs=output/'private-inputs.json';inputs.write_text(json.dumps(rows,separators=(',',':'))+'\n')
    cmd=[sys.executable,'-I',str(ROOT/'scripts/evaluate_spi_checker_candidate.py'),'--worker',
         '--candidate',str(candidate),'--inputs',str(inputs),'--output',str(output/'evaluations.json')]
    env={k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-driver-eval-') as cwd:
        result=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
    (output/'worker.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError('Checker worker failed')
    values=json.loads((output/'evaluations.json').read_text())
    summary={'status':'evaluated_not_frozen','checker_sha256':sha(candidate/'checker.py'),'driver_summary_sha256':sha(driver/'summary.json'),
             'cases':values['cases'],'errors':values['errors'],'new_simulations':0,'new_model_calls':0,
             'selftests':values['selftests'],'hashes':{str(p):sha(p) for p in [Path(__file__),inputs,candidate/'authorship.json',driver/'summary.json']}}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({n:{'verdict':r.get('verdict'),'failures':len(r.get('failures',[])),
                          'assumptions':len(r.get('assumption_violations',[]))} for n,r in values['cases'].items()
                      if r.get('verdict')!='scoped_pass'}))
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('candidate','driver','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();evaluate(a.candidate.resolve(),a.driver.resolve(),a.output.resolve())
