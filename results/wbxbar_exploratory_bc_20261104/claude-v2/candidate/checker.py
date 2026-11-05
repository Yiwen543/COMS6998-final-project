import collections

W={'i_reset':1,'i_mcyc':1,'i_mstb':1,'i_mwe':1,'i_maddr':8,'i_mdata':32,'i_msel':4,'i_sstall':1,'i_sack':1,'i_sdata':32,'i_serr':1,'o_mstall':1,'o_mack':1,'o_mdata':32,'o_merr':1,'o_scyc':1,'o_sstb':1,'o_swe':1,'o_saddr':8,'o_sdata':32,'o_ssel':4}
CTRL_IN=['i_reset','i_mcyc','i_mstb','i_sstall','i_sack','i_serr']
CTRL_OUT=['o_mstall','o_mack','o_merr','o_scyc','o_sstb']

def _f(pre,k,i):
    v=pre.get(k)
    if v is None:
        return None
    w=W[k]
    return (v>>(i*w))&((1<<w)-1)

def _lm(sel):
    m=0
    for i in range(4):
        if sel is not None and (sel>>i)&1:
            m|=0xff<<(8*i)
    return m

def _weq(d1,d2,sel):
    # write-data equality over SEL-enabled byte lanes only (F6)
    if d1 is None or d2 is None:
        return d1==d2
    m=_lm(sel)
    return (d1&m)==(d2&m)

def _dec(a):
    if a is None:
        return None
    if (a&0xf0)==0x00:
        return 0
    if (a&0xf0)==0x10:
        return 1
    return None

def check_rows(rows):
    failures=[]
    av=[]
    events=[]
    unresolved=[]
    cnt=collections.Counter()
    def fail(c,cat,d):
        failures.append({'cycle':c,'category':cat,'detail':d})
    def asm(c,cat,d):
        av.append({'cycle':c,'category':cat,'detail':d})
    mq=[[],[]]
    sq=[[],[]]
    amb=False
    prev=None
    seen_reset=False
    lastc=None
    if not isinstance(rows,list) or not rows:
        asm(None,'scope','empty or non-list trace')
        rows=[]
    for r in rows:
        if not isinstance(r,dict) or not isinstance(r.get('pre'),dict) or not isinstance(r.get('post'),dict) or not isinstance(r.get('cycle'),int):
            asm(None,'scope','malformed row')
            break
        c=r['cycle']
        pre=r['pre']
        post=r['post']
        if lastc is not None and c!=lastc+1:
            asm(c,'scope','non-contiguous cycle numbering')
            break
        lastc=c
        bad=False
        for k in W:
            if k not in pre:
                asm(c,'scope','missing pre field '+k)
                bad=True
                continue
            v=pre[k]
            n=1 if k=='i_reset' else 2
            if v is not None and (not isinstance(v,int) or v<0 or v>=(1<<(W[k]*n))):
                asm(c,'scope','out-of-range pre field '+k)
                bad=True
        for k in CTRL_IN+CTRL_OUT:
            if k in pre and pre.get(k) is None:
                if k in CTRL_IN:
                    asm(c,'scope','undefined control input '+k)
                else:
                    fail(c,'control','undefined control output '+k)
                bad=True
        if bad:
            break
        if pre['i_reset']&1:
            seen_reset=True
            for m in (0,1):
                if _f(pre,'i_mcyc',m) or _f(pre,'i_mstb',m):
                    asm(c,'reset','master %d CYC/STB active during reset'%m)
                cnt['discarded_by_reset']+=len(mq[m])
            mq=[[],[]]
            sq=[[],[]]
            amb=False
            prev=None
            for k in ('o_scyc','o_sstb'):
                v=post.get(k)
                if v is None or v!=0:
                    fail(c,'reset','post-reset-edge %s not inactive: %r'%(k,v))
            events.append({'family':'reset','kind':'reset_edge','start_cycle':c,'end_cycle':c,'evidence':'i_reset high at rising edge (synchronous)'})
            continue
        if not seen_reset:
            asm(c,'scope','trace does not begin with reset')
            seen_reset=True
        def g(k,i):
            return _f(pre,k,i)
        if prev is not None:
            def p(k,i):
                return _f(prev,k,i)
            for m in (0,1):
                if p('i_mcyc',m) and p('i_mstb',m) and p('o_mstall',m) and g('i_mcyc',m):
                    if (not g('i_mstb',m)) or any(p(k,m)!=g(k,m) for k in ('i_mwe','i_maddr','i_msel')) or (p('i_mwe',m) and not _weq(p('i_mdata',m),g('i_mdata',m),p('i_msel',m))):
                        asm(c,'hold','master %d changed/withdrew stalled request without dropping CYC'%m)
            for s in (0,1):
                if p('o_scyc',s) and p('o_sstb',s) and p('i_sstall',s) and g('o_scyc',s):
                    if (not g('o_sstb',s)) or any(p(k,s)!=g(k,s) for k in ('o_swe','o_saddr','o_ssel')) or (p('o_swe',s) and not _weq(p('o_sdata',s),g('o_sdata',s),p('o_ssel',s))):
                        fail(c,'hold','slave %d stalled request changed/withdrawn without dropping CYC'%s)
        for m in (0,1):
            if g('i_mstb',m) and not g('i_mcyc',m):
                asm(c,'protocol','master %d STB without CYC'%m)
            if g('o_mack',m) and g('o_merr',m):
                fail(c,'protocol','master %d ACK and ERR coincide'%m)
        for s in (0,1):
            if g('o_sstb',s) and not g('o_scyc',s):
                fail(c,'protocol','slave %d STB without CYC'%s)
            if g('i_sack',s) and g('i_serr',s) and g('o_scyc',s):
                asm(c,'protocol','slave %d ACK and ERR coincide'%s)
        for m in (0,1):
            if not g('i_mcyc',m):
                if mq[m]:
                    for e in mq[m]:
                        e['st']='aborted'
                    cnt['aborted']+=len(mq[m])
                    events.append({'family':'abort','kind':'master_cycle_withdrawn','start_cycle':mq[m][0]['acc'],'end_cycle':c,'evidence':'master %d dropped CYC with %d outstanding'%(m,len(mq[m]))})
                mq[m]=[]
            elif g('i_mstb',m) and not g('o_mstall',m):
                we=g('i_mwe',m)
                a=g('i_maddr',m)
                sel=g('i_msel',m)
                d=g('i_mdata',m)
                if we is None or a is None or sel is None or (we and d is None):
                    asm(c,'payload','master %d accepted request with undefined payload'%m)
                mq[m].append({'m':m,'we':we,'a':a,'sel':sel,'d':d,'acc':c,'st':'new','sl':_dec(a),'rd':None,'fc':None,'sc':None})
                cnt['master_accepted']+=1
        for s in (0,1):
            if not g('o_scyc',s):
                for se in sq[s]:
                    for e in (se['own'] or []):
                        if e['st']=='fwd':
                            e['st']='dropped'
                sq[s]=[]
                continue
            if g('o_sstb',s) and not g('i_sstall',s):
                we=g('o_swe',s)
                a=g('o_saddr',s)
                sel=g('o_ssel',s)
                d=g('o_sdata',s)
                if we is None or a is None or sel is None or (we and d is None):
                    fail(c,'payload','slave %d request with undefined payload'%s)
                if _dec(a)!=s:
                    fail(c,'routing','address %r presented to slave %d'%(a,s))
                cnt['slave_accepted']+=1
                if amb:
                    sq[s].append({'own':None})
                    continue
                cands=[]
                for m in (0,1):
                    h=None
                    for e in mq[m]:
                        if e['st']=='new' and e['sl'] is not None:
                            h=e
                            break
                    if h is not None and h['sl']==s and h['we']==we and h['a']==a and h['sel']==sel and ((not we) or _weq(h['d'],d,sel)):
                        cands.append(h)
                if not cands:
                    fail(c,'routing_payload','slave %d accepted request (we=%r,a=%r,sel=%r,d=%r) matching no oldest unforwarded master request: invented, duplicated, reordered or corrupted'%(s,we,a,sel,d))
                    sq[s].append({'own':None})
                elif len(cands)==1:
                    cands[0]['st']='fwd'
                    cands[0]['fc']=c
                    cands[0]['fs']=s
                    sq[s].append({'own':cands})
                    cnt['forwarded']+=1
                else:
                    amb=True
                    unresolved.append({'cycle':c,'item':'ownership_ambiguous','detail':'identical requests from both masters; ownership/data checks suspended until reset'})
                    sq[s].append({'own':None})
        for s in (0,1):
            if not g('o_scyc',s):
                continue
            ack=g('i_sack',s)
            er=g('i_serr',s)
            if ack or er:
                if not sq[s]:
                    if not amb:
                        asm(c,'unsolicited','slave %d response with no outstanding accepted request'%s)
                    continue
                se=sq[s].pop(0)
                if se['own'] is None:
                    continue
                e=se['own'][0]
                if e['st']!='fwd':
                    cnt['orphan_slave_responses_discarded']+=1
                    continue
                e['sc']=c
                if ack and not er:
                    e['st']='sacked'
                    if not e['we']:
                        e['rd']=g('i_sdata',s)
                        if e['rd'] is None:
                            asm(c,'payload','slave %d read ACK with undefined data'%s)
                else:
                    e['st']='serr'
        for m in (0,1):
            if not g('i_mcyc',m):
                continue
            ack=g('o_mack',m)
            er=g('o_merr',m)
            if not (ack or er):
                continue
            if not mq[m]:
                if not amb:
                    fail(c,'invented_response','master %d %s with no outstanding request'%(m,'ACK' if ack else 'ERR'))
                continue
            e=mq[m].pop(0)
            st=e['st']
            e['st']='retired'
            if amb:
                continue
            if ack and not er:
                if st=='sacked':
                    if not e['we']:
                        md=g('o_mdata',m)
                        if md is None or md!=e['rd']:
                            fail(c,'read_data','master %d got %r, slave returned %r'%(m,md,e['rd']))
                    cnt['completed_ok']+=1
                    events.append({'family':'transaction','kind':'write_ok' if e['we'] else 'read_ok','start_cycle':e['acc'],'end_cycle':c,'evidence':'m%d accept@%d slave%d accept@%d slaveACK@%d masterACK@%d'%(m,e['acc'],e.get('fs',-1),e['fc'],e['sc'],c)})
                else:
                    fail(c,'response','master %d ACK but oldest request state is %s (decode error, slave error, dropped, or no slave ACK)'%(m,st))
            else:
                if st=='sacked':
                    fail(c,'response','master %d ERR although slave ACKed oldest request'%m)
                else:
                    if e['sl'] is None or st=='serr':
                        kind='decode_err' if e['sl'] is None else 'slave_err'
                        cnt[kind]+=1
                        events.append({'family':'error','kind':kind,'start_cycle':e['acc'],'end_cycle':c,'evidence':'m%d accept@%d state %s ERR@%d'%(m,e['acc'],st,c)})
                    else:
                        cnt['unexplained_err']+=1
                        unresolved.append({'cycle':c,'item':'unexplained_mapped_err','detail':'m%d accept@%d addr %r slave%r state %s ERR@%d (%d cycles) with no matching slave ERR; timeout/starvation eligibility not established; persists for batch'%(m,e['acc'],e['a'],e['sl'],st,c,c-e['acc'])})
        prev=pre
    pm=sum(len(q) for q in mq)
    ps=sum(1 for q in sq for se in q if se['own'] and se['own'][0]['st']=='fwd')
    cnt['pending_master']=pm
    cnt['pending_slave']=ps
    if pm or ps:
        unresolved.append({'cycle':lastc,'item':'pending_at_batch_end','detail':'%d master-side and %d slave-side obligations outstanding; inconclusive, not a liveness violation'%(pm,ps)})
    fc=[f['cycle'] for f in failures+av if f['cycle'] is not None]
    if any(f['cycle'] is None for f in failures+av):
        events=[]
    events=[e for e in events if not any(e['start_cycle']<=x<=e['end_cycle'] for x in fc)]
    if av:
        verdict='input_or_scope_invalid'
    elif failures:
        verdict='dut_violation'
    elif unresolved:
        verdict='unresolved'
    else:
        verdict='scoped_pass'
    return {'failures':failures,'assumption_violations':av,'events':events,'unresolved':unresolved,'verdict':verdict,'counts':dict(cnt)}


