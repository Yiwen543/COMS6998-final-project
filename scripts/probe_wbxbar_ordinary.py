"""Ordinary-operation exclusion only; fixed JSON transport, NO functional checker.

No coverage-aware generation, solver witness or LLM. Original source counters
can be rejected by ordinary hits; no positive correctness claim is possible.
"""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha,invoke
from prove_wbxbar_index import configuration,SCOPE
from inventory_natural_coverage import load_all
from preflight_spi_host import identity

FIELDS={'rst':1,'offer':2,'addr':16,'data':64,'we':2,'sel':8,'slave_error':2}
BASE=ROOT/'results/wbxbar_conditional_20261104/screen-v2'

def action(**kw):return dict({'rst':0,'offer':0,'addr':0,'data':0,'we':0,'sel':0,'slave_error':0},**kw)
def seed():return [action(rst=1),action(rst=1)]+[action() for _ in range(6)]

def cases():
    result={}
    def add(name,offers,error=0):
        result[name]=seed()+[action(**a,slave_error=error) for a in offers]+[action(slave_error=error) for _ in range(64)]
    def beat(master,dest,i,we,sel):
        return {'offer':1<<master,'addr':(dest*16+(i%16))<<(8*master),
                'data':((0x12345678+37*i+master)&0xffffffff)<<(32*master),'we':we<<master,'sel':sel<<(4*master)}
    for master in range(2):
        for dest in range(3):
            for we in range(2):
                mask=(0,1,5,15)[(master+dest+we)%4]
                add(f'isolated_m{master}_d{dest}_w{we}',[beat(master,dest,0,we,mask)])
        for dest in range(2):
            for n in (2,4,7):
                add(f'burst_m{master}_d{dest}_n{n}',[beat(master,dest,i,(i+n)%2,(0,1,5,15)[i%4]) for i in range(n)])
            for we in range(2):add(f'error_m{master}_d{dest}_w{we}',[beat(master,dest,0,we,15)],1<<dest)
            offers=[beat(master,dest,0,0,15)]+[{} for _ in range(20)]+[beat(master,1-dest,0,1,5)]
            add(f'release_reacquire_m{master}_d{dest}',offers)
    for swapped in range(2):
        for n in (1,2,4,7):
            offers=[]
            for i in range(n):
                a,b=beat(0,swapped,i,i%2,15),beat(1,1-swapped,i,1-i%2,5)
                offers.append({k:a[k]|b[k] for k in a})
            add(f'disjoint_concurrent_s{swapped}_n{n}',offers)
    return result

def validate(actions):
    if not 8<=len(actions)<=392 or actions[:8]!=seed():raise ValueError('Seed/physical-cycle bound')
    for a in actions:
        if set(a)!=set(FIELDS) or any(type(a[k]) is not int or not 0<=a[k]<1<<w for k,w in FIELDS.items()):raise ValueError('JSON field/width/type')

def driver(c,ports):
    ins=[n for n,p in ports.items() if p['direction']=='input' and n!='i_clk'];outs=[n for n,p in ports.items() if p['direction']=='output']
    decl=['logic '+(f'[{len(p["bits"])-1}:0] ' if len(p['bits'])>1 else '')+n+';' for n,p in ports.items()]
    fields=['logic '+(f'[{w-1}:0] ' if w>1 else '')+'r_'+n+';' for n,w in FIELDS.items()]
    params=','.join('.'+k+'('+str(v)+')' for k,v in c['parameters'].items())
    def display(tag,fs):return '$display("'+tag+' %0d'+(' %h'*len(fs))+'",cycle,'+','.join(fs)+');'
    tb='`timescale 1ns/1ps\nmodule tb_natural_inventory;\n'+'\n'.join(decl+fields)+f'\nwbxbar #({params}) dut(.*);\n'+'''
integer fd,nread,cycle,m,head[0:1],tail[0:1],pending[0:1],accepted[0:1],returned[0:1];
reg [7:0] addrq[0:1][0:391];reg [31:0] dataq[0:1][0:391];reg weq[0:1][0:391];reg [3:0] selq[0:1][0:391];
reg [1:0] previous_slave,pre_master,pre_response,pre_slave;reg [63:0] response_data;string vectors;
initial begin
'''+ '\n'.join(n+'=0;' for n,p in ports.items() if p['direction']=='input')+'''
cycle=0;previous_slave=0;response_data=0;
for(m=0;m<2;m=m+1) begin head[m]=0;tail[m]=0;pending[m]=0;accepted[m]=0;returned[m]=0;end
if(!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"missing vectors");
fd=$fopen(vectors,"r");if(!fd) $fatal(1,"cannot open vectors");
while(!$feof(fd)) begin
 nread=$fscanf(fd,"%h %h %h %h %h %h %h",r_rst,r_offer,r_addr,r_data,r_we,r_sel,r_slave_error);
 if(nread==7) begin
  if(cycle>=392) $fatal(1,"cycle limit");
  i_reset=r_rst;i_mcyc=0;i_mstb=0;i_maddr=0;i_mdata=0;i_mwe=0;i_msel=0;i_sstall=0;
  for(m=0;m<2;m=m+1) begin
   if(r_rst) begin head[m]=0;tail[m]=0;pending[m]=0;accepted[m]=0;returned[m]=0;end
   else if(r_offer[m]) begin
    if(tail[m]>=392) $fatal(1,"queue overflow");
    addrq[m][tail[m]]=r_addr[m*8+:8];dataq[m][tail[m]]=r_data[m*32+:32];weq[m][tail[m]]=r_we[m];selq[m][tail[m]]=r_sel[m*4+:4];tail[m]=tail[m]+1;
   end
   i_mcyc[m]=!r_rst && (head[m]<tail[m] || pending[m]>0);
   i_mstb[m]=!r_rst && head[m]<tail[m];
   if(i_mstb[m]) begin i_maddr[m*8+:8]=addrq[m][head[m]];i_mdata[m*32+:32]=dataq[m][head[m]];i_mwe[m]=weq[m][head[m]];i_msel[m*4+:4]=selq[m][head[m]];end
  end
  if(r_rst) begin previous_slave=0;response_data=0;end
  i_sack=previous_slave & ~r_slave_error & o_scyc & {2{!r_rst}};
  i_serr=previous_slave & r_slave_error & o_scyc & {2{!r_rst}};
  i_sdata=response_data;
  #4;
  pre_master=i_mcyc & i_mstb & ~o_mstall;
  pre_response=i_mcyc & (o_mack | o_merr);
  pre_slave=o_scyc & o_sstb & ~i_sstall & {2{!r_rst}};
'''+display('PRE',ins+outs)+'''
  for(m=0;m<2;m=m+1) response_data[m*32+:32]=32'ha55a0000 | {24'd0,o_saddr[m*8+:8]};
  #1;i_clk=1;#4;
'''+display('POST',outs)+'''
  #1;i_clk=0;
  for(m=0;m<2;m=m+1) begin
   if(pre_master[m]) begin head[m]=head[m]+1;accepted[m]=accepted[m]+1;end
   if(pre_response[m]) returned[m]=returned[m]+1;
   pending[m]=pending[m]+(pre_master[m]?1:0)-(pre_response[m]?1:0);
   if(pending[m]<0) $fatal(1,"orphan master response");
   $display("QUEUE %0d %0d %0d %0d %0d %0d %0d",cycle,m,head[m],tail[m],pending[m],accepted[m],returned[m]);
  end
  previous_slave=pre_slave;cycle=cycle+1;
 end else if(!$feof(fd)) $fatal(1,"bad vector");
end
for(m=0;m<2;m=m+1) if(head[m]!=tail[m] || pending[m]!=0) $fatal(1,"ordinary delivery incomplete");
$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
'''
    return tb,ins,outs

def parse(log,actions,ins,outs):
    rec={};ledger={}
    for line in log.splitlines():
        xs=line.split()
        if not xs or xs[0] not in ('PRE','POST','QUEUE'):continue
        if xs[0]=='QUEUE':ledger[(int(xs[1]),int(xs[2]))]=list(map(int,xs[3:]));continue
        fields=ins+outs if xs[0]=='PRE' else outs
        if len(xs)!=len(fields)+2:raise ValueError('Trace schema mismatch')
        rec.setdefault(int(xs[1]),{})[xs[0]]={k:None if any(x in v.lower() for x in 'xz') else int(v,16) for k,v in zip(fields,xs[2:])}
    if list(rec)!=list(range(len(actions))) or len(ledger)!=2*len(actions):raise ValueError('Incomplete trace')
    queues=[[],[]];sent=[0,0];done=[0,0];pending=[0,0];previous_slave=0;data=0;trace=[]
    for cycle,a in enumerate(actions):
        pre,post=rec[cycle]['PRE'],rec[cycle]['POST'];want={'i_reset':a['rst'],'i_sstall':0,'i_mcyc':0,'i_mstb':0,'i_maddr':0,'i_mdata':0,'i_mwe':0,'i_msel':0}
        if a['rst']:queues=[[],[]];sent=[0,0];done=[0,0];pending=[0,0];previous_slave=0;data=0
        for m in (0,1):
            if not a['rst'] and a['offer']>>m&1:queues[m].append(tuple(a[k]>>off&((1<<w)-1) for k,off,w in [('addr',8*m,8),('data',32*m,32),('we',m,1),('sel',4*m,4)]))
            want['i_mcyc']|=int(bool(queues[m] or pending[m]))<<m;want['i_mstb']|=int(bool(queues[m]))<<m
            if queues[m]:
                for k,x,off in zip(('i_maddr','i_mdata','i_mwe','i_msel'),queues[m][0],(8*m,32*m,m,4*m)):want[k]|=x<<off
        # Slave response values follow actual accepted slave requests; this is
        # input transport checking, never an expected DUT read-data scoreboard.
        scyc=pre['o_scyc'] if pre['o_scyc'] is not None else 0
        want.update(i_sack=previous_slave & ~a['slave_error'] & scyc & (0 if a['rst'] else 3),
                    i_serr=previous_slave & a['slave_error'] & scyc & (0 if a['rst'] else 3),i_sdata=data)
        if any(pre[k]!=v for k,v in want.items()):raise ValueError('Input driver/JSON mismatch at '+str(cycle))
        if not a['rst'] and pre['o_mack']&pre['o_merr']:raise ValueError('Conflicting master responses')
        for m in (0,1):
            accept=bool(want['i_mcyc']>>m&1 and want['i_mstb']>>m&1 and not pre['o_mstall']>>m&1)
            response=bool(want['i_mcyc']>>m&1 and (pre['o_mack']|pre['o_merr'])>>m&1)
            if accept:queues[m].pop(0);sent[m]+=1
            if response:done[m]+=1
            pending[m]+=int(accept)-int(response)
            h,t,p,ac,ret=ledger[cycle,m]
            if pending[m]<0 or (h,t-h,p,ac,ret)!=(sent[m],len(queues[m]),pending[m],sent[m],done[m]):raise ValueError('Transport ledger disagreement')
        if a['rst']:previous_slave=0
        else:previous_slave=pre['o_scyc']&pre['o_sstb']
        data=sum((0xa55a0000 | ((pre['o_saddr'] or 0)>>(m*8)&255))<<(m*32) for m in (0,1))
        trace.append({'cycle':cycle,'pre':pre,'post':post,'ledger':[ledger[cycle,m] for m in (0,1)]})
    if any(queues) or any(pending):raise ValueError('Ordinary input delivery incomplete')
    return trace

def comparable(trace,outs):
    rows=[]
    for t in trace:
        for phase in ('pre','post'):
            if phase=='pre' and t['pre']['i_reset']:continue
            d=t[phase];r={k:d[k] for k in ('o_mstall','o_mack','o_merr','o_scyc','o_sstb')}
            for m in (0,1):
                if d['o_mack']>>m&1:r['master_data'+str(m)]=None if d['o_mdata'] is None else d['o_mdata']>>(32*m)&0xffffffff
                if d['o_scyc']>>m&1 and d['o_sstb']>>m&1:
                    for n,w in [('o_swe',1),('o_saddr',8),('o_sdata',32),('o_ssel',4)]:r[n+str(m)]=None if d[n] is None else d[n]>>(w*m)&((1<<w)-1)
            if None in r.values():raise ValueError('Unknown meaningful output')
            rows.append((t['cycle'],phase,r))
    return rows

def run(out,base=BASE):
    scope,c=configuration();screen=json.loads((base/'screen/screen.json').read_text())
    if not screen['static_count_gate_pass']:raise ValueError('Static gate has not passed')
    for p,h in screen['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Static screen provenance drift: '+p)
    out.mkdir(parents=True,exist_ok=False);ports=json.loads((base/'netlist.json').read_text())['modules']['wbxbar']['ports']
    tb,ins,outs=driver(c,ports);path=out/'tb_natural_inventory.sv';path.write_text(tb)
    (out/'schema.json').write_text(json.dumps({'fields':FIELDS,'physical_cycle_limit':392,'seed':seed(),'semantics':'Offer FIFO per master; hold CYC through responses, STB/payload through acceptance; prompt in-order slave responses; no functional checker'},indent=2)+'\n')
    files=[str(Path(c['root'])/f) for f in c['sources']];builds={};compiles=[]
    for sim in ('verilator','iverilog'):
        folder=out/sim;folder.mkdir();binary=folder/('obj/Vtb_natural_inventory' if sim=='verilator' else 'tb.vvp')
        cmd=(['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',folder/'obj','-j','2'] if sim=='verilator' else ['iverilog','-g2012','-s','tb_natural_inventory','-o',binary])+files+[path]
        seconds,_=invoke(cmd,folder/'compile.log',300);builds[sim]=binary;compiles.append({'simulator':sim,'seconds':seconds,'command':list(map(str,cmd))})
    seedpoints=json.loads((base/'inventory/raw-points.json').read_text());denom={identity(p) for p in seedpoints};union=set();rows=[]
    groups=[g for g in screen['groups'] if g['static_candidate_group']]
    allcases=cases();(out/'cases.json').write_text(json.dumps(allcases,indent=2)+'\n')
    for name,actions in allcases.items():
        validate(actions);traces={};points=[]
        for sim,binary in builds.items():
            d=out/name/sim;d.mkdir(parents=True);vec=d/'vectors.txt';vec.write_text(''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions));cov=d/'coverage.dat'
            cmd=([binary] if sim=='verilator' else ['vvp',binary])+['+VECTORS='+str(vec)]
            if sim=='verilator':cmd+=['+verilator+coverage+file+'+str(cov)]
            seconds,log=invoke(cmd,d/'simulation.log',30)
            (d/'execution.json').write_text(json.dumps({'command':list(map(str,cmd)),'seconds':seconds,'cycles':sum(x.startswith('PRE ') for x in log.splitlines())},indent=2)+'\n')
            if 'DRIVER_OK steps='+str(len(actions)) not in log:raise ValueError('Incomplete driver run')
            trace=parse(log,actions,ins,outs);(d/'trace.json').write_text(json.dumps(trace,indent=2)+'\n');traces[sim]=trace
            if sim=='verilator':
                points=load_all(cov,files)
                if {identity(p) for p in points}!=denom:raise ValueError('DUT denominator drift')
        if comparable(traces['verilator'],outs)!=comparable(traces['iverilog'],outs):raise ValueError('Dual-simulator meaningful trace mismatch: '+name)
        hit={identity(p) for p in points if p['hits']>0};union|=hit
        rows.append({'case':name,'cycles_per_simulator':len(actions),'dual_simulator_match':True,'covered':len(hit)})
        print(name,'ok',flush=True)
    excluded=[];surviving=[]
    for g in groups:
        ids={identity(m['mapping']['point']) for m in g['members'] if m['seed_zero_dynamic_candidate']}
        row={'eclass':g['eclass'],'nontrivial':g['nontrivial_static_candidate'],'source_members':sorted(ids),'ordinary_hit_members':sorted(ids&union)}
        (excluded if ids&union else surviving).append(row)
    r={'status':'negative_ordinary_screen_complete','scope_sha256':sha(SCOPE),'script_sha256':sha(Path(__file__)),'driver_sha256':sha(path),
       'screen_sha256':sha(base/'screen/screen.json'),'cases':rows,'compilations':compiles,'executions':len(rows)*2,'executed_cycles':sum(r['cycles_per_simulator']*2 for r in rows),
       'raw_denominator':len(denom),'ordinary_union_covered':len(union),'excluded_groups':excluded,'surviving_groups':surviving,
       'ordinary_gate_pass':len(surviving)>=3 and sum(g['nontrivial'] for g in surviving)>=2,
       'model_calls':0,'checker_exists':False,'B_allowed':False,'C_allowed':False,
       'limits':'Negative exclusion only. No specification-based golden output checking or positive multistep reachability. Undefined inactive payload excluded from simulator comparison. No solver/model-derived stimulus.'}
    (out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('executions','executed_cycles','ordinary_gate_pass','raw_denominator')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.output.resolve())
