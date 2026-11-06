"""Saved-evidence BMC chain audit; never executes EDA, a monitor or a model.

Consistency acceptance is separate from scientific adjudication. Selected pre(S)
alarms are never confirmed by a reference that saw only through post(S-1).
"""
import argparse
import ast
from collections import Counter
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import time
import zlib

ROOT=Path(__file__).resolve().parents[2]
INPUTS=('rst','s_valid','s_data','s_last','m_ready','h_ready')
OUTPUTS=('s_ready','m_data','m_valid','m_last','h_valid','h_pad','h_truncate','h_length','h_original_length')
WIDTHS=dict(zip(INPUTS,(1,1,8,1,1,1)),**dict(zip(OUTPUTS,(1,8,1,1,1,1,1,16,16))))
CHECKER_SHA='b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee'
P01_SHA='79d5bdb4f86bb82fa94c273afb7ec07cec695f05077a6e05621ac11df7bf1cbf'


def sha(data):return hashlib.sha256(data).hexdigest()
def need(ok,why):
    if not ok:raise ValueError(why)
def canon(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


class Saved:
    def __init__(self,root,anchors=None):self.root=Path(root).resolve();self.anchors=anchors or {};self.files={};self.unanchored=set()
    def path(self,p):
        p=Path(p).resolve();need(p.is_relative_to(self.root) and not p.is_relative_to(self.root/'build/private'),'evidence path outside allowlist');return p
    def raw(self,p):
        p=self.path(p);data=p.read_bytes();key=str(p.relative_to(self.root));h=sha(data)
        if key in self.anchors:need(h==self.anchors[key],'independent saved-input anchor mismatch: '+key)
        else:self.unanchored.add(key)
        self.files[key]=h;return data
    def text(self,p):return self.raw(p).decode()
    def load(self,p):return json.loads(self.raw(p))


def decode_vcd(text,slot):
    """Independently parse declared top pins and explicit SMT-state assignments."""
    need(type(slot) is int and 0<=slot<6,'bad selected slot')
    scopes=[];pins={};width={};step_id=None;body=False;values={};seen=set();frames={};partials={}
    def flush():
        if step_id not in values:return
        step=values[step_id];need(step>=0,'unknown SMT step')
        required={pins[n] for n in INPUTS+('active','ok')}
        if required<=seen:
            frame={n:values.get(i,-1) for n,i in pins.items()}
            if step in frames:need(frames[step]==frame,'VCD state changed within one SMT step')
            frames[step]=frame
        else:partials[step]=seen & {pins[n] for n in INPUTS}
    for raw in text.splitlines():
        s=raw.strip();w=s.split()
        if not body:
            if s.startswith('$scope '):scopes.append(w[2])
            elif s.startswith('$upscope'):need(bool(scopes),'VCD scope underflow');scopes.pop()
            elif s.startswith('$var '):
                if w[4]=='smt_step' and not scopes:need(step_id is None,'duplicate SMT step');step_id=w[3];width[w[3]]=int(w[2])
                if scopes==['formal_top'] and w[4] in INPUTS+OUTPUTS+('active','ok'):
                    n=w[4];need(n not in pins,'duplicate VCD public pin');declared=int(w[2])
                    need((slot < declared <= 6) if n in ('active','ok') else declared==WIDTHS[n], 'VCD selected slot/pin width mismatch')
                    pins[n]=w[3];width[w[3]]=declared
            elif s.startswith('$enddefinitions'):
                need(step_id is not None and set(INPUTS+OUTPUTS+('active','ok'))<=set(pins),'VCD missing declared inputs/monitor pins');body=True
            continue
        if s.startswith('#'):flush();continue
        if s.startswith('b'):
            bits,ident=s[1:].split()
        elif s and s[0] in '01xz':bits,ident=s[0],s[1:]
        else:continue
        if ident not in width:continue
        need(bool(re.fullmatch('[01xz]+',bits.lower())) and len(bits)<=width[ident],'invalid VCD literal width/value')
        v=-1 if any(c in bits.lower() for c in 'xz') else int(bits,2)
        if ident==step_id and values.get(ident)!=v:seen.clear()
        values[ident]=v;seen.add(ident)
    need(body,'truncated VCD header');flush()
    need(len(frames)>=2 and sorted(frames)==list(range(len(frames))),'missing/truncated consecutive VCD input states')
    need(all(s in frames or s==len(frames) and not touched for s,touched in partials.items()),'truncated VCD input frame')
    ordered=[frames[i] for i in range(len(frames))]
    inputs=[{n:f[n] for n in INPUTS} for f in ordered]
    need(all(0<=v<2**WIDTHS[n] for x in inputs for n,v in x.items()),'unknown/out-of-range VCD input')
    alarms=[i for i,f in enumerate(ordered) if i>0 and f['active']>=0 and f['ok']>=0 and f['active']&(1<<slot) and not f['ok']&(1<<slot)]
    need(bool(alarms),'no definite selected-slot VCD alarm');s=alarms[0]
    return inputs[:s+1],[{n:f[n] for n in OUTPUTS if n in f} for f in ordered[:s+1]],s


def parse_physical(text,inputs):
    expected=[(i,p) for i in range(len(inputs)) for p in ('pre','post')];observed=[];rows=[dict(cycle=i,inputs=copy.deepcopy(x)) for i,x in enumerate(inputs)];done=[]
    for line in text.splitlines():
        w=line.split()
        if not w:continue
        if w[0]=='LITERAL_COMPLETE':need(len(w)==2,'malformed physical completion');done.append(int(w[1]));continue
        if w[0] not in ('PRE','POST'):continue
        phase=w[0].lower();need(len(w)==2+len(OUTPUTS)+(len(INPUTS) if phase=='pre' else 0),'physical pin count mismatch')
        cycle=int(w[1]);need(0<=cycle<len(rows),'physical cycle out of range');observed.append((cycle,phase))
        def number(s):
            need(bool(re.fullmatch(r'(?:-?\d+|[xXzZ]+)',s)),'invalid physical bit literal')
            return -1 if any(c in s.lower() for c in 'xz') else int(s)
        vals=[number(s) for s in w[2:]]
        if phase=='pre':need(vals[:len(INPUTS)]==[inputs[cycle][n] for n in INPUTS],'literal input/timing offset');vals=vals[len(INPUTS):]
        need(all(-1<=v<2**WIDTHS[n] for n,v in zip(OUTPUTS,vals)),'physical output width mismatch')
        rows[cycle][phase]=dict(zip(OUTPUTS,vals))
    need(done==[len(inputs)] and observed==expected,'physical log missing/truncated/duplicate/phase-offset samples')
    return rows


def meaningful(rows):
    result=copy.deepcopy(rows)
    for r in result:
        for phase in ('pre','post'):
            v=r[phase]
            r[phase]=None if r['cycle']==0 and phase=='pre' else {n:value if n in ('s_ready','m_valid','h_valid') or v['h_valid' if n.startswith('h_') else 'm_valid']!=0 else None for n,value in v.items()}
    return result


def legal(inputs,rows):
    need(inputs[0]['rst']==1,'initial reset absent');count=0
    for i,x in enumerate(inputs):
        if x['rst']:need(x['s_valid']==0,'offer during reset');count=0;continue
        if i and not inputs[i-1]['rst'] and inputs[i-1]['s_valid'] and rows[i-1]['pre']['s_ready']==0:
            need(all(x[n]==inputs[i-1][n] for n in ('s_valid','s_data','s_last')),'blocked offer stability violated')
        if x['s_valid'] and rows[i]['pre']['s_ready']==1:
            count+=1;need(count<=12 and (count<12 or x['s_last']),'frame assumption violated')
            if x['s_last']:count=0


def parse_mon(raw,cycles):
    samples=[]
    for line in raw.decode().splitlines():
        w=line.split()
        if not w or w[0]!='MON':continue
        need(len(w)==5 and w[2] in ('pre','post') and all(re.fullmatch('[01xz]{6}',s) for s in w[3:]),'malformed raw MON')
        samples.append((int(w[1]),w[2],w[3],w[4]))
    expected=[(i,p) for i in range(cycles) for p in ('pre','post') if i or p=='post']
    need([(i,p) for i,p,a,k in samples]==expected and raw.decode().splitlines().count('REPLAY_COMPLETE')==1,'MON missing/truncated/wrong phase or cycle')
    props=[]
    for slot in range(6):
        checks=0;failures=[];unknown=[]
        for cycle,phase,a,k in samples:
            active,ok=a[5-slot],k[5-slot]
            if active not in '01' or active=='1' and ok not in '01':unknown.append([cycle,phase])
            elif active=='1':
                checks+=1
                if ok=='0':failures.append([cycle,phase])
        props.append(dict(id=f'P{slot}',checks=checks,failures=failures,unknown=unknown,end_sample_checks=0,ordinary_sample_checks=checks,vacuous_on_trace=checks==0))
    return samples,props


def encode_hex(rows):
    vals=lambda r:[r['cycle']]+[r['inputs'][n] for n in INPUTS]+[r[p][n] for p in ('pre','post') for n in OUTPUTS]
    return ('\n'.join(' '.join('x' if v==-1 else format(v,'x') for v in vals(r)) for r in rows)+'\n').encode()


def load_checker(path,expected_sha=CHECKER_SHA):
    data=Path(path).read_bytes();need(sha(data)==expected_sha,'frozen checker hash mismatch')
    tree=ast.parse(data)
    need(all(isinstance(n,(ast.Import,ast.FunctionDef,ast.Assign)) for n in tree.body),'unexpected frozen checker top-level execution')
    need(all(a.name in ('collections','copy','math') for n in tree.body if isinstance(n,ast.Import) for a in n.names),'unexpected frozen checker import')
    spec=importlib.util.spec_from_file_location('_exact_frozen_claude_reference',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module.check_rows


def inspect_chain(job,slot,reader,checker):
    physical=job/'physical';vcd=list((job/'work').glob('engine_*/trace.vcd'));need(len(vcd)==1,'missing/duplicate raw VCD')
    inputs,model_outputs,alarm=decode_vcd(reader.text(vcd[0]),slot)
    need(reader.load(physical/'formal-inputs.json')==inputs,'VCD/formal-inputs mismatch')
    both={}
    for sim in ('iverilog','verilator'):
        d=physical/sim;transport=reader.text(d/'inputs.txt')
        expected=''.join(' '.join(str(x[n]) for n in INPUTS)+'\n' for x in inputs);need(transport==expected,'literal transport file mismatch')
        raw=reader.raw(d/'simulation.log');rows=parse_physical(raw.decode(),inputs)
        need(reader.load(d/'rows.json')==rows,'raw physical log/rows mismatch');legal(inputs,rows)
        exe=reader.load(d/'execution.json');need(exe['status']=='complete' and exe['returncode']==0 and exe['cycles']==len(rows),'physical execution incomplete')
        need(exe['log_sha256']==sha(raw),'physical execution log digest mismatch')
        need('+INPUTS='+str(d/'inputs.txt') in exe['argv'],'physical argv transport binding mismatch');both[sim]=rows
    rows=both['iverilog'];need(meaningful(rows)==meaningful(both['verilator']),'dual simulator meaningful-output mismatch')
    for i,outputs in enumerate(model_outputs):
        if i==0:continue
        for name,value in outputs.items():
            if name in ('s_ready','m_valid','h_valid') or rows[i]['pre']['h_valid' if name.startswith('h_') else 'm_valid']==1:
                need(value>=0 and value==rows[i]['pre'][name],'VCD/physical retained pre output mismatch')
    d=physical/'candidate-replay';m=reader.load(d/'result.json');compressed=reader.raw(d/'replay.log.gz');raw=gzip.decompress(compressed)
    need(m['compressed_log_sha256']==sha(compressed) and m['raw_log_sha256']==sha(raw) and m['execution']['log_sha256']==sha(raw),'MON compressed/raw log binding mismatch')
    need(m['complete'] and m['execution']['status']=='complete' and m['execution']['returncode']==0,'monitor saved execution incomplete')
    need(m['trace_done_sample'] is None and m['safety_projection'] and m['DUT_inputs_unchanged'],'monitor projection metadata mismatch')
    args=m['execution']['argv'];need(args.count('+LAST=-1')==1,'monitor final-marker/projection mismatch')
    rowpaths=[a[6:] for a in args if a.startswith('+ROWS=')];need(len(rowpaths)==1,'monitor input transport missing/duplicate')
    rowpath=reader.path(rowpaths[0]);rowhash=sha(canon(rows));need(m['rows_sha256']==rowhash and rowpath.stem==rowhash,'monitor input rows digest mismatch')
    need(reader.raw(rowpath)==encode_hex(rows),'MON HEX transport/physical rows mismatch')
    samples,props=parse_mon(raw,len(rows));need(m['properties']==props,'raw MON/property summary mismatch')
    need(m['samples']==len(samples) and m['cycles']==len(rows) and m['attempted_cycles']==len(rows),'MON sample/cycle count mismatch')
    reproduced=[alarm,'pre'] in props[slot]['failures'];p=reader.load(physical/'result.json')
    selected=next((active[5-slot],ok[5-slot]) for cycle,phase,active,ok in samples if (cycle,phase)==(alarm,'pre'))
    receipt=dict(chain_consistency='PASS',selected_sample=dict(cycle=alarm,phase='pre',slot=slot),selected_physical_bits=dict(active=selected[0],ok=selected[1]),selected_candidate_unknown=selected[0] not in '01' or selected[0]=='1' and selected[1] not in '01',physical_alarm_reproduced=reproduced,scientific_adjudication='UNRESOLVED',reference_verdict=None,reference_confirmed_selected_alarm=False,finite_completion_proved=False,candidate_correctness_proved=False)
    need(p.get('candidate_false_alarm_claim',False) is False, 'unattributed prefix upgraded to false-alarm claim')
    need(p.get('trace_done')==0 and p.get('finite_completion_proved') is False,'physical scope metadata mismatch')
    if reproduced:
        prefix=reader.load(physical/'reference-prefix-rows.json');need(prefix==rows[:alarm],'reference prefix phase/length mismatch')
        ref=reader.load(physical/'reference.json');fresh=checker(copy.deepcopy(prefix),require_drained=False,min_tail=32);need(fresh==ref,'saved/frozen-pure-reference result mismatch')
        need(p['reference_verdict']==ref['verdict'] and p['reference_failures']==ref['failures'] and p['reference_unknown']==ref['unknown'],'physical/reference summary mismatch')
        need(p['selected_alarm']==dict(cycle=alarm,phase='pre',slot=slot,category='UNATTRIBUTED'),'selected slot/phase/category mismatch')
        need(p['reference_last_sample']==dict(cycle=alarm-1,phase='post') and p['reference_rows']==alarm,'reference prefix scope mismatch')
        need(p['reference_confirmed_selected_alarm'] is False and p['formal_alarm_reproduced'] is True,'reference scope improperly upgraded')
        need(p['witness_sha256']==reader.files[str(vcd[0].resolve().relative_to(reader.root))],'physical VCD digest mismatch')
        need(p['formal_states']==len(inputs) and p['physical_cycles']==2*len(inputs) and p['candidate_monitor_cycles']==len(inputs) and p['observed_alarm_state']==alarm,'physical chain cost/state count mismatch')
        receipt.update(reference_verdict=ref['verdict'],reference_last_sample=dict(cycle=alarm-1,phase='post'),reference_unknown=ref['unknown'],pure_reference_rechecked=True)
    else:
        need(p['status']=='unresolved' and not p.get('formal_alarm_reproduced',False),'unreproduced witness upgraded')
        need(not (physical/'reference.json').exists() and not (physical/'reference-prefix-rows.json').exists() and 'reference_verdict' not in p,'unreproduced witness has unexpected reference evidence')
        receipt.update(reference_verdict=None,reference_not_evaluated=True,pure_reference_rechecked=False,unresolved_reason='Selected physical alarm not reproduced; no reference verdict recorded. Root cause not established.')
    return receipt,m


def check_native(job,row,reader,candidate):
    result=reader.load(job/'result.json');need(all(result[k]==row[k] for k in result),'native job/summary identity mismatch')
    need(row['mode']=='bmc' and row['status']=='FAIL' and row['trace_done']==0 and row['scope']=='safety_projection','unsupported native witness scope')
    need(reader.text(job/'work/status').split()[0]=='FAIL','native raw status mismatch')
    need(sha(reader.raw(job/'sby.log'))==result['log_sha256'],'native log digest mismatch')
    config=reader.text(job/'job.sby');need('mode bmc\n' in config and 'depth 24\n' in config,'native profile mismatch')
    section=config.split('[files]\n')[1];sources={}
    for line in section.splitlines():
        if not line.strip():continue
        w=line.split();need(len(w) in (1,2),'malformed native source map');path=reader.path(w[-1]);alias=w[0] if len(w)==2 else path.name;sources[alias]=path
        need(reader.raw(path)==reader.raw(job/'work/src'/alias),'native copied source mismatch')
    need(set(sources)==set(('dut.v','axis_fifo.v','axis_frame_length_adjust_fifo.v','task_top_v3.sv','candidate.sv','harness.sv')), 'native source inventory mismatch')
    need(sources['candidate.sv']==candidate/'candidate.sv','native candidate identity mismatch')
    source=sources['dut.v'];need((row['source']=='correct' and source.name=='axis_frame_length_adjust.v') or source.name==row['source']+'.v','DUT/mutant native identity mismatch')
    slot=row['slot'];harness=reader.text(job/'harness.sv')
    need(sources['harness.sv']==job/'harness.sv' and f'assert(!active[{slot}] || ok[{slot}]);' in harness and f'cover(active[{slot}]);' in harness,'native harness selected slot mismatch')
    need("wire trace_done=1'b0;" in harness,'native final marker scope changed')
    return source


def audit_saved(root,formal,run):
    review=root/'docs/audits/agent_bridge_2026-11-05/P01/review.json';need(sha(review.read_bytes())==P01_SHA,'independent anchor review hash mismatch')
    anchors=json.loads(review.read_text())['formal_raw_verification']['evidence'];reader=Saved(root,anchors);reader.raw(review)
    checker_path=root/'test2/tasks/axis_length_fifo_v1/reference/frozen-v2/checker.py';reader.raw(checker_path);checker=load_checker(checker_path)
    release=reader.load(run/'release.json')
    for name,h in release['files'].items():need(sha(reader.raw(run/name))==h,'candidate release artifact mismatch')
    finals=reader.load(run/'final-candidates.json')['candidates'];candidates={}
    rounds=reader.load(run/'all-round-candidates.json')['rounds']
    for f in finals:
        d=run/f['directory'];snapfile=d.parent/'snapshot.json';entry=next(x for x in rounds if run/x['snapshot']==snapfile)
        need(sha(reader.raw(snapfile))==entry['sha256'],'final candidate snapshot changed');snap=reader.load(snapfile)
        for name in ('candidate.sv','replay.vvp'):
            p=d/name;need(sha(reader.raw(p))==snap['files'][str(p.relative_to(run))],'candidate artifact changed')
        candidates[f['arm'],f['repetition']]=d
    summary=reader.load(formal/'summary.json');need(summary['release_sha256']==sha(reader.raw(run/'release.json')),'formal release binding')
    jobs=summary['jobs'];keys=[(r['arm'],r['repetition'],r['source'],r['slot'],r['mode']) for r in jobs];need(len(keys)==len(set(keys)),'duplicate native job identity')
    selected=[r for r in jobs if r['status']=='FAIL' and r['mode']=='bmc'];receipts=[];errors=[]
    for row in selected:
        job=formal/row['arm']/('rep'+str(row['repetition']))/row['source']/('P'+str(row['slot'])+'-bmc')
        ident={k:row[k] for k in ('arm','repetition','source','slot','mode')}
        try:
            candidate=candidates[row['arm'],row['repetition']];source=check_native(job,row,reader,candidate)
            expected_source=root/('test2/tasks/axis_length_fifo_v1/public/rtl/axis_frame_length_adjust.v' if row['source']=='correct' else 'test2/tasks/axis_length_done_v1/private/mutants/'+row['source']+'.v')
            need(source==expected_source, 'native source outside registered DUT/mutant identity')
            for dependency in ('work/model/design_prep.ys','work/model/design_smt2.smt2','work/engine_0/logfile.txt'):
                reader.raw(job/dependency)
            for sim in ('iverilog','verilator'):
                cache=formal/'physical-cache'/sha(reader.raw(source))/sim
                binary=cache/('literal.vvp' if sim=='iverilog' else 'obj/Vliteral_replay')
                exe=reader.load(job/'physical'/sim/'execution.json')
                need(exe['argv']==(['vvp',str(binary)] if sim=='iverilog' else [str(binary)])+['+INPUTS='+str(job/'physical'/sim/'inputs.txt')], 'physical binary/source identity mismatch')
                build=reader.load(cache/'compile.json');need(build['status']=='complete' and build['returncode']==0 and str(source) in build['argv'], 'physical compile/source binding mismatch')
                need(build['log_sha256']==sha(reader.raw(cache/'compile.log')), 'physical compile log mismatch')
                reader.raw(cache/'driver.sv');reader.raw(binary)
            receipt,monitor=inspect_chain(job,row['slot'],reader,checker)
            need(str(candidate/'replay.vvp') in monitor['execution']['argv'],'monitor candidate binary identity mismatch')
            need(reader.load(job/'physical/result.json')==row['witness'],'saved witness summary binding mismatch')
            receipts.append(dict(ident,**receipt))
        except (ValueError,KeyError,TypeError,OSError,EOFError,zlib.error) as error:
            errors.append(dict(ident,status='REJECT',error_type=type(error).__name__,reason=str(error)))
    reproduced=[r for r in receipts if r['physical_alarm_reproduced']]
    unrep=[r for r in receipts if not r['physical_alarm_reproduced']]
    return dict(status='REJECT' if errors else 'PASS_CHAIN_CONSISTENCY_WITH_SCIENTIFIC_UNRESOLVED',native_statuses=dict(Counter(r['status'] for r in jobs)),native_bmc_fail_chains=len(selected),chains_consistent=len(receipts),physical_alarm_reproduced=len(reproduced),unreproduced_unresolved=len(unrep),pure_reference_calls=sum(r['pure_reference_rechecked'] for r in receipts),reference_prefix_verdicts=dict(Counter(r['reference_verdict'] for r in reproduced)),unreproduced_by_arm=dict(Counter(r['arm'] for r in unrep)),same_sample_category_confirmed=0,finite_completion_proved=False,candidate_correctness_proved=False,root_cause_of_all_unreproduced='UNDETERMINED',errors=errors,chains=receipts,evidence_sha256=reader.files,independent_anchor_matches=len(set(reader.files)&set(anchors)),additional_hashed_dependencies_without_P01_anchor=sorted(reader.unanchored),claim_scope='Saved raw-chain consistency only. Prefix through post(S-1) does not confirm selected pre(S)/category.74unreproduced are not oracle UNKNOWN or confirmed false alarms.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    out=args.out.resolve();need(out.is_relative_to(ROOT/'test2/results'),'output outside new-result allowlist');out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
    try:result=audit_saved(ROOT,ROOT/'test2/results/controller-done-live-formal-v2',ROOT/'test2/results/controller-done-live-v2')
    except (ValueError,KeyError,TypeError,OSError,EOFError,StopIteration,zlib.error) as error:result=dict(status='REJECT',reason=str(error),error_type=type(error).__name__)
    result.update(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256=sha(Path(__file__).read_bytes()),parse_wall_seconds=time.perf_counter()-start,new_DUT_simulations=0,new_native_formal_jobs=0,new_monitor_replays=0,new_API_calls=0)
    (out/'audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k in ('status','native_bmc_fail_chains','chains_consistent','physical_alarm_reproduced','unreproduced_unresolved','pure_reference_calls','parse_wall_seconds','reason')}));return int(result['status']=='REJECT')


if __name__=='__main__':raise SystemExit(main())
