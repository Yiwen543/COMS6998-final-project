#!/usr/bin/env python3
"""Replay fixed JSON on the original SPI DUT with the frozen Claude event checker."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import compile_driver, simulate
from spi_host_fixture import validate_actions, parse
from evaluate_spi_checker_candidate import load_candidate

PROFILE=ROOT/'examples/heldout_spi_host_events'


def require_freeze():
    freeze=json.loads((PROFILE/'freeze.json').read_text())
    for name,digest in freeze['hashes'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Frozen event boundary changed: '+name)
    return freeze


def run(actions_file, output):
    freeze=require_freeze()
    actions=validate_actions(json.loads(actions_file.read_text()),100000,require_initial_reset=True)
    output.mkdir(parents=True,exist_ok=False)
    binary,command,seconds=compile_driver(output)
    data=simulate(binary,actions,output)
    # The shared legacy helper's diagnostic remains visible but does not judge
    # the newly scoped events. It never changes simulation execution or counters.
    legacy=data.pop('checker')
    rows=parse((output/'batch.sim.log').read_text(),actions)
    checker=load_candidate(PROFILE/'checker.py')['check_rows'](rows)
    result={**data,'checker':checker,'legacy_checker_diagnostic':legacy,
        'compile_seconds':seconds,'compile_command':list(map(str,command)),
        'compilations':1,'simulator_executions':1,'executed_cycles':len(actions),
        'model_calls':0,'checker_role':'claude-opus-5-5','stimulus_role':freeze['roles']['stimulus'],
        'freeze_sha256':sha(PROFILE/'freeze.json'),
        'event_policy':'Keep event-window status AND overall trace verdict; a local event in a failing trace is not clean-trace qualification.'}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--actions',type=Path,required=True);cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args();r=run(args.actions.resolve(),args.output.resolve())
    print(json.dumps({'verdict':r['checker']['verdict'],'events':r['checker']['events'],
                      'coverage':r['coverage']},indent=2))
