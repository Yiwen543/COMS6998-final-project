#!/usr/bin/env python3
"""Exercise installed SBY modes with plumbing controls, never score model quality."""
import argparse
import json
from pathlib import Path
from common import BASE, dump
from monitor import compile_monitor, run_formal

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path)
    args=p.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    results=[]
    for label,ok in [('always_true',"6'b111111"),('always_false',"6'b000000")]:
        body=f"assign active=6'b111111;assign ok={ok};"
        candidate={'body':body,'properties':[{'id':f'P{i}','description':'plumbing only'} for i in range(6)]}
        d=out/label
        info=compile_monitor(candidate,d)
        if info['status']!='complete':raise RuntimeError('Smoke monitor compile')
        modes=('bmc','prove','cover') if label=='always_true' else ('bmc',)
        for mode in modes:
            r=run_formal(d,BASE/'public/sfifo.v',out/f'{label}-{mode}',mode)
            results.append({'control':label,'mode':mode,'status':r['status'],'seconds':r['seconds']})
    result={'scope':'toolchain plumbing only; tautologies are not useful FIFO properties',
            'results':results,'expected':['PASS','PASS','PASS','FAIL'],'actual':[r['status'] for r in results]}
    dump(out/'summary.json',result)
    print(json.dumps(result,indent=2))
    if result['actual']!=result['expected']:raise RuntimeError('Formal integration smoke mismatch')

if __name__=='__main__':main()
