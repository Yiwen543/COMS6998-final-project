"""Reuse bounded Claude author/reviewer transport under the new repair registration."""
import argparse
import json
from pathlib import Path
import run_i2c_checker_roles as transport
from prepare_wbxbar_cancel_contract import verify_packet,verify_registration,PRIOR,REG
from run_midterm_fixed import sha


def run(packet,output):
    verify_packet(packet,PRIOR)
    original=transport.call
    def call(prompt,path,env,role):
        return original(prompt,path,env,role.replace('I2C','WBXBAR cancellation contract'))
    transport.call=call
    try:
        transport.run(packet,output,PRIOR)
    finally:
        transport.call=original
        verify_registration()
        if output.exists():
            (output/'role-wrapper.json').write_text(json.dumps({'registration_sha256':sha(REG),
                'wrapper_sha256':sha(Path(__file__)),'transport_sha256':sha(Path(transport.__file__)),
                'new_generation_calls':0,'original_evidence_unchanged':True,
                'policy':'Claude-only exact author patches; fresh read-only review; original pilot immutable.'},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    run(a.packet.resolve(),a.output.resolve())
