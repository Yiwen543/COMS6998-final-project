"""Post-review offline control repairs; original Claude source stays immutable."""
import argparse
import copy
import json
from pathlib import Path
import probe_spi_core_events as runner
from spi_core_interface import action,seed
from run_midterm_fixed import sha

def cases():
    def write():
        a=seed()+[action(sd=10) for _ in range(128)]
        a[8].update(tx_data=0xa5a5a5a5,tx_be=15,tx_valid=1)
        a[10].update(valid=1,write=1,length=3)
        return a
    good=write();bad=write();bad[28].update(valid=1,read=1,length=3)
    hw=seed()+[action(sd=10) for _ in range(176)]
    hw[8].update(valid=1,read=1,length=19)
    for i in (48,49):hw[i].update(rst_n=0)
    hw[58].update(tx_data=0xa5a5a5a5,tx_be=15,tx_valid=1)
    hw[60].update(valid=1,write=1,length=3)
    return {'uniform_write_baseline':good,'withdraw_pending_command':bad,'hardware_abort_restart':hw}

def prepare_controls(sim,out):
    out.mkdir(parents=True,exist_ok=False)
    data={n:json.loads((sim/n/'trace.json').read_text()) for n in cases()}
    if not data['withdraw_pending_command'][28]['action']['valid'] or data['withdraw_pending_command'][28]['pre']['ready']:raise ValueError('Control did not offer while blocked')
    # One changed input action, with genuinely re-simulated DUT outputs.
    bad=copy.deepcopy(data['hardware_abort_restart']);bad[48]['post']['csb']=0;data['negative/hardware_reset_select']=bad
    data['truncated/hardware_abort']=copy.deepcopy(data['hardware_abort_restart'][:50])
    controls=[
        {'name':'uniform_write_baseline','kind':'observational_positive','expected':'Scoped pass; repeating bytes intentionally avoid unresolved byte-order convention; no new endian validation'},
        {'name':'withdraw_pending_command','kind':'input_protocol','baseline':'uniform_write_baseline','expected':'Assumption violation at cycle29; outputs re-simulated rather than copied'},
        {'name':'hardware_abort_restart','kind':'observational_positive','expected':'Hardware reset during active RX, fresh TX completes; event checked offline, not formal proof'},
        {'name':'negative/hardware_reset_select','kind':'single_fault','baseline':'hardware_abort_restart','expected':'Reset CS violation; credit only on clean baseline','changes':[{'cycle':48,'side':'post','field':'csb','after':0}]},
        {'name':'truncated/hardware_abort','kind':'incomplete','baseline':'hardware_abort_restart','expected':'No successful restart before reset release/new command'}]
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'post-review supplemental controls, not in initial reviewer packet','script_sha256':sha(Path(__file__)),'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'cases':len(data),'new_model_calls':0,'source':'Actual new dual-simulator traces plus disclosed single-fault and truncation controls'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--screen',type=Path,required=True);a=p.parse_args();out=a.output.resolve()
    runner.cases=cases;runner.run(out/'simulation',a.screen.resolve());prepare_controls(out/'simulation',out/'controls')
