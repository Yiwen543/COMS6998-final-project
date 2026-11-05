"""Negative-only ordinary-input screen. No expected DUT output or LLM calls.

A source counter observed under simple legal inputs is ineligible for the
registered event-only target. No functional correctness or positive multistep
qualification can be obtained here; those require the independent checker.
"""
import argparse
import json
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha,invoke
from screen_multistep_events import configuration,SCOPE
from probe_write_scopes import verify
from inventory_natural_coverage import load_all
from probe_spi_core_events import identity
from coverage import summary

FIELDS={'rst':1,'offer':1,'data':8,'last':1,'user':1,'data_ready':1,'header_ready':1}

def action(**kw):return dict({'rst':0,'offer':0,'data':0,'last':0,'user':0,'data_ready':1,'header_ready':1},**kw)

def cases():
    # Public length boundaries registered before this probe. Neither target
    # identities nor source predicates influence these inputs.
    seed=[action(rst=1),action(rst=1)]+[action() for _ in range(6)]
    return {f'length_{n}':seed+[action(offer=1,data=(17*i+3)%256,last=int(i==n-1)) for i in range(n)]+[action() for _ in range(48)]
            for n in (1,2,4,8,16,20)}

def validate(actions):
    if not 8<=len(actions)<=392:raise ValueError('Physical cycle budget')
    for a in actions:
        if set(a)!=set(FIELDS):raise ValueError('Unknown/missing input')
        if any(type(a[k]) is not int or not 0<=a[k]<1<<w for k,w in FIELDS.items()):raise ValueError('Input width/type')
    if actions[:8]!=[action(rst=1),action(rst=1)]+[action() for _ in range(6)]:raise ValueError('Shared seed mismatch')

def driver(ports,c):
    names=list(ports);ins=[n for n in names if ports[n]['direction']=='input' and n!='clk'];outs=[n for n in names if ports[n]['direction']=='output']
    if any(p['direction'] not in ('input','output') for p in ports.values()):raise ValueError('Unexpected direction')
    decl=['logic '+(f'[{len(p["bits"])-1}:0] ' if len(p['bits'])>1 else '')+n+';' for n,p in ports.items()]
    params=','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())
    def display(phase,fields):return '$display("'+phase+' %0d'+(' %0d'*len(fields))+'", cycle,'+','.join(fields)+');'
    s='''`timescale 1ns/1ps
module tb_frame_ordinary;
'''+ '\n'.join(decl)+f'\n{c["top"]} #({params}) dut(.*);\n'+'''
integer fd,nread,cycle,head,tail,accepted,pre_accept;
integer r_rst,r_offer,r_data,r_last,r_user,r_dr,r_hr;
reg [7:0] data_q[0:391]; reg last_q[0:391];reg user_q[0:391];
string vectors;
initial begin
'''+ '\n'.join(n+'=0;' for n in names if ports[n]['direction']=='input')+'''
cycle=0;head=0;tail=0;accepted=0;
length_min=4;length_max=16;s_axis_tkeep=0;
if (!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"missing vectors");
fd=$fopen(vectors,"r"); if (!fd) $fatal(1,"cannot open vectors");
while (!$feof(fd)) begin
 nread=$fscanf(fd,"%d %d %d %d %d %d %d",r_rst,r_offer,r_data,r_last,r_user,r_dr,r_hr);
 if(nread==7) begin
  if(cycle>=392) $fatal(1,"cycle limit");
  rst=r_rst;m_axis_tready=r_dr;m_axis_hdr_ready=r_hr;
  s_axis_tkeep=(cycle>=8);
  if(rst) begin head=0;tail=0;end
  else if(r_offer) begin
   if(tail>=392) $fatal(1,"queue overflow");
   data_q[tail]=r_data;last_q[tail]=r_last;user_q[tail]=r_user;tail=tail+1;
  end
  s_axis_tvalid=(!rst && head<tail);
  s_axis_tdata=s_axis_tvalid?data_q[head]:0;
  s_axis_tlast=s_axis_tvalid?last_q[head]:0;
  s_axis_tuser=s_axis_tvalid?user_q[head]:0;
  #4;
  pre_accept=(!rst && s_axis_tvalid && s_axis_tready);
'''+display('PRE',ins+outs)+'''
  #1;clk=1;#4;
'''+display('POST',outs)+'''
  #1;clk=0;
  if(pre_accept) begin head=head+1;accepted=accepted+1;end
  $display("QUEUE %0d %0d %0d %0d",cycle,head,tail,accepted);
  cycle=cycle+1;
 end else if(!$feof(fd)) $fatal(1,"bad vector");
end
$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
'''
    return s,ins,outs

def parse(log,actions,ins,outs):
    records={};queue={}
    def integer(s):return None if any(c in s.lower() for c in 'xz') else int(s)
    for line in log.splitlines():
        xs=line.split()
        if not xs or xs[0] not in ('PRE','POST','QUEUE'):continue
        kind=xs[0];cycle=int(xs[1]);vals=[integer(s) for s in xs[2:]]
        if kind=='QUEUE':queue[cycle]=vals;continue
        fields=ins+outs if kind=='PRE' else outs
        if len(vals)!=len(fields):raise ValueError('Trace width')
        records.setdefault(cycle,{})[kind]=dict(zip(fields,vals))
    if list(records)!=list(range(len(actions))) or list(queue)!=list(records):raise ValueError('Incomplete trace')
    pending=[];accepted=[];trace=[]
    for i,a in enumerate(actions):
        row=records[i];pre,post=row['PRE'],row['POST']
        if a['rst']:pending=[]
        elif a['offer']:pending.append((i,a['data'],a['last'],a['user']))
        want=pending[0] if pending else (-1,0,0,0)
        expected={'rst':a['rst'],'s_axis_tvalid':int(bool(pending)),'s_axis_tdata':want[1],
                  's_axis_tlast':want[2],'s_axis_tuser':want[3],'s_axis_tkeep':int(i>=8),'s_axis_tid':0,'s_axis_tdest':0,
                  'length_min':4,'length_max':16,'m_axis_tready':a['data_ready'],'m_axis_hdr_ready':a['header_ready']}
        if any(pre[k]!=v for k,v in expected.items()):raise ValueError('Driver transport/input mismatch')
        for phase,values in [('pre',pre),('post',post)]:
            if phase=='pre' and a['rst']:continue
            for k in outs:
                # Stream payload is unspecified when its valid is low. Keep X
                # in saved traces, but never compare it to Verilator's zero.
                enable=('m_axis_hdr_valid' if k.startswith('m_axis_hdr_') else 'm_axis_tvalid')
                if k in ('s_axis_tready','m_axis_tvalid','m_axis_hdr_valid') or values[enable]:
                    if values[k] is None:raise ValueError('Unknown meaningful output')
        if pending and pre['s_axis_tready']:accepted.append(pending.pop(0)[0])
        head,tail,count=queue[i]
        if tail-head!=len(pending) or count!=len(accepted):raise ValueError('Queue ledger mismatch')
        trace.append({'cycle':i,'action':expected,'pre':{k:pre[k] for k in outs},'post':post,'queue':queue[i]})
    if pending:raise ValueError('Incomplete input delivery; cannot use ordinary negative screen')
    if accepted!=[i for i,a in enumerate(actions) if a['offer'] and not a['rst']]:raise ValueError('Lost/reordered input offer')
    return trace,accepted

def run(base,out):
    c=configuration('axis_frame_length_adjust_fifo');verify(c)
    if json.loads((base/'decision.json').read_text())['status']!='static_gate_pass':raise ValueError('Static gate failed')
    ports=json.loads((base/'netlist.json').read_text())['modules'][c['top']]['ports']
    s,ins,outs=driver(ports,c);out.mkdir(parents=True,exist_ok=False);tb=out/'tb_frame_ordinary.sv';tb.write_text(s)
    source=[str(Path(c['root'])/x) for x in c['sources']];builds={};times={}
    for sim in ('verilator','iverilog'):
        folder=out/sim;folder.mkdir()
        binary=folder/('obj/Vtb_frame_ordinary' if sim=='verilator' else 'tb.vvp')
        cmd=(['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_frame_ordinary','--Mdir',folder/'obj','-j','2'] if sim=='verilator' else ['iverilog','-g2012','-s','tb_frame_ordinary','-o',binary])+source+[tb]
        seconds,_=invoke(cmd,folder/'compile.log',timeout=300);builds[sim]=binary;times[sim]={'command':list(map(str,cmd)),'seconds':seconds}
        (folder/'compile.json').write_text(json.dumps(times[sim],indent=2)+'\n')
    screen=json.loads((base/'screen/screen.json').read_text())
    groups=[{**g,'members':[m for m in g['members'] if m['seed_zero_dynamic_candidate'] and m['mapping']['status']=='mapped']}
            for g in screen['groups'] if g['static_candidate_group']]
    if any(len(g['members'])<2 for g in groups):raise ValueError('Static candidate has fewer than two admitted source members')
    seed=json.loads((base/'inventory/raw-points.json').read_text());denom={identity(p) for p in seed}
    result={'status':'negative_only_no_functional_checker','cases':{},'model_calls':0,'checker_called':False,'B_allowed':False,'C_allowed':False,
            'scope_sha256':sha(SCOPE),'script_sha256':sha(Path(__file__)),'driver_sha256':sha(tb),'screen_sha256':sha(base/'screen/screen.json'),
            'compilations':times,'new_executions':0,'executed_cycles':0,'simulation_seconds':0,'raw_denominator':len(denom),
            'limits':'Legal input/queue integrity and raw counter observations only, not specification output checking. Initial synchronous-reset pre outputs may be X in Icarus; compare post and all nonreset pre outputs. No LLM/positive event/verification claim.'}
    hit_union=set()
    for name,actions in cases().items():
        validate(actions);traces={};pts=[]
        for sim,binary in builds.items():
            f=out/name/sim;f.mkdir(parents=True);vec=f/'vectors.txt';vec.write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in actions))
            (f/'actions.json').write_text(json.dumps({'actions':actions},indent=2)+'\n');raw=f/'coverage.dat'
            cmd=([binary] if sim=='verilator' else ['vvp',binary])+['+VECTORS='+str(vec)]
            if sim=='verilator':cmd+=['+verilator+coverage+file+'+str(raw)]
            start=time.perf_counter()
            try:seconds,log=invoke(cmd,f/'simulation.log',timeout=30)
            finally:
                elapsed=time.perf_counter()-start
                recorded=(f/'simulation.log').read_text() if (f/'simulation.log').exists() else ''
                (f/'attempt.json').write_text(json.dumps({'command':list(map(str,cmd)),'elapsed_seconds':elapsed,
                    'cycles':sum(x.startswith('QUEUE ') for x in recorded.splitlines()),
                    'driver_complete':f'DRIVER_OK steps={len(actions)}' in recorded},indent=2)+'\n')
            if f'DRIVER_OK steps={len(actions)}' not in log:raise ValueError('Incomplete execution')
            trace,accepted=parse(log,actions,ins,outs);traces[sim]=trace
            (f/'trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n')
            (f/'execution.json').write_text(json.dumps({'command':list(map(str,cmd)),'seconds':seconds,'cycles':len(trace),'accepted_ids':accepted},indent=2)+'\n')
            result['new_executions']+=1;result['executed_cycles']+=len(trace);result['simulation_seconds']+=seconds
            if sim=='verilator':
                pts=load_all(raw,source)
                if {identity(p) for p in pts}!=denom:raise ValueError('DUT denominator changed')
                (f/'raw-points.json').write_text(json.dumps(pts,indent=2)+'\n')
        def comparable(rows):
            def meaningful(values):
                return {k:(v if k in ('s_axis_tready','m_axis_tvalid','m_axis_hdr_valid') or values['m_axis_hdr_valid' if k.startswith('m_axis_hdr_') else 'm_axis_tvalid'] else None) for k,v in values.items()}
            return [{**r,'pre':None if r['action']['rst'] else meaningful(r['pre']),'post':meaningful(r['post'])} for r in rows]
        if comparable(traces['verilator'])!=comparable(traces['iverilog']):raise ValueError('Dual simulator mismatch')
        by={identity(p):p['hits'] for p in pts};hit_union.update(k for k,v in by.items() if v>0)
        hits=[{'eclass':g['eclass'],'source_hits':[by[identity(m['mapping']['point'])] for m in g['members']]} for g in groups]
        result['cases'][name]={'cycles':len(actions),'input_beats_accepted':len(accepted),'dual_simulator_equal':True,'groups':hits,'coverage':summary(pts)}
    result['eligible_event_groups']=[g['eclass'] for g in groups if all(identity(m['mapping']['point']) not in hit_union for m in g['members'])]
    result['ordinary_contaminated_groups']=[g['eclass'] for g in groups if any(identity(m['mapping']['point']) in hit_union for m in g['members'])]
    result['gate']='reject_before_checker' if len(result['eligible_event_groups'])<3 else 'requires_independent_checker_and_multistep_controls'
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('gate','eligible_event_groups','ordinary_contaminated_groups','new_executions','executed_cycles')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.base.resolve(),a.output.resolve())
