"""Private specification-derived public traces, never read from DUT simulation.

This is a stimulus/control fixture, not a checker. Positive and single-fault
traces exercise independent checker discrimination. No RTL internals are used.
"""
import copy
from i2c_fixture import OBS,action


class WireReference:
    def __init__(self,timeout=False):
        self.rows=[];self.head=None;self.nak=0;self.timeout=0;self.toen=int(timeout)
        self.active=False;self.scl=1;self.sda=1
        for _ in range(2):self.level(1,1,1,act={'rst_n':0,'enable':0})
        self.level(1,1,6)

    def level(self,scl,sda,n=1,*,act=None,obs=None):
        for i in range(n):
            a=action(nak_timeout_enable=self.toen,**(act or {}))
            o={k:0 for k in OBS}
            o.update(scl=scl,sda=sda,scl_i=scl,sda_i=sda,scl_o=scl,sda_o=sda,scl_pin=scl,sda_pin=sda,
                     idle=int(not self.active),bus_free=int(not self.active),
                     unhandled_nak=self.nak,unhandled_timeout=self.timeout)
            if self.head:
                o.update(valid=1,depth=1,fmt_byte=self.head['byte'],fmt_start=self.head['start'],
                         fmt_stop=self.head['stop'],fmt_nak_ok=self.head['nak_ok'])
            o.update(obs or {})
            self.rows.append({'cycle':len(self.rows),'action':a,'pre':dict(o),'post':dict(o)})
        self.scl=scl;self.sda=sda

    def push(self,byte,stop):
        self.head=dict(byte=byte,start=1,stop=stop,nak_ok=0)
        self.level(self.scl,self.sda,act={'push':1,'byte':byte,'start':1,'stop':stop})

    def start(self):
        if self.active:self.level(0,1,5)
        self.level(1,1,5);self.active=True;self.level(1,0,5);self.level(0,0,3)

    def byte(self,value,ack=True,stretch=False):
        for i in range(7,-1,-1):
            bit=(value>>i)&1;self.level(0,bit,6)
            if stretch and i==4:
                self.level(0,bit,12,act={'stretch':1},obs={'scl_pin':1,'scl_o':1})
            self.level(1,bit,5)
        ab=int(not ack)
        self.level(0,ab,6,obs={'target_low':int(ack),'sda_pin':1,'sda_o':1})
        self.level(1,ab,5,obs={'target_low':int(ack),'sda_pin':1,'sda_o':1})
        self.level(0,1,3)
        if not ack:
            self.nak=1;self.level(0,1,obs={'nak':1})
        self.level(0,1,4)

    def pop(self):
        self.level(self.scl,self.sda,obs={'ready':1});self.head=None;self.level(self.scl,self.sda)

    def stop(self):
        self.level(0,0,6);self.level(1,0,5);self.level(1,1,5);self.active=False
        self.level(1,1,4)

    def flush_clear(self):
        self.head=None;self.level(self.scl,self.sda,act={'flush':1})
        self.push(0x52,1)
        self.nak=0;self.timeout=0;self.level(self.scl,self.sda,act={'clear_events':1})


def event_reference(family):
    w=WireReference(timeout=family=='nak_timeout_recovery')
    w.push(0x50,int(family=='stretch_recovery'));w.start()
    w.byte(0x50,ack=family=='stretch_recovery',stretch=family=='stretch_recovery')
    if family=='stretch_recovery':w.stop();w.pop()
    else:
        w.pop();w.level(0,1,20)
        if family=='nak_timeout_recovery':
            w.timeout=1;w.level(0,1,obs={'nak_timeout':1});w.stop();w.level(1,1,8)
        w.flush_clear();w.start();w.byte(0x52);w.stop();w.pop()
    w.level(1,1,8)
    return w.rows


def controls():
    out={}
    for family in ['stretch_recovery','nak_restart','nak_timeout_recovery']:
        out['reference_'+family]=event_reference(family)
    # Preserve the early STOP waveform, remove all timeout status until after it.
    bad=copy.deepcopy(out['reference_nak_timeout_recovery'])
    clear=next(r['cycle'] for r in bad if r['action']['clear_events'])
    for r in bad[:clear]:
        for ph in ['pre','post']:
            r[ph]['nak_timeout']=0;r[ph]['unhandled_timeout']=0
    # A later spurious pulse cannot retrospectively justify the earlier STOP.
    bad[clear+1]['pre']['nak_timeout']=1
    out['premature_timeout_stop']=bad
    missing=copy.deepcopy(out['reference_nak_restart'])
    for r in missing:
        for ph in ['pre','post']:r[ph]['nak']=0;r[ph]['unhandled_nak']=0
    out['missing_nak_status']=missing
    return out
