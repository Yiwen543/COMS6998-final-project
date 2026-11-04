"""Private public-spec trace fixtures, independent of RTL simulation and checker."""
import copy
from i2c_read_fixture import OBS,action


class ReadWire:
    def __init__(self):
        self.rows=[];self.queue=[];self.active=False;self.scl=1;self.sda=1
        self.level(1,1,2,act={'rst_n':0,'enable':0});self.level(1,1,6)

    def level(self,scl,sda,n=1,act=None,obs=None):
        for _ in range(n):
            o={k:0 for k in OBS}
            o.update(scl=scl,sda=sda,scl_i=scl,sda_i=sda,scl_o=scl,sda_o=sda,scl_pin=scl,sda_pin=sda,
                     idle=int(not self.active),bus_free=int(not self.active))
            if self.queue:
                h=self.queue[0];o.update(valid=1,depth=len(self.queue),fmt_byte=h['byte'],fmt_start=h['start'],
                    fmt_stop=h['stop'],fmt_nak_ok=h['nak_ok'],fmt_read=h['read'],fmt_rcont=h['rcont'])
            o.update(obs or {})
            self.rows.append({'cycle':len(self.rows),'action':action(**(act or {})), 'pre':dict(o),'post':dict(o)})
        self.scl=scl;self.sda=sda

    def push(self,**kw):
        cmd=action(push=1,**kw);self.queue.append(cmd)
        self.level(self.scl,self.sda,act=cmd)

    def pop(self):
        self.level(self.scl,self.sda,obs={'ready':1});self.queue.pop(0);self.level(self.scl,self.sda)

    def start(self):
        if self.active:self.level(0,1,4)
        self.level(1,1,5);self.active=True;self.level(1,0,5);self.level(0,0,3)

    def write(self,value):
        for i in range(7,-1,-1):
            b=(value>>i)&1;self.level(0,b,6);self.level(1,b,5)
        self.level(0,0,6,obs={'sda_o':1,'sda_pin':1,'target_low':1})
        self.level(1,0,5,obs={'sda_o':1,'sda_pin':1,'target_low':1});self.level(0,1,5)

    def read(self,value,ack,stretch=False):
        for i in range(7,-1,-1):
            b=(value>>i)&1;extern={'sda_pin':1,'sda_o':1,'target_low':1-b}
            self.level(0,b,6,obs=extern)
            if stretch and i==4:self.level(0,b,12,act={'stretch':1},obs={**extern,'scl_pin':1,'scl_o':1})
            self.level(1,b,5,obs=extern)
        # RX delivery after eight bits, BEFORE controller's ninth ACK slot.
        self.level(0,1,obs={'rx_valid':1,'rx_data':value});self.level(0,1,3)
        self.level(0,int(not ack),3);self.level(1,int(not ack),5);self.level(0,1,5)

    def stop(self):
        self.level(0,0,6);self.level(1,0,5);self.level(1,1,5);self.active=False;self.level(1,1,3)


def reference(kind):
    w=ReadWire();w.push(byte=0x51,start=1)
    w.push(byte=2 if kind=='multi_read' else (0 if kind=='zero_partial' else 1),read=1,
           rcont=int(kind=='rcont_chain'),stop=int(kind in ('ordinary_read','multi_read','read_stretch','zero_partial')))
    if kind=='rcont_chain':w.push(byte=1,read=1,stop=1)
    if kind=='read_restart':w.push(byte=0x50,start=1,stop=1)
    w.start();w.write(0x51);w.pop()
    w.read(0xA6,ack=kind in ('multi_read','rcont_chain','zero_partial'),stretch=kind=='read_stretch')
    if kind=='multi_read':w.read(0x3C,ack=False)
    if kind=='rcont_chain':w.pop();w.read(0x3C,ack=False)
    if kind=='read_restart':w.pop();w.start();w.write(0x50)
    if kind!='zero_partial':w.stop();w.pop();w.level(1,1,8)
    return w.rows


def controls():
    out={name:reference(name) for name in ['ordinary_read','multi_read','rcont_chain','read_restart','read_stretch','zero_partial']}
    bad=copy.deepcopy(out['ordinary_read'])
    r=next(r for r in bad if r['pre']['rx_valid']);r['pre']['rx_data']^=1
    out['rx_corrupt']=bad
    bad=copy.deepcopy(out['ordinary_read'])
    r=next(r for r in bad if r['pre']['rx_valid']);n=r['cycle'];bad[n+1]['pre'].update(rx_valid=1,rx_data=r['pre']['rx_data'])
    out['rx_duplicate']=bad
    bad=copy.deepcopy(out['ordinary_read'])
    for r in bad:r['pre']['rx_valid']=0;r['post']['rx_valid']=0
    out['rx_missing']=bad
    bad=copy.deepcopy(out['rcont_chain'])
    # Same valid wire history, but RCONT command promises NACK at the first boundary.
    for r in bad:
        if r['action']['push'] and r['action']['read'] and r['action']['rcont']:r['action']['rcont']=0
        for phase in ('pre','post'):
            if r[phase]['fmt_read']:r[phase]['fmt_rcont']=0
    out['wrong_boundary_ack']=bad
    bad=copy.deepcopy(out['ordinary_read']);bad[10]['pre']['ready']=1;out['premature_pop']=bad
    out['truncated_read']=copy.deepcopy(out['ordinary_read'][:165])
    return out
