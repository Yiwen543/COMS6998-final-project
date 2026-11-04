"""Fixed write-mode controller environment, schema and trace codec. No oracle."""
import json

FIELDS = {'rst_n':1, 'enable':1, 'push':1, 'byte':8, 'start':1, 'stop':1,
          'nak_ok':1, 'flush':1, 'clear_events':1, 'target_ack':1, 'stretch':1,
          'nak_timeout_enable':1, 'nak_timeout':31}
DEFAULT = dict(rst_n=1, enable=1, push=0, byte=0, start=0, stop=0, nak_ok=0,
               flush=0, clear_events=0, target_ack=1, stretch=0,
               nak_timeout_enable=0, nak_timeout=12)
TIMING = dict(thigh=4, tlow=6, t_r=1, t_f=1, thd_sta=4, tsu_sta=4, tsu_sto=4, thd_dat=2)
OBS = ('scl','sda','scl_i','sda_i','scl_o','sda_o','ready','idle','transmitting',
       'nak','nak_timeout','arbitration','scl_interference','stretch_timeout','sda_unstable',
       'complete','rx_valid','rx_data','valid','depth','fmt_byte','fmt_start','fmt_stop','fmt_nak_ok',
       'unhandled_nak','unhandled_timeout','bus_free','target_low','scl_pin','sda_pin')


def action(**kw):
    return {**DEFAULT, **kw}


def seed():
    return [action(rst_n=0, enable=0) for _ in range(2)]+[action() for _ in range(6)]


def validate_actions(data, limit=392, initial=True):
    if not isinstance(data, dict) or set(data) != {'actions'} or not isinstance(data['actions'], list):
        raise ValueError('Expected only actions array')
    actions = data['actions']
    if not 1 <= len(actions) <= limit:
        raise ValueError('Cycle limit exceeded or empty')
    for a in actions:
        if not isinstance(a, dict) or set(a) != set(FIELDS):
            raise ValueError('Unknown or missing action fields')
        if any(type(a[k]) != int or not 0 <= a[k] < 2**w for k,w in FIELDS.items()):
            raise ValueError('Non-integer or width violation')
        if not a['rst_n'] and a['push']:
            raise ValueError('Cannot enqueue during reset')
        if a['push'] and a['flush']:
            raise ValueError('Separate FIFO flush and enqueue')
    if initial and (len(actions)<2 or any(a['rst_n'] for a in actions[:2])):
        raise ValueError('Two initial reset cycles required')
    return actions


def write_vectors(actions, path):
    path.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in actions))


def parse(actions, log):
    rows=[]
    for line in log.splitlines():
        if not line.startswith('TRACE '): continue
        v=list(map(int,line.split()[1:]))
        if len(v)!=1+2*len(OBS) or v[0]!=len(rows): raise ValueError('Malformed trace')
        rows.append(dict(cycle=v[0],action=actions[v[0]],pre=dict(zip(OBS,v[1:1+len(OBS)])),post=dict(zip(OBS,v[1+len(OBS):]))))
    if len(rows)!=len(actions): raise ValueError('Incomplete trace')
    return rows


def schema(limit=64):
    return {'type':'object','additionalProperties':False,'required':['actions'], 'properties':{
        'actions':{'type':'array','minItems':1,'maxItems':limit,'items':{'type':'object',
        'additionalProperties':False,'required':list(FIELDS),'properties':{
            k:{'type':'integer','minimum':0,'maximum':2**w-1} for k,w in FIELDS.items()}}}}}
