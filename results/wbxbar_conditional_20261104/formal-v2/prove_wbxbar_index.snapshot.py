"""Original-transition conditional index proof; observers never enter DUT coverage."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from probe_natural_frontends import TOOLS
from probe_write_scopes import verify

SCOPE=ROOT/'configs/wbxbar_conditional_index_v1.json'
OLD=ROOT/'results/transaction_recovery_screen_20261104/wbxbar-final'

def configuration():
    s=json.loads(SCOPE.read_text());c=s['candidates'][0];verify(c)
    assert c['top']=='wbxbar' and c['parameters']['NM']==2 and c['parameters']['NS']==2
    assert sha(ROOT/s['parent_scope']['path'])==s['parent_scope']['sha256']
    return s,c

def observer(c,ports,activation):
    names=list(ports);decl=[]
    for n,p in ports.items():
        assert p['direction'] in ('input','output')
        w=len(p['bits']);decl.append(p['direction']+' wire '+(f'[{w-1}:0] ' if w>1 else '')+n)
    params=','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())
    return 'module wbxbar_range_formal(\n'+',\n'.join(decl)+'\n);\n'+f'wbxbar #({params}) dut(.*);\n'+'''
// No input/protocol assumptions; preserve original initial values. No mindex reset.
for (genvar n=0;n<2;n=n+1) begin: monitor
 wire [1:0] index_value = dut.mindex[n];
 wire active = dut.mgrant[n];
 wire [2:0] request_value = dut.request[n];
 wire [2:0] grant_value = dut.grant[n];
 wire selected = active && !grant_value[2];
 always @(posedge i_clk) begin
`ifdef CHECK_COVER
  cover(active && index_value==0);
  cover(active && index_value==1);
  cover(active && index_value==2);
`elsif CHECK_UNCONDITIONAL
  assert(index_value<=2);
`elsif CHECK_FALSE
  assert(!selected || index_value==0);
`else
  assert(!PROOF_ACTIVATION || index_value<=2);
`ifdef CHECK_HELPERS
  assert((request_value & (request_value-3'd1))==0);
  assert((grant_value & (grant_value-3'd1))==0);
  assert(active == (|grant_value));
  assert(!selected || grant_value==(3'b001 << index_value));
`endif
`endif
 end
end
endmodule
'''.replace('PROOF_ACTIVATION','selected' if activation=='selected' else 'active')

def prepare(out,activation):
    scope,c=configuration();out.mkdir(parents=True,exist_ok=False)
    ports=json.loads((OLD/'netlist.json').read_text())['modules']['wbxbar']['ports']
    wrapper=out/'wbxbar_range_formal.sv';wrapper.write_text(observer(c,ports,activation))
    tasks={'prove':('prove',20,[],'pass'),'strengthened':('prove',20,['CHECK_HELPERS'],'pass'),
           'false_active':('bmc',20,['CHECK_FALSE'],'fail'),'unconditional':('bmc',20,['CHECK_UNCONDITIONAL'],'fail'),
           'activation':('cover',40,['CHECK_COVER'],'pass')}
    sources=[ROOT/c['root']/p for p in c['sources']]
    for name,(mode,depth,defines,expect) in tasks.items():
        script='read_slang --top wbxbar_range_formal -U FORMAL '+ ' '.join('-D '+d for d in defines)+' '+' '.join(p.name for p in sources+[wrapper])+'\nprep -top wbxbar_range_formal\n'
        body=f'[options]\nmode {mode}\ndepth {depth}\ntimeout 120\nexpect {expect}\n\n[engines]\nsmtbmc --dumpsmt2 z3\n\n[script]\n'+script+'\n[files]\n'+'\n'.join(str(p) for p in sources+[wrapper])+'\n'
        (out/(name+'.sby')).write_text(body)
    evidence={'scope_sha256':sha(SCOPE),'script_sha256':sha(Path(__file__)),'tasks':list(tasks),'proof_activation':activation,
              'hashes':{str(p):sha(p) for p in [SCOPE,Path(__file__).resolve(),wrapper,*sources]},
              'source_netlist_for_port_widths':{'path':str(OLD/'netlist.json'),'sha256':sha(OLD/'netlist.json')},
              'assumptions':[],'initial_state':'Original RTL initial assignments only; all other state arbitrary.',
              'not_a_checker':'Proof-only internal observation. Not a spec-output model or experimental stimulus.'}
    (out/'manifest.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('prepared',out)

def run(out,task):
    configuration();m=json.loads((out/'manifest.json').read_text())
    for p,h in m['hashes'].items():assert sha(Path(p))==h,('drift',p)
    assert task in m['tasks'];dest=out/task
    if dest.exists():raise ValueError('Never overwrite proof attempt')
    env=os.environ.copy();env['PATH']=str(TOOLS)+os.pathsep+env['PATH']
    cmd=[str(TOOLS/'sby'),'-d',str(dest),str(out/(task+'.sby'))]
    start=time.perf_counter();p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True,timeout=150)
    log=out/(task+'-invocation.log');log.write_text(p.stdout+p.stderr)
    status=(dest/'status').read_text().strip() if (dest/'status').exists() else 'NO_STATUS'
    result={'task':task,'status':status,'returncode':p.returncode,'seconds':time.perf_counter()-start,'command':cmd,
            'scope_sha256':sha(SCOPE),'sby_sha256':sha(out/(task+'.sby')),'invocation_log_sha256':sha(log),'model_calls':0}
    (out/(task+'-result.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--task');p.add_argument('--activation',choices=['active','selected'],default='selected')
    a=p.parse_args();prepare(a.output.resolve(),a.activation) if a.stage=='prepare' else run(a.output.resolve(),a.task)
