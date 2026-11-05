"""Execute intentionally broken SV transport variants, isolated from production.

No mutation is used by the LLM runner. Checks intent delivery, not DUT golden data.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_runtime import DRIVER,compile_driver,simulate,SafeExecutionError
from spi_core_safe_interface import FIELDS,STATE
from spi_core_interface import FIELDS as PINS,parse as pin_parse
from preflight_spi_core_safe_driver import cases

def run(out,preflight):
    out.mkdir(parents=True,exist_ok=False);source=DRIVER.read_text();data=cases();records=[]
    modifications={
        'dropped_offer':('calibration_partial_then_csid_switch',[
            ('if(v_cmd_offer) begin','if(v_cmd_offer && cycle!=8) begin')]),
        'duplicate_acceptance':('calibration_partial_then_csid_switch',[
            ('cmd_taken=cmd_ids[ch];ch=ch+1;cmd_accepted=cmd_accepted+1;',
             'cmd_taken=cmd_ids[ch];if(cycle!=8) ch=ch+1;cmd_accepted=cmd_accepted+1;'),
            ('if(cmd_offered!=cmd_accepted+cmd_cancelled+ct-ch) $fatal(1,"Command conservation");','// Deliberately disabled in this duplicate fault only.')]),
        'reordered_head':('pending_queues_hardware_abort_restart',[
            ('command_i=cmd_mem[ch];command_csid_i=csid_mem[ch];','command_i=cmd_mem[ct-1];command_csid_i=csid_mem[ct-1];')]),
        'post_edge_acceptance':('calibration_partial_then_csid_switch',[
            ('cmd_fire=command_valid_i && command_ready_o;','cmd_fire=0; // Deliberate wrong sampling phase'),
            ('if(cmd_fire) begin cmd_taken','cmd_fire=command_valid_i && command_ready_o;\nif(cmd_fire) begin cmd_taken')])}
    for name,(case,patches) in modifications.items():
        variant=source
        for old,new in patches:
            if variant.count(old)!=1:raise ValueError('Nonunique mutation')
            variant=variant.replace(old,new,1)
        path=out/(name+'.sv');path.write_text(variant)
        binary,compile_record=compile_driver(out/name/'compiled',driver=path)
        rejected=None
        try:simulate(binary,data[case],out/name/'execution')
        except SafeExecutionError as e:rejected={'stage':e.stage,'detail':str(e)}
        if not rejected or rejected['stage']!='transport':raise ValueError('Fault did not fail the transport oracle: '+name)
        folder=out/name/'execution';log=(folder/'simulation.log').read_text();actual=[];queue=[]
        for line in log.splitlines():
            if line.startswith('TRACE '):
                v=list(map(int,line.split()[1:]));actual.append(dict(zip(PINS,v[1:1+len(PINS)])))
            if line.startswith('QUEUE '):queue.append(dict(zip(STATE,map(int,line.split()[1:]))))
        trace=pin_parse(log,actual)
        ids=[r['cmd_accept_id'] for r in queue if r['cmd_accept_id']!=-1]
        duplicates=sorted(k for k,v in Counter(ids).items() if v>1)
        if name=='duplicate_acceptance' and not duplicates:raise ValueError('No actual duplicate acceptance generated')
        differences=[r['cycle'] for r in trace if r['pre']['ready']!=r['post']['ready']]
        if name=='post_edge_acceptance' and not differences:raise ValueError('No pre/post ready difference exercised')
        (folder/'actual-trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n')
        records.append({'name':name,'source_case':case,'source_sha256':sha(path),'patches':patches,
            'compile':compile_record,'rejection':rejected,'executed_cycles':len(trace),
            'duplicate_accept_ids':duplicates,'pre_post_ready_differ_cycles':differences,
            'execution':json.loads((folder/'execution.json').read_text()),'actual_trace_sha256':sha(folder/'actual-trace.json')})
        print(name,rejected,flush=True)
    short=preflight/'pending_prefix/verilator';full=preflight/'calibration_partial_then_csid_switch/verilator'
    comparisons={}
    for name in ('trace.json','transport.json'):
        a=json.loads((short/name).read_text());b=json.loads((full/name).read_text())
        if a!=b[:len(a)]:raise ValueError('Pending cumulative replay prefix mismatch')
        comparisons[name]={'short_sha256':sha(short/name),'full_sha256':sha(full/name),'prefix_rows':len(a),'equal':True}
    pending=json.loads((short/'transport.json').read_text())[-1]
    full_states=json.loads((full/'transport.json').read_text())
    assert pending['cmd_pending']>0
    result={'status':'pass','new_api_calls':0,'actual_faulty_driver_simulations':len(records),
            'actual_faulty_driver_cycles':sum(r['executed_cycles'] for r in records),'faults':records,
            'pending_prefix_replay':comparisons,'prefix_last_queue':pending,
            'boundary_queue_excerpt':full_states[86:93],
            'production_driver_sha256':sha(DRIVER),'script_sha256':sha(Path(__file__)),
            'scope':'Protocol delivery oracle rejects actual faulty SV drivers. Original DUT/checker and live driver unchanged. Not a DUT bug test.'}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight',type=Path,required=True);a=p.parse_args();run(a.output.resolve(),a.preflight.resolve())
