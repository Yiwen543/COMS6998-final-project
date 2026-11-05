"""Compare original Verilator vs Yosys-lowered Icarus on the reset inventory.

The original SV Icarus compile failure stays recorded. This is a limited
translation/simulator smoke check, not sequential equivalence or a checker.
"""
import argparse
import json
from pathlib import Path
from probe_natural_frontends import configuration,verify,TOOLS
from run_midterm_fixed import ROOT,invoke,sha


def check(base,out):
    c=configuration('flash_ctrl_rd');verify(c);out.mkdir(parents=True,exist_ok=False)
    net=base/'flat-simplified.json';ports=json.loads(net.read_text())['modules']['flash_ctrl_rd']['ports']
    ys=out/'lower.ys';v=out/'lowered.v'
    ys.write_text(f'read_json {net}; write_verilog -noattr {v}\n')
    lower_t,_=invoke([TOOLS/'yosys','-Q','-T','-s',ys],out/'lower.log',timeout=60)
    text=(base/'inventory/tb_natural_inventory.sv').read_text()
    fmt=' '.join('%h' for _ in ports);vals=', '.join(ports)
    text=text.replace('#5;\nend',f'#5; $display("PORTS %0d {fmt}", i, {vals});\nend')
    if 'PORTS' not in text:raise ValueError('Unrecognized inventory harness')
    tb=out/'tb_natural_inventory.sv';tb.write_text(text)
    files=[str(Path(c['root'])/f) for f in c['sources']]
    cmd=['verilator','--binary','--timing','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',out/'obj','-j','2',
         *['-D'+d for d in c['defines']],*['-I'+str(Path(c['root'])/d) for d in c['include_dirs']],*files,tb]
    vt,_=invoke(cmd,out/'verilator-compile.log',timeout=300)
    it,_=invoke(['iverilog','-g2012','-s','tb_natural_inventory','-o',out/'lowered.vvp',v,tb],out/'iverilog-compile.log',timeout=60)
    vs,vl=invoke([out/'obj/Vtb_natural_inventory'],out/'verilator-run.log',timeout=30)
    ins,il=invoke(['vvp',out/'lowered.vvp'],out/'iverilog-run.log',timeout=30)
    select=lambda s:[l.lower() for l in s.splitlines() if l.startswith('PORTS ')]
    a,b=select(vl),select(il)
    result={'status':'pass' if len(a)==8 and a==b else 'mismatch','cycles_each':8,'simulator_executions':2,
        'source_variant':'Original pinned SV in Verilator; same Slang/Yosys lowered netlist in Icarus.',
        'not_original_icarus_compatibility':True,'not_sequential_equivalence_proof':True,'no_functional_checker_claim':True,
        'no_coverage_from_lowered_design':True,'ports':list(ports),'trace_original':a,'trace_lowered':b,
        'seconds':{'lowering':lower_t,'verilator_compile':vt,'iverilog_compile':it,'verilator_sim':vs,'iverilog_sim':ins},
        'hashes':{str(p):sha(p) for p in [net,v,tb,Path(__file__)]}}
    (out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
    if result['status']!='pass':raise ValueError('Reset inventory mismatch')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();check(a.base.resolve(),a.output.resolve())
