"""Pinned-source frontend integration. No stubs, checker, or model calls."""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha

TOOLS=ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin'


def configuration(name):
    if name=='axi_dma_rd':
        return {'root':'third_party/verilog_axi_candidate','top':name,'sources':['rtl/axi_dma_rd.v'],
            'include_dirs':[],'defines':[],'parameters':{'ENABLE_UNALIGNED':1},'clock':'clk','reset':'rst','reset_active':1,
            'revision':'516bd5dadc3365b7f9e225d2af8fe0b8d804fe53'}
    c=json.loads((ROOT/'configs/flash_read_sources.json').read_text())
    return {**c,'parameters':{},'clock':'clk_i','reset':'rst_ni','reset_active':0}


def verify(c):
    if c['top']=='axi_dma_rd':
        src=ROOT/c['root']/c['sources'][0]
        if sha(src)!='853ff3aedc44ec0c12ef3ae8b84d7559800d372f76832c7c133ed5eecac61dd8':
            raise ValueError('DMA source changed')
    else:
        manifest=json.loads((ROOT/'results/natural_ip_integration_20261104/flash-sources.json').read_text())
        for item in manifest['files']:
            b=(ROOT/c['root']/item['path']).read_bytes()
            if hashlib.sha256(b).hexdigest()!=item['sha256'] or hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()!=item['blob']:
                raise ValueError('Upstream source changed: '+item['path'])


def probe(name,out):
    c=configuration(name);verify(c);out.mkdir(parents=True,exist_ok=False)
    files=[str(Path(c['root'])/f) for f in c['sources']]
    inc=[str(Path(c['root'])/f) for f in c['include_dirs']]
    common=[x for d in c['defines'] for x in ['-D',d]]+[x for d in inc for x in ['-I',d]]
    params=[x for k,v in c['parameters'].items() for x in ['-G',f'{k}={v}']]
    commands=[('slang',[TOOLS/'slang','--single-unit','--top',c['top'],*params,*common,
        '--ast-json',out/'ast.json','--ast-json-source-info','--ast-json-detailed-types',*files]),
      ('verilator',['verilator','--lint-only','--timing','-Wno-fatal','--top-module',c['top'],
        *['-G'+str(k)+'='+str(v) for k,v in c['parameters'].items()],*['-D'+d for d in c['defines']],*['-I'+d for d in inc],*files]),
      ('iverilog',['iverilog','-g2012','-s',c['top'],'-tnull',
        *['-P'+c['top']+'.'+str(k)+'='+str(v) for k,v in c['parameters'].items()],*common,*files])]
    ys='read_slang --single-unit --top '+c['top']+' '+' '.join([*params,*common,*files])+f'; proc; write_json {out}/netlist.json; flatten; write_json {out}/flat.json; opt_expr; opt_clean; write_json {out}/flat-simplified.json\n'
    (out/'probe.ys').write_text(ys);commands.append(('yosys',[TOOLS/'yosys','-Q','-T','-s',out/'probe.ys']))
    runs=[]
    for stage,cmd in commands:
        t=time.monotonic()
        p=subprocess.run(list(map(str,cmd)),cwd=ROOT,capture_output=True,text=True,timeout=120)
        (out/(stage+'.log')).write_text(p.stdout+p.stderr)
        runs.append({'stage':stage,'returncode':p.returncode,'seconds':time.monotonic()-t,'command':list(map(str,cmd))})
        print(stage,p.returncode,flush=True)
    result={'configuration':c,'runs':runs,'source_sha256':{p:sha(ROOT/p) for p in files},
        'no_model_calls':True,'no_functional_checker_claim':True,'qualified_for_B':False,
        'assertions':'SYNTHESIS selects upstream synthesis-compatible assertion macros for flash; not assertion verification.'}
    (out/'probe.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',choices=['axi_dma_rd','flash_ctrl_rd'],required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();probe(a.candidate,a.output.resolve())
