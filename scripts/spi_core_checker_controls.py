"""Independent checker controls. GPT authors traces, never expected-output code.

Hand traces below follow the public SPI mode-0 and core byte-order contracts.
They do not read RTL, coverage, or the Claude checker. Model author never sees
these controls; only a separate reviewer sees them after generation.
"""
import argparse
import copy
import json
from pathlib import Path
from spi_core_interface import OUTPUTS,action,seed
from run_midterm_fixed import sha

def reference(payload,read=False):
    """One Standard mode-0 segment, 1..3 bytes, generous CS lead/trail gaps."""
    if not 1<=len(payload)<=3:raise ValueError('Control supports 1..3 bytes')
    rows=[]
    state={**dict.fromkeys(OUTPUTS,0),'csb':3,'tx_ready':1}
    def emit(a=None,**changes):
        nonlocal state
        a=a or action();pre=dict(state);pre['ready']=int(bool(a['enable'] and a['rst_n'] and not state['active']))
        post={**pre,**changes};rows.append({'cycle':len(rows),'action':a,'pre':pre,'post':post});state=post
    for a in seed():emit(a)
    word=sum(b<<(24-8*i) for i,b in enumerate(payload));be=((1<<len(payload))-1)<<(4-len(payload))
    emit(action(tx_data=word,tx_be=be,tx_valid=int(not read)),tx_full=int(not read))
    emit()
    bits=[(b>>i)&1 for b in payload for i in reversed(range(8))]
    emit(action(valid=1,read=int(read),write=int(not read),length=len(payload)-1),
         csb=2,active=1,ready=0,sd=bits[0] if not read else 0,sd_en=1,tx_full=0)
    emit(action(sd=bits[0]<<1 if read else 0))
    for index,bit in enumerate(bits):
        emit(action(sd=bit<<1 if read else 0),sck=1)
        # CPHA=0: change transmitted data only on the trailing clock edge.
        nxt=bits[index+1] if index+1<len(bits) else bit
        emit(action(sd=bit<<1 if read else 0),sck=0,sd=nxt if not read else 0)
    if read:
        emit(action(sd=bits[-1]<<1),rx_valid=1,rx_data=word)
        emit(action(sd=bits[-1]<<1),rx_valid=0)
    else:emit()
    emit(csb=3,active=0,sd_en=0,ready=1)
    for _ in range(3):emit()
    return rows

def prepare(calibration,out):
    out.mkdir(parents=True,exist_ok=False);inputs={};controls=[]
    for name,payload,rd in [('write_one',[0xa1],False),('write_two',[0xa1,0x3c],False),('read_one',[0xa5],True),('read_partial_three',[0xa5,0x5a,0xf0],True)]:
        key='reference/'+name;inputs[key]=reference(payload,rd)
        controls.append({'name':key,'kind':'independent_positive','expected':'no failures/assumption violations; pending or unresolved disclosed separately','authority':'Public theory_of_operation.md mode0 lines 24-42; timing 249-277; byte order/packing 685-740'})
    for folder in sorted(calibration.iterdir()):
        if (folder/'trace.json').exists():inputs['calibration/'+folder.name]=json.loads((folder/'trace.json').read_text())
    def mutation(name,base,fn,expected='DUT violation'):
        rows=copy.deepcopy(inputs[base]);changes=fn(rows)
        if rows==inputs[base]:raise ValueError('No-op control '+name)
        key='negative/'+name;inputs[key]=rows
        controls.append({'name':key,'kind':'single_fault','baseline':base,'expected':expected,'changes':changes,'credit_policy':'Only credit with clean baseline and no assumption violations; not a formal fault coverage claim.'})
    def set_one(rows,pred,side,field,value):
        r=next(r for r in rows if pred(r));old=r[side][field];r[side][field]=value(old)
        return [{'cycle':r['cycle'],'side':side,'field':field,'before':old,'after':r[side][field]}]
    def wrong_tx_bit(rs):
        i=next(r['cycle'] for r in rs if r['pre']['sck']==0 and r['post']['sck']==1);changed=[]
        # The wrong bit is stable before and after the sample edge, avoiding
        # any ambiguity about simultaneous data/clock changes.
        for j,side in [(i-1,'post'),(i,'pre'),(i,'post')]:
            old=rs[j][side]['sd'];rs[j][side]['sd']=old^1
            changed.append({'cycle':j,'side':side,'field':'sd','before':old,'after':old^1})
        return changed
    mutation('wrong_tx_sampled_bit','reference/write_one',wrong_tx_bit)
    mutation('wrong_rx_byte','reference/read_one',lambda rs:set_one(rs,lambda r:r['pre']['rx_valid'],'pre','rx_data',lambda x:x^(1<<24)))
    mutation('wrong_partial_padding','reference/read_partial_three',lambda rs:set_one(rs,lambda r:r['pre']['rx_valid'],'pre','rx_data',lambda x:x^1))
    def drop_rx(rs):
        changed=[]
        for r in rs:
            for side in ('pre','post'):
                if r[side]['rx_valid']:changed.append({'cycle':r['cycle'],'side':side,'field':'rx_valid','before':1,'after':0});r[side]['rx_valid']=0
        return changed
    mutation('missing_rx_word','reference/read_one',drop_rx)
    def duplicate(rs):
        i=next(r['cycle'] for r in rs if r['pre']['rx_valid']);rs[i]['post'].update(rx_valid=1);rs[i+1]['pre'].update(rx_valid=1,rx_data=rs[i]['pre']['rx_data'])
        return [{'cycle':i+1,'fault':'Repeated already-consumed RX word at next pre handshake'}]
    mutation('duplicate_rx_word','reference/read_one',duplicate)
    mutation('multiple_chip_selects','reference/write_one',lambda rs:set_one(rs,lambda r:r['post']['csb']==2,'post','csb',lambda x:0))
    def short(rs):
        i=[r['cycle'] for r in rs if r['pre']['sck']==0 and r['post']['sck']==1][3]+1
        for r in rs[i+1:]:
            for side in ('pre','post'):r[side].update(csb=3,sck=0,active=0,sd_en=0)
        return [{'cycle':i+1,'fault':'Deselect after only four payload bits, remain idle'}]
    mutation('premature_deselect','reference/write_one',short)
    mutation('clock_during_tx_stall','calibration/tx_starvation_resume',lambda rs:set_one(rs,lambda r:r['pre']['tx_stall'],'post','sck',lambda x:1-x))
    mutation('select_during_rx_stall','calibration/rx_backpressure_resume',lambda rs:set_one(rs,lambda r:r['pre']['rx_stall'],'post','csb',lambda x:3))
    mutation('wrong_reset_select','calibration/software_reset_restart',lambda rs:set_one(rs,lambda r:r['action']['sw_reset'],'post','csb',lambda x:0))
    mutation('wrong_recovered_rx_word','calibration/rx_backpressure_resume',lambda rs:set_one(rs,lambda r:r['pre']['rx_valid'] and r['action']['rx_ready'],'pre','rx_data',lambda x:x^0x1000000))
    # Completion false positives are checked independently of defect detection.
    for name,field in [('tx_starvation_resume','tx_stall'),('rx_backpressure_resume','rx_stall')]:
        base='calibration/'+name;rs=inputs[base];cut=next(r['cycle']+1 for r in rs if r['pre'][field]);key='truncated/'+name;inputs[key]=copy.deepcopy(rs[:cut]);controls.append({'name':key,'kind':'incomplete','expected':'No successful recovery event','baseline':base,'cutoff':cut})
    for name,cut in [('partial_then_csid_switch',91),('software_reset_restart',53)]:
        base='calibration/'+name;key='truncated/'+name;inputs[key]=copy.deepcopy(inputs[base][:cut]);controls.append({'name':key,'kind':'incomplete','expected':'No completed switch/restart event','baseline':base,'cutoff':cut})
    rs=copy.deepcopy(inputs['calibration/partial_then_csid_switch']);pending=next(r for r in rs if r['action']['valid'] and not r['pre']['ready']);rs[pending['cycle']+1]['action']['valid']=0
    inputs['invalid_input/drop_pending_command']=rs;controls.append({'name':'invalid_input/drop_pending_command','kind':'input_protocol','expected':'assumption violation; not credited as a DUT defect'})
    (out/'inputs.json').write_text(json.dumps(inputs,separators=(',',':'))+'\n')
    (out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_before_checker_inspection','author_role':'GPT independent test inputs only; no checker edits','script_sha256':sha(Path(__file__)),'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'cases':len(inputs),'no_new_simulations':True,'not_model_prompt':True},indent=2)+'\n')
    print('Prepared',len(inputs),'private controls/calibration cases')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--calibration',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();prepare(a.calibration.resolve(),a.output.resolve())
