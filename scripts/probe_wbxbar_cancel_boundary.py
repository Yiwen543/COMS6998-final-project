"""Read-only version-specific quiescence characterization, never a spec checker."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from prove_wbxbar_index import configuration,OLD
from probe_natural_frontends import TOOLS
from replay_wbxbar_cancel import verify_replay_freeze

SCOPE=ROOT/'configs/wbxbar_conformance_gate_v1.json'


def verify_scope():
    verify_replay_freeze(ROOT/'configs/wbxbar_cancel_replay_freeze_v1.json')
    scope=json.loads(SCOPE.read_text())
    for p,h in scope['parent_hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Parent changed: '+p)
    return scope


def prepare(output):
    verify_scope();_,c=configuration()
    ports=json.loads((OLD/'netlist.json').read_text())['modules']['wbxbar']['ports']
    decl=[p['direction']+' wire '+(f'[{len(p["bits"])-1}:0] ' if len(p['bits'])>1 else '')+n for n,p in ports.items()]
    params=','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())
    source='module wbxbar_quiet_observer(\n'+',\n'.join(decl)+'\n);\n'+f'wbxbar #({params}) dut(.*);\n'+'''
// No input assumptions. Original transition system; FORMAL define is disabled.
// This observes a version-specific pin implication, not request cancellation.
reg past_valid = 1'b0;
always @(posedge i_clk) begin
    past_valid <= 1'b1;
`ifdef OBS_COVER
    cover(past_valid && $past(i_mcyc != 0) && i_mcyc == 0 && o_scyc != 0);
    cover(past_valid && $past(i_mcyc == 0) && i_mcyc != 0 && o_scyc == 0);
`elsif OBS_INSTANT
    if (past_valid && i_mcyc == 0) assert(o_scyc == 0 && o_sstb == 0);
`else
    if (past_valid && $past(i_mcyc == 0)) assert(o_scyc == 0 && o_sstb == 0);
`endif
end
endmodule
'''
    output.mkdir(parents=True,exist_ok=False);wrapper=output/'observer.sv';wrapper.write_text(source)
    tasks={'quiet_prove':('prove',20,[],'pass'),'instant_negative':('bmc',20,['OBS_INSTANT'],'fail'),
           'nonvacuity':('cover',40,['OBS_COVER'],'pass')}
    sources=[ROOT/c['root']/p for p in c['sources']]
    for name,(mode,depth,defines,expect) in tasks.items():
        script='read_slang --top wbxbar_quiet_observer -U FORMAL '+' '.join('-D '+d for d in defines)+' '+' '.join(p.name for p in sources+[wrapper])+'\nprep -top wbxbar_quiet_observer\n'
        (output/(name+'.sby')).write_text(f'[options]\nmode {mode}\ndepth {depth}\ntimeout 120\nexpect {expect}\n\n[engines]\nsmtbmc --dumpsmt2 z3\n\n[script]\n'+script+'\n[files]\n'+'\n'.join(map(str,sources+[wrapper]))+'\n')
    manifest={'scope_sha256':sha(SCOPE),'tasks':tasks,'configuration':c,'input_assumptions':[],
        'claim':'At consecutive sampled rising edges, all master CYC low at the preceding edge implies slave CYC/STB low now. Only this fixed RTL/configuration.',
        'excluded':['No claim that decoder/skid buffers are empty','No stale-work exclusion after restart','No general Wishbone cancellation bound','No new functional checker or coverage instrumentation','No protocol-legality claim for unconstrained cover/negative witnesses'],
        'hashes':{str(p):sha(p) for p in [Path(__file__).resolve(),SCOPE,wrapper,*sources]}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest


def run(output,task):
    verify_scope();m=json.loads((output/'manifest.json').read_text())
    for p,h in m['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Proof input changed')
    if task not in m['tasks'] or (output/task).exists():raise ValueError('Unknown task or existing result')
    env=dict(os.environ);env['PATH']=str(TOOLS)+os.pathsep+env['PATH']
    command=[str(TOOLS/'sby'),'-d',str(output/task),str(output/(task+'.sby'))]
    t=time.monotonic();r=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True,timeout=150)
    (output/(task+'.log')).write_text(r.stdout+r.stderr)
    status=(output/task/'status').read_text().strip() if (output/task/'status').exists() else 'NO_STATUS'
    result={'task':task,'status':status,'exit_code':r.returncode,'expected':m['tasks'][task][3],'seconds':time.monotonic()-t,
        'command':command,'model_calls':0,'sby_sha256':sha(output/(task+'.sby'))}
    (output/(task+'-result.json')).write_text(json.dumps(result,indent=2)+'\n');return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--task');a=p.parse_args()
    r=prepare(a.output.resolve()) if a.stage=='prepare' else run(a.output.resolve(),a.task)
    print(json.dumps({k:v for k,v in r.items() if k not in ('configuration','hashes')},indent=2))
