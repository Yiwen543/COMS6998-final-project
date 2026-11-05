"""Public-pin cycle interface for the original SPI core; contains no checker."""
FIELDS = {'rst_n':1,'enable':1,'sw_reset':1,'valid':1,'csid':1,'speed':2,
          'write':1,'read':1,'length':20,'keep_cs':1,'clkdiv':16,'idle':4,
          'lead':4,'trail':4,'full_cycle':1,'cpha':1,'cpol':1,
          'tx_data':32,'tx_be':4,'tx_valid':1,'rx_ready':1,'sd':4}
OUTPUTS = ('ready','tx_ready','tx_full','rx_data','rx_valid','sck','csb',
           'sd','sd_en','rx_stall','tx_stall','active')

def action(**changes):
    if set(changes)-set(FIELDS):raise ValueError('Unknown field')
    return {**dict.fromkeys(FIELDS,0),'rst_n':1,'enable':1,'rx_ready':1,**changes}

def seed():
    return [{**dict.fromkeys(FIELDS,0),'rst_n':int(i>=2)} for i in range(8)]

def schema(limit=64):
    return {'type':'object','additionalProperties':False,'required':['actions'],
        'properties':{'actions':{'type':'array','minItems':1,'maxItems':limit,
        'items':{'type':'object','additionalProperties':False,'required':list(FIELDS),
        'properties':{k:{'type':'integer','minimum':0,'maximum':2 if k=='speed' else (1<<w)-1} for k,w in FIELDS.items()}}}}}

def validate(payload,limit,initial=False):
    if not isinstance(payload,dict) or set(payload)!={'actions'}:raise ValueError('Expected actions only')
    aa=payload['actions']
    if not isinstance(aa,list) or not 1<=len(aa)<=limit:raise ValueError('Cycle budget')
    for a in aa:
        if not isinstance(a,dict) or set(a)!=set(FIELDS):raise ValueError('Exact fields required')
        if any(type(a[k]) is not int or not 0<=a[k]<(1<<w) for k,w in FIELDS.items()):raise ValueError('Width/type')
        if a['speed']==3 or (a['speed'] and a['read'] and a['write']):raise ValueError('Reserved/illegal speed-direction')
        if (not a['rst_n'] or a['sw_reset']) and (a['valid'] or a['tx_valid']):raise ValueError('Transfer during reset')
    if initial and aa[:8]!=seed():raise ValueError('Shared registered seed required')
    return aa

def parse(log,actions):
    rows=[]
    for line in log.splitlines():
        if not line.startswith('TRACE '):continue
        v=list(map(int,line.split()[1:]));i=1+len(FIELDS)
        if len(v)!=i+2*len(OUTPUTS):raise ValueError('Malformed trace')
        rows.append({'cycle':v[0],'action':dict(zip(FIELDS,v[1:i])),
                     'pre':dict(zip(OUTPUTS,v[i:i+len(OUTPUTS)])),
                     'post':dict(zip(OUTPUTS,v[i+len(OUTPUTS):]))})
    if len(rows)!=len(actions) or any(r['cycle']!=i or r['action']!=actions[i] for i,r in enumerate(rows)):raise ValueError('Trace input/order mismatch')
    return rows
