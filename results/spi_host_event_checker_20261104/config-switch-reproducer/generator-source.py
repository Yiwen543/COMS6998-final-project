#!/usr/bin/env python3
"""Reproduce and inventory a public-pin discrepancy; not a replacement checker."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import SOURCE, DRIVER, TOP, simulate, verify_source
from spi_host_fixture import parse


def inspect(calibration, output):
    output.mkdir(parents=True,exist_ok=False)
    verify_source()
    full=json.loads((calibration/'configuration_switch/actions.json').read_text())['actions']
    actions=full[:50]
    (output/'actions.json').write_text(json.dumps({'actions':actions},indent=2)+'\n')
    binaries={'verilator':calibration/'compile-verilator/verilator-build'/('V'+TOP),
              'iverilog':calibration/'compile-iverilog'/(TOP+'.vvp')}
    records={}
    for simulator,binary in binaries.items():
        folder=output/simulator;folder.mkdir()
        result=simulate(binary,actions,folder,simulator=simulator)
        rows=parse((folder/'batch.sim.log').read_text(),actions)
        (folder/'rows.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
        records[simulator]={'cycles':len(actions),'simulation_seconds':result['simulation_seconds'],
            'rows_sha256':sha(folder/'rows.json'),'last_rows':rows[-3:],
            'legacy_checker_scope_verdict':result['checker']['verdict']}
    same=records['verilator']['last_rows']==records['iverilog']['last_rows']
    rtl=SOURCE.read_text().splitlines()
    artifact={'status':'reproduced_public_pin_discrepancy; not a full-peripheral or formal defect proof',
        'dut_sha256':sha(SOURCE),'driver_sha256':sha(DRIVER),'actions_sha256':sha(output/'actions.json'),
        'same_public_trace':(output/'verilator/rows.json').read_bytes()==(output/'iverilog/rows.json').read_bytes(),
        'simulations':2,'executed_cycles':100,'compilations':0,'records':records,
        'spec_references':{'file':'third_party/opentitan_candidate/hw/ip/spi_host/doc/theory_of_operation.md',
            'lines':[241,246,247,248,249,323,324],
            'rule':'CONFIGOPTS changes while CSAAT was held require ending the old transaction and changing configuration with all selects inactive.'},
        'rtl_review':[{'start_line':start,'end_line':end,'text':'\n'.join(rtl[start-1:end])}
                      for start,end in [(123,130),(133,140),(198,207),(210,236)]],
        'adapter_review':'Fixed SV assigns config fields by named struct member; pre/post samples bracket the rising edge. Input JSON values and echoed TRACE inputs agree. Different simulators agree. No checker source or RTL was changed to obtain this trace.',
        'observations':'At cycle 49 a same-CSID configuration-changed command is accepted while csb stays 2; SCK changes 0 to 1. The full trace has no all-high gap before the changed-config transfer. The active-CS next-state path checks changed CSID but not config_changed; the idle path checks config_changed.',
        'classification':'One candidate specification/implementation discrepancy: reconfiguration while CS remains active. Related clock/select symptoms are not counted as separate defects.',
        'remaining':'Independent full-IP interface-assumption review and/or formal property before an upstream-confirmed defect claim. This evidence is excluded from experimental stimulus prompts.'}
    (output/'evidence.json').write_text(json.dumps(artifact,indent=2)+'\n')
    return artifact


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--calibration',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True);args=cli.parse_args()
    d=inspect(args.calibration.resolve(),args.output.resolve())
    print(json.dumps({k:d[k] for k in ('status','same_public_trace','simulations','executed_cycles')},indent=2))
