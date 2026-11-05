"""Reset/quiescence harness to inventory all DUT source counters, not a checker."""
import argparse
import json
import re
from pathlib import Path
from probe_natural_frontends import configuration,verify
from run_midterm_fixed import ROOT,invoke,sha
from coverage import summary


def load_all(path,allowed):
    lines=path.read_text().splitlines()
    if lines[0]!='# SystemC::Coverage-3':raise ValueError('Unknown raw coverage format')
    points=[]
    for line in lines[1:]:
        if not line.strip():continue
        m=re.fullmatch(r"C '(.*)' (\d+)",line)
        if not m:raise ValueError('Invalid raw coverage row')
        f=dict(p.split('\x02',1) for p in m[1].split('\x01') if p)
        if 'dut' not in f.get('h','').split('.'):continue
        src=f['f'];matches=[s for s in allowed if src==s or src.endswith('/'+s)]
        if len(matches)!=1:raise ValueError('DUT counter source not pinned: '+src)
        points.append({'source':matches[0],'line':int(f['l']),'column':int(f.get('n',0)),
            'type':f['t'],'outcome':f.get('o',''),'hierarchy':f['h'],'span':f.get('S'),'hits':int(m[2])})
    if not points:raise ValueError('No DUT counters')
    return points


def inventory(name,frontend,out):
    c=configuration(name);verify(c);out.mkdir(parents=True,exist_ok=False)
    top=c['top'];ports=json.loads((frontend/'netlist.json').read_text())['modules'][top]['ports']
    decl=[];init=[]
    for n,p in ports.items():
        w=len(p['bits']);decl.append('logic '+(f'[{w-1}:0] ' if w>1 else '')+n+';')
        if p['direction']=='input':init.append(n+"='0;")
    parameters=' #('+','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())+')' if c['parameters'] else ''
    source='`timescale 1ns/1ps\nmodule tb_natural_inventory;\n'+'\n'.join(decl)+'\n'+top+parameters+' dut(.*);\ninitial begin\n'+'\n'.join(init)+'\n'
    source+=f"{c['reset']}={c['reset_active']};\nfor(integer i=0;i<8;i=i+1) begin\n{c['clock']}=0; if(i==2) {c['reset']}={1-c['reset_active']}; #5; {c['clock']}=1; #5;\nend\n$display(\"INVENTORY_OK cycles=8\"); $finish;\nend\nendmodule\n"
    tb=out/'tb_natural_inventory.sv';tb.write_text(source)
    files=[str(Path(c['root'])/f) for f in c['sources']]
    cmd=['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory',
         '--Mdir',out/'verilator-build','-j','2',*['-D'+d for d in c['defines']],
         *['-I'+str(Path(c['root'])/d) for d in c['include_dirs']],*files,tb]
    ct,_=invoke(cmd,out/'compile.log',timeout=300)
    raw=out/'seed.dat';cmdsim=[out/'verilator-build/Vtb_natural_inventory','+verilator+coverage+file+'+str(raw)]
    st,log=invoke(cmdsim,out/'seed.log',timeout=30)
    if 'INVENTORY_OK cycles=8' not in log:raise ValueError('Incomplete reset inventory')
    points=load_all(raw,files);(out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
    result={'status':'inventory_only','cycles':8,'compile_seconds':ct,'simulation_seconds':st,'compile_command':list(map(str,cmd)),
        'simulation_command':list(map(str,cmdsim)),'coverage':summary(points),'no_checker':True,'no_reachability_claim':True,
        'policy':'All pinned DUT source counters, including actual child instances, retained. TB excluded. Reset/initialization included. Fresh process.',
        'hashes':{p:sha(ROOT/p) for p in files},'driver_sha256':sha(tb),'raw_sha256':sha(raw)}
    (out/'inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['coverage']))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',choices=['axi_dma_rd','flash_ctrl_rd'],required=True)
    for n in ['frontend','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();inventory(a.candidate,a.frontend.resolve(),a.output.resolve())
