"""Offer-per-cycle transport and independent queue oracle, NOT a DUT checker."""
import copy
from collections import deque
from spi_core_interface import FIELDS as PIN_FIELDS, OUTPUTS, action as pin_action, seed as pin_seed, parse as pin_parse

RENAMES={'valid':'cmd_offer','tx_valid':'tx_offer'}
FIELDS={RENAMES.get(k,k):w for k,w in PIN_FIELDS.items()}
CMD=('csid','speed','write','read','length','keep_cs','clkdiv','idle','lead','trail','full_cycle','cpha','cpol')
TX=('tx_data','tx_be')
STATE=('cycle','cmd_offer_id','tx_offer_id','cmd_accept_id','tx_accept_id','cmd_pending','tx_pending',
       'cmd_offered','tx_offered','cmd_accepted','tx_accepted','cmd_cancelled','tx_cancelled')

def action(**kw):
    if set(kw)-set(FIELDS):raise ValueError('Unknown offer field')
    return {**{RENAMES.get(k,k):v for k,v in pin_action().items()},**kw}

def seed():return [{RENAMES.get(k,k):v for k,v in a.items()} for a in pin_seed()]

def schema(limit=64):
    props={k:{'type':'integer','minimum':0,'maximum':2 if k=='speed' else (1<<w)-1} for k,w in FIELDS.items()}
    props['enable']['enum']=[1];props['sw_reset']['enum']=[0]
    return {'type':'object','additionalProperties':False,'required':['actions'],'properties':{
        'actions':{'type':'array','minItems':1,'maxItems':limit,'items':{'type':'object',
        'additionalProperties':False,'required':list(FIELDS),'properties':props}}}}

def validate(payload,limit,initial=False):
    if not isinstance(payload,dict) or set(payload)!={'actions'}:raise ValueError('Expected actions only')
    aa=payload['actions']
    if not isinstance(aa,list) or not 1<=len(aa)<=limit:raise ValueError('Cycle budget')
    for i,a in enumerate(aa):
        if not isinstance(a,dict) or set(a)!=set(FIELDS):raise ValueError('Exact offer fields required')
        if any(type(a[k]) is not int or not 0<=a[k]<(1<<w) for k,w in FIELDS.items()):raise ValueError('Width/type')
        if (not initial or i>=8) and (a['enable']!=1 or a['sw_reset']!=0):raise ValueError('Limited profile enable=1/sw_reset=0')
        if a['speed']==3 or (a['speed'] and a['read'] and a['write']):raise ValueError('Illegal speed/direction')
        if a['cmd_offer'] and not(a['read'] or a['write']):raise ValueError('Dummy unsupported')
        if not a['rst_n'] and (a['cmd_offer'] or a['tx_offer']):raise ValueError('Offer during reset')
    if initial and aa[:8]!=seed():raise ValueError('Original eight-cycle seed required')
    return aa

class TransportOracle:
    """Specification of delivery only. Reads public ready, never expected DUT data."""
    def __init__(self):
        self.cmd=deque();self.tx=deque();self.cmd_payload=dict.fromkeys(CMD,0);self.tx_payload=dict.fromkeys(TX,0)
        self.total=dict.fromkeys(('cmd_offered','tx_offered','cmd_accepted','tx_accepted','cmd_cancelled','tx_cancelled'),0)
        self.cycle=0

    def drive(self,a):
        ci=ti=-1
        if not a['rst_n']:
            self.total['cmd_cancelled']+=len(self.cmd);self.total['tx_cancelled']+=len(self.tx)
            self.cmd.clear();self.tx.clear();self.cmd_payload=dict.fromkeys(CMD,0);self.tx_payload=dict.fromkeys(TX,0)
        else:
            if a['cmd_offer']:
                ci=self.cycle;self.cmd.append((ci,{k:a[k] for k in CMD}));self.total['cmd_offered']+=1
            if a['tx_offer']:
                ti=self.cycle;self.tx.append((ti,{k:a[k] for k in TX}));self.total['tx_offered']+=1
        if self.cmd:self.cmd_payload=self.cmd[0][1].copy()
        if self.tx:self.tx_payload=self.tx[0][1].copy()
        pins={k:a[k] for k in ('rst_n','enable','sw_reset','rx_ready','sd')}
        pins.update(self.cmd_payload);pins.update(self.tx_payload)
        pins.update(valid=int(bool(self.cmd)),tx_valid=int(bool(self.tx)))
        self.added=(ci,ti)
        return pins

    def advance(self,pre):
        ca=ta=-1
        if self.cmd and pre['ready']:
            ca=self.cmd.popleft()[0];self.total['cmd_accepted']+=1
        if self.tx and pre['tx_ready']:
            ta=self.tx.popleft()[0];self.total['tx_accepted']+=1
        state={'cycle':self.cycle,'cmd_offer_id':self.added[0],'tx_offer_id':self.added[1],
               'cmd_accept_id':ca,'tx_accept_id':ta,'cmd_pending':len(self.cmd),'tx_pending':len(self.tx),**self.total}
        for prefix in ('cmd','tx'):
            if state[prefix+'_offered']!=sum(state[prefix+'_'+k] for k in ('accepted','cancelled','pending')):
                raise ValueError('Transport conservation')
        self.cycle+=1
        return state

def parse(log,requests):
    actual=[];states=[]
    for line in log.splitlines():
        if line.startswith('TRACE '):
            values=list(map(int,line.split()[1:]));actual.append(dict(zip(PIN_FIELDS,values[1:1+len(PIN_FIELDS)])))
        if line.startswith('QUEUE '):
            values=list(map(int,line.split()[1:]))
            if len(values)!=len(STATE):raise ValueError('Malformed queue ledger')
            states.append(dict(zip(STATE,values)))
    rows=pin_parse(log,actual)
    validate({'actions':requests},392,initial=True)
    if len(rows)!=len(requests) or len(states)!=len(rows):raise ValueError('One action must equal one actual cycle')
    oracle=TransportOracle()
    for a,r,state in zip(requests,rows,states):
        expected=oracle.drive(a)
        if expected!=r['action']:raise ValueError(f'Incorrect driven transport at cycle {r["cycle"]}')
        if oracle.advance(r['pre'])!=state:raise ValueError(f'Incorrect acceptance/conservation at cycle {r["cycle"]}')
    return rows,states

def request_ids(states):
    """Recover explicit pending/cancelled IDs from the checked queue journal."""
    out={}
    for prefix in ('cmd','tx'):
        pending=deque();cancelled=[];accepted=[];last_cancelled=0
        for s in states:
            delta=s[prefix+'_cancelled']-last_cancelled
            if delta:
                if delta!=len(pending):raise ValueError('Partial/unknown reset cancellation')
                cancelled.extend(pending);pending.clear()
            last_cancelled=s[prefix+'_cancelled']
            if s[prefix+'_offer_id']!=-1:pending.append(s[prefix+'_offer_id'])
            if s[prefix+'_accept_id']!=-1:
                if not pending or pending.popleft()!=s[prefix+'_accept_id']:raise ValueError('Duplicate/out-of-order accept ID')
                accepted.append(s[prefix+'_accept_id'])
            if len(pending)!=s[prefix+'_pending']:raise ValueError('Pending ID/count mismatch')
        out.update({prefix+'_pending_ids':list(pending),prefix+'_cancelled_ids':cancelled,prefix+'_accepted_ids':accepted})
    return out

def offers_from_legal_trace(rows):
    """PRIVATE calibration conversion, never an experimental output repair.

    Only the first cycle of each valid offer is submitted; a held offer is not
    copied into several transactions. Uses recorded acceptance for conversion.
    """
    out=[];cmd_pending=tx_pending=False
    for r in rows:
        a=r['action'];n={RENAMES.get(k,k):v for k,v in a.items()}
        if not a['rst_n']:cmd_pending=tx_pending=False
        n['cmd_offer']=int(bool(a['valid']) and not cmd_pending)
        n['tx_offer']=int(bool(a['tx_valid']) and not tx_pending)
        cmd_pending=bool(a['valid'] and not r['pre']['ready'])
        tx_pending=bool(a['tx_valid'] and not r['pre']['tx_ready'])
        out.append(n)
    validate({'actions':out},392,initial=True)
    return out
