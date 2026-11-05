"""Prospectively registered original-parent screening; no model/key access."""
import argparse
import json
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from run_midterm_fixed import ROOT,sha,invoke
from coverage import summary
from probe_natural_frontends import TOOLS
import probe_natural_frontends as front
import hierarchy_netlist_proof as proof_module
import screen_write_hierarchy as screen_module
from real_parent_semantics import ParentAdapter,ParentBitVectors
from probe_write_scopes import verify
from inventory_natural_coverage import load_all

SCOPE=ROOT/'configs/real_parent_screen.json'

def configuration(top):
    c=next(x for x in json.loads(SCOPE.read_text())['candidates'] if x['top']==top)
    overlay=json.loads((ROOT/'configs/real_parent_dependencies.json').read_text())
    if overlay['scope_sha256']!=sha(SCOPE):raise ValueError('Dependency overlay scope drift')
    extra=overlay['additions'].get(top,{})
    c['sources']=extra.get('sources_prepend',[])+c['sources']
    c['source_hashes'].update(extra.get('source_hashes',{}));c['git_blobs'].update(extra.get('git_blobs',{}))
    return c

@contextmanager
def replace(module,**values):
    old={k:getattr(module,k) for k in values}
    for k,v in values.items():setattr(module,k,v)
    try:yield
    finally:
        for k,v in old.items():setattr(module,k,v)

def probe(top,out):
    c=configuration(top);verify(c)
    with replace(front,configuration=configuration,verify=verify):front.probe(top,out)
    (out/'scope.json').write_bytes(SCOPE.read_bytes())
    (out/'scope-sha256.txt').write_text(sha(SCOPE)+'\n')
    (out/'dependency-overlay.json').write_bytes((ROOT/'configs/real_parent_dependencies.json').read_bytes())
    # Preserve original named probe wires across opt_clean. These attributes
    # affect proof observability only, never original-SV simulation.
    if c['proof_keep']:
        ys=(out/'probe.ys').read_text().split('; opt_expr;')[0]
        ys+='; setattr -set keep 1 '+' '.join('w:'+n for n in c['proof_keep'])+f'; opt_expr; opt_clean; write_json {out}/flat-kept.json\n'
        (out/'keep-names.ys').write_text(ys);t=time.monotonic();cmd=[str(TOOLS/'yosys'),'-Q','-T','-s',str(out/'keep-names.ys')]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=120);(out/'keep-names.log').write_text(p.stdout+p.stderr)
        (out/'keep-names-run.json').write_text(json.dumps({'command':cmd,'seconds':time.monotonic()-t,'returncode':p.returncode},indent=2)+'\n');p.check_returncode()

def preserve(top,base):
    a=ParentAdapter(json.loads((base/'ast.json').read_text()),top).extract();m=ParentBitVectors(a,procedural=True)
    m.guards()
    for d in m.definition_sources.values():m.term(d['rhs'])
    names=sorted({x['lhs']['symbol'] for x in m.definition_sources.values()} | {n['symbol'] for n in m.variables.values() if n['kind']=='NamedValue'})
    net=json.loads((base/'flat.json').read_text())['modules'][top]
    missing=[n for n in names if n not in net['netnames']]
    if missing:raise ValueError('Original names absent before optimization: '+str(missing))
    ys=f'read_json {base}/flat.json; setattr -set keep 1 '+' '.join('w:'+n for n in names)+f'; opt_expr; opt_clean; write_json {base}/flat-kept.json\n'
    (base/'keep-original-definitions.ys').write_text(ys);start=time.monotonic();cmd=[str(TOOLS/'yosys'),'-Q','-T','-s',str(base/'keep-original-definitions.ys')]
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=120);(base/'keep-original-definitions.log').write_text(p.stdout+p.stderr)
    (base/'kept-definitions.json').write_text(json.dumps({'names':names,'seconds':time.monotonic()-start,'returncode':p.returncode,'command':cmd,'AST_unresolved':m.unresolved},indent=2)+'\n');p.check_returncode()

def inventory(top,base,out):
    c=configuration(top);verify(c);out.mkdir(parents=True,exist_ok=False)
    ports=json.loads((base/'netlist.json').read_text())['modules'][top]['ports'];decl=[];init=[]
    for n,p in ports.items():
        if p['direction'] not in ('input','output'):raise ValueError('Inout bus requires explicit fixed electrical driver')
        w=len(p['bits']);decl.append('logic '+(f'[{w-1}:0] ' if w>1 else '')+n+';')
        if p['direction']=='input':init.append(n+f"={w}'d{c['seed_inputs'].get(n,0)};")
    if not set(c['seed_inputs'])<=set(ports):raise ValueError('Unknown seed field')
    params=' #('+','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())+')' if c['parameters'] else ''
    body='`timescale 1ns/1ps\nmodule tb_natural_inventory;\n'+'\n'.join(decl)+'\n'+top+params+' dut(.*);\ninitial begin\n'+'\n'.join(init)+'\n'
    body+=f"{c['reset']}={c['reset_active']};\nfor(integer i=0;i<8;i=i+1) begin\n{c['clock']}=0; if(i==2) {c['reset']}={1-c['reset_active']}; #5; {c['clock']}=1; #5;\nend\n$display(\"INVENTORY_OK cycles=8\"); $finish;\nend\nendmodule\n"
    tb=out/'tb_natural_inventory.sv';tb.write_text(body);files=[str(Path(c['root'])/f) for f in c['sources']]
    cmd=['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',out/'verilator-build','-j','2',*['-D'+d for d in c['defines']],*['-I'+str(Path(c['root'])/d) for d in c['include_dirs']],*files,tb]
    ct,_=invoke(cmd,out/'compile.log',timeout=300);raw=out/'seed.dat';sim=[out/'verilator-build/Vtb_natural_inventory','+verilator+coverage+file+'+str(raw)];st,log=invoke(sim,out/'seed.log',timeout=30)
    if 'INVENTORY_OK cycles=8' not in log:raise ValueError('Incomplete reset inventory')
    points=load_all(raw,files);(out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
    result={'status':'inventory_only','cycles':8,'no_checker':True,'no_reachability_claim':True,'seed_inputs':c['seed_inputs'],'compile_seconds':ct,'simulation_seconds':st,'compile_command':list(map(str,cmd)),'simulation_command':list(map(str,sim)),'coverage':summary(points),'policy':'Original DUT and all real child source counters; TB excluded. Fresh process. Reset/initialization included. Shared counters retained exactly as emitted.','hashes':{p:sha(ROOT/p) for p in files},'driver_sha256':sha(tb),'raw_sha256':sha(raw)}
    (out/'inventory.json').write_text(json.dumps(result,indent=2)+'\n');return result

def prove(top,base,out):
    net=base/('flat-kept.json' if (base/'flat-kept.json').exists() else 'flat-simplified.json')
    with replace(proof_module,NaturalAdapter=ParentAdapter,NaturalBitVectors=ParentBitVectors):
        result=proof_module.prove(base/'ast.json',net,top,out)
    if 'hashes' in result:
        result['hashes'].update({str(p):sha(p) for p in [Path(__file__).resolve(),Path(__file__).with_name('real_parent_semantics.py').resolve(),SCOPE,ROOT/'configs/real_parent_dependencies.json']})
        (out/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def screen(top,base,out,proof):
    with replace(screen_module,SCOPE=SCOPE,configuration=configuration,verify=verify,HierarchyAdapter=ParentAdapter,HierarchyBitVectors=ParentBitVectors):screen_module.screen(top,base,out,proof)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['probe','preserve','inventory','proof','screen']);p.add_argument('--top',required=True);p.add_argument('--base',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--proof',type=Path);a=p.parse_args();out=a.output.resolve();base=a.base.resolve() if a.base else None
    if a.stage=='probe':probe(a.top,out)
    elif a.stage=='preserve':preserve(a.top,base)
    elif a.stage=='inventory':inventory(a.top,base,out)
    elif a.stage=='proof':prove(a.top,base,out)
    else:screen(a.top,base,out,a.proof.resolve())
