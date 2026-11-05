"""One bounded, tool-free Claude design call; no checker/driver/DUT changes."""
import argparse
import json
import os
from pathlib import Path
from prepare_wbxbar_conformance_role import verify_packet
from probe_wbxbar_cancel_boundary import verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE


def run(packet,output):
    verify_packet(packet)
    if output.exists():raise ValueError('Never overwrite a model call')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode&0o077:raise ValueError('Hidden key absent or unsafe')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    try:
        result=call((packet/'prompt.txt').read_text(),output,env,'WBXBAR independent specification and property architect')
        expected={'clause_matrix','ownership_algorithm','formal_obligations','synthetic_control_assessments','implementation_plan','unresolved','ready_for_implementation'}
        if set(result)!=expected or type(result['ready_for_implementation']) is not bool:raise ValueError('Design response schema')
        (output/'design.json').write_text(json.dumps(result,indent=2)+'\n')
        return {'design_received':True,'model_ready_for_implementation':result['ready_for_implementation'],'checker_changed':False,'live_B_allowed':False,'live_C_allowed':False}
    finally:
        KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None);verify_scope()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.packet.resolve(),a.output.resolve()),indent=2))
