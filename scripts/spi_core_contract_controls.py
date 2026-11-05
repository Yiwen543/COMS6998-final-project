"""Private contract-v2 controls: hand traces and actual fixed-driver probes.

This file authors stimuli/control traces only, never the Claude checker. The
historical MSB controls are retained in their original directory, not relabelled.
"""
import argparse
import copy
import json
from pathlib import Path
import probe_spi_core_events as runner
from spi_core_interface import action, seed, OUTPUTS, validate
from run_midterm_fixed import ROOT, sha

BASE=ROOT/'results/real_parent_screen_20261104'


def reference(payload, read=False, lanes=None):
    """Public mode-0 contract; chosen lanes correspond to enabled TX byte lanes."""
    if not 1<=len(payload)<=4:raise ValueError('One word only')
    lanes=list(range(len(payload))) if lanes is None else lanes
    if len(lanes)!=len(payload) or lanes!=sorted(set(lanes)) or any(i not in range(4) for i in lanes):raise ValueError('TX lane ordering')
    if read and lanes!=list(range(len(payload))):raise ValueError('RX fills contiguous low lanes')
    word=sum(b<<(8*i) for i,b in zip(lanes,payload));be=sum(1<<i for i in lanes)
    rows=[];state={**dict.fromkeys(OUTPUTS,0),'csb':3,'tx_ready':1}
    def emit(a=None,**changes):
        nonlocal state
        a=action() if a is None else a;pre=dict(state)
        pre['ready']=int(bool(a['enable'] and a['rst_n'] and not state['active']))
        post={**pre,**changes};rows.append({'cycle':len(rows),'action':a,'pre':pre,'post':post});state=post
    for a in seed():emit(a)
    emit(action(tx_data=word,tx_be=be,tx_valid=int(not read)),tx_full=int(not read));emit()
    bits=[(b>>i)&1 for b in payload for i in reversed(range(8))]
    emit(action(valid=1,read=int(read),write=int(not read),length=len(payload)-1),csb=2,active=1,ready=0,sd=bits[0] if not read else 0,sd_en=1,tx_full=0)
    emit(action(sd=bits[0]<<1 if read else 0))
    for i,bit in enumerate(bits):
        emit(action(sd=bit<<1 if read else 0),sck=1)
        nxt=bits[i+1] if i+1<len(bits) else bit
        emit(action(sd=bit<<1 if read else 0),sck=0,sd=nxt if not read else 0)
    if read:
        emit(action(sd=bits[-1]<<1),rx_valid=1,rx_data=word)
        emit(action(sd=bits[-1]<<1),rx_valid=0)
    else:emit()
    emit(csb=3,active=0,sd_en=0,ready=1)
    for _ in range(3):emit()
    validate({'actions':[r['action'] for r in rows]},392,initial=True)
    return rows


def probes():
    out={}
    for speed in (0,1,2):
        for mode in (0,1,2,3):
            aa=seed()+[action() for _ in range(176)]
            aa[8].update(tx_data=0xa1b2c3d4,tx_be=15,tx_valid=1)
            aa[10].update(valid=1,write=1,length=3,speed=speed,cpol=mode>>1,cpha=mode&1,clkdiv=1,lead=1,trail=1)
            out['write_speed%d_mode%d'%(speed,mode)]=aa
    # Use an earlier public SCK schedule ONLY to place external RX stimulus.
    # No observed data are used as golden results; timing is checked after rerun.
    basis=BASE/'spi_core_events-v3/ordinary_fullcycle_read'
    rows=json.loads((basis/'trace.json').read_text())
    edges=[r['cycle'] for r in rows if r['pre']['sck']==0 and r['post']['sck']==1 and r['post']['csb']==2]
    bits=[(b>>i)&1 for b in (0xa5,0x5a,0x3c) for i in reversed(range(8))]
    if len(edges)!=len(bits):raise ValueError('RX scheduling template changed')
    for full in (0,1):
        aa=copy.deepcopy(json.loads((basis/'actions.json').read_text())['actions'])
        for a in aa[8:]:a['sd']=0
        aa[8]['full_cycle']=full
        for c,b in zip(edges,bits):
            for k in (c,c+1):aa[k]['sd']=b<<1
        out['read_asymmetric_full%d'%full]=aa
    return out


def prepare(out, simulation=None):
    out.mkdir(parents=True,exist_ok=False);data={};controls=[]
    def add(name,rows,kind,**kw):
        data[name]=rows;controls.append({'name':name,'kind':kind,**kw})
    payload=[0xa5,0x5a,0x3c,0xc3]
    for n in (1,2,3,4):
        for rd in (False,True):
            add('reference/'+('read' if rd else 'write')+str(n),reference(payload[:n],rd),'independent_positive',
                expected='Scoped pass under registered LSB contract; asymmetric bytes and high padding',authority='contract-repair-v2/authority/contract.json')
    add('reference/write_sparse',reference([0xd4,0xb2],False,[0,2]),'independent_positive',expected='Only enabled lanes0,2 in increasing index')
    # Existing calibration is observational evidence, not a golden model.
    for f in sorted((BASE/'spi_core_events-v3').iterdir()):
        if (f/'trace.json').exists():add('calibration/'+f.name,json.loads((f/'trace.json').read_text()),'observational_positive',expected='Report all failures/unresolved; do not presume correct')
    extra=BASE/'spi-checker-postreview-v1/controls-v2'
    dd=json.loads((extra/'inputs.json').read_text())
    for meta in json.loads((extra/'controls.json').read_text()):
        m=copy.deepcopy(meta);name='followup/'+m.pop('name');kind=m.pop('kind')
        if 'baseline'in m:m['baseline']='followup/'+m['baseline']
        add(name,dd[meta['name']],kind,**m)
    if simulation:
        for name in probes():add('probe/'+name,json.loads((simulation/name/'trace.json').read_text()),'observational_positive',expected='Public timing/mode/payload control; report, never assume DUT correctness')
    def mut(name,base,fn,expected):
        rows=copy.deepcopy(data[base]);fn(rows)
        if rows==data[base]:raise ValueError('No-op mutation')
        add('negative/'+name,rows,'single_fault',baseline=base,expected=expected)
    def word_mut(rows,fn):
        for r in rows:
            for side in ('pre','post'):
                if r[side]['rx_valid']:r[side]['rx_data']=fn(r[side]['rx_data'])
    mut('reversed_rx_lanes','reference/read3',lambda rs:word_mut(rs,lambda w:int.from_bytes(w.to_bytes(4,'little'),'big')),'rx_payload/rx_padding failure; old contradictory ordering is not accepted')
    mut('high_padding_nonzero','reference/read3',lambda rs:word_mut(rs,lambda w:w|0x01000000),'rx_padding failure')
    mut('wrong_low_rx_byte','reference/read3',lambda rs:word_mut(rs,lambda w:w^1),'rx_payload failure')
    def wrong_tx(rows):
        i=next(r['cycle'] for r in rows if r['pre']['sck']==0 and r['post']['sck']==1)
        for j,side in ((i-1,'post'),(i,'pre'),(i,'post')):rows[j][side]['sd']^=1
    mut('wrong_tx_bit','reference/write3',wrong_tx,'tx_payload failure at sampling; wrong value stable across edge')
    def miss_word(rows):
        for r in rows:
            for side in ('pre','post'):r[side]['rx_valid']=0
    mut('missing_rx_word','reference/read3',miss_word,'inconclusive pending, not pass; no invented timeout')
    def bad_cs(rows):
        next(r for r in rows if r['post']['csb']==2)['post']['csb']=0
    mut('multiple_selects','reference/write3',bad_cs,'CS failure')
    for family,flag in [('tx_starvation_resume','tx_stall'),('rx_backpressure_resume','rx_stall')]:
        base='calibration/'+family;cut=next(r['cycle']+1 for r in data[base] if r['pre'][flag])
        add('truncated/'+family,copy.deepcopy(data[base][:cut]),'incomplete',baseline=base,expected='Explicit pending/failed event, no successful recovery',required_event_family=family)
        if family.startswith('tx'):
            mut('dirty_tx_recovery',base,wrong_tx,'Payload error before starvation must prevent success for transaction-wide recovery')
        else:mut('dirty_rx_recovery',base,lambda rs:word_mut(rs,lambda w:w^1),'RX mismatch prevents recovery success')
    # Output corruption inside an actual stalled interval, no change of inputs.
    def stall_clock(rs):
        r=next(r for r in rs if r['pre']['tx_stall']);r['post']['sck']^=1
    mut('clock_during_tx_stall','calibration/tx_starvation_resume',stall_clock,'Detect SCK change with no TX data; never success')
    # All new controls remain outside LLM stimulus/author prompts.
    for n,rows in data.items():
        if not rows or any(r['cycle']!=i for i,r in enumerate(rows)):raise ValueError('Non-contiguous control '+n)
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    (out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_without_new_checker_access','script_sha256':sha(Path(__file__)),
        'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'cases':len(data),
        'contract_sha256':sha(BASE/'contract-repair-v2/authority/contract.json'),
        'new_model_calls':0,'no_checker_edits':True,'historical_MSB_controls':'retained separately, not overwritten',
        'simulation':str(simulation) if simulation else None},indent=2)+'\n')
    print(json.dumps({'cases':len(data),'independent_positives':9,'private':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--simulation',type=Path);p.add_argument('--run-probes',action='store_true')
    a=p.parse_args()
    if a.run_probes:
        if not a.simulation:raise ValueError('--simulation required')
        runner.cases=probes
        runner.run(a.simulation.resolve(),BASE/'spi_host_core_v2/screen-v2/screen.json')
    prepare(a.output.resolve(),a.simulation.resolve() if a.simulation else None)
