"""Private offline READB reachability probes, never experimental prompt material."""
import argparse
import copy
import json
from pathlib import Path
from i2c_read_fixture import action, seed
from run_i2c_read_fixed import compile_driver, simulate


def batches():
    cases={'seed':seed()}
    for name in ['ordinary_write','ordinary_read','multi_read','rcont_chain','read_restart','read_stretch','zero_count_partial']:
        a=seed()+[action() for _ in range(384)]
        a[8]=action(push=1,byte=0x50 if name=='ordinary_write' else 0x51,start=1,stop=int(name=='ordinary_write'))
        if name!='ordinary_write':
            a[9]=action(push=1,byte=2 if name=='multi_read' else (0 if name=='zero_count_partial' else 1),
                        read=1,stop=int(name not in ['rcont_chain','read_restart']),rcont=int(name=='rcont_chain'))
        if name=='rcont_chain':a[10]=action(push=1,byte=1,read=1,stop=1)
        if name=='read_restart':a[10]=action(push=1,byte=0x50,start=1,stop=1)
        if name=='read_stretch':
            for i in range(134,153):a[i]['stretch']=1
        cases[name]=a
    varied=copy.deepcopy(cases['multi_read'])
    for a in varied[230:]:a['target_data']=0x3C
    cases['multi_read_varied']=varied
    return cases


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--simulator',choices=['verilator','iverilog'],default='verilator');a=p.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    binary=compile_driver(out,a.simulator)
    for name,actions in batches().items():
        result,_=simulate(binary,actions,out,name,a.simulator)
        print(json.dumps({'name':name,'cycles':result['steps'],'environment_valid':result['environment_valid']}),flush=True)
