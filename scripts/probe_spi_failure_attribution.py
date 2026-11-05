"""Private diagnostic inputs only; original DUT, driver and Claude checker fixed.

Measure public observations without inventing a golden model or editing verdicts.
New controls never enter experimental model prompts or target selection.
"""
import argparse
import json
from pathlib import Path
from spi_core_safe_experiment import verify_freeze
from spi_core_safe_interface import action,seed
from spi_core_safe_runtime import BASE,simulate
from run_midterm_fixed import sha

def probe(out):
    f=verify_freeze();pre=BASE/'preflight-v3';out.mkdir(parents=True,exist_ok=False)
    cases={}
    for name,first_change,second_change in [
      ('same_config_held_cs',{},{}),('clkdiv_only_same_cs',{}, {'clkdiv':2}),
      ('changed_csid_and_cpol',{}, {'csid':1,'cpol':1}),('released_cs_then_cpol',{'keep_cs':0},{'cpol':1}),
      ('cpol_only_cpha0',{}, {'cpol':1}),('cpol_only_cpha1',{'cpha':1},{'cpol':1,'cpha':1})]:
        aa=seed()+[action(sd=10) for _ in range(128)]
        first=dict(cmd_offer=1,write=1,read=0,speed=2,csid=0,length=0,keep_cs=1,clkdiv=1,idle=1,lead=1,trail=1,cpha=0,cpol=0,
            tx_offer=1,tx_data=165,tx_be=1,sd=10)
        first.update(first_change);second={**first,'write':0,'read':1,'keep_cs':0,'tx_offer':0};second.update(second_change)
        aa[8]=action(**first);aa[9]=action(**second);cases[name]=aa
    (out/'control-definition.json').write_text(json.dumps(cases,indent=2)+'\n')
    records={};executions=0;cycles=0;seconds=0
    for name,aa in cases.items():
        observations=[]
        for tool,binary in [('verilator',pre/'verilator/obj/Vtb_spi_core'),('iverilog',pre/'iverilog/tb.vvp')]:
            r,_,t,q=simulate(binary,aa,out/name/tool,tool);executions+=1;cycles+=len(t);seconds+=r['simulation_seconds']
            observations.append((r,t,q))
        a,b=observations
        if a[1:]!=b[1:] or a[0]['checker']!=b[0]['checker']:raise ValueError('Dual simulator disagreement: '+name)
        r,t,q=a
        accepted=[{'cycle':x['cycle'],'offer_id':y['cmd_accept_id'],'configuration':{k:x['action'][k] for k in ('csid','keep_cs','clkdiv','cpol','cpha','idle','lead','trail')}} for x,y in zip(t,q) if y['cmd_accept_id']>=0]
        transitions=[];previous=3
        for x in t:
            for phase in ('pre','post'):
                value=x[phase]['csb']
                if value!=previous:transitions.append({'cycle':x['cycle'],'phase':phase,'before':previous,'after':value});previous=value
        records[name]={'checker':r['checker'],'delivery_complete':r['delivery_complete'],'accepted_commands':accepted,
            'csb_transitions':transitions,'dual_simulator_equal':True,
            'interpretation':'Observed transitions/verdict only. No GPT-authored expected-output rule.'}
        print(name,r['checker']['verdict'],len(r['checker']['failures']),flush=True)
    # Exact accepted-cycle correction for the independent review's hand decoding.
    originals={}
    for case,rep in [('case_x',3),('case_z',2)]:
        p=BASE/f'b-live-v1/rep{rep}/round6';t=json.loads((p/'trace.json').read_text());q=json.loads((p/'transport.json').read_text())
        originals[case]=[{'cycle':r['cycle'],'offer_id':s['cmd_accept_id'],'csid':r['action']['csid'],'keep_cs':r['action']['keep_cs'],
            'cpol':r['action']['cpol'],'cpha':r['action']['cpha']} for r,s in zip(t,q) if s['cmd_accept_id']>=0]
    aa=json.loads((BASE/'b-live-v1/rep1/round6/requests.json').read_text())['actions']
    r,_,t,q=simulate(pre/'iverilog/tb.vvp',aa,out/'positive_case_y_iverilog','iverilog');executions+=1;cycles+=len(t);seconds+=r['simulation_seconds']
    p=BASE/'b-live-v1/rep1/round6'
    positive_equal=t==json.loads((p/'trace.json').read_text()) and q==json.loads((p/'transport.json').read_text()) and r['checker']==json.loads((p/'result.json').read_text())['checker']
    assert positive_equal
    result={'status':'controls_executed_not_new_checker_certification','controls':records,
      'exact_original_acceptance':originals,'positive_case_y_dual_simulator_equal':positive_equal,
      'new_compilations':0,'executions':executions,'executed_cycles':cycles,'simulation_seconds':seconds,'model_calls':0,
      'checker_sha256':f['checker_sha256'],'script_sha256':sha(Path(__file__)),
      'limits':'Finite controls only; no independent golden formal proof; old verdicts and checker unchanged. These are diagnostic inputs, not LLM/B results.'}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();probe(a.output.resolve())
