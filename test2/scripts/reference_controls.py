"""Independent hand-specified checker unit controls, not a production oracle.

These finite expected examples are hidden from the reference author. Each output
state is a declared fixture; no executable FIFO reference algorithm is here.
"""
import copy
from common import BASE, dump
from prepare import action

def state(fill, data=-1):
    return dict(fill=fill, full=int(fill==16), empty=int(fill==0), data=data)

def trajectory(actions, states):
    assert len(states)==len(actions)
    return [{'cycle':i,'action':a,'pre':copy.deepcopy(states[i-1]) if i else dict(fill=-1,full=-1,empty=-1,data=-1),
             'post':copy.deepcopy(states[i])} for i,a in enumerate(actions)]

def controls():
    cases={}
    def add(name,rows,verdict): cases[name]={'rows':rows,'expected_verdict':verdict}
    actions=[action(reset=1),action(wr=1,data=11),action(wr=1,data=22),
             action(wr=1,rd=1,data=33),action(rd=1),action(rd=1),
             action(rd=1),action(wr=1,rd=1,data=44),action(reset=1),action()]
    states=[state(0),state(1,11),state(2,11),state(2,22),state(1,33),state(0),state(0),state(1,44),state(0),state(0)]
    order=trajectory(actions,states);add('legal_order_and_reset',order,'PASS')
    actions=[action(reset=1)]+[action(wr=1,data=i) for i in range(1,17)]
    states=[state(0)]+[state(i,1) for i in range(1,17)]
    actions += [action(wr=1,data=99),action(wr=1,rd=1,data=100)] + [action(rd=1) for _ in range(16)]
    states += [state(16,1),state(15,2)] + [state(14-i,3+i) if i<14 else state(0) for i in range(16)]
    # There are fifteen remaining words after the full simultaneous operation.
    full=trajectory(actions,states);add('legal_capacity',full,'PASS')
    actions=[action(reset=1)];states=[state(0)]
    for i in range(40):
        actions += [action(wr=1,data=i+1),action(rd=1)]
        states += [state(1,i+1),state(0)]
    add('legal_multiple_wraps',trajectory(actions,states),'PASS')
    def corrupt(name,original,cycle,phase,key,value,verdict='FAIL'):
        rows=copy.deepcopy(original);rows[cycle][phase][key]=value;add(name,rows,verdict)
    corrupt('wrong_data',order,4,'post','data',11)
    corrupt('wrong_fill',order,2,'post','fill',1)
    corrupt('wrong_full',full,16,'post','full',0)
    corrupt('wrong_empty',order,1,'post','empty',1)
    corrupt('bad_clear',order,8,'post','fill',1)
    corrupt('async_reset_change',order,8,'pre','fill',0)
    corrupt('simultaneous_order',order,3,'post','data',33)
    corrupt('full_simultaneous_count',full,18,'post','fill',16)
    corrupt('unknown_nonempty',order,4,'post','data',-1,'UNRESOLVED')
    rows=copy.deepcopy(order);rows[2]['post']['fill']=1;rows[4]['post']['data']=-1
    add('failure_then_unknown',rows,'FAIL')
    rows=copy.deepcopy(order);rows[1]['post']['data']=-1;rows[4]['post']['fill']=2
    add('unknown_then_failure',rows,'FAIL')
    rows=copy.deepcopy(order);rows[0]['action']['reset']=0;add('missing_initial_reset',rows,'INVALID_INPUT')
    rows=copy.deepcopy(order);rows[0]['action']['wr']=1;add('illegal_reset_write',rows,'INVALID_INPUT')
    rows=copy.deepcopy(order);rows[1]['action']['data']=256;add('bad_width',rows,'INVALID_INPUT')
    rows=copy.deepcopy(order);rows[1]['action']['wr']=True;add('boolean_not_integer',rows,'INVALID_INPUT')
    rows=copy.deepcopy(order);rows[1]['cycle']=3;add('wrong_cycle_order',rows,'INVALID_INPUT')
    add('empty_trace',[],'INVALID_INPUT')
    return cases

if __name__=='__main__':
    path=BASE/'private/reference-controls-v1.json'
    if path.exists(): raise SystemExit('Already registered')
    dump(path,controls())
    print('registered',len(controls()),'independent finite checker controls')
