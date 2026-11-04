#!/usr/bin/env python3
"""Offline frontend-only probe of a different natural controller; no qualification claim."""
import argparse
import json
import subprocess
import time
from pathlib import Path
from run_midterm_fixed import ROOT, sha
from spi_semantic_v2 import RichAdapter


def probe(output):
    output.mkdir(parents=True,exist_ok=False)
    tools=ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin'
    base=ROOT/'third_party/opentitan_candidate/hw/ip'
    files=[base/'i2c/rtl/i2c_pkg.sv',base/'i2c/rtl/i2c_controller_fsm.sv']
    sources=[str(p.relative_to(ROOT)) for p in files]
    inc=str((base/'prim/rtl').relative_to(ROOT))
    top='i2c_controller_fsm'
    records=[]
    def call(name,argv):
        start=time.perf_counter()
        p=subprocess.run(list(map(str,argv)),cwd=ROOT,capture_output=True,text=True,timeout=90)
        (output/(name+'.log')).write_text(p.stdout+p.stderr)
        records.append({'stage':name,'command':list(map(str,argv)), 'returncode':p.returncode,
                        'seconds':time.perf_counter()-start})
        return p.returncode
    status=call('slang',[tools/'slang','--single-unit','--top',top,'-D','SYNTHESIS','-I',inc,
               '--ast-json',output/'ast.json','--ast-json-source-info','--ast-json-detailed-types',*sources])
    call('verilator',['verilator','--lint-only','--timing','-Wno-fatal','--top-module',top,
                      '-DSYNTHESIS','-I'+inc,*sources])
    call('iverilog',['iverilog','-g2012','-s',top,'-DSYNTHESIS','-I',inc,'-tnull',*sources])
    yosys_script=f'read_slang --single-unit --top {top} -D SYNTHESIS -I {inc} '+ ' '.join(sources)+f'; proc; write_json {output}/netlist.json'
    (output/'probe.ys').write_text(yosys_script+'\n')
    call('yosys',[tools/'yosys','-Q','-T','-s',output/'probe.ys'])
    counts={}
    if status==0:
        adapter=RichAdapter(json.loads((output/'ast.json').read_text()),top).extract()
        artifact={'targets':adapter.targets,'atoms':adapter.atoms,'unsupported':adapter.unsupported}
        (output/'lexical-predicates.json').write_text(json.dumps(artifact,indent=2)+'\n')
        counts={'lexical_targets':len(adapter.targets),'typed_atoms':len(adapter.atoms),
                'unsupported_extraction_entries':len(adapter.unsupported)}
    result={'candidate':'OpenTitan I2C controller FSM; distinct IP from SPI_HOST, same upstream repository',
        'revision':subprocess.check_output(['git','-C',str(ROOT/'third_party/opentitan_candidate'),'rev-parse','HEAD'],text=True).strip(),
        'sources_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files+[base/'i2c/doc/theory_of_operation.md',base/'i2c/doc/registers.md']},
        'parameters':{'FifoDepth':64},'runs':records,**counts,
        'spec_event_candidates':['clock stretch then resume','unexpected NACK, software handling and repeated START','NACK-handler timeout, automatic STOP and release'],
        'required_assumptions':['open-drain wired-AND bus model','legal positive timing parameters','stable FMT entry until ready','responsive target except deliberate bounded stretch/NACK'],
        'no_model_calls':True,'qualified':False,
        'unresolved':['Independent specification checker and fixed driver absent','No reachability or original-counter source mapping','No certified nontrivial groups','No B development run'],
        'interpretation':'Frontend feasibility and public temporal-behavior shortlist only; module size is not the selection criterion.'}
    (output/'probe.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    result=probe(args.output.resolve())
    print(json.dumps({'stages':[(r['stage'],r['returncode']) for r in result['runs']],
        'lexical_targets':result.get('lexical_targets'),'qualified':result['qualified']},indent=2))
