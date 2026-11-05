"""Prospectively pinned write-scope frontend/inventory adapter.

Reuse the preceding integration commands verbatim, supplying an explicit pinned
configuration. Old evidence and old module defaults are not rewritten.
"""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha
import probe_natural_frontends as frontend
import inventory_natural_coverage as counters

SCOPE=ROOT/'configs/natural_write_scope.json'

def configuration(name):
    return next(c for c in json.loads(SCOPE.read_text())['candidates'] if c['top']==name)

def verify(c):
    if 'source_manifest' in c:
        for item in json.loads((ROOT/c['source_manifest']).read_text())['files']:
            b=(ROOT/c['root']/item['path']).read_bytes()
            if hashlib.sha256(b).hexdigest()!=item['sha256'] or hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()!=item['blob']:
                raise ValueError('Source drift: '+item['path'])
    else:
        for path,h in c['source_hashes'].items():
            if sha(ROOT/path)!=h:raise ValueError('Source drift: '+path)

def probe(name,out):
    saved=frontend.configuration,frontend.verify
    try:
        frontend.configuration,frontend.verify=configuration,verify
        frontend.probe(name,out)
    finally:frontend.configuration,frontend.verify=saved
    if name=='axi_dma_wr':
        # opt_clean otherwise drops these original, useful SSA probe signals.
        # Keep affects proof observability only, not simulation RTL or budgets.
        ys=(out/'probe.ys').read_text().split('; opt_expr;')[0]
        ys+=f'; setattr -set keep 1 w:cycle_size w:tr_word_count_next w:input_last_cycle_next; opt_expr; opt_clean; write_json {out}/flat-kept.json\n'
        (out/'keep-names.ys').write_text(ys);cmd=[str(frontend.TOOLS/'yosys'),'-Q','-T','-s',str(out/'keep-names.ys')]
        start=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=120)
        (out/'keep-names.log').write_text(p.stdout+p.stderr)
        (out/'keep-names-run.json').write_text(json.dumps({'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-start},indent=2)+'\n')
        p.check_returncode()
    (out/'scope.json').write_bytes(SCOPE.read_bytes())
    (out/'scope-sha256.txt').write_text(sha(SCOPE)+'\n')

def inventory(name,base,out):
    saved=counters.configuration,counters.verify
    try:
        counters.configuration,counters.verify=configuration,verify
        counters.inventory(name,base,out)
    finally:counters.configuration,counters.verify=saved

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['probe','inventory']);p.add_argument('--top',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--base',type=Path)
    a=p.parse_args()
    if a.mode=='probe':probe(a.top,a.output.resolve())
    else:inventory(a.top,a.base.resolve(),a.output.resolve())
