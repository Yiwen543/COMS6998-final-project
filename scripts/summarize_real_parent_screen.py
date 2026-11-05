"""Evidence-based gate decision. No functional verdict or model access."""
import argparse
import json
import re
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from probe_spi_core_events import identity

COMMAND=('csid','speed','write','read','length','keep_cs','clkdiv','idle','lead','trail','full_cycle','cpha','cpol')

def transport_violations(rows):
    """Input-agent transport obligations only, not expected DUT behavior."""
    pending={'command':None,'tx':None};errors=[]
    for r in rows:
        a,p=r['action'],r['pre']
        if not a['rst_n'] or a['sw_reset']:
            pending={'command':None,'tx':None};continue
        for name,v,ready,fields in [('command','valid','ready',COMMAND),('tx','tx_valid','tx_ready',('tx_data','tx_be'))]:
            data=tuple(a[x] for x in fields)
            if pending[name] is not None and (not a[v] or data!=pending[name]):errors.append({'cycle':r['cycle'],'channel':name,'reason':'Offered valid/payload not held until acceptance/reset'})
            pending[name]=data if a[v] and not p[ready] else None
    return errors

def summarize(base):
    def load(p):return json.loads((base/p).read_text())
    ax=load('axi_dma/screen-v1/screen.json');sp=load('spi_host_core_v2/screen-v2/screen.json');obs=load('spi_core_events-v3/observations.json')
    proof_paths=['axi_dma/proof-v3/proof.json','spi_host_core_v2/proof-v4/proof.json']
    for name in proof_paths:
        proof=load(name)
        if proof['status']!='pass':raise ValueError('Proof not passing')
        for p,h in proof['hashes'].items():
            if sha(Path(p))!=h:raise ValueError('Proof provenance changed: '+p)
    for p,h in obs['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Observation implementation changed: '+p)
    if obs['screen_sha256']!=sha(base/'spi_host_core_v2/screen-v2/screen.json'):raise ValueError('Observation/screen drift')
    old={identity(p):p['hits'] for p in load('spi_host_core_v2/inventory/raw-points.json')}
    new={identity(p):p['hits'] for p in load('spi_core_events-v3/seed/raw-points.json')}
    if old.keys()!=new.keys():raise ValueError('Original counter denominator changed')
    transitions=[{'identity':list(k),'inventory_hits':old[k],'driver_hits':new[k]} for k in old if (old[k]>0)!=(new[k]>0)]
    if any(x['identity'][3]!='toggle' or x['identity'][4]!='rst_ni:1->0' for x in transitions):raise ValueError('Unexpected seed activity difference')
    ordinary=set();rows=[]
    for r in obs['cases']:
        if r['case'].startswith('ordinary'):ordinary|={g['eclass'] for g in r['groups'] if g['all_source_counters_hit']}
    for r in obs['cases']:
        trace=load('spi_core_events-v3/'+r['case']+'/trace.json');violations=transport_violations(trace)
        if violations:raise ValueError('Private calibration transport invalid: '+str(violations))
        reached={g['eclass'] for g in r['groups'] if g['all_source_counters_hit']}
        rows.append({'case':r['case'],'cycles_including_seed':r['cycles_per_simulator'],'transport_violations':violations,
            'simulator_trace_agreement':r['trace_agreement'],'accepted_commands':r['observations']['accepted_commands'],
            'tx_stall_cycles':len(r['observations']['tx_stall_cycles']),'rx_stall_cycles':len(r['observations']['rx_stall_cycles']),
            'fully_hit_groups':sorted(reached),'additional_groups_over_ordinary_union':sorted(reached-ordinary),
            'functional_status':'unjudged_pending_independent_checker'})
    if any(g['all_source_counters_hit'] for g in obs['cases'][0]['groups']):raise ValueError('Selected groups no longer seed zero')
    attempts=[]
    for folder in sorted(base.glob('spi_core_events-v*')):
        simulations=[]
        for log in sorted(folder.glob('*/*.log')):
            if log.name not in ('verilator.log','iverilog.log'):continue
            done=re.findall(r'DRIVER_OK steps=(\d+)',log.read_text())
            simulations.append({'log':str(log.relative_to(base)),'executed_cycles':int(done[-1]) if done else None,'completed':bool(done)})
        attempts.append({'directory':folder.name,'compilation_attempts':len(list(folder.glob('*/compile.log'))),'simulations':simulations})
    def static(s):return {k:s[k] for k in ['raw_targets','typed_supported','mapped','unresolved','raw_dut_denominator','static_candidate_groups','nontrivial_static_candidates','static_count_gate_pass','pair_counts']}
    result={'scope_sha256':sha(ROOT/'configs/real_parent_screen.json'),'repository_commit':json.loads((ROOT/'configs/real_parent_screen.json').read_text())['repository_commit'],
        'status':'SPI static/driver gate passed; independent checker construction is next; B remains blocked',
        'candidate_decisions':{'axi_dma':{'status':'static_target_gate_rejected',**static(ax)},
            'spi_host_core':{'status':'eligible_for_independent_checker_construction_only',**static(sp)},
            'i2c_master_axil':{'status':'adapter_blocked','evidence':'i2c_master_axil/adapter-gate.json'},
            'flash_ctrl':{'status':'multiclock_dependency_scope_deferred_before_execution'}},
        'ordinary_control_union_groups':sorted(ordinary),'calibration_observations':rows,
        'limits':['Observed recovery is not specification-validated recovery.',
            'TX and RX stalls share one equivalent guard group; do not count them as two distinct semantic groups.',
            'A software-reset predicate is not proof of abort/restart correctness or a necessarily difficult target.',
            'SPI was already explored as a standalone FSM; this is a new integration scope of the same IP family, not an independent held-out design.',
            'Independent checker controls, event-to-source specificity, and B development acceptance remain outstanding. Static gate alone never enables B.',
            'No evidence here establishes C over B. Most groups are reached by ordinary transfers.'],
        'reset_policy':{'fresh_process':True,'seed_cycles':8,'initial_settle_ns':1,'extra_clock_cycles':0,'denominator_identical':True,'initial_reset_toggle_differences':transitions,'qualification_groups_remain_seed_zero':True},
        'accounting':{'live_model_calls':0,'API_tokens':0,'final_calibration_compilations':len(obs['compilations']),'final_calibration_executions':obs['executions'],'final_calibration_cycles_all_simulators':obs['total_executed_cycles'],'all_calibration_attempts_compilations':sum(x['compilation_attempts'] for x in attempts),'all_calibration_attempts_executions':sum(len(x['simulations']) for x in attempts),'all_calibration_attempts_cycles_all_simulators':sum(s['executed_cycles'] or 0 for x in attempts for s in x['simulations']),'attempts':attempts,'failed_first_attempt':'v1 reset assertion at time zero produced pre-edge simulator mismatch; retained; fixed 1 ns inactive-reset settle without adding a clock cycle','rejected_case_in_v2':'Single-cycle CSID-switch offer withdrew valid while not ready; v3 holds through acceptance.'},
        'B_allowed':False,'checker_started':False,'OpenAI_key_requested':False,
        'checker_packet':'spi-core-spec-packet-v2','checker_request_ready':True,
        'next_gate':'Claude authors from isolated public spec/interface; independent controls and fresh review. Do not run B if selected events lack correct checker support or required distinct reachable source targets.',
        'hashes':{str(p):sha(p) for p in [Path(__file__),base/'spi_host_core_v2/screen-v2/screen.json',base/'axi_dma/screen-v1/screen.json',base/'spi_core_events-v3/observations.json',base/'spi-core-spec-packet-v2/packet.json']}}
    (base/'decision.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);r=summarize(p.parse_args().base.resolve());print(r['status'])
