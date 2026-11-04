"""Credential-free subprocess controls for the independently authored checker."""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from run_spi_checker_author import validate_source
from run_midterm_fixed import ROOT,sha
from i2c_fixture import OBS,action


def reference_write(byte=0x50):
    """Hand-built legal wire transaction, not simulated from the DUT."""
    rows=[]
    head=False
    def add(scl,sda,n=1,**act):
        nonlocal head
        for i in range(n):
            a=action(**act) if i==0 else action()
            if a['push']:head=True
            o={k:0 for k in OBS}
            o.update(scl=scl,sda=sda,scl_i=scl,sda_i=sda,scl_o=scl,sda_o=sda,
                scl_pin=scl,sda_pin=sda,valid=int(head),depth=int(head),fmt_byte=0x50 if head else 0,
                fmt_start=int(head),fmt_stop=int(head),idle=int(not head),bus_free=int(not head))
            rows.append({'cycle':len(rows),'action':a,'pre':dict(o),'post':dict(o)})
    add(1,1,rst_n=0,enable=0);add(1,1,rst_n=0,enable=0)
    add(1,1,6);add(1,1,push=1,byte=0x50,start=1,stop=1)
    add(1,0,5)
    for i in range(7,-1,-1):
        bit=(byte>>i)&1;add(0,bit,6);add(1,bit,5)
    add(0,0,6);add(1,0,5) # ACK
    add(0,1,2);add(0,0,4);add(1,0,5);add(1,1,5) # STOP setup clock is not a data byte
    rows[-1]['pre']['ready']=1
    head=False;add(1,1,8)
    return rows


def worker(candidate,base,out):
    import resource
    resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    auth=json.loads((candidate/'authorship.json').read_text())
    for f,h in auth['artifact_sha256'].items():
        if sha(candidate/f)!=h:raise ValueError('Checker authorship hash drift')
    def module(path):
        s=path.read_text();validate_source(s);ns={};exec(compile(s,str(path),'exec'),ns);return ns
    check=module(candidate/'checker.py')['check_rows']
    try:selftest=module(candidate/'selftest.py')['run'](check)
    except Exception as e:selftest={'error_type':type(e).__name__,'detail':str(e)}
    cases={'independent_write':reference_write(),'wrong_wire_byte':reference_write(0x51)}
    reset_bad=reference_write();reset_bad[0]['post']['sda_o']=0;cases['wrong_reset_output']=reset_bad
    trunc=reference_write()[:70];cases['truncated']=trunc
    for path in sorted((base/'driver-v2').glob('*.trace.json')):cases['dut_'+path.name.split('.')[0]]=json.loads(path.read_text())
    event_controls=[]
    for family,slug in [('stretch_recovery','stretch'),('nak_restart','nak_restart'),('nak_timeout_recovery','nak_timeout')]:
        good=cases['dut_'+slug]
        fault=copy.deepcopy(good)
        push_cycles=[r['cycle'] for r in good if r['action']['push']]
        start=push_cycles[-1]
        fault[start]['action']['byte']^=1
        for r in fault[start:]:
            for ph in ['pre','post']:
                if r[ph]['valid']:r[ph]['fmt_byte']^=1
        name='bad_byte_during_'+slug;cases[name]=fault
        event_controls.append({'name':name,'baseline':'dut_'+slug,'family':family})
        name='truncated_'+slug;cases[name]=copy.deepcopy(good[:start+90])
        event_controls.append({'name':name,'baseline':'dut_'+slug,'family':family,'truncated':True})
    results={name:check(rows) for name,rows in cases.items()}
    clean=lambda x:not x['failures'] and not x['assumption_violations']
    baseline=clean(results['independent_write'])
    for item in event_controls:
        r=results[item['name']]
        item['baseline_clean']=clean(results[item['baseline']])
        item['success_rejected']=not any(e.get('kind')=='success' and e.get('family')==item['family'] for e in r['events'])
        item['credited_detection']=item['baseline_clean'] and item['success_rejected'] and (item.get('truncated',False) or bool(r['failures']))
    result={'author_selftests':selftest,'independent_baseline_pass':baseline,'cases':results,
            'negative_controls':[{'name':name,'rejected':bool(results[name]['failures']),
                                  'credited_detection':baseline and bool(results[name]['failures'])}
                                 for name in ['wrong_wire_byte','wrong_reset_output']],
            'truncated_no_success':not any(e.get('kind')=='success' for e in results['truncated']['events']),
            'event_controls':event_controls,'checker_sha256':sha(candidate/'checker.py')}
    out.mkdir(parents=True,exist_ok=False)
    (out/'evaluator-source.py').write_bytes(Path(__file__).read_bytes())
    (out/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'private-controls.json').write_text(json.dumps({k:v for k,v in cases.items() if not k.startswith('dut_')},indent=2)+'\n')
    print(json.dumps({'baseline':baseline,'case_failures':{k:len(v['failures']) for k,v in results.items()}}))


def evaluate(candidate,base,out):
    # Pure-code restrictions supplement subprocess isolation; not an OS security proof.
    env={k:v for k,v in os.environ.items() if not any(t in k.upper() for t in ('KEY','TOKEN','SECRET','CREDENTIAL','PASSWORD'))}
    script=Path(__file__).resolve()
    with tempfile.TemporaryDirectory(prefix='i2c-controls-') as cwd:
        code='import sys;sys.path.insert(0,'+repr(str(script.parent))+');from evaluate_i2c_checker import worker;from pathlib import Path;worker(*map(Path,sys.argv[1:]))'
        p=subprocess.run([sys.executable,'-I','-c',code,str(candidate),str(base),str(out)],cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
    if p.returncode:raise RuntimeError(p.stderr)
    return p.stdout


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(evaluate(a.candidate.resolve(),a.base.resolve(),a.output.resolve()))
