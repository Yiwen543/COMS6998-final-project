"""Protocol-safe offer driver; no expected DUT outputs or coverage targeting.

Separate from the frozen ordinary-screen driver: supports pending batches and
mandatory low-CYC gap after errors, keeping queued unaccepted offers for restart.
"""
import argparse
import json
from pathlib import Path
from probe_wbxbar_ordinary import FIELDS, seed, action, cases, driver as ordinary_driver, comparable
from probe_wbxbar_ordinary import validate as ordinary_validate
from prepare_wbxbar_checker_role import verify_scope
from run_midterm_fixed import ROOT, sha, invoke
from inventory_natural_coverage import load_all
from preflight_spi_host import identity

BASE = ROOT / 'results/wbxbar_conditional_20261104/screen-v2'


def validate(actions):
    ordinary_validate(actions)
    if any(a['rst'] and a['offer'] for a in actions):
        raise ValueError('Offers during reset are not supported')


def driver(candidate, ports):
    text, inputs, outputs = ordinary_driver(candidate, ports)
    replacements = [
        ('integer fd,nread,cycle,m,head[0:1]', 'integer cooldown[0:1];\ninteger fd,nread,cycle,m,head[0:1]'),
        ('returned[m]=0;', 'returned[m]=0;cooldown[m]=0;'),
        ('i_mcyc[m]=!r_rst &&', 'i_mcyc[m]=!r_rst && cooldown[m]==0 &&'),
        ('i_mstb[m]=!r_rst &&', 'i_mstb[m]=!r_rst && cooldown[m]==0 &&'),
        ('  if(r_rst) begin previous_slave=0;response_data=0;end',
         '  for(m=0;m<2;m=m+1) if(cooldown[m]>0) cooldown[m]=cooldown[m]-1;\n  if(r_rst) begin previous_slave=0;response_data=0;end'),
        ('   if(pending[m]<0) $fatal(1,"orphan master response");',
         '   if(pending[m]<0) begin $display("DUT_DIAGNOSTIC orphan_response cycle=%0d master=%0d",cycle,m);pending[m]=0;end\n'
         '   if(pre_response[m] && o_merr[m]) begin pending[m]=0;cooldown[m]=1;end'),
        ('for(m=0;m<2;m=m+1) if(head[m]!=tail[m] || pending[m]!=0) $fatal(1,"ordinary delivery incomplete");',
         'for(m=0;m<2;m=m+1) $display("PENDING %0d %0d %0d",m,tail[m]-head[m],pending[m]);')]
    # Error must use the sampled PRE error, not the next POST output.
    replacements += [
        ('reg [1:0] previous_slave,pre_master,pre_response,pre_slave;', 'reg [1:0] previous_slave,pre_master,pre_response,pre_slave,pre_error;'),
        ('  pre_response=i_mcyc & (o_mack | o_merr);', '  pre_response=i_mcyc & (o_mack | o_merr);pre_error=i_mcyc & o_merr;'),
        ('if(pre_response[m] && o_merr[m])', 'if(pre_error[m])')]
    for before, after in replacements:
        expected = 2 if before == 'returned[m]=0;' else 1
        if text.count(before) != expected: raise ValueError('Ordinary template drift: ' + before)
        text = text.replace(before, after)
    return text, inputs, outputs


def parse(log, actions, inputs, outputs):
    records, ledgers = {}, {}
    for line in log.splitlines():
        fields = line.split()
        if not fields: continue
        if fields[0] == 'QUEUE':
            ledgers[int(fields[1]), int(fields[2])] = list(map(int, fields[3:])); continue
        if fields[0] not in ('PRE','POST'): continue
        names = inputs + outputs if fields[0] == 'PRE' else outputs
        if len(fields) != len(names)+2: raise ValueError('Trace field count')
        phase = fields[0].lower(); cycle = int(fields[1])
        if phase in records.setdefault(cycle, {}): raise ValueError('Duplicate trace row')
        records[cycle][phase] = {n: None if any(c in v.lower() for c in 'xz') else int(v,16) for n,v in zip(names, fields[2:])}
    if list(records) != list(range(len(actions))) or len(ledgers) != 2*len(actions):
        raise ValueError('Incomplete trace')
    queues = [[],[]]; sent = [0,0]; returned = [0,0]; pending = [0,0]; cooldown = [0,0]
    previous_slave = 0; response_data = 0; trace = []; diagnostics = []
    totals = dict.fromkeys(['offers','accepted','responses','reset_discarded_queued','reset_discarded_accepted','error_aborted_accepted'],0)
    for cycle, a in enumerate(actions):
        pre, post = records[cycle]['pre'], records[cycle]['post']
        want = dict.fromkeys(inputs,0); want['i_reset'] = a['rst']
        if a['rst']:
            totals['reset_discarded_queued'] += sum(map(len,queues)); totals['reset_discarded_accepted'] += sum(pending)
            queues=[[],[]];sent=[0,0];returned=[0,0];pending=[0,0];cooldown=[0,0];previous_slave=0;response_data=0
        for m in (0,1):
            if not a['rst'] and a['offer'] >> m & 1:
                queues[m].append(tuple(a[k]>>shift & ((1<<width)-1) for k,shift,width in
                    [('addr',8*m,8),('data',32*m,32),('we',m,1),('sel',4*m,4)]))
                totals['offers'] += 1
            active = not a['rst'] and cooldown[m] == 0
            want['i_mcyc'] |= int(active and bool(queues[m] or pending[m])) << m
            want['i_mstb'] |= int(active and bool(queues[m])) << m
            if want['i_mstb'] >> m & 1:
                for key,value,shift in zip(('i_maddr','i_mdata','i_mwe','i_msel'),queues[m][0],(8*m,32*m,m,4*m)):
                    want[key] |= value << shift
            cooldown[m] = max(0,cooldown[m]-1)
        scyc = pre['o_scyc'] or 0
        want.update(i_sack=previous_slave & ~a['slave_error'] & scyc & (0 if a['rst'] else 3),
                    i_serr=previous_slave & a['slave_error'] & scyc & (0 if a['rst'] else 3), i_sdata=response_data)
        if any(pre[k] != v for k,v in want.items()):
            raise ValueError('JSON/pin mismatch at cycle ' + str(cycle))
        for m in (0,1):
            accept = bool(want['i_mcyc']>>m&1 and want['i_mstb']>>m&1 and not pre['o_mstall']>>m&1)
            response = bool(want['i_mcyc']>>m&1 and (pre['o_mack']|pre['o_merr'])>>m&1)
            error = bool(want['i_mcyc']>>m&1 and pre['o_merr']>>m&1)
            if accept:queues[m].pop(0);sent[m]+=1;totals['accepted']+=1
            if response:returned[m]+=1;totals['responses']+=1
            pending[m] += int(accept)-int(response)
            if pending[m] < 0:
                diagnostics.append({'cycle':cycle,'master':m,'kind':'orphan_response'});pending[m]=0
            if error:
                totals['error_aborted_accepted'] += pending[m];pending[m]=0;cooldown[m]=1
            h,t,p,ac,ret = ledgers[cycle,m]
            if (h,t-h,p,ac,ret) != (sent[m],len(queues[m]),pending[m],sent[m],returned[m]):
                raise ValueError('Transport ledger mismatch')
        previous_slave = 0 if a['rst'] else pre['o_scyc'] & pre['o_sstb']
        response_data = sum((0xa55a0000 | ((pre['o_saddr'] or 0)>>(8*m)&255))<<(32*m) for m in (0,1))
        trace.append({'cycle':cycle,'pre':pre,'post':post})
    totals.update(queued=sum(map(len,queues)),outstanding=sum(pending),diagnostics=diagnostics,
                  delivery_complete=not any(queues) and not any(pending),cycles=len(actions))
    return trace, totals


def compile_driver(output):
    _, candidate = verify_scope()
    ports = json.loads((BASE/'netlist.json').read_text())['modules']['wbxbar']['ports']
    source, inputs, outputs = driver(candidate, ports)
    output.mkdir(parents=True, exist_ok=False)
    path = output / 'tb_natural_inventory.sv';path.write_text(source)
    files = [str(Path(candidate['root'])/name) for name in candidate['sources']]
    binaries = {}; compiles = []
    for simulator in ('verilator','iverilog'):
        folder=output/simulator;folder.mkdir();binary=folder/('obj/Vtb_natural_inventory' if simulator=='verilator' else 'tb.vvp')
        command=(['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',folder/'obj','-j','2'] if simulator=='verilator' else ['iverilog','-g2012','-s','tb_natural_inventory','-o',binary])+files+[path]
        seconds,_=invoke(command,folder/'compile.log',300)
        compiles.append({'simulator':simulator,'seconds':seconds,'command':list(map(str,command))});binaries[simulator]=binary
    manifest={'script_sha256':sha(Path(__file__)),'template_sha256':sha(ROOT/'scripts/probe_wbxbar_ordinary.py'),
              'driver_sha256':sha(path),'compilations':compiles,'fields':FIELDS,'inputs':inputs,'outputs':outputs,'sources':files}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return binaries, manifest


def simulate(binary, simulator, actions, output, manifest):
    validate(actions);output.mkdir(parents=True,exist_ok=False)
    vectors=output/'vectors.txt';vectors.write_text(''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions))
    command=([binary] if simulator=='verilator' else ['vvp',binary])+['+VECTORS='+str(vectors)]
    if simulator=='verilator':command+=['+verilator+coverage+file+'+str(output/'coverage.dat')]
    seconds,log=invoke(command,output/'simulation.log',30)
    execution={'command':list(map(str,command)),'seconds':seconds,'cycles':sum(line.startswith('PRE ') for line in log.splitlines())}
    (output/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    if 'DRIVER_OK steps='+str(len(actions)) not in log:raise ValueError('Incomplete simulation')
    trace,transport=parse(log,actions,manifest['inputs'],manifest['outputs'])
    (output/'trace.json').write_text(json.dumps(trace,indent=2)+'\n')
    (output/'transport.json').write_text(json.dumps(transport,indent=2)+'\n')
    return trace,transport


def preflight(output):
    output.mkdir(parents=True,exist_ok=False)
    binaries,manifest=compile_driver(output/'compiled')
    inputs=cases()
    inputs['pending_prefix']=seed()+[action(offer=1,addr=3,data=0x11223344,sel=15)]
    inputs['contended_burst']=seed()+[action(offer=3,addr=0x0302,data=0x8877665544332211,sel=255,we=3) for _ in range(4)]+[action() for _ in range(64)]
    inputs['error_burst_restart']=seed()+[action(offer=1,addr=3,data=0x11223344,sel=15,slave_error=1) for _ in range(4)]+[action(slave_error=1) for _ in range(12)]+[action(offer=1,addr=4,data=0x55667788,sel=15)]+[action() for _ in range(64)]
    inputs['reset_pending_restart']=seed()+[action(offer=1,addr=3,data=0x11223344,sel=15),action(rst=1),action(rst=1),action(offer=1,addr=4,data=0x55667788,sel=15)]+[action() for _ in range(64)]
    (output/'actions.json').write_text(json.dumps(inputs,indent=2)+'\n')
    denom={identity(p) for p in json.loads((BASE/'inventory/raw-points.json').read_text())}
    rows=[]
    for name,actions in inputs.items():
        traces={};transports={}
        for sim,binary in binaries.items():
            traces[sim],transports[sim]=simulate(binary,sim,actions,output/name/sim,manifest)
        if comparable(traces['verilator'],manifest['outputs'])!=comparable(traces['iverilog'],manifest['outputs']):raise ValueError('Simulator disagreement: '+name)
        if transports['verilator']!=transports['iverilog']:raise ValueError('Transport disagreement: '+name)
        points=load_all(output/name/'verilator/coverage.dat',manifest['sources'])
        if {identity(p) for p in points}!=denom:raise ValueError('Raw denominator drift')
        rows.append({'case':name,'transport':transports['verilator'],'dual_simulator_match':True})
    if rows[-4]['transport']['delivery_complete']:raise ValueError('Pending prefix incorrectly completed')
    result={'status':'driver_transport_preflight_not_functional_freeze','cases':rows,'raw_denominator':len(denom),
            'executions':len(rows)*2,'executed_cycles':sum(len(a)*2 for a in inputs.values()),'model_calls':0,
            'hashes':{str(p):sha(p) for p in [Path(__file__),output/'actions.json',output/'compiled/manifest.json']}}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','executions','executed_cycles','raw_denominator')}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    preflight(a.output.resolve())
