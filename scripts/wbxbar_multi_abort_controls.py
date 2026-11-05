"""Independent synthetic abort controls; no DUT implementation or live trace inputs."""
import argparse
import copy
import json
from pathlib import Path
from run_midterm_fixed import sha
from wbxbar_checker_controls import empty_rows, put, settle, transfer


def request(rows, cycle, addr, data, master=0, we=1, sel=5):
    for port, width, value in [('i_mcyc',1,1),('i_mstb',1,1),('i_mwe',1,we),
                               ('i_maddr',8,addr),('i_mdata',32,data),('i_msel',4,sel)]:
        put(rows,cycle,port,master,width,value)


def forward(rows, cycle, addr, data, slave=0, we=1, sel=5):
    for port,width,value in [('o_scyc',1,1),('o_sstb',1,1),('o_swe',1,we),
                             ('o_saddr',8,addr),('o_sdata',32,data),('o_ssel',4,sel)]:
        put(rows,cycle,port,slave,width,value)
    put(rows,cycle+1,'o_scyc',slave,1,1)
    put(rows,cycle+1,'i_sack',slave,1,1)


def multi_abort(index=1, master=0, slave=0, count=3, forward_cycle=14, sel=5):
    rows=empty_rows(32)
    for i in range(count):
        request(rows,6+i,16*slave+5+i,0x23456780+i,master=master,sel=sel)
    # At 6+count CYC is withdrawn. Some accepted work may be canceled; observing
    # a residual forward is an unresolved scenario, not a normative valid trace.
    forward(rows,forward_cycle,16*slave+5+index,0x23456780+index,slave=slave,sel=sel)
    return settle(rows)


def additions():
    traces,records={},[]
    def add(name,rows,expect,basis,baseline=None,expose=False):
        traces[name]=settle(rows)
        records.append({'name':name,'expected':expect,'basis':basis,'baseline':baseline,
                        'author_example':expose,'source':'synthetic public-pin scenario; not DUT-derived'})
    for m in (0,1):
        for s in (0,1):
            name=f'multi_abort/m{m}_s{s}_later_identity'
            add(name,multi_abort(master=m,slave=s),'unresolved',
                'CYC withdrawal invalidates outstanding completion. Public authority does not settle partial cancellation or propagation latency; matching residual work must not be called proven invented work.',expose=(m==0 and s==0))
    base='multi_abort/m0_s0_later_identity'
    add('multi_abort/third_identity',multi_abort(index=2),'unresolved','Multiple older accepted requests may remain unobserved; do not assume all survive cancellation.')
    add('multi_abort/late_identity',multi_abort(forward_cycle=23),'unresolved','No new fixed grace period or latency assumption may be invented.')
    add('multi_abort/disabled_byte_change',multi_abort(),'unresolved','A disabled write-byte change does not establish corruption.',base)
    traces['multi_abort/disabled_byte_change'][14]['pre']['o_sdata'] ^= 0xff00
    traces['multi_abort/disabled_byte_change']=settle(traces['multi_abort/disabled_byte_change'])
    add('multi_abort/sel_zero',multi_abort(sel=0),'unresolved','SEL zero does not supply data evidence but retains address/direction/SEL identity.')
    for label,port,value in [('address','o_saddr',12),('enabled_byte','o_sdata',0x23456790),
                             ('direction','o_swe',0),('select','o_ssel',7)]:
        rows=copy.deepcopy(traces[base]);rows[14]['pre'][port]=value
        add('fault/aborted_'+label,rows,'dut_violation','No accepted live or aborted request has this active identity; unresolved abort timing does not forgive corruption.',base,expose=(label=='enabled_byte'))
    rows=copy.deepcopy(traces[base]);forward(rows,18,6,0x23456781)
    add('fault/duplicate_consumed_identity',rows,'dut_violation','An accepted identity cannot justify two downstream accepts.',base)
    rows=multi_abort();rows[11]['pre']['i_reset']=1;rows[12]['pre']['i_reset']=1
    add('fault/reset_then_old_forward',rows,'dut_violation','Reset removes old request identity; it cannot explain post-reset work.',base)
    rows=copy.deepcopy(traces[base]);rows[19]['pre']['i_reset']=1;rows[20]['pre']['i_reset']=1
    add('multi_abort/reset_preserves_prior_uncertainty',rows,'unresolved','Reset clears current identities but cannot erase already observed uncertainty.',base)
    rows=copy.deepcopy(traces[base]);request(rows,12,6,0x23456781,master=1)
    for c in range(13,18):put(rows,c,'i_mcyc',1,1,1)
    add('multi_abort/live_aborted_same_identity',rows,'unresolved','Indistinguishable old and live owners cannot be assigned by guesswork.',base)
    rows=copy.deepcopy(traces[base]);request(rows,7,5,0x23456780)
    # Two old identities are byte-identical: this requires ambiguity accounting.
    rows[14]['pre']['o_saddr']=5;rows[14]['pre']['o_sdata']=0x23456780
    add('multi_abort/identical_aborted_requests',rows,'unresolved','Multiplicity must not be silently collapsed or reused.',base)
    rows=empty_rows(32)
    for i in range(3):request(rows,6+i,5+i,0x23456780+i)
    transfer(rows,accept=18,forward=20,response=21,returned=22,addr=11,we=1,data=0xabcdef01,sel=15)
    add('positive/cancel_all_then_fresh',rows,'scoped_pass','Canceled work is never completed; new distinct work has matching downstream ACK.',expose=True)
    rows=copy.deepcopy(traces['positive/cancel_all_then_fresh']);put(rows,18,'o_mack',0,1,1)
    add('fault/stale_ack_into_fresh',rows,'dut_violation','New request cannot complete before its slave acceptance/response.','positive/cancel_all_then_fresh')
    rows=empty_rows(32)
    transfer(rows,accept=6,forward=10,response=11,returned=12,addr=5,we=1,data=0x23456780,sel=5)
    transfer(rows,accept=7,forward=11,response=12,returned=13,addr=6,we=1,data=0x23456781,sel=5)
    add('positive/live_fifo_order',rows,'scoped_pass','Two distinguishable non-aborted requests forwarded and retired in order.',expose=True)
    rows=copy.deepcopy(traces['positive/live_fifo_order'])
    for port in ('o_swe','o_saddr','o_sdata','o_ssel'):
        rows[10]['pre'][port],rows[11]['pre'][port]=rows[11]['pre'][port],rows[10]['pre'][port]
    add('fault/live_order_swap',rows,'dut_violation','Unaborted ordered traffic must retain existing order checks; cancellation uncertainty cannot be generalized.','positive/live_fifo_order',expose=True)
    rows=empty_rows(32)
    transfer(rows,accept=6,forward=8,response=9,returned=10,addr=5,we=1,data=0x23456780,sel=5,error=True)
    request(rows,7,6,0x23456781);request(rows,10,7,0x23456782)
    # Accept a third request on the same edge as ERR; CYC drops at 11.
    forward(rows,14,7,0x23456782)
    add('multi_abort/accept_same_edge_err',rows,'unresolved','Pre-edge acceptance and error retirement are distinct; later matching buffered work has unsettled abort status.',expose=True)
    rows=copy.deepcopy(traces['multi_abort/accept_same_edge_err']);forward(rows,18,5,0x23456780)
    add('fault/retired_error_identity_reused',rows,'dut_violation','Already forwarded and ERR-retired work cannot be recycled as unforwarded aborted work.','multi_abort/accept_same_edge_err')
    for name,rs in traces.items():
        for i,r in enumerate(rs):
            assert r['cycle']==i
            assert not (r['pre']['i_mstb'] & ~r['pre']['i_mcyc'])
            assert not (r['pre']['o_sstb'] & ~r['pre']['o_scyc'])
    return traces,records


def prepare(parent,output):
    pm=json.loads((parent/'manifest.json').read_text())
    if sha(parent/'private-inputs.json')!=pm['inputs_sha256']:raise ValueError('Historical control drift')
    prior=json.loads((parent/'private-inputs.json').read_text());new,records=additions()
    if set(prior)&set(new):raise ValueError('Control collision')
    output.mkdir(parents=True,exist_ok=False)
    (output/'private-inputs.json').write_text(json.dumps({**prior,**new},separators=(',',':'))+'\n')
    manifest={'parent':str(parent),'parent_inputs_sha256':sha(parent/'private-inputs.json'),
        'inputs_sha256':sha(output/'private-inputs.json'),'builder_sha256':sha(Path(__file__)),
        'historical_controls':pm['controls'],'new_controls':records,
        'counts':{'historical':len(prior),'new':len(new),'total':len(prior)+len(new)},
        'classification_note':'Expectations are integration-role proposed controls, not a new normative specification. Claude independently challenges their validity. Unresolved-baseline fault detection is separate from clean-baseline mutation sensitivity.'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    print(json.dumps(prepare(a.parent.resolve(),a.output.resolve())['counts']))
