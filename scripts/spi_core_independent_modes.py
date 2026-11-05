"""Independent public-SPI hand controls; no RTL or checker imports."""
import argparse
import copy
import json
from pathlib import Path
from spi_core_interface import action, seed, OUTPUTS, validate
from run_midterm_fixed import sha


def hand(mode=0, speed=0, read=False, full=0, starve=False):
    if read and (mode&1 or speed):raise ValueError('RX controls scoped to CPHA0 Standard')
    if starve and (mode or speed or read):raise ValueError('Starvation control scoped to mode0 Standard TX')
    payload=[0xa5,0x5a,0x3c,0xc3,0x96,0x69,0xf0,0x0f] if starve else [0xa5,0x5a,0x3c]
    width=1<<speed;mask=(1<<width)-1;pol=mode>>1;phase=mode&1;half=2
    rows=[];state={**dict.fromkeys(OUTPUTS,0),'csb':3,'tx_ready':1};sdin=0
    def emit(a=None,**changes):
        nonlocal state
        a=action(sd=sdin) if a is None else a;pre=dict(state)
        pre['ready']=int(bool(a['enable'] and a['rst_n'] and not state['active']))
        post={**pre,**changes};rows.append({'cycle':len(rows),'action':a,'pre':pre,'post':post});state=post
    for a in seed():emit(a)
    first=payload[:4];word=sum(b<<(8*i) for i,b in enumerate(first))
    emit(action(tx_valid=int(not read),tx_data=word,tx_be=(1<<len(first))-1),tx_full=int(not read));emit()
    emit(action(valid=1,write=int(not read),read=int(read),length=len(payload)-1,cpol=pol,cpha=phase,speed=speed,clkdiv=1,lead=1,trail=1,full_cycle=full),active=1,sck=pol,csb=3,ready=0)
    emit();emit(csb=2,sd_en=1 if read else mask,tx_full=0)
    for _ in range(4):emit()
    beats=[(b>>i)&mask for b in payload for i in range(8-width,-1,-width)]
    for i,b in enumerate(beats):
        sdin=(b<<1) if read else 0
        if not phase:
            emit(sd=0 if read else b)
            emit(sck=1-pol)
            if starve and i==31:
                emit(tx_stall=1)
                for _ in range(12):emit()
                second=sum(b<<(8*j) for j,b in enumerate(payload[4:]))
                emit(action(tx_data=second,tx_be=15,tx_valid=1),tx_stall=0)
            else:emit()
            emit(sck=pol)
        else:
            emit(sck=1-pol,sd=b);emit();emit(sck=pol);emit()
    for _ in range(4):emit()
    if read:
        emit(rx_valid=1,rx_data=word);emit(rx_valid=0)
    emit(csb=3,active=0,sd_en=0)
    for _ in range(4):emit()
    validate({'actions':[r['action'] for r in rows]},392,initial=True)
    return rows


def prepare(prior,out):
    out.mkdir(parents=True,exist_ok=False)
    data=json.loads((prior/'inputs.json').read_text());controls=json.loads((prior/'controls.json').read_text())
    def add(name,rows,kind,**kw):data[name]=rows;controls.append({'name':name,'kind':kind,**kw})
    for mode in range(4):
        for speed in range(3):add('hand/write_mode%d_speed%d'%(mode,speed),hand(mode,speed),'independent_positive',expected='Public SPI mode/width, nonzero divider/lead/trail; all-CS-high CPOL setup is not payload')
    for mode in (0,2):
        for full in (0,1):add('hand/read_mode%d_full%d'%(mode,full),hand(mode,read=True,full=full),'independent_positive',expected='Nonuniform RX, stable sample window, high-lane padding')
    rs=hand(starve=True);name='hand/tx_starvation'
    add(name,rs,'independent_positive',expected='Complete correct recovery; new TX word accepted before postponed trailing edge',required_event_family='tx_starvation_resume')
    c=next(r['cycle'] for r in rs if r['pre']['tx_stall'])
    add('hand/truncated_starvation',copy.deepcopy(rs[:c+1]),'incomplete',baseline=name,expected='Explicit pending starvation event',required_event_family='tx_starvation_resume')
    bad=copy.deepcopy(rs)
    # Corrupt a sampled payload bit AFTER starvation resolves, while keeping it
    # stable on both sides of the edge. This lies within any valid event window.
    i=next(r['cycle'] for r in rs if r['cycle']>c+15 and r['pre']['sck']==0 and r['post']['sck']==1)
    for j,side in ((i-1,'post'),(i,'pre'),(i,'post')):bad[j][side]['sd']^=1
    add('hand/dirty_starvation',bad,'single_fault',baseline=name,expected='Payload failure prevents successful recovery',required_event_family='tx_starvation_resume')
    base='hand/write_mode2_speed0';bad=copy.deepcopy(data[base])
    i=next(r['cycle'] for r in bad if r['pre']['csb']==2 and r['pre']['sck']==1 and r['post']['sck']==0)
    for j,side in ((i-1,'post'),(i,'pre'),(i,'post')):bad[j][side]['sd']^=1
    add('hand/wrong_cpol1_payload',bad,'single_fault',baseline=base,expected='Real selected sample mismatch; idle-polarity filtering must not suppress payload checks')
    for m in controls:
        if m['name']=='calibration/tx_starvation_resume':m['required_event_family']='tx_starvation_resume'
    (out/'inputs.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_before_v3_checker','script_sha256':sha(Path(__file__)),'prior_inputs_sha256':sha(prior/'inputs.json'),
        'inputs_sha256':sha(out/'inputs.json'),'controls_sha256':sha(out/'controls.json'),'cases':len(data),'no_new_simulations':True,'no_checker_edits':True},indent=2)+'\n')
    print(json.dumps({'cases':len(data),'new_independent_positives':17,'new_model_calls':0}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prior',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();prepare(a.prior.resolve(),a.output.resolve())
