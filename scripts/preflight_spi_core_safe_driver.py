"""Fixed private transport controls, unchanged checker and original 17 targets."""
import argparse
import copy
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_experiment import BASE as OLD_BASE,verify_freeze,check_trace
from spi_core_safe_runtime import compile_driver,simulate,PREREG,DRIVER
from spi_core_safe_interface import seed,action,offers_from_legal_trace,parse
from evaluate_spi_core_checker import scoped_pass

def cases():
    result={}
    old=OLD_BASE/'spi_core_events-v3'
    for name in ['seed','ordinary_standard_write','ordinary_three_speeds','ordinary_fullcycle_read',
                 'tx_starvation_resume','rx_backpressure_resume','partial_then_csid_switch']:
        result['calibration_'+name]=offers_from_legal_trace(json.loads((old/name/'trace.json').read_text()))
    def batch(n):return seed()+[action() for _ in range(n)]
    q=batch(40)
    for i in range(8,24):q[i].update(tx_offer=1,tx_data=0x11223300+i,tx_be=15)
    result['tx_queue_pending_at_eof']=q
    a=batch(112)
    a[8].update(cmd_offer=1,read=1,length=31)
    for i in range(9,13):a[i].update(cmd_offer=1,read=1,length=0,csid=i%2)
    for i in range(10,26):a[i].update(tx_offer=1,tx_be=15,tx_data=0x22334400+i)
    a[40]=action(rst_n=0);a[41]=action(rst_n=0)
    a[48].update(tx_offer=1,tx_be=15,tx_data=0x12345678)
    a[49].update(cmd_offer=1,write=1)
    result['pending_queues_hardware_abort_restart']=a
    a=batch(80)
    a[8].update(tx_offer=1,tx_be=15,tx_data=0x22222222)
    a[9].update(tx_offer=1,tx_be=15,tx_data=0x22222222)
    a[10].update(cmd_offer=1,write=1,length=7)
    result['same_payload_two_distinct_offers']=a
    result['same_payload_two_offers_complete']=a+[action() for _ in range(96)]
    result['pending_prefix']=result['calibration_partial_then_csid_switch'][:89]
    # Preserve old failure unchanged; this is a labeled PRIVATE transport regression.
    p=OLD_BASE/'spi_core_b_live_v1/rep3/round6/trace.json'
    result['historical_failed_intent_private_regression']=offers_from_legal_trace(json.loads(p.read_text()))
    return result

def preflight(out):
    parent=verify_freeze();out.mkdir(parents=True,exist_ok=False)
    aa=cases();(out/'case-definition.json').write_text(json.dumps(aa,indent=2)+'\n')
    compile_records=[];binaries={};reports={};failures=[];observations=[]
    for tool in ('verilator','iverilog'):
        binaries[tool],m=compile_driver(out/tool,tool);compile_records.append(m)
    for name,requests in aa.items():
        results={};traces={};states={}
        for tool in binaries:
            result,points,trace,state=simulate(binaries[tool],requests,out/name/tool,tool)
            results[tool]=result;traces[tool]=trace;states[tool]=state;observations.append(result)
        if traces['verilator']!=traces['iverilog'] or states['verilator']!=states['iverilog']:
            failures.append(name+': dual simulator disagreement')
        r=results['verilator'];reports[name]={'checker':r['checker'],'transport':r['transport'],
            'delivery_complete':r['delivery_complete'],'verification_complete':r['verification_complete'],
            'cycles':len(requests),'groups':r['groups'],'dual_simulator_agreement':traces['verilator']==traces['iverilog'] and states['verilator']==states['iverilog']}
        if r['checker'].get('assumption_violations'):failures.append(name+': input protocol violation')
        if name.startswith('calibration_') and (not scoped_pass(r['checker']) or not r['delivery_complete']):
            failures.append(name+': calibration not complete and scoped pass')
        print(name,r['checker']['verdict'],'pending',r['transport']['pending'],'groups',sum(g['all_hit'] for g in r['groups']),flush=True)
    # Both queued and presented commands must stay pending at a round boundary.
    for tool in binaries:
        short=json.loads((out/'pending_prefix'/tool/'trace.json').read_text())
        full=json.loads((out/'calibration_partial_then_csid_switch'/tool/'trace.json').read_text())
        if short!=full[:len(short)]:failures.append('cumulative prefix differs: '+tool)
    if not reports['pending_prefix']['transport']['pending']:failures.append('prefix did not exercise pending offer')
    if not reports['tx_queue_pending_at_eof']['transport']['pending']:failures.append('TX pending EOF not exercised')
    if reports['tx_queue_pending_at_eof']['verification_complete']:failures.append('Pending delivery called complete')
    rst=reports['pending_queues_hardware_abort_restart']['transport']['last']
    if not(rst['cmd_cancelled']>0 and rst['tx_cancelled']>0):failures.append('Reset did not cancel both queues')
    hits={g['eclass'] for n,r in reports.items() if n.startswith('calibration_') and scoped_pass(r['checker']) and r['delivery_complete'] for g in r['groups'] if g['all_hit']}
    if hits!={g['eclass'] for g in parent['targets']}:failures.append('Original 17-target reachability not preserved')
    # Deliberate output-trace corruptions test queue oracle AND unchanged Claude checker.
    negatives=[]
    for channel,field in [('cmd','valid'),('cmd','length'),('tx','tx_valid'),('tx','tx_data')]:
        name='calibration_partial_then_csid_switch' if channel=='cmd' else 'tx_queue_pending_at_eof'
        original=json.loads((out/name/'verilator/trace.json').read_text())
        ready='ready' if channel=='cmd' else 'tx_ready';valid='valid' if channel=='cmd' else 'tx_valid'
        index=next(i for i in range(1,len(original)) if original[i-1]['action'][valid] and not original[i-1]['pre'][ready])
        altered=copy.deepcopy(original);altered[index]['action'][field]^=1
        destination=out/'negative'/f'{channel}_{field}';destination.mkdir(parents=True)
        checked=check_trace(altered,destination)
        detected=bool(checked['assumption_violations'])
        from spi_core_safe_interface import TransportOracle
        oracle=TransportOracle();oracle_rejected=False
        for req,row in zip(aa[name],altered):
            if oracle.drive(req)!=row['action']:oracle_rejected=True;break
            oracle.advance(row['pre'])
        negatives.append({'name':f'{channel}_{field}','cycle':index,'checker_assumption_detected':detected,
                          'transport_oracle_rejected':oracle_rejected,'source_case':name})
        if not detected or not oracle_rejected:failures.append('negative not rejected: '+field)
    summary={'status':'pass' if not failures else 'blocked','B_allowed':False,
        'requires_independent_claude_review':True,'failures':failures,'cases':reports,
        'transport_negative_controls':negatives,'unchanged_targets_reachable':sorted(hits),
        'compilations':compile_records,'simulations':len(observations),
        'executed_cycles':sum(r['executed_cycles'] for r in observations),
        'simulation_seconds':sum(r['simulation_seconds'] for r in observations),
        'coverage_denominator':parent['raw_denominator'],'checker_sha256':parent['checker_sha256'],
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [PREREG,DRIVER,Path(__file__),ROOT/'scripts/spi_core_safe_interface.py',ROOT/'scripts/spi_core_safe_runtime.py',out/'case-definition.json']}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'status':summary['status'],'failures':failures,'simulations':len(observations)}))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();preflight(a.output.resolve())
